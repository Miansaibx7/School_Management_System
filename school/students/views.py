from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import  StudentForm
from .models import Student

from django.shortcuts import get_object_or_404, redirect, render
from base.decorators import admin_required

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
