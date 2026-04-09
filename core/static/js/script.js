// Global variable for Chart.js
let studentAttendanceChart = null;

// Initialize UI events on load
document.addEventListener("DOMContentLoaded", () => {
    // Hide loader
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => loader.style.display = 'none', 500);
    }

    initThemeToggle();
    initClock();
    initTeacherToggles();
});

function initThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;
    
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        toggleBtn.textContent = '☀️';
    } else {
        document.documentElement.removeAttribute('data-theme');
        toggleBtn.textContent = '🌙';
    }

    toggleBtn.addEventListener('click', () => {
        let theme = localStorage.getItem('theme') || 'light';
        if (theme === 'light') {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            toggleBtn.textContent = '☀️';
        } else {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
            toggleBtn.textContent = '🌙';
        }
    });
}

function initClock() {
    const clockEl = document.getElementById('dynamic-clock');
    const greetingEl = document.getElementById('dynamic-greeting');
    if (!clockEl && !greetingEl) return;

    function updateTime() {
        const now = new Date();
        
        if (clockEl) {
            let hours = now.getHours();
            let minutes = now.getMinutes();
            let seconds = now.getSeconds();
            let ampm = hours >= 12 ? 'PM' : 'AM';
            
            // Analog calculations
            const hourHand = document.querySelector('.hour-hand');
            const minuteHand = document.querySelector('.minute-hand');
            if (hourHand && minuteHand) {
                let hRotation = (hours % 12) * 30 + (minutes / 2);
                let mRotation = minutes * 6 + (seconds / 10);
                hourHand.style.transform = `translateX(-50%) rotate(${hRotation}deg)`;
                minuteHand.style.transform = `translateX(-50%) rotate(${mRotation}deg)`;
            }

            hours = hours % 12;
            hours = hours ? hours : 12;
            let displayMins = minutes < 10 ? '0' + minutes : minutes;
            const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
            const dayName = days[now.getDay()];
            clockEl.textContent = `${hours}:${displayMins} ${ampm} | ${dayName}`;
        }

        const greetingEl = document.getElementById('greeting-time');

        if (greetingEl) {
            const currentHour = now.getHours();
            let greeting = "Good Evening";
            if (currentHour < 12) greeting = "Good Morning";
            else if (currentHour < 17) greeting = "Good Afternoon";
            
            greetingEl.textContent = greeting;
        }
    }
    
    updateTime();
    setInterval(updateTime, 1000);
}


// Teacher Dash: Toggle Class logic
function initTeacherToggles() {
    const toggles = document.querySelectorAll(".toggle-class-status");
    toggles.forEach(toggle => {
        toggle.addEventListener("change", function() {
            const timetableId = this.dataset.id;
            const isChecked = this.checked;
            const label = document.getElementById(`status-label-${timetableId}`);
            const card = this.closest('.class-card');
            
            // Visual optimistic update
            if(isChecked) {
                label.textContent = "ON";
                label.className = "status-label status-on";
                card.classList.remove('cancelled');
                let btn = document.getElementById(`attendance-btn-${timetableId}`);
                if(btn) btn.style.display = 'block';
            } else {
                label.textContent = "NO CLASS";
                label.className = "status-label status-off";
                card.classList.add('cancelled');
                let btn = document.getElementById(`attendance-btn-${timetableId}`);
                if(btn) btn.style.display = 'none';
            }

            // AJAX request to backend
            fetch(window.API_TOGGLE_URL + timetableId + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.CSRF_TOKEN
                },
                body: JSON.stringify({ is_active: isChecked })
            })
            .then(res => res.json())
            .then(data => {
                if(!data.success) {
                    alert("Failed to update class status.");
                    this.checked = !isChecked; // Revert on failure
                } else if(isChecked) {
                     // update attendance link dynamically if re-activated
                     let btn = document.getElementById(`attendance-btn-${timetableId}`);
                     if(btn && data.daily_class_id) {
                         let anchor = btn.querySelector('a');
                         anchor.href = `/teacher/attendance/${data.daily_class_id}/`;
                     }
                }
            })
            .catch(err => {
                console.error("Error toggling class:", err);
                alert("Network error. Please try again.");
                this.checked = !isChecked; // Revert
            });
        });
        
        // Setup initial label classes
        const id = toggle.dataset.id;
        const label = document.getElementById(`status-label-${id}`);
        if(label) {
            if(toggle.checked) { label.className = "status-label status-on"; }
            else { label.className = "status-label status-off"; toggle.closest('.class-card').classList.add('cancelled'); }
        }
    });
}

// Student Dash: AJAX Polling
function fetchStudentData() {
    if(!window.API_STUDENT_DATA_URL) return;

    fetch(window.API_STUDENT_DATA_URL)
        .then(res => res.json())
        .then(data => {
            renderStudentClasses(data.classes);
            renderStudentNotifications(data.notifications);
            renderTodayAttendance(data.today_attendance);
            renderTotalAttendance(data.attendance_history);
        })
        .catch(err => console.error("Error fetching student data:", err));
}

function renderStudentClasses(classes) {
    const list = document.getElementById('student-classes');
    if(!list) return;
    
    if(classes.length === 0) {
        list.innerHTML = `<div class="empty-state">No classes scheduled for today. Enjoy your day!</div>`;
        return;
    }
    
    list.innerHTML = classes.map(c => `
        <div class="class-card ${c.is_active ? '' : 'cancelled'}">
            <div class="class-info">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <h4>${c.subject_name}</h4>
                    <span style="border: 1px solid var(--text-muted); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; color: var(--text-muted);">Section ${c.target_section}</span>
                </div>
                <p class="meta">
                    <span class="teacher">Prof. ${c.teacher_name}</span>
                    <span class="time">${c.time}</span>
                    <span class="room">Room ${c.room_number}</span>
                </p>
            </div>
            <div class="class-status" style="display: ${c.is_active ? 'block' : 'none'};">
                <span class="status-label status-on">
                    Class is ON
                </span>
            </div>
            <div class="class-status" style="display: ${!c.is_active ? 'block' : 'none'};">
                <span class="status-label status-off">
                    Class Cancelled
                </span>
            </div>
        </div>
    `).join('');
}

function renderTodayAttendance(history) {
    const list = document.getElementById('today-attendance-list');
    if(!list) return;
    
    if(!history || history.length === 0) {
        list.innerHTML = `<div class="empty-state" style="color: var(--text-muted);">No attendance records for today.</div>`;
        return;
    }
    
    list.innerHTML = history.map(h => `
        <div class="class-card" style="padding: 15px; margin-bottom: 10px; cursor: default;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0;">${h.subject}</h4>
                    <span style="font-size: 12px; color: var(--text-muted);">${h.date}</span>
                </div>
                <span class="status-label ${h.status === 'Present' ? 'status-on' : 'status-off'}" style="font-size: 13px; font-weight: bold; border: 1px solid currentColor; padding: 4px 10px; border-radius: 4px;">
                    ${h.status.toUpperCase()}
                </span>
            </div>
        </div>
    `).join('');
}

function renderTotalAttendance(history) {
    const list = document.getElementById('attendance-history-list');
    const textList = document.getElementById('attendance-history-text');
    const canvas = document.getElementById('totalAttendanceChart');
    if(!list || !textList || !canvas) return;
    
    if(!history || history.length === 0) {
        textList.innerHTML = `<div class="empty-state" style="color: var(--text-muted);">No overall attendance records yet.</div>`;
        canvas.style.display = 'none';
        return;
    }
    
    canvas.style.display = 'block';
    
    // Wrap labels by splitting on spaces for better X-axis rendering
    const labels = history.map(h => {
        let words = h.subject.split(' ');
        if (words.length > 3) return [words.slice(0,2).join(' '), words.slice(2).join(' ')];
        return words;
    });
    
    const attendedData = history.map(h => h.attended);
    const totalData = history.map(h => h.total);
    
    if (studentAttendanceChart) {
        studentAttendanceChart.data.labels = labels;
        studentAttendanceChart.data.datasets[0].data = attendedData;
        studentAttendanceChart.data.datasets[1].data = totalData;
        studentAttendanceChart.update();
    } else {
        const ctx = canvas.getContext('2d');
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const colorText = isDark ? '#f8fafc' : '#0f172a';
        
        studentAttendanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Classes Attended',
                        data: attendedData,
                        backgroundColor: 'rgba(52, 211, 153, 0.8)',
                    },
                    {
                        label: 'Total Conducted',
                        data: totalData,
                        backgroundColor: 'rgba(96, 165, 250, 0.4)',
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1, color: colorText } },
                    x: { ticks: { color: colorText, maxRotation: 0, minRotation: 0, autoSkip: false } }
                },
                plugins: {
                    legend: { labels: { color: colorText } }
                }
            }
        });
    }

    textList.innerHTML = history.map(h => `
        <p style="font-size: 15px; margin-bottom: 8px; color: var(--text-main); display: flex; align-items: center; gap: 8px;">
            <span style="color: var(--primary); font-size: 1.2em;">•</span> 
            You attended <strong>${h.attended} out of ${h.total}</strong> ${h.subject} classes.
        </p>
    `).join('');
}

function renderStudentNotifications(notifications) {
    const list = document.getElementById('student-notifications');
    if(!list) return;
    
    if(notifications.length === 0) {
        list.innerHTML = `<div class="empty-state">No new notifications.</div>`;
        return;
    }
    
    list.innerHTML = notifications.map(n => `
        <div class="notification-card">
            <p>${n.message}</p>
            <span class="time">${n.time}</span>
        </div>
    `).join('');
}


// Unified Login Slide Logic
document.addEventListener("DOMContentLoaded", () => {
    const loginText = document.querySelector(".title-text .login");
    const loginForm = document.querySelector("form.login");
    const loginBtn = document.querySelector("label.login");
    const signupBtn = document.querySelector("label.signup");
    
    if (signupBtn && loginBtn && loginForm && loginText) {
        signupBtn.onclick = (() => {
            loginForm.style.marginLeft = "-50%";
            loginText.style.marginLeft = "-50%";
        });
        loginBtn.onclick = (() => {
            loginForm.style.marginLeft = "0%";
            loginText.style.marginLeft = "0%";
        });
        
        // Initial setup based on radio buttons
        const signupRadio = document.getElementById("signup");
        if (signupRadio && signupRadio.checked) {
            loginForm.style.marginLeft = "-50%";
            loginText.style.marginLeft = "-50%";
        }
    }
});
