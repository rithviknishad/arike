from arike_app.forms import ScheduleVisitForm
from arike_app.models import VisitSchedule
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelDeleteView,
    GenericModelDetailView,
    GenericModelListView,
    GenericModelUpdateView,
)
from arike_app.views.mixins import PatientRelatedViewMixin


class _ViewMixin(PatientRelatedViewMixin):
    model = VisitSchedule
    name = "patient_visits"


class Create(_ViewMixin, GenericModelCreateView):
    form_class = ScheduleVisitForm

    def pre_save_object(self) -> None:
        super().pre_save_object()
        self.object.nurse = self.request.user


class List(_ViewMixin, GenericModelListView):
    pass


class Details(_ViewMixin, GenericModelDetailView):
    pass


class Update(_ViewMixin, GenericModelUpdateView):
    form_class = ScheduleVisitForm


class Delete(_ViewMixin, GenericModelDeleteView):
    pass
