from arike_app.filters import WardsFilter
from arike_app.forms import WardForm
from arike_app.models import Ward
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelListView,
    GenericModelDetailView,
    GenericModelUpdateView,
    GenericModelDeleteView,
)


class __WardsViewsMixin:
    model = Ward
    name = "wards"


class Create(__WardsViewsMixin, GenericModelCreateView):
    form_class = WardForm


class Delete(__WardsViewsMixin, GenericModelDeleteView):
    pass


class Details(__WardsViewsMixin, GenericModelDetailView):
    pass


class Update(__WardsViewsMixin, GenericModelUpdateView):
    form_class = WardForm


class List(__WardsViewsMixin, GenericModelListView):
    filterset_class = WardsFilter

    def get_queryset(self):
        return super().get_queryset().filter(lsg_body__district=self.request.user.district)
