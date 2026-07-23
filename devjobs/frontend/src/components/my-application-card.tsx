import {
  ROUTES,
  SALARY_STYLES,
  STATUS_OPTIONS,
  STATUS_STYLES,
} from '@/lib/constants'
import { ApplicationResponseCandidate } from '@/types/application'
import { formatDate } from '@/utils/fecha'
import { Link } from 'react-router'

export function MyApplicationCard({
  application,
}: {
  application: ApplicationResponseCandidate
}) {
  return (
    <Link to={ROUTES.toOfferDetail(application.offer.id)}>
      <article className='bg-card text-card-foreground border-border flex justify-between rounded-xl border p-4'>
        <div className='flex-warp flex flex-col justify-between'>
          <header>
            <h3 className='text-lg font-semibold'>{application.offer.title}</h3>
            <p className='text-muted-foreground flex flex-col text-sm capitalize'>
              <span className='text-secondary-foreground'>
                {application.offer.recruiter.company.name}
              </span>
              <span>
                {application.offer.location.name} ({application.offer.modality})
              </span>
            </p>
          </header>
          <p className='text-secondary-foreground flex flex-col gap-x-2 text-sm'>
            <span>
              Reclutador: {application.offer.recruiter.user.first_name}
            </span>
            <span>Aplicaste el {formatDate(application.created)}</span>
          </p>
        </div>
        <div className='flex flex-col justify-between'>
          <ul className='flex justify-end gap-x-1.5 text-xs'>
            <li className='bg-secondary text-secondary-foreground self-center rounded-xl px-2.5 py-1 capitalize'>
              {application.offer.seniority}
            </li>
            <li
              className={
                'self-center rounded-xl border px-2.5 py-1 ' + SALARY_STYLES
              }
            >
              S/{application.offer.salary}
            </li>
          </ul>
          <div
            className={
              'flex items-center justify-center self-end rounded-xl border px-2.5 py-1 ' +
              STATUS_STYLES[application.status]
            }
          >
            {STATUS_OPTIONS.find(s => s.value === application.status)?.label}
          </div>
          <span className='text-secondary-foreground flex flex-col gap-x-2 text-sm'>
            Actualizado el {formatDate(application.modified)}
          </span>
        </div>
      </article>
    </Link>
  )
}
