import { useTranslation } from '@/lib/i18n';
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
  seventh_lord_nakshatra?: string;
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
  mars_house?: number;
  female_mangal_note_en?: string;
  female_mangal_note_hi?: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const severityStyles: Record<string, { badge: string; label_en: string; label_hi: string }> = {
  auspicious:  { badge: 'bg-emerald-100 text-emerald-800', label_en: 'Auspicious',  label_hi: 'शुभ' },
  moderate:    { badge: 'bg-amber-100 text-amber-800',     label_en: 'Moderate',    label_hi: 'मध्यम' },
  challenging: { badge: 'bg-orange-100 text-orange-800',   label_en: 'Challenging', label_hi: 'कठिन' },
  high:        { badge: 'bg-red-100 text-red-800',         label_en: 'High Risk',   label_hi: 'गंभीर' },
};

const thCls = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdMuted = 'p-1.5 text-xs text-muted-foreground border-t border-border align-top';

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';

export default function StriJatakaTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<StriJatakaData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const isHi = language === 'hi';

  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <Heart className="w-6 h-6" />
        {isHi ? 'स्त्री जातक' : 'Stri Jataka'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {isHi ? 'पारंपरिक स्त्री कुंडली — विवाह और स्त्री संकेतक' : 'Traditional female horoscopy — marriage & feminine signifiers'}
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
        const res = await api.get<StriJatakaData>(`/api/kundli/${kundliId}/stri-jataka`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || t('auto.genericError'));
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
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-sm text-foreground">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        {header}
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
      </div>
    );
  }

  if (!data) return null;

  if (!data.applicable) {
    return (
      <div className="space-y-6">
        {header}
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Heart className="w-4 h-4" />
            <span>{t('auto.striJataka')}</span>
          </div>
          <div className="px-4 py-3">
            <p className="text-xs text-muted-foreground mb-3">{t('auto.striJatakaDesc')}</p>
            <div className="flex items-start gap-3 text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded-lg p-3">
              <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-700" />
              <div>
                <p className="font-semibold">{t('auto.striJatakaNotApplicable')}</p>
                {data.reason && <p className="text-sm mt-1">{data.reason}</p>}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const prospect = data.marital_prospect;
  const prospectBadge =
    prospect === 'favorable' ? 'bg-emerald-100 text-emerald-800' :
    prospect === 'challenging' ? 'bg-red-100 text-red-800' :
    'bg-amber-100 text-amber-800';
  const prospectLabel =
    prospect === 'favorable' ? t('auto.prospectFavorable') :
    prospect === 'challenging' ? t('auto.prospectChallenging') :
    t('auto.prospectMixed');

  const sa = data.seventh_house_analysis || {};
  const recs = isHi ? data.recommendations_hi : data.recommendations_en;

  const rows7th: { label: string; value: string }[] = [
    { label: t('auto.seventhLord'), value: [sa.seventh_lord, sa.seventh_lord_sign ? `(${sa.seventh_lord_sign})` : ''].filter(Boolean).join(' ') || '—' },
    { label: t('auto.placement'), value: sa.seventh_lord_placement ? `${t('auto.house')} ${sa.seventh_lord_placement}` : '—' },
    { label: t('auto.strength'), value: sa.seventh_lord_strength || '—' },
    ...(sa.seventh_lord_nakshatra ? [{ label: isHi ? 'नक्षत्र' : 'Nakshatra', value: sa.seventh_lord_nakshatra }] : []),
    { label: t('auto.maleficsIn7th'), value: sa.malefics_in_7th?.length ? sa.malefics_in_7th.join(', ') : '—' },
    { label: t('auto.beneficsIn7th'), value: sa.benefics_in_7th?.length ? sa.benefics_in_7th.join(', ') : '—' },
    { label: t('auto.jupiterAspects7th'), value: sa.jupiter_aspects_7th ? t('common.yes') : t('common.no') },
  ];

  return (
    <div className="space-y-6">
      {header}

      {/* Header */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Heart className="w-4 h-4" />
          <span>{t('auto.striJataka')}</span>
          <span className={`ml-auto text-[12px] font-semibold px-2 py-0.5 rounded capitalize ${prospectBadge}`}>
            <CheckCircle2 className="w-3 h-3 inline mr-1" />
            {prospectLabel}
          </span>
        </div>
        <div className="px-4 py-2">
          <p className="text-xs text-muted-foreground">{t('auto.striJatakaDesc')}</p>
        </div>
      </div>

      {/* 7th House Analysis */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Info className="w-4 h-4" />
          <span>{t('auto.seventhHouseAnalysis')}</span>
        </div>
        <div className="overflow-x-auto">
        <table style={{ tableLayout: 'fixed', minWidth: '280px', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '40%' }} />
            <col style={{ width: '60%' }} />
          </colgroup>
          <thead>
            <tr>
              <th className={thCls}>{isHi ? 'विषय' : 'Factor'}</th>
              <th className={thCls}>{isHi ? 'विवरण' : 'Detail'}</th>
            </tr>
          </thead>
          <tbody>
            {rows7th.map((r, i) => (
              <tr key={i}>
                <td className={tdMuted}>{r.label}</td>
                <td className={`${tdCls} font-medium capitalize`}>{r.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
        {(sa.interpretation_en || sa.interpretation_hi) && (
          <div className="px-3 py-2 border-t border-border">
            <p className="text-xs text-foreground/80 leading-relaxed">
              {isHi ? sa.interpretation_hi : sa.interpretation_en}
            </p>
          </div>
        )}
      </div>

      {/* Female Mangal Dosha */}
      {data.female_mangal_note_en && (
        <div className={ohContainer}>
          <div className={`${ohHeader} ${
            data.mars_house === 8 ? 'bg-red-700' :
            data.mars_house === 7 ? 'bg-orange-700' :
            'bg-amber-700'
          }`}>
            <AlertTriangle className="w-4 h-4" />
            <span>{isHi ? 'मांगलिक दोष — स्त्री-जातक (अध्याय 11)' : 'Mangal Dosha — Female Chart (Adh. 11)'}</span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm leading-relaxed text-foreground">
              {isHi ? data.female_mangal_note_hi : data.female_mangal_note_en}
            </p>
          </div>
        </div>
      )}

      {/* Detected Yogas */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Heart className="w-4 h-4" />
          <span>{t('auto.detectedYogas')}</span>
          <span className="ml-auto text-[12px] font-normal opacity-80">{data.yogas_detected.length}</span>
        </div>
        {data.yogas_detected.length === 0 ? (
          <div className="px-4 py-3 text-sm text-muted-foreground">{t('auto.noStriJatakaYogas')}</div>
        ) : (
          <div className="p-3 grid grid-cols-1 md:grid-cols-2 gap-3">
            {data.yogas_detected.map((y) => {
              const name = isHi ? y.name_hi : y.name_en;
              const effect = isHi ? y.effect_hi : y.effect_en;
              const sev = severityStyles[y.severity] || severityStyles.moderate;
              const sevLabel = isHi ? sev.label_hi : sev.label_en;
              return (
                <div key={y.key} className="rounded-lg border border-border p-3">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <div>
                      <p className="text-sm font-semibold text-foreground">{name}</p>
                      {!isHi && y.name_hi && <p className="text-[10px] text-muted-foreground">{y.name_hi}</p>}
                    </div>
                    <span className={`shrink-0 text-[10px] font-semibold px-1.5 py-0.5 rounded ${sev.badge}`}>
                      {sevLabel}
                    </span>
                  </div>
                  <p className="text-xs text-foreground/80 leading-relaxed mb-2">{effect}</p>
                  {y.supporting_factors && y.supporting_factors.length > 0 && (
                    <ul className="space-y-0.5 mb-2">
                      {y.supporting_factors.map((f, i) => (
                        <li key={i} className="text-xs text-foreground/70 flex items-start gap-1.5">
                          <span className="text-sacred-gold-dark mt-0.5">•</span>
                          <span>{f}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                  <div className="flex items-center gap-1.5 pt-2 border-t border-border text-[11px] text-muted-foreground">
                    <BookOpen className="w-3 h-3" />
                    <span className="italic">{y.sloka_ref}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Recommendations */}
      {recs.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <CheckCircle2 className="w-4 h-4" />
            <span>{t('auto.recommendations')}</span>
          </div>
          <div className="px-4 py-3">
            <ul className="space-y-1.5">
              {recs.map((r, i) => (
                <li key={i} className="text-sm text-foreground/90 flex items-start gap-2">
                  <span className="text-sacred-gold-dark mt-0.5">•</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Sloka footer */}
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground italic border-t border-border pt-3">
        <BookOpen className="w-3 h-3" />
        <span>{data.sloka_ref}</span>
      </div>
    </div>
  );
}
