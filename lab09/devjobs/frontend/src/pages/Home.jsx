import { useRouter } from '../hooks/useRouter'
import styles from './Home.module.css'

export default function Home () {
  const { navegarA } = useRouter()
  const manejarBusqueda = (e) => {
    // Evitamos que recargue la pág el form
    e.preventDefault()
    // Recuperamos los campos del form (nativo)
    const formData = new FormData(e.target)
    // Recuperamos el término del input con name 'search'
    const terminoDeBusqueda = formData.get('search')

    const url = terminoDeBusqueda
      ? `/busqueda?text=${encodeURIComponent(terminoDeBusqueda)}` // Para que codifique los espacios (%20)
      : '/busqueda'
    navegarA(url)
  }

  return (
    <main>
      <section className={styles.hero}>
        <img src='..\public\persona-trabajando.jpg' alt='persona-trabajando' />
        <h1>Encuentra el trabajo de tus sueños</h1>
        <p>Únete a la comunidad más grande de desarrolladores y encuentra tu próxima oportunidad.</p>
        <form onSubmit={manejarBusqueda} role='search' aria-label='Buscar en el sitio'>
          <input name='search' id='q' type='search' placeholder='Buscar empleos por título, habilidad o empresa' aria-label='Buscar' autoComplete='off' />
          <button type='submit' aria-label='Enviar búsqueda'>
            <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-  outline icon-tabler-search'>
              <path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0' /><path d='M21 21l-6 -6' />
            </svg>
          </button>
        </form>
      </section>
      <section className={styles.features}>
        <h2>¿Por qué DevJobs?</h2>
        <p>DevJobs es la principal bolsa de trabajo para desarrolladores. Conectamos a los desarrolladores con las mejores empresas del mundo.</p>
        <div className='features-cards'>
          <article>
            <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-briefcase'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M3 7m0 2a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v9a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2z' /><path d='M8 7v-2a2 2 0 0 1 2 -2h4a2 2 0 0 1 2 2v2' /><path d='M12 12l0 .01' /><path d='M3 13a20 20 0 0 0 18 0' /></svg>
            <h3 className='feature-card__title'>Encuentra el trabajo de tus sueños</h3>
            <p className='feature-card__text'>Busca miles de empleos de las mejores empresas de todo el mundo</p>
          </article>
          <article>
            <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-users'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0' /><path d='M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2' /><path d='M16 3.13a4 4 0 0 1 0 7.75' /><path d='M21 21v-2a4 4 0 0 0 -3 -3.85' /></svg>
            <h3 className='feature-card__title'>Conecta con las mejores empresas</h3>
            <p className='feature-card__text'>Conecta con empresas que están contratando por tus habilidades</p>
          </article>
          <article>
            <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-building-skyscraper'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M3 21l18 0' /><path d='M5 21v-14l8 -4v18' /><path d='M19 21v-10l-6 -4' /><path d='M9 9l0 .01' /><path d='M9 12l0 .01' /><path d='M9 15l0 .01' /><path d='M9 18l0 .01' /></svg>
            <h3 className='feature-card__title'>Obtén el salario que mereces</h3>
            <p className='feature-card__text'>Obtén el salario que mereces con nuestra calculadora de salarios</p>
          </article>
        </div>
      </section>
    </main>
  )
}
