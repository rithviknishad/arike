from django_filters import FilterSet, OrderingFilter

from arike_app.models import *


class UsersFilter(FilterSet):
    o = OrderingFilter(fields=["first_name", "facility", "role"])

    class Meta:
        model = User
        fields = ["first_name", "facility", "role"]


class FacilitiesFilter(FilterSet):
    class Meta:
        model = Facility
        fields = ["kind", "name", "ward"]


class WardsFilter(FilterSet):
    class Meta:
        model = Ward
        fields = ["name", "lsg_body"]


class PatientsFilter(FilterSet):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "ward",
            "facility",
            "gender",
        ]


class LsgBodyFilter(FilterSet):
    class Meta:
        model = LsgBody
        fields = ["kind", "district"]
