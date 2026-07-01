import { create } from 'zustand'
// Set es para actualizar la store desde dentro
export const useAuthStore = create((set) => ({
  isLogueado: false,
  login: () => set({ isLogueado: true }),
  logout: () => set({ isLogueado: false })
}))
