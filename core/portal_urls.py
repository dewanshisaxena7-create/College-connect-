from django.urls import path
from . import admin_portal_views

urlpatterns = [
    path('login/', admin_portal_views.portal_login, name='portal_login'),
    path('logout/', admin_portal_views.portal_logout, name='portal_logout'),
    path('dashboard/', admin_portal_views.portal_dashboard, name='portal_dashboard'),
    path('students/', admin_portal_views.portal_students, name='portal_students'),
    path('teachers/', admin_portal_views.portal_teachers, name='portal_teachers'),
    path('schedules/', admin_portal_views.portal_schedules, name='portal_schedules'),
    path('attendance/', admin_portal_views.portal_attendance, name='portal_attendance'),
    path('attendance/export/', admin_portal_views.portal_attendance_export, name='portal_attendance_export'),
    path('notifications/', admin_portal_views.portal_notifications, name='portal_notifications'),
]
