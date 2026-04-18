import { useState, useEffect } from 'react';
import { Loader2, Baby, BookOpen, Heart, Sparkles, Calendar, Eye, ShieldAlert, Clock, Users } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface ApatyaYoga {
  key: string;
  name_en: string;
  name_hi: string;
  effect_en: string;
  effect_hi: string;
  probability: 'high' | 'moderate' | 'low';
  sloka_ref: string;
  supporting_factors?: string[];
}

interface FifthHouseAnalysis {
  fifth_lord: string;
  fifth_lord_placement: number;
  fifth_lord_sign: string;
  fifth_lord_strength: string;
  fifth_sign: string;
  jupiter_placement: number;
  jupiter_sign: string;
  jupiter_strength: string;
  planets_in_5th: string[];
  benefics_in_5th: string[];
  malefics_in_5th: string[];
  interpretation_en: string;
  interpretation_hi: string;
}

interface DashaPlanet {
  planet: string;
  role_en: string;
  role_hi: string;
  favorable: boolean;
  reason_en: string;
  reason_hi: string;
}

interface TransitTrigger {
  planet: string;
  watch_sign: string;
  house_ref: number | null;
  trigger_en: string;
  trigger_hi: string;
  significance_en: string;
  significance_hi: string;
}

interface ChildrenTiming {
  favorable_dasha_planets: DashaPlanet[];
  transit_triggers: TransitTrigger[];
  summary_en: string;
  summary_hi: string;
  sloka_ref: string;
}

interface ChildCountEstimate {
  point_estimate: number;
  count_low: number;
  count_high: number;
  label_en: string;
  label_hi: string;
  method_en: string;
  method_hi: string;
  supporting_factors: string[];
  sloka_ref: string;
}

interface GenderYoga {
  key: string;
  name_en: string;
  name_hi: string;
  effect_en: string;
  effect_hi: string;
  severity: string;
  sloka_ref: string;
}

interface GenderAnalysis {
  dominant_gender: string;
  male_score: number;
  female_score: number;
  yogas: GenderYoga[];
  rationale_en: string;
  rationale_hi: string;
  sloka_ref: string;
}

interface FecundityScore {
  score: number;
  band: string;
  band_hi: string;
  components: Record<string, number>;
  max_score: number;
  sloka_ref: string;
}

interface AdoptionReason {
  reason_en: string;
  reason_hi: string;
}

interface AdoptionIndicators {
  indicated: boolean;
  strength: 'strong' | 'moderate' | 'none';
  reasons: AdoptionReason[];
  sloka_ref: string;
}

interface ChildGenderReasons {
  reason_en: string;
  reason_hi: string;
}

interface FemaleChildYogas {
  indicated: boolean;
  reasons: ChildGenderReasons[];
  sloka_ref: string;
}

interface MaleChildYogas {
  indicated: boolean;
  reasons: ChildGenderReasons[];
  sloka_ref: string;
}

interface ConceptionWindow {
  period_en: string;
  period_hi: string;
  jupiter_position: string;
  type: 'transit' | 'dasha';
}

interface ConceptionTiming {
  favorable_windows: ConceptionWindow[];
  current_favorable: boolean;
  note_en: string;
  note_hi: string;
  sloka_ref: string;
}

interface DeliveryIndicators {
  method_en: string;
  method_hi: string;
  estimated_months_range: string;
  note_en: string;
  note_hi: string;
  sloka_ref: string;
}

interface ChildLossYoga {
  key: string;
  name_en: string;
  name_hi: string;
  description_en: string;
  description_hi: string;
  severity: 'high' | 'moderate_high' | 'moderate';
}

interface ChildLossYogas {
  present: boolean;
  overall_risk: 'very_high' | 'high' | 'moderate' | 'none';
  yogas: ChildLossYoga[];
  note_en: string;
  note_hi: string;
  sloka_ref: string;
}

interface ApatyaData {
  fifth_house_analysis: FifthHouseAnalysis;
  yogas_detected: ApatyaYoga[];
  progeny_prospect: 'favorable' | 'challenging' | 'mixed';
  children_timing?: ChildrenTiming;
  child_count_estimate?: ChildCountEstimate | null;
  gender_analysis?: GenderAnalysis | null;
  fecundity_score?: FecundityScore | null;
  // Sprint F — advanced analysis
  adoption_indicators?: AdoptionIndicators | null;
  female_child_yogas?: FemaleChildYogas | null;
  male_child_yogas?: MaleChildYogas | null;
  conception_timing?: ConceptionTiming | null;
  delivery_indicators?: DeliveryIndicators | null;
  child_loss_yogas?: ChildLossYogas | null;
  recommendations_en: string[];
  recommendations_hi: string[];
  remedies_en: string[];
  remedies_hi: string[];
  sloka_ref: string;
  kundli_id?: string;
  person_name?: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const PROBABILITY_STYLES: Record<string, string> = {
  high: 'bg-emerald-100 text-emerald-800 border-emerald-300',
  moderate: 'bg-amber-100 text-amber-800 border-amber-300',
  low: 'bg-red-100 text-red-800 border-red-300',
};

const PROSPECT_STYLES: Record<string, { bg: string; border: string; text: string }> = {
  favorable: { bg: 'bg-emerald-50', border: 'border-emerald-300', text: 'text-emerald-900' },
  challenging: { bg: 'bg-red-50', border: 'border-red-300', text: 'text-red-900' },
  mixed: { bg: 'bg-amber-50', border: 'border-amber-300', text: 'text-amber-900' },
};

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'बृहस्पति', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const SEVERITY_STYLES: Record<string, string> = {
  high: 'bg-red-100 text-red-800 border-red-300',
  moderate_high: 'bg-orange-100 text-orange-800 border-orange-300',
  moderate: 'bg-amber-100 text-amber-800 border-amber-300',
};

const RISK_LABEL: Record<string, { en: string; hi: string }> = {
  very_high: { en: 'Very High Risk', hi: 'अत्यंत उच्च जोखिम' },
  high: { en: 'High Risk', hi: 'उच्च जोखिम' },
  moderate: { en: 'Moderate Risk', hi: 'मध्यम जोखिम' },
  none: { en: 'No Risk', hi: 'कोई जोखिम नहीं' },
};

export default function ApatyaTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<ApatyaData | null>(null);
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
        const res = await api.get<ApatyaData>(`/api/kundli/${kundliId}/apatya`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Apatya analysis');
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
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
    );
  }

  if (!data) return null;

  const fifth = data.fifth_house_analysis;
  const prospectStyle = PROSPECT_STYLES[data.progeny_prospect] || PROSPECT_STYLES.mixed;
  const recs = isHi ? data.recommendations_hi : data.recommendations_en;
  const rems = isHi ? data.remedies_hi : data.remedies_en;
  const pName = (p: string) => isHi ? (PLANET_HI[p] || p) : p;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Baby className="w-6 h-6" />
          {t('auto.apatya')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.apatyaDesc')}</p>
      </div>

      {/* Prospect banner */}
      <div className={`p-4 rounded-xl border ${prospectStyle.bg} ${prospectStyle.border} ${prospectStyle.text} flex items-start gap-3`}>
        <Heart className="w-5 h-5 shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold capitalize">
            {t('auto.progenyProspect')}: {isHi ? translateProspectHi(data.progeny_prospect) : data.progeny_prospect}
          </p>
          <p className="text-sm mt-0.5">
            {data.yogas_detected.length} {data.yogas_detected.length === 1 ? 'yoga' : 'yogas'}{' '}
            {t('auto.detected')}
          </p>
        </div>
      </div>

      {/* Fifth house analysis card */}
      <div className="p-5 rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm">
        <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('auto.fifthHouseAnalysis')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm mb-3">
          <div>
            <span className="text-muted-foreground">{t('auto.fifthLord')}: </span>
            <span className="font-semibold">
              {fifth.fifth_lord || '—'}{' '}
              {fifth.fifth_lord_placement > 0 && `(${t('auto.house')} ${fifth.fifth_lord_placement})`}
            </span>
          </div>
          <div>
            <span className="text-muted-foreground">{t('auto.jupiter')}: </span>
            <span className="font-semibold">
              {fifth.jupiter_sign || '—'}{' '}
              {fifth.jupiter_placement > 0 && `(${t('auto.house')} ${fifth.jupiter_placement})`}
            </span>
          </div>
          <div>
            <span className="text-muted-foreground">{t('auto.fifthLordStrength')}: </span>
            <span className="font-semibold capitalize">{fifth.fifth_lord_strength}</span>
          </div>
          <div>
            <span className="text-muted-foreground">{t('auto.jupiterStrength')}: </span>
            <span className="font-semibold capitalize">{fifth.jupiter_strength}</span>
          </div>
        </div>
        {fifth.benefics_in_5th.length > 0 && (
          <div className="text-sm mb-1">
            <span className="text-muted-foreground">{t('auto.beneficsIn5th')}: </span>
            <span className="text-emerald-700 font-medium">{fifth.benefics_in_5th.join(', ')}</span>
          </div>
        )}
        {fifth.malefics_in_5th.length > 0 && (
          <div className="text-sm mb-3">
            <span className="text-muted-foreground">{t('auto.maleficsIn5th')}: </span>
            <span className="text-red-700 font-medium">{fifth.malefics_in_5th.join(', ')}</span>
          </div>
        )}
        <p className="text-sm text-foreground/80 leading-relaxed mt-2">
          {isHi ? fifth.interpretation_hi : fifth.interpretation_en}
        </p>
      </div>

      {/* Yogas detected */}
      {data.yogas_detected.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.yogas_detected.map((yoga) => {
            const name = isHi ? yoga.name_hi : yoga.name_en;
            const effect = isHi ? yoga.effect_hi : yoga.effect_en;
            const probLabel = t(`auto.probability${cap(yoga.probability)}`);
            return (
              <div key={yoga.key} className="p-5 rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm">
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <h3 className="text-lg font-bold text-sacred-gold-dark">{name}</h3>
                    {!isHi && yoga.name_hi && (
                      <p className="text-xs text-muted-foreground">{yoga.name_hi}</p>
                    )}
                  </div>
                  <div className={`shrink-0 px-2 py-1 rounded-md text-xs font-semibold border ${PROBABILITY_STYLES[yoga.probability] || PROBABILITY_STYLES.moderate}`}>
                    {probLabel}
                  </div>
                </div>
                <p className="text-sm text-foreground leading-relaxed mb-3">{effect}</p>
                {yoga.supporting_factors && yoga.supporting_factors.length > 0 && (
                  <ul className="space-y-1 mb-3">
                    {yoga.supporting_factors.map((f, i) => (
                      <li key={i} className="text-xs text-foreground/80 flex items-start gap-1.5">
                        <span className="text-sacred-gold mt-0.5">•</span>
                        <span>{f}</span>
                      </li>
                    ))}
                  </ul>
                )}
                <div className="flex items-center gap-1.5 pt-2 border-t border-sacred-gold/15 text-[11px] text-muted-foreground">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{yoga.sloka_ref}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Children timing — dasha + transit window */}
      {data.children_timing && (
        <section className="rounded-xl border-2 border-violet-200 bg-violet-50 p-5">
          <h3 className="text-lg font-semibold text-violet-900 mb-1 flex items-center gap-2">
            <Calendar className="w-5 h-5" />
            {isHi ? 'संतान-प्राप्ति काल — दशा एवं गोचर' : 'Timing for Children — Dasha & Transit'}
          </h3>
          <p className="text-xs text-violet-700 leading-relaxed mb-4">
            {isHi ? data.children_timing.summary_hi : data.children_timing.summary_en}
          </p>

          {/* Favorable dasha planets */}
          <div className="mb-4">
            <h4 className="text-sm font-semibold text-violet-800 mb-2">
              {isHi ? 'अनुकूल दशा-ग्रह' : 'Favorable Dasha Periods'}
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {data.children_timing.favorable_dasha_planets.map((dp) => (
                <div
                  key={dp.planet}
                  className={`rounded-lg border p-3 ${dp.favorable ? 'border-emerald-200 bg-emerald-50' : 'border-red-200 bg-red-50'}`}
                >
                  <div className="flex items-center justify-between gap-2 mb-1.5">
                    <span className="font-bold text-sm text-foreground">{pName(dp.planet)}</span>
                    <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded ${dp.favorable ? 'bg-emerald-600 text-white' : 'bg-red-600 text-white'}`}>
                      {dp.favorable ? (isHi ? 'अनुकूल' : 'Favorable') : (isHi ? 'विलम्बकारक' : 'Delaying')}
                    </span>
                  </div>
                  <p className="text-[10px] text-muted-foreground italic mb-1">
                    {isHi ? dp.role_hi : dp.role_en}
                  </p>
                  <p className="text-xs text-foreground/80 leading-relaxed">
                    {isHi ? dp.reason_hi : dp.reason_en}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Jupiter transit triggers */}
          {data.children_timing.transit_triggers.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-violet-800 mb-2">
                {isHi ? 'गुरु गोचर — संकेत खिड़कियाँ' : 'Jupiter Transit Windows'}
              </h4>
              <div className="space-y-2">
                {data.children_timing.transit_triggers.map((tr, i) => (
                  <div key={i} className="rounded-lg border border-violet-200 bg-white/70 p-3">
                    <div className="flex items-start gap-2 mb-1">
                      <Eye className="w-3.5 h-3.5 shrink-0 mt-0.5 text-violet-500" />
                      <span className="text-xs font-semibold text-violet-900">
                        {isHi ? tr.trigger_hi : tr.trigger_en}
                        {tr.house_ref && (
                          <span className="ml-1.5 text-[10px] font-normal text-muted-foreground">
                            ({isHi ? `भाव ${tr.house_ref}` : `House ${tr.house_ref}`})
                          </span>
                        )}
                      </span>
                    </div>
                    <p className="text-xs text-foreground/70 leading-relaxed pl-5 italic">
                      {isHi ? tr.significance_hi : tr.significance_en}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center gap-1.5 mt-3 pt-3 border-t border-violet-200 text-[10px] text-violet-600">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.children_timing.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Sprint E — Child Count Estimate */}
      {data.child_count_estimate && (
        <section className="rounded-xl border border-blue-200 bg-blue-50 p-5">
          <h3 className="text-base font-semibold text-blue-900 mb-2 flex items-center gap-2">
            <Baby className="w-4 h-4" />
            {isHi ? 'संतान संख्या अनुमान' : 'Child Count Estimate'}
          </h3>
          <p className="text-xl font-bold text-blue-800 mb-1">
            {isHi ? data.child_count_estimate.label_hi : data.child_count_estimate.label_en}
          </p>
          <p className="text-xs text-blue-700 leading-relaxed mb-3">
            {isHi ? data.child_count_estimate.method_hi : data.child_count_estimate.method_en}
          </p>
          {data.child_count_estimate.supporting_factors.length > 0 && (
            <ul className="space-y-1 mb-3">
              {data.child_count_estimate.supporting_factors.map((f, i) => (
                <li key={i} className="text-xs text-foreground/80 flex items-start gap-1.5">
                  <span className="text-blue-500 mt-0.5">•</span>
                  <span>{f}</span>
                </li>
              ))}
            </ul>
          )}
          <div className="flex items-center gap-1.5 pt-2 border-t border-blue-200 text-[10px] text-blue-600">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.child_count_estimate.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Sprint E — Gender Analysis */}
      {data.gender_analysis && (
        <section className="rounded-xl border border-purple-200 bg-purple-50 p-5">
          <h3 className="text-base font-semibold text-purple-900 mb-2 flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            {isHi ? 'संतान लिंग विश्लेषण' : 'Gender Tendency Analysis'}
          </h3>
          {data.gender_analysis.yogas.map((yoga, i) => (
            <div key={i} className="mb-2">
              <p className="font-semibold text-sm text-purple-800">
                {isHi ? yoga.name_hi : yoga.name_en}
              </p>
              <p className="text-sm text-foreground/80 leading-relaxed">
                {isHi ? yoga.effect_hi : yoga.effect_en}
              </p>
            </div>
          ))}
          <p className="text-xs text-purple-700 italic mt-2 leading-relaxed">
            {isHi ? data.gender_analysis.rationale_hi : data.gender_analysis.rationale_en}
          </p>
          <div className="flex items-center gap-1.5 pt-2 border-t border-purple-200 text-[10px] text-purple-600 mt-3">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.gender_analysis.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Sprint E — Fecundity Score */}
      {data.fecundity_score && (
        <section className="rounded-xl border border-emerald-200 bg-emerald-50 p-5">
          <h3 className="text-base font-semibold text-emerald-900 mb-3 flex items-center gap-2">
            <Heart className="w-4 h-4" />
            {isHi ? 'प्रजनन शक्ति स्कोर' : 'Fecundity Score'}
          </h3>
          <div className="flex items-end gap-3 mb-2">
            <span className="text-4xl font-bold text-emerald-700">{data.fecundity_score.score}</span>
            <span className="text-sm text-muted-foreground mb-1">/ {data.fecundity_score.max_score}</span>
            <span className="mb-1 text-sm font-semibold text-emerald-800 capitalize">
              {isHi ? data.fecundity_score.band_hi : data.fecundity_score.band.replace(/_/g, ' ')}
            </span>
          </div>
          <div className="w-full bg-emerald-100 rounded-full h-2 mb-4">
            <div
              className="bg-emerald-500 h-2 rounded-full transition-all"
              style={{ width: `${data.fecundity_score.score}%` }}
            />
          </div>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-foreground/70 mb-3">
            {Object.entries(data.fecundity_score.components).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="capitalize">{k.replace(/_/g, ' ')}</span>
                <span className="font-semibold text-emerald-700">{v}</span>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-1.5 pt-2 border-t border-emerald-200 text-[10px] text-emerald-600">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.fecundity_score.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Sprint F — Gender of Children (male + female yogas side by side) */}
      {(data.female_child_yogas?.indicated || data.male_child_yogas?.indicated) && (
        <section className="rounded-xl border border-pink-200 bg-pink-50 p-5">
          <h3 className="text-base font-semibold text-pink-900 mb-3 flex items-center gap-2">
            <Users className="w-4 h-4" />
            {isHi ? 'संतान लिंग योग' : 'Gender of Children Yogas'}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Female yogas */}
            {data.female_child_yogas?.indicated && (
              <div className="rounded-lg border border-pink-300 bg-white/70 p-4">
                <p className="text-sm font-semibold text-pink-800 mb-2">
                  {isHi ? 'कन्या संतान योग' : 'Female Children Yoga'}
                </p>
                <ul className="space-y-2">
                  {data.female_child_yogas.reasons.map((r, i) => (
                    <li key={i} className="text-xs text-foreground/80 flex items-start gap-1.5">
                      <span className="text-pink-500 mt-0.5">•</span>
                      <span>{isHi ? r.reason_hi : r.reason_en}</span>
                    </li>
                  ))}
                </ul>
                <div className="flex items-center gap-1.5 mt-3 pt-2 border-t border-pink-200 text-[10px] text-pink-600">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{data.female_child_yogas.sloka_ref}</span>
                </div>
              </div>
            )}
            {/* Male yogas */}
            {data.male_child_yogas?.indicated && (
              <div className="rounded-lg border border-blue-300 bg-white/70 p-4">
                <p className="text-sm font-semibold text-blue-800 mb-2">
                  {isHi ? 'पुत्र संतान योग' : 'Male Children Yoga'}
                </p>
                <ul className="space-y-2">
                  {data.male_child_yogas.reasons.map((r, i) => (
                    <li key={i} className="text-xs text-foreground/80 flex items-start gap-1.5">
                      <span className="text-blue-500 mt-0.5">•</span>
                      <span>{isHi ? r.reason_hi : r.reason_en}</span>
                    </li>
                  ))}
                </ul>
                <div className="flex items-center gap-1.5 mt-3 pt-2 border-t border-blue-200 text-[10px] text-blue-600">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{data.male_child_yogas.sloka_ref}</span>
                </div>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Sprint F — Adoption Indicators (shown only when indicated or strength != none) */}
      {data.adoption_indicators && data.adoption_indicators.strength !== 'none' && (
        <section className="rounded-xl border border-amber-200 bg-amber-50 p-5">
          <h3 className="text-base font-semibold text-amber-900 mb-3 flex items-center gap-2">
            <Heart className="w-4 h-4" />
            {isHi ? 'दत्तक संतान संकेत' : 'Adoption Indicators'}
            <span className={`ml-auto text-xs font-semibold px-2 py-0.5 rounded border ${
              data.adoption_indicators.strength === 'strong'
                ? 'bg-orange-100 text-orange-800 border-orange-300'
                : 'bg-amber-100 text-amber-800 border-amber-300'
            }`}>
              {data.adoption_indicators.strength === 'strong'
                ? (isHi ? 'प्रबल' : 'Strong')
                : (isHi ? 'मध्यम' : 'Moderate')}
            </span>
          </h3>
          <ul className="space-y-2 mb-3">
            {data.adoption_indicators.reasons.map((r, i) => (
              <li key={i} className="text-sm text-foreground/80 flex items-start gap-2">
                <span className="text-amber-600 mt-0.5">•</span>
                <span>{isHi ? r.reason_hi : r.reason_en}</span>
              </li>
            ))}
          </ul>
          <div className="flex items-center gap-1.5 pt-2 border-t border-amber-200 text-[10px] text-amber-700">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.adoption_indicators.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Sprint F — Conception Timing */}
      {data.conception_timing && data.conception_timing.favorable_windows.length > 0 && (
        <section className="rounded-xl border border-teal-200 bg-teal-50 p-5">
          <h3 className="text-base font-semibold text-teal-900 mb-3 flex items-center gap-2">
            <Clock className="w-4 h-4" />
            {isHi ? 'गर्भधारण अनुकूल काल' : 'Conception Timing Windows'}
          </h3>
          <p className="text-xs text-teal-700 leading-relaxed mb-4">
            {isHi ? data.conception_timing.note_hi : data.conception_timing.note_en}
          </p>
          <div className="space-y-2 mb-3">
            {data.conception_timing.favorable_windows.map((w, i) => (
              <div key={i} className={`rounded-lg border p-3 flex items-start gap-2 ${
                w.type === 'dasha'
                  ? 'border-violet-200 bg-violet-50/80'
                  : 'border-teal-200 bg-white/70'
              }`}>
                <span className={`shrink-0 text-[10px] font-bold px-1.5 py-0.5 rounded mt-0.5 ${
                  w.type === 'dasha'
                    ? 'bg-violet-600 text-white'
                    : 'bg-teal-600 text-white'
                }`}>
                  {w.type === 'dasha' ? (isHi ? 'दशा' : 'DASHA') : (isHi ? 'गोचर' : 'TRANSIT')}
                </span>
                <div>
                  <p className="text-xs font-medium text-foreground leading-snug">
                    {isHi ? w.period_hi : w.period_en}
                  </p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">
                    {isHi ? 'गुरु स्थिति:' : 'Jupiter:'} {w.jupiter_position}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-1.5 pt-2 border-t border-teal-200 text-[10px] text-teal-600">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.conception_timing.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Sprint F — Delivery Notes */}
      {data.delivery_indicators && (
        <section className="rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFFBF0] to-white p-5">
          <h3 className="text-base font-semibold text-sacred-gold-dark mb-2 flex items-center gap-2">
            <Baby className="w-4 h-4" />
            {isHi ? 'प्रसव काल — शास्त्रीय विधि' : 'Delivery Timing — Classical Method'}
            <span className="ml-auto text-xs font-medium bg-sacred-gold/10 text-sacred-gold-dark border border-sacred-gold/30 px-2 py-0.5 rounded">
              {data.delivery_indicators.estimated_months_range} {isHi ? 'माह' : 'months'}
            </span>
          </h3>
          <p className="text-sm text-foreground/80 leading-relaxed mb-3">
            {isHi ? data.delivery_indicators.method_hi : data.delivery_indicators.method_en}
          </p>
          <p className="text-xs text-muted-foreground leading-relaxed italic mb-3">
            {isHi ? data.delivery_indicators.note_hi : data.delivery_indicators.note_en}
          </p>
          <div className="flex items-center gap-1.5 pt-2 border-t border-sacred-gold/15 text-[10px] text-muted-foreground">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.delivery_indicators.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Sprint F — Child Loss Yogas (complete) */}
      {data.child_loss_yogas?.present && (
        <section className={`rounded-xl border-2 p-5 ${
          data.child_loss_yogas.overall_risk === 'very_high' || data.child_loss_yogas.overall_risk === 'high'
            ? 'border-red-300 bg-red-50'
            : 'border-orange-200 bg-orange-50'
        }`}>
          <div className="flex items-center justify-between mb-3">
            <h3 className={`text-base font-semibold flex items-center gap-2 ${
              data.child_loss_yogas.overall_risk === 'very_high' || data.child_loss_yogas.overall_risk === 'high'
                ? 'text-red-900'
                : 'text-orange-900'
            }`}>
              <ShieldAlert className="w-4 h-4" />
              {isHi ? 'संतान-हानि योग' : 'Child Loss Yogas'}
            </h3>
            <span className={`text-xs font-bold px-2 py-1 rounded border ${
              data.child_loss_yogas.overall_risk === 'very_high'
                ? 'bg-red-200 text-red-900 border-red-400'
                : data.child_loss_yogas.overall_risk === 'high'
                  ? 'bg-red-100 text-red-800 border-red-300'
                  : 'bg-orange-100 text-orange-800 border-orange-300'
            }`}>
              {isHi
                ? RISK_LABEL[data.child_loss_yogas.overall_risk]?.hi
                : RISK_LABEL[data.child_loss_yogas.overall_risk]?.en}
            </span>
          </div>
          <div className="space-y-3 mb-3">
            {data.child_loss_yogas.yogas.map((yoga, i) => (
              <div key={i} className="rounded-lg border bg-white/70 p-3">
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <p className="text-sm font-semibold text-foreground">
                    {isHi ? yoga.name_hi : yoga.name_en}
                  </p>
                  <span className={`shrink-0 text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${SEVERITY_STYLES[yoga.severity] || SEVERITY_STYLES.moderate}`}>
                    {yoga.severity === 'high' ? (isHi ? 'उच्च' : 'High')
                      : yoga.severity === 'moderate_high' ? (isHi ? 'मध्यम-उच्च' : 'Mod-High')
                      : (isHi ? 'मध्यम' : 'Moderate')}
                  </span>
                </div>
                <p className="text-xs text-foreground/80 leading-relaxed">
                  {isHi ? yoga.description_hi : yoga.description_en}
                </p>
              </div>
            ))}
          </div>
          {(isHi ? data.child_loss_yogas.note_hi : data.child_loss_yogas.note_en) && (
            <p className="text-xs text-foreground/70 italic leading-relaxed mb-3 p-3 bg-white/60 rounded-lg border border-current/10">
              {isHi ? data.child_loss_yogas.note_hi : data.child_loss_yogas.note_en}
            </p>
          )}
          <div className="flex items-center gap-1.5 pt-2 border-t border-red-200 text-[10px] text-red-600">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.child_loss_yogas.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Recommendations */}
      {recs.length > 0 && (
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-white shadow-sm">
          <h3 className="text-base font-bold text-sacred-gold-dark mb-2">
            {t('auto.apatyaRecommendations')}
          </h3>
          <ul className="space-y-1.5">
            {recs.map((r, i) => (
              <li key={i} className="text-sm text-foreground/80 flex items-start gap-2">
                <span className="text-sacred-gold mt-0.5">•</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Remedies */}
      {rems.length > 0 && (
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-amber-50 to-white shadow-sm">
          <h3 className="text-base font-bold text-sacred-gold-dark mb-2">
            {t('auto.apatyaRemedies')}
          </h3>
          <ul className="space-y-1.5">
            {rems.map((r, i) => (
              <li key={i} className="text-sm text-foreground/80 flex items-start gap-2">
                <span className="text-sacred-gold mt-0.5">•</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Sloka ref footer */}
      <div className="flex items-center gap-1.5 pt-2 text-xs text-muted-foreground italic">
        <BookOpen className="w-3 h-3" />
        {data.sloka_ref}
      </div>
    </div>
  );
}

function cap(s: string): string {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
}

function translateProspectHi(p: string): string {
  switch (p) {
    case 'favorable': return 'अनुकूल';
    case 'challenging': return 'कठिन';
    case 'mixed': return 'मिश्रित';
    default: return p;
  }
}
