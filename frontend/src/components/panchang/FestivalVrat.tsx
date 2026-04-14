import { Card, CardContent } from '@/components/ui/card';
import { Flame } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translateBackend } from '@/lib/backend-translations';

interface Festival {
  name: string;
  name_hindi?: string;
  type: string;
  description: string;
  rituals?: string;
}

interface FestivalVratProps {
  festivals: Festival[];
}

const typeBadgeColors: Record<string, string> = {
  major: 'bg-sacred-gold/15 text-sacred-gold border-sacred-gold/30',
  fasting: 'bg-amber-500/15 text-amber-400 border-amber-300/30',
  auspicious: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  regional: 'bg-blue-500/15 text-blue-400 border-blue-500/30',
};

function TypeBadge({ type }: { type: string }) {
  const { language } = useTranslation();
  const colors =
    typeBadgeColors[type.toLowerCase()] ??
    'bg-cosmic-text-secondary/15 text-cosmic-text-secondary border-cosmic-text-secondary/30';

  return (
    <span
      className={`inline-block text-sm font-medium px-2.5 py-0.5 rounded-full border capitalize ${colors}`}
    >
      {translateBackend(type, language)}
    </span>
  );
}

function FestivalVrat({ festivals }: FestivalVratProps) {
  const { language } = useTranslation();
  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <Flame className="h-5 w-5 text-sacred-gold" />
          <h3 className="text-lg font-semibold text-cosmic-text">
            {t('auto.festivalsVrat')}
          </h3>
        </div>

        {festivals.length === 0 ? (
          <p className="text-sm text-cosmic-text-secondary italic">
            {t('auto.noSpecialObservanceT')}
          </p>
        ) : (
          <div className="flex flex-col gap-3">
            {festivals.map((festival, index) => (
              <div
                key={index}
                className="rounded-xl bg-cosmic-card border border-sacred-gold/10 p-4"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <span className="text-cosmic-text font-semibold">
                      {festival.name}
                    </span>
                    {festival.name_hindi && (
                      <span className="ml-2 text-cosmic-text-secondary text-sm">
                        ({festival.name_hindi})
                      </span>
                    )}
                  </div>
                  <TypeBadge type={festival.type} />
                </div>

                <p className="text-sm text-cosmic-text-secondary mb-2">
                  {translateBackend(festival.description, language)}
                </p>

                {festival.rituals && (
                  <div className="text-sm text-cosmic-text-secondary bg-sacred-gold/5 rounded-lg px-3 py-2 border border-sacred-gold/10">
                    <span className="font-medium text-sacred-gold">{t('auto.rituals')}</span>
                    {translateBackend(festival.rituals, language)}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default FestivalVrat;
