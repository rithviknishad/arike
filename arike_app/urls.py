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

from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import path

from arike_app.views.views import HomeView, ProfileUpdateView
from arike_app.views.auth import *
from arike_app.views import (
    users,
    patients,
    facilities,
    lsg_bodies,
    wards,
    patient_disease_history,
    patient_family_details,
    patient_treatments,
    patient_visits,
    schedule,
)


def _(name: str, views, url_prefix: str = "") -> List:
    results = []
    if hasattr(views, "List"):
        results.append(path(f"{url_prefix}{name}/", views.List.as_view()))
    if hasattr(views, "Create"):
        results.append(path(f"{url_prefix}{name}/create/", views.Create.as_view()))
    if hasattr(views, "Details"):
        results.append(path(f"{url_prefix}{name}/<pk>/", views.Details.as_view()))
    if hasattr(views, "Update"):
        results.append(path(f"{url_prefix}{name}/<pk>/edit/", views.Update.as_view()))
    if hasattr(views, "Delete"):
        results.append(path(f"{url_prefix}{name}/<pk>/delete/", views.Delete.as_view()))
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
    *_("users", users),
    *_("facilities", facilities),
    *_("lsg_bodies", lsg_bodies),
    *_("wards", wards),
    *_("patients", patients),
    *_("disease_history", patient_disease_history, url_prefix="patients/<patient_id>/"),
    *_("family_details", patient_family_details, url_prefix="patients/<patient_id>/"),
    *_("treatments", patient_treatments, url_prefix="patients/<patient_id>/"),
    *_("visits", patient_visits, url_prefix="patients/<patient_id>/"),
    *_("schedule", schedule),
    path("schedule/create/<patient_id>/", patient_visits.Create.as_view(success_url="/schedule")),
    path("schedule/agenda/", schedule.Agenda.as_view()),
    path("schedule/visit/<schedule_id>/", schedule.VisitPatient.as_view()),
    # Profile
    path("profile/", ProfileUpdateView.as_view()),
]
