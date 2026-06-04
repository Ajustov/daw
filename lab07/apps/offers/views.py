from django.shortcuts import get_object_or_404
from django.db import models
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Offer, Candidate, Application, Recruiter, Technology, OfferTechnology, Company
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, JsonResponse
from django.core.exceptions import ValidationError

# FLUJO DEL CANDIDATO (Candidate)

def lista_ofertas(request):
    """
    Muestra todas las ofertas de trabajo activas.
    Permite filtros combinados por modalidad, palabras clave en el título y ubicación.
    """
    ofertas = Offer.objects.filter(status=True)
    
    # Captura de Query Params
    modalidad_filtro = request.GET.get('modality', None)
    titulo_filtro = request.GET.get('title', None)
    ubicacion_filtro = request.GET.get('location', None)
    
    # Aplicación de filtros encadenados
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
    """
    Busca una oferta específica por su ID, muestra su descripción 
    y lista las tecnologías asociadas de forma segura y eficiente.
    """
    # Buscar la oferta o lanzar un 404 si el UUID no existe
    oferta = get_object_or_404(Offer, id=offer_id)
    
    # Traer los registros de la tabla intermedia para esta oferta
    tecnologias_vinculadas = OfferTechnology.objects.filter(offer_id=oferta)
    
    # Extraer los UUIDs. Debido al nombre del campo, 'vinculo.technology_id' entrega el UUID directo.
    tech_uuids = [vinculo.technology_id for vinculo in tecnologias_vinculadas]
    
    # Consultar directamente al modelo Technology usando los UUIDs en una sola consulta masiva
    lista_tecnologias = list(
        Technology.objects.filter(id__in=tech_uuids).values_list('name', flat=True)
    )
    
    # Construir y retornar la respuesta JSON
    data = {
        'id': str(oferta.id),
        'title': oferta.title,
        'description': oferta.description,
        'location': oferta.location,
        'modality': oferta.modality,
        'seniority': oferta.seniority,
        'salary': str(oferta.salary) if oferta.salary else "No especificado",
        'required_technologies': lista_tecnologias  # Ahora devolverá un array limpio de strings ['PYTHON', 'REACT']
    }
    return JsonResponse(data)


@csrf_exempt
def postular_a_oferta(request, offer_id):
    """
    Simula la postulación de un candidato a una oferta de trabajo.
    Crea un registro en la tabla Application con estado PENDING.
    """
    if request.method == 'POST':
        oferta = get_object_or_404(Offer, id=offer_id)
        
        try:
            body = json.loads(request.body)
            candidate_id = body.get('candidate_id')
            candidato = get_object_or_404(Candidate, id=candidate_id)
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Debe proporcionar un candidate_id válido en el JSON'}, status=400)
            
        # Comprobamos si el candidato ya postuló previamente a esta misma oferta
        ya_postulo = Application.objects.filter(offer_id=oferta, candidate_id=candidato).exists()
        if ya_postulo:
            return JsonResponse({'message': 'Ya te has postulado a esta oferta anteriormente.'}, status=400)
            
        # Extraemos de forma segura la instancia de usuario para evitar ValueError
        usuario_creador = candidato.user_id

        # Creamos la nueva postulación (Application)
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
        }, status=201) # Corregido de 21 a 201
        
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)


def mis_postulaciones(request, candidate_id):
    """
    Muestra el historial de ofertas a las que ha aplicado un candidato específico.
    """
    candidato = get_object_or_404(Candidate, id=candidate_id)
    postulaciones = Application.objects.filter(candidate_id=candidato)
    
    data = []
    for postu in postulaciones:
        # Buscamos el reclutador usando el UUID guardado en la oferta para obtener la empresa real
        reclutador = Recruiter.objects.filter(id=postu.offer_id.recruiter_id).first()
        nombre_empresa = reclutador.company_id.name if reclutador and reclutador.company_id else "No especificada"

        data.append({
            'application_id': str(postu.id),
            'offer_title': postu.offer_id.title,
            'company': nombre_empresa, # Corregido para que muestre la empresa real y no el título
            'status': postu.status,
            'applied_at': postu.created.strftime('%Y-%m-%d %H:%M') if postu.created else "No registrada"
        })
        
    return JsonResponse({'my_applications': data}, safe=False)


# FLUFLOW DEL RECLUTADOR (Recruiter / Company)

@csrf_exempt
def crear_oferta(request):
    """
    Permite a un reclutador registrar una nueva oferta de trabajo (Offer) en el sistema.
    """
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
    """
    Permite al reclutador ver una lista de qué candidatos han aplicado a una de sus ofertas.
    """
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
    """
    Modifica el estado de una postulación (ej: de 'pending' a 'reviewed', 'rejected' o 'hired')
    """
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


# VISTAS DEL PERFIL / DASHBOARD (Comunes)

@csrf_exempt
def editar_perfil_candidato(request, candidate_id):
    """
    Actualiza datos básicos del perfil del candidato como los años de experiencia.
    """
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
    """
    Vista inteligente de bienvenida. Identifica qué tipo de rol tiene el 'user_id'
    (Candidato o Reclutador) y le da una respuesta personalizada.
    """
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
    """
    Registra un nuevo usuario y su perfil de Candidato incluyendo la subida del CV.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
        
    try:
        # Adaptado para form.data mediante Postaman o formularios HTML tradicionales
        username = request.POST.get('username')
        password = request.POST.get('password')
        seniority = request.POST.get('seniority')
        experience_years = request.POST.get('experienceYears')
        
        if not all([username, password, seniority, experience_years]):
            return JsonResponse({'error': 'Faltan campos obligatorios en el formulario'}, status=400)
        
        # Crear el usuario base
        nuevo_usuario = User.objects.create_user(
            username=username,
            password=password,
            email=request.POST.get('email', ''),
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', '')
        )
        
        # Capturar el archivo PDF desde request.FILES
        archivo_cv = request.FILES.get('cv', None)
        
        # Crear el perfil de Candidato vinculado
        nuevo_candidato = Candidate.objects.create(
            user_id=nuevo_usuario,
            description=request.POST.get('description', None),
            seniority=seniority,
            experienceYears=int(experience_years),
            cv=archivo_cv, # Django se encarga de guardarlo en la carpeta /cv/ gracias al modelo
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
    """
    Registra un nuevo usuario base y lo vincula a una empresa existente como Reclutador.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
        
    try:
        body = json.loads(request.body)
        empresa = get_object_or_404(Company, id=body['company_id'])
        
        # 1. Crear el usuario base
        nuevo_usuario = User.objects.create_user(
            username=body['username'],
            password=body['password'],
            email=body.get('email', ''),
            first_name=body.get('first_name', ''),
            last_name=body.get('last_name', '')
        )
        
        # 2. Crear el perfil de Reclutador vinculado
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
    """
    Autentica las credenciales del usuario e inicia sesión en el sistema.
    """
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
    """
    Cierra la sesión activa del usuario.
    """
    if request.method in ['POST', 'GET']:
        logout(request)
        return JsonResponse({'message': 'Sesión cerrada correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def cerrar_oferta(request, offer_id):
    """
    Permite al reclutador deshabilitar o cerrar una vacante de empleo.
    """
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
    """
    Vincula una lista de IDs de tecnologías a una oferta de trabajo específica.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
        
    oferta = get_object_or_404(Offer, id=offer_id)
    
    try:
        body = json.loads(request.body)
        tecnologias_ids = body.get('technology_ids', [])
        
        if not isinstance(tecnologias_ids, list):
            return JsonResponse({'error': 'El campo technology_ids debe ser una lista'}, status=400)
            
        # Limpieza previa opcional para evitar duplicados en actualizaciones complejas
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
    """
    Busca al candidato y descarga su archivo de currículum en formato PDF si existe.
    """
    candidato = get_object_or_404(Candidate, id=candidate_id)
    
    if not candidato.cv:
        return JsonResponse({'error': 'El candidato no ha subido ningún archivo de CV'}, status=404)
        
    try:
        # Abrimos el archivo en modo lectura binaria
        file_handle = candidato.cv.open('rb')
        response = FileResponse(file_handle, content_type='application/pdf')
        # Configura la descarga directa en el navegador/Postman
        response['Content-Disposition'] = f'attachment; filename="CV_{candidato.id}.pdf"'
        return response
    except Exception as e:
        return JsonResponse({'error': f'No se pudo recuperar el archivo: {str(e)}'}, status=500)
    