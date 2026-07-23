import { ROUTES } from '@/lib/constants'
import { userOptions } from '@/queries/user.queries'
import { useAuthStore } from '@/store/auth-store'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { Navigate, Outlet, useLocation } from 'react-router'

export function ProtectedRoute({
  profile,
}: {
  profile?: 'candidate' | 'recruiter'
}) {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const location = useLocation()
  const { data, isLoading, isError } = useQuery(userOptions(isAuthenticated))

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.login} state={location.pathname} replace />
  }

  if (isLoading) {
    return (
      <main className='flex w-full flex-1 items-center justify-center p-8'>
        <Loader2 className='animate-spin' />
      </main>
    )
  }

  if (isError || !data) {
    return null
  }
  if (profile) {
    const profileMap = {
      candidate: data.has_candidate,
      recruiter: data.has_recruiter,
    }

    if (!profileMap[profile]) {
      return <Navigate to={ROUTES.profile} />
    }

  }
  return <Outlet />
}
