import type React from 'react';
import { Heading } from '@/components/ui/heading';

export default function PanchangTabHeader({
  icon: Icon,
  title,
  description,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
}) {
  return (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <Icon className="w-6 h-6" />
        {title}
      </Heading>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}

