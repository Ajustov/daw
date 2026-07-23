import { useUpdateUserPassword } from '@/mutations/user.mutations'
import {
  userUpdatePasswordConfirm,
  UserUpdatePasswordConfirm,
} from '@/schemas/user'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm, useWatch } from 'react-hook-form'
import { FormInput } from './form-input'
import { Button } from './ui/button'
import { Loader2 } from 'lucide-react'

export function ProfilePassword() {
  const valuesUserPassword: UserUpdatePasswordConfirm = {
    current_password: '',
    new_password: '',
    confirm_password: '',
  }
  const { handleSubmit, control } = useForm<UserUpdatePasswordConfirm>({
    resolver: zodResolver(userUpdatePasswordConfirm),
    defaultValues: valuesUserPassword,
  })
  const { mutate, isPending } = useUpdateUserPassword()
  const submit = (passwords: UserUpdatePasswordConfirm) => {
    const { confirm_password, ...payload } = passwords
    mutate(payload)
  }
  const currentPassword = useWatch({ control, name: 'current_password' })
  const newPassword = useWatch({ control, name: 'new_password' })
  const confirmPassword = useWatch({ control, name: 'confirm_password' })
  return (
    <form
      className='flex w-full flex-col gap-y-3'
      onSubmit={handleSubmit(submit)}
    >
      <FormInput
        name='current_password'
        control={control}
        label='Current password'
        type='password'
        autoComplete='off'
      />
      <FormInput
        name='new_password'
        control={control}
        label='New password'
        type='password'
        autoComplete='off'
      />
      <FormInput
        name='confirm_password'
        control={control}
        label='Confirm new password'
        type='password'
        autoComplete='off'
      />
      {(currentPassword || newPassword || confirmPassword) && (
        <Button
          size='lg'
          type='submit'
          disabled={isPending}
          className='w-fit self-start'
        >
          {isPending ? <Loader2 className='animate-spin' /> : 'Change password'}
        </Button>
      )}
    </form>
  )
}
