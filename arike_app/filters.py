from django_filters import FilterSet, OrderingFilter

from arike_app.models import *


class UsersFilter(FilterSet):
    o = OrderingFilter(fields=["first_name", "facility", "role"])

    class Meta:
        model = User
        fields = ["first_name", "facility", "role"]


class FacilitiesFilter(FilterSet):
    o = OrderingFilter(fields=["name", "ward", "kind"])

    class Meta:
        model = Facility
        fields = ["kind", "name", "ward"]


class WardsFilter(FilterSet):
    o = OrderingFilter(fields=["name", "number", "lsg_body"])

    class Meta:
        model = Ward
        fields = ["name", "lsg_body"]


class PatientsFilter(FilterSet):
    o = OrderingFilter(fields=["first_name", "date_of_birth", "ward", "facility"])

    class Meta:
        model = Patient
        fields = [
            "first_name",
            "ward",
            "facility",
            "gender",
        ]


class LsgBodyFilter(FilterSet):
    o = OrderingFilter(fields=["name", "kind", "lsg_body_code"])

    class Meta:
        model = LsgBody
        fields = ["kind", "district"]
