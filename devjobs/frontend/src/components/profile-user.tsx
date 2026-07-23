import { useDeactivateUser, useUpdateUser } from '@/mutations/user.mutations'
import { userOptions } from '@/queries/user.queries'
import { userUpdate, UserUpdate } from '@/schemas/user'
import { useAuthStore } from '@/store/auth-store'
import { zodResolver } from '@hookform/resolvers/zod'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { FormInput } from './form-input'
import { Button } from './ui/button'
import { ProfilePassword } from './profile-password'

export function ProfileUser() {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const { data, isError } = useQuery(userOptions(isAuthenticated))
  const values: UserUpdate = {
    username: data?.username ?? '',
    first_name: data?.first_name ?? '',
    last_name: data?.last_name ?? '',
    email: data?.email ?? '',
  }

  const { handleSubmit, control, formState } = useForm<UserUpdate>({
    resolver: zodResolver(userUpdate),
    values: values,
  })

  const { mutate: update, isPending: isUpdating } = useUpdateUser()
  const submit = (user: UserUpdate) => {
    update(user)
  }

  const { mutate: deactivate, isPending: isDeactivating } = useDeactivateUser()
  const handleDeactivate = () => {
    if (!confirm('¿Estás seguro de que quieres desactivar tu cuenta?')) return
    deactivate()
  }
  return (
    <article className='border-border flex min-h-130 max-w-100 min-w-50 flex-1 flex-col items-center justify-start gap-y-3 rounded-xl border p-4'>
      {isError ? (
        <p className='my-auto p-4'>Error al cargar el perfil usuario</p>
      ) : !data ? (
        <p className='my-auto p-4'>
          <Loader2 className='animate-spin' />
        </p>
      ) : (
        <>
          <form
            id='profile-user'
            className='flex w-full flex-col gap-y-3'
            onSubmit={handleSubmit(submit)}
          >
            <h1 className='text-3xl font-semibold'>User</h1>
            <FormInput name='username' control={control} label='Username' />
            <FormInput name='first_name' control={control} label='First name' />
            <FormInput name='last_name' control={control} label='Last name' />
            <FormInput name='email' control={control} label='Email' />
          </form>
          <ProfilePassword />
          <Button
            form='profile-user'
            size='lg'
            type='submit'
            disabled={isUpdating || !formState.isDirty}
            className='w-fit self-start'
          >
            {isUpdating ? <Loader2 className='animate-spin' /> : 'Guardar'}
          </Button>
          <Button
            className='w-fit self-start mt-auto'
            size='lg'
            variant='destructive'
            onClick={handleDeactivate}
          >
            {isDeactivating ? (
              <Loader2 className='animate-spin' />
            ) : (
              'Desactivar User'
            )}
          </Button>
        </>
      )}
    </article>
  )
}
