import { Routes, Route } from 'react-router'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { OfferDetail } from './pages/offer-detail'
import { Login } from './pages/login'
import { Layout } from './pages/layout'
import { GuestRoute } from './pages/guest-route'
import { Register } from './pages/register'
import { queryClient } from './lib/query-client'
import { MyApplications } from './pages/my-applications'
import { ProtectedRoute } from './pages/protected-route'
import { Home } from './pages/home'
import { Offers } from './pages/offers'
import { Profile } from './pages/profile'
import { ROUTES } from './lib/constants'
import { MyOffers } from './pages/my-offers'
import { FormOffer } from './pages/form-offer'
import { NotFound } from './pages/not-found'

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Routes>
        <Route element={<Layout />}>
          <Route path={ROUTES.home} element={<Home />} />
          <Route path={ROUTES.offers} element={<Offers />} />
          <Route path={ROUTES.offerDetail} element={<OfferDetail />} />
          <Route element={<ProtectedRoute profile='candidate' />}>
            <Route path={ROUTES.applicationsMe} element={<MyApplications />} />
          </Route>
          <Route path={ROUTES.notFound} element={<NotFound />} />
          <Route element={<ProtectedRoute profile='recruiter' />}>
            <Route path={ROUTES.offersMe} element={<MyOffers />} />
            <Route path={ROUTES.offersMeDetail} element={<FormOffer />} />
            <Route path={ROUTES.offersMeCreate} element={<FormOffer />} />
          </Route>
          <Route element={<ProtectedRoute />}>
            <Route path={ROUTES.profile} element={<Profile />} />
          </Route>
        </Route>
        <Route element={<GuestRoute />}>
          <Route path={ROUTES.login} element={<Login />} />
          <Route path={ROUTES.register} element={<Register />} />
        </Route>
        <Route path='*' element={<NotFound />} />
      </Routes>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
