import * as React from 'react';
import { cn } from './cn';

/**
 * CSS-based fade+scale (150ms, ease-out).
 * If you prefer Framer Motion, replace with:
 *   import { motion, AnimatePresence } from 'framer-motion'
 * and swap this component’s root with <AnimatePresence> + <motion.div>.
 */
export function FadeScale({
  show,
  children,
  className,
}: {
  show: boolean;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        'transition duration-150 ease-out',
        show ? 'opacity-100 scale-100' : 'pointer-events-none opacity-0 scale-95',
        className,
      )}
    >
      {children}
    </div>
  );
}

