import { Header } from '@/components/header'
import { Outlet } from 'react-router'

export function Layout() {
  // Outlet: Si hay un hijo route lo renderiza
  return (
    <div className='flex h-screen flex-col'>
      <Header />
      <div className='flex flex-1 flex-col items-center overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden'>
        <Outlet />
        <footer className='border-input w-full border-t p-4 text-center'>
          <p>&copy; 2026 DevJobs. Todos los derechos reservados.</p>
        </footer>
      </div>
    </div>
  )
}
