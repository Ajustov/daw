from django.contrib import admin
from django.urls import path
from apps.offers import views  # Importamos tus vistas

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLS DEL CANDIDATO
    path('ofertas/', views.lista_ofertas, name='lista_ofertas'),
    
    path('ofertas/<uuid:offer_id>/', views.ver_detalle_oferta, name='ver_detalle_oferta'),
    
    path('ofertas/<uuid:offer_id>/postular/', views.postular_a_oferta, name='postular_a_oferta'),
    
    path('candidatos/<uuid:candidate_id>/postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),

    # URLS DEL RECLUTADOR 
    path('ofertas/crear/', views.crear_oferta, name='crear_oferta'),
    
    path('ofertas/<uuid:offer_id>/postulados/', views.ver_postulados_oferta, name='ver_postulados_oferta'),
    
    path('postulaciones/<uuid:application_id>/estado/', views.actualizar_estado_postulacion, name='actualizar_estado_postulacion'),

    # URLS COMUNES
    path('candidatos/<uuid:candidate_id>/editar/', views.editar_perfil_candidato, name='editar_perfil_candidato'),
    
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),

    # NUEVAS RUTAS SISTEMA DE AUTENTICACIÓN
    path('auth/registro/candidato/', views.registro_candidato, name='registro_candidato'),

    path('auth/registro/reclutador/', views.registro_reclutador, name='registro_reclutador'),

    path('auth/login/', views.login_view, name='login'),

    path('auth/logout/', views.logout_view, name='logout'),

    # NUEVAS RUTAS OPERATIVAS RECLUTADOR
    path('ofertas/<uuid:offer_id>/cerrar/', views.cerrar_oferta, name='cerrar_oferta'),

    path('ofertas/<uuid:offer_id>/tecnologias/', views.vincular_tecnologias_oferta, name='vincular_tecnologias_oferta'),

    path('candidatos/<uuid:candidate_id>/descargar-cv/', views.descargar_cv, name='descargar_cv'),
]
