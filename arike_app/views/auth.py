from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth import forms as auth_forms
from arike_app.tokens import account_activation_token

from arike_app.forms import LoginForm
from arike_app.tokens import account_activation_token
from arike_app.mixins import CustomFormStyleMixin


class UserLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = LoginForm


class CustomSetPasswordForm(CustomFormStyleMixin, auth_forms.SetPasswordForm):
    pass


class ActivateAccountView(PasswordResetConfirmView):
    template_name = "auth/activate.html"
    success_url = "/"
    token_generator = account_activation_token
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        res = super().form_valid(form)
        user = form.save()
        user.is_verified = True
        user.save()
        return res
