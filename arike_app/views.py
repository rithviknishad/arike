from dataclasses import dataclass
from typing import List
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.views.generic import View, CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from arike_app.models import *
from arike_app.dashboard import DASHBOARD_PAGES


class DashboardViewMixin(LoginRequiredMixin, ContextMixin, View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: show tabs based on permissions only
        context["dashboard_tabs"] = DASHBOARD_PAGES
        return context


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


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "facility", "role"]


class ProfileUpdateView(DashboardViewMixin, UpdateView):
    template_name = "dashboard/profile.html"


class CreateUserView(DashboardViewMixin, CreateView):
    template_name = "dashboard/users/create.html"
    form_class = UserForm
    success_url = "../"

    def get_success_url(self) -> str:
        return super().get_success_url()


class ListUsersView(DashboardViewMixin, ListView):
    template_name = "dashboard/users/list.html"
    context_object_name = "users"

    def get_queryset(self):
        # TODO: show only current district users.
        return User.objects.all()
