from arike_app.forms import PatientDiseaseForm
from arike_app.models import PatientDisease
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelDeleteView,
    GenericModelDetailView,
    GenericModelListView,
    GenericModelUpdateView,
)
from arike_app.views.mixins import PatientRelatedViewMixin


class _ViewMixin(PatientRelatedViewMixin):
    model = PatientDisease
    name = "patient_disease_history"


class Create(_ViewMixin, GenericModelCreateView):
    form_class = PatientDiseaseForm


class List(_ViewMixin, GenericModelListView):
    pass


class Details(_ViewMixin, GenericModelDetailView):
    pass


class Update(_ViewMixin, GenericModelUpdateView):
    form_class = PatientDiseaseForm


class Delete(_ViewMixin, GenericModelDeleteView):
    pass
