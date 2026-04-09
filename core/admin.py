from django.contrib import admin
from .models import Teacher, Student, ClassSchedule, Notification, DailyClassStatus, StudentAttendance

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_id', 'is_first_login')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number')
    search_fields = ('name', 'roll_number')

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'day', 'start_time', 'end_time', 'is_active')
    list_filter = ('day', 'is_active', 'teacher')

admin.site.register(Notification)

@admin.register(DailyClassStatus)
class DailyClassStatusAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date', 'status')
    list_filter = ('date', 'status')

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'daily_class', 'is_present')
    list_filter = ('is_present', 'daily_class__date')
