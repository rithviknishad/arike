from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm, ValidationError, HiddenInput, DateInput, DateTimeInput
from arike_app.models import *
from arike_app.mixins import CustomFormStyleMixin
from arike_app.views.schedule import VisitPatient


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
        fields = ["kind", "name", "lsg_body_code"]


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
            "gender",
        ]
        widgets = {
            "date_of_birth": DateInput(attrs={"type": "date"}),
        }


class PatientFamilyDetailForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = FamilyDetail
        fields = [
            "full_name",
            "phone",
            "date_of_birth",
            "email",
            "relation",
            "address",
            "education",
            "occupation",
            "remarks",
            "is_primary",
        ]
        widgets = {
            "date_of_birth": DateInput(attrs={"type": "date"}),
        }


class PatientDiseaseForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = PatientDisease
        fields = ["disease", "note"]


class PatientTreatmentForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = Treatment
        fields = ["care_type_and_sub_type", "description"]


class ScheduleVisitForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = VisitSchedule
        fields = ["schedule_time", "duration"]
        widgets = {
            "schedule_time": DateTimeInput(attrs={"type": "datetime-local"}),
        }


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


class VisitDetailsForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = VisitDetails
        fields = [
            "palliative_phase",
            "blood_pressure",
            "pulse",
            "general_random_blood_sugar",
            "personal_hygiene",
            "mouth_hygiene",
            "public_hygiene",
            "systemic_examination",
            "systemic_examination_details",
            "patient_at_peace",
            "pain",
            "notes",
            "treatment_notes",
        ]


class ProfileForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]


class ProfileReportConfigFOrm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = UserReportConfiguration
        fields = ["preferred_time"]


class WardForm(CustomFormStyleMixin, ModelForm):
    class Meta:
        model = Ward
        fields = ["number", "name", "lsg_body"]
