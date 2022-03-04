from arike_app.filters import LsgBodyFilter
from arike_app.forms import LsgBodyForm
from arike_app.models import LsgBody
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelListView,
    GenericModelDetailView,
    GenericModelUpdateView,
    GenericModelDeleteView,
)


class __LsgBodiesViewMixin:
    model = LsgBody
    name = "lsg_bodies"


class Create(__LsgBodiesViewMixin, GenericModelCreateView):
    form_class = LsgBodyForm


class Delete(__LsgBodiesViewMixin, GenericModelDeleteView):
    pass


class Details(__LsgBodiesViewMixin, GenericModelDetailView):
    pass


class Update(__LsgBodiesViewMixin, GenericModelUpdateView):
    form_class = LsgBodyForm


class List(__LsgBodiesViewMixin, GenericModelListView):
    filterset_class = LsgBodyFilter

    def get_queryset(self):
        return super().get_queryset().filter(district=self.request.user.district)
