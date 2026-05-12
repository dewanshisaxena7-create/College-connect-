from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Teacher, Student, ClassSchedule, Notification, DailyClassStatus, StudentAttendance
import json

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'teacher_id' not in request.session:
            return redirect('teacher_login')
        try:
            Teacher.objects.get(id=request.session['teacher_id'])
        except Teacher.DoesNotExist:
            request.session.flush()
            return redirect('teacher_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'student_id' not in request.session:
            return redirect('student_login')
        try:
            Student.objects.get(id=request.session['student_id'])
        except Student.DoesNotExist:
            request.session.flush()
            return redirect('student_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def index_view(request):
    if 'teacher_id' in request.session:
        try:
            Teacher.objects.get(id=request.session['teacher_id'])
            return redirect('teacher_dashboard')
        except Teacher.DoesNotExist:
            request.session.flush()
    if 'student_id' in request.session:
        try:
            Student.objects.get(id=request.session['student_id'])
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            request.session.flush()
    return render(request, 'unified_login.html')

def student_login_view(request):
    if 'student_id' in request.session:
        try:
            Student.objects.get(id=request.session['student_id'])
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            request.session.flush()
    error_msg = None
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        roll_number = request.POST.get('roll_number', '').strip().upper()
        try:
            student = Student.objects.get(roll_number__iexact=roll_number)
            if student.name.lower() == name.lower():
                if check_password(roll_number, student.password):
                    request.session['student_id'] = student.id
                    return redirect('student_dashboard')
                else:
                    error_msg = "Invalid roll number."
            else:
                error_msg = "Name and Roll Number do not match."
        except Student.DoesNotExist:
            error_msg = "Student record not found."
    return render(request, 'unified_login.html', {'student_error': error_msg, 'active_tab': 'student'})

def teacher_login_view(request):
    if 'teacher_id' in request.session:
        try:
            Teacher.objects.get(id=request.session['teacher_id'])
            return redirect('teacher_dashboard')
        except Teacher.DoesNotExist:
            request.session.flush()
    error_msg = None
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        password = request.POST.get('password', '')
        try:
            teacher = Teacher.objects.get(teacher_id__iexact=teacher_id)
            if teacher.is_first_login:
                if not teacher.email:
                    error_msg = "Please contact the administrator to add an email address to your account before logging in."
                else:
                    # Generate 4-digit OTP
                    otp = get_random_string(length=4, allowed_chars='0123456789')
                    teacher.otp = otp
                    teacher.save()
                    
                    # Send Email
                    subject = 'College Connect - Account Setup Verification'
                    message = f'Hello {teacher.name},\n\nWelcome to College Connect!\nYour OTP to verify your account and set up your password is {otp}.\nPlease use this to complete your setup.'
                    send_mail(subject, message, None, [teacher.email], fail_silently=False)
                    
                    request.session['reset_teacher_id'] = teacher.id
                    return redirect('verify_otp')
            else:
                if check_password(password, teacher.password):
                    request.session['teacher_id'] = teacher.id
                    return redirect('teacher_dashboard')
                else:
                    error_msg = "Invalid teacher credentials."
        except Teacher.DoesNotExist:
            error_msg = "Invalid teacher credentials."
    return render(request, 'unified_login.html', {'teacher_error': error_msg, 'active_tab': 'teacher'})

def teacher_setup_view(request):
    if 'setup_teacher_id' not in request.session:
        return redirect('teacher_login')
        
    teacher = Teacher.objects.get(id=request.session['setup_teacher_id'])
    error_msg = None
    
    if request.method == 'POST':
        new_username = request.POST.get('new_username', '').strip()
        email = request.POST.get('email', '').strip()
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            # Check if Username is already taken
            if new_username and Teacher.objects.filter(teacher_id__iexact=new_username).exclude(id=teacher.id).exists():
                error_msg = "This username is already taken. Please choose another one."
            # Check if Email is already taken
            elif email and Teacher.objects.filter(email__iexact=email).exclude(id=teacher.id).exists():
                error_msg = "This email is already registered to another teacher."
            else:
                teacher.password = make_password(new_password)
                if email:
                    teacher.email = email
                if new_username:
                    teacher.teacher_id = new_username
                teacher.is_first_login = False
                teacher.save()
                
                request.session['teacher_id'] = teacher.id
                del request.session['setup_teacher_id']
                return redirect('teacher_dashboard')
        else:
            error_msg = "Passwords do not match."
            
    days = ClassSchedule.DAYS_OF_WEEK
    return render(request, 'teacher_setup.html', {'error': error_msg, 'days': days, 'teacher': teacher})

def forgot_password_view(request):
    error_msg = None
    success_msg = None
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        email = request.POST.get('email')
        
        try:
            teacher = Teacher.objects.get(teacher_id__iexact=teacher_id, email__iexact=email)
            
            # Generate 4-digit OTP
            otp = get_random_string(length=4, allowed_chars='0123456789')
            teacher.otp = otp
            teacher.save()
            
            # Send Email
            subject = 'College Connect - Password Reset OTP'
            message = f'Hello {teacher.name},\n\nYour OTP for password reset is {otp}.\nPlease use this to reset your password.'
            send_mail(subject, message, None, [teacher.email], fail_silently=False)
            
            request.session['reset_teacher_id'] = teacher.id
            return redirect('verify_otp')
            
        except Teacher.DoesNotExist:
            error_msg = "Invalid Teacher ID or Email."
            
    return render(request, 'forgot_password.html', {'error': error_msg, 'success': success_msg})

def verify_otp_view(request):
    error_msg = None
    success_msg = None
    teacher_id_val = ""
    is_first_login = False
    
    if 'reset_teacher_id' in request.session:
        try:
            tea = Teacher.objects.get(id=request.session['reset_teacher_id'])
            teacher_id_val = tea.teacher_id
            is_first_login = tea.is_first_login
        except Teacher.DoesNotExist:
            pass

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        try:
            teacher = Teacher.objects.get(teacher_id__iexact=teacher_id)
            if teacher.otp and teacher.otp == otp:
                if new_password and new_password == confirm_password:
                    teacher.password = make_password(new_password)
                    teacher.otp = None
                    if teacher.is_first_login:
                        teacher.is_first_login = False
                        success_msg_text = "Account setup complete! You can now log in."
                    else:
                        success_msg_text = "Password reset successfully! You can now log in."
                    teacher.save()
                    if 'reset_teacher_id' in request.session:
                        del request.session['reset_teacher_id']
                    return render(request, 'forgot_password.html', {'success': success_msg_text})
                else:
                    error_msg = "Passwords do not match."
                    teacher_id_val = teacher_id
            else:
                error_msg = "Invalid OTP."
                teacher_id_val = teacher_id
        except Teacher.DoesNotExist:
            error_msg = "Invalid Teacher ID."
            teacher_id_val = teacher_id
            
    return render(request, 'verify_otp.html', {'error': error_msg, 'teacher_id_val': teacher_id_val, 'is_first_login': is_first_login})

@teacher_required
def change_password_view(request):
    error_msg = None
    success_msg = None
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.session['teacher_id'])
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(old_password, teacher.password):
            if new_password and new_password == confirm_password:
                teacher.password = make_password(new_password)
                teacher.save()
                success_msg = "Password changed successfully!"
            else:
                error_msg = "New passwords do not match."
        else:
            error_msg = "Incorrect old password."
            
    return render(request, 'change_password.html', {'error': error_msg, 'success': success_msg})

def logout_view(request):
    request.session.flush()
    return redirect('index')

@teacher_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(id=request.session['teacher_id'])
    today_name = timezone.localtime().strftime('%A')
    today_date = timezone.localtime().date()
    
    # Get today's classes
    schedules = ClassSchedule.objects.filter(teacher=teacher, day=today_name).order_by('start_time')
    
    active_schedules_data = []
    history_schedules_data = []
    
    current_time = timezone.localtime().time()
    for s in schedules:
        daily_status, _ = DailyClassStatus.objects.get_or_create(
            schedule=s, date=today_date, defaults={'status': False}
        )
        data = {
            'schedule': s,
            'daily_status': daily_status
        }
        if current_time > s.end_time:
            history_schedules_data.append(data)
        else:
            active_schedules_data.append(data)
        
    # Analytics Calculations
    total_today = schedules.count()
    all_today_data = active_schedules_data + history_schedules_data
    conducted_today = sum(1 for item in all_today_data if item['daily_status'].status)
    cancelled_today = sum(1 for item in all_today_data if not item['daily_status'].status and item['daily_status'].is_started)
    
    week_ago = today_date - timezone.timedelta(days=7)
    weekly_statuses = DailyClassStatus.objects.filter(
        schedule__teacher=teacher,
        date__gte=week_ago,
        date__lte=today_date
    )
    weekly_on = weekly_statuses.filter(status=True).count()
    weekly_off = weekly_statuses.filter(status=False).count()
    
    # Fetch all schedules to show the teacher their complete timetable
    all_schedules = ClassSchedule.objects.filter(teacher=teacher).order_by('day', 'start_time')
    
    context = {
        'teacher': teacher,
        'today': today_name,
        'active_schedules_data': active_schedules_data,
        'history_schedules_data': history_schedules_data,
        'all_schedules': all_schedules,
        'days': ClassSchedule.DAYS_OF_WEEK,
        'analytics': {
            'total': total_today,
            'conducted': conducted_today,
            'cancelled': cancelled_today,
            'weekly_on': weekly_on,
            'weekly_off': weekly_off
        }
    }
    return render(request, 'teacher_dashboard.html', context)

@teacher_required
def add_schedule(request):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.session['teacher_id'])
        subject = request.POST.get('subject')
        room_number = request.POST.get('room_number')
        day = request.POST.get('day', timezone.localtime().strftime('%A'))
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        target_section = request.POST.get('target_section', 'A')
        
        ClassSchedule.objects.create(
            teacher=teacher, subject=subject, room_number=room_number,
            day=day, start_time=start_time, end_time=end_time,
            target_section=target_section
        )
    return redirect('teacher_dashboard')

@student_required
def student_dashboard(request):
    student = Student.objects.get(id=request.session['student_id'])
    today_name = timezone.localtime().strftime('%A')
    
    context = {
        'student': student,
        'today': today_name
    }
    return render(request, 'student_dashboard.html', context)

@teacher_required
def api_toggle_class(request, schedule_id):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.session['teacher_id'])
        schedule = get_object_or_404(ClassSchedule, id=schedule_id, teacher=teacher)
        today_date = timezone.localtime().date()
        daily_status, _ = DailyClassStatus.objects.get_or_create(
            schedule=schedule, date=today_date, defaults={'status': False}
        )
        
        try:
            data = json.loads(request.body)
            new_status = data.get('is_active', True)
        except:
            new_status = not daily_status.status
            
        daily_status.status = new_status
        daily_status.is_started = True
        daily_status.save()
        
        # Create a notification
        status_text = "ON" if new_status else "CANCELLED"
        msg = f"Class '{schedule.subject}' scheduled for {schedule.start_time.strftime('%H:%M')} today is now {status_text}."
        Notification.objects.create(schedule=schedule, message=msg)
        
        return JsonResponse({'success': True, 'is_active': daily_status.status, 'daily_class_id': daily_status.id})
        
    return JsonResponse({'success': False}, status=403)

@teacher_required
def take_attendance_view(request, daily_class_id):
    teacher = Teacher.objects.get(id=request.session['teacher_id'])
    daily_class = get_object_or_404(DailyClassStatus, id=daily_class_id, schedule__teacher=teacher)
    
    if request.method == 'POST':
        present_student_ids = []
        for key in request.POST:
            if key.startswith('student_'):
                student_id = key.split('_')[1]
                present_student_ids.append(int(student_id))
        
        # Save all checked students as present, others as absent
        students = Student.objects.all()
        for student in students:
            is_present = student.id in present_student_ids
            att, _ = StudentAttendance.objects.get_or_create(daily_class=daily_class, student=student)
            att.is_present = is_present
            att.save()
            
        return redirect('teacher_dashboard')
        
    # Filtering students based on the schedule's target section
    target_sec = daily_class.schedule.target_section
    students_in_section = list(Student.objects.filter(section=target_sec))
    
    def extract_roll_number_int(student):
        try:
            return int(student.roll_number.split('-')[-1])
        except (ValueError, IndexError):
            return 9999
            
    students_in_section.sort(key=extract_roll_number_int)
    
    attendances = StudentAttendance.objects.filter(daily_class=daily_class)
    present_ids = [att.student.id for att in attendances if att.is_present]
    
    return render(request, 'take_attendance.html', {
        'daily_class': daily_class,
        'students': students_in_section,
        'target_section': target_sec,
        'present_ids': present_ids
    })

@teacher_required
def view_attendance_report(request):
    teacher = Teacher.objects.get(id=request.session['teacher_id'])
    
    # All subjects ever taught by this teacher
    subjects = ClassSchedule.objects.filter(teacher=teacher).values_list('subject', flat=True).distinct()
    
    subject_filter = request.GET.get('subject')
    
    if not subject_filter:
        return render(request, 'view_attendance.html', {
            'subjects': subjects,
            'selected_subject': None
        })
        
    def extract_roll_number_int(student):
        try:
            return int(student.roll_number.split('-')[-1])
        except (ValueError, IndexError):
            return 9999
            
    # Get all students and sort purely in memory by section then numerical roll
    students = list(Student.objects.all())
    students.sort(key=lambda s: (s.section, extract_roll_number_int(s)))
    
    # Calculate stats
    report_data = []
    # Only consider classes taught by this teacher for the SPECIFIC subject
    teacher_classes = DailyClassStatus.objects.filter(schedule__teacher=teacher, schedule__subject=subject_filter)
    
    for s in students:
        total_records = StudentAttendance.objects.filter(student=s, daily_class__in=teacher_classes).count()
        attended = StudentAttendance.objects.filter(student=s, daily_class__in=teacher_classes, is_present=True).count()
        
        report_data.append({
            'student': s,
            'total': total_records,
            'attended': attended
        })
        
    return render(request, 'view_attendance.html', {
        'report_data': report_data,
        'selected_subject': subject_filter,
        'subjects': subjects
    })

@student_required
def api_student_data(request):
    """Returns today's active schedule and latest notifications based on section."""
    student = Student.objects.get(id=request.session['student_id'])
    today_name = timezone.localtime().strftime('%A')
    today_date = timezone.localtime().date()
    
    # Use the student's official section from the database
    real_section = student.section

    # Active timetables for today for this specific section
    schedules = ClassSchedule.objects.filter(day=today_name, target_section=real_section).order_by('start_time')
    
    classes_data = []
    for s in schedules:
        # Hide classes only after 30 mins past end_time
        end_datetime = timezone.localtime().replace(hour=s.end_time.hour, minute=s.end_time.minute)
        grace_time = end_datetime + timezone.timedelta(minutes=30)
        
        if timezone.localtime() > grace_time:
            continue
            
        daily_status, _ = DailyClassStatus.objects.get_or_create(
            schedule=s, date=today_date, defaults={'status': False}
        )
        has_self_marked = StudentAttendance.objects.filter(student=student, daily_class=daily_status, is_present=True).exists()
        
        # Determine explicit UI status
        if daily_status.status:
            ui_status = "ON"
        elif daily_status.is_started:
            ui_status = "CANCELLED"
        else:
            ui_status = "WAITING"

        classes_data.append({
            'daily_class_id': daily_status.id,
            'subject_name': s.subject,
            'teacher_name': s.teacher.name,
            'time': f"{s.start_time.strftime('%H:%M')} - {s.end_time.strftime('%H:%M')}",
            'room_number': s.room_number,
            'is_active': daily_status.status,
            'ui_status': ui_status,
            'target_section': s.target_section
        })
        
    # Latest notifications across matching schedules
    recent_schedules = ClassSchedule.objects.filter(target_section=real_section)
    notifications = Notification.objects.filter(schedule__in=recent_schedules).order_by('-timestamp')[:10]
    
    notif_data = []
    for n in notifications:
        diff = timezone.now() - n.timestamp
        total_mins = int(diff.total_seconds() // 60)
        
        if total_mins < 1:
            time_str = "Just now"
        elif total_mins < 60:
            time_str = f"{total_mins} mins ago"
        elif total_mins < 1440:
            hours = total_mins // 60
            time_str = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            days = total_mins // 1440
            time_str = f"{days} day{'s' if days > 1 else ''} ago"

        notif_data.append({
            'message': n.message,
            'time': time_str,
            'subject': n.schedule.subject if n.schedule else 'General',
            'is_upcoming': False
        })
        
    # Dynamically inject upcoming class if starting within the next 60 minutes
    now = timezone.localtime()
    for s in schedules:
        class_datetime = timezone.localtime().replace(hour=s.start_time.hour, minute=s.start_time.minute, second=0, microsecond=0)
        diff_mins = (class_datetime - now).total_seconds() / 60.0
        # If class starts within 60 mins, AND it hasn't ended yet
        if 0 < diff_mins <= 60:
            notif_data.insert(0, {
                'message': f"Next class '{s.subject}' starts in {int(diff_mins)} minutes in Room {s.room_number}.",
                'time': 'Upcoming',
                'subject': s.subject,
                'is_upcoming': True
            })
            break # Only show the absolute next one
        
    # Calculate Student's Personal Attendance Stats
    total_classes = StudentAttendance.objects.filter(student=student).count()
    attended_classes = StudentAttendance.objects.filter(student=student, is_present=True).count()
        
    # Fetch Personal Attendance History
    # Aggregate Attendance History by Subject
    history_data = []
    
    # Get all classes for the student's section up to today that were ACTIVE
    past_active_classes = DailyClassStatus.objects.filter(
        schedule__target_section=real_section,
        status=True,
    )
    
    # Unique subjects currently scheduled
    subjects = past_active_classes.values_list('schedule__subject', flat=True).distinct()
    
    for sub in subjects:
        total_sub_classes = past_active_classes.filter(schedule__subject=sub).count()
        attended_sub_classes = StudentAttendance.objects.filter(
            student=student, 
            daily_class__schedule__subject=sub, 
            is_present=True
        ).count()
        
        history_data.append({
            'date': 'Total',
            'subject': sub,
            'status': f'{attended_sub_classes} out of {total_sub_classes} classes attended',
            'attended': attended_sub_classes,
            'total': total_sub_classes
        })
        
    # Also fetch specifically today's attendance so they can see immediate feedback
    today_records = StudentAttendance.objects.filter(student=student, daily_class__date=today_date)
    today_data = []
    for r in today_records:
        today_data.append({
            'date': r.daily_class.date.strftime('%Y-%m-%d'),
            'subject': r.daily_class.schedule.subject,
            'status': 'Present' if r.is_present else 'Absent'
        })
        
    return JsonResponse({
        'classes': classes_data,
        'notifications': notif_data,
        'attendance_stats': {
            'total': total_classes,
            'attended': attended_classes
        },
        'attendance_history': history_data,
        'today_attendance': today_data
    })

# Removed api_self_mark_attendance as per user request (Only Teacher marks attendance)

@student_required
def api_clear_notifications(request):
    if request.method == 'POST':
        Notification.objects.all().delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)

@teacher_required
def api_clear_schedules(request):
    """Deletes ALL Master Weekly schedules."""
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.session['teacher_id'])
        ClassSchedule.objects.filter(teacher=teacher).delete()
        return redirect('teacher_dashboard')
    return redirect('teacher_dashboard')

@teacher_required
def api_clear_today(request):
    """Deletes TODAY'S one-off active classes."""
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.session['teacher_id'])
        today_date = timezone.localtime().date()
        # Delete only today's DailyClassStatus for this teacher
        DailyClassStatus.objects.filter(schedule__teacher=teacher, date=today_date).delete()
        # Also clean up the master schedule if they use this system entirely "at the moment"
        # Since they "make schedule at the moment only", deleting today means 
        # wiping out the ClassSchedule entries made today for today.
        today_name = timezone.localtime().strftime('%A')
        ClassSchedule.objects.filter(teacher=teacher, day=today_name).delete()
        return redirect('teacher_dashboard')
    return redirect('teacher_dashboard')

@teacher_required
def api_delete_schedule(request, schedule_id):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.session['teacher_id'])
        schedule = get_object_or_404(ClassSchedule, id=schedule_id, teacher=teacher)
        schedule.delete()
        return redirect('teacher_dashboard')
    return redirect('teacher_dashboard')


@teacher_required
def api_export_attendance(request):
    import csv
    from django.http import HttpResponse
    teacher = Teacher.objects.get(id=request.session['teacher_id'])
    subject_filter = request.GET.get('subject')
    if not subject_filter:
        return redirect('view_attendance_report')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{subject_filter}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Roll Number', 'Name', 'Section', 'Classes Attended', 'Total Conducted', 'Percentage'])
    
    students = list(Student.objects.all())
    def extract_roll_number_int(student):
        try:
            return int(student.roll_number.split('-')[-1])
        except:
            return 9999
    students.sort(key=lambda s: (s.section, extract_roll_number_int(s)))
    teacher_classes = DailyClassStatus.objects.filter(schedule__teacher=teacher, schedule__subject=subject_filter)
    for s in students:
        total = StudentAttendance.objects.filter(student=s, daily_class__in=teacher_classes).count()
        attended = StudentAttendance.objects.filter(student=s, daily_class__in=teacher_classes, is_present=True).count()
        pct = f'{int((attended/total)*100)}%' if total > 0 else 'N/A'
        writer.writerow([s.roll_number, s.name, s.section, attended, total, pct])
    return response



@teacher_required
def api_edit_schedule(request, schedule_id):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.session['teacher_id'])
        schedule = get_object_or_404(ClassSchedule, id=schedule_id, teacher=teacher)
        
        schedule.subject = request.POST.get('edit_subject', schedule.subject)
        schedule.room_number = request.POST.get('edit_room_number', schedule.room_number)
        schedule.day = request.POST.get('edit_day', schedule.day)
        schedule.start_time = request.POST.get('edit_start_time', schedule.start_time)
        schedule.end_time = request.POST.get('edit_end_time', schedule.end_time)
        schedule.target_section = request.POST.get('edit_target_section', schedule.target_section)
        schedule.save()
        
    return redirect('teacher_dashboard')

