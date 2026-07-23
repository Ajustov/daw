import { Control, Controller, FieldValues, Path } from 'react-hook-form'
import { Field, FieldError, FieldLabel } from './ui/field'
import { Input } from './ui/input'

export function FormInput<TInput extends FieldValues, TOutput = TInput>({
  name,
  control,
  label,
  type,
  ...props
}: {
  name: Path<TInput>
  control: Control<
    TInput,
    any, // eslint-disable-line @typescript-eslint/no-explicit-any
    TOutput
  >
  label: string
} & React.ComponentProps<'input'>) {
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
            <Input
              {...field}
              value={field.value ?? ''}
              onChange={e => {
                if (type === 'number') {
                  const value = e.target.value
                  field.onChange(value === '' ? '' : Number(value))
                } else if (type === 'decimal') {
                  const value = e.target.value.replace(',', '.')
                  if (/^\d*\.?\d{0,2}$/.test(value) || value === '') {
                    field.onChange(value)
                  }
                } else {
                  field.onChange(e)
                }
              }}
              type={type}
              placeholder={label}
              aria-invalid={isInvalid}
              id={field.name}
              {...props}
            />
            {isInvalid && <FieldError errors={[fieldState.error]} />}
          </Field>
        )
      }}
    />
  )
}
