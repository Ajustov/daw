import { Loader2 } from 'lucide-react'
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from './ui/combobox'

export function FilterCombobox<T extends string>({
  currentValue,
  placeholder,
  setFilterParam,
  items,
  isLoading,
  isError,
}: {
  currentValue: string | null
  placeholder: string
  setFilterParam: (value: T | null) => void
  items: {
    label: string
    value: T
  }[]
  isLoading?: boolean
  isError?: boolean
}) {
  const selected = items.find(item => item.value === currentValue) ?? null
  return (
    <Combobox
      value={selected}
      onValueChange={item => setFilterParam(item?.value ?? null)}
      items={items}
    >
      <ComboboxInput
        placeholder={placeholder}
        showClear={true}
        className='max-w-45 min-w-30 flex-1'
      />
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
  )
}
