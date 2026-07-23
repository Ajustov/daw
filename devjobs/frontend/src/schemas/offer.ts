import { Modality, Seniority } from '@/types/enums'
import z from 'zod'

export const offer = z.object({
  title: z.string().min(3).max(255),
  description_detail: z.string().min(10).max(2000),
  location_id: z.uuid(),
  modality: z.enum(Modality),
  seniority: z.enum(Seniority),
  salary: z
    .string()
    .transform(v => (v === '' ? undefined : Number(v)))
    .pipe(z.number().min(0)),
  technologies_ids: z.array(z.uuid()),
})

export type OfferInput = z.input<typeof offer>
export type Offer = z.output<typeof offer>
