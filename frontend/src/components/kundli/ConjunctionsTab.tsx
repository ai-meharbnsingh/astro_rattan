import { useState, useEffect } from 'react';
import { Loader2, Link2, Sparkles, TrendingUp, TrendingDown, BookOpen, Zap } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

const EFFECT_STRENGTH_BADGE: Record<string, string> = {
  full:     'bg-emerald-100 text-emerald-800',
  partial:  'bg-amber-100 text-amber-800',
  reversed: 'bg-red-100 text-red-800',
};
const EFFECT_STRENGTH_LABEL: Record<string, { en: string; hi: string }> = {
  full:     { en: 'Full Effect', hi: 'पूर्ण फल' },
  partial:  { en: 'Partial Effect', hi: 'आंशिक फल' },
  reversed: { en: 'Reversed Effect', hi: 'विपरीत फल' },
};

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
  effect_strength?: 'full' | 'partial' | 'reversed';
  effect_strength_reason_en?: string;
  effect_strength_reason_hi?: string;
  d12_also_conjunct?: boolean;
  d12_amplified_en?: string | null;
  d12_amplified_hi?: string | null;
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

const NATURE_BADGE: Record<string, string> = {
  benefic: 'bg-emerald-100 text-emerald-800',
  malefic: 'bg-red-100 text-red-800',
  mixed:   'bg-amber-100 text-amber-800',
};

const NATURE_KEY: Record<string, string> = {
  benefic: 'auto.natureBenefic',
  malefic: 'auto.natureMalefic',
  mixed:   'auto.natureMixed',
};

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';

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
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-sm text-foreground">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1">
          {isHi ? 'ग्रह युतियाँ' : 'Conjunctions'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi ? 'ग्रहों की युतियाँ और कुंडली में उनके संयुक्त प्रभाव' : 'Planetary conjunctions and their combined effects in chart'}
        </p>
      </div>

      {/* Header */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Link2 className="w-4 h-4" />
          <span>{t('auto.conjunctions')}</span>
          {data.count > 0 && (
            <span className="ml-auto text-[12px] font-normal opacity-80">
              {data.count} {isHi ? `युति${data.count !== 1 ? 'याँ' : ''}` : `conjunction${data.count !== 1 ? 's' : ''}`}
            </span>
          )}
        </div>
        <div className="px-4 py-2">
          <p className="text-xs text-muted-foreground">{t('auto.conjunctionsDesc')}</p>
        </div>
      </div>

      {/* No conjunctions */}
      {data.count === 0 && (
        <div className="p-6 rounded-xl border border-border text-muted-foreground text-center text-sm">
          {t('auto.noConjunctionsFound')}
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
            const strengthLabel = c.effect_strength ? EFFECT_STRENGTH_LABEL[c.effect_strength] : null;
            const strengthReason = isHi ? c.effect_strength_reason_hi : c.effect_strength_reason_en;
            const d12Amp = isHi ? c.d12_amplified_hi : c.d12_amplified_en;

            return (
              <div key={`${c.key}-${i}`} className="rounded-xl border border-border overflow-hidden">
                {/* Card header */}
                <div className="bg-sacred-gold-dark text-white px-3 py-2 flex items-start justify-between gap-2">
                  <div className="min-w-0">
                    <p className="text-[13px] font-semibold leading-snug truncate">{name}</p>
                    <p className="text-[10px] opacity-75 mt-0.5">
                      {t('auto.house')} {c.house} · {c.sign} · {t('auto.conjunctionOrb')}: {c.orb}°
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-1 shrink-0">
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded capitalize ${NATURE_BADGE[c.nature] || NATURE_BADGE.mixed}`}>
                      {t(NATURE_KEY[c.nature] || 'auto.natureMixed')}
                    </span>
                    {c.effect_strength && strengthLabel && (
                      <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${EFFECT_STRENGTH_BADGE[c.effect_strength]}`}>
                        {isHi ? strengthLabel.hi : strengthLabel.en}
                      </span>
                    )}
                    {c.special_yoga && (
                      <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-white/20 flex items-center gap-1">
                        <Sparkles className="w-2.5 h-2.5" />
                        {c.special_yoga}
                      </span>
                    )}
                  </div>
                </div>

                {/* Card body */}
                <div className="p-3 space-y-2">
                  {/* Effect strength reason */}
                  {strengthReason && (
                    <div className={`px-2 py-1.5 rounded text-xs flex items-start gap-1.5 ${
                      c.effect_strength === 'full'     ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' :
                      c.effect_strength === 'reversed' ? 'bg-red-50 text-red-800 border border-red-200' :
                                                         'bg-amber-50 text-amber-800 border border-amber-200'
                    }`}>
                      <span className="font-semibold shrink-0">{isHi ? 'कारण:' : 'Reason:'}</span>
                      <span>{strengthReason}</span>
                    </div>
                  )}

                  {/* Main effect */}
                  <p className="text-xs text-foreground leading-relaxed">{effect}</p>

                  {/* Enhanced */}
                  {c.enhanced && enhanced && (
                    <div className="p-2 rounded border border-border text-xs flex items-start gap-1.5">
                      <TrendingUp className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-emerald-700">{t('auto.enhancedInKendra')}</p>
                        <p className="text-foreground/80">{enhanced}</p>
                      </div>
                    </div>
                  )}

                  {/* Weakened */}
                  {weakened && (
                    <div className="p-2 rounded border border-border text-xs flex items-start gap-1.5">
                      <TrendingDown className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-blue-700">{t('auto.weakenedByBenefic')}</p>
                        <p className="text-foreground/80">{weakened}</p>
                      </div>
                    </div>
                  )}

                  {/* D12 amplification */}
                  {c.d12_also_conjunct && d12Amp && (
                    <div className="p-2 rounded border border-border text-xs flex items-start gap-1.5">
                      <Zap className="w-3.5 h-3.5 text-violet-600 shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-violet-700">
                          {isHi ? 'D12 में भी युत — प्रभाव प्रबल' : 'Also conjunct in D12 — Amplified'}
                        </p>
                        <p className="text-foreground/80">{d12Amp}</p>
                      </div>
                    </div>
                  )}

                  {/* Sloka ref */}
                  <div className="flex items-center gap-1.5 pt-1 border-t border-border text-[11px] text-muted-foreground">
                    <BookOpen className="w-3 h-3" />
                    <span className="italic">{c.sloka_ref}</span>
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
