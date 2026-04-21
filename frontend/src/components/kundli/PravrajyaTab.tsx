import { useState, useEffect } from 'react';
import { Loader2, Flame, CheckCircle2, BookOpen, XCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import SlokaHover from './SlokaHover';

interface PravrajyaYoga {
  key: string;
  name_en: string;
  name_hi: string;
  strength: number;            // 1-10
  effect_en: string;
  effect_hi: string;
  sloka_ref: string;
  supporting_factors: string[];
}

interface PravrajyaData {
  yogas_found: PravrajyaYoga[];
  count: number;
  has_ascetic_tendency: boolean;
  kundli_id?: string;
  person_name?: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

export default function PravrajyaTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<PravrajyaData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const isHi = language === 'hi';

  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <Flame className="w-6 h-6" />
        {isHi ? 'प्रव्रज्या योग' : 'Pravrajya Yogas'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {isHi ? 'त्याग, अध्यात्म और संन्यास जीवन के योग' : 'Yogas for renunciation, spirituality & monastic life'}
      </p>
    </div>
  );

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const res = await api.get<PravrajyaData>(`/api/kundli/${kundliId}/pravrajya`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Pravrajya yogas');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="space-y-4">
        {header}
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        {header}
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
          {error}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="space-y-4">
        {header}
        <p className="text-center text-foreground py-8">{t('common.noData')}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {header}
      {/* Header container */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
          <Flame className="w-4 h-4" />
          <span>{t('auto.pravrajyaYogas')}</span>
          {data.has_ascetic_tendency && (
            <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">
              {data.count} {data.count === 1 ? 'yoga' : 'yogas'} {isHi ? 'पाए गए' : 'detected'}
            </span>
          )}
        </div>
        <div className="px-4 py-3">
          {data.has_ascetic_tendency ? (
            <div className="flex items-start gap-3 text-sm text-foreground">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>{t('auto.asceticTendency')}</span>
            </div>
          ) : (
            <div className="flex items-start gap-3 text-sm text-muted-foreground">
              <XCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{t('auto.noPravrajyaFound')}</span>
            </div>
          )}
          <p className="text-xs text-muted-foreground mt-1">{t('auto.pravrajyaDesc')}</p>
        </div>
      </div>

      {/* Yoga cards */}
      {data.yogas_found.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.yogas_found.map((yoga) => {
            const name = isHi ? yoga.name_hi : yoga.name_en;
            const effect = isHi ? yoga.effect_hi : yoga.effect_en;
            const strengthPct = (yoga.strength / 10) * 100;
            const strengthColor =
              yoga.strength >= 8 ? 'bg-emerald-500' :
              yoga.strength >= 5 ? 'bg-sacred-gold' : 'bg-orange-400';

            return (
              <div
                key={yoga.key}
                className="rounded-xl border border-border bg-transparent overflow-hidden"
              >
                <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[13px] font-semibold flex items-start justify-between gap-2">
                  <div>
                    <span>{name}</span>
                    {!isHi && yoga.name_hi && (
                      <span className="ml-2 text-[11px] font-normal opacity-80">{yoga.name_hi}</span>
                    )}
                  </div>
                  <span className="shrink-0 text-[12px] bg-white/20 px-2 py-0.5 rounded">{yoga.strength}/10</span>
                </div>
                <div className="p-4">
                  {/* Strength bar */}
                  <div className="mb-3">
                    <div className="flex items-center justify-between text-[11px] text-muted-foreground mb-1">
                      <span>{t('auto.yogaStrength')}</span>
                      <span>{yoga.strength}/10</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-border overflow-hidden">
                      <div
                        className={`h-full ${strengthColor} transition-all`}
                        style={{ width: `${strengthPct}%` }}
                      />
                    </div>
                  </div>

                  {/* Effect */}
                  <p className="text-sm text-foreground leading-relaxed mb-3">{effect}</p>

                  {/* Supporting factors */}
                  {yoga.supporting_factors.length > 0 && (
                    <div className="mb-3">
                      <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                        {t('auto.supportingFactors')}
                      </p>
                      <ul className="space-y-1">
                        {yoga.supporting_factors.map((f, i) => (
                          <li key={i} className="text-xs text-foreground/80 flex items-start gap-1.5">
                            <span className="text-sacred-gold-dark mt-0.5">•</span>
                            <span>{f}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Sloka ref */}
                  <div className="flex items-center gap-1.5 pt-2 border-t border-border text-[11px] text-muted-foreground">
                    <BookOpen className="w-3 h-3" />
                    <SlokaHover slokaRef={yoga.sloka_ref} language={language} className="italic" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
