import { ProfileCandidate } from '@/components/profile-candidate'
import { ProfileRecruiter } from '@/components/profile-recruiter'
import { ProfileUser } from '@/components/profile-user'

export function Profile() {
  return (
    <main className='flex w-full flex-1 flex-col items-center gap-y-6 p-8'>
      <header className='flex min-h-30 items-center text-4xl font-bold'>
        <h2>Edita tu perfil</h2>
      </header>
      <div className='flex w-full flex-wrap items-start justify-center gap-6'>
        <ProfileUser />
        <ProfileCandidate />
        <ProfileRecruiter />
      </div>
    </main>
  )
}
