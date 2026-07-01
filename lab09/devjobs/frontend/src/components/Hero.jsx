import { useId } from 'react'
import styles from './Hero.module.css'

export function Hero ({ fnTextField, fnTecnologia, fnUbicacion, fnExperiencia, initialText }) {
  // Generar IDs únicos para accesibilidad
  const idSearch = useId()
  const idTecnologia = useId()
  const idUbicacion = useId()
  const idExperiencia = useId()

  // Manejadores, que llaman a las funciones pasadas coomo props
  const manejarInputText = (e) => {
    fnTextField(e.target.value)
  }
  const manejarTecnologia = (e) => {
    fnTecnologia(e.target.value)
  }
  const manejarUbicacion = (e) => {
    fnUbicacion(e.target.value)
  }
  const manejarExperiencia = (e) => {
    fnExperiencia(e.target.value)
  }
  return (
    <section className={styles.hero}>

      <header>
        <h1>Encuentra tu próximo trabajo</h1>
        <p>Explora miles de oportunidades en el sector tecnológico.</p>
      </header>

      <form role='search' aria-label='Buscar en el sitio'>
        <input
          name={idSearch} id='search' required type='text'
          placeholder='Buscar trabajos, empresas o habilidades' aria-label='Buscar'
          onChange={manejarInputText}
          defaultValue={initialText}
        />
        <button type='submit' aria-label='Enviar búsqueda'>
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-  outline icon-tabler-search'>
            <path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0' /><path d='M21 21l-6 -6' />
          </svg>
        </button>
      </form>

      <nav>

        <select
          name={idTecnologia}
          id='filter-technology'
          onChange={manejarTecnologia}
        >
          <option value=''>Tecnología</option>
          <option value='java'>Java</option>
          <option value='javascript'>JavaScript</option>
          <option value='spring boot'>Spring Boot</option>
          <option value='typescript'>TypeScript</option>
          <option value='python'>Python</option>
          <option value='angular'>Angular</option>
          <option value='docker'>Docker</option>
        </select>

        <select
          name={idUbicacion} id='filter-ubicacion'
          onChange={manejarUbicacion}
        >
          <option value=''>Ubicación</option>
          <option value='remoto'>Remoto</option>
          <option value='cdmx'>Ciudad de México</option>
          <option value='guadalajara'>Guadalajara</option>
          <option value='monterrey'>Monterrey</option>
          <option value='barcelona'>Barcelona</option>
        </select>

        <select
          name={idExperiencia} id='filter-experience'
          onChange={manejarExperiencia}
        >
          <option value=''>Nivel de experiencia</option>
          <option value='junior'>Junior</option>
          <option value='mid'>Semi Senior</option>
          <option value='senior'>Senior</option>
          <option value='lead'>Líder técnico</option>
        </select>
      </nav>
    </section>
  )
}
