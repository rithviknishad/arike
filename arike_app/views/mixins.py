from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin

from arike_app.dashboard import DASHBOARD_PAGES
from arike_app.models import Patient


class DashboardTabViewMixin(LoginRequiredMixin, PermissionRequiredMixin, ContextMixin):
    name = None
    view_type = None
    context_object_name = "object"
    permission_required = []

    def __init__(self) -> None:
        super().__init__()
        self.template_name = f"dashboard/{self.name}/{self.view_type}.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: show tabs based on permissions only
        context["dashboard_tabs"] = DASHBOARD_PAGES
        return context


class ModelTabViewMixin(DashboardTabViewMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_create_perm"] = self.model.has_create_permission(self.request)
        context["has_delete_perm"] = self.model.has_delete_permission(self.request)
        return context


class PatientRelatedViewMixin:
    @property
    def patient_id(self):
        return self.kwargs.get("patient_id")

    @property
    def patient(self):
        return Patient.objects.get(id=self.patient_id)

    def get_queryset(self):
        return super().get_queryset().filter(patient__id=self.patient_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = self.patient
        return context

    def pre_save_object(self) -> None:
        if not self.object.patient:
            self.object.patient = self.patient

    def form_valid(self, form) -> HttpResponse:
        res = super().form_valid(form)
        self.pre_save_object()
        self.object.save()
        return res
