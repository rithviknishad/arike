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
from django.views.generic import View

from arike_app.views import *


def _(name: str, views_cls) -> List:
    return [
        path(f"{name}/", views_cls.List.as_view()),
        path(f"{name}/create/", views_cls.Create.as_view()),
        path(f"{name}/<pk>/", views_cls.Details.as_view()),
        path(f"{name}/<pk>/edit/", views_cls.Update.as_view()),
        path(f"{name}/<pk>/delete/", views_cls.Delete.as_view()),
    ]


urlpatterns = [
    # Authentication
    path("auth/login/", UserLoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    # Home
    path("", lambda req: redirect("/home/")),
    path("home/", HomeView.as_view()),
    # Models CRUD urls
    *_("users", UsersViews),
    *_("facilities", FacilitiesViews),
    *_("patients", PatientsViews),
    *_("lsg-bodies", LsgBodiesViews),
    *_("wards", WardsViews),
    # Profile
    path("profile/", ProfileUpdateView.as_view()),
]
