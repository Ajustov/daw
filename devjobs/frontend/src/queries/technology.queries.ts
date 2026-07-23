import { validateRetry } from '@/services/errors'
import { getAllTechnologies } from '@/services/technology-service'
import { queryOptions } from '@tanstack/react-query'

export const technologyKeys = {
  all: ['technologies'] as const,
}

export function technologyOptions() {
  return queryOptions({
    queryKey: technologyKeys.all,
    queryFn: () => getAllTechnologies(),
    staleTime: Infinity,
    retry: validateRetry(1),
  })
}
