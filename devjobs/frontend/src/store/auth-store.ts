import { create } from 'zustand'
import { getAccessToken, saveTokens, clearTokens } from '@/lib/storage'

interface AuthState {
  isAuthenticated: boolean
  login: (access: string, refresh: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(set => ({
  isAuthenticated: getAccessToken() !== null,
  login: (access, refresh) => {
    saveTokens(access, refresh)
    set({ isAuthenticated: true })
  },

  logout: () => {
    clearTokens()
    window.location.href = '/'
  },
}))
