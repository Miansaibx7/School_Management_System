import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import accountant_required, admin_required
from .forms import (ClassForm, FeeForm, SalaryForm, SectionForm, StudentForm,
    TeacherForm, TransactionForm )
from .models import Class, Fee, Salary, Section, Student, Teacher, Transaction


@login_required(login_url="loginPage")
def dashboard(request):

    now = timezone.now()
    # REFRESH STUDENT FEE STATUS
    students = Student.objects.select_related("class_room")

    for student in students:
        student.update_fee_status()

    # BASIC STATS
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()

    students_this_month = Student.objects.filter(created_at__year=now.year, created_at__month=now.month).count()
    teachers_this_month = Teacher.objects.filter(created_at__year=now.year, created_at__month=now.month).count()

    # FINANCIAL STATS
    total_income = Transaction.objects.filter(transaction_type="income").aggregate( total=Sum("amount"))["total"] or Decimal("0.00")
    total_expense = Transaction.objects.filter(transaction_type="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    profit = total_income - total_expense

    # RECENT STUDENTS
    recent_students = Student.objects.select_related("class_room", "section").order_by("-created_at")[:5]

    # REAL FEE DEFAULTERS (IMPORTANT FIX)
    defaulters = (Student.objects.annotate(paid=Coalesce(Sum("fee_payments__amount"), Decimal("0.00"))
        ).filter(paid__lt=F("class_room__monthly_fee")).order_by("paid")[:10]
    )

    # CONTEXT
    context = {
        "user_role": request.user.role,
        "stats": {
            "students": total_students,
            "student_trend": students_this_month,
            "teachers": total_teachers,
            "teachers_trend": teachers_this_month,
            "classes": total_classes,
            "monthly_revenue": total_income,
            "profit": profit,
        },
        "recent_students": recent_students,
        "defaulters": defaulters,
        "now": now,
    }
    return render(request, "dashboard.html", context)


# ========================= Teacher Function ===================================================================
@login_required(login_url="loginPage")
@admin_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {"teachers": teachers}
    return render(request, "teachers/all_teacher.html", context)


@login_required(login_url="loginPage")
@admin_required
def teacher_create(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Teacher created successfully")
        return redirect("teacher_list")
    context = {"form": form}
    return render(request, "teachers/teacher_form.html", context)


@login_required(login_url="loginPage")
@admin_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
    if form.is_valid():
        form.save()
        messages.success(request, "Teacher updated successfully")
        return redirect("teacher_list")
    context = {"form": form}
    return render(request, "teachers/teacher_form.html", context)


@login_required(login_url="loginPage")
@admin_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    # Only delete on POST to prevent accidental/malicious URL hits
    if request.method == "POST":
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect("teacher_list")

    context = {"teacher": teacher}
    return render(request, "teachers/teacher_confirm_delete.html", context)


# ========================= Class Function =======================================================================================
@login_required(login_url="loginPage")
@admin_required
def class_list(request):
    classes = Class.objects.prefetch_related("sections").order_by("name")

    context = {"classes": classes}
    return render(request, "classes/all_classes.html", context)


@login_required(login_url="loginPage")
@admin_required
def class_create(request):
    form = ClassForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Class created successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})


@login_required(login_url="loginPage")
@admin_required
def class_update(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    form = ClassForm(request.POST or None, request.FILES or None, instance=class_obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Class updated successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})


@login_required(login_url="loginPage")
@admin_required
def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == "POST":
        class_obj.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect("class_list")

    context = {"class_obj": class_obj}
    return render(request, "classes/class_confirm_delete.html", context)


# ========================= Section Function =======================================================================================
@login_required(login_url="loginPage")
@admin_required
def section_list(request):
    sections = Section.objects.all()
    return render(request, "sections/all_sections.html", {"sections": sections})


@login_required(login_url="loginPage")
@admin_required
def section_create(request):
    form = SectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Section created successfully")
        return redirect("section_list")
    return render(request, "sections/section_form.html", {"form": form})


@login_required(login_url="loginPage")
@admin_required
def section_update(request, pk):
    section_obj = get_object_or_404(Section, pk=pk)
    form = SectionForm(
        request.POST or None, request.FILES or None, instance=section_obj
    )
    if form.is_valid():
        form.save()
        messages.success(request, "Section updated successfully")
        return redirect("section_list")
    return render(request, "sections/section_form.html", {"form": form})


@login_required(login_url="loginPage")
@admin_required
def section_delete(request, pk):
    section_obj = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        section_obj.delete()
        messages.success(request, "Section deleted successfully.")
        return redirect("section_list")

    context = {"section_obj": section_obj}
    return render(request, "sections/section_confirm_delete.html", context)


# ========================= Student Function =======================================================================================
@login_required(login_url="loginPage")
@admin_required
def student_list(request):
    student = Student.objects.all()
    return render(request, "students/all_student.html", {"student": student})


@login_required(login_url="loginPage")
@admin_required
def student_create(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Student created successfully")
        return redirect("student_list")
    return render(request, "students/student_form.html", {"form": form})


@login_required(login_url="loginPage")
@admin_required
def student_update(request, pk):
    student_obj = get_object_or_404(Student, pk=pk)
    form = StudentForm(
        request.POST or None, request.FILES or None, instance=student_obj
    )
    if form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully")
        return redirect("student_list")
    return render(request, "students/student_form.html", {"form": form})


@login_required(login_url="loginPage")
@admin_required
def student_delete(request, pk):
    student_obj = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student_obj.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")

    context = {"student_obj": student_obj}
    return render(request, "students/student_confirm_delete.html", context)


# ========================= Transaction Function =======================================================================================
@login_required(login_url="loginPage")
@accountant_required
def all_transactions(request):
    transactions = Transaction.objects.all().order_by("-date", "-created_at")

    total_income = Transaction.objects.filter(transaction_type="income").aggregate(total=Sum("amount"))["total"] or 0
    total_expense = Transaction.objects.filter(transaction_type="expense").aggregate(total=Sum("amount"))["total"] or 0
    
    total_balance = total_income - total_expense

    context = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_balance": total_balance,
    }

    return render(request, "transactions/all_transaction.html", context)


@login_required(login_url="loginPage")
@accountant_required
def transaction_list(request):
    # All Transactions
    transactions = Transaction.objects.all().order_by("-date", "-created_at")

    # Total Income
    total_income = (
        Transaction.objects.filter(transaction_type="income").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    # Total Expense
    total_expense = (
        Transaction.objects.filter(transaction_type="expense").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    # Final Balance
    total_balance = total_income - total_expense

    context = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_balance": total_balance,
    }
    return render(request, "transactions/all_transaction.html", context)


@login_required(login_url="loginPage")
@accountant_required
def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            # commit=False pauses the save to the database
            transaction = form.save(commit=False)
            # Assign the current logged-in user to the excluded 'recorded_by' field
            transaction.recorded_by = request.user
            transaction.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm()

    return render(
        request,
        "transactions/transaction_form.html",
        {"form": form, "title": "Add Transaction"},
    )


@login_required(login_url="loginPage")
@accountant_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=transaction)
    return render(
        request,
        "transactions/transaction_form.html",
        {"form": form, "title": "Edit Transaction"},
    )


@login_required(login_url="loginPage")
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        transaction.delete()
        return redirect("transaction_list")
    return render(
        request,
        "transactions/transaction_confirm_delete.html",
        {"transaction": transaction},
    )


# ========================= Fee Function =======================================================================================
@login_required(login_url="loginPage")
@accountant_required
def fee_list(request):
    fees = Fee.objects.all()
    # TOTAL COLLECTED (PAID + PARTIAL)
    collected_data = Fee.objects.filter(status__in=["paid", "partial"]).aggregate(total=Sum("amount"))
    total_collected = collected_data["total"] or Decimal("0.00")

    # PENDING DUES
    pending_data = Fee.objects.filter(status="pending").aggregate(total=Sum("amount"))
    pending_dues = pending_data["total"] or Decimal("0.00")

    context = {
        "fees": fees,
        "total_collected": total_collected,
        "pending_dues": pending_dues,
    }

    return render(request, "fees/all_fee.html", context)


@login_required(login_url="loginPage")
@accountant_required
def fee_create(request):
    if request.method == "POST":
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.received_by = (request.user)  # Set the received_by field to the current user
            fee.save()
            messages.success(request, "Fee payment recorded successfully.")
            return redirect("fee_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeeForm()

    return render(request, "fees/fee_form.html", {"form": form, "title": "Add Fee"})


@login_required(login_url="loginPage")
@accountant_required
def fee_update(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == "POST":
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee payment updated successfully.")
            return redirect("fee_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeeForm(instance=fee)
    return render(request, "fees/fee_form.html", {"form": form, "title": "Edit Fee"})


@login_required(login_url="loginPage")
@accountant_required
def fee_delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == "POST":
        fee.delete()
        messages.success(request, "Fee payment deleted successfully.")
        return redirect("fee_list")
    return render(request, "fees/fee_confirm_delete.html", {"fee": fee})


# ========================= Salary Function =======================================================================================
@login_required(login_url="loginPage")
@accountant_required
def salary_list(request):
    salaries = Salary.objects.all().order_by("-created_at")
    # Total Disbursed Salary
    total_disbursed_data = Salary.objects.filter(status="paid").aggregate(
        total=Sum("amount")
    )
    total_disbursed = total_disbursed_data["total"] or Decimal("0.00")

    # Pending Salaries
    pending_salary_data = Salary.objects.filter(status="pending").aggregate(
        total=Sum("amount")
    )
    pending_salaries = pending_salary_data["total"] or Decimal("0.00")

    context = {
        "salaries": salaries,
        "total_disbursed": total_disbursed,
        "pending_salaries": pending_salaries,
    }

    return render(request, "salaries/all_salary.html", context)


@login_required(login_url="loginPage")
@accountant_required
def salary_create(request):
    if request.method == "POST":
        form = SalaryForm(request.POST)

        if form.is_valid():
            salary = form.save(commit=False)
            salary.paid_by = request.user

            try:
                salary.save()
                messages.success(request, "Salary payment recorded successfully.")
                return redirect("salary_list")

            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SalaryForm()
    return render(request, "salaries/salary_form.html", {"form": form})


@login_required(login_url="loginPage")
@accountant_required
def salary_update(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == "POST":
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary payment updated successfully.")
            return redirect("salary_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SalaryForm(instance=salary)
    return render(
        request, "salaries/salary_form.html", {"form": form, "title": "Edit Salary"}
    )


@login_required(login_url="loginPage")
@accountant_required
def salary_delete(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == "POST":
        salary.delete()
        messages.success(request, "Salary payment deleted successfully.")
        return redirect("salary_list")
    return render(request, "salaries/salary_confirm_delete.html", {"salary": salary})


@login_required(login_url="loginPage")
def financial_reports(request):

    now = timezone.now()
    # BASIC COUNTS
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()

    # TRANSACTION TOTALS
    total_income = Transaction.objects.filter(transaction_type="income").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    total_expense = Transaction.objects.filter(transaction_type="expense").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    total_balance = total_income - total_expense

    # FEES DATA
    total_collected = Fee.objects.filter(status__in=["paid", "partial"]).aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    pending_dues = Fee.objects.filter(status="pending").aggregate(total=Sum("amount"))[
        "total"
    ] or Decimal("0.00")

    # SALARY DATA
    total_salary_paid = Salary.objects.filter(status="paid").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    pending_salary = Salary.objects.filter(status="pending").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    # MONTHLY CHART DATA
    months = []
    income_chart = []
    expense_chart = []
    current_year = now.year

    for month in range(1, 13):
        month_name = timezone.datetime(current_year, month, 1).strftime("%b")

        months.append(month_name)

        monthly_income = Transaction.objects.filter(
            transaction_type="income", date__year=current_year, date__month=month
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        monthly_expense = Transaction.objects.filter(
            transaction_type="expense", date__year=current_year, date__month=month
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        income_chart.append(float(monthly_income))
        expense_chart.append(float(monthly_expense))

    # FEE STATUS CHART
    paid_fees = Fee.objects.filter(status="paid").count()
    partial_fees = Fee.objects.filter(status="partial").count()
    pending_fees = Fee.objects.filter(status="pending").count()

    # RECENT TRANSACTIONS
    recent_transactions = Transaction.objects.order_by("-date", "-created_at")[:10]
    # CONTEXT
    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_classes": total_classes,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_balance": total_balance,
        "total_collected": total_collected,
        "pending_dues": pending_dues,
        "total_salary_paid": total_salary_paid,
        "pending_salary": pending_salary,
        # Charts
        "months": json.dumps(months),
        "income_chart": json.dumps(income_chart),
        "expense_chart": json.dumps(expense_chart),
        "paid_fees": paid_fees,
        "partial_fees": partial_fees,
        "pending_fees": pending_fees,
        # Transactions
        "recent_transactions": recent_transactions,
    }
    return render(request, "reports/financial_reports.html", context)
