import * as React from 'react';
import { Container } from './layout/Container';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './Card';
import { Button } from './Button';
import { Input } from './Input';
import { Modal } from './Modal';

export function LuxDemo() {
  const [open, setOpen] = React.useState(false);

  return (
    <Container>
      <div className="grid gap-8 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Card Title</CardTitle>
            <CardDescription>Subtle description with muted foreground.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4">
              <Input placeholder="Your email" aria-label="Email address" />
              <div className="flex gap-3">
                <Button variant="gold">Primary</Button>
                <Button variant="violet">Secondary</Button>
                <Button variant="outline">Outline</Button>
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button variant="solid-gold" onClick={() => setOpen(true)}>
              Open Modal
            </Button>
          </CardFooter>
        </Card>

        <Card className="flex items-center justify-center text-center">
          <div>
            <h3 className="font-display text-xl">Heavy Dark Luxury</h3>
            <p className="mt-2 text-muted-foreground">Silky gradients. Hairline borders. Gold accents.</p>
          </div>
        </Card>
      </div>

      <Modal open={open} onClose={() => setOpen(false)}>
        <div className="space-y-4">
          <h3 className="font-display text-lg">Subscribe</h3>
          <p className="text-sm text-muted-foreground">Get updates delivered to your inbox.</p>
          <div className="flex gap-3">
            <Input placeholder="Email" />
            <Button variant="gold">Join</Button>
          </div>
        </div>
      </Modal>
    </Container>
  );
}

