from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # <- Importamos el Admin especial de autenticación
from apps.offers.models.Application import Application
from apps.offers.models.Candidate import Candidate
from apps.offers.models.CandidateTechnology import CandidateTechnology
from apps.offers.models.Company import Company
from apps.offers.models.Offer import Offer
from apps.offers.models.OfferTechnology import OfferTechnology
from apps.offers.models.Recruiter import Recruiter
from apps.offers.models.Technology import Technology
from apps.offers.models.User import User


class BaseAdmin(admin.ModelAdmin):  # type: ignore
  readonly_fields = ['created_id', 'modified_id', 'created', 'modified']

  def save_model(self, request, obj, form, change):  # type: ignore
    if not change:
      obj.created_id = request.user
    obj.modified_id = request.user
    super().save_model(request, obj, form, change)  # type: ignore


# Creamos un Admin exclusivo para tu modelo User heredando de UserAdmin
class CustomUserAdmin(UserAdmin):
  
  # Mantenemos tu lógica de auditoría idéntica
  def save_model(self, request, obj, form, change):
    if not change:
      obj.created_id = request.user
    obj.modified_id = request.user
    super().save_model(request, obj, form, change)

  # Acoplamos tus campos de auditoría al diseño visual del Django Admin
  fieldsets = UserAdmin.fieldsets + (
      ('Información de Auditoría', {'fields': ('created_id', 'modified_id')}),
  )
  readonly_fields = UserAdmin.readonly_fields + ('created', 'modified', 'created_id', 'modified_id')


# Registramos el modelo User con su nuevo Admin especializado
admin.site.register(User, CustomUserAdmin) # <- ¡Cambio clave aquí!

# El resto de tus tablas se quedan exactamente igual con BaseAdmin
admin.site.register(Candidate, BaseAdmin)
admin.site.register(Recruiter, BaseAdmin)
admin.site.register(Company, BaseAdmin)
admin.site.register(Offer, BaseAdmin)
admin.site.register(Technology, BaseAdmin)
admin.site.register(Application, BaseAdmin)
admin.site.register(CandidateTechnology)
admin.site.register(OfferTechnology)