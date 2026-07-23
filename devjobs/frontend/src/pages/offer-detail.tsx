import { Button } from '@/components/ui/button'
import { ROUTES, SALARY_STYLES } from '@/lib/constants'
import { useCreateApplication } from '@/mutations/application.mutations'
import { applicationsOptions } from '@/queries/application.queries'
import { offerDetailOptions } from '@/queries/offer.queries'
import { userOptions } from '@/queries/user.queries'
import { useAuthStore } from '@/store/auth-store'
import { formatDate } from '@/utils/fecha'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { Link, useParams } from 'react-router'

export function OfferDetail() {
  const { id } = useParams()
  const { data: offerDetail, isError: isErrorOfferDetail } = useQuery(
    offerDetailOptions(id!)
  )
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const { data: user, isError: isErrorUser } = useQuery(
    userOptions(isAuthenticated)
  )
  const hasCandidate = isAuthenticated && !!user?.has_candidate
  const { data: applications } = useQuery(applicationsOptions(hasCandidate))
  const { mutate, isPending, isSuccess } = useCreateApplication(id!)
  const alreadyApplied =
    applications?.some(application => application.offer.id === id) ?? false
  return (
    <main className='flex max-w-230 min-w-100 flex-1 flex-col items-start gap-y-6 p-8'>
      {isErrorOfferDetail ? (
        <p className='my-auto p-4'>Error al cargar la oferta</p>
      ) : !offerDetail ? (
        <p className='my-auto p-4'>
          <Loader2 className='animate-spin' />
        </p>
      ) : (
        <>
          <header className='border-border flex w-full justify-between gap-x-4 border-b-2 pb-5'>
            <div className='flex flex-col gap-y-3'>
              <h2 className='text-4xl font-bold'>{offerDetail.title}</h2>
              <ul className='flex flex-wrap gap-2 capitalize'>
                <li
                  className={
                    'self-center rounded-xl border px-2.5 py-1 ' + SALARY_STYLES
                  }
                >
                  S/{offerDetail.salary}
                </li>
                <li className='bg-secondary text-secondary-foreground self-center rounded-xl px-2.5 py-1 capitalize'>
                  {offerDetail.seniority}
                </li>
                {offerDetail.technologies.map(tech => (
                  <li
                    key={tech.id}
                    className='border-border text-foreground self-center rounded-xl border px-2.5 py-1'
                  >
                    {tech.name}
                  </li>
                ))}
              </ul>
              <span className='text-muted-foreground'>
                {formatDate(offerDetail.created)}
              </span>
            </div>
            <div className='flex flex-col justify-around'>
              <p className='text-muted-foreground flex flex-col justify-center text-lg font-medium'>
                <span className='text-secondary-foreground'>
                  {offerDetail.recruiter.company.name}
                </span>
                <span>
                  {offerDetail.location.name} ({offerDetail.modality})
                </span>
              </p>
              {!isAuthenticated ? (
                <Link to={ROUTES.login} state={location.pathname}>
                  <Button>Aplicar</Button>
                </Link>
              ) : isErrorUser ? (
                <Button disabled>Aplicar</Button>
              ) : !user ? (
                <Button disabled>
                  <Loader2 className='animate-spin' />
                </Button>
              ) : !user.has_candidate ? (
                <Link to={ROUTES.profile}>
                  <Button>Completa tu perfil</Button>
                </Link>
              ) : alreadyApplied || isSuccess ? (
                <Button disabled>¡Aplicado!</Button>
              ) : (
                <Button onClick={() => mutate()} disabled={isPending}>
                  {isPending ? <Loader2 className='animate-spin' /> : 'Aplicar'}
                </Button>
              )}
            </div>
          </header>
          <p className='text-secondary-foreground border-border border-b-2 pb-6 text-lg w-full'>
            {offerDetail.description_detail}
          </p>
          <article className='text-secondary-foreground flex flex-col self-start'>
            <span>
              <strong>Reclutador: </strong>
              {offerDetail.recruiter.user.first_name}
            </span>
            <span>
              <strong>Email: </strong>
              {offerDetail.recruiter.contact_email}
            </span>
            <span>
              <strong>Ultima modificación: </strong>
              {formatDate(offerDetail.modified)}
            </span>
          </article>
        </>
      )}
    </main>
  )
}
