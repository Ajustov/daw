import { Pagination } from '../components/Pagination.jsx'
import { Hero } from '../components/Hero.jsx'
import { ListaEmpleos } from '../components/ListaEmpleos.jsx'
import { useFilters } from '../hooks/useFilters.jsx'
export default function Busqueda () {
  const {
    empleos,
    loading,
    inputText,
    manejarInputText,
    manejarTecnologia,
    manejarUbicacion,
    manejarExperiencia,
    NUMERO_DE_PAGINAS,
    pagina,
    cambiarPag
  } = useFilters()
  return (
    <main>
      <Hero
        initialText={inputText}
        fnTextField={manejarInputText}
        fnTecnologia={manejarTecnologia}
        fnUbicacion={manejarUbicacion}
        fnExperiencia={manejarExperiencia}
      />
      <section className='empleoContainer'>
        <h2>Resultados de búsqueda</h2>
        {
          loading ? <p style={{ margin: 'auto', textAlign: 'center' }}>Cargando...</p> : <ListaEmpleos data={empleos} />
        }
        <Pagination nroPaginas={NUMERO_DE_PAGINAS} paginaActual={pagina} cambiarPag={cambiarPag} />
      </section>
    </main>
  )
}
