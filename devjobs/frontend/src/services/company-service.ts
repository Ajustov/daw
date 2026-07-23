import { BASE_URL } from '@/lib/constants'
import { HttpError } from './errors'
import { CompanyResponseDetail } from '@/types/company'

const URL = `${BASE_URL}/api/companies`

export async function getAllCompanies(): Promise<CompanyResponseDetail[]> {
  const res = await fetch(`${URL}`)
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener las compañias')
  return res.json()
}
