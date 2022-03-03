"""arike URL Configuration

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List

from django.contrib.auth.views import LogoutView, PasswordResetConfirmView
from django.shortcuts import redirect
from django.urls import path, re_path
from django.views.generic import View

from arike_app.views import *
from arike_app.auth_views import *


def _(name: str, views_cls, url_prefix: str = "") -> List:
    results = []
    if hasattr(views_cls, "List"):
        results.append(path(f"{url_prefix}{name}/", views_cls.List.as_view()))
    if hasattr(views_cls, "Create"):
        results.append(path(f"{url_prefix}{name}/create/", views_cls.Create.as_view()))
    if hasattr(views_cls, "Details"):
        results.append(path(f"{url_prefix}{name}/<pk>/", views_cls.Details.as_view()))
    if hasattr(views_cls, "Update"):
        results.append(path(f"{url_prefix}{name}/<pk>/edit/", views_cls.Update.as_view()))
    if hasattr(views_cls, "Delete"):
        results.append(path(f"{url_prefix}{name}/<pk>/delete/", views_cls.Delete.as_view()))
    return results


urlpatterns = [
    # Authentication
    path("auth/login/", UserLoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="password_reset_confirm"),
    # Home
    path("", lambda _: redirect("/home/")),
    path("home/", HomeView.as_view()),
    # Models CRUD urls
    *_("users", UsersViews),
    *_("facilities", FacilitiesViews),
    *_("lsg-bodies", LsgBodiesViews),
    *_("wards", WardsViews),
    *_("patients", PatientsViews),
    *_("family-details", PatientFamilyDetailsViews, url_prefix="patients/<patient_id>/"),
    *_("disease-history", PatientDiseaseHistoryViews, url_prefix="patients/<patient_id>/"),
    *_("treatments", PatientTreatmentsViews, url_prefix="patients/<patient_id>/"),
    *_("visits", PatientVisitsViews, url_prefix="patients/<patient_id>/"),
    *_("schedule", ScheduleViews),
    # Profile
    path("profile/", ProfileUpdateView.as_view()),
]
