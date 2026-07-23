import { queryClient } from '@/lib/query-client'
import { candidateKeys } from '@/queries/candidate.queries'
import { userKeys } from '@/queries/user.queries'
import {
  createCandidate,
  deactivateCandidate,
  updateCandidate,
} from '@/services/candidate-service'
import { useMutation } from '@tanstack/react-query'

export function useCreateCandidate() {
  return useMutation({
    mutationFn: createCandidate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: candidateKeys.me })
      queryClient.invalidateQueries({ queryKey: userKeys.me })
    },
  })
}

export function useUpdateCandidate() {
  return useMutation({
    mutationFn: updateCandidate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: candidateKeys.me })
    },
  })
}

export function useDeactivateCandidate() {
  return useMutation({
    mutationFn: deactivateCandidate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: candidateKeys.me })
      queryClient.invalidateQueries({ queryKey: userKeys.me })
    },
  })
}
