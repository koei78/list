import * as React from 'react';
import { cn } from './cn';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = 'text', ...props }, ref) => {
    return (
      <input
        ref={ref}
        type={type}
        className={cn(
          'h-11 w-full rounded-2xl',
          'bg-[color:var(--lux-bg-subtle)]/80 lux-glass',
          'px-4 text-foreground placeholder:text-muted-foreground/70',
          'border border-[color:var(--lux-border)]',
          'focus-visible:ring-2 focus-visible:ring-[color:var(--lux-gold)] focus-visible:ring-offset-2 focus-visible:ring-offset-[color:var(--lux-bg)]',
          'transition duration-200 ease-out',
          className,
        )}
        {...props}
      />
    );
  },
);
Input.displayName = 'Input';

