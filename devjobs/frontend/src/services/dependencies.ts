import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  saveTokens,
} from '@/lib/storage'
import { HttpError } from './errors'
import { refreshReq } from './auth-service'
import { useAuthStore } from '@/store/auth-store'

let refreshInVuelo: Promise<string> | null = null
let isRedirecting = false

async function getNewAccessToken(refreshToken: string) {
  try {
    const { access, refresh } = await refreshReq(refreshToken)
    saveTokens(access, refresh)
    return access
  } catch {
    sessionExpirada()
  } finally {
    refreshInVuelo = null
  }
}
async function handleRefreshInVuelo(refreshToken: string) {
  if (refreshInVuelo) return refreshInVuelo
  refreshInVuelo = getNewAccessToken(refreshToken)
  return refreshInVuelo
}

function setAccessToken(
  options: RequestInit,
  accessToken: string | null
): RequestInit {
  if (!accessToken) return options
  return {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
    },
  }
}

// Esta fn nunca termina, no es void porque no sigue
function sessionExpirada(): never {
  if (!isRedirecting) {
    isRedirecting = true
    clearTokens()
    useAuthStore.getState().logout()
  }
  throw new HttpError(401, 'Sesión expirada')
}

export async function authFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const accessToken = getAccessToken()
  const response = await fetch(url, setAccessToken(options, accessToken))

  if (response.status !== 401) return response

  const refreshToken = getRefreshToken()
  if (!refreshToken) sessionExpirada()
  const access = await handleRefreshInVuelo(refreshToken)
  return fetch(url, setAccessToken(options, access))
}
