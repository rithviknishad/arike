from datetime import datetime

from arike_app.filters import FacilitiesFilter
from arike_app.forms import FacilityForm
from arike_app.models import VisitSchedule, Patient
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelListView,
    GenericModelDetailView,
    GenericModelUpdateView,
    GenericModelDeleteView,
)
from arike_app.models import VisitSchedule


class __ScheduleViewsMixin:
    model = VisitSchedule
    name = "schedule"


class List(__ScheduleViewsMixin, GenericModelListView):
    model = Patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Overriding to disable New button from being shown, as create (schedule a visit) is done by clicking on the patient card.
        context["has_create_perm"] = False
        return context

    def get_queryset(self):
        return super().get_queryset().filter(facility=self.request.user.facility)


class Agenda(__ScheduleViewsMixin, GenericModelListView):
    model = VisitSchedule
    view_type = "agenda"

    def get_queryset(self):
        return super().get_queryset().filter(nurse=self.request.user, schedule_time__gte=datetime.today())


class Delete(__ScheduleViewsMixin, GenericModelDeleteView):
    pass