import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router'
import { useDebounce } from './useDebounce'
import { Modality, Seniority } from '@/types/enums'
import { setFilterParam } from '@/utils/filters'
import { FILTER_PARAMS, LIMIT } from '@/lib/constants'

export function useFilters() {
  const [searchParams, setSearchParams] = useSearchParams()
  const stringFilters = useMemo(
    () =>
      Object.fromEntries(
        FILTER_PARAMS.map(key => [key, searchParams.get(key) ?? null])
      ) as Record<
        (typeof FILTER_PARAMS)[number], //  "location_id" | "technology_id"
        string | null
      >,
    [searchParams]
  )
  const filters = {
    ...stringFilters,
    title: searchParams.get('title') ?? '',
    modality: (searchParams.get('modality') as Modality) ?? null,
    seniority: (searchParams.get('seniority') as Seniority) ?? null,
  }
  const setFilter = useMemo(
    () =>
      // fromEntries: Convierte [['a', 1], ['b', 2]] => { a: 1, b: 2 }
      Object.fromEntries(
        FILTER_PARAMS.map(param => [
          param,
          setFilterParam(param, setSearchParams),
        ])
      ) as Record<
        (typeof FILTER_PARAMS)[number], //  "location_id" | "technology_id"
        (value: string | null) => void
      >,
    [setSearchParams]
  )

  const setTitle = setFilterParam('title', setSearchParams)
  const setModality = setFilterParam<Modality>('modality', setSearchParams)
  const setSeniority = setFilterParam<Seniority>('seniority', setSearchParams)

  const [inputText, setInputText] = useState(() => filters.title)
  const debouncedSearch = useDebounce(inputText, 300)

  useEffect(() => {
    if (debouncedSearch !== filters.title) {
      setTitle(debouncedSearch)
    }
    //Incluir setTitle/setFilter aquí provoca una doble ejecución (aún memoizando) del efecto por cada búsqueda. Solo debouncedSearch debe disparar este efecto
  }, [debouncedSearch]) // eslint-disable-line react-hooks/exhaustive-deps

  // Number(null) = 0
  const pagina = Number(searchParams.get('pagina')) || 1

  const toPagina = (newPagina: number) => {
    // Es una copia porque al renderizar en pagination, tiene que saber el valor de antemano ejecutando asi el toPagina por cada calculo
    const params = new URLSearchParams(searchParams)
    params.set('pagina', String(newPagina))
    return `?${params.toString()}`
  }

  const offset = (pagina - 1) * LIMIT

  return {
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
  }
}
