import { BASE_URL } from '@/lib/constants'
import { UserResponseMe, UserResponsePrivate } from '@/types/user'
import { HttpError } from './errors'
import { authFetch } from './dependencies'
import { UserUpdate, UserUpdatePassword } from '@/schemas/user'

const URL = `${BASE_URL}/api/users`

export async function getMeUser(): Promise<UserResponseMe> {
  const res = await authFetch(`${URL}/me`)
  if (!res.ok) throw new HttpError(res.status, 'Error al obtener al usuario')
  return res.json()
}

export async function updateUserPassword(
  passwords: UserUpdatePassword
): Promise<void> {
  const res = await authFetch(`${URL}/me/password`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(passwords),
  })
  if (!res.ok)
    throw new HttpError(res.status, 'Error al actualizar la contraseña')
}

export async function updateUser(
  user: UserUpdate
): Promise<UserResponsePrivate> {
  const res = await authFetch(`${URL}/me`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  })
  if (!res.ok) throw new HttpError(res.status, 'Error al actualizar al usuario')
  return res.json()
}

export async function deactivateUser(): Promise<void> {
  const res = await authFetch(`${URL}/me`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new HttpError(res.status, 'Error al desactivar al usuario')
}
