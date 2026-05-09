from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (User,
            Teacher,
            Class,
            Section,
            Student,
            Transaction,
            Fee,
            Salary)

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm

from .forms import (
            MyUserCreationForm,
            UserForm,
            TeacherForm,
            ClassForm,
            SectionForm,
            StudentForm,
            TransactionForm,
            FeeForm,
            SalaryForm)

from django.core.mail import send_mail
from django.conf import settings

# Import FAQ data from separate file
from .data.faqs import CONTACT_FAQS

from .services.fee_service import FeeService
from .models import Student

def home(request):
    context = {}
    return render(request,'home.html',context)

def LoginPage(request):
    page = 'loginPage_'

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Email or password is incorrect')

    context = {'page': page}
    return render(request, 'login.html', context)


def Logoutpage(request):
    logout(request)
    return redirect('home')


def Register(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login.html', {'form': form})


@login_required(login_url='loginPage')
def dashboard(request):
    return render(request, 'dashboard.html')




def contact_view(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter')
        
        # Process form data (send email, save to database, etc.)
        try:
            # Send email notification
            email_subject = f"New Contact Form Submission: {subject}"
            email_message = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}
            
            Message:
            {message}
            
            Newsletter Subscription: {'Yes' if newsletter else 'No'}
            """
            
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['hello@ourschoolsoftware.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
            
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
    
    context = {
        'faqs': CONTACT_FAQS,  # Use imported FAQ data
        'page_title': 'Contact Us - School Management System',
        'meta_description': 'Get in touch with us for school management software inquiries. WhatsApp: +92 348 2258263, Email: hello@ourschoolsoftware.com',
    }
    
    return render(request, 'contact.html', context)



def pricing_view(request):
    return render(request, 'pricing.html')


@login_required(login_url='loginPage')
def features_view(request):
    
    features = [
        {
            'title': 'Free Mobile App',
            'description': 'Enjoy an absolutely 100% free modern UI mobile app for For Parents, Students & School Staff.',
            'icon_type': 'image',
            'icon_url': 'https://kimi-web-img.moonshot.cn/prod-data/online-image/search-upload/65fd16a33598303f03ab844579cc6a6d.svg',
        },
        {
            'title': 'Cloud Based',
            'description': 'Access your school software from anywhere, any time with the help of an internet browser.',
            'icon_type': 'image',
            'icon_url': 'https://kimi-web-img.moonshot.cn/prod-data/online-image/search-upload/5c71e3c943d17582fe85bab025d3600d.svg',
        },
        {
            'title': 'Multi Campus',
            'description': 'Setup your all school campuses on cloud for whole institution chain within no time.',
            'icon_type': 'image',
            'icon_url': 'https://kimi-web-img.moonshot.cn/prod-data/online-image/search-upload/65fd16a33598303f03ab844579cc6a6d.svg',
        },
        {
            'title': 'Multi Portal',
            'description': 'Separate login portals for Admin, Teachers, Students, Parents & Management staff.',
            'icon_type': 'image',
            'icon_url': 'https://kimi-web-img.moonshot.cn/prod-data/online-image/search-upload/5c71e3c943d17582fe85bab025d3600d.svg',
        },
        {
            'title': 'Student Management',
            'description': 'Complete student information system from admission to alumni with detailed records.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-user-graduate',
        },
        {
            'title': 'Attendance System',
            'description': 'Digital attendance tracking with biometric integration and automated reports.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-calendar-check',
        },
        {
            'title': 'Examination',
            'description': 'Manage exams, create timetables, handle grading and generate result cards instantly.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-file-alt',
        },
        {
            'title': 'Fee Management',
            'description': 'Automated fee collection, invoicing, and financial reporting with payment gateway.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-money-bill-wave',
        },
        {
            'title': 'Timetable',
            'description': 'Dynamic class scheduling system with conflict detection and substitution management.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-clock',
        },
        {
            'title': 'Homework',
            'description': 'Digital homework assignment, submission and evaluation with parent notifications.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-book',
        },
        {
            'title': 'Online Classes',
            'description': 'Integrated virtual classroom with video conferencing and recording capabilities.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-video',
        },
        {
            'title': 'SMS/Email Alerts',
            'description': 'Instant notifications for attendance, fees, exams and important announcements.',
            'icon_type': 'fontawesome',
            'icon_class': 'fas fa-bell',
        },
    ]
    
    context = {
        'features': features,
        'page_title': 'Features - School Management System',
        'meta_description': 'Explore the best features of our free school management system including mobile app, cloud access, multi-campus support, and more.',
    }
    
    return render(request, 'features.html', context)



def about_view(request):
    context = {}
    return render (request,'about.html',context)



def learn_more(request):
    context = {
        'title': 'Learn More - School Management System',
        'meta_description': 'Discover powerful features of our school management system.',
    }
    return render(request, 'learn_more.html', context)


def dashboard(request):
    now = timezone.now()
    # Calculate "This Month" (Teachers added since the 1st of the current month)
    teachers_this_month = Teacher.objects.filter(
        created_at__year=now.year, 
        created_at__month=now.month
    ).count()
    # We create a dictionary to match what your HTML expects
    context = {
        'stats': {
            'teachers': Teacher.objects.count(),
            'teachers_trend': teachers_this_month,
            # You can add more here later:
            # 'students': Student.objects.count(),
            'classes': Class.objects.count(),
        }
    }
    return render(request, 'dashboard.html', context)


#========================= Teacher Function ===================================================================
@login_required(login_url='loginPage')
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {"teachers": teachers}
    return render(request, "teachers/all_teacher.html", context)

@login_required(login_url='loginPage')
def teacher_create(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Teacher created successfully")
        return redirect("teacher_list")
    context = {"form":form}
    return render(request, "teachers/teacher_form.html", context)

@login_required(login_url='loginPage')
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(
        request.POST or None,
        request.FILES or None,
        instance=teacher
    )
    if form.is_valid():
        form.save()
        messages.success(request, "Teacher updated successfully")
        return redirect("teacher_list")
    context = {"form":form}
    return render(request, "teachers/teacher_form.html", context)

@login_required(login_url='loginPage')
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    
    # CRITICAL FIX: Only delete on POST to prevent accidental/malicious URL hits
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect("teacher_list")
        
    # If GET request, render a confirmation page
    context = {"teacher": teacher}
    return render(request, "teachers/teacher_confirm_delete.html", context)


#========================= Class Function =======================================================================================
def class_list(request):
    classes = Class.objects.all()
    return render(request, "classes/all_classes.html", {"classes": classes})

def class_create(request):
    form = ClassForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Class created successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})

def class_update(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    form = ClassForm(
        request.POST or None,
        request.FILES or None,
        instance=class_obj
    )
    if form.is_valid():
        form.save()
        messages.success(request, "Class updated successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})

def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect("class_list")

    context = {"class_obj": class_obj}
    return render(request, "classes/class_confirm_delete.html", context)
    

#========================= Section Function =======================================================================================
def section_list(request):
    sections = Section.objects.all()
    return render(request, "sections/all_sections.html", {"sections": sections})

def section_create(request):
    form = SectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Section created successfully")
        return redirect("section_list")
    return render(request, "sections/section_form.html", {"form": form})
    
def section_update(request,pk):
    section_obj = get_object_or_404(Section, pk=pk)
    form = SectionForm(
        request.POST or None,
        request.FILES or None,
        instance= section_obj
    )
    if form.is_valid():
        form.save()
        messages.success(request,"Section updated successfully")
        return redirect("section_list")
    return render(request,"sections/section_form.html",{"form": form})

def section_delete(request,pk):
    section_obj = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section_obj.delete()
        messages.success(request,'Section deleted successfully.')
        return redirect('section_list')
        
    context = {"section_obj": section_obj}
    return render(request,'sections/section_confirm_delete.html',context)


#========================= Student Function =======================================================================================
def student_list(request):
    student = Student.objects.all()
    return render(request,"students/all_student.html",{'student': student})

def student_create(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Student created successfully")
        return redirect("student_list")
    return render(request,"students/student_form.html",{"form": form})

def student_update(request, pk):
    student_obj = get_object_or_404(Student, pk=pk)
    form = StudentForm(
        request.POST or None,
        request.FILES or None,
        instance= student_obj
    )
    if form.is_valid():
        form.save()
        messages.success(request,"Student updated successfully")
        return redirect("student_list")
    return render(request,"students/student_form.html",{"form": form})

def student_delete(request, pk):
    student_obj = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student_obj.delete()
        messages.success(request,'Student deleted successfully.')
        return redirect('student_list')
        
    context = {"student_obj": student_obj}
    return render(request,'students/student_confirm_delete.html',context)