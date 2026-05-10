import hashlib
import base64
import os

teachers = [
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

all_students = students_a + students_b

def django_pbkdf2_sha256(password):
    iterations = 720000
    salt = os.urandom(12).hex() # 12 bytes = 24 hex characters
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('ascii'), iterations)
    hash_b64 = base64.b64encode(hash_bytes).decode('ascii')
    return f"pbkdf2_sha256${iterations}${salt}${hash_b64}"

def gen_teacher_id(name):
    # e.g., Kirti Mathu -> kir.thu
    parts = name.split()
    first = parts[0][:3].lower()
    last = parts[-1][-3:].lower()
    return f"{first}.{last}"

with open("college_connect_mysql.sql", "w", encoding="utf-8") as f:
    f.write("-- College Connect Custom MySQL Dump\n")
    f.write("CREATE DATABASE IF NOT EXISTS college_connect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
    f.write("USE college_connect;\n\n")

    f.write("CREATE TABLE IF NOT EXISTS `core_teacher` (\n")
    f.write("  `id` bigint NOT NULL AUTO_INCREMENT,\n")
    f.write("  `name` varchar(100) NOT NULL,\n")
    f.write("  `teacher_id` varchar(100) NOT NULL UNIQUE,\n")
    f.write("  `password` varchar(255) DEFAULT NULL,\n")
    f.write("  `is_first_login` tinyint(1) NOT NULL DEFAULT 1,\n")
    f.write("  PRIMARY KEY (`id`)\n")
    f.write(");\n\n")

    f.write("CREATE TABLE IF NOT EXISTS `core_student` (\n")
    f.write("  `id` bigint NOT NULL AUTO_INCREMENT,\n")
    f.write("  `roll_number` varchar(50) NOT NULL UNIQUE,\n")
    f.write("  `name` varchar(100) NOT NULL,\n")
    f.write("  `password` varchar(255) NOT NULL,\n")
    f.write("  PRIMARY KEY (`id`)\n")
    f.write(");\n\n")
    
    f.write("CREATE TABLE IF NOT EXISTS `core_classschedule` (\n")
    f.write("  `id` bigint NOT NULL AUTO_INCREMENT,\n")
    f.write("  `subject` varchar(100) NOT NULL,\n")
    f.write("  `room_number` varchar(50) NOT NULL,\n")
    f.write("  `day` varchar(10) NOT NULL,\n")
    f.write("  `start_time` time(6) NOT NULL,\n")
    f.write("  `end_time` time(6) NOT NULL,\n")
    f.write("  `is_active` tinyint(1) NOT NULL,\n")
    f.write("  `teacher_id` bigint NOT NULL,\n")
    f.write("  PRIMARY KEY (`id`),\n")
    f.write("  FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`id`) ON DELETE CASCADE\n")
    f.write(");\n\n")
    
    f.write("CREATE TABLE IF NOT EXISTS `core_notification` (\n")
    f.write("  `id` bigint NOT NULL AUTO_INCREMENT,\n")
    f.write("  `message` longtext NOT NULL,\n")
    f.write("  `timestamp` datetime(6) NOT NULL,\n")
    f.write("  `schedule_id` bigint DEFAULT NULL,\n")
    f.write("  PRIMARY KEY (`id`),\n")
    f.write("  FOREIGN KEY (`schedule_id`) REFERENCES `core_classschedule` (`id`) ON DELETE CASCADE\n")
    f.write(");\n\n")

    f.write("-- Inserting Teachers\n")
    for t in teachers:
        t_id = gen_teacher_id(t)
        f.write(f"INSERT IGNORE INTO `core_teacher` (`name`, `teacher_id`, `password`, `is_first_login`) VALUES ('{t}', '{t_id}', NULL, 1);\n")

    f.write("\n-- Inserting Students\n")
    for roll, name in all_students:
        pwd = django_pbkdf2_sha256(roll.upper()) # Explicitly uppercase roll as password
        f.write(f"INSERT IGNORE INTO `core_student` (`roll_number`, `name`, `password`) VALUES ('{roll}', '{name}', '{pwd}');\n")

print("Generated college_connect_mysql.sql safely.")
