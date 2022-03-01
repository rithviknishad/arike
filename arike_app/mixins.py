from django.core.mail import send_mail
from arike_app.tokens import account_activation_token
from django.contrib.auth.models import AbstractBaseUser


class UserOnboardingMailDispatcherMixin:
    def send_onboarding_mail(self, user: AbstractBaseUser):
        token = account_activation_token.make_token(user)
        send_mail(
            subject="You've been invited to join Arike",
            message="Click http://rithviknishad-arike.herokuapp.com/auth/activate/{user.id}/{token}/ to activate your account.",
            from_email="Arike Onboarding Bot <noreply@arike.in>",
            recipient_list=[self.object.email],
        )
