from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Teacher, Student, ClassSchedule, DailyClassStatus, StudentAttendance, Notification
import csv

def is_admin(user):
    return user.is_authenticated and user.is_superuser

# ----------------- Authentication -----------------

def portal_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('portal_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('portal_dashboard')
        else:
            messages.error(request, "Invalid Admin Credentials.")
            
    return render(request, 'portal/login.html')

def portal_logout(request):
    logout(request)
    return redirect('portal_login')

# ----------------- Dashboard -----------------

@user_passes_test(is_admin, login_url='portal_login')
def portal_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = ClassSchedule.objects.count()
    
    today = timezone.now().date()
    active_classes_today = DailyClassStatus.objects.filter(date=today, status=True).count()
    cancelled_classes_today = DailyClassStatus.objects.filter(date=today, status=False, is_started=True).count()
    
    recent_notifications = Notification.objects.all().order_by('-timestamp')[:5]
    recent_attendance = StudentAttendance.objects.all().order_by('-id')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'active_classes_today': active_classes_today,
        'cancelled_classes_today': cancelled_classes_today,
        'recent_notifications': recent_notifications,
        'recent_attendance': recent_attendance,
        'current_path': 'dashboard',
    }
    return render(request, 'portal/dashboard.html', context)

# ----------------- Student Management -----------------

@user_passes_test(is_admin, login_url='portal_login')
def portal_students(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            roll_number = request.POST.get('roll_number')
            name = request.POST.get('name')
            section = request.POST.get('section')
            email = request.POST.get('email')
            password = request.POST.get('password') # In a real app, hash this properly
            Student.objects.create(roll_number=roll_number, name=name, section=section, email=email, password=password)
            messages.success(request, "Student added successfully.")
        elif action == 'edit':
            student_id = request.POST.get('student_id')
            student = get_object_or_404(Student, id=student_id)
            student.name = request.POST.get('name')
            student.section = request.POST.get('section')
            student.email = request.POST.get('email')
            student.is_active = request.POST.get('is_active') == 'on'
            student.save()
            messages.success(request, "Student updated successfully.")
        elif action == 'delete':
            student_id = request.POST.get('student_id')
            Student.objects.filter(id=student_id).delete()
            messages.success(request, "Student deleted successfully.")
        return redirect('portal_students')

    students = Student.objects.all().order_by('roll_number')
    context = {'students': students, 'current_path': 'students'}
    return render(request, 'portal/students.html', context)

# ----------------- Teacher Management -----------------

@user_passes_test(is_admin, login_url='portal_login')
def portal_teachers(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name')
            teacher_id = request.POST.get('teacher_id')
            email = request.POST.get('email')
            Teacher.objects.create(name=name, teacher_id=teacher_id, email=email)
            messages.success(request, "Teacher added successfully.")
        elif action == 'edit':
            t_id = request.POST.get('id')
            teacher = get_object_or_404(Teacher, id=t_id)
            teacher.name = request.POST.get('name')
            teacher.email = request.POST.get('email')
            teacher.is_active = request.POST.get('is_active') == 'on'
            teacher.save()
            messages.success(request, "Teacher updated successfully.")
        elif action == 'delete':
            t_id = request.POST.get('id')
            Teacher.objects.filter(id=t_id).delete()
            messages.success(request, "Teacher deleted successfully.")
        return redirect('portal_teachers')

    teachers = Teacher.objects.all().order_by('name')
    context = {'teachers': teachers, 'current_path': 'teachers'}
    return render(request, 'portal/teachers.html', context)

# ----------------- Schedule Management -----------------

@user_passes_test(is_admin, login_url='portal_login')
def portal_schedules(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            teacher_id = request.POST.get('teacher_id')
            subject = request.POST.get('subject')
            room_number = request.POST.get('room_number')
            day = request.POST.get('day')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            section = request.POST.get('target_section')
            
            # Simple conflict detection could go here
            ClassSchedule.objects.create(
                teacher_id=teacher_id, subject=subject, room_number=room_number,
                day=day, start_time=start_time, end_time=end_time, target_section=section
            )
            messages.success(request, "Schedule added successfully.")
        elif action == 'delete':
            s_id = request.POST.get('id')
            ClassSchedule.objects.filter(id=s_id).delete()
            messages.success(request, "Schedule deleted successfully.")
        return redirect('portal_schedules')

    schedules = ClassSchedule.objects.all().select_related('teacher').order_by('day', 'start_time')
    teachers = Teacher.objects.filter(is_active=True)
    context = {
        'schedules': schedules, 
        'teachers': teachers, 
        'days': ClassSchedule.DAYS_OF_WEEK,
        'current_path': 'schedules'
    }
    return render(request, 'portal/schedules.html', context)

# ----------------- Attendance Management -----------------

@user_passes_test(is_admin, login_url='portal_login')
def portal_attendance(request):
    records = StudentAttendance.objects.all().select_related('student', 'daily_class__schedule').order_by('-daily_class__date')
    context = {'records': records, 'current_path': 'attendance'}
    return render(request, 'portal/attendance.html', context)

@user_passes_test(is_admin, login_url='portal_login')
def portal_attendance_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Student', 'Roll No', 'Section', 'Subject', 'Teacher', 'Status'])
    
    records = StudentAttendance.objects.all().select_related('student', 'daily_class__schedule').order_by('-daily_class__date')
    for r in records:
        writer.writerow([
            r.daily_class.date, r.student.name, r.student.roll_number,
            r.student.section, r.daily_class.schedule.subject,
            r.daily_class.schedule.teacher.name,
            'Present' if r.is_present else 'Absent'
        ])
    return response

# ----------------- Notifications -----------------

@user_passes_test(is_admin, login_url='portal_login')
def portal_notifications(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        target = request.POST.get('target') # 'all', 'students', 'teachers', 'section_a', 'section_b'
        
        # In current models, Notification isn't explicitly targeted globally, it relies on Schedule.
        # We can just create a general notification with null schedule.
        Notification.objects.create(message=f"[{target.upper()}] {message}")
        messages.success(request, "Notification broadcasted successfully.")
        return redirect('portal_notifications')

    notifications = Notification.objects.all().order_by('-timestamp')
    context = {'notifications': notifications, 'current_path': 'notifications'}
    return render(request, 'portal/notifications.html', context)
