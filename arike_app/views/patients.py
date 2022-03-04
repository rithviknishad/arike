from django.http import HttpResponse

from arike_app.filters import PatientsFilter
from arike_app.forms import PatientForm
from arike_app.models import Patient
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelListView,
    GenericModelDetailView,
    GenericModelUpdateView,
    GenericModelDeleteView,
)


class __PatientsViewMixin:
    model = Patient
    name = "patients"


class Create(__PatientsViewMixin, GenericModelCreateView):
    form_class = PatientForm

    def form_valid(self, form) -> HttpResponse:
        res = super().form_valid(form)
        self.object.facility = self.request.user.facility
        self.object.save()
        return res


class Delete(__PatientsViewMixin, GenericModelDeleteView):
    pass


class Details(__PatientsViewMixin, GenericModelDetailView):
    pass


class Update(__PatientsViewMixin, GenericModelUpdateView):
    form_class = PatientForm


class List(__PatientsViewMixin, GenericModelListView):
    filterset_class = PatientsFilter

    def get_queryset(self):
        return super().get_queryset().filter(facility=self.request.user.facility)
