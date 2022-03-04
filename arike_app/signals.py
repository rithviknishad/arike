from typing import Optional
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

import inspect

from arike_app.models import Patient, Treatment, FamilyDetail


def __compose_treatment_update_report_body(treatment: Treatment) -> str:
    patient: Patient = treatment.patient
    return inspect.cleandoc(
        f"""
        Dear relative of {patient.full_name},

        Here are the treatment updates.

        Description: {treatment.description}
        Care Type: {treatment.care_type_and_sub_type}
        Treatment Notes:
            {treatment.treatment_notes.note}
            {treatment.treatment_notes.description}

        ---

        With <3 from Arike
        http://rithviknishad-arike.herokuapp.com"""
    )


@receiver(pre_save, sender=Treatment)
def on_treatment_update(sender, instance: Treatment, **kwargs) -> None:
    send_mail(
        subject=f"{instance.patient.first_name}'s Treatment Updates | Arike",
        message=__compose_treatment_update_report_body(instance),
        from_email="Arike <rithvikn2001@gmail.com>",
        recipient_list=[
            relative.email
            for relative in FamilyDetail.objects.filter(deleted=False, patient=instance.patient, is_primary=True)
        ],
    )
