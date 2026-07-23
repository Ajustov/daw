import { FormInput } from '@/components/form-input'
import { Button } from '@/components/ui/button'
import { ROUTES } from '@/lib/constants'
import { useRegister } from '@/mutations/auth.mutations'
import { register, Register } from '@/schemas/auth'
import { zodResolver } from '@hookform/resolvers/zod'
import { Loader2 } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router'

export function Register() {
  const values: Register = {
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  }
  const { handleSubmit, control } = useForm<Register>({
    resolver: zodResolver(register),
    defaultValues: values,
  })
  const { mutate, isPending } = useRegister()
  const navigate = useNavigate()
  const submit = (user: Register) => {
    mutate(user, {
      onSuccess: () => {
        navigate(ROUTES.login)
      },
    })
  }
  return (
    <main className='flex h-screen w-full flex-col items-center justify-center'>
      <div className='flex min-h-57 w-full max-w-148 flex-col gap-y-4'>
        <h1 className='text-4xl font-semibold'>Regístrate</h1>
        <form className='flex flex-col gap-y-3' onSubmit={handleSubmit(submit)}>
          <FormInput
            name='username'
            control={control}
            label='Username'
            className='h-12'
          />
          <FormInput
            name='first_name'
            control={control}
            label='First name'
            className='h-12'
          />
          <FormInput
            name='last_name'
            control={control}
            label='Last name'
            className='h-12'
          />
          <FormInput
            name='email'
            control={control}
            label='Email'
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
            <Link to={ROUTES.login} className='font-medium underline'>
              Sign in with your account instead
            </Link>
            <Button size='lg' type='submit' disabled={isPending}>
              {isPending ? <Loader2 className='animate-spin' /> : 'Register'}
            </Button>
          </div>
        </form>
      </div>
    </main>
  )
}
