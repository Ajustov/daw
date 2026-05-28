from apps.offers.models.Application import Application
from apps.offers.models.Candidate import Candidate
from apps.offers.models.Company import Company
from apps.offers.models.Offer import Offer
from apps.offers.models.Recruiter import Recruiter
from apps.offers.models.Technology import Technology
from apps.offers.models.User import User
from django.contrib import admin

admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Recruiter)
admin.site.register(Company)
admin.site.register(Offer)
admin.site.register(Technology)
admin.site.register(Application)
