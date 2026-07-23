import { validateRetry } from '@/services/errors'
import { getMeUser } from '@/services/user-service'
import { queryOptions } from '@tanstack/react-query'

export const userKeys = {
  me: ['user', 'me'] as const,
}
export function userOptions (isAuthenticated: boolean) {
  return queryOptions({
    queryKey: userKeys.me,
    queryFn: () => getMeUser(),
    staleTime: 1000 * 60 * 5,
    retry: validateRetry(2),
    enabled: isAuthenticated,
  })
}
