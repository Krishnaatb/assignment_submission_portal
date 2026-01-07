from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/', views.domain_role, {'role':'Teacher'}, name='teacher'),
    path('student/', views.domain_role, {'role':'Student'}, name='student'),
    path('login/', views.login_view, name='login'),
    
    # Teacher Routes
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('create-notice/', views.create_notice, name='create_notice'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('assignment/<int:assignment_id>/grade/', views.grade_assignment, name='grade_assignment'),

    # Student Routes
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('submit/<int:notice_id>/', views.submit_assignment, name='submit_assignment'),
]
