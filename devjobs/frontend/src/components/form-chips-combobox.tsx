import { Control, Controller, FieldValues, Path } from 'react-hook-form'
import { Field, FieldError, FieldLabel } from './ui/field'
import {
  Combobox,
  ComboboxChip,
  ComboboxChips,
  ComboboxChipsInput,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxItem,
  ComboboxList,
  ComboboxValue,
} from './ui/combobox'
import { Loader2 } from 'lucide-react'

export function FormChipsCombobox<
  TInput extends FieldValues,
  TOutput = TInput,
>({
  name,
  control,
  label,
  items,
  isLoading,
  isError,
}: {
  name: Path<TInput>
  control: Control<
    TInput,
    any, // eslint-disable-line @typescript-eslint/no-explicit-any
    TOutput
  >
  label: string
  items: { label: string; value: string }[]
  isLoading?: boolean
  isError?: boolean
}) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => {
        const isInvalid = fieldState.invalid
        const selectedValues: string[] = field.value ?? []
        const selectedItems = items.filter(i =>
          selectedValues.includes(i.value)
        )
        return (
          <Field data-invalid={isInvalid} className='w-fit'>
            <FieldLabel className='sr-only' htmlFor={field.name}>
              {label}
            </FieldLabel>
            <Combobox
              multiple
              items={items}
              value={selectedItems}
              onValueChange={newItems =>
                field.onChange(newItems.map(i => i.value))
              }
            >
              <ComboboxChips>
                <ComboboxValue>
                  {(values: typeof items) => (
                    <>
                      {values.map(v => (
                        <ComboboxChip key={v.value}>{v.label}</ComboboxChip>
                      ))}
                      <ComboboxChipsInput />
                    </>
                  )}
                </ComboboxValue>
              </ComboboxChips>
              <ComboboxContent>
                <ComboboxEmpty>
                  {isLoading ? (
                    <Loader2 className='animate-spin' />
                  ) : isError ? (
                    'Error al cargar'
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
