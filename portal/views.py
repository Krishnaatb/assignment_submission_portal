from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, Notice
from django.utils import timezone

def home(request):
    return render(request, 'portal/home.html')

def domain_role(request, role):
    if request.method == 'POST':
        request.session['domain'] = request.POST['domain']
        request.session['role'] = role
        return redirect('login')
    return render(request, 'portal/domain.html', {'role': role})

def login_view(request):
    role = request.session.get('role')
    domain = request.session.get('domain')
    
    if request.method == 'POST':
        # Flowchart Step: Separate Logins
        if role == 'Teacher':
            # Teacher Login Logic (Email/Password simulation)
            email = request.POST.get('email')
            # In a real app, authenticate here.
            request.session['user_id'] = email 
            return redirect('teacher_dashboard')
        else:
            # Student Login Logic (Student ID/Password simulation)
            student_id = request.POST.get('student_id')
            request.session['user_id'] = student_id
            return redirect('student_dashboard')
            
    return render(request, 'portal/login.html', {'role': role})

# --- Teacher Views ---

def teacher_dashboard(request):
    domain = request.session.get('domain')
    # Show notices created for this domain
    teacher_email = request.session.get('user_id')
    notices = Notice.objects.filter(domain=domain, teacher_email=teacher_email).order_by('-created_at')
    
    # Get unique students who have submitted to these notices
    submitted_assignments = Assignment.objects.filter(notice__in=notices)
    unique_students = {}
    for asn in submitted_assignments:
        if asn.student_id not in unique_students:
            unique_students[asn.student_id] = asn.student_name
            
    # Convert to list of dicts for template
    students_list = [{'id': sid, 'name': name} for sid, name in unique_students.items()]
    
    return render(request, 'portal/teacher_dashboard.html', {
        'notices': notices,
        'domain': domain,
        'students': students_list
    })

def create_notice(request):
    if request.method == 'POST':
        Notice.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            due_date=request.POST['due_date'],
            domain=request.session.get('domain'),
            teacher_email=request.session.get('user_id')
        )
        return redirect('teacher_dashboard')
    return redirect('teacher_dashboard')

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    
    # Permission Check
    role = request.session.get('role')
    user_id = request.session.get('user_id')
    
    if role == 'Teacher':
        if notice.teacher_email != user_id:
             # Unauthorized access for this teacher
             return redirect('teacher_dashboard')
             
    assignments = notice.assignments.all()
    return render(request, 'portal/notice_detail.html', {
        'notice': notice,
        'assignments': assignments
    })

def grade_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Permission Check
    if request.session.get('role') == 'Teacher':
        if assignment.notice.teacher_email != request.session.get('user_id'):
            return redirect('teacher_dashboard')

    if request.method == 'POST':
        assignment.grade = request.POST['grade']
        assignment.review = request.POST['review']
        assignment.save()
        return redirect('notice_detail', notice_id=assignment.notice.id)
    return redirect('teacher_dashboard')

# --- Student Views ---

def student_dashboard(request):
    domain = request.session.get('domain')
    student_id = request.session.get('user_id')
    
    # Available notices
    notices = Notice.objects.filter(domain=domain, due_date__gte=timezone.now().date())
    
    # My submissions
    my_submissions = Assignment.objects.filter(student_id=student_id)
    
    return render(request, 'portal/student_dashboard.html', {
        'notices': notices,
        'submissions': my_submissions,
        'student_id': student_id
    })

def submit_assignment(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        Assignment.objects.create(
            notice=notice,
            student_name=request.POST['student_name'],
            student_id=request.session.get('user_id'),
            file=request.FILES['file'],
        )
        return redirect('student_dashboard')
    
    return render(request, 'portal/submit.html', {'notice': notice})

