from django_filters import FilterSet, OrderingFilter, CharFilter

from arike_app.models import *


class UsersFilter(FilterSet):
    search = CharFilter("first_name", lookup_expr="icontains")
    o = OrderingFilter(fields=["first_name", "facility", "role"])

    class Meta:
        model = User
        fields = ["facility", "role"]


class FacilitiesFilter(FilterSet):
    search = CharFilter("name", lookup_expr="icontains")
    o = OrderingFilter(fields=["name", "ward", "kind"])

    class Meta:
        model = Facility
        fields = ["kind", "ward"]


class WardsFilter(FilterSet):
    search = CharFilter("name", lookup_expr="icontains")
    o = OrderingFilter(fields=("name", "number", "lsg_body"))

    class Meta:
        model = Ward
        fields = ["lsg_body"]


class PatientsFilter(FilterSet):
    search = CharFilter("irst_name", lookup_expr="icontains")
    o = OrderingFilter(fields=["first_name", "date_of_birth", "ward", "facility"])

    class Meta:
        model = Patient
        fields = ["ward", "facility", "gender"]


class LsgBodyFilter(FilterSet):
    search = CharFilter("name", lookup_expr="icontains")
    o = OrderingFilter(fields=["name", "kind", "lsg_body_code"])

    class Meta:
        model = LsgBody
        fields = ["kind", "district"]
