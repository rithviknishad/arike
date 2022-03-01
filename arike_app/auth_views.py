from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import redirect, render
from django.contrib.auth import login
from arike_app.tokens import account_activation_token
from django.views.generic import View

from arike_app.forms import LoginForm
from arike_app.models import User


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = LoginForm


class ActivateAccountView(View):
    def get(self, request, pk, token):
        try:
            user = User.objects.get(id=pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and user.is_verified:
            return render(request, "auth/already_verified.html")

        if user is not None and account_activation_token.check_token(user, token):
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect("/auth/rest-password/")
        else:
            return render(request, "auth/invalid_token.html")


class ResetPasswordView(PasswordResetView):
    template_name = "auth/reset.html"
    success_url = "/"
