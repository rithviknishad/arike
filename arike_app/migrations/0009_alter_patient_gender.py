# Generated by Django 4.0.2 on 2022-02-27 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arike_app', '0008_rename_phone_patient_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=2),
        ),
    ]