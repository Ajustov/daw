import { UserResponsePrivate } from '@/types/user'
import { HttpError } from './errors'
import { Login, Register } from '@/schemas/auth'
import { LoginResponse, RefreshResponse } from '@/types/auth'
import { BASE_URL } from '@/lib/constants'

const URL = `${BASE_URL}/api/token`

export async function login(credentials: Login): Promise<LoginResponse> {
  const res = await fetch(`${URL}/pair`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  })
  if (!res.ok) {
    throw new HttpError(res.status, 'Credenciales de acceso incorrectas')
  }
  return res.json()
}
export async function register(user: Register): Promise<UserResponsePrivate> {
  const res = await fetch(`${BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  })
  if (res.status === 409) {
    throw new HttpError(409, 'El usuario ya existe')
  }
  if (!res.ok) {
    throw new HttpError(res.status, 'Error al registrar el usuario')
  }
  return res.json()
}

export async function refreshReq(refresh: string): Promise<RefreshResponse> {
  const res = await fetch(`${URL}/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })
  if (!res.ok) {
    throw new HttpError(res.status, 'No se pudo renovar la sesión activa')
  }
  return res.json()
}
