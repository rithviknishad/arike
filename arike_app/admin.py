from django.contrib import admin

from arike_app import models

admin.sites.site.register(
    [
        models.State,
        models.District,
        models.LsgBody,
        models.Ward,
        models.Facility,
        models.User,
        models.Patient,
    ]
)
