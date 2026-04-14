import { Card, CardContent } from '@/components/ui/card';
import { Moon, Star, Sparkles, Layers } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translateBackend } from '@/lib/backend-translations';

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
  const { language } = useTranslation();
  const formatted = formatEndTime(endTime);

  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent className="flex flex-col items-start gap-2">
        <div className="flex items-center gap-2 text-gray-600 text-sm">
          {icon}
          <span>{label}</span>
        </div>
        <div className="text-cosmic-text font-semibold text-lg">{value}</div>
        <div className="text-gray-600 text-sm">{subInfo}</div>
        {formatted && (
          <span className="text-sm px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20">
            {t('auto.upto')} {formatted}
          </span>
        )}
        {nextValue && (
          <span className="text-sm text-gray-500">→ {translateBackend(nextValue, language)}</span>
        )}
      </CardContent>
    </Card>
  );
}

function PanchangCore({ tithi, nakshatra, yoga, karana }: PanchangCoreProps) {
  const { language } = useTranslation();
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <ElementCard
        icon={<Moon className="w-4 h-4" />}
        label={t('auto.tithi')}
        value={translateBackend(tithi.name, language)}
        subInfo={translateBackend(tithi.paksha, language)}
        endTime={tithi.end_time}
        nextValue={translateBackend(tithi.next, language)}
      />
      <ElementCard
        icon={<Star className="w-4 h-4" />}
        label={t('auto.nakshatra')}
        value={translateBackend(nakshatra.name, language)}
        subInfo={`${t('auto.pada')} ${nakshatra.pada} · ${t('auto.lord')}: ${translateBackend(nakshatra.lord, language)}`}
        endTime={nakshatra.end_time}
        nextValue={translateBackend(nakshatra.next, language)}
      />
      <ElementCard
        icon={<Sparkles className="w-4 h-4" />}
        label={t('auto.yoga')}
        value={translateBackend(yoga.name, language)}
        subInfo={`#${yoga.number}`}
        endTime={yoga.end_time}
        nextValue={translateBackend(yoga.next, language)}
      />
      <ElementCard
        icon={<Layers className="w-4 h-4" />}
        label={t('auto.karana')}
        value={translateBackend(karana.name, language)}
        subInfo={karana.second_karana ? `${t('auto.2nd')}: ${translateBackend(karana.second_karana, language)}` : `#${karana.number}`}
        endTime={karana.end_time}
      />
    </div>
  );
}

export default PanchangCore;
