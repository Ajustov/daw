import z from 'zod'

export const userUpdatePassword = z.object({
  current_password: z.string().min(1),
  new_password: z
    .string()
    .min(8)
    // refine, una validación personalizada
    .refine(value => !/^\d+$/.test(value)),
})

export type UserUpdatePassword = z.output<typeof userUpdatePassword>

export const userUpdatePasswordConfirm = userUpdatePassword
  .extend({
    confirm_password: z
      .string()
      .min(8)
      // refine, una validación personalizada
      .refine(value => !/^\d+$/.test(value)),
  })
  .refine(data => data.new_password === data.confirm_password, {
    // Le especificamos a quien pertenece el error porque lo aplicamos a todo el objeto
    path: ['confirm_password'],
  })

export type UserUpdatePasswordConfirm = z.output<
  typeof userUpdatePasswordConfirm
>

export const userUpdate = z.object({
  username: z
    .string()
    .min(3)
    .max(150)
    .regex(/^[\w.@+-]+$/),
  first_name: z.string().min(2).max(150),
  last_name: z.string().min(2).max(150),
  email: z.email(),
})

export type UserUpdate = z.output<typeof userUpdate>
