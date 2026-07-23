import { Modality, Seniority, Status } from '@/types/enums'

export const BASE_URL = import.meta.env.VITE_API_URL || ''

export const LIMIT = 3

export const ROUTES = {
  home: '/',
  offers: '/offers',
  offerDetail: '/offers/:id',
  toOfferDetail: (id: string) => `/offers/${id}`,
  toOffersSearch: (title: string) =>
    `/offers?title=${encodeURIComponent(title)}`,
  applicationsMe: '/applications/me',
  profile: '/profile',
  login: '/login',
  register: '/register',
  offersMe: '/offers/me',
  offersMeCreate: '/offers/me/create',
  offersMeDetail: '/offers/me/:id',
  toOfferMeDetail: (id: string) => `/offers/me/${id}`,
  notFound: '/404',
} as const

export const SENIORITY_OPTIONS = [
  { label: 'Trainee', value: Seniority.TRAINEE },
  { label: 'Junior', value: Seniority.JUNIOR },
  { label: 'Mid', value: Seniority.MID },
  { label: 'Senior', value: Seniority.SENIOR },
  { label: 'Lead', value: Seniority.LEAD },
]

export const MODALITY_OPTIONS = [
  { label: 'Remoto', value: Modality.REMOTE },
  { label: 'Presencial', value: Modality.PRESENTIAL },
  { label: 'Híbrido', value: Modality.HYBRID },
]

export const STATUS_OPTIONS = [
  { label: 'Pendiente', value: Status.PENDING },
  { label: 'Revisado', value: Status.REVIEWED },
  { label: 'Rechazado', value: Status.REJECTED },
  { label: 'Contratado', value: Status.HIRED },
]

export const STATUS_STYLES: Record<Status, string> = {
  [Status.PENDING]:
    'border-amber-800/70 bg-amber-100 text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-400',
  [Status.REVIEWED]:
    'border-blue-800/70 bg-blue-100 text-blue-900 dark:border-blue-800 dark:bg-blue-950/40 dark:text-blue-400',
  [Status.REJECTED]:
    'border-red-800/70 bg-red-100 text-red-900 dark:border-red-800 dark:bg-red-950/40 dark:text-red-400',
  [Status.HIRED]:
    'border-green-800/70 bg-green-100 text-green-900 dark:border-green-800 dark:bg-green-950/40 dark:text-green-400',
}

export const SALARY_STYLES =
  'border-green-800/70 bg-green-100 text-green-900 dark:border-green-800 dark:bg-green-950/40 dark:text-green-400'

export const FILTER_PARAMS = ['location_id', 'technology_id'] as const
