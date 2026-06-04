# DevJobs API - Backend con Django - Implementación del Views

Este repositorio contiene la implementación práctica del **Laboratorio 07: Implementación del Views** para el curso de **Desarrollo de Aplicaciones Web** en la **Universidad Nacional de San Agustín de Arequipa (UNSA)**. 

## Integrantes del Grupo
* **García Daza, Luis Alberto**
* **Condori Catasi, Jonnier Angel**
* **Justo Vilca, Alessandro Josue**

**Semestre Académico:** 2026-A

---

## Objetivos del Proyecto
* Implementar vistas basadas en funciones (FBVs) en Django para procesar la lógica de negocio de candidatos y reclutadores.
* Configurar rutas URL dinámicas empleando el convertidor `<uuid:>` para asegurar identificadores persistentes y evitar ataques de enumeración secuencial.
* Validar operaciones de lectura y escritura (GET, POST, PUT) manejando códigos de estado HTTP correctos (200, 201, 400, 405) y respuestas JSON.
* Estructurar un entorno de pruebas optimizado en Postman (entorno Lab_07) mediante la variable global `{{base_url}}` para un desarrollo iterativo.

---

## Tecnologías y Arquitectura
* **Backend:** Django Framework. Utilizando nativamente el patrón MVT, enfocado puramente en la Vista y el Modelo, retornando colecciones estructuradas mediante `JsonResponse` (sin usar Plantillas).
* **Testing de API:** Postman para emulación de peticiones HTTP de clientes, al no disponer de frontend en esta etapa.

---

## Endpoints Principales y Enrutamiento (`urls.py`)

El archivo despachador organiza de manera granular los patrones de búsqueda, haciendo uso explícito de UUIDs para capturar parámetros de forma segura:

### Flujo del Candidato
* `GET /ofertas/` - Lista ofertas de trabajo activas (`status=True`) con filtros opcionales por modalidad, título y ubicación.
* `GET /ofertas/<uuid:offer_id>/` - Muestra detalles de la oferta cruzando información para devolver las tecnologías requeridas.
* `POST /ofertas/<uuid:offer_id>/postular/` - Registra una postulación validando que no se repitan aplicaciones a la misma oferta.
* `GET /candidatos/<uuid:candidate_id>/postulaciones/` - Historial completo de postulaciones del candidato.
* `GET /candidatos/<uuid:candidate_id>/descargar-cv/` - Descarga segura del currículum en formato PDF mediante un flujo binario `FileResponse`.
* `POST/PUT /candidatos/<uuid:candidate_id>/editar/` - Actualiza los datos del perfil (experiencia y descripción).

### Flujo del Reclutador / Empresa
* `POST /ofertas/crear/` - Recibe un JSON básico y publica una nueva oferta.
* `GET /ofertas/<uuid:offer_id>/postulados/` - Lista todos los aplicantes a una oferta concreta desglosando su perfil.
* `POST/PUT /postulaciones/<uuid:application_id>/estado/` - Transiciona el estado de postulación entre valores controlados (pending, reviewed, rejected, hired).
* `POST/PUT /ofertas/<uuid:offer_id>/cerrar/` - Cambia el estado lógico a inactivo (`status=False`).
* `POST /ofertas/<uuid:offer_id>/tecnologias/` - Asocia un listado masivo de IDs de tecnologías a una vacante.

### Autenticación y Comunes
* `POST /auth/registro/candidato/` - Crea el usuario base (`create_user`) y sube el archivo CV en PDF.
* `POST /auth/registro/reclutador/` - Crea un usuario reclutador vinculándolo relacionalmente a una empresa.
* `POST /auth/login/` e `GET/POST /auth/logout/` - Gestión de sesiones a través del sistema nativo de autenticación de Django.
* `GET /dashboard/<uuid:user_id>/` - Inspecciona el rol y sirve las respuestas dinámicas correspondientes al panel.

---

## Detalles de Implementación de las Vistas (`views.py`)

La capa lógica del backend está desarrollada exclusivamente mediante **Vistas Basadas en Funciones (FBVs)**. Cada vista procesa peticiones HTTP específicas, interactúa con la base de datos a través del ORM de Django y retorna estructuras estandarizadas en formato JSON mediante `JsonResponse`.

A continuación se detalla la lógica interna y las validaciones clave implementadas en los controladores:

### 1. Gestión de Usuarios y Autenticación
* **`registro_candidato(request)` [POST]:** * Deserializa los datos del formulario (`request.POST`).
  * Utiliza `User.objects.create_user` para registrar de forma segura las credenciales en la tabla nativa de Django (con hashing de contraseña).
  * Instancia el perfil de tipo `Candidate`.
  * Gestiona la persistencia física del archivo **Curriculum Vitae (PDF)**, almacenándolo en el directorio `media/` del servidor y asociando la ruta al registro del candidato.
* **`registro_reclutador(request)` [POST]:** * Extrae los datos del payload JSON y crea el usuario base.
  * Realiza una búsqueda relacional para vincular al nuevo usuario con una empresa (`Company`) existente mediante su identificador.
* **`login_view(request)` [POST] / `logout_view(request)` [POST/GET]:**
  * Invoca los métodos nativos `authenticate()`, `login()` y `logout()` de Django.
  * Valida la correspondencia de credenciales antes de iniciar la sesión de usuario y maneja el control de sesiones activas por medio de cookies del lado del cliente.

### 2. Controlador de Candidatos
* **`lista_ofertas(request)` [GET]:**
  * Recupera únicamente las vacantes con estado activo (`status=True`).
  * Implementa filtros opcionales leídos desde los parámetros de consulta de la URL (`request.GET.get()`), tales como `modality`, `title` y `location`.
  * Serializa los resultados en un arreglo de diccionarios dentro de un objeto `JsonResponse`.
* **`ver_detalle_oferta(request, offer_id)` [GET]:**
  * Busca la vacante utilizando su identificador seguro `UUID`. Lanza un error HTTP 404 si el recurso no existe.
  * Realiza una consulta a la tabla asociativa `OfferTechnology` para mapear y concatenar los nombres de las herramientas técnicas solicitadas.
* **`postular_a_oferta(request, offer_id)` [POST]:**
  * Valida la identidad del candidato autenticado.
  * Ejecuta una validación de redundancia: comprueba si ya existe un registro en `Application` que vincule al mismo candidato con la misma oferta para impedir postulaciones duplicadas.
  * Si la validación pasa, registra la postulación con estado inicial `pending` (código HTTP 201).
* **`descargar_cv(request, candidate_id)` [GET]:**
  * Recupera de la base de datos la ruta del archivo PDF del candidato.
  * Abre el archivo en modo de lectura binaria y lo sirve mediante un objeto `FileResponse`, configurando los headers HTTP apropiados (`Content-Type: application/pdf`) para forzar o permitir la descarga segura.

### 3. Controlador de Reclutadores y Empresas
* **`crear_oferta(request)` [POST]:**
  * Extrae el payload en formato JSON desde el cuerpo de la petición (`json.loads(request.body)`).
  * Crea una nueva instancia en la entidad `Offer`, asociándola de forma obligatoria con el reclutador autenticado.
* **`ver_postulados_oferta(request, offer_id)` [GET]:**
  * Filtra la tabla `Application` por el `UUID` de la oferta seleccionada.
  * Extrae la información detallada de los perfiles de los candidatos aplicantes (experiencia, descripción, datos de contacto) para construir el reporte del reclutador.
* **`actualizar_estado_postulacion(request, application_id)` [POST/PUT]:**
  * Modifica el campo de estado dentro del registro de la postulación.
  * Restringe las transiciones únicamente a los valores predefinidos en las reglas de negocio del flujo de selección: `pending`, `reviewed`, `rejected` y `hired`.

---

## Validaciones Generales y Manejo de Errores

Para garantizar un comportamiento robusto frente a peticiones malformadas o flujos incorrectos, todas las vistas incorporan las siguientes capas de control:

1. **Restricción de Métodos HTTP:** Se valida rigurosamente el método de la petición (`request.method`). Si un endpoint diseñado para `POST` recibe una petición `GET`, responde inmediatamente con un código **HTTP 405 Method Not Allowed**.
2. **Manejo de Excepciones de Base de Datos:** Las consultas críticas están envueltas en bloques `try-except`. La ausencia de un recurso (por ejemplo, un `UUID` inválido) es capturada mediante la excepción `DoesNotExist` y manejada devolviendo una respuesta limpia con código **HTTP 404 Not Found**.
3. **Decodificación Segura de JSON:** Las peticiones de tipo de escritura procesan el cuerpo de la solicitud de manera segura. Ante payloads corruptos o con formato JSON inválido, el sistema responde con un código **HTTP 400 Bad Request**.
4. **Respuestas Estandarizadas:** Todas las respuestas mantienen una estructura homogénea:
   * **Éxito:** `{"status": "success", "data": {...}}` o `{"status": "success", "message": "..."}`
   * **Fallo:** `{"status": "error", "message": "Descripción detallada del error"}`

---

## Repositorio y Demostración
* **Código Fuente:** [https://github.com/Ajustov/daw.git](https://github.com/Ajustov/daw.git)
* **Video Demostrativo:** [Ver en Google Drive](https://drive.google.com/drive/folders/1RWgZ992i-1C1FMqVgtoU_Saz5_I0cL6L?usp=sharing)

---

## Conclusiones
* **Arquitectura:** El diseño y codificación de vistas basadas en funciones permitió estructurar una solución clara para resolver validaciones cruciales del lado del servidor, como el control de duplicados.
* **Seguridad:** La sustitución de llaves primarias tradicionales por `<uuid:>` eleva los estándares, previniendo ataques de recolección de datos y protegiendo identidades.
* **Eficiencia en Pruebas:** La organización paramétrica (`base_url`) en Postman agilizó el ciclo de vida del desarrollo y permitió simular escenarios reales de integración.
* **Robustez de la API:** La estandarización en JSON junto con códigos HTTP explícitos establece un contrato predecible para que futuros desarrollos web o móviles puedan consumirla sin fricciones.