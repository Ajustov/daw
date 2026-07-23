import { FormChipsCombobox } from '@/components/form-chips-combobox'
import { FormCombobox } from '@/components/form-combobox'
import { FormInput } from '@/components/form-input'
import { FormTextarea } from '@/components/form-textarea'
import { Button } from '@/components/ui/button'
import { MODALITY_OPTIONS, SENIORITY_OPTIONS } from '@/lib/constants'
import {
  useCreateOffer,
  useDeactivateOffer,
  useUpdateOffer,
} from '@/mutations/offer.mutations'
import { companyOptions } from '@/queries/company.queries'
import { locationOptions } from '@/queries/location.queries'
import { offerDetailOptions } from '@/queries/offer.queries'
import { recruiterOptions } from '@/queries/recruiter.queries'
import { technologyOptions } from '@/queries/technology.queries'
import { userOptions } from '@/queries/user.queries'
import { offer, Offer, OfferInput } from '@/schemas/offer'
import { useAuthStore } from '@/store/auth-store'
import { Modality, Seniority } from '@/types/enums'
import { formatDate } from '@/utils/fecha'
import { zodResolver } from '@hookform/resolvers/zod'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { Navigate, useParams } from 'react-router'

export function FormOffer() {
  const { id } = useParams()
  const isAuthenticated = useAuthStore(s => s.isAuthenticated)
  const {
    data: offerDetail,
    isLoading,
    isError,
  } = useQuery(offerDetailOptions(id!))
  const { data: user, isError: isErrorUser } = useQuery(
    userOptions(isAuthenticated)
  )
  const hasRecruiter = isAuthenticated && !!user?.has_recruiter
  const { data: recruiter, isError: isErrorRecruiter } = useQuery(
    recruiterOptions(hasRecruiter)
  )
  const { data: companies, isError: isErrorCompanies } =
    useQuery(companyOptions())

  const locationResponse = useQuery(locationOptions())
  const itemsLocation =
    locationResponse.data?.map(l => ({ label: l.name, value: l.id })) ?? []

  const values: OfferInput = {
    title: offerDetail?.title ?? '',
    description_detail: offerDetail?.description_detail ?? '',
    location_id: offerDetail?.location?.id ?? '',
    modality: offerDetail?.modality ?? Modality.PRESENTIAL,
    seniority: offerDetail?.seniority ?? Seniority.JUNIOR,
    technologies_ids: offerDetail?.technologies.map(t => t.id) ?? [],
    salary: offerDetail?.salary?.toString() ?? '',
  }
  const { handleSubmit, control, formState } = useForm<
    OfferInput,
    any, // eslint-disable-line @typescript-eslint/no-explicit-any
    Offer
  >({
    resolver: zodResolver(offer),
    values: values,
  })

  const { mutate: create, isPending: isCreating, isSuccess } = useCreateOffer()
  const submitCreate = (offer: Offer) => {
    create(offer)
  }
  const { mutate: update, isPending: isUpdating } = useUpdateOffer(id!)
  const submitUpdate = (offer: Offer) => {
    update(offer)
  }
  const { mutate: deactivate, isPending: isDeactivating } = useDeactivateOffer(
    id!
  )
  const handleDeactivate = () => {
    if (!confirm('¿Estás seguro de que quieres desactivar la oferta?')) return
    deactivate()
  }
  const technologyResponse = useQuery(technologyOptions())
  const itemsTechnology =
    technologyResponse.data?.map(t => ({ label: t.name, value: t.id })) ?? []

  if (
    id &&
    offerDetail &&
    recruiter &&
    offerDetail.recruiter.id !== recruiter.id
  ) {
    return <Navigate to='/404' replace />
  }
  return (
    <main className='flex max-w-230 min-w-100 flex-1 flex-col items-start p-8'>
      {isError ? (
        <p className='my-auto p-4'>Error al cargar la oferta</p>
      ) : !id && isLoading ? (
        <p className='my-auto p-4'>
          <Loader2 className='animate-spin' />
        </p>
      ) : (
        <form
          className='flex flex-col gap-y-6'
          onSubmit={handleSubmit(!id ? submitCreate : submitUpdate)}
        >
          <header className='flex w-full justify-between gap-x-4'>
            <div className='flex flex-col gap-y-3'>
              <FormInput name='title' control={control} label='Title' />
              <ul className='flex flex-wrap gap-2'>
                <li>
                  <FormInput
                    name='salary'
                    control={control}
                    type='decimal'
                    label='Salary'
                  />
                </li>
                <li>
                  <FormCombobox
                    items={SENIORITY_OPTIONS}
                    name='seniority'
                    control={control}
                    label='Seniority'
                  />
                </li>
                <FormChipsCombobox
                  name='technologies_ids'
                  control={control}
                  label='Technologies'
                  items={itemsTechnology}
                  isLoading={technologyResponse.isLoading}
                  isError={technologyResponse.isError}
                />
              </ul>
              <span className='text-muted-foreground'>
                {formatDate(offerDetail?.created ?? new Date().toISOString())}
              </span>
            </div>
            <div className='flex flex-col justify-center gap-y-2'>
              {offerDetail ? (
                <span className='text-muted-foreground text-lg font-medium'>
                  {offerDetail.recruiter.company.name}
                </span>
              ) : isErrorRecruiter || isErrorCompanies ? (
                <span className='text-muted-foreground text-lg font-medium'>
                  Error al cargar la empresa
                </span>
              ) : !companies || !recruiter ? (
                <Loader2 className='animate-spin' />
              ) : (
                <span className='text-muted-foreground text-lg font-medium'>
                  {companies.find(c => c.id === recruiter.company_id)?.name ??
                    'Empresa no encontrada'}
                </span>
              )}
              <FormCombobox
                items={itemsLocation}
                name='location_id'
                control={control}
                label='Location'
                isLoading={locationResponse.isLoading}
                isError={locationResponse.isError}
              />
              <FormCombobox
                items={MODALITY_OPTIONS}
                name='modality'
                control={control}
                label='Modality'
              />
            </div>
          </header>
          <FormTextarea
            name='description_detail'
            control={control}
            label='Description'
            className='max-h-100'
          />
          <article className='text-secondary-foreground flex flex-col'>
            <span>
              <strong>Reclutador: </strong>
              {offerDetail ? (
                <span>{offerDetail.recruiter.user.first_name}</span>
              ) : isErrorUser ? (
                <span>Error al cargar el usuario</span>
              ) : !user ? (
                <Loader2 className='animate-spin' />
              ) : (
                <span>{user.first_name}</span>
              )}
            </span>
            <span>
              <strong>Email: </strong>
              {offerDetail ? (
                <span>{offerDetail.recruiter.contact_email}</span>
              ) : isErrorRecruiter ? (
                <span>Error al cargar el email</span>
              ) : !recruiter ? (
                <Loader2 className='animate-spin' />
              ) : (
                <span>{recruiter.contact_email}</span>
              )}
            </span>
            <span>
              <strong>Ultima modificación: </strong>
              {formatDate(offerDetail?.modified ?? new Date().toISOString())}
            </span>
          </article>
          <Button
            type='submit'
            size='lg'
            className='w-fit self-start'
            disabled={
              isCreating ||
              isUpdating ||
              isSuccess ||
              (!!id && !formState.isDirty)
            }
          >
            {isCreating || isUpdating ? (
              <Loader2 className='animate-spin' />
            ) : !id ? (
              isSuccess ? (
                'Oferta creada'
              ) : (
                'Crear oferta'
              )
            ) : (
              'Guardar'
            )}
          </Button>
        </form>
      )}
      <Button
        className='mt-auto w-fit self-start'
        size='lg'
        variant='destructive'
        onClick={handleDeactivate}
      >
        {isDeactivating ? (
          <Loader2 className='animate-spin' />
        ) : (
          'Desactivar Oferta'
        )}
      </Button>
    </main>
  )
}
