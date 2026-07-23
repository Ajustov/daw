import { TechnologyResponse } from '@/types/technology'
import { HttpError } from './errors'
import { BASE_URL } from '@/lib/constants'

const URL = `${BASE_URL}/api/technologies`

export async function getAllTechnologies(): Promise<TechnologyResponse[]> {
  const res = await fetch(`${URL}`)
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener las tecnologías')
  return res.json()
}
