from celery.task import periodic_task
from datetime import datetime, timedelta
from django.core.mail import send_mail

from arike_app.models import User, UserReportConfiguration

import inspect


def __compose_nurse_report_body(nurse: User) -> str:
    return inspect.cleandoc(
        f"""
        Dear {nurse.first_name},

        Here is your daily report.

        // TODO

        ---

        With <3 from Arike
        http://rithviknishad-arike.herokuapp.com"""
    )


@periodic_task(run_every=timedelta(seconds=10))
def dispatch_nurse_daily_reports():
    now = datetime.now()
    for report_config in UserReportConfiguration.objects.filter(
        deleted=False,
        last_dispatched__lt=(now - timedelta(days=1)),
    ):
        report_config: UserReportConfiguration = report_config
        user: User = User.objects.get(id=report_config.user.id)
        send_mail(
            subject="Your daily report | Arike",
            message=__compose_nurse_report_body(user),
            from_email="Arike <rithvikn2001@gmail.com>",
            recipient_list=[user.email],
        )
        dt = report_config.dispatch_time
        report_config.last_dispatched = now.replace(hour=dt.hour, minute=dt.minute)
        report_config.save(update_fields=["last_dispatched"])
