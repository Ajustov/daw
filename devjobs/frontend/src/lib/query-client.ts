import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60, // 1 minute, default: 0, tiempo en el que se considera fresco la data
      // gcTime: 1000 * 60 * 5, // 5 minutes, garbage collection, se reinicia el temporizador cada vez que no se usa
      retry: 0, // Intentos por si falla
      // refetchOnWindowFocus: true,
      // refetchOnReconnect: true,
    },
  },
})
