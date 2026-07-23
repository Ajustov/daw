import z from 'zod'

export const recruiter = z.object({
  company_id: z.uuid(),
  contact_email: z.email(),
  description: z.string().max(500),
})

export type Recruiter = z.output<typeof recruiter>
