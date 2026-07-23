import { MyOfferCard } from '@/components/my-offer-card'
import { Accordion } from '@/components/ui/accordion'
import { Button } from '@/components/ui/button'
import { ROUTES } from '@/lib/constants'
import { offersMeOptions } from '@/queries/offer.queries'
import { userOptions } from '@/queries/user.queries'
import { useAuthStore } from '@/store/auth-store'
import { useQuery } from '@tanstack/react-query'
import { Loader2, Plus } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router'

export function MyOffers() {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const { data: user } = useQuery(userOptions(isAuthenticated))
  const hasRecruiter = isAuthenticated && !!user?.has_recruiter
  const { data: offers, isError } = useQuery(offersMeOptions(hasRecruiter))
  const [openIds, setOpenIds] = useState<string[]>([])
  return (
    <section className='flex w-full flex-1 justify-center p-8'>
      <div className='flex w-full max-w-150 min-w-120 flex-col items-center gap-y-3'>
        <h2 className='flex self-start text-4xl font-bold'>Tus ofertas</h2>
        <Link to={ROUTES.offersMeCreate} className='w-full'>
          <Button variant='outline' className='w-full'>
            <Plus />
          </Button>
        </Link>
        {isError ? (
          <p className='my-auto p-4'>Error al cargar las ofertas</p>
        ) : !offers ? (
          <p className='my-auto p-4'>
            <Loader2 className='animate-spin' />
          </p>
        ) : (
          <>
            {offers.length === 0 ? (
              <p className='my-auto p-4 text-center'>
                No se encontraron empleos
              </p>
            ) : (
              <Accordion
                multiple
                value={openIds}
                onValueChange={setOpenIds}
                className='gap-y-3'
              >
                {offers.map(offer => (
                  <MyOfferCard
                    key={offer.id}
                    offer={offer}
                    isOpen={openIds.includes(offer.id)}
                  />
                ))}
              </Accordion>
            )}
          </>
        )}
      </div>
    </section>
  )
}
