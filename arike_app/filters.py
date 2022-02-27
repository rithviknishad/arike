from django_filters import FilterSet

from arike_app.models import *


class UsersFilter(FilterSet):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "facility", "role"]


class FacilitiesFilter(FilterSet):
    class Meta:
        model = Facility
        fields = ["kind", "name", "address", "ward", "pincode", "phone"]


class WardsFilter(FilterSet):
    class Meta:
        model = Ward
        fields = ["number", "name", "lsg_body"]


class PatientsFilter(FilterSet):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone_number",
            "address",
            "landmark",
            "ward",
            "facility",
            "gender",
        ]


class LsgBodyForm(FilterSet):
    class Meta:
        model = LsgBody
        fields = ["kind", "name", "lsg_body_code", "district"]
