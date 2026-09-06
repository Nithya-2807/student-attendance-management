\# 🎓 Student Attendance Management System



A web-based Student Attendance Management System built using Python and Flask.  

The system helps manage students, faculty, classes, attendance, and attendance reports through a simple and responsive web interface.



\## 🌐 Live Demo



👉 \[Open Student Attendance Management System](https://student-attendance-management-zmzs.onrender.com)



\## ✨ Features



\### 👨‍🎓 Student Management

\- Add students

\- Edit student details

\- Delete students

\- Search students by roll number or name

\- Filter students by department and section



\### 👩‍🏫 Faculty Management

\- Add faculty members

\- Edit faculty details

\- Delete faculty members

\- Search faculty



\### 📚 Class Management

\- Manage up to 8 periods per day

\- Department and section-wise class scheduling

\- Regular, Adjusted, and Leisure class types

\- Subject-wise class records

\- Date-wise class management



\### 📝 Attendance Management

\- Select department, section, date, and periods

\- Mark Present/Absent attendance

\- Automatically record class information

\- Leisure and Not Conducted periods are excluded from attendance calculations

\- Department and section-wise attendance



\### 📊 Attendance Reports

\- Date-wise attendance reports

\- Department and section filters

\- Period-wise attendance

\- Total conducted and attended periods

\- Attendance percentage

\- Low-attendance identification



\## 🛠️ Technologies Used



\- Python

\- Flask

\- HTML

\- CSS

\- CSV



\## 📁 Project Structure



```text

Student-Attendance-Web/

│

├── backend/

│   ├── app.py

│   └── data/

│       ├── students.csv

│       ├── faculty.csv

│       ├── classes.csv

│       └── attendance.csv

│

├── static/

│   └── css/

│       └── style.css

│

├── templates/

│   ├── index.html

│   ├── students.html

│   ├── edit\_student.html

│   ├── faculty.html

│   ├── edit\_faculty.html

│   ├── classes.html

│   ├── attendance.html

│   └── reports.html

│

├── requirements.txt

└── README.md

