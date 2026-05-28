from django.contrib import admin

from .models import (
    Company,
    Profile,
    Technology,
    Job,
    Application,
    Skill
)

admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(Technology)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Skill)