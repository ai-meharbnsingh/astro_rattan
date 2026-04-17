import { Sparkles, Loader2 } from 'lucide-react';
import { useState, useEffect } from 'react';
import { apiFetch } from '@/lib/api';
import { translatePlanet, translateRemedy } from '@/lib/backend-translations';
import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';

interface GeneralRemediesProps {
  language: string;
  t?: (key: string) => string;
  title?: string;
  kundliId?: string;
}

// No static remedies — all remedies must come from backend chart analysis

export default function GeneralRemedies({ language, t: tProp, title, kundliId }: GeneralRemediesProps) {
  const { t: tContext } = useTranslation();
  const t = tProp ?? tContext;
  const lang = language as any;
  const isHi = language === 'hi';
  const [dynamicRemedies, setDynamicRemedies] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (kundliId) {
      setLoading(true);
      apiFetch('/api/lalkitab/remedies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kundli_id: kundliId }),
      })
        .then(async (res) => {
          if (!res.ok) return null;
          return res.json();
        })
        .then((data) => {
          if (data?.remedies) setDynamicRemedies(data.remedies);
        })
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [kundliId]);

  const defaultTitle = t('auto.astrologicalRemedies');

  return (
    <div className="bg-muted rounded-xl p-5 border border-border mt-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-primary" />
          <Heading as={4} variant={4}>{title || defaultTitle}</Heading>
        </div>
        {loading && <Loader2 className="w-4 h-4 animate-spin text-primary" />}
      </div>
      
      {/* Dynamic Results if available */}
      {dynamicRemedies && dynamicRemedies.length > 0 && (
        <div className="mb-6 space-y-3">
          <Heading as={5} variant={5} className="text-primary border-b border-border/30 pb-1">
            {t('auto.basedOnYourChart')}
          </Heading>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {dynamicRemedies.map((rem, idx) => (
              <div key={idx} className="bg-muted/5 rounded-lg p-3 border border-border/20">
                <p className="text-sm font-semibold text-foreground">
                  {translatePlanet(rem.planet_en, lang)}
                </p>
                <p className="text-xs text-foreground mt-1">
                  {translateRemedy(rem.remedy_en, lang)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No static fallback — only dynamic chart-based remedies */}
      {(!dynamicRemedies || dynamicRemedies.length === 0) && !loading && (
        <p className="text-sm text-muted-foreground text-center py-4">
          {t('auto.noChartSpecificRemedies')}
        </p>
      )}
    </div>
  );
}
