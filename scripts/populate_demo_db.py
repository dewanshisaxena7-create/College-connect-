import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_connect.settings')
django.setup()

from core.models import Teacher, Student, ClassSchedule
from django.contrib.auth.hashers import make_password

# Data from previous turn
teachers_data = [
    "Kirti Mathu", "Ramesh Thakur", "Shaligram Prajapat", "Yasmin Shaikh",
    "Rahul Singhai", "Jugendra Dongre", "Manju Suchdeo", "Poonam Mangwani",
    "Vivek Shrivastava", "Basant Namdeo", "Nitin Nagar", "Rupesh Sendre",
    "Shraddha Soni", "Kirti Vijayvargiya", "Rajesh Verma", "Pradeep K. Jatav", "Shailvi Verma"
]

students_a = [
("IC-2K23-01", "AASTHA MATHANIYA"), ("IC-2K23-02", "AAYUSH CHOURASIA"),
("IC-2K23-03", "AAYUSH SURYAWANSHI"), ("IC-2K23-04", "AAYUSHI RATHORE"),
("IC-2K23-05", "ABDUL REHMAN MANSOORI"), ("IC-2K23-06", "ABHISHEK YADAV"),
("IC-2K23-07", "AKSHAT THAKUR"), ("IC-2K23-08", "AKSHATA RAMESH GHODCHAR"),
("IC-2K23-09", "AKSHAY JAIN"), ("IC-2K23-10", "ANIKA BABAR"),
("IC-2K23-11", "ANSHITA SONI"), ("IC-2K23-12", "ANUSHKA SHARMA"),
("IC-2K23-13", "ASHWIN SUPATH"), ("IC-2K23-14", "ATHARV CHINCHE"),
("IC-2K23-15", "ATHARVA CHAUHAN"), ("IC-2K23-16", "AYUSH JAISWAL"),
("IC-2K23-17", "AYUSH SINDHIYA"), ("IC-2K23-18", "BISHAL KUMAR"),
("IC-2K23-19", "CHINDAN KUSHWAHA"), ("IC-2K23-20", "DEEPSHIKHA VISHWAKARMA"),
("IC-2K23-21", "DEV KUMAR JAIN"), ("IC-2K23-22", "DEV PANDEY"),
("IC-2K23-23", "DEVANSHI KARVE"), ("IC-2K23-24", "DEVANSHI SAXENA"),
("IC-2K23-25", "DEVASHISH PATEL"), ("IC-2K23-26", "DHAIRYA JOSHI"),
("IC-2K23-27", "DISHA CHAWLA"), ("IC-2K23-28", "DISHAN SHEIKH"),
("IC-2K23-29", "DIVYA SHARMA"), ("IC-2K23-30", "DIVYANSH AREKAR"),
("IC-2K23-31", "DIVYANSH VERMA"), ("IC-2K23-32", "DIVYESH SINGH GEHLOT"),
("IC-2K23-33", "HANSIKA GURJAR"), ("IC-2K23-34", "HARSH DEV SINGH THAKUR"),
("IC-2K23-35", "HARSHIT HARDIYA"), ("IC-2K23-36", "HARSHIT SONEL"),
("IC-2K23-37", "HARSHITA SOHNER"), ("IC-2K23-38", "HIMANSHU KANAS"),
("IC-2K23-39", "HITESH GUPTA"), ("IC-2K23-40", "ISHA KHAN"),
("IC-2K23-41", "ISHA VEERWANI"), ("IC-2K23-42", "ISHITA AGRAWAL"),
("IC-2K23-43", "JAGRATI TRIPATHI"), ("IC-2K23-44", "JALAJ MEHTA"),
("IC-2K23-45", "JAYESH SOLANKI"), ("IC-2K23-46", "JEET VERMA"),
("IC-2K23-47", "KALPANA PATIDAR"), ("IC-2K23-48", "KARTIK GURJAR"),
("IC-2K23-49", "KASHISH NANKANI"), ("IC-2K23-50", "KESHAV SHARMA")
]

students_b = [
("IC-2K22-73", "SANDEEP YADAV"), ("IC-2K22-87", "SNEHA SALVE"),
("IC-2K23-51", "KHUSHI DIXIT"), ("IC-2K23-52", "KRISHNKANT UPADHYAY"),
("IC-2K23-54", "LALIT SOLANKI"), ("IC-2K23-55", "MAHAK LODHI"),
("IC-2K23-56", "MAHIMA CHHABRA"), ("IC-2K23-57", "MANAS PATHAK"),
("IC-2K23-58", "MANTHAN SHARMA"), ("IC-2K23-60", "NACHIKETA NAYAK"),
("IC-2K23-61", "NAINA RAGHUWANSHI"), ("IC-2K23-62", "NANDANI RATHORE"),
("IC-2K23-63", "NIKHIL PATEL"), ("IC-2K23-64", "PARANJAY SHARMA"),
("IC-2K23-65", "PRAGATI SIKARWAR"), ("IC-2K23-66", "PRAKHAR PANCHOLI"),
("IC-2K23-67", "PRANEETA PATIDAR"), ("IC-2K23-68", "PRANJAL YADAV"),
("IC-2K23-69", "PRITAM SINGH RATHORE"), ("IC-2K23-70", "PRIYANKA GOSWAMI"),
("IC-2K23-71", "RAJ GOUR"), ("IC-2K23-72", "RISHABH DULGAJ"),
("IC-2K23-73", "ROHAN LAKHAN"), ("IC-2K23-74", "RUDRA JAGGI"),
("IC-2K23-75", "RUDRA SADAWARTE"), ("IC-2K23-76", "RUNNU PATIDAR"),
("IC-2K23-79", "SAMBHAV SHARMA"), ("IC-2K23-80", "SHANTANU PALIWAL"),
("IC-2K23-81", "SHIVKANT PATEL"), ("IC-2K23-82", "SHREYA PATIDAR"),
("IC-2K23-83", "SHREYANSH SHIVHARE"), ("IC-2K23-84", "SHREYAS NAMDEO"),
("IC-2K23-85", "SHRIJAL KUMAR JAISWAL"), ("IC-2K23-86", "SIDDHANT JAIN"),
("IC-2K23-87", "SNEHA SOLANKI"), ("IC-2K23-88", "SUMIT YOGI"),
("IC-2K23-89", "SURUCHI KUMARI"), ("IC-2K23-90", "SUSHMEET KAUR SALUJA"),
("IC-2K23-91", "SWASTIK SHINDE"), ("IC-2K23-92", "TANISH SETHIYA"),
("IC-2K23-93", "TANISHA NAGWANI"), ("IC-2K23-94", "TANUSHKA KAMLE"),
("IC-2K23-95", "TASNEEM SAFDARI"), ("IC-2K23-96", "TUSHAR KHARADE"),
("IC-2K23-97", "TUSHAR PAWAR"), ("IC-2K23-98", "UTKARSH DUBEY"),
("IC-2K23-99", "VINISHA WAGH"), ("IC-2K23-100", "YASH GURJAR"),
("IC-2K23-101", "YASH KUMAR CHOUREY"), ("IC-2K23-102", "NEHA BHADKARE")
]

def gen_teacher_id(name):
    parts = name.split()
    first = parts[0][:3].lower()
    last = parts[-1][-3:].lower()
    return f"{first}.{last}"

def populate():
    print("Clearing old data...")
    Teacher.objects.all().delete()
    Student.objects.all().delete()
    ClassSchedule.objects.all().delete()
    
    print("Populating Teachers...")
    t_objs = []
    for t_name in teachers_data:
        t_id = gen_teacher_id(t_name)
        t_objs.append(Teacher(name=t_name, teacher_id=t_id, password=None, is_first_login=True))
    Teacher.objects.bulk_create(t_objs)
    
    print("Populating Students...")
    s_objs = []
    all_studs = students_a + students_b
    for roll, s_name in all_studs:
        # roll.upper() as default password
        pwd = make_password(roll.upper())
        s_objs.append(Student(name=s_name, roll_number=roll, password=pwd))
    Student.objects.bulk_create(s_objs)
    
    # Add a sample schedule for today for at least one teacher
    import datetime
    today_name = datetime.datetime.now().strftime("%A")
    first_teacher = Teacher.objects.first()
    ClassSchedule.objects.create(
        teacher=first_teacher,
        subject="Sample Today Class",
        room_number="101",
        day=today_name,
        start_time="09:00",
        end_time="10:00",
        is_active=True
    )
    
    print("Population complete.")

if __name__ == "__main__":
    populate()
