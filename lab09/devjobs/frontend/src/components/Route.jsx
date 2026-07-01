import { useRouter } from '../hooks/useRouter'
export function Route ({ path, component: Component }) {
  // Custom hook para obtener el paht actual y comparar
  const { pathActual } = useRouter()

  if (pathActual !== path) return null

  return <Component />
}
