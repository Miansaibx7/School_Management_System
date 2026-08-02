from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import logging

from .models import User
from .forms import MyUserCreationForm, UserForm, ProfileForm
from .data.faqs import CONTACT_FAQS
from .data.features import features_info
from base.decorators import admin_required  # FIX: now actually used below

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html', {})


# ========================= CONTACT VIEW WITH FAQS AND EMAIL NOTIFICATIONS ==========================
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter')

        try:
            email_subject = f"New Contact Form Submission: {subject}"
            email_message = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Subject: {subject}\n\n"
                f"Message:\n{message}\n\n"
                f"Newsletter Subscription: {'Yes' if newsletter else 'No'}"
            )

            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                # FIX: pull recipient from settings instead of hardcoding it here,
                # so changing the inbox doesn't require a code deploy.
                [settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )

            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')

        except Exception:
            # FIX: log the real exception (stack trace) instead of swallowing it —
            # the old code caught `as e` and never used it, so failures were
            # invisible in production logs.
            logger.exception("Failed to send contact form email")
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')

    context = {
        'faqs': CONTACT_FAQS,
        'page_title': 'Contact Us - School Management System',
        'meta_description': 'Get in touch with us for school management software inquiries. '
                             'WhatsApp: +92 306 8363688, Email: hello@ourschoolsoftware.com',
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
    return render(request, 'about.html', {})


def learn_more(request):
    context = {
        'title': 'Learn More - School Management System',
        'meta_description': 'Discover powerful features of our school management system.',
    }
    return render(request, 'learn_more.html', context)


# ========================== LoginPage View ======================================================================
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

    return render(request, 'login.html', {'page': page})


def Logoutpage(request):
    logout(request)
    return redirect('home')


# ====================== Register View ===================================================================================
def Register(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            # FIX: email is already normalized/lowercased in form.clean_email()
            # now, so no need to touch it again here, and no risk of the
            # unhandled IntegrityError the old post-validation lowering could cause.
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            # FIX: surface the actual validation error instead of a generic
            # message, so the user knows *why* (e.g. "email already exists").
            first_error = next(iter(form.errors.values()))[0]
            messages.error(request, first_error)

    return render(request, 'login.html', {'form': form})


# ========================= USER FUNCTIONS ==============================================================================
# FIX: every view below now requires @admin_required in addition to
# @login_required — this was the critical privilege-escalation gap.

@login_required(login_url='loginPage')
@admin_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, "users/all_users.html", {"users": users})


@login_required(login_url='loginPage')
@admin_required
def user_create(request):
    form = UserForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, "User created successfully.")
        return redirect('user_list')

    return render(request, "users/user_form.html", {"form": form})


@login_required(login_url='loginPage')
@admin_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, request.FILES or None, instance=user)

    if form.is_valid():
        form.save()
        messages.success(request, "User updated successfully.")
        return redirect('user_list')

    return render(request, "users/user_form.html", {"form": form})


@login_required(login_url='loginPage')
@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("user_list")

    return render(request, "users/user_confirm_delete.html", {"user": user})


# ========================= USER PROFILE VIEW ===========================================================================
@login_required(login_url="loginPage")
def profile(request):
    # FIX: reuse the model's own `role` property instead of re-deriving it here.
    # The old inline logic never checked is_superuser, so a superuser incorrectly
    # saw "Staff User" on their own profile page.
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("dashboard")

    return render(request, "user_profile/profile.html", {
        "form": form,
        "user_role": request.user.role,
    })