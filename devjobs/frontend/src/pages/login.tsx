import { FormInput } from '@/components/form-input'
import { Button } from '@/components/ui/button'
import { ROUTES } from '@/lib/constants'
import { useLogin } from '@/mutations/auth.mutations'
import { login, Login } from '@/schemas/auth'
import { zodResolver } from '@hookform/resolvers/zod'
import { Loader2 } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { Link, useLocation, useNavigate } from 'react-router'

export function Login() {
  const values: Login = { username: '', password: '' }
  const { handleSubmit, control } = useForm<Login>({
    resolver: zodResolver(login),
    defaultValues: values,
  })
  const { mutate, isPending } = useLogin()
  const navigate = useNavigate()
  const location = useLocation()

  const submit = (credentials: Login) => {
    mutate(credentials, {
      onSuccess: () => {
        const state = location.state as string | null
        navigate(state ?? ROUTES.home, { replace: true })
      },
    })
  }
  return (
    <main className='flex h-screen w-full flex-col items-center justify-center'>
      <div className='flex min-h-57 w-full max-w-148 flex-col gap-y-4'>
        <h1 className='text-4xl font-semibold'>Iniciar sesión</h1>
        <form className='flex flex-col gap-y-3' onSubmit={handleSubmit(submit)}>
          <FormInput
            name='username'
            control={control}
            label='Username'
            className='h-12'
          />
          <FormInput
            name='password'
            control={control}
            label='Password'
            className='h-12'
            type='password'
            autoComplete='off'
          />
          <div className='flex items-center justify-end gap-x-6'>
            <Link to={ROUTES.register} className='font-medium underline'>
              Create a new account instead
            </Link>
            <Button size='lg' type='submit' disabled={isPending}>
              {isPending ? <Loader2 className='animate-spin' /> : 'Login'}
            </Button>
          </div>
        </form>
      </div>
    </main>
  )
}
