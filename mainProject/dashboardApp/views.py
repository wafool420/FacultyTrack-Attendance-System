from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import RegisterUserForm
from .models import Profile


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request, "Incorrect user or password.")
            return redirect("login")

    return render(request, "authentication/login.html", {})


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.create(user=user, status="Pending")

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = RegisterUserForm()

    return render(request, "authentication/register.html", {
        "form": form,
    })


@login_required
def home(request):
    if request.user.profile.status != "Approved":
        return render(request, "app/pending_approval.html")

    return render(request, "app/home.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("login")

    return render(request, "authentication/delete_account.html")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "authentication/change_password.html", {
        "form": form,
    })


@login_required
def incoming_requests(request):
    if request.user.profile.position != "Administrator" or request.user.profile.status != "Approved":
        return redirect("home")

    selected_status = request.GET.get("status", "All")

    all_profiles = Profile.objects.all()

    if selected_status == "Approved":
        profiles = all_profiles.filter(status="Approved")
    elif selected_status == "Rejected":
        profiles = all_profiles.filter(status="Rejected")
    else:
        profiles = all_profiles.filter(status="Pending")

    return render(request, "app/incoming_requests.html", {
        "profiles": profiles,
        "selected_status": selected_status,
        "total_requests": all_profiles.filter(status="Pending").count(),
        "pending_count": all_profiles.filter(status="Pending").count(),
        "approved_count": all_profiles.filter(status="Approved").count(),
        "rejected_count": all_profiles.filter(status="Rejected").count(),
    })


@login_required
def approve_user(request, profile_id):
    if request.user.profile.position != "Administrator" or request.user.profile.status != "Approved":
        return redirect("home")

    profile = Profile.objects.get(id=profile_id)
    profile.status = "Approved"
    profile.save()

    return redirect("incoming_requests")


@login_required
def reject_user(request, profile_id):
    if request.user.profile.position != "Administrator" or request.user.profile.status != "Approved":
        return redirect("home")

    profile = Profile.objects.get(id=profile_id)
    profile.status = "Rejected"
    profile.save()

    return redirect("incoming_requests")


@login_required
def delete_rejected_user(request, profile_id):
    if request.user.profile.position != "Administrator" or request.user.profile.status != "Approved":
        return redirect("home")

    profile = Profile.objects.get(id=profile_id)
    user = profile.user
    user.delete()

    return redirect("incoming_requests")

@login_required
def remove_approved_user(request, profile_id):
    if request.user.profile.position != "Administrator" or request.user.profile.status != "Approved":
        return redirect("home")

    profile = Profile.objects.get(id=profile_id)
    profile.status = "Pending"
    profile.save()

    return redirect("incoming_requests")