import { useState, useEffect } from 'react';
import { Loader2, Info, BookOpen, Heart, Clock3, Moon as MoonIcon, Sparkles, Eye, Activity, AlertTriangle, Star, TrendingUp, CheckCircle2, XCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface MarakaPlanet {
  planet: string;
  role: string;
  role_hi?: string;
  placement: number;
  strength: 'strong' | 'moderate' | 'weak' | 'unknown';
  notes_en: string;
  notes_hi: string;
}

interface EighthHouseAnalysis {
  eighth_lord: string;
  eighth_lord_placement: number;
  eighth_lord_strength: string;
  planets_in_8th: string[];
  interpretation_en: string;
  interpretation_hi: string;
}

interface SaturnAssessment {
  saturn_placement: number;
  saturn_sign?: string;
  saturn_strength: string;
  interpretation_en: string;
  interpretation_hi: string;
}

interface TransitTimingIndicator {
  planet_transit: string;
  target_sign: string;
  target_house: number;
  significance_en: string;
  significance_hi: string;
  watch_period_en: string;
  watch_period_hi: string;
  intensity: 'high' | 'moderate' | 'low';
}

interface TransitTimingSection {
  indicators: TransitTimingIndicator[];
  summary_en: string;
  summary_hi: string;
  sloka_ref: string;
}

interface DashaSignal {
  dasha: string;
  lord: string;
  role: string;
  en: string;
  hi: string;
}

interface DashaGochara {
  signals: DashaSignal[];
  convergence: 'high' | 'moderate' | 'low';
  summary_en: string;
  summary_hi: string;
  mahadasha_lord?: string;
  antardasha_lord?: string;
}

// Feature 1: Saturn Transit Death Indicator
interface SaturnTransitDeathIndicator {
  current_saturn_house_from_moon: number;
  is_8th_from_moon: boolean;
  saturn_8th_lord_transit: boolean;
  eighth_lord: string;
  eighth_lord_sign: string;
  moon_house: number;
  saturn_house: number;
  interpretation_en: string;
  interpretation_hi: string;
  severity: 'high' | 'moderate' | 'low';
  sloka_ref: string;
}

// Feature 2: Moon Transit at Death
interface MoonDeathTransit {
  janma_nakshatra: string;
  watch_for_en: string;
  watch_for_hi: string;
  note_en: string;
  note_hi: string;
  sloka_ref: string;
}

// Feature 3: Classical Demise Timing
interface DemiseTimingClassical {
  likely_month_indicator: {
    sign: string;
    month_name_en: string;
    month_name_hi: string;
    planet: string;
    reason_en: string;
    reason_hi: string;
  };
  likely_lagna_at_death: {
    sign: string;
    reason_en: string;
    reason_hi: string;
  };
  disclaimer_en: string;
  disclaimer_hi: string;
  sloka_ref: string;
}

// Feature 4: Dasha + Gochara + Lagna Score
interface DashaGochaScoreSignal {
  signal_en: string;
  signal_hi: string;
  points: number;
  triggered: boolean;
}

interface DashaGochaLagnaScore {
  total: number;
  signals: DashaGochaScoreSignal[];
  verdict_en: string;
  verdict_hi: string;
  disclaimer_en: string;
  sloka_ref: string;
}

// Feature 6: Lucky Time Estimate
interface LuckyPeriod {
  period_type: 'dasha' | 'transit';
  description_en: string;
  description_hi: string;
  approximate_age_range: string;
  quality: 'excellent' | 'good' | 'neutral' | 'challenging';
}

interface LuckyTimeEstimate {
  peak_periods: LuckyPeriod[];
  current_period_quality: 'excellent' | 'good' | 'neutral' | 'challenging';
  current_mahadasha: string;
  sloka_ref: string;
}

interface ApiResponse {
  kundli_id?: string;
  person_name?: string;
  overall_longevity_strength: 'strong' | 'moderate' | 'weak';
  maraka_planets: MarakaPlanet[];
  eighth_house_analysis: EighthHouseAnalysis;
  saturn_longevity_assessment: SaturnAssessment;
  karmic_transitions_en: string;
  karmic_transitions_hi: string;
  life_chapters_en: string[];
  life_chapters_hi: string[];
  transit_timing_indicators?: TransitTimingSection;
  dasha_gochara_timing?: DashaGochara;
  // New features
  saturn_transit_death_indicator?: SaturnTransitDeathIndicator;
  moon_death_transit?: MoonDeathTransit;
  demise_timing_classical?: DemiseTimingClassical;
  dasha_gochara_lagna_score?: DashaGochaLagnaScore;
  lucky_time_estimate?: LuckyTimeEstimate;
  region_after_death?: {
    region_en: string;
    region_hi: string;
    narrative_en: string;
    narrative_hi: string;
    indicators: string[];
    sloka_ref: string;
  };
  sloka_ref: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'बृहस्पति', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const STRENGTH_STYLE: Record<string, { card: string; badge: string; key: string }> = {
  strong:   { card: 'border-emerald-300 bg-emerald-50', badge: 'bg-emerald-600 text-white', key: 'auto.longevityStrong' },
  moderate: { card: 'border-sacred-gold/30 bg-sacred-gold/5', badge: 'bg-sacred-gold-dark text-white', key: 'auto.longevityModerate' },
  weak:     { card: 'border-amber-300 bg-amber-50', badge: 'bg-amber-600 text-white', key: 'auto.longevityWeak' },
};

const INTENSITY_STYLE: Record<string, { card: string; badge: string; label: string; labelHi: string }> = {
  high:     { card: 'border-red-200 bg-red-50',    badge: 'bg-red-600 text-white',    label: 'High',     labelHi: 'उच्च' },
  moderate: { card: 'border-amber-200 bg-amber-50', badge: 'bg-amber-500 text-white', label: 'Moderate', labelHi: 'मध्यम' },
  low:      { card: 'border-blue-200 bg-blue-50',   badge: 'bg-blue-500 text-white',  label: 'Low',      labelHi: 'निम्न' },
};

export default function LongevityTab({ kundliId, language, t }: Props) {
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
        const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/longevity-indicators`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load longevity indicators');
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

  const overallStyle = STRENGTH_STYLE[data.overall_longevity_strength] || STRENGTH_STYLE.moderate;
  const planetName = (p: string) => (isHi ? (PLANET_HI[p] || p) : p);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Clock3 className="w-6 h-6" />
          {t('auto.longevity')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.longevityDesc')}</p>
      </div>

      {/* Disclaimer banner */}
      <div className="rounded-lg border-2 border-blue-300 bg-blue-50 p-4 flex items-start gap-3">
        <Info className="w-5 h-5 text-blue-700 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-blue-900 leading-relaxed">
          {t('auto.longevityDisclaimer')}
        </p>
      </div>

      {/* Overall strength card */}
      <div className={`rounded-xl border-2 p-5 ${overallStyle.card}`}>
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Heart className="w-5 h-5" />
            <h3 className="font-semibold text-foreground">
              {t('auto.overallLongevityStrength')}
            </h3>
          </div>
          <span className={`text-xs font-semibold uppercase tracking-wider px-3 py-1 rounded ${overallStyle.badge}`}>
            {t(overallStyle.key)}
          </span>
        </div>
      </div>

      {/* Maraka planets */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('auto.marakaPlanets')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.maraka_planets.map((m, i) => {
            const notes = isHi ? m.notes_hi : m.notes_en;
            const role = isHi && m.role_hi ? m.role_hi : m.role;
            const style = STRENGTH_STYLE[m.strength] || STRENGTH_STYLE.moderate;
            return (
              <div key={`${m.planet}-${i}`} className={`rounded-xl border-2 p-4 ${style.card}`}>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <h4 className="font-bold text-foreground">{planetName(m.planet)}</h4>
                    <div className="text-xs text-muted-foreground">{role}</div>
                  </div>
                  <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded ${style.badge}`}>
                    {t(style.key)}
                  </span>
                </div>
                <p className="text-xs text-foreground/80 leading-relaxed">{notes}</p>
              </div>
            );
          })}
          {data.maraka_planets.length === 0 && (
            <div className="md:col-span-2 p-4 rounded-lg bg-gray-50 border border-gray-200 text-sm text-gray-600 italic">
              {t('auto.marakaDataNotAvailable')}
            </div>
          )}
        </div>
      </section>

      {/* 8th house + Saturn side-by-side */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
          <h3 className="font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <MoonIcon className="w-5 h-5" />
            {t('auto.eighthHouseAnalysis')}
          </h3>
          <div className="text-xs text-muted-foreground mb-2">
            {t('auto.eighthLord')}:{' '}
            <span className="font-semibold text-foreground">
              {data.eighth_house_analysis.eighth_lord
                ? planetName(data.eighth_house_analysis.eighth_lord)
                : '—'}
            </span>
            {data.eighth_house_analysis.eighth_lord_placement > 0 && (
              <span className="ml-1">
                ({t('auto.bhavaShort')} {data.eighth_house_analysis.eighth_lord_placement})
              </span>
            )}
          </div>
          {data.eighth_house_analysis.planets_in_8th.length > 0 && (
            <div className="text-xs text-muted-foreground mb-3">
              {t('auto.planetsIn8th')}:{' '}
              <span className="text-foreground">
                {data.eighth_house_analysis.planets_in_8th.map(planetName).join(', ')}
              </span>
            </div>
          )}
          <p className="text-sm text-foreground/90 leading-relaxed">
            {isHi ? data.eighth_house_analysis.interpretation_hi : data.eighth_house_analysis.interpretation_en}
          </p>
        </div>

        <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
          <h3 className="font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <Clock3 className="w-5 h-5" />
            {t('auto.saturnLongevity')}
          </h3>
          <div className="text-xs text-muted-foreground mb-3">
            {t('auto.placement')}:{' '}
            <span className="font-semibold text-foreground">
              {data.saturn_longevity_assessment.saturn_placement > 0
                ? `${t('auto.bhavaShort')} ${data.saturn_longevity_assessment.saturn_placement}`
                : '—'}
            </span>
            {data.saturn_longevity_assessment.saturn_sign && (
              <span className="ml-2">({data.saturn_longevity_assessment.saturn_sign})</span>
            )}
          </div>
          <p className="text-sm text-foreground/90 leading-relaxed">
            {isHi
              ? data.saturn_longevity_assessment.interpretation_hi
              : data.saturn_longevity_assessment.interpretation_en}
          </p>
        </div>
      </section>

      {/* Transit timing indicators (death timing — Phaladeepika Adh. 17) */}
      {data.transit_timing_indicators && data.transit_timing_indicators.indicators.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold text-sacred-gold-dark mb-1 flex items-center gap-2">
            <Activity className="w-5 h-5" />
            {isHi ? 'कर्म-संक्रमण गोचर संकेत' : 'Karmic Transition Transit Markers'}
          </h3>
          <p className="text-xs text-muted-foreground mb-3">
            {isHi
              ? data.transit_timing_indicators.summary_hi
              : data.transit_timing_indicators.summary_en}
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.transit_timing_indicators.indicators.map((ind, i) => {
              const style = INTENSITY_STYLE[ind.intensity] || INTENSITY_STYLE.moderate;
              return (
                <div key={i} className={`rounded-xl border-2 p-4 ${style.card}`}>
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div>
                      <h4 className="font-bold text-foreground text-sm">
                        {planetName(ind.planet_transit)}
                        <span className="font-normal text-muted-foreground ml-1">→</span>
                        <span className="ml-1">{ind.target_sign}</span>
                      </h4>
                      <div className="text-[10px] text-muted-foreground uppercase tracking-wide mt-0.5">
                        {isHi ? `भाव ${ind.target_house}` : `House ${ind.target_house}`}
                      </div>
                    </div>
                    <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded shrink-0 ${style.badge}`}>
                      {isHi ? style.labelHi : style.label}
                    </span>
                  </div>
                  <p className="text-xs text-foreground/80 leading-relaxed mb-2">
                    {isHi ? ind.significance_hi : ind.significance_en}
                  </p>
                  <div className="rounded-lg bg-white/60 border border-current/10 px-3 py-2 flex items-start gap-2 text-xs">
                    <Eye className="w-3.5 h-3.5 shrink-0 mt-0.5 text-muted-foreground" />
                    <span className="text-foreground/70 italic leading-relaxed">
                      {isHi ? ind.watch_period_hi : ind.watch_period_en}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
          <div className="flex items-center gap-1.5 mt-3 text-[10px] text-muted-foreground">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{data.transit_timing_indicators.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Dasha–Lagna Multi-Signal Analysis */}
      {data.dasha_gochara_timing && (
        <section className="rounded-xl border-2 border-indigo-200 bg-indigo-50 p-5">
          <h3 className="font-semibold text-indigo-900 mb-1 flex items-center gap-2">
            <Activity className="w-5 h-5" />
            {isHi ? 'दशा–लग्न बहु-संकेत विश्लेषण' : 'Dasha–Lagna Multi-Signal Analysis'}
          </h3>
          {data.dasha_gochara_timing.mahadasha_lord && (
            <p className="text-xs text-indigo-700 mb-3">
              {isHi ? 'महादशा' : 'Mahadasha'}: <strong>{data.dasha_gochara_timing.mahadasha_lord}</strong>
              {data.dasha_gochara_timing.antardasha_lord && (
                <> · {isHi ? 'अन्तर्दशा' : 'Antardasha'}: <strong>{data.dasha_gochara_timing.antardasha_lord}</strong></>
              )}
              {' '}
              <span className={`ml-2 px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                data.dasha_gochara_timing.convergence === 'high' ? 'bg-red-100 text-red-800' :
                data.dasha_gochara_timing.convergence === 'moderate' ? 'bg-amber-100 text-amber-800' :
                'bg-blue-100 text-blue-800'
              }`}>
                {data.dasha_gochara_timing.convergence === 'high' ? (isHi ? 'उच्च संरेखण' : 'High Convergence') :
                 data.dasha_gochara_timing.convergence === 'moderate' ? (isHi ? 'मध्यम संरेखण' : 'Moderate Convergence') :
                 (isHi ? 'निम्न संरेखण' : 'Low Convergence')}
              </span>
            </p>
          )}
          <p className="text-sm text-indigo-900/90 leading-relaxed mb-3">
            {isHi ? data.dasha_gochara_timing.summary_hi : data.dasha_gochara_timing.summary_en}
          </p>
          {data.dasha_gochara_timing.signals.length > 0 && (
            <div className="space-y-2">
              {data.dasha_gochara_timing.signals.map((sig, i) => (
                <div key={i} className="rounded-lg bg-white/70 border border-indigo-100 px-3 py-2 text-xs text-indigo-800">
                  <span className="font-semibold">{sig.dasha} ({sig.lord})</span>: {isHi ? sig.hi : sig.en}
                </div>
              ))}
            </div>
          )}
          <p className="text-[10px] text-indigo-500 italic mt-3">
            {isHi
              ? 'यह विश्लेषण शास्त्रीय दृष्टिकोण है — कोई विशिष्ट आयु-भविष्यवाणी नहीं।'
              : 'This is classical philosophical framing — no specific age or date prediction is made.'}
          </p>
        </section>
      )}

      {/* ── Feature 4: Combined Death Risk Score ─────────────────── */}
      {data.dasha_gochara_lagna_score && (
        <section className="rounded-xl border-2 border-orange-200 bg-orange-50 p-5">
          <div className="flex items-start justify-between gap-3 mb-1">
            <h3 className="font-semibold text-orange-900 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              {isHi ? 'मृत्यु-काल बहु-संकेत अंक (अ. 17)' : 'Combined Death Risk Score (Adh. 17)'}
            </h3>
            {/* Score gauge */}
            <div className="flex flex-col items-center shrink-0">
              <div className={`w-14 h-14 rounded-full border-4 flex items-center justify-center font-bold text-xl ${
                data.dasha_gochara_lagna_score.total >= 6
                  ? 'border-red-500 bg-red-100 text-red-800'
                  : data.dasha_gochara_lagna_score.total >= 3
                  ? 'border-orange-500 bg-orange-100 text-orange-800'
                  : 'border-green-500 bg-green-100 text-green-800'
              }`}>
                {data.dasha_gochara_lagna_score.total}
              </div>
              <span className="text-[9px] text-muted-foreground mt-0.5">/ 8</span>
            </div>
          </div>
          {/* Disclaimer banner — prominent */}
          <div className="flex items-start gap-2 rounded-lg bg-orange-100 border border-orange-300 px-3 py-2 mb-3">
            <Info className="w-4 h-4 text-orange-700 shrink-0 mt-0.5" />
            <p className="text-xs text-orange-800 leading-relaxed">
              {data.dasha_gochara_lagna_score.disclaimer_en}
            </p>
          </div>
          {/* Verdict */}
          <p className="text-sm text-orange-900/90 leading-relaxed mb-3">
            {isHi ? data.dasha_gochara_lagna_score.verdict_hi : data.dasha_gochara_lagna_score.verdict_en}
          </p>
          {/* Signal checklist */}
          <div className="space-y-2">
            {data.dasha_gochara_lagna_score.signals.map((sig, i) => (
              <div key={i} className={`flex items-start gap-2 rounded-lg px-3 py-2 text-xs ${
                sig.triggered ? 'bg-orange-100 border border-orange-200' : 'bg-white/70 border border-orange-100'
              }`}>
                {sig.triggered
                  ? <CheckCircle2 className="w-4 h-4 text-orange-700 shrink-0 mt-0.5" />
                  : <XCircle className="w-4 h-4 text-gray-400 shrink-0 mt-0.5" />
                }
                <div className="flex-1">
                  <span className={`leading-relaxed ${sig.triggered ? 'text-orange-900 font-medium' : 'text-gray-500'}`}>
                    {isHi ? sig.signal_hi : sig.signal_en}
                  </span>
                </div>
                <span className={`shrink-0 text-[10px] font-bold px-1.5 py-0.5 rounded ml-2 ${
                  sig.triggered ? 'bg-orange-600 text-white' : 'bg-gray-200 text-gray-500'
                }`}>
                  +{sig.points}
                </span>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-1.5 mt-3 text-[10px] text-orange-400 italic">
            <BookOpen className="w-3 h-3" />
            <span>{data.dasha_gochara_lagna_score.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* ── Feature 1: Saturn Transit Death Indicator ─────────────── */}
      {data.saturn_transit_death_indicator && (
        <section>
          <h3 className="text-base font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <Clock3 className="w-5 h-5" />
            {isHi ? 'शनि गोचर निधन-संकेत (अ. 17)' : 'Saturn Transit Death Indicator (Adh. 17)'}
          </h3>
          {(() => {
            const s = data.saturn_transit_death_indicator!;
            const sStyle = INTENSITY_STYLE[s.severity] || INTENSITY_STYLE.moderate;
            return (
              <div className={`rounded-xl border-2 p-4 ${sStyle.card}`}>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div className="text-sm font-medium text-foreground">
                    {isHi ? `शनि: भाव ${s.saturn_house} | चंद्र से: भाव ${s.current_saturn_house_from_moon}` : `Saturn: House ${s.saturn_house} | From Moon: House ${s.current_saturn_house_from_moon}`}
                  </div>
                  <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded shrink-0 ${sStyle.badge}`}>
                    {isHi ? sStyle.labelHi : sStyle.label}
                  </span>
                </div>
                <div className="flex gap-3 text-xs text-muted-foreground mb-2">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${s.is_8th_from_moon ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-600'}`}>
                    {isHi ? `चंद्र से 8वें में: ${s.is_8th_from_moon ? 'हाँ' : 'नहीं'}` : `8th from Moon: ${s.is_8th_from_moon ? 'Yes' : 'No'}`}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${s.saturn_8th_lord_transit ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-600'}`}>
                    {isHi ? `8वें स्वामी राशि में: ${s.saturn_8th_lord_transit ? 'हाँ' : 'नहीं'}` : `8th lord sign: ${s.saturn_8th_lord_transit ? 'Yes' : 'No'}`}
                  </span>
                </div>
                <p className="text-xs text-foreground/80 leading-relaxed">
                  {isHi ? s.interpretation_hi : s.interpretation_en}
                </p>
                <div className="flex items-center gap-1.5 mt-2 text-[10px] text-muted-foreground italic">
                  <BookOpen className="w-3 h-3" /><span>{s.sloka_ref}</span>
                </div>
              </div>
            );
          })()}
        </section>
      )}

      {/* ── Feature 2 & 3: Classical Death Timing Indicators ─────── */}
      {(data.moon_death_transit?.janma_nakshatra || data.demise_timing_classical) && (
        <section>
          <h3 className="text-base font-semibold text-sacred-gold-dark mb-1 flex items-center gap-2">
            <MoonIcon className="w-5 h-5" />
            {isHi ? 'शास्त्रीय निधन-काल संकेत (अ. 17)' : 'Classical Death Timing Indicators (Adh. 17)'}
          </h3>
          {/* Strong disclaimer */}
          <div className="rounded-lg border border-blue-300 bg-blue-50 px-3 py-2 mb-3 flex items-start gap-2">
            <Info className="w-4 h-4 text-blue-700 shrink-0 mt-0.5" />
            <p className="text-xs text-blue-800 leading-relaxed italic">
              {data.demise_timing_classical
                ? (isHi ? data.demise_timing_classical.disclaimer_hi : data.demise_timing_classical.disclaimer_en)
                : 'These are philosophical classical indicators — NOT death predictions.'}
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Feature 2: Moon transit at death */}
            {data.moon_death_transit?.janma_nakshatra && (
              <div className="rounded-xl border-2 border-indigo-200 bg-indigo-50 p-4">
                <h4 className="font-semibold text-indigo-900 text-sm mb-2 flex items-center gap-1.5">
                  <MoonIcon className="w-4 h-4" />
                  {isHi ? 'जन्म नक्षत्र संवेदनशीलता' : 'Janma Nakshatra Sensitivity'}
                </h4>
                <p className="text-xs text-indigo-700 font-medium mb-2">
                  {isHi ? 'जन्म नक्षत्र:' : 'Janma Nakshatra:'} <strong>{data.moon_death_transit.janma_nakshatra}</strong>
                </p>
                <p className="text-xs text-indigo-900/80 leading-relaxed mb-2">
                  {isHi ? data.moon_death_transit.watch_for_hi : data.moon_death_transit.watch_for_en}
                </p>
                <div className="rounded-lg bg-white/70 border border-indigo-100 px-2 py-2 text-xs text-indigo-700 leading-relaxed">
                  {isHi ? data.moon_death_transit.note_hi : data.moon_death_transit.note_en}
                </div>
                <div className="flex items-center gap-1.5 mt-2 text-[10px] text-indigo-400 italic">
                  <BookOpen className="w-3 h-3" /><span>{data.moon_death_transit.sloka_ref}</span>
                </div>
              </div>
            )}
            {/* Feature 3: Month & Lagna of Demise */}
            {data.demise_timing_classical && (
              <div className="rounded-xl border-2 border-purple-200 bg-purple-50 p-4">
                <h4 className="font-semibold text-purple-900 text-sm mb-2">
                  {isHi ? 'निधन माह एवं लग्न अनुमान' : 'Demise Month & Lagna Estimate'}
                </h4>
                <div className="space-y-2 text-xs">
                  <div className="flex gap-2">
                    <span className="text-purple-600 font-medium shrink-0">
                      {isHi ? 'संकेतक माह:' : 'Indicated Month:'}
                    </span>
                    <span className="text-purple-900 font-semibold">
                      {isHi
                        ? data.demise_timing_classical.likely_month_indicator.month_name_hi
                        : data.demise_timing_classical.likely_month_indicator.month_name_en}
                      {data.demise_timing_classical.likely_month_indicator.sign && (
                        <span className="font-normal text-purple-600 ml-1">
                          ({data.demise_timing_classical.likely_month_indicator.sign})
                        </span>
                      )}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <span className="text-purple-600 font-medium shrink-0">
                      {isHi ? 'संकेतक लग्न:' : 'Indicated Lagna:'}
                    </span>
                    <span className="text-purple-900 font-semibold">
                      {data.demise_timing_classical.likely_lagna_at_death.sign || '—'}
                    </span>
                  </div>
                  <p className="text-purple-800/70 leading-relaxed mt-1">
                    {isHi
                      ? data.demise_timing_classical.likely_month_indicator.reason_hi
                      : data.demise_timing_classical.likely_month_indicator.reason_en}
                  </p>
                  <p className="text-purple-800/70 leading-relaxed">
                    {isHi
                      ? data.demise_timing_classical.likely_lagna_at_death.reason_hi
                      : data.demise_timing_classical.likely_lagna_at_death.reason_en}
                  </p>
                </div>
                <div className="flex items-center gap-1.5 mt-2 text-[10px] text-purple-400 italic">
                  <BookOpen className="w-3 h-3" /><span>{data.demise_timing_classical.sloka_ref}</span>
                </div>
              </div>
            )}
          </div>
        </section>
      )}

      {/* ── Feature 6: Peak Lucky Periods (Adhyaya 13) ────────────── */}
      {data.lucky_time_estimate && data.lucky_time_estimate.peak_periods.length > 0 && (
        <section>
          <h3 className="text-base font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            {isHi ? 'सर्वोत्तम भाग्य काल (अ. 13)' : 'Peak Lucky Periods (Adh. 13)'}
          </h3>
          {/* Current period quality */}
          <div className={`rounded-lg border px-3 py-2 mb-3 flex items-center gap-2 text-sm ${
            data.lucky_time_estimate.current_period_quality === 'excellent'
              ? 'bg-emerald-50 border-emerald-300 text-emerald-800'
              : data.lucky_time_estimate.current_period_quality === 'good'
              ? 'bg-blue-50 border-blue-300 text-blue-800'
              : data.lucky_time_estimate.current_period_quality === 'challenging'
              ? 'bg-amber-50 border-amber-300 text-amber-800'
              : 'bg-gray-50 border-gray-200 text-gray-700'
          }`}>
            <Star className="w-4 h-4 shrink-0" />
            <span className="font-medium">
              {isHi ? 'वर्तमान काल:' : 'Current period:'} {data.lucky_time_estimate.current_mahadasha} Mahadasha
            </span>
            <span className={`ml-auto text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
              data.lucky_time_estimate.current_period_quality === 'excellent' ? 'bg-emerald-600 text-white'
              : data.lucky_time_estimate.current_period_quality === 'good' ? 'bg-blue-600 text-white'
              : data.lucky_time_estimate.current_period_quality === 'challenging' ? 'bg-amber-600 text-white'
              : 'bg-gray-400 text-white'
            }`}>
              {data.lucky_time_estimate.current_period_quality}
            </span>
          </div>
          {/* Peak periods timeline */}
          <div className="space-y-3">
            {data.lucky_time_estimate.peak_periods.map((period, i) => (
              <div key={i} className={`flex gap-3 rounded-xl border-2 p-4 ${
                period.quality === 'excellent'
                  ? 'border-emerald-300 bg-emerald-50'
                  : period.quality === 'good'
                  ? 'border-blue-200 bg-blue-50'
                  : 'border-gray-200 bg-gray-50'
              }`}>
                {/* Timeline dot */}
                <div className="flex flex-col items-center">
                  <div className={`w-3 h-3 rounded-full shrink-0 mt-1 ${
                    period.quality === 'excellent' ? 'bg-emerald-500'
                    : period.quality === 'good' ? 'bg-blue-500'
                    : 'bg-gray-400'
                  }`} />
                  {i < (data.lucky_time_estimate?.peak_periods.length ?? 0) - 1 && (
                    <div className="w-px flex-1 bg-gray-200 mt-1" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className={`text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded ${
                      period.period_type === 'dasha' ? 'bg-indigo-100 text-indigo-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      {period.period_type}
                    </span>
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded ${
                      period.quality === 'excellent' ? 'bg-emerald-600 text-white'
                      : period.quality === 'good' ? 'bg-blue-600 text-white'
                      : 'bg-gray-400 text-white'
                    }`}>
                      {period.quality}
                    </span>
                  </div>
                  <p className="text-xs text-foreground/85 leading-relaxed mb-1">
                    {isHi ? period.description_hi : period.description_en}
                  </p>
                  <p className="text-[10px] text-muted-foreground italic">
                    {period.approximate_age_range}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-1.5 mt-3 text-[10px] text-muted-foreground italic">
            <BookOpen className="w-3 h-3" />
            <span>{data.lucky_time_estimate.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Region after death */}
      {data.region_after_death && (
        <section className="rounded-xl border-2 border-indigo-200 bg-indigo-50 p-5">
          <h3 className="font-semibold text-indigo-900 mb-1 flex items-center gap-2">
            <Star className="w-5 h-5" />
            {isHi ? 'मृत्यु पश्चात् क्षेत्र' : 'Region After Death'}
          </h3>
          <div className="inline-block text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-indigo-600 text-white mb-3">
            {isHi ? data.region_after_death.region_hi : data.region_after_death.region_en}
          </div>
          <p className="text-sm text-indigo-900/90 leading-relaxed italic mb-3">
            {isHi ? data.region_after_death.narrative_hi : data.region_after_death.narrative_en}
          </p>
          {data.region_after_death.indicators.length > 0 && (
            <ul className="text-xs text-indigo-700 space-y-1 mb-3">
              {data.region_after_death.indicators.map((ind, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="mt-0.5 shrink-0">•</span>{ind}
                </li>
              ))}
            </ul>
          )}
          <div className="flex items-center gap-1.5 text-[10px] text-indigo-500 italic">
            <BookOpen className="w-3 h-3" />
            <span>{data.region_after_death.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Karmic transitions */}
      <section className="rounded-xl border-2 border-purple-200 bg-purple-50 p-5">
        <h3 className="font-semibold text-purple-900 mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('auto.karmicTransitions')}
        </h3>
        <p className="text-sm text-purple-900/90 leading-relaxed italic">
          {isHi ? data.karmic_transitions_hi : data.karmic_transitions_en}
        </p>
      </section>

      {/* Life chapters */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3">
          {t('auto.lifeChapters')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(isHi ? data.life_chapters_hi : data.life_chapters_en).map((chapter, i) => {
            const titles = isHi
              ? ['प्रारम्भिक', 'मध्य', 'उत्तर']
              : ['Early', 'Middle', 'Later'];
            return (
              <div
                key={i}
                className="rounded-xl border-2 border-sacred-gold/30 bg-gradient-to-br from-sacred-gold/5 to-transparent p-4"
              >
                <div className="text-[10px] uppercase tracking-widest text-sacred-gold-dark font-semibold mb-2">
                  {titles[i] || `#${i + 1}`}
                </div>
                <p className="text-sm text-foreground/90 leading-relaxed">{chapter}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Footer sloka ref */}
      <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground italic pt-4 border-t border-sacred-gold/20">
        <BookOpen className="w-3 h-3" />
        <span>{data.sloka_ref}</span>
      </div>
    </div>
  );
}
