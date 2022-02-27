from dataclasses import field
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm, Form
from arike_app.models import *


class CustomFormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_field_style = "bg-white rounded-xl w-full py-2 px-4"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = text_field_style
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label


class LoginForm(CustomFormStyleMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        text_field_style = "bg-gray-200 rounded-xl w-full py-2 px-4"
        for field in ["username", "password"]:
            self.fields[field].widget.attrs["class"] = text_field_style
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label


class ProfileForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class FacilityForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = Facility
        fields = ["kind", "name", "address", "ward", "pincode", "phone"]


class LsgBodyForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = LsgBody
        fields = ["kind", "name", "lsg_body_code", "district"]


class PatientForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone_number",
            "emergency_phone_number",
            "address",
            "landmark",
            "ward",
            "facility",
            "gender",
        ]


class UserChangeForm(CustomFormStyleMixin, auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "district", "facility", "role"]


class UserCreationForm(CustomFormStyleMixin, auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", *UserChangeForm.Meta.fields]


# class ProfileForm(ModelForm):
#     class Meta:
#         model = User
#         fields = UserCreationForm.Meta.fields


class WardForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = Ward
        fields = ["number", "name", "lsg_body"]
