import * as React from 'react';
import { Container } from './Container';
import { Button } from '../Button';

export function Header() {
  return (
    <header className="sticky top-0 z-40 border-b border-[color:var(--lux-border)]/80 bg-[color:var(--lux-bg)]/70 backdrop-blur-[6px]">
      <Container className="flex h-16 items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-[color:var(--lux-gold)] to-[color:var(--lux-violet)]" />
          <span className="font-display text-sm tracking-wide text-foreground">Lux UI</span>
        </div>
        <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
          <a className="hover:text-foreground transition-colors" href="#features">Features</a>
          <a className="hover:text-foreground transition-colors" href="#pricing">Pricing</a>
          <a className="hover:text-foreground transition-colors" href="#about">About</a>
        </nav>
        <div className="flex items-center gap-3">
          <Button variant="violet" size="sm">Sign in</Button>
          <Button variant="gold" size="sm">Get started</Button>
        </div>
      </Container>
    </header>
  );
}

