import { queryClient } from '@/lib/query-client'
import { recruiterKeys } from '@/queries/recruiter.queries'
import { userKeys } from '@/queries/user.queries'
import {
  createRecruiter,
  deactivateRecruiter,
  updateRecruiter,
} from '@/services/recruiter-service'
import { useMutation } from '@tanstack/react-query'

export function useCreateRecruiter() {
  return useMutation({
    mutationFn: createRecruiter,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: recruiterKeys.me })
      queryClient.invalidateQueries({ queryKey: userKeys.me })
    },
  })
}

export function useUpdateRecruiter() {
  return useMutation({
    mutationFn: updateRecruiter,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: recruiterKeys.me })
    },
  })
}

export function useDeactivateRecruiter() {
  return useMutation({
    mutationFn: deactivateRecruiter,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: recruiterKeys.me })
      queryClient.invalidateQueries({ queryKey: userKeys.me })
    },
  })
}
