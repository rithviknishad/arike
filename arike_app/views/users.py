from django.http import HttpResponse

from arike_app.filters import UsersFilter
from arike_app.forms import UserCreationForm, UserChangeForm
from arike_app.models import User
from arike_app.utils import send_onboarding_mail
from arike_app.views.generic import (
    GenericModelCreateView,
    GenericModelListView,
    GenericModelDetailView,
    GenericModelUpdateView,
    GenericModelDeleteView,
)


class __UsersViewMixin:
    model = User
    name = "users"


class Create(__UsersViewMixin, GenericModelCreateView):
    form_class = UserCreationForm

    def form_valid(self, form) -> HttpResponse:
        res = super().form_valid(form)
        self.object.district = self.request.user.district
        self.object.is_verified = False
        self.object.save()
        send_onboarding_mail(self.object)
        return res


class List(__UsersViewMixin, GenericModelListView):
    filterset_class = UsersFilter
    queryset = User.objects.filter(deleted=False)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(district=self.request.user.district, is_superuser=False)
        return qs


class Details(__UsersViewMixin, GenericModelDetailView):
    pass


class Update(__UsersViewMixin, GenericModelUpdateView):
    form_class = UserChangeForm


class Delete(__UsersViewMixin, GenericModelDeleteView):
    pass
