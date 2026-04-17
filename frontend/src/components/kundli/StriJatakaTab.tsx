import { useState, useEffect } from 'react';
import { Loader2, Heart, AlertTriangle, BookOpen, Info, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface StriYoga {
  key: string;
  name_en: string;
  name_hi: string;
  effect_en: string;
  effect_hi: string;
  severity: 'auspicious' | 'moderate' | 'challenging' | 'high' | string;
  sloka_ref: string;
  supporting_factors?: string[];
}

interface SeventhHouseAnalysis {
  seventh_sign?: string;
  seventh_lord?: string;
  seventh_lord_placement?: number;
  seventh_lord_sign?: string;
  seventh_lord_dignity?: string;
  seventh_lord_strength?: string;
  malefics_in_7th?: string[];
  benefics_in_7th?: string[];
  jupiter_aspects_7th?: boolean;
  venus_position?: string;
  interpretation_en?: string;
  interpretation_hi?: string;
}

interface StriJatakaData {
  applicable: boolean;
  reason?: string;
  yogas_detected: StriYoga[];
  seventh_house_analysis: SeventhHouseAnalysis;
  marital_prospect: 'favorable' | 'challenging' | 'mixed' | string;
  recommendations_en: string[];
  recommendations_hi: string[];
  sloka_ref: string;
  gender?: string;
  person_name?: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const severityStyles: Record<string, { badge: string; label_en: string; label_hi: string }> = {
  auspicious:  { badge: 'bg-emerald-100 text-emerald-800 border-emerald-200', label_en: 'Auspicious',  label_hi: 'शुभ' },
  moderate:    { badge: 'bg-amber-100 text-amber-800 border-amber-200',      label_en: 'Moderate',    label_hi: 'मध्यम' },
  challenging: { badge: 'bg-orange-100 text-orange-800 border-orange-200',   label_en: 'Challenging', label_hi: 'कठिन' },
  high:        { badge: 'bg-red-100 text-red-800 border-red-300',            label_en: 'High Risk',   label_hi: 'गंभीर' },
};

export default function StriJatakaTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<StriJatakaData | null>(null);
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
        const res = await api.get<StriJatakaData>(`/api/kundli/${kundliId}/stri-jataka`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Stri-Jataka analysis');
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

  // Not applicable (male/other)
  if (!data.applicable) {
    return (
      <div className="space-y-6">
        <div>
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
            <Heart className="w-6 h-6" />
            {t('auto.striJataka')}
          </Heading>
          <p className="text-sm text-muted-foreground">{t('auto.striJatakaDesc')}</p>
        </div>
        <div className="p-5 rounded-xl bg-amber-50 border border-amber-300 text-amber-900 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">{t('auto.striJatakaNotApplicable')}</p>
            {data.reason && <p className="text-sm mt-1">{data.reason}</p>}
          </div>
        </div>
      </div>
    );
  }

  const prospect = data.marital_prospect;
  const prospectStyle =
    prospect === 'favorable'
      ? { bg: 'bg-emerald-50 border-emerald-300', text: 'text-emerald-900', label: t('auto.prospectFavorable') }
      : prospect === 'challenging'
      ? { bg: 'bg-red-50 border-red-300', text: 'text-red-900', label: t('auto.prospectChallenging') }
      : { bg: 'bg-amber-50 border-amber-300', text: 'text-amber-900', label: t('auto.prospectMixed') };

  const sa = data.seventh_house_analysis || {};
  const recs = isHi ? data.recommendations_hi : data.recommendations_en;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Heart className="w-6 h-6" />
          {t('auto.striJataka')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.striJatakaDesc')}</p>
      </div>

      {/* Marital prospect banner */}
      <div className={`p-4 rounded-xl border ${prospectStyle.bg} ${prospectStyle.text} flex items-start gap-3`}>
        <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5" />
        <div>
          <p className="text-xs uppercase tracking-wide opacity-70">{t('auto.maritalProspect')}</p>
          <p className="text-lg font-bold">{prospectStyle.label}</p>
        </div>
      </div>

      {/* 7th house analysis */}
      <div className="p-5 rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm">
        <h3 className="text-base font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Info className="w-4 h-4" />
          {t('auto.seventhHouseAnalysis')}
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
          <div>
            <p className="text-[11px] uppercase tracking-wide text-muted-foreground">{t('auto.seventhLord')}</p>
            <p className="font-medium">
              {sa.seventh_lord || '—'}{sa.seventh_lord_sign ? ` (${sa.seventh_lord_sign})` : ''}
            </p>
          </div>
          <div>
            <p className="text-[11px] uppercase tracking-wide text-muted-foreground">
              {isHi ? 'स्थिति' : 'Placement'}
            </p>
            <p className="font-medium">
              {sa.seventh_lord_placement ? (isHi ? `भाव ${sa.seventh_lord_placement}` : `House ${sa.seventh_lord_placement}`) : '—'}
            </p>
          </div>
          <div>
            <p className="text-[11px] uppercase tracking-wide text-muted-foreground">
              {isHi ? 'बल' : 'Strength'}
            </p>
            <p className="font-medium capitalize">{sa.seventh_lord_strength || '—'}</p>
          </div>
          <div>
            <p className="text-[11px] uppercase tracking-wide text-muted-foreground">
              {isHi ? '7वें में पापी ग्रह' : 'Malefics in 7th'}
            </p>
            <p className="font-medium">{sa.malefics_in_7th?.length ? sa.malefics_in_7th.join(', ') : '—'}</p>
          </div>
          <div>
            <p className="text-[11px] uppercase tracking-wide text-muted-foreground">
              {isHi ? '7वें में शुभ ग्रह' : 'Benefics in 7th'}
            </p>
            <p className="font-medium">{sa.benefics_in_7th?.length ? sa.benefics_in_7th.join(', ') : '—'}</p>
          </div>
          <div>
            <p className="text-[11px] uppercase tracking-wide text-muted-foreground">
              {isHi ? 'गुरु दृष्टि' : 'Jupiter aspects 7th'}
            </p>
            <p className="font-medium">
              {sa.jupiter_aspects_7th ? (isHi ? 'हाँ' : 'Yes') : (isHi ? 'नहीं' : 'No')}
            </p>
          </div>
        </div>
        <p className="text-sm text-foreground/80 mt-4 leading-relaxed">
          {isHi ? sa.interpretation_hi : sa.interpretation_en}
        </p>
      </div>

      {/* Detected yogas */}
      {data.yogas_detected.length > 0 ? (
        <div>
          <h3 className="text-base font-semibold text-sacred-gold-dark mb-3">
            {t('auto.detectedYogas')} ({data.yogas_detected.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.yogas_detected.map((y) => {
              const name = isHi ? y.name_hi : y.name_en;
              const effect = isHi ? y.effect_hi : y.effect_en;
              const sev = severityStyles[y.severity] || severityStyles.moderate;
              const sevLabel = isHi ? sev.label_hi : sev.label_en;
              return (
                <div
                  key={y.key}
                  className="p-5 rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm"
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div>
                      <h4 className="text-lg font-bold text-sacred-gold-dark">{name}</h4>
                      {!isHi && y.name_hi && (
                        <p className="text-xs text-muted-foreground">{y.name_hi}</p>
                      )}
                    </div>
                    <span className={`shrink-0 px-2 py-1 rounded-md text-[11px] font-semibold border ${sev.badge}`}>
                      {sevLabel}
                    </span>
                  </div>
                  <p className="text-sm text-foreground leading-relaxed mb-3">{effect}</p>
                  {y.supporting_factors && y.supporting_factors.length > 0 && (
                    <div className="mb-3">
                      <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                        {t('auto.supportingFactors')}
                      </p>
                      <ul className="space-y-1">
                        {y.supporting_factors.map((f, i) => (
                          <li key={i} className="text-xs text-foreground/80 flex items-start gap-1.5">
                            <span className="text-sacred-gold mt-0.5">•</span>
                            <span>{f}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <div className="flex items-center gap-1.5 pt-2 border-t border-sacred-gold/15 text-[11px] text-muted-foreground">
                    <BookOpen className="w-3 h-3" />
                    <span className="italic">{y.sloka_ref}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 text-gray-700 text-sm">
          {isHi ? 'कोई विशेष स्त्री-जातक योग नहीं पाया गया।' : 'No specific Stri-Jataka yogas detected.'}
        </div>
      )}

      {/* Recommendations */}
      {recs.length > 0 && (
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-white shadow-sm">
          <h3 className="text-base font-semibold text-sacred-gold-dark mb-3">
            {t('auto.recommendations')}
          </h3>
          <ul className="space-y-2">
            {recs.map((r, i) => (
              <li key={i} className="text-sm text-foreground/90 flex items-start gap-2">
                <span className="text-sacred-gold mt-0.5">•</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Sloka footer */}
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground italic border-t border-sacred-gold/15 pt-3">
        <BookOpen className="w-3 h-3" />
        <span>{data.sloka_ref}</span>
      </div>
    </div>
  );
}
