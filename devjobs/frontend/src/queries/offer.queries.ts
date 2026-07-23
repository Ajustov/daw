import { validateRetry } from '@/services/errors'
import {
  getAllOffers,
  getApplications,
  getMeOffers,
  getOffer,
} from '@/services/offer-service'
import { Filters } from '@/types/offer'
import { queryOptions } from '@tanstack/react-query'

export const offerKeys = {
  all: ['offers'] as const,
  summary: (filters: Filters) => ['offers', 'summary', filters] as const,
  detail: (id: string) => ['offers', 'detail', id] as const,
  me: ['offers', 'me'] as const,
  applications: (id: string) =>
    ['offers', 'detail', id, 'applications'] as const,
}

export function offerSummaryOptions(filters: Filters) {
  return queryOptions({
    queryKey: offerKeys.summary(filters),
    queryFn: () => getAllOffers(filters),
    retry: validateRetry(2),
  })
}

export function offerDetailOptions(id: string) {
  return queryOptions({
    queryKey: offerKeys.detail(id),
    queryFn: () => getOffer(id),
    retry: validateRetry(2),
    enabled: !!id,
  })
}

export function offersMeOptions(hasRecruiter: boolean) {
  return queryOptions({
    queryKey: offerKeys.me,
    queryFn: getMeOffers,
    retry: validateRetry(2),
    enabled: hasRecruiter,
  })
}

export function offerApplicationsOptions(
  id: string,
  isOpen: boolean,
  hasRecruiter: boolean
) {
  return queryOptions({
    queryKey: offerKeys.applications(id),
    queryFn: () => getApplications(id),
    retry: validateRetry(2),
    enabled: isOpen && hasRecruiter,
  })
}
