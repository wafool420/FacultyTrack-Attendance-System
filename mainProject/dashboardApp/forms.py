from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    POSITION_CHOICES = [
        ("Staff", "Staff"),
        ("Administrator", "Administrator"),
    ]

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    position = forms.ChoiceField(choices=POSITION_CHOICES, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "position",
            "password1",
            "password2",
        ]