# Proyecto : DevJobs

## Descripción de la aplicación web

DevJobs es una plataforma web Full Stack especializada en la búsqueda, publicación y filtrado de empleo en el sector tecnológico. A diferencia de las bolsas de trabajo tradicionales generalistas, DevJobs permite filtrar ofertas laborales de manera muy precisa utilizando criterios nativos de la industria: el **Stack Tecnológico** (lenguajes, frameworks y herramientas) y el nivel de **Seniority** (Intern, Junior, Semi-Senior, Senior, Lead).

La arquitectura del sistema fue diseñada con un enfoque moderno y modular. Permite que cualquier usuario registrado gestione perfiles independientes de **Candidato** y **Reclutador** dentro de una misma cuenta basándose en una estrategia progresiva y no excluyente. De esta manera, un usuario puede buscar empleo y, al mismo tiempo o en el futuro, publicar vacantes para su empresa.

El módulo del **Candidato** permite explorar ofertas en tiempo real (mediante técnicas de *debounce* y multicriterio), postularse de forma ágil en un solo clic, evitar postulaciones duplicadas e interactuar con un panel para realizar el seguimiento del estado de sus aplicaciones (*Pending*, *Reviewed*, *Hired*, *Rejected*). Por otro lado, el módulo del **Reclutador** ofrece un panel integral para publicar vacantes con etiquetas dinámicas de tecnologías, gestionar el ciclo de vida de cada oferta laboral y administrar las postulaciones recibidas.

Todo el ecosistema está respaldado por estándares de alta seguridad, implementación rigurosa de control de acceso basado en roles, autenticación mediante **JSON Web Tokens (JWT)** con mecanismos de rotación y *blacklist*, lógica de validación centralizada en el Backend y persistencia en una base de datos relacional robusta con eliminaciones lógicas (*soft deletes*) y trazabilidad de auditoría.

---

# Equipo

| Integrante | Rol | Porcentaje |
|---|---|---|
| Luis Alberto García Daza | Desarrollador Full Stack | 100% |
| Jonnier Angel Condori Catasi | Desarrollador Backend | 100% |
| Alessandro Josue Justo Vilca | Desarrollador de la Base de Datos (backend) | 100% |
| | **Total** | **100%** |

---

# Entregables

| **Entregable** | **Enlace** |
|----------------|------------|
| Frontend Deploy | <https://devjobs-frontend-0r4h.onrender.com> |
| Backend Deploy (API REST) | <https://devjobs-backend-ovi4.onrender.com> |
| Documentación API (Swagger/OpenAPI) | <https://devjobs-backend-ovi4.onrender.com/api/docs> |
| Informe Final | <https://drive.google.com/file/d/1c408lOlv9dmLFeD_AQ39-PEE5qyjAvOM/view?usp=drive_link> |
| Poster DevJobs | <https://drive.google.com/file/d/1L74ktfx-Sobwt0JZjCjLgYvVhgKlyXH-/view?usp=drive_link> |

---

# Tecnología utilizada

| Ítem | Tecnología |
|---|---|
| Entorno de Desarrollo | GNU/Linux / Windows |
| | Git |
| | GitHub |
| | Visual Studio Code |
| Frontend | React 19 |
| | TypeScript |
| | Vite |
| | React Router DOM v7 |
| | TanStack Query v5 (React Query) |
| | Zustand (Gestión de estado global y sesión) |
| | Tailwind CSS v4 |
| | Shadcn UI + Lucide React (Componentes de interfaz) |
| | React Hook Form + Zod (Validación de formularios) |
| | Axios |
| Backend | Python 3 |
| | Django 5.2 |
| | Django Ninja (API REST declarativa con Pydantic) |
| | Django Ninja JWT / Extra (Autenticación y rotación de tokens) |
| | Uvicorn (Servidor ASGI de alto rendimiento) |
| | uv (Gestor de dependencias ultrarrápido para Python) |
| | django-cors-headers |
| Base de datos | PostgreSQL 16 |
| | psycopg2 / psycopg2-binary |
| Despliegue e Infraestructura| Render (Frontend, Backend y Base de Datos) |
| | Docker & Docker Compose |
| Pruebas y API Docs | Swagger UI / Redoc (Generados por Django Ninja) |
| | Postman |

---

# Estructura del proyecto

El proyecto está separado formalmente en dos repositorios/módulos principales para desacoplar las responsabilidades y permitir un despliegue independiente:

```text
DevJobs/
├── backend/ (DevJobs_Backend)
│   ├── config/                     # Configuración global de Django (settings, urls, wsgi, asgi)
│   ├── core/                       # Aplicación principal de la lógica de negocio
│   ├── api/                        # Capa de presentación de API REST (Django Ninja Routers)
│   │   ├── api.py                  # Instancia principal de NinjaAPI y registro de enrutadores
│   │   ├── auth.py                 # Endpoints de autenticación, login, registro y rotación de tokens
│   │   ├── jobs.py                 # Endpoints CRUD para ofertas de trabajo
│   │   ├── applications.py         # Endpoints para postulaciones y gestión de candidatos
│   │   └── profiles.py             # Endpoints para perfiles (Candidato/Reclutador)
│   ├── schemas/                    # Contratos de datos (Pydantic Schemas de entrada y salida)
│   ├── models/                     # Modelos ORM relacionales (User, CandidateProfile, JobProfile, Job, etc.)
│   ├── migrations/                 # Historial de control de versiones de la base de datos
│   ├── Dockerfile                  # Contenedor para despliegue en producción
│   ├── pyproject.toml / uv.lock     # Control de dependencias de Python con `uv`
│   └── README.md
│
├── frontend/ (DevJobs_Frontend)
│   ├── public/                     # Activos estáticos
│   ├── src/
│   │   ├── api/                    # Configuración de Axios con interceptores de tokens JWT
│   │   ├── components/             # Componentes modulares y reutilizables
│   │   │   ├── ui/                 # Componentes base del sistema de diseño (Shadcn UI)
│   │   │   ├── jobs/               # Tarjetas de ofertas, filtros multicriterio, modales
│   │   │   └── layout/             # Navbar, Footer, Contenedores principales
│   │   ├── hooks/                  # Custom hooks (e.g., useDebounce para búsqueda en tiempo real)
│   │   ├── pages/                  # Vistas principales del enrutador
│   │   │   ├── auth/               # Login, Registro, Recuperación
│   │   │   ├── jobs/               # Explorador de ofertas, Detalle de vacante
│   │   │   ├── candidate/          # Dashboard de postulaciones y gestión de currículum
│   │   │   └── recruiter/          # Publicación de empleos y administración de candidatos
│   │   ├── store/                  # Estado global de la sesión (Zustand)
│   │   ├── types/                  # Definiciones estáticas de tipos e interfaces TypeScript
│   │   ├── utils/                  # Formateadores, validadores y funciones auxiliares
│   │   ├── App.tsx                 # Configuración de proveedores (QueryClient, Router)
│   │   └── main.tsx                # Punto de entrada de la aplicación React
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── README.md
│
└── README.md
```


# Funcionalidades Principales

## Registro y Autenticación Segura
* **Gestión de sesiones:** Autenticación basada en tokens JWT.
* **Seguridad avanzada:** Rotación automática de *Refresh Tokens*.
* **Cierre de sesión seguro:** Mecanismo de lista negra (*blacklist*) para invalidar sesiones activas.

## Perfiles Duales (Candidato / Reclutador)
* **Sistema progresivo:** Arquitectura no excluyente vinculada a una sola cuenta.
* **Alternancia transparente:** Permite activar y cambiar de rol sin cerrar sesión.
* **Flexibilidad:** Acceso simultáneo a búsqueda de empleo y gestión de selección.

## Filtrado Multicriterio en Tiempo Real
* **Optimización:** Motor de búsqueda combinada con técnicas de *debounce* para proteger el servidor.
* **Filtros simultáneos:**
  * **Texto:** Palabra clave por título o descripción.
  * **Geografía:** Ubicación física del puesto.
  * **Modalidad:** Presencial (*On-site*), híbrido (*Hybrid*) o remoto (*Remote*).
  * **Stack Tecnológico:** Etiquetas dinámicas (ej. React, Python, Docker).
  * **Experiencia:** Niveles de *Seniority* (Intern, Junior, Semi-Senior, Senior, Lead).

## Módulo de Candidatos
* **Perfil profesional:** Configuración de *skills*, biografía y enlaces (GitHub, LinkedIn, portafolio).
* **Postulación rápida:** Aplicación a vacantes con un solo clic (*One-Click Apply*).
* **Integridad de datos:** Prevención estricta de postulaciones duplicadas en la base de datos.
* **Panel de control:** *Dashboard* de seguimiento para monitorear estados en tiempo real (*Pending, Reviewed, Hired, Rejected*).

## Módulo de Reclutadores
* **Publicación ágil:** Formulario asistido para crear y editar ofertas laborales.
* **Variables dinámicas:** Gestión de etiquetas tecnológicas y rangos salariales proyectados.
* **Seguimiento de vacantes:** Panel centralizado para revisar la lista de candidatos postulados.
* **Flujo de selección:** Capacidad de evaluar y cambiar el estado de cada postulación.

## Seguridad y Control de Acceso Granular
* **Validación en backend:** Permisos declarativos centralizados por cada endpoint.
* **Verificación de propiedad:** Los reclutadores solo gestionan postulantes de sus propias vacantes.
* **Persistencia segura:** Borrado lógico (*Soft Delete*) para mantener la integridad referencial y reportes históricos.

## Documentación Dinámica de la API
* **Estándar interactivo:** Exposición de endpoints en vivo mediante OpenAPI y Swagger UI.
* **Acceso directo:** Consola de pruebas generada directamente desde el servidor.


#Referencias y Documentación

## Herramientas de Desarrollo y Control de Versiones
* [Git](https://git-scm.com/) - Sistema de control de versiones.
* [GitHub](https://github.com/) - Plataforma de alojamiento de código.
* [Visual Studio Code](https://code.visualstudio.com/) - Editor de código fuente.

## Frontend (React & TypeScript Ecosystem)
* [React](https://es.react.dev/) - Biblioteca para interfaces de usuario.
* [TypeScript](https://www.typescriptlang.org/docs/) - Superset de JavaScript con tipado estático.
* [Vite](https://vite.dev/guide/) - Herramienta de construcción y empaquetador.
* [React Router](https://reactrouter.com/) - Enrutamiento declarativo para React.
* [TanStack Query](https://tanstack.com) - Gestión y sincronización de estado asíncrono.
* [Zustand](https://github.com/pmndrs/zustand) - Gestión de estado global simplificada.

## Diseño y Estilos
* [Tailwind CSS](https://tailwindcss.com/docs) - Framework de CSS utilitario.
* [shadcn/ui](https://ui.shadcn.com/) - Componentes de interfaz reutilizables y accesibles.

## Formularios y Validación
* [React Hook Form](https://react-hook-form.com/) - Validación de formularios flexible y extensible.
* [Zod](https://zod.dev/) - Declaración y validación de esquemas TypeScript.

## Backend & API Client
* [Axios](https://axios-http.com/docs/intro) - Cliente HTTP basado en promesas.
* [Python](https://www.python.org/doc/) - Lenguaje de programación del backend.
* [Django](https://docs.djangoproject.com/) - Framework web para el backend.
* [Django Ninja](https://django-ninja.rest/) - Framework para APIs REST basado en tipos de Python.

## Base de Datos, Entorno y Despliegue
* [uv](https://github.com/astral-sh/uv) - Gestor rápido de paquetes y entornos de Python.
* [PostgreSQL](https://www.postgresql.org/docs/) - Sistema de base de datos relacional.
* [Docker](https://docs.docker.com/) - Plataforma de contenedores.
* [Render](https://render.com/docs) - Plataforma de alojamiento y despliegue en la nube.

## Documentación y Pruebas de API
* [OpenAPI / Swagger](https://swagger.io/specification/) - Especificación para describir APIs REST.
* [Postman](https://learning.postman.com/) - Plataforma para el desarrollo y pruebas de APIs.
