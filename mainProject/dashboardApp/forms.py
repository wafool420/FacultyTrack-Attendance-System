from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AttendanceEntry

class RegisterUserForm(UserCreationForm):

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]

class AttendanceEntryForm(forms.ModelForm):
    class Meta:
        model = AttendanceEntry
        fields = ["name", "campus", "sex", "signature_image"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name"
            }),
            "campus": forms.Select(attrs={"class": "form-select"}),
            "sex": forms.Select(attrs={"class": "form-select"}),
            "signature_image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            }),
        }