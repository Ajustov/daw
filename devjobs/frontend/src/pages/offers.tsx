import { FilterCombobox } from '@/components/filter-combobox'
import { OfferCard } from '@/components/offer-card'
import { Pagination } from '@/components/pagination'

import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from '@/components/ui/input-group'

import { useFilters } from '@/hooks/useFilters'
import { LIMIT, MODALITY_OPTIONS, SENIORITY_OPTIONS } from '@/lib/constants'
import { locationOptions } from '@/queries/location.queries'
import { offerSummaryOptions } from '@/queries/offer.queries'
import { technologyOptions } from '@/queries/technology.queries'
import { useQuery } from '@tanstack/react-query'
import { Loader2, Search } from 'lucide-react'

export function Offers() {
  const {
    searchParams,
    inputText,
    setInputText,
    filters,
    setFilter,
    setModality,
    setSeniority,
    pagina,
    toPagina,
    offset,
  } = useFilters()
  const locationResponse = useQuery(locationOptions())
  const technologyResponse = useQuery(technologyOptions())
  const { data, isError } = useQuery(
    offerSummaryOptions({ ...filters, limit: LIMIT, offset: offset })
  )
  const itemsTechnology =
    technologyResponse.data?.map(t => ({ label: t.name, value: t.id })) ?? []
  const itemsLocation =
    locationResponse.data?.map(l => ({ label: l.name, value: l.id })) ?? []
  return (
    <main className='flex w-full flex-1 flex-col items-center gap-y-10 p-8'>
      <section className='flex min-h-70 w-full flex-col items-center justify-end gap-y-4'>
        <header className='flex max-w-200 min-w-0 flex-col gap-y-3 pb-8 text-center'>
          <h1 className='text-5xl font-bold'>Encuentra tu próximo trabajo</h1>
          <p className='text-lg'>
            Explora miles de oportunidades en el sector tecnológico.
          </p>
        </header>
        <form
          role='search'
          aria-label='Buscar en el sitio'
          className='w-full max-w-210 min-w-0'
        >
          <InputGroup>
            <InputGroupInput
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              type='search'
              placeholder='Buscar empleos por título, habilidad o empresa'
              aria-label='Buscar'
              autoComplete='off'
            />
            <InputGroupAddon>
              <Search />
            </InputGroupAddon>
          </InputGroup>
        </form>
        <nav className='flex flex-wrap gap-2'>
          <FilterCombobox
            currentValue={filters.location_id}
            placeholder='Ubicación'
            setFilterParam={setFilter.location_id}
            items={itemsLocation}
            isLoading={locationResponse.isLoading}
            isError={locationResponse.isError}
          />
          <FilterCombobox
            currentValue={filters.technology_id}
            placeholder='Tecnología'
            setFilterParam={setFilter.technology_id}
            items={itemsTechnology}
            isLoading={technologyResponse.isLoading}
            isError={technologyResponse.isError}
          />
          <FilterCombobox
            items={MODALITY_OPTIONS}
            currentValue={filters.modality}
            placeholder='Modalidad'
            setFilterParam={setModality}
          />
          <FilterCombobox
            items={SENIORITY_OPTIONS}
            currentValue={filters.seniority}
            placeholder='Seniority'
            setFilterParam={setSeniority}
          />
        </nav>
      </section>
      <section className='flex w-full max-w-230 min-w-0 flex-1 flex-col items-center gap-y-8'>
        {isError ? (
          <p className='my-auto p-4'>Error al cargar las ofertas</p>
        ) : !data ? (
          <p className='my-auto p-4'>
            <Loader2 className='animate-spin' />
          </p>
        ) : (
          <>
            {data.count === 0 ? (
              <p className='my-auto p-4 text-center'>
                No se encontraron empleos
              </p>
            ) : (
              <ul className='flex flex-1 w-full flex-col gap-y-3'>
                {data.items.map(offer => (
                  <li key={offer.id}>
                    <OfferCard offer={offer} />
                  </li>
                ))}
              </ul>
            )}
            <Pagination
              pagina={pagina}
              toPagina={toPagina}
              nroPaginas={Math.ceil(data.count / LIMIT)}
            />
          </>
        )}
      </section>
    </main>
  )
}
