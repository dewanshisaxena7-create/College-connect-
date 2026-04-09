# College Connect

A modern full-stack Django web application for managing college class schedules and real-time status updates/notifications. Designed with a clean, glassmorphic UI using Vanilla CSS.

## Features
- **Role-based Authentication:** Separate dashboards for Teachers and Students.
- **Teacher Dashboard:** View today's classes and instantly toggle a class status (ON / No Class).
- **Student Dashboard:** Real-time (AJAX polling) view of today's classes and recent notifications.
- **Responsive minimalist UI:** Built purely with Vanilla CSS and Inter font.

---

## 🚀 Setup & Execution Instructions

### 1. Prerequisites
- Python 3.9+
- MySQL Server (XAMPP, WAMP, or standalone MySQL)

### 2. Database Configuration
By default, the application is configured to use a MySQL database named `college_connect` with the user `root` and an empty password `""`.
If your MySQL root user has a password, update `college_connect/settings.py` (`DATABASES` section) accordingly.

1. Open your MySQL client or CLI (e.g., `mysql -u root -p`).
2. Run the provided SQL script to create the database:
```sql
SOURCE database_setup.sql;
```
*(Alternatively, just manually run `CREATE DATABASE college_connect;`)*

### 3. Install Dependencies
Open a terminal in the project root (`college_connect`) and install requirements:
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
Apply the database schema:
```bash
python manage.py makemigrations core
python manage.py migrate
```

### 5. Generate Sample Data
Populate the database with a test teacher, student, subjects, and timetables:
```bash
python setup_sample_data.py
```
*Note: This script assigns classes to every day of the week so you can test it on any given day.*

### 6. Start the Server
Run the local development server:
```bash
python manage.py runserver
```

### 7. Test the Application
Open your browser and navigate to `http://127.0.0.1:8000`.

**Test Accounts:**
- **Teacher:** ID: `T101` / Password: `password`
- **Student:** ID: `S101` / Password: `password`
- **Admin:** ID: `admin` / Password: `admin`

*Tip: Open a regular browser window logged in as the Teacher, and an Incognito/Private window logged in as the Student. Toggle a class off in the Teacher's dash, and watch it dynamically update on the Student's dash within 10 seconds!*
