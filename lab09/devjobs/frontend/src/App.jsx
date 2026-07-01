import { Routes, Route } from 'react-router'
import { Header } from './components/Header.jsx'
import { Footer } from './components/Footer.jsx'
import { lazy } from 'react'
import { ProtectedRoute } from './components/ProtectedRoute.jsx'

const Home = lazy(() => import('./pages/Home.jsx'))
const Busqueda = lazy(() => import('./pages/Busqueda.jsx'))
const NotFoundPage = lazy(() => import('./pages/NotFoundPage.jsx'))
const Job = lazy(() => import('./pages/Job.jsx'))
const Perfil = lazy(() => import('./pages/Perfil.jsx'))

export default function App () {
  return (
    <>
      <Header />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/busqueda' element={<Busqueda />} />
        <Route path='/jobs/:id' element={<Job />} />
        <Route path='*' element={<NotFoundPage />} />
        <Route
          path='/perfil'
          element={
            <ProtectedRoute>
              <Perfil />
            </ProtectedRoute>
          }
        />
      </Routes>
      <Footer />
    </>
  )
}
