
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ClassForm
from .models import Class

from django.shortcuts import get_object_or_404, redirect, render
from base.decorators import accountant_required

# ========================= Class Function =======================================================================================
@login_required(login_url="loginPage")
@accountant_required
def class_list(request):
    classes = Class.objects.prefetch_related("sections").order_by("name")

    context = {"classes": classes}
    return render(request, "classes/all_classes.html", context)


@login_required(login_url="loginPage")
@accountant_required
def class_create(request):
    form = ClassForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Class created successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})


@login_required(login_url="loginPage")
@accountant_required
def class_update(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    form = ClassForm(request.POST or None, request.FILES or None, instance=class_obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Class updated successfully")
        return redirect("class_list")
    return render(request, "classes/classes_form.html", {"form": form})


@login_required(login_url="loginPage")
@accountant_required
def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == "POST":
        class_obj.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect("class_list")

    context = {"class_obj": class_obj}
    return render(request, "classes/class_confirm_delete.html", context)

