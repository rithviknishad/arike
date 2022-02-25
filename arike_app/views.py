from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from arike_app.models import *


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


class HomeView(TemplateView):
    template_name = "dashboard/home.html"


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class FacilitiesView(LoginRequiredMixin, ListView):
    template_name = "dashboard/facilities.html"

    def get_queryset(self):
        # TODO: show only current district users.
        return Facility.objects.all()


class ProfileUpdateView(UpdateView):
    template_name = "dashboard/profile.html"


class UsersListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/users.html"
    context_object_name = "users"

    def get_queryset(self):
        # TODO: show only current district users.
        return User.objects.all()
