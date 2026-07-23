import { Modality, Seniority } from './enums'
import { LocationResponseDetail, LocationResponseSummary } from './location'
import {
  RecruiterResponseApplication,
  RecruiterResponsePublic,
  RecruiterResponseSummary,
} from './recruiter'
import { TechnologyResponse } from './technology'

export interface Filters {
  title: string
  location_id: string | null
  modality: Modality | null
  technology_id: string | null
  seniority: Seniority | null
  limit: number | null
  offset: number | null
}

export interface OfferResponseSummary {
  id: string
  recruiter: RecruiterResponseSummary
  title: string
  description_summary: string
  location: LocationResponseSummary
  modality: Modality
  seniority: Seniority
  salary: number | null
  technologies: TechnologyResponse[]
}

export interface OfferResponseDetail {
  id: string
  recruiter: RecruiterResponsePublic
  title: string
  description_detail: string
  location: LocationResponseDetail
  modality: Modality
  seniority: Seniority
  salary: number | null
  technologies: TechnologyResponse[]
  created: string
  modified: string
}

export interface OfferResponseApplication {
  id: string
  recruiter: RecruiterResponseApplication
  title: string
  description_detail: string
  location: LocationResponseSummary
  modality: Modality
  seniority: Seniority
  salary: number | null
}

export interface OfferResponseRecruiter {
  id: string
  title: string
  location: LocationResponseSummary
  modality: Modality
  seniority: Seniority
  salary: Decimal | None
}
