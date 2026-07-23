import { BriefcaseBusiness, Building2, Search, Users } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useNavigate } from 'react-router'
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from '@/components/ui/input-group'
import { ROUTES } from '@/lib/constants'

export function Home() {
  const navigate = useNavigate()

  // currentTarget: burbujea
  // target: donde de verdad pasa
  const handleBusqueda = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget) // currentTarget por TS
    const busqueda = String(formData.get('busqueda')) // String porque no es un File
    const url = busqueda ? ROUTES.toOffersSearch(busqueda) : ROUTES.offers
    navigate(url)
  }

  return (
    <main className='flex w-full flex-1 flex-col gap-y-8 pb-8'>
      <section
        className={cn(
          'relative flex h-[55vh] flex-col items-center justify-center gap-y-9 p-8 after:absolute after:z-1',
          'after:inset-0', // Cubre todo el contenedor
          'after:bg-linear-to-b', // Degradado de arriba -> abajo
          'after:from-white/20 after:to-background',
          'dark:after:from-black/50 ',
          'after:content-[""]' // Content vacío para que renderice
        )}
      >
        <img
          src='/persona-trabajando.jpg'
          className={cn(
            'absolute top-0 left-0 z-0 h-full w-full',
            'object-cover' // Mantiene la proporción
          )}
          alt='persona-trabajando'
        />
        <h1 className='relative z-2 text-center text-6xl font-bold text-foreground'>
          Encuentra el trabajo de tus sueños
        </h1>
        <p className='relative z-2 max-w-200 text-center text-xl'>
          Únete a la comunidad más grande de desarrolladores y encuentra tu
          próxima oportunidad.
        </p>
        <form
          onSubmit={handleBusqueda}
          className='relative z-2 w-full max-w-187.5'
          role='search'
          aria-label='Buscar en el sitio'
        >
          <InputGroup className='bg-card'>
            <InputGroupInput
              name='busqueda'
              type='search'
              placeholder='Buscar empleos por título, habilidad o empresa'
              aria-label='Buscar'
              autoComplete='off'
            />
            <InputGroupAddon align='inline-end'>
              <InputGroupButton type='submit' aria-label='Enviar búsqueda'>
                <Search />
              </InputGroupButton>
            </InputGroupAddon>
          </InputGroup>
        </form>
      </section>
      <section className='flex min-h-[30vh] flex-col items-center justify-center gap-8 p-8'>
        <h2 className='text-4xl'>¿Por qué DevJobs?</h2>
        <p className='max-w-175 text-center text-xl'>
          DevJobs es la principal bolsa de trabajo para desarrolladores.
          Conectamos a los desarrolladores con las mejores empresas del mundo.
        </p>
        <div className='flex flex-wrap justify-center gap-6'>
          <article className='bg-card flex max-w-112.5 flex-col gap-4 rounded-xl p-8 text-center'>
            <BriefcaseBusiness className='mx-auto h-12 w-12' />
            <h3 className='text-xl font-bold'>Encuentra tu trabajo</h3>
            <p>
              Busca miles de empleos de las mejores empresas de todo el mundo
            </p>
          </article>
          <article className='bg-card flex max-w-112.5 flex-col gap-4 rounded-xl p-8 text-center'>
            <Users className='mx-auto h-12 w-12' />
            <h3 className='text-xl font-bold'>
              Conecta con las mejores empresas
            </h3>
            <p>
              Conecta con empresas que están contratando por tus habilidades
            </p>
          </article>
          <article className='bg-card flex max-w-112.5 flex-col gap-4 rounded-xl p-8 text-center'>
            <Building2 className='mx-auto h-12 w-12' />
            <h3 className='text-xl font-bold'>Obtén el salario que mereces</h3>
            <p>
              Obtén el salario que mereces con nuestra calculadora de salarios
            </p>
          </article>
        </div>
      </section>
    </main>
  )
}
