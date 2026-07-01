import { create } from 'zustand'

export const useFavoritosStore = create((set, get, store) => ({
  // Estado
  favoritos: [],

  // Acciones
  anadirFavorito: (id) => {
    set((state) => ({
      favoritos: state.favoritos.includes(id)
        ? state.favoritos
        : [...state.favoritos, id]
    }))
  },

  eliminarFavorito: (id) => {
    set((state) => ({
      // Filtramos los que tengan diferente id, eliminando asi los que si tengan
      favoritos: state.favoritos.filter((idInput) => idInput !== id)
    }))
  },

  isFavorito: (id) => get().favoritos.includes(id),

  alternarFavorito: (id) => {
    const { anadirFavorito, eliminarFavorito, isFavorito } = get()
    isFavorito(id) ? eliminarFavorito(id) : anadirFavorito(id)
  },

  contarFavoritos: () => get().favoritos.length,

  limpiarFavoritos: () => {
    set(store.getInitialState())
  }
}))
