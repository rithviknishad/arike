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


class CustomDeleteView(DashboardViewMixin, DeleteView):
    view_type = "delete"


class CustomCreateView(DashboardViewMixin, CreateView):
    view_type = "create"


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


class UsersViewMixin:
    model = User
    name = "users"


class CreateUserView(UsersViewMixin, CustomCreateView):
    form_class = UserCreationForm
    success_url = "../"


class UserDeleteView(UsersViewMixin, CustomDeleteView):
    success_url = "/users"


class UserDetailsView(UsersViewMixin, CustomDetailView):
    pass


class UserEditView(UsersViewMixin, CustomUpdateView):
    form_class = UserChangeForm
    success_url = "../"


class ListUsersView(UsersViewMixin, CustomListView):
    pass


class FacilitiesViewMixin:
    model = Facility
    name = "facilities"
    form_class = FacilityForm


class CreateFacilityView(FacilitiesViewMixin, CustomCreateView):
    success_url = "../"


class FacilityDeleteView(FacilitiesViewMixin, CustomDeleteView):
    success_url = "/facilities"


class FacilityDetailsView(FacilitiesViewMixin, CustomDetailView):
    pass


class FacilityEditView(FacilitiesViewMixin, CustomUpdateView):
    success_url = "../"


class ListFacilitiesView(FacilitiesViewMixin, CustomListView):
    pass


class WardsViewMixin:
    model = Ward
    name = "wards"
    form_class = FacilityForm


class CreateWardView(WardsViewMixin, CustomCreateView):
    success_url = "../"


class WardDeleteView(WardsViewMixin, CustomDeleteView):
    success_url = "/Wards"


class WardDetailsView(WardsViewMixin, CustomDetailView):
    pass


class WardEditView(WardsViewMixin, CustomUpdateView):
    success_url = "../"


class ListWardsView(WardsViewMixin, CustomListView):
    pass


class PatientsViewMixin:
    model = Patient
    name = "patients"
    form_class = FacilityForm


class CreatePatientView(PatientsViewMixin, CustomCreateView):
    success_url = "../"


class PatientDeleteView(PatientsViewMixin, CustomDeleteView):
    success_url = "/Patients"


class PatientDetailsView(PatientsViewMixin, CustomDetailView):
    pass


class PatientEditView(PatientsViewMixin, CustomUpdateView):
    success_url = "../"


class ListPatientsView(PatientsViewMixin, CustomListView):
    pass


class LsgBodiesViewMixin:
    model = LsgBody
    name = "lsg-bodies"
    form_class = LsgBodyForm


class CreateLsgBodyView(LsgBodiesViewMixin, CustomCreateView):
    success_url = "../"


class LsgBodyDeleteView(LsgBodiesViewMixin, CustomDeleteView):
    success_url = "/LsgBodies"


class LsgBodyDetailsView(LsgBodiesViewMixin, CustomDetailView):
    pass


class LsgBodyEditView(LsgBodiesViewMixin, CustomUpdateView):
    success_url = "../"


class ListLsgBodiesView(LsgBodiesViewMixin, CustomListView):
    pass
