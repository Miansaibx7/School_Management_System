from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from base.decorators import admin_required
from django.contrib.auth.decorators import login_required

from .models import Teacher
from .forms import TeacherForm




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

