from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from datetime import datetime


class ArikeModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(default=datetime.now)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class State(ArikeModelMixin, models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class District(ArikeModelMixin, models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"


LOCAL_BODY_CHOICES = (
    # Panchayath levels
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    # Municipality levels
    (10, "Municipality"),
    # Corporation levels
    (20, "Corporation"),
    # Unknown
    (50, "Others"),
)


class LsgBody(ArikeModelMixin, models.Model):

    name = models.CharField(max_length=255)
    kind = models.IntegerField(choices=LOCAL_BODY_CHOICES)
    lsg_body_code = models.CharField(max_length=20, blank=True, null=True)

    district = models.ForeignKey(District, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("kind", "name", "district")

    def __str__(self):
        return f"{self.name} ({self.kind})"


class Ward(ArikeModelMixin, models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()

    lsg_body = models.ForeignKey(LsgBody, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("name", "number", "lsg_body")

    def __str__(self):
        return f"{self.name}"


class Facility(ArikeModelMixin, models.Model):
    class Kinds(models.TextChoices):
        PHC = "PHC", "Primary Health Centers"
        CHC = "CHC", "Community Health Centers"

    kind = models.CharField(max_length=6, choices=Kinds.choices)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)


class Genders(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "FEMALE"


UserRole = models.IntegerChoices(
    "UserRole",
    "DISTRICT_ADMIN PRIMARY_NURSE SECONDARY_NURSE",
)


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields["phone"] = "+919696969696"
        extra_fields["is_verified"] = True
        return super().create_superuser(username, email, password, **extra_fields)


class User(ArikeModelMixin, AbstractUser):
    role = models.IntegerField(choices=UserRole.choices, null=True, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    is_verified = models.BooleanField(default=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT, blank=False, null=True)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, blank=False, null=True)

    objects = CustomUserManager()


class Patient(ArikeModelMixin, models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=2, choices=Genders.choices)
    emergency_phone_number = models.CharField(max_length=15)
    expired_time = models.DateTimeField(null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)


class FamilyDetail(ArikeModelMixin, models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True)
    email = models.EmailField("email address", null=True)
    relation = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    education = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)


class Disease(ArikeModelMixin, models.Model):
    name = models.CharField(max_length=255)
    icds_code = models.CharField(max_length=8)


class PatientDisease(ArikeModelMixin, models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT)
    note = models.TextField()


class TreatmentNotes(ArikeModelMixin, models.Model):
    note = models.TextField(blank=True)
    description = models.TextField(blank=True)
    care_type = models.CharField(max_length=255, blank=True)
    care_sub_type = models.CharField(max_length=255, blank=True)


class Treatment(ArikeModelMixin, models.Model):
    description = models.TextField(blank=True)
    care_type = models.CharField(max_length=255, blank=True)
    care_sub_type = models.CharField(max_length=255, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    treatment_notes = models.ForeignKey(TreatmentNotes, on_delete=models.PROTECT)


class VisitSchedule(ArikeModelMixin, models.Model):
    schedule_time = models.DateTimeField()
    duration = models.DurationField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)


class VisitDetails(ArikeModelMixin, models.Model):
    palliative_phase = models.CharField(max_length=255, blank=True)
    blood_pressure = models.CharField(max_length=255, blank=True)
    pulse = models.CharField(max_length=255, blank=True)
    general_random_blood_sugar = models.CharField(max_length=255, blank=True)
    personal_hygiene = models.CharField(max_length=255, blank=True)
    mouth_hygiene = models.CharField(max_length=255, blank=True)
    public_hygiene = models.CharField(max_length=255, blank=True)
    systemic_examination = models.CharField(max_length=255, blank=True)
    patient_at_peace = models.BooleanField()
    pain = models.BooleanField()
    note = models.TextField(blank=True)
    visit_schedule = models.ForeignKey(VisitSchedule, on_delete=models.PROTECT)
    treatment_notes = models.ForeignKey(TreatmentNotes, on_delete=models.PROTECT)
