import { useState, useEffect } from 'react';
import { Loader2, Link2, Sparkles, TrendingUp, TrendingDown, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface Conjunction {
  key: string;
  planets: string[];
  house: number;
  sign: string;
  orb: number;
  name_en: string;
  name_hi: string;
  nature: 'benefic' | 'malefic' | 'mixed';
  effect_en: string;
  effect_hi: string;
  enhanced: boolean;
  enhanced_en?: string | null;
  enhanced_hi?: string | null;
  weakened: boolean;
  weakened_en?: string | null;
  weakened_hi?: string | null;
  special_yoga?: string | null;
  sloka_ref: string;
}

interface ApiResponse {
  kundli_id?: string;
  person_name?: string;
  conjunctions: Conjunction[];
  count: number;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const NATURE_COLOR: Record<string, string> = {
  benefic: 'border-emerald-300 bg-emerald-50',
  malefic: 'border-red-300 bg-red-50',
  mixed: 'border-sacred-gold/40 bg-sacred-gold/5',
};

const NATURE_BADGE: Record<string, string> = {
  benefic: 'bg-emerald-600 text-white',
  malefic: 'bg-red-600 text-white',
  mixed: 'bg-sacred-gold-dark text-white',
};

const NATURE_KEY: Record<string, string> = {
  benefic: 'auto.natureBenefic',
  malefic: 'auto.natureMalefic',
  mixed: 'auto.natureMixed',
};

export default function ConjunctionsTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/conjunctions`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load conjunctions');
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
          <Link2 className="w-6 h-6" />
          {t('auto.conjunctions')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.conjunctionsDesc')}</p>
      </div>

      {/* Summary */}
      {data.count === 0 ? (
        <div className="p-6 rounded-xl bg-gray-50 border border-gray-200 text-gray-700 text-center">
          {t('auto.noConjunctionsFound')}
        </div>
      ) : (
        <div className="p-4 rounded-xl bg-sacred-gold/10 border border-sacred-gold/30">
          <p className="text-sm">
            <span className="font-semibold text-sacred-gold-dark">{data.count}</span>{' '}
            {isHi ? 'युति' + (data.count !== 1 ? 'याँ' : '') + ' पाई गईं' : `conjunction${data.count !== 1 ? 's' : ''} detected`}
          </p>
        </div>
      )}

      {/* Conjunction cards */}
      {data.conjunctions.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {data.conjunctions.map((c, i) => {
            const name = isHi ? c.name_hi : c.name_en;
            const effect = isHi ? c.effect_hi : c.effect_en;
            const enhanced = isHi ? c.enhanced_hi : c.enhanced_en;
            const weakened = isHi ? c.weakened_hi : c.weakened_en;

            return (
              <div
                key={`${c.key}-${i}`}
                className={`rounded-xl border-2 p-5 ${NATURE_COLOR[c.nature] || NATURE_COLOR.mixed}`}
              >
                {/* Header row */}
                <div className="flex items-start justify-between gap-3 mb-3 flex-wrap">
                  <div>
                    <h3 className="text-lg font-bold text-foreground">{name}</h3>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                      <span>{isHi ? 'भाव' : 'House'} {c.house}</span>
                      <span>•</span>
                      <span>{c.sign}</span>
                      <span>•</span>
                      <span>{t('auto.conjunctionOrb')}: {c.orb}°</span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded ${NATURE_BADGE[c.nature] || NATURE_BADGE.mixed}`}>
                      {t(NATURE_KEY[c.nature] || 'auto.natureMixed')}
                    </span>
                    {c.special_yoga && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-violet-600 text-white flex items-center gap-1">
                        <Sparkles className="w-3 h-3" />
                        {c.special_yoga}
                      </span>
                    )}
                  </div>
                </div>

                {/* Effect */}
                <p className="text-sm text-foreground leading-relaxed mb-3">{effect}</p>

                {/* Enhanced */}
                {c.enhanced && enhanced && (
                  <div className="mt-3 p-2 rounded bg-emerald-100/70 border border-emerald-200 text-xs flex items-start gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-700 shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-emerald-800">{t('auto.enhancedInKendra')}</p>
                      <p className="text-emerald-900/80">{enhanced}</p>
                    </div>
                  </div>
                )}

                {/* Weakened info */}
                {weakened && (
                  <div className="mt-2 p-2 rounded bg-blue-100/60 border border-blue-200 text-xs flex items-start gap-1.5">
                    <TrendingDown className="w-3.5 h-3.5 text-blue-700 shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-blue-800">{t('auto.weakenedByBenefic')}</p>
                      <p className="text-blue-900/80">{weakened}</p>
                    </div>
                  </div>
                )}

                {/* Sloka ref */}
                <div className="flex items-center gap-1.5 mt-3 pt-2 border-t border-current/10 text-[11px] text-muted-foreground">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{c.sloka_ref}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
