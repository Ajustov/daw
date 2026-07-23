import {
  useCreateRecruiter,
  useDeactivateRecruiter,
  useUpdateRecruiter,
} from '@/mutations/recruiter.mutations'
import { companyOptions } from '@/queries/company.queries'
import { recruiterOptions } from '@/queries/recruiter.queries'
import { recruiter, Recruiter } from '@/schemas/recruiter'
import { useAuthStore } from '@/store/auth-store'
import { zodResolver } from '@hookform/resolvers/zod'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { FormCombobox } from './form-combobox'
import { FormTextarea } from './form-textarea'
import { Button } from './ui/button'
import { FormInput } from './form-input'
import { userOptions } from '@/queries/user.queries'

export function ProfileRecruiter() {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const {
    data: user,
    isLoading: isLoadingUser,
    isError: isErrorUser,
  } = useQuery(userOptions(isAuthenticated))
  const hasRecruiter = isAuthenticated && !!user?.has_recruiter
  const {
    data,
    isLoading: isLoadingRecruiter,
    isError: isErrorRecruiter,
  } = useQuery(recruiterOptions(hasRecruiter))
  const companyResponse = useQuery(companyOptions())
  const itemsCompany =
    companyResponse.data?.map(c => ({ label: c.name, value: c.id })) ?? []
  const values: Recruiter = {
    company_id: data?.company_id ?? '',
    contact_email: data?.contact_email ?? '',
    description: data?.description ?? '',
  }
  const { handleSubmit, control, formState } = useForm<Recruiter>({
    resolver: zodResolver(recruiter),
    values: values,
  })

  const { mutate: create, isPending: isCreating } = useCreateRecruiter()
  const submitCreate = (recruiter: Recruiter) => {
    create(recruiter)
  }

  const { mutate: update, isPending: isUpdating } = useUpdateRecruiter()
  const submitUpdate = (recruiter: Recruiter) => {
    update(recruiter)
  }

  const { mutate: deactivate, isPending: isDeactivating } =
    useDeactivateRecruiter()
  const handleDeactivate = () => {
    if (
      !confirm(
        '¿Estás seguro de que quieres desactivar tu perfil de reclutador?'
      )
    )
      return
    deactivate()
  }
  const isLoading = isLoadingUser || (hasRecruiter && isLoadingRecruiter)
  const isError = isErrorUser || (hasRecruiter && isErrorRecruiter)
  return (
    <article className='border-border flex min-h-130 max-w-100 min-w-70 flex-1 flex-col items-center justify-start gap-y-3 rounded-xl border p-4'>
      {isError ? (
        <p className='my-auto p-4'>Error al cargar el perfil reclutador</p>
      ) : isLoading ? (
        <p className='my-auto p-4'>
          <Loader2 className='animate-spin' />
        </p>
      ) : (
        <>
          <form
            className='flex w-full flex-col gap-y-3'
            onSubmit={handleSubmit(!hasRecruiter ? submitCreate : submitUpdate)}
          >
            <h1 className='text-3xl font-semibold'>Recruiter</h1>
            <FormCombobox
              items={itemsCompany}
              name='company_id'
              control={control}
              label='Company'
              isLoading={companyResponse.isLoading}
              isError={companyResponse.isError}
            />
            <FormInput
              name='contact_email'
              control={control}
              label='Contact email'
              type='email'
            />
            <FormTextarea
              name='description'
              control={control}
              label='Description'
            />
            <Button
              type='submit'
              size='lg'
              className='w-fit self-start'
              disabled={
                isCreating || isUpdating || (hasRecruiter && !formState.isDirty)
              }
            >
              {isCreating || isUpdating ? (
                <Loader2 className='animate-spin' />
              ) : !hasRecruiter ? (
                'Crear perfil'
              ) : (
                'Guardar'
              )}
            </Button>
          </form>
          <Button
            className='mt-auto w-fit self-start'
            size='lg'
            variant='destructive'
            onClick={handleDeactivate}
            disabled={!hasRecruiter}
          >
            {isDeactivating ? (
              <Loader2 className='animate-spin' />
            ) : (
              'Desactivar Recruiter'
            )}
          </Button>
        </>
      )}
    </article>
  )
}
