from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SectionForm
from .models import  Section

from django.shortcuts import get_object_or_404, redirect, render
from base.decorators import accountant_required

# ========================= Section Function =======================================================================================
@login_required(login_url="loginPage")
@accountant_required
def section_list(request):
    sections = Section.objects.all()
    return render(request, "sections/all_sections.html", {"sections": sections})


@login_required(login_url="loginPage")
@accountant_required
def section_create(request):
    form = SectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Section created successfully")
        return redirect("section_list")
    return render(request, "sections/section_form.html", {"form": form})


@login_required(login_url="loginPage")
@accountant_required
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
@accountant_required
def section_delete(request, pk):
    section_obj = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        section_obj.delete()
        messages.success(request, "Section deleted successfully.")
        return redirect("section_list")

    context = {"section_obj": section_obj}
    return render(request, "sections/section_confirm_delete.html", context)

