import { useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router'

export function useFilters () {
  // Usamos useRef para la persistencia, donde la variable inicializada estará en 'current'
  const timeoutId = useRef(null)
  const [searchParams, setSearchParams] = useSearchParams()

  const [pagina, setPagina] = useState(() => {
    const urlPag = searchParams.get('pagina')
    return urlPag ? Number(urlPag) : 1
  })
  const cambiarPag = (page) => {
    setPagina(page)
  }
  // Es una fx para que se ejecute una vez
  const [inputText, setInputText] = useState(() => searchParams.get('text') || '')
  const manejarInputText = (e) => {
    if (timeoutId.current) {
      clearTimeout(timeoutId.current)
    }
    timeoutId.current = setTimeout(() => {
      setInputText(e)
    }, 500)
    setPagina(1)
  }

  const [filtroTecnologia, setFiltroTecnologia] = useState(() => searchParams.get('technology') || '')
  const manejarTecnologia = (e) => {
    setFiltroTecnologia(e)
    setPagina(1)
  }

  const [filtroUbicacion, setFiltroUbicacion] = useState(() => searchParams.get('type') || '')
  const manejarUbicacion = (e) => {
    setFiltroUbicacion(e)
    setPagina(1)
  }
  const [filtroExperiencia, setFiltroExperiencia] = useState(() => searchParams.get('level') || '')
  const manejarExperiencia = (e) => {
    setFiltroExperiencia(e)
    setPagina(1)
  }

  const EMPLEOS_POR_PAGINA = 3

  const [empleos, setEmpleos] = useState([])

  // El total de empleos encontrados
  const [total, setTotal] = useState(0)

  // Para informar al usuario si se está cargando la petición
  const [loading, setLoading] = useState(true)

  // useEffect es necesario para hacer fetching de datos
  useEffect(() => {
    async function fetchEmpleos () {
      try {
        // Cambiamos el valor de loading en true
        setLoading(true)

        // Los query params
        const params = new URLSearchParams()
        if (inputText) params.append('text', inputText)
        if (filtroTecnologia) params.append('technology', filtroTecnologia)
        if (filtroUbicacion) params.append('type', filtroUbicacion)
        if (filtroExperiencia) params.append('level', filtroExperiencia)

        // Simulando la paginación
        const offset = (pagina - 1) * EMPLEOS_POR_PAGINA
        params.append('limit', EMPLEOS_POR_PAGINA)
        params.append('offset', offset)

        // Guardando todos los filtros
        const queryParams = params.toString()
        const response = await fetch(`http://localhost:3000/trabajos?${queryParams}`)
        const json = await response.json()
        setEmpleos(json.data)
        setTotal(json.total)
      } catch (error) {
        console.error('Error fetching json:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchEmpleos()
  }, [inputText, filtroTecnologia, filtroUbicacion, filtroExperiencia, pagina])

  // useEffect
  useEffect(() => {
    setSearchParams((params) => {
      if (inputText) params.set('text', inputText)
      if (filtroTecnologia) params.set('technology', filtroTecnologia)
      if (filtroUbicacion) params.set('type', filtroUbicacion)
      if (filtroExperiencia) params.set('level', filtroExperiencia)
      if (pagina > 1) params.set('pagina', pagina)
      return params
    })
  }, [inputText, filtroTecnologia, filtroUbicacion, filtroExperiencia, pagina])

  // Para calcular el número de páginas, usando el total
  const NUMERO_DE_PAGINAS = Math.ceil(total / EMPLEOS_POR_PAGINA)

  return {
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
  }
}
