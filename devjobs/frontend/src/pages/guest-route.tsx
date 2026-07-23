import { ROUTES } from '@/lib/constants'
import { getAccessToken } from '@/lib/storage'
import { Navigate, Outlet } from 'react-router'

export function GuestRoute() {
  if (getAccessToken() !== null) return <Navigate to={ROUTES.home} replace />
  return <Outlet />
}
