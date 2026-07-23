import { Control, Controller, FieldValues, Path } from 'react-hook-form'
import { Field, FieldError, FieldLabel } from './ui/field'
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from './ui/combobox'
import { Loader2 } from 'lucide-react';

export function FormCombobox<
  TInput extends FieldValues,
  TOutput = TInput,
  TValue extends string = string,
>({
  items,
  name,
  control,
  label,
  isLoading,
  isError,
}: {
  items: { label: string; value: TValue }[]
  name: Path<TInput>
  control: Control<
    TInput,
    any, // eslint-disable-line @typescript-eslint/no-explicit-any
    TOutput
  >
  label: string
  isLoading?: boolean
  isError?: boolean
}) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => {
        const isInvalid = fieldState.invalid
        const selected = items.find(opt => opt.value === field.value) ?? null
        return (
          <Field data-invalid={isInvalid}>
            <FieldLabel className='sr-only' htmlFor={field.name}>
              {label}
            </FieldLabel>
            <Combobox
              value={selected}
              onValueChange={item => field.onChange(item?.value ?? '')}
              items={items}
            >
              <ComboboxInput placeholder={label} showClear={true} />
              <ComboboxContent>
                <ComboboxEmpty>
                  {isLoading ? (
                    <Loader2 className='animate-spin' />
                  ) : isError ? (
                    'Error al cargar los elementos'
                  ) : (
                    'No se encontraron elementos'
                  )}
                </ComboboxEmpty>
                <ComboboxList>
                  {item => (
                    <ComboboxItem key={item.value} value={item}>
                      {item.label}
                    </ComboboxItem>
                  )}
                </ComboboxList>
              </ComboboxContent>
            </Combobox>
            {isInvalid && <FieldError errors={[fieldState.error]} />}
          </Field>
        )
      }}
    />
  )
}
