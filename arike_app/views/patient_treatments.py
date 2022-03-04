from arike_app.forms import PatientTreatmentForm
from arike_app.models import Treatment
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelDeleteView,
    GenericModelDetailView,
    GenericModelListView,
    GenericModelUpdateView,
)
from arike_app.views.mixins import PatientRelatedViewMixin


class _ViewMixin(PatientRelatedViewMixin):
    model = Treatment
    name = "patient_treatments"


class Create(_ViewMixin, GenericModelCreateView):
    form_class = PatientTreatmentForm


class List(_ViewMixin, GenericModelListView):
    pass


class Details(_ViewMixin, GenericModelDetailView):
    pass


class Update(_ViewMixin, GenericModelUpdateView):
    form_class = PatientTreatmentForm


class Delete(_ViewMixin, GenericModelDeleteView):
    pass
