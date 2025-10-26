import * as React from 'react';
import { Header } from './Header';
import { Footer } from './Footer';

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-dvh bg-[color:var(--lux-bg)] text-foreground">
      <Header />
      <main className="lux-section">
        {children}
      </main>
      <Footer />
    </div>
  );
}

