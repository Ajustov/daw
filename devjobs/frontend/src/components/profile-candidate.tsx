import {
  useCreateCandidate,
  useDeactivateCandidate,
  useUpdateCandidate,
} from '@/mutations/candidate.mutations'
import { candidateOptions } from '@/queries/candidate.queries'
import { candidate, Candidate, CandidateInput } from '@/schemas/candidate'
import { useAuthStore } from '@/store/auth-store'
import { Seniority } from '@/types/enums'
import { zodResolver } from '@hookform/resolvers/zod'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { FormInput } from './form-input'
import { FormCombobox } from './form-combobox'
import { SENIORITY_OPTIONS } from '@/lib/constants'
import { FormTextarea } from './form-textarea'
import { Button } from './ui/button'
import { userOptions } from '@/queries/user.queries'

export function ProfileCandidate() {
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const {
    data: user,
    isLoading: isLoadingUser,
    isError: isErrorUser,
  } = useQuery(userOptions(isAuthenticated))
  const hasCandidate = isAuthenticated && !!user?.has_candidate
  const {
    data,
    isLoading: isLoadingCandidate,
    isError: isErrorCandidate,
  } = useQuery(candidateOptions(hasCandidate))

  const values: CandidateInput = {
    description: data?.description ?? '',
    seniority: data?.seniority ?? Seniority.TRAINEE,
    experience_years: data?.experience_years ?? '',
  }
  const { handleSubmit, control, formState } = useForm<
    CandidateInput,
    any, // eslint-disable-line @typescript-eslint/no-explicit-any
    Candidate
  >({
    resolver: zodResolver(candidate),
    values: values,
  })

  const { mutate: create, isPending: isCreating } = useCreateCandidate()
  const submitCreate = (candidate: Candidate) => {
    create(candidate)
  }

  const { mutate: update, isPending: isUpdating } = useUpdateCandidate()
  const submitUpdate = (candidate: Candidate) => {
    update(candidate)
  }

  const { mutate: deactivate, isPending: isDeactivating } =
    useDeactivateCandidate()
  const handleDeactivate = () => {
    if (
      !confirm(
        '¿Estás seguro de que quieres desactivar tu perfil de candidato?'
      )
    )
      return
    deactivate()
  }
  const isLoading = isLoadingUser || (hasCandidate && isLoadingCandidate)
  const isError = isErrorUser || (hasCandidate && isErrorCandidate)
  return (
    <article className='border-border flex min-h-130 max-w-100 min-w-50 flex-1 flex-col items-center justify-start gap-y-3 rounded-xl border p-4'>
      {isError ? (
        <p className='my-auto p-4'>Error al cargar el perfil candidato</p>
      ) : isLoading ? (
        <p className='my-auto p-4'>
          <Loader2 className='animate-spin' />
        </p>
      ) : (
        <>
          <form
            className='flex w-full flex-col gap-y-3'
            onSubmit={handleSubmit(!hasCandidate ? submitCreate : submitUpdate)}
          >
            <h1 className='text-3xl font-semibold'>Candidate</h1>
            <FormInput
              name='experience_years'
              control={control}
              type='number'
              label='Experience years'
              min={0}
              max={50}
            />
            <FormCombobox
              items={SENIORITY_OPTIONS}
              name='seniority'
              control={control}
              label='Seniority'
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
                isCreating || isUpdating || (hasCandidate && !formState.isDirty)
              }
            >
              {isCreating || isUpdating ? (
                <Loader2 className='animate-spin' />
              ) : !hasCandidate ? (
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
            disabled={!hasCandidate}
          >
            {isDeactivating ? (
              <Loader2 className='animate-spin' />
            ) : (
              'Desactivar Candidate'
            )}
          </Button>
        </>
      )}
    </article>
  )
}
