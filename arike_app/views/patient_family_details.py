from arike_app.forms import PatientFamilyDetailForm
from arike_app.models import FamilyDetail
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelDeleteView,
    GenericModelDetailView,
    GenericModelListView,
    GenericModelUpdateView,
)
from arike_app.views.mixins import PatientRelatedViewMixin


class _ViewMixin(PatientRelatedViewMixin):
    model = FamilyDetail
    name = "patient_family_details"


class Create(_ViewMixin, GenericModelCreateView):
    form_class = PatientFamilyDetailForm


class List(_ViewMixin, GenericModelListView):
    pass


class Details(_ViewMixin, GenericModelDetailView):
    pass


class Update(_ViewMixin, GenericModelUpdateView):
    form_class = PatientFamilyDetailForm


class Delete(_ViewMixin, GenericModelDeleteView):
    pass
