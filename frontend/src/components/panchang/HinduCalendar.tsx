import { Card, CardContent } from '@/components/ui/card';
import { BookOpen } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translateBackend } from '@/lib/backend-translations';

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
      <span className="block text-sm text-cosmic-text-secondary">{label}</span>
      <span className="block text-sm font-medium text-cosmic-text">{value}</span>
    </div>
  );
}

function HinduCalendar({ hindu_calendar, vaar }: HinduCalendarProps) {
  const { language } = useTranslation();
  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="h-5 w-5 text-sacred-gold" />
          <h3 className="text-lg font-semibold text-cosmic-text">
            {t('auto.hinduCalendar')}
          </h3>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <InfoCell label={t('auto.vikramSamvat')} value={hindu_calendar.vikram_samvat} />
          <InfoCell label={t('auto.shakaSamvat')} value={hindu_calendar.shaka_samvat} />
          <InfoCell label={t('auto.maas')} value={translateBackend(hindu_calendar.maas, language)} />
          <InfoCell label={t('auto.paksha')} value={translateBackend(hindu_calendar.paksha, language)} />
          <InfoCell
            label={t('auto.ritu')}
            value={t('auto.HinducalendarRituHin')}
          />
          <InfoCell label={t('auto.ayana')} value={translateBackend(hindu_calendar.ayana, language)} />
          <InfoCell
            label={t('auto.vaar')}
            value={t('auto.VaarNameVaarEnglish')}
          />
        </div>
      </CardContent>
    </Card>
  );
}

export default HinduCalendar;
