from django.views.generic import TemplateView, UpdateView

from arike_app.views.mixins import DashboardTabViewMixin


class HomeView(DashboardTabViewMixin, TemplateView):
    def __init__(self) -> None:
        super().__init__()
        self.template_name = "dashboard/home.html"


class ProfileUpdateView(DashboardTabViewMixin, UpdateView):
    template_name = "dashboard/profile.html"
