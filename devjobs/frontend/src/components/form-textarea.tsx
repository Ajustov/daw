import { Control, Controller, FieldValues, Path } from 'react-hook-form'
import { Field, FieldError, FieldLabel } from './ui/field'
import { Textarea } from './ui/textarea'
import { cn } from '@/lib/utils'

export function FormTextarea<TInput extends FieldValues, TOutput = TInput>({
  name,
  control,
  label,
  className,
  ...props
}: {
  name: Path<TInput>
  control: Control<
    TInput,
    any, // eslint-disable-line @typescript-eslint/no-explicit-any
    TOutput
  >
  label: string
} & React.ComponentProps<'textarea'>) {
  return (
    <Controller
      name={name}
      control={control}
      // field: value, onChange, onBlur, name, ref
      render={({ field, fieldState }) => {
        const isInvalid = fieldState.invalid
        return (
          <Field data-invalid={isInvalid}>
            <FieldLabel className='sr-only' htmlFor={field.name}>
              {label}
            </FieldLabel>
            <Textarea
              {...field}
              value={field.value ?? ''}
              placeholder={label}
              id={field.name}
              aria-invalid={isInvalid}
              className={cn(
                'max-h-40 resize-none overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden',
                className
              )}
              {...props}
            />
            {isInvalid && <FieldError errors={[fieldState.error]} />}
          </Field>
        )
      }}
    />
  )
}
