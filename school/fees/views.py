from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FeeForm
from .models import  Fee

from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from base.decorators import accountant_required

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