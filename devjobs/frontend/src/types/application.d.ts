import { CandidateResponsePublic } from './candidate'
import { Status } from './enums'
import { OfferResponseApplication } from './offer'

export interface ApplicationResponseRecruiter {
  id: string
  candidate: CandidateResponsePublic
  status: Status
  created: string
  modified: string
}

export interface ApplicationResponseCandidate {
  id: string
  offer: OfferResponseApplication
  status: Status
  created: string
  modified: string
}
