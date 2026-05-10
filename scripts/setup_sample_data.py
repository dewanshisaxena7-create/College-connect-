import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_connect.settings')
django.setup()

from core.models import Teacher, Student, ClassSchedule

def run():
    print("Clearing old data...")
    Student.objects.all().delete()
    Teacher.objects.all().delete()
    ClassSchedule.objects.all().delete()

    print("Creating Teacher...")
    teacher = Teacher.objects.create(name="Prof. Smith", unique_key="smith123")

    print("Creating Student...")
    student = Student.objects.create(roll_number="S101", name="Jane Doe", password="password")

    print("Creating Schedules...")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for day in days:
        ClassSchedule.objects.create(
            teacher=teacher,
            subject="Python Programming",
            room_number="Lab 1",
            day=day,
            start_time="09:00",
            end_time="10:30",
            is_active=True
        )
        ClassSchedule.objects.create(
            teacher=teacher,
            subject="Data Structures",
            room_number="Lab 2",
            day=day,
            start_time="11:00",
            end_time="12:30",
            is_active=True
        )
    print("Sample data generated successfully!")

if __name__ == '__main__':
    run()
