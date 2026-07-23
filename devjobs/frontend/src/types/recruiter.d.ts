import { CompanyResponseSummary } from './company'
import { UserResponseRecruiter } from './user'

export interface RecruiterResponsePrivate {
  id: string
  company_id: string
  contact_email: string
  description: str | null
}

export interface RecruiterResponseSummary {
  company: CompanyResponseSummary
}

export interface RecruiterResponseApplication extends RecruiterResponseSummary {
  user: UserResponseRecruiter
}

export interface RecruiterResponsePublic extends RecruiterResponseSummary {
  id: string
  user: UserResponseRecruiter
  contact_email: string
}
