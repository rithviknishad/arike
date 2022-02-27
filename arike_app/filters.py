from django_filters import FilterSet

from arike_app.models import *


class FacilitiesFilter(FilterSet):
    class Meta:
        model = Facility
        fields = ["kind", "name", "address", "ward", "pincode", "phone"]
