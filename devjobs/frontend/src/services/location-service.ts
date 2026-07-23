import { LocationResponseDetail } from '@/types/location'
import { HttpError } from './errors'
import { BASE_URL } from '@/lib/constants'

const URL = `${BASE_URL}/api/locations`

export async function getAllLocations(): Promise<LocationResponseDetail[]> {
  const res = await fetch(`${URL}`)
  if (!res.ok)
    throw new HttpError(res.status, 'Error al obtener las ubicaciones')
  return res.json()
}
