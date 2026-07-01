import { useLocation, useNavigate } from 'react-router'

export function useRouter () {
  const navigate = useNavigate()
  const location = useLocation()

  function navegarA (path) {
    navigate(path)
  }
  return {
    pathActual: location.pathname,
    navegarA
  }
}
