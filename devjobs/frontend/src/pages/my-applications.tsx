import { MyApplicationCard } from '@/components/my-application-card'
import { applicationsOptions } from '@/queries/application.queries'
import { userOptions } from '@/queries/user.queries'
import { useAuthStore } from '@/store/auth-store'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'

export function MyApplications() {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const { data: user } = useQuery(userOptions(isAuthenticated))
  const hasCandidate = isAuthenticated && !!user?.has_candidate
  const { data: applications, isError } = useQuery(
    applicationsOptions(hasCandidate)
  )
  return (
    <section className='flex w-full flex-1 justify-center p-8'>
      <div className='flex w-full max-w-150 min-w-120 flex-col items-center gap-y-6'>
        <h2 className='flex self-start text-4xl font-bold'>
          Tus applicaciones
        </h2>
        {isError ? (
          <p className='my-auto p-4'>Error al cargar las applicaciones</p>
        ) : !applications ? (
          <p className='my-auto p-4'>
            <Loader2 className='animate-spin' />
          </p>
        ) : (
          <>
            {applications.length === 0 ? (
              <p className='my-auto p-4 text-center'>
                No se encontraron applicaciones
              </p>
            ) : (
              <ul className='flex w-full flex-1 flex-col gap-y-3'>
                {applications.map(application => (
                  <li key={application.id}>
                    <MyApplicationCard application={application} />
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </div>
    </section>
  )
}
