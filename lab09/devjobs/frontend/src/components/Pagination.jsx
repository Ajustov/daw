import styles from './Pagination.module.css'
export function Pagination ({ paginaActual = 1, nroPaginas = 5, cambiarPag }) {
  const paginas = Array.from({ length: nroPaginas }, (_, index) => index + 1)
  const aOpaco = { pointerEvents: 'none', opacity: 0.5 }

  const manejarPrevClick = (e) => {
    e.preventDefault()
    cambiarPag(paginaActual - 1)
  }
  const manejarNextClick = (e) => {
    e.preventDefault()
    cambiarPag(paginaActual + 1)
  }
  const urlPag = (paginaActual) => {
    const url = new URL(window.location)
    // Cambiamos los params
    url.searchParams.set('pagina', paginaActual)
    return `${url.pathname}?${url.searchParams.toString()}`
  }
  return (
    <nav className={styles.pagination}>
      <a
        href={urlPag(paginaActual - 1)}
        style={paginaActual === 1 ? aOpaco : {}}
        onClick={manejarPrevClick}
      >
        <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-left'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M15 6l-6 6l6 6' /></svg>
      </a>
      {paginas.map(pagina => (
        <a
          key={pagina}
          href={urlPag(pagina)}
          className={`pagination__number ${paginaActual === pagina ? styles.estasAqui : ''}`}
          onClick={(e) => {
            e.preventDefault()
            cambiarPag(pagina)
          }}
        >
          {pagina}
        </a>
      ))}
      <a
        href={urlPag(paginaActual + 1)}
        style={paginaActual === nroPaginas ? aOpaco : {}}
        onClick={manejarNextClick}
      >
        <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-right'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M9 6l6 6l-6 6' /></svg>
      </a>
    </nav>
  )
}
