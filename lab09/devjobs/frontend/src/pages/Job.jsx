import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import { useRouter } from '../hooks/useRouter'
import { Link } from '../components/Link'
import snarkdown from 'snarkdown'
import styles from './Job.module.css'
import { useAuthStore } from '../store/authStore'
import { useFavoritosStore } from '../store/favoritosStore'

function JobSection ({ titulo, contenido }) {
  const html = snarkdown(contenido)
  return (
    <section>
      <h2>
        {titulo}
      </h2>
      <div
        dangerouslySetInnerHTML={{ __html: html }} // Para renderizar html si o si
      />
    </section>
  )
}

function JobFavoritoBtn ({ id }) {
  const { alternarFavorito, isFavorito } = useFavoritosStore()
  const { isLogueado } = useAuthStore()
  const manejarFavorito = () => {
    alternarFavorito(id)
  }

  return (
    <button
      onClick={manejarFavorito}
      disabled={!isLogueado}
    >
      {isFavorito(id) ? '❤️' : '🤍'}
    </button>
  )
}

export default function Job () {
  // El 'id' tiene que ser el mismo que aparece en jobs/id
  const { id } = useParams()
  const [job, setJob] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const { isLogueado } = useAuthStore()

  useEffect(() => {
    fetch(`http://localhost:3000/trabajos/${id}`)
      .then(response => {
        // Verificar si la response dio okey
        if (!response.ok) throw new Error('Job no encontrado')
        return response.json()
      })
      .then(json => {
        setJob(json)
      })
      .catch(error => {
        setError(error.message)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [id])

  const { navegarA } = useRouter()

  if (loading) {
    return (
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 1rem' }}>
        <div className={styles.loading}>
          <p className={styles.loadingText}>Cargando...</p>
        </div>
      </div>
    )
  }

  if (error || !job) {
    return (
      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 1rem' }}>
        <div className={styles.error}>
          <h2 className={styles.errorTitle}>
            Empleo no encontrado
          </h2>
          <button
            className={styles.errorBtn}
            onClick={() => navegarA('/')}
          >
            Volver al inicio
          </button>
        </div>
      </main>
    )
  }
  return (
    <main className={styles.mainJob}>
      <nav className={styles.breadcrumb}>
        <Link href='/busqueda'>Empleos</Link>
        <span className={styles.breadcrumbSeparacion}>/</span>
        <span className={styles.breadcrumbActual}>{job.titulo}</span>
      </nav>
      <article>
        <header>
          <div className={styles.column1}>
            <h1 className={styles.title}>
              {job.titulo}
            </h1>
            <p className={styles.meta}>
              {job.empresa} · {job.ubicacion}
            </p>
          </div>
          <div className={styles.column2}>
            <button disabled={!isLogueado}>
              {isLogueado ? 'Aplicar ahora' : 'Inicia sesión para aplicar'}
            </button>
            <JobFavoritoBtn id={id} />
          </div>
        </header>
        <JobSection
          titulo='Descripción del puesto'
          contenido={job.content.description}
        />
        <JobSection
          titulo='Responsabilidades'
          contenido={job.content.responsibilities}
        />
        <JobSection
          titulo='Requisitos'
          contenido={job.content.requirements}
        />
        <JobSection
          titulo='Acerca de la empresa'
          contenido={job.content.about}
        />
      </article>
    </main>
  )
}
