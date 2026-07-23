import { validateRetry } from '@/services/errors'
import { getMeRecruiter } from '@/services/recruiter-service'
import { queryOptions } from '@tanstack/react-query'

export const recruiterKeys = {
  me: ['recruiter', 'me'] as const,
}
export function recruiterOptions(hasRecruiter: boolean) {
  return queryOptions({
    queryKey: recruiterKeys.me,
    queryFn: () => getMeRecruiter(),
    staleTime: 1000 * 60 * 5,
    retry: validateRetry(2),
    enabled: hasRecruiter,
  })
}
