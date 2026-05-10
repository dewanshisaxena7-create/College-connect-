# College Connect 🎓

College Connect is a professional Student Management & Attendance Coordination platform designed for modern academic environments. It features a sleek, theme-aware UI, real-time class status tracking, and advanced attendance analytics for both faculty and students.

## ✨ Core Features

### 👨‍🏫 Faculty Dashboard
- **Live Scheduling:** Create and manage classes with a 3-tier status system (`WAITING`, `ON`, `CANCELLED`).
- **Dynamic Attendance:** Quickly mark student attendance per section and subject.
- **Reporting:** Filter attendance records by subject and export rosters directly to **CSV/Excel**.
- **Edit on the Fly:** Modify existing schedules (Room, Time, Subject) without deleting data.

### 👨‍🎓 Student Dashboard
- **Real-time Status:** Instant updates on which classes are currently active or cancelled.
- **Visual Analytics:** Interactive `Chart.js` bars and a card-based grid showing subject-wise attendance percentages.
- **Smart Notifications:** Priority "Upcoming Class" alerts pinned with visual highlights for classes starting within 60 minutes.
- **Theme Support:** Fully compatible with Light and Dark mode preferences.

## 🛠️ Tech Stack
- **Backend:** Django (Python) 🐍
- **Database:** SQLite (Default) / MySQL (Compatible) 🗄️
- **Frontend:** Vanilla JS, HTML5, CSS3 🎨
- **Library:** Chart.js, MDTimePicker 📈

## 🚀 Quick Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd college_connect
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Initialize Roster (Optional):**
   ```bash
   python scripts/reset_roster.py
   ```

5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

---

## 📂 Documentation
For detailed technical info, check the `docs/` directory:
- [Implementation Plans](docs/implementation_plans.md)
- [Deployment Guide](docs/deployment_guide.md)
- [Faculty Credentials](docs/faculty_credentials.md)
