import { Seniority } from './enums'
import { UserResponseCandidate } from './user'

export interface CandidateResponsePrivate {
  description: str | null
  seniority: Seniority
  experience_years: number
}

export interface CandidateResponsePublic {
  user: UserResponseCandidate
  description: str | null
  seniority: Seniority
  experience_years: number
}
