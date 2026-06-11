# apps/offers/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.offers.views import (
    user_views, 
    company_views, 
    recruiter_views, 
    candidate_views, 
    technology_views, 
    offer_views, 
    application_views,
    auth_views,
    registration_views,
    application_metrics_views,
    candidate_technology_views,  # <- Agregado
    offer_match_views            # <- Agregado
)

router = DefaultRouter()

# Registros de ViewSets estándar (CRUD)
router.register(r'users', user_views.UserViewSet, basename='user')
router.register(r'companies', company_views.CompanyViewSet, basename='company')
router.register(r'recruiters', recruiter_views.RecruiterViewSet, basename='recruiter')
router.register(r'candidates', candidate_views.CandidateViewSet, basename='candidate')
router.register(r'technologies', technology_views.TechnologyViewSet, basename='technology')
router.register(r'offers', offer_views.OfferViewSet, basename='offer')
router.register(r'applications', application_views.ApplicationViewSet, basename='application')

# Registro para la asignación masiva de tecnologías por candidato
router.register(r'candidate-technologies', candidate_technology_views.CandidateTechnologyViewSet, basename='candidate-technology')

urlpatterns = [
    path('', include(router.urls)),

    # Autenticación y Cierre de Sesión
    path('auth/login/', auth_views.LoginView.as_view(), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'), 
    
    # Registro de Perfiles (CORREGIDO)
    path('registro-candidato/', registration_views.RegistroCandidatoView.as_view(), name='registro-candidato'),
    path('registro-reclutador/', registration_views.RegistroReclutadorView.as_view(), name='registro-reclutador'),

    # Motor de Match Técnico
    path('candidates/<uuid:candidate_id>/sugerencias/', offer_match_views.OfertasSugeridasView.as_view(), name='ofertas-sugeridas'),

    # Métricas del Reclutador
    path('metrics/<uuid:recruiter_id>/', application_metrics_views.DashboardMetricasView.as_view(), name='dashboard-metrics'),
]