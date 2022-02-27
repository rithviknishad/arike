from dataclasses import field
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm
from arike_app.models import *


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "facility", "role"]


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", *UserChangeForm.Meta.fields]


class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = ["kind", "name", "address", "ward", "pincode", "phone"]
