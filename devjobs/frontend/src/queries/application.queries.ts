import { getMeApplications } from '@/services/application-service'
import { validateRetry } from '@/services/errors'
import { queryOptions } from '@tanstack/react-query'

export const applicationKeys = {
  all: ['applications'] as const,
}

export function applicationsOptions(hasCandidate: boolean) {
  return queryOptions({
    queryKey: applicationKeys.all,
    queryFn: () => getMeApplications(),
    retry: validateRetry(2),
    enabled: hasCandidate,
  })
}
