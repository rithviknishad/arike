from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView
from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from django_filters.views import FilterView

from arike_app.dashboard import DASHBOARD_PAGES
from arike_app.filters import *
from arike_app.forms import *
from arike_app.models import *


class ModelTabViewMixin(LoginRequiredMixin, PermissionRequiredMixin, ContextMixin):
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


class GenericModelListView(ModelTabViewMixin, FilterView):
    view_type = "list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_create_perm"] = self.model.has_create_permission(self.request)
        return context

    def has_permission(self) -> bool:
        return super().has_permission() and self.model.has_read_permission(self.request)


class GenericModelDetailView(ModelTabViewMixin, DetailView):
    view_type = "details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_update_perm"] = self.get_object().has_object_update_permission(self.request)
        context["has_delete_perm"] = self.model.has_delete_permission(self.request)
        return context

    def has_permission(self) -> bool:
        return super().has_permission() and self.get_object().has_object_read_permission(self.request)


class GenericModelUpdateView(ModelTabViewMixin, UpdateView):
    view_type = "edit"
    success_url = "../"

    def has_permission(self) -> bool:
        return super().has_permission() and self.get_object().has_object_update_permission(self.request)


class GenericModelDeleteView(ModelTabViewMixin, DeleteView):
    view_type = "delete"
    success_url = "../../"

    def has_permission(self) -> bool:
        # TODO: move to CustomDeleteView
        return super().has_permission() and self.model.has_delete_permission(self.request)


class GenericModelCreateView(ModelTabViewMixin, CreateView):
    view_type = "create"
    success_url = "../"

    def has_permission(self) -> bool:
        return super().has_permission() and self.model.has_create_permission(self.request)


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = LoginForm


class HomeView(ModelTabViewMixin, TemplateView):
    def __init__(self) -> None:
        super().__init__()
        self.template_name = "dashboard/home.html"


class ProfileUpdateView(ModelTabViewMixin, UpdateView):
    template_name = "dashboard/profile.html"


class UsersViews:
    class _ViewMixin:
        model = User
        name = "users"
        filterset_class = UsersFilter
        queryset = User.objects.filter(deleted=False)

    class Create(_ViewMixin, GenericModelCreateView):
        form_class = UserCreationForm

        def form_valid(self, form) -> HttpResponse:
            """Injects district of district admin's district."""
            res = super().form_valid(form)
            self.object.district = self.request.user.district
            self.object.save()
            return res

    class Delete(_ViewMixin, GenericModelDeleteView):
        pass

    class Details(_ViewMixin, GenericModelDetailView):
        pass

    class Update(_ViewMixin, GenericModelUpdateView):
        form_class = UserChangeForm

    class List(_ViewMixin, GenericModelListView):
        def get_queryset(self):
            qs = super().get_queryset()
            qs = qs.filter(district=self.request.user.district)
            return qs


class FacilitiesViews:
    class _ViewMixin:
        model = Facility
        name = "facilities"
        form_class = FacilityForm
        filterset_class = FacilitiesFilter

    class Create(_ViewMixin, GenericModelCreateView):
        pass

    class Delete(_ViewMixin, GenericModelDeleteView):
        pass

    class Details(_ViewMixin, GenericModelDetailView):
        pass

    class Update(_ViewMixin, GenericModelUpdateView):
        pass

    class List(_ViewMixin, GenericModelListView):
        pass


class WardsViews:
    class _ViewMixin:
        model = Ward
        name = "wards"
        form_class = WardForm
        filterset_class = WardsFilter

    class Create(_ViewMixin, GenericModelCreateView):
        pass

    class Delete(_ViewMixin, GenericModelDeleteView):
        pass

    class Details(_ViewMixin, GenericModelDetailView):
        pass

    class Update(_ViewMixin, GenericModelUpdateView):
        pass

    class List(_ViewMixin, GenericModelListView):
        pass


class PatientsViews:
    class _ViewMixin:
        model = Patient
        name = "patients"
        form_class = PatientForm
        filterset_class = PatientsFilter

    class Create(_ViewMixin, GenericModelCreateView):
        pass

    class Delete(_ViewMixin, GenericModelDeleteView):
        pass

    class Details(_ViewMixin, GenericModelDetailView):
        pass

    class Update(_ViewMixin, GenericModelUpdateView):
        pass

    class List(_ViewMixin, GenericModelListView):
        pass


class LsgBodiesViews:
    class _ViewMixin:
        model = LsgBody
        name = "lsg-bodies"
        form_class = LsgBodyForm
        filterset_class = LsgBodyFilter

    class Create(_ViewMixin, GenericModelCreateView):
        pass

    class Delete(_ViewMixin, GenericModelDeleteView):
        pass

    class Details(_ViewMixin, GenericModelDetailView):
        pass

    class Update(_ViewMixin, GenericModelUpdateView):
        pass

    class List(_ViewMixin, GenericModelListView):
        pass
