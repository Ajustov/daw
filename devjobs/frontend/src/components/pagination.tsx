import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Link } from 'react-router'

export function Pagination({
  pagina,
  toPagina,
  nroPaginas,
}: {
  pagina: number
  toPagina: (newPagina: number) => string
  nroPaginas: number
}) {
  const paginas = Array.from({ length: nroPaginas }, (_, i) => i + 1)
  return (
    <nav className='flex justify-center gap-2'>
      <Link
        to={toPagina(pagina - 1)}
        className={`text-foreground/70 hover:bg-accent flex size-10 items-center justify-center rounded-xl ${
          pagina === 1 ? 'pointer-events-none opacity-50' : ''
        }`}
      >
        <ChevronLeft />
      </Link>
      {paginas.map(pag => (
        <Link
          key={pag}
          to={toPagina(pag)}
          className={`flex size-10 items-center justify-center rounded-xl ${
            pagina === pag
              ? 'bg-primary text-primary-foreground pointer-events-none'
              : 'text-foreground/70 hover:bg-accent'
          }`}
        >
          {pag}
        </Link>
      ))}
      <Link
        to={toPagina(pagina + 1)}
        className={`text-foreground/70 hover:bg-accent flex size-10 items-center justify-center rounded-xl ${
          pagina === nroPaginas ? 'pointer-events-none opacity-50' : ''
        }`}
      >
        <ChevronRight />
      </Link>
    </nav>
  )
}
