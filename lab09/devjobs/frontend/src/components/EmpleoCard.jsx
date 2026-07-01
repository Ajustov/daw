import { useState } from 'react'
import styles from './EmpleoCard.module.css'
import { Link } from './Link'
import { useFavoritosStore } from '../store/favoritosStore'
import { useAuthStore } from '../store/authStore'

function EmpleoCardFavoritoBtn ({ id }) {
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

function EmpleoCardApplyBtn ({ id }) {
  const [clickeado, setClickeado] = useState(false)
  const { isLogueado } = useAuthStore()
  const manejarApply = () => {
    setClickeado(true)
  }
  return (
    <button
      className={clickeado ? styles.clickeado : ''}
      onClick={manejarApply}
      disabled={!isLogueado}
    >{clickeado ? 'Aplicado' : 'Aplicar'}
    </button>
  )
}
export function EmpleoCard ({ empleo }) {
  return (
    <article className={styles.empleoCard} data-id={empleo.id}>
      <div className={styles.empleo} data-nivel={empleo.data.nivel} data-tecnologia={empleo.data.technology.join(',')}>
        <div className={styles.empleoColumn1}>
          <header>
            <h3>
              <Link
                className={styles.titulo}
                href={`/jobs/${empleo.id}`}
              >
                {empleo.titulo}
              </Link>
            </h3>
            <p>
              {empleo.empresa} | <span data-lugar={empleo.data.ubicacion}>{empleo.ubicacion}</span>
            </p>
          </header>
          <p>{empleo.descripcion}</p>
        </div>
        <div className={styles.empleoColumn2}>
          <Link
            className={styles.detalles}
            href={`/jobs/${empleo.id}`}
          >
            Ver detalles
          </Link>
          <EmpleoCardApplyBtn id={empleo.id} />
          <EmpleoCardFavoritoBtn id={empleo.id} />
        </div>
      </div>
    </article>
  )
}
