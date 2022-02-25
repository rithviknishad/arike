"""arike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from arike_app import views

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    # Authentication
    path("auth/login/", views.UserLoginView.as_view()),
    # Home
    path("home/", views.HomeView.as_view()),
    # Facilities
    # path("facilities/", views.FacilitiesView.as_view()),
    # Profile
    path("profile/", views.ProfileUpdateView.as_view()),
    # Users
    path("users/", views.UsersListView.as_view()),
    # path("auth/logout"),
]
