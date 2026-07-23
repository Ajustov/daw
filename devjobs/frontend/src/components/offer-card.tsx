import { Link } from 'react-router'
import type { OfferResponseSummary } from '../types/offer'
import { ROUTES, SALARY_STYLES } from '@/lib/constants'

export function OfferCard({ offer }: { offer: OfferResponseSummary }) {
  return (
    <Link to={ROUTES.toOfferDetail(offer.id)}>
      <article className='bg-card text-card-foreground border-border flex flex-col gap-3 rounded-xl border p-4'>
        <header className='flex flex-col gap-1'>
          <div className='flex-warp flex justify-between gap-x-2'>
            <h3 className='text-lg font-semibold'>{offer.title}</h3>
            <ul className='flex flex-row-reverse flex-wrap gap-x-1.5 gap-y-1 text-xs'>
              <li
                className={
                  'self-center rounded-xl border px-2.5 py-1 ' + SALARY_STYLES
                }
              >
                S/{offer.salary}
              </li>
              <li className='bg-secondary text-secondary-foreground self-center rounded-xl px-2.5 py-1 capitalize'>
                {offer.seniority}
              </li>
              {offer.technologies.map(tech => (
                <li
                  key={tech.id}
                  className='border-border text-foreground self-center rounded-xl border px-2.5 py-1'
                >
                  {tech.name}
                </li>
              ))}
            </ul>
          </div>
          <p className='text-muted-foreground flex flex-col text-sm capitalize'>
            <span className='text-secondary-foreground'>
              {offer.recruiter.company.name}
            </span>
            <span>
              {offer.location.name} ({offer.modality})
            </span>
          </p>
        </header>
        <p className='text-secondary-foreground line-clamp-2'>
          {offer.description_summary}
        </p>
      </article>
    </Link>
  )
}
