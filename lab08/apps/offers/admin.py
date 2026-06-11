from apps.offers.models.Application import Application
from apps.offers.models.Candidate import Candidate
from apps.offers.models.CandidateTechnology import CandidateTechnology
from apps.offers.models.Company import Company
from apps.offers.models.Offer import Offer
from apps.offers.models.OfferTechnology import OfferTechnology
from apps.offers.models.Recruiter import Recruiter
from apps.offers.models.Technology import Technology
from apps.offers.models.User import User
from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
  readonly_fields = ['created_id', 'modified_id', 'created', 'modified']

  def save_model(self, request, obj, form, change):
    if not change:
      obj.created_id = request.user
    obj.modified_id = request.user
    super().save_model(request, obj, form, change)


admin.site.register(User, BaseAdmin)
admin.site.register(Candidate, BaseAdmin)
admin.site.register(Recruiter, BaseAdmin)
admin.site.register(Company, BaseAdmin)
admin.site.register(Offer, BaseAdmin)
admin.site.register(Technology, BaseAdmin)
admin.site.register(Application, BaseAdmin)
admin.site.register(CandidateTechnology)
admin.site.register(OfferTechnology)
