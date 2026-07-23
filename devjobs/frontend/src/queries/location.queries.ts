import { validateRetry } from '@/services/errors'
import { getAllLocations } from '@/services/location-service'
import { queryOptions } from '@tanstack/react-query'

export const locationKeys = {
  all: ['locations'] as const,
}

export function locationOptions() {
  return queryOptions({
    queryKey: locationKeys.all,
    queryFn: () => getAllLocations(),
    staleTime: Infinity,
    retry: validateRetry(1),
  })
}
