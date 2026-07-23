import {
  Filters,
  OfferResponseDetail,
  OfferResponseRecruiter,
  OfferResponseSummary,
} from '@/types/offer'
import { HttpError } from './errors'
import { BASE_URL } from '@/lib/constants'
import { Offer } from '@/schemas/offer'
import { authFetch } from './dependencies'
import { ApplicationResponseRecruiter } from '@/types/application'

const URL = `${BASE_URL}/api/offers`

export async function getAllOffers({
  title,
  location_id,
  modality,
  technology_id,
  seniority,
  limit,
  offset,
}: Filters): Promise<{ items: OfferResponseSummary[]; count: number }> {
  const params = new URLSearchParams()
  if (title !== null) params.append('title', title)
  if (location_id !== null) params.append('location_id', location_id)
  if (modality !== null) params.append('modality', modality)
  if (technology_id !== null) params.append('technology_id', technology_id)
  if (seniority !== null) params.append('seniority', seniority)
  if (limit !== null) params.append('limit', String(limit))
  if (offset !== null) params.append('offset', String(offset))
  const res = await fetch(`${URL}?${params.toString()}`)
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener las ofertas')
  return res.json()
}

export async function getOffer(id: string): Promise<OfferResponseDetail> {
  const res = await fetch(`${URL}/${id}`)
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener la oferta')
  return res.json()
}

export async function getMeOffers(): Promise<OfferResponseRecruiter[]> {
  const res = await authFetch(`${URL}/me`)
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener las ofertas')
  return res.json()
}

export async function getApplications(
  id: string
): Promise<ApplicationResponseRecruiter[]> {
  const res = await authFetch(`${URL}/${id}/applications`)
  if (!res.ok)
    throw new HttpError(res.status, 'Error al obtener las applicaciones')
  return res.json()
}

export async function createOffer(offer: Offer): Promise<OfferResponseDetail> {
  const res = await authFetch(URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(offer),
  })
  if (!res.ok) throw new HttpError(res.status, 'Error al crear la oferta')
  return res.json()
}

export async function updateOffer(
  id: string,
  offer: Offer
): Promise<OfferResponseDetail> {
  const res = await authFetch(`${URL}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(offer),
  })
  if (!res.ok) throw new HttpError(res.status, 'Error al actualizar la oferta')
  return res.json()
}

export async function deactivateOffer(id: string): Promise<void> {
  const res = await authFetch(`${URL}/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new HttpError(res.status, 'Error al eliminar la oferta')
}
