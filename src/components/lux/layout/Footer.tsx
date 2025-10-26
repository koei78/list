import * as React from 'react';
import { Container } from './Container';

export function Footer() {
  return (
    <footer className="border-t border-[color:var(--lux-border)]/80">
      <Container className="flex h-20 items-center justify-between text-sm text-muted-foreground">
        <span>© {new Date().getFullYear()} Lux UI</span>
        <div className="flex gap-4">
          <a className="hover:text-foreground transition-colors" href="#privacy">Privacy</a>
          <a className="hover:text-foreground transition-colors" href="#terms">Terms</a>
        </div>
      </Container>
    </footer>
  );
}

