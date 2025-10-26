import * as React from 'react';
import { cn } from './cn';

export type ButtonVariant = 'gold' | 'violet' | 'ghost' | 'outline' | 'solid-gold';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

const base =
  'inline-flex items-center justify-center select-none rounded-2xl font-medium focus-visible:outline-none transition duration-200 ease-out will-change-transform';

const sizes: Record<ButtonSize, string> = {
  sm: 'h-9 px-4 text-sm',
  md: 'h-11 px-6 text-sm',
  lg: 'h-12 px-7 text-base',
};

const variants: Record<ButtonVariant, string> = {
  // Primary style: dark base with gold accent for 7:1 contrast
  gold:
    'text-[color:var(--lux-gold)] bg-[color:var(--lux-bg-subtle)] border border-[color:var(--lux-gold)]/35 hover:bg-[color:var(--lux-gold)]/10 active:scale-[0.99] shadow-lux',
  violet:
    'text-[color:var(--lux-violet)] bg-[color:var(--lux-bg-subtle)] border border-[color:var(--lux-violet)]/40 hover:bg-[color:var(--lux-violet)]/12 active:scale-[0.99] shadow-lux',
  ghost:
    'text-[color:var(--lux-fg)] bg-transparent hover:bg-white/5 border border-transparent',
  outline:
    'text-[color:var(--lux-fg)] bg-transparent border border-[color:var(--lux-border)] hover:border-white/20 hover:bg-white/4',
  // Solid gold CTA: use for large/bold text only to maintain contrast
  'solid-gold':
    'text-[color:var(--lux-bg)] bg-[color:var(--lux-gold)] hover:bg-[color:var(--lux-gold)]/90 border border-[color:var(--lux-gold)] shadow-lux',
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'gold', size = 'md', children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          base,
          'focus-visible:ring-2 focus-visible:ring-[color:var(--lux-gold)] focus-visible:ring-offset-2 focus-visible:ring-offset-[color:var(--lux-bg)]',
          sizes[size],
          variants[variant],
          className,
        )}
        {...props}
      >
        {children}
      </button>
    );
  },
);
Button.displayName = 'Button';

