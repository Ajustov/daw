import { BASE_URL } from '@/lib/constants'
import { HttpError } from './errors'
import { RecruiterResponsePrivate } from '@/types/recruiter'
import { authFetch } from './dependencies'
import { Recruiter } from '@/schemas/recruiter'

const URL = `${BASE_URL}/api/recruiters`

export async function getMeRecruiter(): Promise<RecruiterResponsePrivate | null> {
  const res = await authFetch(`${URL}/me`)
  if (res.status === 403) return null // 403 cuando no tiene ese perfil
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener al recruiter')
  return res.json()
}

export async function createRecruiter(
  recruiter: Recruiter
): Promise<RecruiterResponsePrivate> {
  const res = await authFetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(recruiter),
  })
  if (!res.ok) throw new HttpError(res.status, 'Error al crear el reclutador')
  return res.json()
}

export async function updateRecruiter(
  recruiter: Recruiter
): Promise<RecruiterResponsePrivate> {
  const res = await authFetch(`${URL}/me`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(recruiter),
  })
  if (!res.ok)
    throw new HttpError(res.status, 'Error al actualizar al reclutador')
  return res.json()
}

export async function deactivateRecruiter(): Promise<void> {
  const res = await authFetch(`${URL}/me`, {
    method: 'DELETE',
  })
  if (!res.ok)
    throw new HttpError(res.status, 'Error al desactivar al reclutador')
}
