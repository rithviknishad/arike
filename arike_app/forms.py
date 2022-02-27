from django.contrib.auth import forms
from arike_app.models import *


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "phone",
            "facility",
            "role",
        ]


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "facility", "role"]
