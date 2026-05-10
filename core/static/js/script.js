// Initialize UI events on load
document.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    initClock();
    initTeacherToggles();
});

let studentAttendanceChart = null;

function initThemeToggle() {
    const toggleBtn = document.getElementById('theme-btn');
    if (!toggleBtn) return;
    
    toggleBtn.addEventListener('click', () => {
        const doc = document.documentElement;
        const currentTheme = doc.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        doc.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        window.dispatchEvent(new Event('themeChanged'));
    });
}

function initClock() {
    const timeEl = document.getElementById('clock-time');
    const dateEl = document.getElementById('clock-date');
    const greetingEl = document.getElementById('greeting-time');
    
    if (!timeEl && !dateEl && !greetingEl) return;

    function updateTime() {
        const now = new Date();
        if (timeEl) {
            let hours = now.getHours();
            let minutes = now.getMinutes();
            let ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12 || 12;
            minutes = minutes < 10 ? '0' + minutes : minutes;
            timeEl.textContent = `${hours}:${minutes} ${ampm}`;
        }
        if (dateEl) {
            const options = { weekday: 'long', month: 'long', day: 'numeric' };
            dateEl.textContent = now.toLocaleDateString('en-US', { weekday: 'long' });
        }
        if (greetingEl) {
            const h = now.getHours();
            let g = h < 12 ? "Good Morning" : h < 17 ? "Good Afternoon" : "Good Evening";
            let i = h < 17 ? "☀️" : "🌙";
            greetingEl.innerHTML = `${g} ${i}`;
        }
    }
    updateTime();
    setInterval(updateTime, 60000); // Minutes is enough
}

function initTeacherToggles() {
    const toggles = document.querySelectorAll(".toggle-class-status");
    toggles.forEach(toggle => {
        toggle.addEventListener("change", function() {
            const id = this.dataset.id;
            const active = this.checked;
            const label = document.getElementById(`status-label-${id}`);
            const btn = document.getElementById(`attendance-btn-${id}`);
            const card = this.closest('.class-item');

            if (active) {
                card.classList.remove('cancelled');
                if (label) { label.innerHTML = "ON"; label.className = "on-label"; }
                if (btn) btn.style.display = 'block';
            } else {
                card.classList.add('cancelled');
                if (label) { label.innerHTML = "OFF"; label.className = "off-label"; }
                if (btn) btn.style.display = 'none';
            }

            fetch(`/api/toggle_class/${id}/`, {
                method: 'POST',
                headers: { 
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ is_active: active })
            });
        });
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Student Dash AJAX Logic
function fetchStudentData() {
    if(!window.API_STUDENT_DATA_URL) return;
    fetch(window.API_STUDENT_DATA_URL)
        .then(res => res.json())
        .then(data => {
            renderClasses(data.classes);
            renderNotifications(data.notifications);
            renderAttendance(data.attendance_history, data.today_attendance);
        });
}

function renderClasses(classes) {
    const list = document.getElementById('student-classes');
    if(!list) return;
    if(classes.length === 0) {
        list.innerHTML = `<div class="stat-card" style="padding:40px; text-align:center; opacity:0.6;">No active classes right now.</div>`;
        return;
    }
    list.innerHTML = classes.map(c => `
        <div class="class-item ${c.is_active ? '' : 'cancelled'}" style="position:relative; padding:2rem;">
            <div style="position:absolute; top:20px; right:20px; display:flex; gap:10px; align-items:center;">
                <span style="background:var(--primary); color:white; padding:2px 8px; border-radius:4px; font-size:0.65rem; font-weight:800;">TODAY</span>
                <span class="${c.is_active ? 'on-label' : 'off-label'}">${c.ui_status}</span>
            </div>
            <div class="class-info">
                <h2 style="font-size:1.8rem; font-weight:800; margin-bottom:15px;">${c.subject_name} 
                    <small style="font-size:0.8rem; opacity:0.6; font-weight:400; margin-left:10px;">Sec ${c.target_section}</small>
                </h2>
                <p style="font-size:0.95rem; display:flex; gap:20px; color:var(--text-secondary);">
                    <span>⏰ ${c.time}</span>
                    <span>📍 Room ${c.room_number}</span>
                    <span>👤 ${c.teacher_name}</span>
                </p>
            </div>
        </div>
    `).join('');
}

function renderNotifications(notifs) {
    const list = document.getElementById('student-notifications');
    if(!list) return;
    if(notifs.length === 0) {
        list.innerHTML = `<p style="opacity:0.5; padding:10px;">No new alerts.</p>`;
        return;
    }
    list.innerHTML = notifs.map(n => `
        <div class="modern-notif">
            <p class="notif-text"><strong>${n.subject}</strong>: ${n.message}</p>
            <span class="notif-time">${n.time}</span>
        </div>
    `).join('');
}

function renderAttendance(history, today) {
    const list = document.getElementById('today-attendance-list');
    if(list) {
        if(today.length === 0) list.innerHTML = `<p style="opacity:0.5;">Not marked yet.</p>`;
        else list.innerHTML = today.map(t => `<div class="stat-card" style="margin-bottom:10px; padding:15px; display:flex; justify-content:space-between;"><span>${t.subject}</span> <strong>${t.status}</strong></div>`).join('');
    }

    // Chart logic (Fixes Double Graph)
    const ctx = document.getElementById('totalAttendanceChart');
    if(!ctx || history.length === 0) return;

    ctx.style.display = 'block';
    const loader = document.getElementById('chart-loader');
    if(loader) loader.style.display = 'none';

    const labels = history.map(h => h.subject);
    const attendedData = history.map(h => h.attended);
    const totalData = history.map(h => h.total);

    if(studentAttendanceChart) studentAttendanceChart.destroy();
    
    studentAttendanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Total Sessions',
                    data: totalData,
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    borderRadius: 8,
                    barPercentage: 0.6
                },
                {
                    label: 'Attended',
                    data: attendedData,
                    backgroundColor: 'linear-gradient(180deg, #3b82f6 0%, #2563eb 100%)',
                    backgroundColor: '#3b82f6', 
                    borderRadius: 8,
                    barPercentage: 0.6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: { bottom: 20 } },
            scales: {
                y: { 
                    beginAtZero: true, 
                    ticks: { color: 'rgba(255,255,255,0.5)', stepSize: 1, font: { size: 10 } },
                    grid: { color: 'rgba(255,255,255,0.03)' }
                },
                x: { 
                    ticks: { 
                        color: 'rgba(255,255,255,0.7)', 
                        maxRotation: 30, 
                        minRotation: 30,
                        font: { size: 10, weight: '600' }
                    },
                    grid: { display: false }
                }
            },
            plugins: { 
                legend: { 
                    display: true, 
                    position: 'top', 
                    align: 'end',
                    labels: { 
                        color: '#fff', 
                        boxWidth: 8, 
                        usePointStyle: true,
                        pointStyle: 'circle',
                        font: { size: 11, weight: '700' } 
                    } 
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleFont: { size: 14, weight: '800' },
                    padding: 12,
                    cornerRadius: 12,
                    displayColors: false
                }
            }
        }
    });

    // Add Text Breakdown below
    const historyText = document.getElementById('attendance-history-text');
    if(historyText) {
        historyText.innerHTML = history.map(h => `
            <div class="stat-card" style="margin-bottom: 10px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="display: block; font-size: 1rem;">${h.subject}</strong>
                    <span style="font-size: 0.8rem; color: var(--text-secondary);">${h.status}</span>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 1.2rem; font-weight: 800; color: var(--primary);">${Math.round((h.attended/h.total)*100)}%</span>
                </div>
            </div>
        `).join('');
    }
}

function getChartColor() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? '#94a3b8' : '#64748b';
}

// Global Sync Starter
function startStudentSync() {
    if(!window.API_STUDENT_DATA_URL) return;
    fetchStudentData();
    setInterval(fetchStudentData, 5000);
}

// Ensure initialization
document.addEventListener("DOMContentLoaded", () => {
    // Small delay to ensure template variables are picked up
    setTimeout(startStudentSync, 500);
});
