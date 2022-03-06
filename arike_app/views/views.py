from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import TemplateView, UpdateView
from arike_app.forms import ProfileForm, PasswordChangeForm
from arike_app.models import User

from arike_app.views.mixins import DashboardTabViewMixin


class HomeView(DashboardTabViewMixin, TemplateView):
    def __init__(self) -> None:
        super().__init__()
        self.template_name = "dashboard/home.html"


class ProfileUpdateView(DashboardTabViewMixin, UpdateView):
    model = User
    form_class = ProfileForm

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template_name = "dashboard/profile.html"
        self.success_url = "./"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)


class ChangePasswordView(DashboardTabViewMixin, PasswordChangeView):
    form_class = PasswordChangeForm

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template_name = "dashboard/profile_change_password.html"
        self.success_url = "../"
