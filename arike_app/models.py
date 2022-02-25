from django.contrib.auth.models import AbstractUser
from django.db import models


class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class District(models.Model):
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


class LsgBody(models.Model):

    name = models.CharField(max_length=255)
    kind = models.IntegerField(choices=LOCAL_BODY_CHOICES)
    lsg_body_code = models.CharField(max_length=20, blank=True, null=True)

    district = models.ForeignKey(District, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("kind", "name", "district")

    def __str__(self):
        return f"{self.name} ({self.kind})"


class Ward(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()

    lsg_body = models.ForeignKey(LsgBody, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("name", "number", "lsg_body")

    def __str__(self):
        return f"{self.name}"


class Facility(models.Model):
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


class User(AbstractUser):
    role = models.IntegerField(choices=UserRole.choices, null=True, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=False)
    is_verified = models.BooleanField(default=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=False)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, null=True, blank=False)


class Patient(models.Model):
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=2, choices=Genders.choices)
    emergency_phone_number = models.CharField(max_length=15)
    expired_time = models.DateTimeField()
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
