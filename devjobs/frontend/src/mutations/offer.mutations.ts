import { queryClient } from '@/lib/query-client'
import { offerKeys } from '@/queries/offer.queries'
import { Offer } from '@/schemas/offer'
import {
  createOffer,
  deactivateOffer,
  updateOffer,
} from '@/services/offer-service'
import { useMutation } from '@tanstack/react-query'

export function useCreateOffer() {
  return useMutation({
    mutationFn: createOffer,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: offerKeys.me })
    },
  })
}

export function useUpdateOffer(id: string) {
  return useMutation({
    mutationFn: (offer: Offer) => updateOffer(id, offer),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: offerKeys.me })
      queryClient.invalidateQueries({ queryKey: offerKeys.detail(id) })
    },
  })
}

export function useDeactivateOffer(id: string) {
  return useMutation({
    mutationFn: () => deactivateOffer(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: offerKeys.me })
      queryClient.invalidateQueries({ queryKey: offerKeys.detail(id) })
    },
  })
}
