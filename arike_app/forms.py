from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm, ValidationError, HiddenInput
from arike_app.models import *
from arike_app.mixins import CustomFormStyleMixin


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
        fields = ["first_name", "last_name", "email", "phone", "facility", "role"]


class UserCreationForm(CustomFormStyleMixin, auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ["username", *UserChangeForm.Meta.fields]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["password1"].required = False
        self.fields["password2"].required = False
        self.fields["password1"].widget.attrs["autocomplete"] = "off"
        self.fields["password2"].widget.attrs["autocomplete"] = "off"
        self.fields["password1"].widget = HiddenInput()
        self.fields["password2"].widget = HiddenInput()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise ValidationError("Fill out both fields")
        return password2


# class ProfileForm(ModelForm):
#     class Meta:
#         model = User
#         fields = UserCreationForm.Meta.fields


class WardForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = Ward
        fields = ["number", "name", "lsg_body"]
