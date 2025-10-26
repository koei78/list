import * as React from 'react';
import { createPortal } from 'react-dom';
import { cn } from './cn';

export interface ModalProps {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  className?: string;
}

export function Modal({ open, onClose, children, className }: ModalProps) {
  const [mounted, setMounted] = React.useState(false);
  React.useEffect(() => { setMounted(true); return () => setMounted(false); }, []);

  if (!mounted) return null;

  return createPortal(
    <div
      role="dialog"
      aria-modal="true"
      className={cn(
        'fixed inset-0 z-50 grid place-items-center',
        'transition-opacity duration-150 ease-out',
        open ? 'opacity-100' : 'pointer-events-none opacity-0',
      )}
      onClick={onClose}
    >
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-[3px]" />

      {/* Panel */}
      <div
        className={cn(
          'relative lux-surface lux-glass w-[min(92vw,640px)]',
          'p-6 md:p-8',
          'transition duration-150 ease-out',
          open ? 'opacity-100 scale-100' : 'opacity-0 scale-95',
          className,
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>,
    document.body,
  );
}

