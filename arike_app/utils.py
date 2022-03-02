from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from arike_app.tokens import account_activation_token
import inspect


def __compose_onboarding_body(user: AbstractBaseUser, activation_link: str):
    return inspect.cleandoc(
        f"""
        Hey {user.get_full_name() or user.get_username()},

        You've been invited to onboard Arike platform at http://rithviknishad-arike.herokuapp.com

        You've been registered with the username: {user.get_username()}.
        To access, you must activate your account by clicking: {activation_link} and set a new password.

        ---

        With <3 from Arike
        http://rithviknishad-arike.herokuapp.com"""
    )


def send_onboarding_mail(user: AbstractBaseUser):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = f"http://rithviknishad-arike.herokuapp.com/auth/activate/{uid}/{token}/"
    send_mail(
        subject="You've been invited to join Arike",
        message=__compose_onboarding_body(user, activation_link),
        from_email="Arike <rithvikn2001@gmail.com>",
        recipient_list=[user.email],
    )
