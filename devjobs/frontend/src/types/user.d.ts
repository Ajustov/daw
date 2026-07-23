export interface UserResponsePrivate {
  username: string
  first_name: string
  last_name: string
  email: string
}
export interface UserResponseMe extends UserResponsePrivate {
  date_joined: string
  has_candidate: boolean
  has_recruiter: boolean
}
export interface UserResponseRecruiter {
  first_name: string
}

export interface UserResponseCandidate extends UserResponseRecruiter {
  last_name: string
}
