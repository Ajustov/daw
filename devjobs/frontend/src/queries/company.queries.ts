import { getAllCompanies } from '@/services/company-service'
import { validateRetry } from '@/services/errors'
import { queryOptions } from '@tanstack/react-query'

export const companyKeys = {
  all: ['companies'] as const,
}

export function companyOptions() {
  return queryOptions({
    queryKey: companyKeys.all,
    queryFn: () => getAllCompanies(),
    staleTime: Infinity,
    retry: validateRetry(1),
  })
}
