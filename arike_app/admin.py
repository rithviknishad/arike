from django.contrib import admin

from arike_app.models import *

admin.sites.site.register(State)
admin.sites.site.register(District)
admin.sites.site.register(LsgBody)
admin.sites.site.register(Ward)
admin.sites.site.register(Facility)
admin.sites.site.register(User)
admin.sites.site.register(Patient)
