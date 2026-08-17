from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction

from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from base.decorators import accountant_required

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

