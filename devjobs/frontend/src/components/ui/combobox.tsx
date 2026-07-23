'use client'

import * as React from 'react'
import { Combobox as ComboboxPrimitive } from '@base-ui/react'
import { CheckIcon, ChevronDownIcon, XIcon } from 'lucide-react'

import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from '@/components/ui/input-group'

const ComboboxAnchorContext =
  React.createContext<React.RefObject<HTMLDivElement | null> | null>(null)

function Combobox<Value, Multiple extends boolean | undefined = false>(
  props: ComboboxPrimitive.Root.Props<Value, Multiple>
) {
  const anchor = React.useRef<HTMLDivElement>(null)
  return (
    <ComboboxAnchorContext.Provider value={anchor}>
      <ComboboxPrimitive.Root {...props} />
    </ComboboxAnchorContext.Provider>
  )
}

function ComboboxValue({ ...props }: ComboboxPrimitive.Value.Props) {
  return <ComboboxPrimitive.Value data-slot='combobox-value' {...props} />
}

function ComboboxTrigger({
  className,
  children,
  ...props
}: ComboboxPrimitive.Trigger.Props) {
  return (
    <ComboboxPrimitive.Trigger
      data-slot='combobox-trigger'
      className={cn(className)}
      {...props}
    >
      {children}
      <ChevronDownIcon className='text-muted-foreground pointer-events-none' />
    </ComboboxPrimitive.Trigger>
  )
}

function ComboboxClear({ className, ...props }: ComboboxPrimitive.Clear.Props) {
  return (
    <ComboboxPrimitive.Clear
      data-slot='combobox-clear'
      className={cn(className)}
      {...props}
      render={
        <InputGroupButton>
          <XIcon className='pointer-events-none' />
        </InputGroupButton>
      }
    />
  )
}

function ComboboxInput({
  className,
  children,
  disabled = false,
  showTrigger = true,
  showClear = false,
  ...props
}: ComboboxPrimitive.Input.Props & {
  showTrigger?: boolean
  showClear?: boolean
}) {
  const anchor = React.useContext(ComboboxAnchorContext)
  return (
    <InputGroup ref={anchor} className={cn('w-full min-w-0', className)}>
      <ComboboxPrimitive.Input
        render={<InputGroupInput disabled={disabled} />}
        {...props}
      />
      {(showTrigger || showClear) && (
        <InputGroupAddon align='inline-end'>
          {showTrigger && (
            <InputGroupButton
              render={<ComboboxTrigger />}
              data-slot='input-group-button'
              className='group-has-data-[slot=combobox-clear]/input-group:hidden data-pressed:bg-transparent'
              disabled={disabled}
            />
          )}
          {showClear && <ComboboxClear disabled={disabled} />}
        </InputGroupAddon>
      )}
      {children}
    </InputGroup>
  )
}
function ComboboxContent({
  className,
  side = 'bottom',
  sideOffset = 7,
  align = 'start',
  alignOffset = 0,
  anchor,
  ...props
}: ComboboxPrimitive.Popup.Props &
  Pick<
    ComboboxPrimitive.Positioner.Props,
    'side' | 'align' | 'sideOffset' | 'alignOffset' | 'anchor'
  >) {
  const contextAnchor = React.useContext(ComboboxAnchorContext)
  const resolvedAnchor = anchor ?? contextAnchor
  return (
    <ComboboxPrimitive.Portal>
      <ComboboxPrimitive.Positioner
        side={side}
        sideOffset={sideOffset}
        align={align}
        alignOffset={alignOffset}
        anchor={resolvedAnchor}
        className='isolate z-50'
      >
        <ComboboxPrimitive.Popup
          data-slot='combobox-content'
          data-chips={!!anchor}
          className={cn(
            'group/combobox-content bg-popover text-popover-foreground ring-input relative overflow-hidden rounded-lg ring-1',
            // Para un input dentro del combobox-content, modifica hijo directo
            '*:data-[slot=input-group]:border-input/30',
            '*:data-[slot=input-group]:bg-input/30',
            '*:data-[slot=input-group]:m-1',
            '*:data-[slot=input-group]:mb-0',
            '*:data-[slot=input-group]:h-8',
            // '*:data-[slot=input-group]:shadow-none',

            // anchor-width: tamaño del inputgroup/comboboxtrigger
            'w-(--anchor-width) min-w-(--anchor-width)',
            'max-h-(--available-height) max-w-(--available-width)',
            'data-[chips=true]:min-w-(--anchor-width)', // Cambia el ancho por las chips

            // 'origin-(--transform-origin)',
            // 'duration-100',
            // 'data-[side=bottom]:slide-in-from-top-2',
            // 'data-[side=inline-end]:slide-in-from-left-2',
            // 'data-[side=inline-start]:slide-in-from-right-2',
            // 'data-[side=left]:slide-in-from-right-2',
            // 'data-[side=right]:slide-in-from-left-2',
            // 'data-[side=top]:slide-in-from-bottom-2',
            // 'data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95',
            // 'shadow-md',
            className
          )}
          {...props}
        />
      </ComboboxPrimitive.Positioner>
    </ComboboxPrimitive.Portal>
  )
}

function ComboboxList({ className, ...props }: ComboboxPrimitive.List.Props) {
  return (
    <ComboboxPrimitive.List
      data-slot='combobox-list'
      className={cn(
        'max-h-[calc(var(--available-height)---spacing(9))] scroll-py-1 overflow-y-auto p-1 data-empty:p-0',
        '[scrollbar-width:none] [&::-webkit-scrollbar]:hidden',
        'overscroll-contain', // Para no permitir el scroll-chaining, cuango llego al limite del scroll despues se lo pasa al padre
        // 'no-scrollbar', // Utility custom, que no tengo porque no instale el paquete de shadcn
        // 'max-h-[min(calc(--spacing(72)---spacing(9)),calc(var(--available-height)---spacing(9)))]',
        className
      )}
      {...props}
    />
  )
}

function ComboboxItem({
  className,
  children,
  ...props
}: ComboboxPrimitive.Item.Props) {
  return (
    <ComboboxPrimitive.Item
      data-slot='combobox-item'
      className={cn(
        "data-highlighted:bg-accent data-highlighted:text-accent-foreground flex w-full cursor-default items-center justify-between rounded-md px-1.5 py-1 text-base outline-hidden select-none data-disabled:pointer-events-none data-disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
        'not-data-[variant=destructive]:data-highlighted:**:text-accent-foreground', // Si no es destructive le colocamos a los hijos ese foreground
        // 'gap-2',
        className
      )}
      {...props}
    >
      {children}
      <ComboboxPrimitive.ItemIndicator
        // Es renderizado condicional, solo que no se ve
        render={
          <span className='pointer-events-none flex size-4 items-center justify-center'>
            <CheckIcon className='pointer-events-none' />
          </span>
        }
      />
    </ComboboxPrimitive.Item>
  )
}

function ComboboxGroup({ className, ...props }: ComboboxPrimitive.Group.Props) {
  return (
    <ComboboxPrimitive.Group
      data-slot='combobox-group'
      className={cn(className)}
      {...props}
    />
  )
}

function ComboboxLabel({
  className,
  ...props
}: ComboboxPrimitive.GroupLabel.Props) {
  return (
    <ComboboxPrimitive.GroupLabel
      data-slot='combobox-label'
      className={cn('text-muted-foreground px-2 py-1.5 text-xs', className)}
      {...props}
    />
  )
}

function ComboboxCollection({ ...props }: ComboboxPrimitive.Collection.Props) {
  return (
    <ComboboxPrimitive.Collection data-slot='combobox-collection' {...props} />
  )
}

function ComboboxEmpty({ className, ...props }: ComboboxPrimitive.Empty.Props) {
  return (
    <ComboboxPrimitive.Empty
      data-slot='combobox-empty'
      className={cn(
        'text-muted-foreground w-full justify-center py-2 text-center text-sm',
        'hidden', // Lo ocultamos defeault
        'group-data-empty/combobox-content:flex', // Si combobox-content tiene data-empty, lo mostramos
        className
      )}
      {...props}
    />
  )
}

function ComboboxSeparator({
  className,
  ...props
}: ComboboxPrimitive.Separator.Props) {
  return (
    <ComboboxPrimitive.Separator
      data-slot='combobox-separator'
      className={cn('bg-border -mx-1 my-1 h-px', className)}
      {...props}
    />
  )
}

function ComboboxChips({
  className,
  ...props
}: React.ComponentPropsWithRef<typeof ComboboxPrimitive.Chips> &
  ComboboxPrimitive.Chips.Props) {
  const anchor = React.useContext(ComboboxAnchorContext)
  return (
    <ComboboxPrimitive.Chips
      data-slot='combobox-chips'
      ref={anchor}
      className={cn(
        'border-input focus-within:ring-ring/50 has-aria-invalid:border-destructive has-aria-invalid:ring-destructive/20 flex min-h-9 flex-wrap items-center gap-1 rounded-lg border bg-transparent bg-clip-padding px-2.5 py-1 text-base focus-within:ring-3 has-aria-invalid:ring-3 has-data-[slot=combobox-chip]:px-1',
        // 'focus-within:border-ring',
        // 'dark:bg-input/30 dark:has-aria-invalid:border-destructive/50 dark:has-aria-invalid:ring-destructive/40',
        // 'transition-colors',
        className
      )}
      {...props}
    />
  )
}

function ComboboxChip({
  className,
  children,
  showRemove = true,
  ...props
}: ComboboxPrimitive.Chip.Props & {
  showRemove?: boolean
}) {
  return (
    <ComboboxPrimitive.Chip
      data-slot='combobox-chip'
      className={cn(
        'bg-muted text-foreground flex w-fit items-center justify-center gap-1 rounded-sm px-1.5 text-xs font-medium whitespace-nowrap has-disabled:pointer-events-none has-disabled:cursor-not-allowed has-disabled:opacity-50 has-data-[slot=combobox-chip-remove]:pr-0',
        // 'h-[calc(--spacing(5.25))]',
        className
      )}
      {...props}
    >
      {children}
      {showRemove && (
        <ComboboxPrimitive.ChipRemove
          className='-ml-1 opacity-50 hover:opacity-100'
          data-slot='combobox-chip-remove'
          render={
            <Button variant='ghost' size='icon-xs'>
              <XIcon className='pointer-events-none' />
            </Button>
          }
        />
      )}
    </ComboboxPrimitive.Chip>
  )
}

function ComboboxChipsInput({
  className,
  ...props
}: ComboboxPrimitive.Input.Props) {
  return (
    <ComboboxPrimitive.Input
      data-slot='combobox-chip-input'
      className={cn('min-w-16 flex-1 outline-none', className)}
      {...props}
    />
  )
}

function useComboboxAnchor() {
  return React.useRef<HTMLDivElement | null>(null)
}

export {
  Combobox,
  ComboboxInput,
  ComboboxContent,
  ComboboxList,
  ComboboxItem,
  ComboboxGroup,
  ComboboxLabel,
  ComboboxCollection,
  ComboboxEmpty,
  ComboboxSeparator,
  ComboboxChips,
  ComboboxChip,
  ComboboxChipsInput,
  ComboboxTrigger,
  ComboboxValue,
  useComboboxAnchor,
}
