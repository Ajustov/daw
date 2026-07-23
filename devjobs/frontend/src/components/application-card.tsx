import { ApplicationResponseRecruiter } from '@/types/application'
import { formatDate } from '@/utils/fecha'
import { FormCombobox } from './form-combobox'
import { STATUS_OPTIONS } from '@/lib/constants'
import { useForm } from 'react-hook-form'
import { applicationUpdate, ApplicationUpdate } from '@/schemas/appplication'
import { zodResolver } from '@hookform/resolvers/zod'
import { Button } from './ui/button'
import { Check, Loader2 } from 'lucide-react'
import { useUpdateApplication } from '@/mutations/application.mutations'

export function ApplicationCard({
  application,
  idOffer,
}: {
  application: ApplicationResponseRecruiter
  idOffer: string
}) {
  const values: ApplicationUpdate = {
    status: application.status,
  }
  const { handleSubmit, control, formState } = useForm<ApplicationUpdate>({
    resolver: zodResolver(applicationUpdate),
    values: values,
  })
  const { mutate: update, isPending: isUpdating } = useUpdateApplication(
    application.id,
    idOffer
  )
  const submit = (application: ApplicationUpdate) => {
    update(application)
  }
  return (
    <article className='bg-secondary text-card-foreground border-border flex justify-between gap-x-6 rounded-lg border p-4 text-sm'>
      <div className='flex-warp flex flex-col gap-y-1'>
        <h3 className='text-base font-semibold'>
          {application.candidate.user.first_name}{' '}
          {application.candidate.user.last_name}
        </h3>
        <ul className='flex justify-end gap-x-1.5 text-xs'>
          <li className='bg-card text-secondary-foreground self-center rounded-xl px-2.5 py-1'>
            {application.candidate.experience_years} año(s) de experiencia
          </li>
          <li className='bg-card text-secondary-foreground self-center rounded-xl px-2.5 py-1 capitalize'>
            {application.candidate.seniority}
          </li>
        </ul>
        <span className='text-secondary-foreground'>
          Aplicó el {formatDate(application.created)}
        </span>
      </div>
      <div className='flex flex-col justify-around gap-y-2'>
        <form
          className='flex items-center gap-x-2'
          onSubmit={handleSubmit(submit)}
        >
          <FormCombobox
            items={STATUS_OPTIONS}
            name='status'
            control={control}
            label='Status'
          />
          <Button
            size='icon-lg'
            variant='outline'
            type='submit'
            disabled={isUpdating || !formState.isDirty}
          >
            {isUpdating ? <Loader2 className='animate-spin' /> : <Check />}
          </Button>
        </form>
        <span className='text-secondary-foreground self-end'>
          Tu última actualización fue el {formatDate(application.modified)}
        </span>
      </div>
    </article>
  )
}
