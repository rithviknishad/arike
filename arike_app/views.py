from dataclasses import dataclass
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.views.generic import View, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from arike_app.models import *
from arike_app.dashboard import DASHBOARD_PAGES


class DashboardViewMixin(LoginRequiredMixin, ContextMixin):

    name = None
    view_type = None

    def __init__(self) -> None:
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
    template_name = "dashboard/home.html"


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
    class UserCreationForm(UserCreationForm):
        class Meta:
            model = User
            fields = [
                "username",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "email",
                "phone",
                "facility",
                "role",
            ]

    form_class = UserCreationForm
    success_url = "../"


class ListUsersView(UsersViewMixin, CustomListView):
    def get_queryset(self):
        # TODO: show only current district users.
        return User.objects.all()


class UserDetailsView(UsersViewMixin, CustomDetailView):
    model = User
    context_object_name = "object"  # Voluntarily overriding as it'll conflict with `user` in context


class UserDeleteView(UsersViewMixin, CustomDeleteView):
    model = User
    success_url = "/users"


class UserEditView(UsersViewMixin, CustomUpdateView):
    class UserChangeForm(UserChangeForm):
        class Meta:
            model = User
            fields = ["first_name", "last_name", "email", "phone", "facility", "role"]

    model = User
    form_class = UserChangeForm
    success_url = "../"
