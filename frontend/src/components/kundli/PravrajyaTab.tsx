import { useState, useEffect } from 'react';
import { Loader2, Flame, CheckCircle2, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

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
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
        {error}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Flame className="w-6 h-6" />
          {t('auto.pravrajyaYogas')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.pravrajyaDesc')}</p>
      </div>

      {/* Status banner */}
      {data.has_ascetic_tendency ? (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-300 text-amber-900 flex items-start gap-3">
          <CheckCircle2 className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">{t('auto.asceticTendency')}</p>
            <p className="text-sm mt-0.5">{data.count} {data.count === 1 ? 'yoga' : 'yogas'} {isHi ? 'पाए गए' : 'detected'}</p>
          </div>
        </div>
      ) : (
        <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 text-gray-700 text-sm">
          {t('auto.noPravrajyaFound')}
        </div>
      )}

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
                className="p-5 rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm"
              >
                {/* Name + strength badge */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <h3 className="text-lg font-bold text-sacred-gold-dark">{name}</h3>
                    {!isHi && yoga.name_hi && (
                      <p className="text-xs text-muted-foreground">{yoga.name_hi}</p>
                    )}
                  </div>
                  <div className="shrink-0 px-2 py-1 rounded-md bg-sacred-gold/15 text-xs font-semibold text-sacred-gold-dark">
                    {yoga.strength}/10
                  </div>
                </div>

                {/* Strength bar */}
                <div className="mb-3">
                  <div className="flex items-center justify-between text-[11px] text-muted-foreground mb-1">
                    <span>{t('auto.yogaStrength')}</span>
                    <span>{yoga.strength}/10</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-gray-200 overflow-hidden">
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
                          <span className="text-sacred-gold mt-0.5">•</span>
                          <span>{f}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Sloka ref */}
                <div className="flex items-center gap-1.5 pt-2 border-t border-sacred-gold/15 text-[11px] text-muted-foreground">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{yoga.sloka_ref}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
