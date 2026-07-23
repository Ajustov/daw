import { login, register } from '@/services/auth-service'
import { useAuthStore } from '@/store/auth-store'
import { useMutation } from '@tanstack/react-query'

export function useLogin() {
  const setAuth = useAuthStore(s => s.login)
  return useMutation({
    mutationFn: login,
    onSuccess: res => {
      setAuth(res.access, res.refresh)
    },
  })
}

export function useRegister() {
  return useMutation({
    mutationFn: register
  })
}