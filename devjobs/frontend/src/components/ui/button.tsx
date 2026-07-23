import { Button as ButtonPrimitive } from '@base-ui/react/button'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const buttonVariants = cva(
  [
    'group/button inline-flex shrink-0 items-center justify-center rounded-lg border border-transparent whitespace-nowrap outline-none focus-visible:ring-3 focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 [&_svg]:pointer-events-none [&_svg]:shrink-0 select-none',
    'font-medium bg-clip-padding', // Para que el fondo no este debajo del borde semitransparente
    // focus-visible:border-ring
    // 'transition-all',
    // 'active:not-aria-[haspopup]:translate-y-px', // El botón se hunde al presionario
  ],
  {
    variants: {
      variant: {
        default: 'bg-primary text-foreground hover:bg-primary/80',
        outline: cn(
          'border-border bg-background text-primary-foreground hover:bg-muted hover:text-foreground dark:hover:bg-input/50',
          'aria-expanded:bg-muted aria-expanded:text-foreground'
          // 'dark:bg-input/30, dark:border-input'
        ),

        secondary:
          'bg-secondary text-secondary-foreground hover:bg-[color-mix(in_oklch,var(--secondary),var(--foreground)_5%)] aria-expanded:bg-secondary aria-expanded:text-secondary-foreground',
        ghost:
          'hover:bg-muted hover:text-foreground aria-expanded:bg-muted aria-expanded:text-foreground dark:hover:bg-muted/50',
        destructive:
          'bg-destructive/10 text-destructive hover:bg-destructive/20 focus-visible:border-destructive/40 focus-visible:ring-destructive/20 dark:bg-destructive/20 dark:hover:bg-destructive/30 dark:focus-visible:ring-destructive/40',
        link: 'text-foreground underline-offset-4 hover:underline',
      },
      size: {
        xs: cn(
          "h-6 gap-x-0.75 rounded-md px-2 text-xs [&_svg:not([class*='size-'])]:size-3",
          'in-data-[slot=button-group]:rounded-lg', // Si hay un ancestro button group usa rounded-lg
          'has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5' // Si hay un descendiente icon, le cambia el padding de su lado
        ),
        sm: cn(
          'h-7 gap-x-1 rounded-lg px-2.5 text-[0.8rem] [&_svg:not([class*="size-"])]:size-3.5',
          'has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 '
        ),
        default: cn(
          'h-8 gap-x-1.5 rounded-lg px-2.5 text-sm [&_svg:not([class*="size-"])]:size-4',
          'has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2'
        ),
        lg: cn(
          'h-9 gap-x-1.5 rounded-lg px-2.5 text-sm [&_svg:not([class*="size-"])]:size-4.5',
          'has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2'
        ),
        'icon-xs': cn(
          "size-6 rounded-md [&_svg:not([class*='size-'])]:size-3",
          'in-data-[slot=button-group]:rounded-lg'
        ),
        'icon-sm': cn(
          'size-7 rounded-md [&_svg:not([class*="size-"])]:size-3.5',
          'in-data-[slot=button-group]:rounded-lg'
        ),
        icon: 'size-8 rounded-lg [&_svg:not([class*="size-"])]:size-4',
        
        'icon-lg': 'size-9 rounded-lg [&_svg:not([class*="size-"])]:size-4.5',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

function Button({
  className,
  variant = 'default',
  size = 'default',
  ...props
}: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>) {
  return (
    <ButtonPrimitive
      data-slot='button'
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
