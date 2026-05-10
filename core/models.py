from django.db import models
from django.utils import timezone

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_first_login = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    roll_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    section = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], default='A')
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class ClassSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules')
    subject = models.CharField(max_length=100)
    room_number = models.CharField(max_length=50)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    target_section = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], default='A')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject} - {self.day} {self.start_time.strftime('%H:%M')}"

class Notification(models.Model):
    schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.message}"
    
    class Meta:
        ordering = ['-timestamp']

class DailyClassStatus(models.Model):
    schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='daily_statuses')
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False) # False = Waiting / Cancelled, True = Active
    is_started = models.BooleanField(default=False) # False = Never turned on (WAITING)

    class Meta:
        unique_together = ('schedule', 'date')

    def __str__(self):
        return f"{self.schedule.subject} on {self.date} - {'Active' if self.status else 'Cancelled'}"

class StudentAttendance(models.Model):
    daily_class = models.ForeignKey(DailyClassStatus, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('daily_class', 'student')

    def __str__(self):
        return f"{self.student.name} - {'Present' if self.is_present else 'Absent'}"
