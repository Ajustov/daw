# apps/offers/views/__init__.py

# Exponemos las clases principales de cada archivo de vistas
from .user_views import UserViewSet
from .company_views import CompanyViewSet
from .recruiter_views import RecruiterViewSet
from .candidate_views import CandidateViewSet
from .technology_views import TechnologyViewSet
from .offer_views import OfferViewSet
from .application_views import ApplicationViewSet

# También las vistas que no son ViewSets (ej. Auth y Métricas)
from .auth_views import LoginView
from .registration_views import RegistroCandidatoView, RegistroReclutadorView
from .application_metrics_views import DashboardMetricasView