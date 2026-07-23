import { ROUTES, SALARY_STYLES } from '@/lib/constants'
import { OfferResponseRecruiter } from '@/types/offer'
import { Link } from 'react-router'
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from './ui/accordion'
import { useQuery } from '@tanstack/react-query'
import { offerApplicationsOptions } from '@/queries/offer.queries'
import { Loader2, SquarePen } from 'lucide-react'
import { ApplicationCard } from './application-card'
import { buttonVariants } from './ui/button'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/store/auth-store'
import { userOptions } from '@/queries/user.queries'

export function MyOfferCard({
  offer,
  isOpen,
}: {
  offer: OfferResponseRecruiter
  isOpen: boolean
}) {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const { data: user } = useQuery(userOptions(isAuthenticated))
  const hasRecruiter = isAuthenticated && !!user?.has_recruiter
  const { data: applications, isError } = useQuery(
    offerApplicationsOptions(offer.id, isOpen, hasRecruiter)
  )
  return (
    <AccordionItem
      value={offer.id}
      className='border-border flex flex-col gap-y-2 rounded-lg border p-1'
    >
      <AccordionTrigger className='focus-visible-ring-none flex p-0 hover:no-underline focus-visible:border-transparent'>
        <article className='bg-card text-card-foreground flex flex-1 justify-between gap-3 rounded-lg border-none p-4'>
          <div className='flex-warp flex flex-col justify-around'>
            <div className='flex items-center gap-x-2'>
              <Link
                to={ROUTES.toOfferDetail(offer.id)}
                className={cn(buttonVariants({ variant: 'link' }), 'p-0')}
                onClick={e => e.stopPropagation()}
              >
                <h3 className='text-lg font-semibold'>{offer.title}</h3>
              </Link>
              <Link
                to={ROUTES.toOfferMeDetail(offer.id)}
                className={cn(
                  buttonVariants({ variant: 'outline', size: 'icon-sm' })
                )}
                onClick={e => e.stopPropagation()}
              >
                <SquarePen />
              </Link>
            </div>
            <p className='text-muted-foreground flex flex-col text-sm capitalize'>
              <span>
                {offer.location.name} ({offer.modality})
              </span>
            </p>
          </div>
          <ul className='flex flex-row-reverse flex-wrap gap-x-1.5 gap-y-1 text-xs'>
            <li
              className={
                'self-center rounded-xl border px-2.5 py-1' + SALARY_STYLES
              }
            >
              S/{offer.salary}
            </li>
            <li className='bg-secondary text-secondary-foreground self-center rounded-xl px-2.5 py-1 capitalize'>
              {offer.seniority}
            </li>
          </ul>
        </article>
      </AccordionTrigger>
      <AccordionContent className='bg-card flex flex-col items-center rounded-lg p-2'>
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
              <ul className='flex w-full flex-1 flex-col gap-y-2'>
                {applications.map(application => (
                  <li key={application.id}>
                    <ApplicationCard
                      application={application}
                      idOffer={offer.id}
                    />
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </AccordionContent>
    </AccordionItem>
  )
}
