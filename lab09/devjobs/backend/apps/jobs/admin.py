from apps.jobs.models.application import Application
from apps.jobs.models.candidate import Candidate
from apps.jobs.models.company import Company
from apps.jobs.models.location import Location
from apps.jobs.models.offer import Offer
from apps.jobs.models.recruiter import Recruiter
from apps.jobs.models.technology import Technology
from apps.jobs.models.user import User
from django.contrib import admin

admin.site.register(Application)
admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(Location)
# admin.site.register(OfferTechnology)
admin.site.register(Offer)
admin.site.register(Recruiter)
admin.site.register(Technology)
admin.site.register(User)
