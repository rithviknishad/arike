from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView, View
from django.views.generic.base import ContextMixin
from django_filters.views import FilterView
from django.contrib.auth import login
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from arike_app.dashboard import DASHBOARD_PAGES
from arike_app.filters import *
from arike_app.forms import *
from arike_app.mixins import UserOnboardingMailDispatcherMixin
from arike_app.models import *
from arike_app.tokens import account_activation_token


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
        return super().has_permission() and self.model.has_delete_permission(self.request)


class GenericModelCreateView(ModelTabViewMixin, CreateView):
    view_type = "create"
    success_url = "../"

    def has_permission(self) -> bool:
        return super().has_permission() and self.model.has_create_permission(self.request)


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = LoginForm


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return redirect("home")
        else:
            return render(request, "auth/invalid_token.html")


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

    class Create(_ViewMixin, UserOnboardingMailDispatcherMixin, GenericModelCreateView):
        form_class = UserCreationForm

        def form_valid(self, form) -> HttpResponse:
            res = super().form_valid(form)
            self.object.district = self.request.user.district
            self.object.is_verified = False
            self.object.save()
            self.send_account_activation_mail(self.object)
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
            if not self.request.user.is_superuser:
                qs = qs.filter(district=self.request.user.district, is_superuser=False)
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
