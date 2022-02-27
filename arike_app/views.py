from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import ModelForm
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView
from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView

from arike_app.dashboard import DASHBOARD_PAGES
from arike_app.forms import *
from arike_app.models import *


class DashboardViewMixin(LoginRequiredMixin, ContextMixin):

    name = None
    view_type = None
    context_object_name = "object"

    def __init__(self) -> None:
        super().__init__()
        self.template_name = f"dashboard/{self.name}/{self.view_type}.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: show tabs based on permissions only
        context["dashboard_tabs"] = DASHBOARD_PAGES
        return context


class CustomListView(DashboardViewMixin, ListView):
    view_type = "list"


class CustomDetailView(DashboardViewMixin, DetailView):
    view_type = "details"


class CustomUpdateView(DashboardViewMixin, UpdateView):
    view_type = "edit"
    success_url = "../"


class CustomDeleteView(DashboardViewMixin, DeleteView):
    view_type = "delete"
    success_url = "../../"


class CustomCreateView(DashboardViewMixin, CreateView):
    view_type = "create"
    success_url = "../"


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        text_field_style = "bg-gray-200 rounded-xl w-full py-2 px-4"
        for field in ["username", "password"]:
            self.fields[field].widget.attrs["class"] = text_field_style
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = LoginForm


class HomeView(DashboardViewMixin, TemplateView):
    def __init__(self) -> None:
        super().__init__()
        self.template_name = "dashboard/home.html"


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class FacilitiesView(DashboardViewMixin, ListView):
    template_name = "dashboard/facilities.html"

    def get_queryset(self):
        # TODO: show only current district users.
        return Facility.objects.all()


class ProfileUpdateView(DashboardViewMixin, UpdateView):
    template_name = "dashboard/profile.html"


class UsersViews:
    class _ViewMixin:
        model = User
        name = "users"

    class Create(_ViewMixin, CustomCreateView):
        form_class = UserCreationForm

    class Delete(_ViewMixin, CustomDeleteView):
        pass

    class Details(_ViewMixin, CustomDetailView):
        pass

    class Edit(_ViewMixin, CustomUpdateView):
        form_class = UserChangeForm

    class List(_ViewMixin, CustomListView):
        pass


class FacilitiesViews:
    class _ViewMixin:
        model = Facility
        name = "facilities"
        form_class = FacilityForm

    class Create(_ViewMixin, CustomCreateView):
        pass

    class Delete(_ViewMixin, CustomDeleteView):
        pass

    class Details(_ViewMixin, CustomDetailView):
        pass

    class Edit(_ViewMixin, CustomUpdateView):
        pass

    class List(_ViewMixin, CustomListView):
        pass


class WardsViews:
    class _ViewMixin:
        model = Ward
        name = "wards"
        form_class = WardForm

    class Create(_ViewMixin, CustomCreateView):
        pass

    class Delete(_ViewMixin, CustomDeleteView):
        pass

    class Details(_ViewMixin, CustomDetailView):
        pass

    class Edit(_ViewMixin, CustomUpdateView):
        pass

    class List(_ViewMixin, CustomListView):
        pass


class PatientsViews:
    class _ViewMixin:
        model = Patient
        name = "patients"
        form_class = PatientForm

    class Create(_ViewMixin, CustomCreateView):
        pass

    class Delete(_ViewMixin, CustomDeleteView):
        pass

    class Details(_ViewMixin, CustomDetailView):
        pass

    class Edit(_ViewMixin, CustomUpdateView):
        pass

    class List(_ViewMixin, CustomListView):
        pass


class LsgBodiesViews:
    class _ViewMixin:
        model = LsgBody
        name = "lsg-bodies"
        form_class = LsgBodyForm

    class Create(_ViewMixin, CustomCreateView):
        pass

    class Delete(_ViewMixin, CustomDeleteView):
        pass

    class Details(_ViewMixin, CustomDetailView):
        pass

    class Edit(_ViewMixin, CustomUpdateView):
        pass

    class List(_ViewMixin, CustomListView):
        pass
