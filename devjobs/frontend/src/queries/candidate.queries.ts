import { getMeCandidate } from '@/services/candidate-service'
import { validateRetry } from '@/services/errors'
import { queryOptions } from '@tanstack/react-query'

export const candidateKeys = {
  me: ['candidate', 'me'] as const,
}
export function candidateOptions(hasCandidate: boolean) {
  return queryOptions({
    queryKey: candidateKeys.me,
    queryFn: () => getMeCandidate(),
    staleTime: 1000 * 60 * 5,
    retry: validateRetry(2),
    enabled: hasCandidate,
  })
}
