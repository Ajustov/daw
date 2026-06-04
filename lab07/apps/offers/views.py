from django.shortcuts import get_object_or_404
from django.db import models
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Offer, Candidate, Application, Recruiter, Technology, OfferTechnology, Company
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, JsonResponse
from django.core.exceptions import ValidationError

# --- FLUJO DEL CANDIDATO (Candidate) ---

def lista_ofertas(request):
    """ Obtiene la lista de ofertas de trabajo activas con filtros opcionales. """
    ofertas = Offer.objects.filter(status=True)
    
    modalidad_filtro = request.GET.get('modality', None)
    titulo_filtro = request.GET.get('title', None)
    ubicacion_filtro = request.GET.get('location', None)
    
    if modalidad_filtro:
        ofertas = ofertas.filter(modality=modalidad_filtro)
    if titulo_filtro:
        ofertas = ofertas.filter(title__icontains=titulo_filtro)
    if ubicacion_filtro:
        ofertas = ofertas.filter(location__icontains=ubicacion_filtro)
        
    data = []
    for oferta in ofertas:
        data.append({
            'id': str(oferta.id),
            'title': oferta.title,
            'location': oferta.location,
            'modality': oferta.modality,
            'seniority': oferta.seniority,
            'salary': str(oferta.salary) if oferta.salary else "No especificado"
        })
        
    return JsonResponse({'offers': data}, safe=False)

def ver_detalle_oferta(request, offer_id):
    """ Obtiene los detalles de una oferta específica y sus tecnologías asociadas. """
    oferta = get_object_or_404(Offer, id=offer_id)
    
    tecnologias_vinculadas = OfferTechnology.objects.filter(offer_id=oferta)
    
    tech_uuids = [vinculo.technology_id for vinculo in tecnologias_vinculadas]
    
    lista_tecnologias = list(
        Technology.objects.filter(id__in=tech_uuids).values_list('name', flat=True)
    )
    
    data = {
        'id': str(oferta.id),
        'title': oferta.title,
        'description': oferta.description,
        'location': oferta.location,
        'modality': oferta.modality,
        'seniority': oferta.seniority,
        'salary': str(oferta.salary) if oferta.salary else "No especificado",
        'required_technologies': lista_tecnologias  
    }
    return JsonResponse(data)


@csrf_exempt
def postular_a_oferta(request, offer_id):
    """ Registra la postulación de un candidato a una oferta de trabajo. """
    if request.method == 'POST':
        oferta = get_object_or_404(Offer, id=offer_id)
        
        try:
            body = json.loads(request.body)
            candidate_id = body.get('candidate_id')
            candidato = get_object_or_404(Candidate, id=candidate_id)
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Debe proporcionar un candidate_id válido en el JSON'}, status=400)
            
        ya_postulo = Application.objects.filter(offer_id=oferta, candidate_id=candidato).exists()
        if ya_postulo:
            return JsonResponse({'message': 'Ya te has postulado a esta oferta anteriormente.'}, status=400)
            
        usuario_creador = candidato.user_id

        nueva_postulacion = Application.objects.create(
            offer_id=oferta,
            candidate_id=candidato,
            status='pending',
            created_id=usuario_creador
        )
        
        return JsonResponse({
            'message': 'Postulación exitosa',
            'application_id': str(nueva_postulacion.id),
            'status': nueva_postulacion.status
        }, status=201) 
        
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)


def mis_postulaciones(request, candidate_id):
    """ Obtiene el historial de ofertas a las que ha aplicado un candidato específico. """
    candidato = get_object_or_404(Candidate, id=candidate_id)
    postulaciones = Application.objects.filter(candidate_id=candidato)
    
    data = []
    for postu in postulaciones:
        reclutador = Recruiter.objects.filter(id=postu.offer_id.recruiter_id).first()
        nombre_empresa = reclutador.company_id.name if reclutador and reclutador.company_id else "No especificada"

        data.append({
            'application_id': str(postu.id),
            'offer_title': postu.offer_id.title,
            'company': nombre_empresa, 
            'status': postu.status,
            'applied_at': postu.created.strftime('%Y-%m-%d %H:%M') if postu.created else "No registrada"
        })
        
    return JsonResponse({'my_applications': data}, safe=False)


# --- FLUJO DEL RECLUTADOR (Recruiter / Company) ---

@csrf_exempt
def crear_oferta(request):
    """ Permite a un reclutador registrar una nueva oferta de trabajo en el sistema. """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            recruiter_id = body.get('recruiter_id')
            reclutador = get_object_or_404(Recruiter, id=recruiter_id)
            
            usuario_creador = reclutador.user_id
            
            nueva_oferta = Offer.objects.create(
                recruiter_id=reclutador.id,
                title=body.get('title'),
                description=body.get('description'),
                location=body.get('location'),
                modality=body.get('modality'),
                seniority=body.get('seniority'),
                salary=body.get('salary', None),
                created_id=usuario_creador
            )
            
            return JsonResponse({
                'message': 'Oferta de trabajo publicada con éxito',
                'offer_id': str(nueva_oferta.id)
            }, status=201)
            
        except KeyError as e:
            return JsonResponse({'error': f'Falta el campo obligatorio: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error_detallado': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)


def ver_postulados_oferta(request, offer_id):
    """ Obtiene la lista de candidatos que han aplicado a una oferta de trabajo. """
    oferta = get_object_or_404(Offer, id=offer_id)
    postulaciones = Application.objects.filter(offer_id=oferta)
    
    candidatos_data = []
    for postu in postulaciones:
        candidato = postu.candidate_id
        candidatos_data.append({
            'application_id': str(postu.id),
            'candidate_id': str(candidato.id),
            'candidate_name': candidato.user_id.get_full_name(),
            'experience_years': candidato.experienceYears,
            'seniority': candidato.seniority,
            'current_status': postu.status
        })
        
    return JsonResponse({
        'offer_title': oferta.title,
        'total_applicants': postulaciones.count(),
        'applicants': candidatos_data
    })


@csrf_exempt
def actualizar_estado_postulacion(request, application_id):
    """ Actualiza el estado de una postulación específica. """
    if request.method in ['PUT', 'POST']:
        postulacion = get_object_or_404(Application, id=application_id)
        
        try:
            body = json.loads(request.body)
            nuevo_estado = body.get('status')
            
            estados_validos = ['pending', 'reviewed', 'rejected', 'hired']
            if nuevo_estado not in estados_validos:
                return JsonResponse({'error': 'Estado no válido. Use pending, reviewed, rejected o hired.'}, status=400)
                
            postulacion.status = nuevo_estado
            postulacion.save()
            
            return JsonResponse({
                'message': 'Estado de postulación actualizado correctamente',
                'application_id': str(postulacion.id),
                'new_status': postulacion.status
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
            
    return JsonResponse({'error': 'Método no permitido. Use POST o PUT.'}, status=405)


# --- VISTAS DEL PERFIL / DASHBOARD (Comunes) ---

@csrf_exempt
def editar_perfil_candidato(request, candidate_id):
    """ Actualiza los datos básicos del perfil de un candidato. """
    if request.method in ['POST', 'PUT']:
        candidato = get_object_or_404(Candidate, id=candidate_id)
        
        try:
            body = json.loads(request.body)
            
            if 'experienceYears' in body:
                candidato.experienceYears = int(body.get('experienceYears'))
                
            if 'description' in body:
                candidato.description = body.get('description')
                
            candidato.save()
            
            return JsonResponse({
                'message': 'Perfil de candidato actualizado correctamente',
                'experienceYears': candidato.experienceYears,
                'description': candidato.description
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def dashboard(request, user_id):
    """ Identifica el rol del usuario para retornar la información personalizada de su panel. """
    es_candidato = Candidate.objects.filter(user_id=user_id).first()
    if es_candidato:
        return JsonResponse({
            'role': 'candidate',
            'message': f'Bienvenido al panel de Candidato. Tienes {es_candidato.experienceYears} años de experiencia listados.'
        })
        
    es_reclutador = Recruiter.objects.filter(user_id=user_id).first()
    if es_reclutador:
        nombre_empresa = es_reclutador.company_id.name if es_reclutador.company_id else "No asignada"
        return JsonResponse({
            'role': 'recruiter',
            'message': f'Bienvenido al panel de Reclutador de la empresa {nombre_empresa}.'
        })
        
    return JsonResponse({
        'role': 'unknown',
        'message': 'Bienvenido a DevJobs. Tu cuenta no tiene un perfil de candidato o reclutador asignado.'
    })

@csrf_exempt
def registro_candidato(request):
    """ Registra un nuevo usuario base y su perfil de Candidato con su archivo CV. """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
        
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        seniority = request.POST.get('seniority')
        experience_years = request.POST.get('experienceYears')
        
        if not all([username, password, seniority, experience_years]):
            return JsonResponse({'error': 'Faltan campos obligatorios en el formulario'}, status=400)
        
        nuevo_usuario = User.objects.create_user(
            username=username,
            password=password,
            email=request.POST.get('email', ''),
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', '')
        )
        
        archivo_cv = request.FILES.get('cv', None)
        
        nuevo_candidato = Candidate.objects.create(
            user_id=nuevo_usuario,
            description=request.POST.get('description', None),
            seniority=seniority,
            experienceYears=int(experience_years),
            cv=archivo_cv, 
            created_id=nuevo_usuario
        )
        
        return JsonResponse({
            'message': 'Usuario candidato con CV registrado de forma exitosa',
            'user_id': str(nuevo_usuario.id),
            'candidate_id': str(nuevo_candidato.id),
            'cv_uploaded': bool(archivo_cv)
        }, status=201)
        
    except ValidationError as e:
        return JsonResponse({'error_validacion': e.messages}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def registro_reclutador(request):
    """ Registra un nuevo usuario base y lo vincula a una empresa como Reclutador. """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
        
    try:
        body = json.loads(request.body)
        empresa = get_object_or_404(Company, id=body['company_id'])
        
        nuevo_usuario = User.objects.create_user(
            username=body['username'],
            password=body['password'],
            email=body.get('email', ''),
            first_name=body.get('first_name', ''),
            last_name=body.get('last_name', '')
        )
        
        nuevo_reclutador = Recruiter.objects.create(
            user_id=nuevo_usuario,
            company_id=empresa,
            description=body.get('description', None),
            created_id=nuevo_usuario
        )
        
        return JsonResponse({
            'message': 'Usuario reclutador registrado de forma exitosa',
            'user_id': str(nuevo_usuario.id),
            'recruiter_id': str(nuevo_reclutador.id)
        }, status=201)
        
    except KeyError as e:
        return JsonResponse({'error': f'Falta el campo obligatorio: {str(e)}'}, status=400)
    except ValidationError as e:
        return JsonResponse({'error_validacion': e.messages}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def login_view(request):
    """ Autentica las credenciales del usuario e inicia sesión en el sistema. """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
        
    try:
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Inicio de sesión exitoso',
                'user_id': str(user.id),
                'username': user.username
            })
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)


@csrf_exempt
def logout_view(request):
    """ Cierra la sesión activa del usuario. """
    if request.method in ['POST', 'GET']:
        logout(request)
        return JsonResponse({'message': 'Sesión cerrada correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def cerrar_oferta(request, offer_id):
    """ Deshabilita o cierra una vacante de empleo específica. """
    if request.method in ['POST', 'PUT']:
        oferta = get_object_or_404(Offer, id=offer_id)
        oferta.status = False
        oferta.save()
        
        return JsonResponse({
            'message': f'La oferta "{oferta.title}" ha sido cerrada correctamente.',
            'offer_id': str(oferta.id),
            'status': oferta.status
        })
        
    return JsonResponse({'error': 'Método no permitido. Use POST o PUT.'}, status=405)

@csrf_exempt
def vincular_tecnologias_oferta(request, offer_id):
    """ Vincula una lista de IDs de tecnologías a una oferta de trabajo específica. """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
        
    oferta = get_object_or_404(Offer, id=offer_id)
    
    try:
        body = json.loads(request.body)
        tecnologias_ids = body.get('technology_ids', [])
        
        if not isinstance(tecnologias_ids, list):
            return JsonResponse({'error': 'El campo technology_ids debe ser una lista'}, status=400)
            
        OfferTechnology.objects.filter(offer_id=oferta).delete()
        
        vinculos_creados = 0
        for tech_id in tecnologias_ids:
            tecnologia = get_object_or_404(Technology, id=tech_id)
            OfferTechnology.objects.create(offer_id=oferta, technology_id=tecnologia)
            vinculos_creados += 1
            
        return JsonResponse({
            'message': 'Tecnologías vinculadas con éxito',
            'offer_id': str(oferta.id),
            'technologies_linked_count': vinculos_creados
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def descargar_cv(request, candidate_id):
    """ Busca al candidato y descarga su archivo de currículum en formato PDF si existe. """
    candidato = get_object_or_404(Candidate, id=candidate_id)
    
    if not candidato.cv:
        return JsonResponse({'error': 'El candidato no ha subido ningún archivo de CV'}, status=404)
        
    try:
        file_handle = candidato.cv.open('rb')
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="CV_{candidato.id}.pdf"'
        return response
    except Exception as e:
        return JsonResponse({'error': f'No se pudo recuperar el archivo: {str(e)}'}, status=500)