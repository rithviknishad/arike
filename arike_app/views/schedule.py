from datetime import datetime

from arike_app.models import Patient, TreatmentNotes, VisitDetails, VisitSchedule
from arike_app.forms import VisitDetailsForm, VisitTreatmentNotesForm
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelDeleteView,
    GenericModelDetailView,
    GenericModelListView,
    GenericModelUpdateView,
)


class __ScheduleViewsMixin:
    model = VisitSchedule
    name = "schedule"


class List(__ScheduleViewsMixin, GenericModelListView):
    model = Patient

    def get_queryset(self):
        return super().get_queryset().filter(facility=self.request.user.facility)


class Agenda(__ScheduleViewsMixin, GenericModelListView):
    model = VisitSchedule
    view_type = "agenda"

    def get_queryset(self):
        return super().get_queryset().filter(nurse=self.request.user, schedule_time__gte=datetime.today())


class Delete(__ScheduleViewsMixin, GenericModelDeleteView):
    success_url = "../../agenda/"


class VisitPatient(__ScheduleViewsMixin, GenericModelDetailView):
    model = VisitSchedule
    view_type = "visit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Voluntarily overriding to hide button. TODO: update template instead of context
        context["has_update_perm"] = False
        context["has_delete_perm"] = False
        visit_details = VisitDetails.objects.filter(visit_schedule=self.object)
        visit_details = (
            visit_details.first()
            if visit_details
            else VisitDetails.objects.create(
                visit_schedule=self.object, treatment_notes=TreatmentNotes.objects.create()
            )
        )
        context["on_click_treatment_notes"] = f"location.href='../treatment_notes/{visit_details.treatment_notes.id}'"
        context["on_click_health_information"] = f"location.href='../health_info/{visit_details.id}'"
        return context


class UpdateHealthInformation(__ScheduleViewsMixin, GenericModelUpdateView):
    model = VisitDetails
    view_type = "update_health_information"
    form_class = VisitDetailsForm


class UpdateTreatmentNotes(__ScheduleViewsMixin, GenericModelUpdateView):
    model = TreatmentNotes
    view_type = "udpate_treatment_notes"
    form_class = VisitTreatmentNotesForm
