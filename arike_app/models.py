from typing import List
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.http import HttpRequest

from datetime import datetime, date


class ArikeModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    @staticmethod
    def has_create_permission(request: HttpRequest):
        return request.user.is_superuser

    @staticmethod
    def has_read_permission(request: HttpRequest):
        return True

    def has_object_read_permission(self, request: HttpRequest):
        return True

    def has_object_update_permission(self, request: HttpRequest):
        return request.user.is_superuser

    @staticmethod
    def has_delete_permission(request: HttpRequest):
        return request.user.is_superuser


class State(ArikeModelMixin, models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def has_delete_permission(request: HttpRequest):
        return request.user.is_superuser


class District(ArikeModelMixin, models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def has_delete_permission(request: HttpRequest):
        return request.user.is_superuser


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

    @staticmethod
    def has_create_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin

    @staticmethod
    def has_read_permission(request: HttpRequest):
        return True

    def has_object_read_permission(self, request: HttpRequest):
        return True

    def has_object_update_permission(self, request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin

    @staticmethod
    def has_delete_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin


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

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def has_create_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin

    @staticmethod
    def has_read_permission(request: HttpRequest):
        return True

    def has_object_read_permission(self, request: HttpRequest):
        print(request.user.district)
        return request.user.is_superuser or self.ward.lsg_body.district == request.user.district

    def has_object_update_permission(self, request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin

    @staticmethod
    def has_delete_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin


class Genders(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other"


UserRole = models.IntegerChoices(
    "UserRole",
    "DISTRICT_ADMIN DOCTOR PRIMARY_NURSE SECONDARY_NURSE",
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

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_district_admin(self):
        return self.role == 1

    @property
    def is_doctor(self):
        return self.role == 2

    @property
    def is_primary_nurse(self):
        return self.role == 3

    @property
    def is_secondary_nurse(self):
        return self.role == 4

    @property
    def is_verified_nurse(self):
        return self.is_verified and (self.is_primary_nurse or self.is_secondary_nurse)

    @staticmethod
    def has_create_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin

    @staticmethod
    def has_read_permission(request: HttpRequest):
        return True

    def has_object_read_permission(self, request: HttpRequest):
        return request.user.is_superuser or self.district == request.user.district

    def has_object_update_permission(self, request: HttpRequest):
        return request.user.is_superuser or self.district == request.user.district

    @staticmethod
    def has_delete_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_district_admin


class PatientDetailsPermsMixin:
    @staticmethod
    def has_create_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_verified_nurse

    @staticmethod
    def has_read_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_verified_nurse or request.user.is_district_admin

    def has_object_read_permission(self, request: HttpRequest):
        return request.user.is_superuser or request.user.is_verified_nurse or request.user.is_district_admin

    def has_object_update_permission(self, request: HttpRequest):
        return request.user.is_superuser or request.user.is_verified_nurse

    @staticmethod
    def has_delete_permission(request: HttpRequest):
        return request.user.is_superuser or request.user.is_verified_nurse


class Patient(PatientDetailsPermsMixin, ArikeModelMixin, models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    emergency_phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, null=True)
    gender = models.CharField(max_length=2, choices=Genders.choices)
    expired_time = models.DateTimeField(null=True, blank=True)

    @property
    def active_treatments(self) -> List[str]:
        result = [str(x) for x in Treatment.objects.filter(patient=self, deleted=False)]
        print(result)
        return result

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def __str__(self):
        return f"{self.full_name}"


class FamilyDetail(PatientDetailsPermsMixin, ArikeModelMixin, models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField("email address", null=True, blank=True)
    relation = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    education = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.full_name}"


class Disease(ArikeModelMixin, models.Model):
    name = models.CharField(max_length=255)
    icds_code = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.name}"


class PatientDisease(PatientDetailsPermsMixin, ArikeModelMixin, models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT)
    note = models.TextField()

    def __str__(self):
        return f"{self.disease}"


class CareType(ArikeModelMixin, models.Model):
    value = models.TextField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.value}"


class CareSubType(ArikeModelMixin, models.Model):
    care_type = models.ForeignKey(CareType, on_delete=models.PROTECT)
    care_sub_type = models.TextField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.care_type} - {self.care_sub_type}"


class TreatmentNotes(PatientDetailsPermsMixin, ArikeModelMixin, models.Model):
    note = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Treatment(PatientDetailsPermsMixin, ArikeModelMixin, models.Model):
    description = models.TextField(blank=True)
    care_type_and_sub_type = models.ForeignKey(CareSubType, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    treatment_notes = models.OneToOneField(TreatmentNotes, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.care_type_and_sub_type.care_sub_type


class VisitSchedule(PatientDetailsPermsMixin, ArikeModelMixin, models.Model):
    schedule_time = models.DateTimeField()
    duration = models.DurationField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    nurse = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.schedule_time} for duration {self.duration}"


PalliativePhase = models.IntegerChoices("PalliativePhase", "STABLE UNSTABLE DETERIORATING DYING")
SystemicExamination = models.IntegerChoices("SystemicExamination", "STABLE UNSTABLE DETERIORATING DYING")


class VisitDetails(PatientDetailsPermsMixin, ArikeModelMixin, models.Model):
    palliative_phase = models.IntegerField(choices=PalliativePhase.choices, null=True)
    blood_pressure = models.CharField(max_length=255, blank=True, null=True)
    pulse = models.CharField(max_length=255, blank=True, null=True)
    general_random_blood_sugar = models.CharField(max_length=255, blank=True, null=True)
    personal_hygiene = models.CharField(max_length=255, blank=True, null=True)
    mouth_hygiene = models.CharField(max_length=255, blank=True, null=True)
    public_hygiene = models.CharField(max_length=255, blank=True, null=True)
    systemic_examination = models.IntegerField(choices=PalliativePhase.choices, null=True)
    systemic_examination_details = models.TextField(blank=True, null=True)
    patient_at_peace = models.BooleanField(null=True)
    pain = models.BooleanField(null=True)
    notes = models.TextField(blank=True, null=True)
    visit_schedule = models.OneToOneField(VisitSchedule, on_delete=models.PROTECT)
    treatment_notes = models.OneToOneField(TreatmentNotes, on_delete=models.PROTECT)


class UserReportConfiguration(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    preferred_time = models.TimeField()
    last_dispatched = models.DateTimeField(default=datetime.now)
