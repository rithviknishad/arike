# Generated by Django 4.0.2 on 2022-03-03 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arike_app', '0003_alter_patient_facility'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitschedule',
            name='nurse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
