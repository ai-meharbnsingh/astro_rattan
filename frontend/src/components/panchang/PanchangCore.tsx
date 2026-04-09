import { Card, CardContent } from '@/components/ui/card';
import { Moon, Star, Sparkles, Layers } from 'lucide-react';

interface PanchangCoreProps {
  tithi: { name: string; number: number; paksha: string; end_time?: string; next?: string };
  nakshatra: { name: string; pada: number; lord: string; end_time?: string; next?: string };
  yoga: { name: string; number: number; end_time?: string; next?: string };
  karana: { name: string; number: number; end_time?: string; second_karana?: string };
}

function formatEndTime(end_time?: string): string | null {
  if (!end_time) return null;
  try {
    const date = new Date(end_time);
    if (isNaN(date.getTime())) return end_time;
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  } catch {
    return end_time;
  }
}

interface ElementCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  subInfo: string;
  endTime?: string;
  nextValue?: string;
}

function ElementCard({ icon, label, value, subInfo, endTime, nextValue }: ElementCardProps) {
  const formatted = formatEndTime(endTime);

  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent className="flex flex-col items-start gap-2">
        <div className="flex items-center gap-2 text-cosmic-text/70 text-sm">
          {icon}
          <span>{label}</span>
        </div>
        <div className="text-cosmic-text font-semibold text-lg">{value}</div>
        <div className="text-cosmic-text/70 text-sm">{subInfo}</div>
        {formatted && (
          <span className="text-sm px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20">
            upto {formatted}
          </span>
        )}
        {nextValue && (
          <span className="text-sm text-cosmic-text/60">→ {nextValue}</span>
        )}
      </CardContent>
    </Card>
  );
}

function PanchangCore({ tithi, nakshatra, yoga, karana }: PanchangCoreProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <ElementCard
        icon={<Moon className="w-4 h-4" />}
        label="Tithi"
        value={tithi.name}
        subInfo={tithi.paksha}
        endTime={tithi.end_time}
        nextValue={tithi.next}
      />
      <ElementCard
        icon={<Star className="w-4 h-4" />}
        label="Nakshatra"
        value={nakshatra.name}
        subInfo={`Pada ${nakshatra.pada} · Lord: ${nakshatra.lord}`}
        endTime={nakshatra.end_time}
        nextValue={nakshatra.next}
      />
      <ElementCard
        icon={<Sparkles className="w-4 h-4" />}
        label="Yoga"
        value={yoga.name}
        subInfo={`#${yoga.number}`}
        endTime={yoga.end_time}
        nextValue={yoga.next}
      />
      <ElementCard
        icon={<Layers className="w-4 h-4" />}
        label="Karana"
        value={karana.name}
        subInfo={karana.second_karana ? `2nd: ${karana.second_karana}` : `#${karana.number}`}
        endTime={karana.end_time}
      />
    </div>
  );
}

export default PanchangCore;
