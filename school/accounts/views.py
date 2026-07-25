from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Import the User model and forms from the same app
from .models import User
from .forms import MyUserCreationForm, UserForm, ProfileForm

# Import decorators from your main app (or move them to a shared location)
from base.decorators import admin_required 




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


# ========================= USER FUNCTIONS ==========================
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


# ========================= USER PROFILE VIEW ==========================
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