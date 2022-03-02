from django.core.mail import send_mail
from arike_app.tokens import account_activation_token
from django.contrib.auth.models import AbstractBaseUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_onboarding_mail(user: AbstractBaseUser):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    send_mail(
        subject="You've been invited to join Arike",
        message=f"Click http://rithviknishad-arike.herokuapp.com/auth/activate/{uid}/{token}/ to activate your account.",
        from_email="Arike <rithvikn2001@gmail.com>",
        recipient_list=[user.email],
    )
