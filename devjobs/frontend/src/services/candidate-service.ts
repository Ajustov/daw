import { BASE_URL } from '@/lib/constants'
import { HttpError } from './errors'
import { CandidateResponsePrivate } from '@/types/candidate'
import { authFetch } from './dependencies'
import { Candidate } from '@/schemas/candidate'

const URL = `${BASE_URL}/api/candidates`

export async function getMeCandidate(): Promise<CandidateResponsePrivate | null> {
  const res = await authFetch(`${URL}/me`)
  if (res.status === 403) return null // 403 cuando no tiene ese perfil
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener al candidate')
  return res.json()
}

export async function createCandidate(
  candidate: Candidate
): Promise<CandidateResponsePrivate> {
  const res = await authFetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(candidate),
  })
  if (!res.ok) throw new HttpError(res.status, 'Error al crear el candidato')
  return res.json()
}

export async function updateCandidate(
  candidate: Candidate
): Promise<CandidateResponsePrivate> {
  const res = await authFetch(`${URL}/me`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(candidate),
  })
  if (!res.ok)
    throw new HttpError(res.status, 'Error al actualizar al candidato')
  return res.json()
}

export async function deactivateCandidate(): Promise<void> {
  const res = await authFetch(`${URL}/me`, {
    method: 'DELETE',
  })
  if (!res.ok)
    throw new HttpError(res.status, 'Error al desactivar al candidato')
}
