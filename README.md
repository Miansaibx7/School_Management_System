# 🏫 EduManager Pro – School Management System

A comprehensive, Django-based School Management System designed to streamline student admissions, teacher management, fee tracking, salary payments, and financial reporting – all from a single, intuitive dashboard.

![Django](https://img.shields.io/badge/Django-5.0-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![HTML](https://img.shields.io/badge/HTML-43.4%-orange)
![CSS](https://img.shields.io/badge/CSS-38.0%-purple)
![JavaScript](https://img.shields.io/badge/JavaScript-1.3%-yellow)

---

## ✨ Features

### 📊 Dashboard
- Real-time overview of total students, teachers, classes & revenue
- Recent admissions table with status tracking
- Quick action buttons for adding students, teachers, recording fees & generating reports
- Fee defaulters alert system

### 👨‍🎓 Student Management
- Add, update, delete student records
- Track admission date, class, section & roll number
- Fee payment history & status tracking

### 👨‍🏫 Teacher Management
- Manage teacher profiles with designation & qualification
- Salary payment tracking & history
- Class teacher assignment

### 🏫 Academic Management
- Class & Section management
- Class teacher assignment for each section
- Capacity tracking

### 💰 Finance Management
- **Fee Payments** – Record student fee payments with multiple payment methods
- **Salary Payments** – Track teacher salary payments
- **Transactions** – Complete income/expense tracking with categories
- **Financial Reports** – Income vs expense charts, fee status pie charts, monthly summaries

### 📈 Reports & Analytics
- Monthly income vs expense bar charts
- Fee status pie chart (Paid/Partial/Pending)
- Transaction history with filtering
- Total balance calculation

### 🔐 Authentication
- Secure login & registration system
- Role-based access (Admin, Accountant, etc.)
- Protected routes & session management

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django** | Web framework |
| **SQLite / PostgreSQL** | Database |
| **HTML5 / CSS3** | Frontend structure & styling |
| **JavaScript** | Client-side interactivity |
| **Chart.js** | Interactive charts & graphs |
| **Font Awesome** | Icons |
| **Bootstrap** | Responsive design |

---


---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip (Python package manager) or uv command
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Miansaibx7/School_Management_System.git
   cd School_Management_System

## Create a virtual environment

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

## Install dependencies

pip install -r requirements.txt

## Run migrations

python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
Open your browser and visit: http://127.0.0.1:8000

## 📊 Dashboard Features in Detail
Home Dashboard
Statistics Cards: Total Students, Teachers, Classes, Monthly Revenue
Recent Admissions: Table with student name, class, admission date & status
Quick Actions: Buttons for common tasks (Add Student, Add Teacher, Record Fee, Reports)
Fee Defaulters: List of students with pending fees

# Financial Reports
Summary Cards: Total Income, Total Expense, Total Balance, Fee Collected, Pending Fees, Salary Paid
Income vs Expense Chart: Monthly bar chart comparing income and expenses
Fee Status Report: Pie chart showing Paid/Partial/Pending fee distribution

# Transaction History
Recent Transactions: Date, Title, Type (Income/Expense), Amount
Search & Filter: Filter transactions by type, date, or category

## 🤝 Contributing

Contributions are welcome! Here's how you can help:
Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request
Areas for Improvement
Add student attendance tracking
Implement exam results management
Add SMS/Email notifications
Export reports as PDF/Excel
Add student & teacher profiles with photos
Implement multi-school/branch support

## 🐛 Bug Reports
Found a bug? Please open an issue with:
Description of the issue
Steps to reproduce
Screenshots (if applicable)
Environment details

## 📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

## 📧 Contact
Mian Muhammad Waqas

GitHub: @Miansaibx7

## ⭐ Show Your Support
If you found this project helpful, please give it a ⭐ on GitHub!

