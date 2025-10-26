import * as React from 'react';
import { cn } from '../cn';

export function Container({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('mx-auto w-full max-w-7xl px-6 md:px-8', className)}
      {...props}
    />
  );
}

