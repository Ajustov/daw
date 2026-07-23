import { Seniority } from '@/types/enums'
import z from 'zod'

export const candidate = z.object({
  description: z.string().max(500),
  seniority: z.enum(Seniority),
  experience_years: z.preprocess(
    v => (v === '' ? undefined : v),
    z.number().min(0).max(50)
  ),
})

export type CandidateInput = z.input<typeof candidate>
export type Candidate = z.output<typeof candidate>
