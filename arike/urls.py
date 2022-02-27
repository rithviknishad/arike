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

from arike_app.views import *
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import View


def _(name: str, list: View, create: View, detail: View, edit: View, delete: View) -> List:
    return [
        path(f"{name}/", list.as_view()),
        path(f"{name}/create/", create.as_view()),
        path(f"{name}/<pk>/", detail.as_view()),
        path(f"{name}/<pk>/edit/", edit.as_view()),
        path(f"{name}/<pk>/delete/", delete.as_view()),
    ]


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    # Authentication
    path("auth/login/", UserLoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    # Home
    path("", lambda req: redirect("/home/")),
    path("home/", HomeView.as_view()),
    # Model CRUD urls
    *_("users", ListUsersView, CreateUserView, UserDetailsView, UserEditView, UserDeleteView),
    *_(
        "facilities", ListFacilitiesView, CreateFacilityView, FacilityDetailsView, FacilityEditView, FacilityDeleteView
    ),
    *_("patients", ListPatientsView, CreatePatientView, PatientDetailsView, PatientEditView, PatientDeleteView),
    *_("lsg-bodies", ListLsgBodiesView, CreateLsgBodyView, LsgBodyDetailsView, LsgBodyEditView, LsgBodyDeleteView),
    *_("wards", ListWardsView, CreateWardView, WardDetailsView, WardEditView, WardDeleteView),
    # Profile
    path("profile/", ProfileUpdateView.as_view()),
]
