# Generated by Django 4.0.2 on 2022-03-03 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arike_app', '0005_remove_treatmentnotes_care_type_and_sub_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='treatment_notes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='arike_app.treatmentnotes'),
        ),
    ]
