import { Card, CardContent } from '@/components/ui/card';
import { BookOpen } from 'lucide-react';

interface HinduCalendarProps {
  hindu_calendar: {
    vikram_samvat: number;
    shaka_samvat: number;
    maas: string;
    paksha: string;
    ritu: string;
    ritu_english: string;
    ayana: string;
  };
  vaar: {
    name: string;
    english: string;
  };
}

interface InfoCellProps {
  label: string;
  value: string | number;
}

function InfoCell({ label, value }: InfoCellProps) {
  return (
    <div className="rounded-lg bg-cosmic-card border border-sacred-gold/10 px-3 py-2">
      <span className="block text-xs text-cosmic-text-secondary">{label}</span>
      <span className="block text-sm font-medium text-cosmic-text">{value}</span>
    </div>
  );
}

function HinduCalendar({ hindu_calendar, vaar }: HinduCalendarProps) {
  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="h-5 w-5 text-sacred-gold" />
          <h3 className="text-lg font-semibold text-cosmic-text">
            Hindu Calendar
          </h3>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <InfoCell label="Vikram Samvat" value={hindu_calendar.vikram_samvat} />
          <InfoCell label="Shaka Samvat" value={hindu_calendar.shaka_samvat} />
          <InfoCell label="Maas" value={hindu_calendar.maas} />
          <InfoCell label="Paksha" value={hindu_calendar.paksha} />
          <InfoCell
            label="Ritu"
            value={`${hindu_calendar.ritu} (${hindu_calendar.ritu_english})`}
          />
          <InfoCell label="Ayana" value={hindu_calendar.ayana} />
          <InfoCell
            label="Vaar"
            value={`${vaar.name} (${vaar.english})`}
          />
        </div>
      </CardContent>
    </Card>
  );
}

export default HinduCalendar;
