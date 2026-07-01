import { Link } from './Link'
import styles from './Header.module.css'
import { NavLink } from 'react-router'
import { useAuthStore } from '../store/authStore'
import { useFavoritosStore } from '../store/favoritosStore'

export function Header () {
  // Importamos desde el context
  const { isLogueado, login, logout } = useAuthStore()
  const { contarFavoritos, limpiarFavoritos } = useFavoritosStore()

  const manejarLogout = () => {
    logout()
    limpiarFavoritos()
  }
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <Link href='/'>
          <img src='/public/devjobs.png' alt='DevJobs logo' width='50' />
        </Link>
        <h1><Link href='/'>DevJobs</Link></h1>
      </div>
      <nav>
        <ul>
          <li>
            <NavLink
              className={({ isActive }) => isActive ? styles.isActive : ''}
              to='/busqueda'
            >
              Empleos
            </NavLink>
          </li>
          {
            isLogueado && (
              <li>
                <NavLink
                  to='/perfil'
                >
                  Favoritos {contarFavoritos()}
                </NavLink>
              </li>
            )
          }
          <li><a href='#empresas'>Empresas</a></li>
          <li><a href='#salarios'>Salarios</a></li>
        </ul>
      </nav>
      <div className={styles.actions}>
        <div>
          {/* <devjobs-avatar></devjobs-avatar> */}
        </div>
        {
          isLogueado
            ? <button onClick={manejarLogout}>Cerrar sesión</button>
            : <button onClick={login}>Iniciar sesión</button>
        }
      </div>
    </header>
  )
}
