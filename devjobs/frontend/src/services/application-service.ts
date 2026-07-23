import { BASE_URL } from '@/lib/constants'
import { ApplicationCreate, ApplicationUpdate } from '@/schemas/appplication'
import {
  ApplicationResponseCandidate,
  ApplicationResponseRecruiter,
} from '@/types/application'
import { authFetch } from './dependencies'
import { HttpError } from './errors'

const URL = `${BASE_URL}/api/applications`

export async function getMeApplications(): Promise<
  ApplicationResponseCandidate[]
> {
  const res = await authFetch(`${URL}/me`)
  if (!res.ok)
    throw new HttpError(res.status, 'Error al obtener las applicaciones')
  return res.json()
}

export async function createApplication(
  application: ApplicationCreate
): Promise<ApplicationResponseCandidate> {
  const res = await authFetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(application),
  })
  if (!res.ok) throw new HttpError(res.status, 'Error al aplicar a la oferta')
  return res.json()
}

export async function updateApplication(
  id: string,
  application: ApplicationUpdate
): Promise<ApplicationResponseRecruiter> {
  const res = await authFetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(application),
  })
  if (!res.ok)
    throw new HttpError(res.status, 'Error al actualizar la application')
  return res.json()
}
