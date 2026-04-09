from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('student/login/', views.student_login_view, name='student_login'),
    path('teacher/login/', views.teacher_login_view, name='teacher_login'),
    path('teacher/setup/', views.teacher_setup_view, name='teacher_setup'),
    path('teacher/forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('teacher/verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('teacher/change-password/', views.change_password_view, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/attendance/<int:daily_class_id>/', views.take_attendance_view, name='take_attendance'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    
    path('student/', views.student_dashboard, name='student_dashboard'),
    
    path('api/toggle_class/<int:schedule_id>/', views.api_toggle_class, name='api_toggle_class'),
    path('api/student_data/', views.api_student_data, name='api_student_data'),
    path('api/clear_notifications/', views.api_clear_notifications, name='api_clear_notifications'),
    path('api/clear_schedules/', views.api_clear_schedules, name='api_clear_schedules'),
    path('api/clear_today/', views.api_clear_today, name='api_clear_today'),
    path('api/delete_schedule/<int:schedule_id>/', views.api_delete_schedule, name='api_delete_schedule'),
    path('teacher/attendance-report/', views.view_attendance_report, name='view_attendance_report'),
]
