from arike_app.filters import FacilitiesFilter
from arike_app.forms import FacilityForm
from arike_app.models import Facility
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelListView,
    GenericModelDetailView,
    GenericModelUpdateView,
    GenericModelDeleteView,
)


class __FacilitiesViewMixin:
    model = Facility
    name = "facilities"


class Create(__FacilitiesViewMixin, GenericModelCreateView):
    form_class = FacilityForm


class Delete(__FacilitiesViewMixin, GenericModelDeleteView):
    pass


class Details(__FacilitiesViewMixin, GenericModelDetailView):
    pass


class Update(__FacilitiesViewMixin, GenericModelUpdateView):
    form_class = FacilityForm


class List(__FacilitiesViewMixin, GenericModelListView):
    filterset_class = FacilitiesFilter

    def get_queryset(self):
        return super().get_queryset().filter(ward__lsg_body__district=self.request.user.district)
