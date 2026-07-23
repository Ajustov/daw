import { queryClient } from '@/lib/query-client'
import { userKeys } from '@/queries/user.queries'
import {
  deactivateUser,
  updateUser,
  updateUserPassword,
} from '@/services/user-service'
import { useAuthStore } from '@/store/auth-store'
import { useMutation } from '@tanstack/react-query'

export function useUpdateUser() {
  return useMutation({
    mutationFn: updateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.me })
    },
  })
}

export function useUpdateUserPassword() {
  return useMutation({
    mutationFn: updateUserPassword,
  })
}

export function useDeactivateUser() {
  const logout = useAuthStore(s => s.logout)
  return useMutation({
    mutationFn: deactivateUser,
    onSuccess: () => {
      logout()
    },
  })
}
