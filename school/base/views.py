from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
import json

from .decorators import admin_required, accountant_required 

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

from .forms import (
            MyUserCreationForm,
            UserForm,
            ProfileForm,
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
from .data.features import features_info

# from .services.fee_service import FeeService


def home(request):
    context = {}
    return render(request,'home.html',context)
# ========================= CONTACT VIEW WITH FAQS AND EMAIL NOTIFICATIONS ==========================
def contact_view(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter')
        
        # Process form data (send email, save to database)
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
            
            Newsletter Subscription: {'Yes' if newsletter else 'No'}"""
            
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
        'meta_description': 'Get in touch with us for school management software inquiries.'
        ' WhatsApp: +92 306 8363688, Email: hello@ourschoolsoftware.com',
    }
    
    return render(request, 'contact.html', context)


def pricing_view(request):
    return render(request, 'pricing.html')



def features_view(request):

    context = {
        'features': features_info,
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


#========================== LoginPage View ======================================================================
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


#====================== Register View ===================================================================================
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


# ========================= USER FUNCTIONS ==============================================================================
@login_required(login_url='loginPage')
def user_list(request):
    users = User.objects.all().order_by('-date_joined')

    context = {"users": users}
    return render(request,"users/all_users.html", context)


@login_required(login_url='loginPage')
def user_create(request):

    form = UserForm( request.POST or None,request.FILES or None)

    if form.is_valid():
        form.save()

        messages.success(request,"User created successfully.")
        return redirect('user_list')

    context = {"form": form}
    return render(request,"users/user_form.html",context)


@login_required(login_url='loginPage')
def user_update(request, pk):

    user = get_object_or_404(User,pk=pk)

    form = UserForm(request.POST or None,request.FILES or None,instance=user)

    if form.is_valid():
        form.save()

        messages.success(request,"User updated successfully.")
        return redirect('user_list')

    context = {"form": form}
    return render(request,"users/user_form.html",context)


@login_required(login_url='loginPage')
def user_delete(request, pk):

    user = get_object_or_404( User,pk=pk)

    if request.method == "POST":
        user.delete()

        messages.success(request,"User deleted successfully.")
        return redirect("user_list")

    context = {"user": user}
    return render(request,"users/user_confirm_delete.html",context)


# ========================= USER PROFILE VIEW ===========================================================================
@login_required(login_url="loginPage")
def profile(request):

    if request.user.is_admin:
        user_role = "Administrator"

    elif request.user.is_accountant:
        user_role = "Accountant"

    else:
        user_role = "Staff User"

    form = ProfileForm( request.POST or None, request.FILES or None, instance=request.user )

    if request.method == "POST":

        if form.is_valid():
            form.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard")

    context = {"form": form, "user_role": user_role}
    return render(request,"user_profile/profile.html",context)


#=============================== Dashboard ==========================================================================
@login_required(login_url='loginPage')
def dashboard(request):

    now = timezone.now()

    # REFRESH STUDENT FEE STATUS
    students = Student.objects.select_related('class_room')

    for student in students:
        student.update_fee_status()

    # BASIC STATS
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()

    students_this_month = Student.objects.filter(
        created_at__year=now.year,
        created_at__month=now.month).count()

    teachers_this_month = Teacher.objects.filter(
        created_at__year=now.year,
        created_at__month=now.month).count()

    # FINANCIAL STATS
    total_income = Transaction.objects.filter(
        transaction_type='income').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    total_expense = Transaction.objects.filter(
        transaction_type='expense').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    profit = total_income - total_expense

    # RECENT STUDENTS
    recent_students = Student.objects.select_related('class_room','section').order_by('-created_at')[:5]


    # REAL FEE DEFAULTERS 
    defaulters = Student.objects.filter(
        total_fee_due__gt=0  # Only grab students who owe more than $0
    ).select_related('class_room', 'section').order_by('-total_fee_due')[:10]

    # CONTEXT
    context = { "user_role": request.user.role,
        'stats': {
            'students': total_students,
            'student_trend': students_this_month,
            'teachers': total_teachers,
            'teachers_trend': teachers_this_month,
            'classes': total_classes,
            'monthly_revenue': total_income,
            'profit': profit,
        },

        'recent_students': recent_students,
        'defaulters': defaulters,
        'now': now,  
    }
    return render(request, 'dashboard.html', context)


#========================= Teacher Function ===================================================================
@login_required(login_url='loginPage')
@admin_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {"teachers": teachers}
    return render(request, "teachers/all_teacher.html", context)

@login_required(login_url='loginPage')
@admin_required
def teacher_create(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Teacher created successfully")
        return redirect("teacher_list")
    context = {"form":form}
    return render(request, "teachers/teacher_form.html", context)

@login_required(login_url='loginPage')
@admin_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    form = TeacherForm(request.POST or None,request.FILES or None,instance=teacher)

    if form.is_valid():
        form.save()
        messages.success(request, "Teacher updated successfully")
        return redirect("teacher_list")
    context = {"form":form}
    return render(request, "teachers/teacher_form.html", context)

@login_required(login_url='loginPage')
@admin_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    
    # Only delete on POST to prevent accidental/malicious URL hits
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect("teacher_list")
        
    context = {"teacher": teacher}
    return render(request, "teachers/teacher_confirm_delete.html", context)


#========================= Class Function =======================================================================================
@login_required(login_url='loginPage')
@admin_required
def class_list(request):
    classes = Class.objects.prefetch_related('sections').order_by('name')

    context = {"classes": classes}
    return render(request, "classes/all_classes.html", context)


@login_required(login_url='loginPage')
@admin_required
def class_create(request):
    form = ClassForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Class created successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})


@login_required(login_url='loginPage')
@admin_required
def class_update(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    
    form = ClassForm(request.POST or None,request.FILES or None,instance=class_obj)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Class updated successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})


@login_required(login_url='loginPage')
@admin_required
def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect("class_list")

    context = {"class_obj": class_obj}
    return render(request, "classes/class_confirm_delete.html", context)
    

#========================= Section Function =======================================================================================
@login_required(login_url='loginPage')
@admin_required
def section_list(request):
    sections = Section.objects.all()
    return render(request, "sections/all_sections.html", {"sections": sections})

@login_required(login_url='loginPage')
@admin_required
def section_create(request):
    form = SectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Section created successfully")
        return redirect("section_list")
    return render(request, "sections/section_form.html", {"form": form})

@login_required(login_url='loginPage')
@admin_required    
def section_update(request,pk):
    section_obj = get_object_or_404(Section, pk=pk)

    form = SectionForm(request.POST or None,request.FILES or None,instance= section_obj)

    if form.is_valid():
        form.save()
        messages.success(request,"Section updated successfully")
        return redirect("section_list")
    return render(request,"sections/section_form.html",{"form": form})

@login_required(login_url='loginPage')
@admin_required
def section_delete(request,pk):
    section_obj = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section_obj.delete()
        messages.success(request,'Section deleted successfully.')
        return redirect('section_list')
        
    context = {"section_obj": section_obj}
    return render(request,'sections/section_confirm_delete.html',context)


#========================= Student Function =======================================================================================
@login_required(login_url='loginPage')
@admin_required
def student_list(request):
    student = Student.objects.all()
    return render(request,"students/all_student.html",{'student': student})

@login_required(login_url='loginPage')
@admin_required
def student_create(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Student created successfully")
        return redirect("student_list")
    return render(request,"students/student_form.html",{"form": form})

@login_required(login_url='loginPage')
@admin_required
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

@login_required(login_url='loginPage')
@admin_required
def student_delete(request, pk):
    student_obj = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student_obj.delete()
        messages.success(request,'Student deleted successfully.')
        return redirect('student_list')
        
    context = {"student_obj": student_obj}
    return render(request,'students/student_confirm_delete.html',context)


#========================= Transaction Function =======================================================================================
@login_required(login_url='loginPage')
@accountant_required
def all_transactions(request):
    transactions = Transaction.objects.all().order_by('-date', '-created_at')

    total_income = Transaction.objects.filter(transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_expense = Transaction.objects.filter(transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_balance = total_income - total_expense

    context = {'transactions': transactions,'total_income': total_income,
        'total_expense': total_expense,'total_balance': total_balance,
    }

    return render(request, 'transactions/all_transaction.html', context)

@login_required(login_url='loginPage')
@accountant_required
def transaction_list(request):
    # All Transactions
    transactions = Transaction.objects.all().order_by('-date', '-created_at')
    
    # Total Income
    total_income = Transaction.objects.filter(transaction_type='income'
    ).aggregate( total=Sum('amount'))['total'] or 0

    # Total Expense
    total_expense = Transaction.objects.filter(transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Final Balance
    total_balance = total_income - total_expense

    context = {"transactions": transactions,"total_income": total_income,
            "total_expense": total_expense,"total_balance": total_balance,
        }
    return render(request,"transactions/all_transaction.html",context)

@login_required(login_url='loginPage')
@accountant_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # commit=False pauses the save to the database
            transaction = form.save(commit=False)
            # Assign the current logged-in user to the excluded 'recorded_by' field
            transaction.recorded_by = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    
    return render(request, 'transactions/transaction_form.html', {'form': form, 'title': 'Add Transaction'})

@login_required(login_url='loginPage')
@accountant_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)  
    return render(request, 'transactions/transaction_form.html', {'form': form, 'title': 'Edit Transaction'})

@login_required(login_url='loginPage')
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list') 
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})


#========================= Fee Function =======================================================================================
@login_required(login_url='loginPage')
@accountant_required
def fee_list(request):
    fees = Fee.objects.all()
    # TOTAL COLLECTED (PAID + PARTIAL)
    collected_data = Fee.objects.filter(status__in=['paid', 'partial']).aggregate(total=Sum('amount'))
    total_collected = collected_data['total'] or Decimal('0.00')

    # PENDING DUES
    pending_data = Fee.objects.filter(status='pending').aggregate(total=Sum('amount'))
    pending_dues = pending_data['total'] or Decimal('0.00')

    context = {
        "fees": fees,
        "total_collected": total_collected,
        "pending_dues": pending_dues,}

    return render(request, "fees/all_fee.html", context)

@login_required(login_url= 'loginPage')
@accountant_required
def fee_create(request):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.received_by = request.user # Set the received_by field to the current user
            fee.save()
            messages.success(request, 'Fee payment recorded successfully.')
            return redirect('fee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeeForm()

    return render(request, 'fees/fee_form.html', {'form': form, 'title': 'Add Fee'})
    
@login_required(login_url='loginPage')
@accountant_required
def fee_update(request,pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee payment updated successfully.')
            return redirect('fee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeeForm(instance=fee)
    return render(request, 'fees/fee_form.html', {'form': form, 'title': 'Edit Fee'})

@login_required(login_url='loginPage')
@accountant_required
def fee_delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        fee.delete()
        messages.success(request, 'Fee payment deleted successfully.')
        return redirect('fee_list')
    return render(request, 'fees/fee_confirm_delete.html', {'fee': fee})


#========================= Salary Function =======================================================================================
@login_required(login_url='loginPage')
@accountant_required
def salary_list(request):
    salaries = Salary.objects.all().order_by('-created_at')
    # Total Disbursed Salary
    total_disbursed_data = Salary.objects.filter(status='paid'
    ).aggregate(total=Sum('amount'))
    total_disbursed = total_disbursed_data['total'] or Decimal('0.00')

    # Pending Salaries
    pending_salary_data = Salary.objects.filter(status='pending'
    ).aggregate(total=Sum('amount'))
    pending_salaries = pending_salary_data['total'] or Decimal('0.00')

    context = {
        "salaries": salaries,
        "total_disbursed": total_disbursed,
        "pending_salaries": pending_salaries,}

    return render(request, "salaries/all_salary.html", context)

@login_required(login_url='loginPage')
@accountant_required
def salary_create(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)

        if form.is_valid():
            salary = form.save(commit=False)
            salary.paid_by = request.user

            try:
                salary.save()
                messages.success(request, 'Salary payment recorded successfully.')
                return redirect('salary_list')

            except Exception as e:
                messages.error(request, str(e))  
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SalaryForm()
    return render(request, 'salaries/salary_form.html', {'form': form})

@login_required(login_url='loginPage')
@accountant_required
def salary_update(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary payment updated successfully.')
            return redirect('salary_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SalaryForm(instance=salary)
    return render(request, 'salaries/salary_form.html', {'form': form, 'title': 'Edit Salary'})

@login_required(login_url='loginPage')
@accountant_required
def salary_delete(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        salary.delete()
        messages.success(request, 'Salary payment deleted successfully.')
        return redirect('salary_list')
    return render(request, 'salaries/salary_confirm_delete.html', {'salary': salary})


@login_required(login_url='loginPage')
def financial_reports(request):

    now = timezone.now()
    # BASIC COUNTS
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()

    # TRANSACTION TOTALS
    total_income = Transaction.objects.filter( transaction_type='income').aggregate(
    total=Sum('amount'))['total'] or Decimal('0.00')

    total_expense = Transaction.objects.filter(transaction_type='expense').aggregate(
    total=Sum('amount'))['total'] or Decimal('0.00')

    total_balance = total_income - total_expense

    # FEES DATA
    total_collected = Fee.objects.filter(status__in=['paid', 'partial']).aggregate(
    total=Sum('amount'))['total'] or Decimal('0.00')

    pending_dues = Fee.objects.filter(status='pending').aggregate(
    total=Sum('amount'))['total'] or Decimal('0.00')

    # SALARY DATA
    total_salary_paid = Salary.objects.filter(status='paid').aggregate(
    total=Sum('amount'))['total'] or Decimal('0.00')

    pending_salary = Salary.objects.filter(status='pending').aggregate(
    total=Sum('amount'))['total'] or Decimal('0.00')

    # MONTHLY CHART DATA
    months = []
    income_chart = []
    expense_chart = []
    current_year = now.year

    for month in range(1, 13):
        month_name = timezone.datetime(current_year,
            month,
            1
        ).strftime('%b')

        months.append(month_name)

        monthly_income = Transaction.objects.filter(transaction_type='income',date__year=current_year,
        date__month=month).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        monthly_expense = Transaction.objects.filter(transaction_type='expense',date__year=current_year,
                                                     date__month=month).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        income_chart.append(float(monthly_income))
        expense_chart.append(float(monthly_expense))

    # FEE STATUS CHART
    paid_fees = Fee.objects.filter(status='paid').count()
    partial_fees = Fee.objects.filter(status='partial').count()
    pending_fees = Fee.objects.filter(status='pending').count()

    # RECENT TRANSACTIONS
    recent_transactions = Transaction.objects.order_by('-date','-created_at')[:10]
    # CONTEXT
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,

        'total_income': total_income,
        'total_expense': total_expense,
        'total_balance': total_balance,

        'total_collected': total_collected,
        'pending_dues': pending_dues,

        'total_salary_paid': total_salary_paid,
        'pending_salary': pending_salary,

        # Charts
        'months': json.dumps(months),
        'income_chart': json.dumps(income_chart),
        'expense_chart': json.dumps(expense_chart),
        'paid_fees': paid_fees,
        'partial_fees': partial_fees,
        'pending_fees': pending_fees,

        # Transactions
        'recent_transactions': recent_transactions,
    }
    return render(request,'reports/financial_reports.html',context)