import { Navigate } from 'react-router'
import { useAuthStore } from '../store/authStore'

export function ProtectedRoute ({ children, redirectTo = '/login' }) {
  const { isLogueado } = useAuthStore()

  if (!isLogueado) {
    return <Navigate to={redirectTo} replace />
  }

  return children
}
