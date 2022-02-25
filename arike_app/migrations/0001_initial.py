# Generated by Django 4.0.2 on 2022-02-25 16:20

import arike_app.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icds_code', models.CharField(max_length=8)),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('PHC', 'Primary Health Centers'), ('CHC', 'Community Health Centers')], max_length=6)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=15)),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LsgBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('kind', models.IntegerField(choices=[(1, 'Grama Panchayath'), (2, 'Block Panchayath'), (3, 'District Panchayath'), (4, 'Nagar Panchayath'), (10, 'Municipality'), (20, 'Corporation'), (50, 'Others')])),
                ('lsg_body_code', models.CharField(blank=True, max_length=20, null=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.district')),
            ],
            options={
                'unique_together': {('kind', 'name', 'district')},
            },
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('landmark', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'FEMALE')], max_length=2)),
                ('emergency_phone_number', models.CharField(max_length=15)),
                ('expired_time', models.DateTimeField(blank=True, null=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.facility')),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TreatmentNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('care_type', models.CharField(blank=True, max_length=255)),
                ('care_sub_type', models.CharField(blank=True, max_length=255)),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
                ('lsg_body', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.lsgbody')),
            ],
            options={
                'unique_together': {('name', 'number', 'lsg_body')},
            },
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VisitSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.patient')),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VisitDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palliative_phase', models.CharField(blank=True, max_length=255)),
                ('blood_pressure', models.CharField(blank=True, max_length=255)),
                ('pulse', models.CharField(blank=True, max_length=255)),
                ('general_random_blood_sugar', models.CharField(blank=True, max_length=255)),
                ('personal_hygiene', models.CharField(blank=True, max_length=255)),
                ('mouth_hygiene', models.CharField(blank=True, max_length=255)),
                ('public_hygiene', models.CharField(blank=True, max_length=255)),
                ('systemic_examination', models.CharField(blank=True, max_length=255)),
                ('patient_at_peace', models.BooleanField()),
                ('pain', models.BooleanField()),
                ('note', models.TextField(blank=True)),
                ('treatment_notes', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.treatmentnotes')),
                ('visit_schedule', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.visitschedule')),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('care_type', models.CharField(blank=True, max_length=255)),
                ('care_sub_type', models.CharField(blank=True, max_length=255)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.patient')),
                ('treatment_notes', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.treatmentnotes')),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PatientDisease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.disease')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.patient')),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='patient',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.ward'),
        ),
        migrations.CreateModel(
            name='FamilyDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('date_of_birth', models.DateField(blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email address')),
                ('relation', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('education', models.CharField(blank=True, max_length=255)),
                ('occupation', models.CharField(blank=True, max_length=255)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('is_primary', models.BooleanField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.patient')),
            ],
            bases=(arike_app.models.ArikeModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='facility',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.ward'),
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.state'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.IntegerField(choices=[(1, 'District Admin'), (2, 'Primary Nurse'), (3, 'Secondary Nurse')], null=True)),
                ('phone', models.CharField(max_length=15)),
                ('is_verified', models.BooleanField(default=False)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.district')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arike_app.facility')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
