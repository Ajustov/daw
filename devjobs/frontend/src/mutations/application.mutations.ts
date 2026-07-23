import { queryClient } from '@/lib/query-client'
import { applicationKeys } from '@/queries/application.queries'
import { offerKeys } from '@/queries/offer.queries'
import { ApplicationUpdate } from '@/schemas/appplication'
import {
  createApplication,
  updateApplication,
} from '@/services/application-service'
import { useMutation } from '@tanstack/react-query'

export function useCreateApplication(id: string) {
  return useMutation({
    mutationFn: () => createApplication({ offer_id: id }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: applicationKeys.all })
      queryClient.invalidateQueries({ queryKey: offerKeys.detail(id) })
    },
  })
}

export function useUpdateApplication(applicationId: string, offerId: string) {
  return useMutation({
    mutationFn: (application: ApplicationUpdate) =>
      updateApplication(applicationId, application),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: offerKeys.applications(offerId),
      })
      queryClient.invalidateQueries({ queryKey: applicationKeys.all })
    },
  })
}
