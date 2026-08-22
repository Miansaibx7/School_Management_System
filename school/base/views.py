import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SalaryForm 
from .models import  Salary

from teacher.models import Teacher
from class_room.models import Class
from students.models import Student
from transaction.models import Transaction
from fees.models import Fee

from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import accountant_required


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
