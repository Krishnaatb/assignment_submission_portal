from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    domain = models.CharField(max_length=50) # AI, CSE, etc.
    teacher = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='notices', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='assignments')
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    file = models.FileField(upload_to='assignments/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Grading fields
    grade = models.CharField(max_length=10, blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_name} - {self.notice.title}"
