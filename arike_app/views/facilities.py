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
    form_class = FacilityForm
    filterset_class = FacilitiesFilter


class Create(__FacilitiesViewMixin, GenericModelCreateView):
    pass


class Delete(__FacilitiesViewMixin, GenericModelDeleteView):
    pass


class Details(__FacilitiesViewMixin, GenericModelDetailView):
    pass


class Update(__FacilitiesViewMixin, GenericModelUpdateView):
    pass


class List(__FacilitiesViewMixin, GenericModelListView):
    def get_queryset(self):
        return super().get_queryset().filter(ward__lsg_body__district=self.request.user.district)
