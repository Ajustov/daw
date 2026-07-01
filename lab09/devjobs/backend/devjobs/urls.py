from apps.jobs.api.endpoints.applications import router_applications
from apps.jobs.api.endpoints.auth import router_auth
from apps.jobs.api.endpoints.candidates import router_candidates
from apps.jobs.api.endpoints.companies import router_companies
from apps.jobs.api.endpoints.locations import router_locations
from apps.jobs.api.endpoints.offers import router_offers
from apps.jobs.api.endpoints.recruiters import router_recruiters
from apps.jobs.api.endpoints.technologies import router_technologies
from apps.jobs.api.endpoints.users import router_users
from django.contrib import admin
from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaExtraAPI()
# Agregamos los endpoints de ninja-extra que depende de ninja-jwt
api.register_controllers(NinjaJWTDefaultController)
api.add_router('/candidates', router_candidates)
api.add_router('/recruiters', router_recruiters)
api.add_router('/companies', router_companies)
api.add_router('/users', router_users)
api.add_router('/auth', router_auth)
api.add_router('/technologies', router_technologies)
api.add_router('/offers', router_offers)
api.add_router('/applications', router_applications)
api.add_router('/locations', router_locations)

urlpatterns = [path('admin/', admin.site.urls), path('api/', api.urls)]
