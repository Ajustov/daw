import z from 'zod'

export const login = z.object({
  username: z
    .string()
    .min(3)
    .max(150)
    .regex(/^[\w.@+-]+$/),
  password: z.string().min(1),
})

export type Login = z.output<typeof login>

export const register = z.object({
  username: z
    .string()
    .min(3)
    .max(150)
    .regex(/^[\w.@+-]+$/),
  first_name: z.string().min(2).max(150),
  last_name: z.string().min(2).max(150),
  email: z.email(),
  password: z
    .string()
    .min(8)
    // refine, una validación personalizada
    .refine(value => !/^\d+$/.test(value)),
})

export type Register = z.output<typeof register>
