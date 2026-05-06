import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { Loader2, Info, BookOpen, Heart, Clock3, Moon as MoonIcon, Sparkles, Eye, Activity, AlertTriangle, Star, TrendingUp, CheckCircle2, XCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import SlokaHover from './SlokaHover';

interface MarakaPlanet { planet: string; role: string; role_hi?: string; placement: number; strength: string; notes_en: string; notes_hi: string; }
interface EighthHouseAnalysis { eighth_lord: string; eighth_lord_placement: number; eighth_lord_strength: string; planets_in_8th: string[]; interpretation_en: string; interpretation_hi: string; }
interface SaturnAssessment { saturn_placement: number; saturn_sign?: string; saturn_strength: string; interpretation_en: string; interpretation_hi: string; }
interface TransitTimingIndicator { planet_transit: string; target_sign: string; target_house: number; significance_en: string; significance_hi: string; watch_period_en: string; watch_period_hi: string; intensity: string; }
interface TransitTimingSection { indicators: TransitTimingIndicator[]; summary_en: string; summary_hi: string; sloka_ref: string; }
interface DashaSignal { dasha: string; lord: string; role: string; en: string; hi: string; }
interface DashaGochara { signals: DashaSignal[]; convergence: string; summary_en: string; summary_hi: string; mahadasha_lord?: string; antardasha_lord?: string; }
interface SaturnTransitDeath { current_saturn_house_from_moon: number; is_8th_from_moon: boolean; saturn_8th_lord_transit: boolean; eighth_lord: string; eighth_lord_sign: string; moon_house: number; saturn_house: number; interpretation_en: string; interpretation_hi: string; severity: string; sloka_ref: string; }
interface MoonDeathTransit { janma_nakshatra: string; watch_for_en: string; watch_for_hi: string; note_en: string; note_hi: string; sloka_ref: string; }
interface DemiseTiming { likely_month_indicator: { sign: string; month_name_en: string; month_name_hi: string; planet: string; reason_en: string; reason_hi: string; }; likely_lagna_at_death: { sign: string; reason_en: string; reason_hi: string; }; disclaimer_en: string; disclaimer_hi: string; sloka_ref: string; }
interface ScoreSignal { signal_en: string; signal_hi: string; points: number; triggered: boolean; }
interface DeathScore { total: number; signals: ScoreSignal[]; verdict_en: string; verdict_hi: string; disclaimer_en: string; sloka_ref: string; }
interface LuckyPeriod { period_type: string; description_en: string; description_hi: string; approximate_age_range: string; quality: string; }
interface LuckyTimeEstimate { peak_periods: LuckyPeriod[]; current_period_quality: string; current_mahadasha: string; sloka_ref: string; }

interface ApiResponse {
  kundli_id?: string; person_name?: string;
  overall_longevity_strength: string;
  maraka_planets: MarakaPlanet[];
  eighth_house_analysis: EighthHouseAnalysis;
  saturn_longevity_assessment: SaturnAssessment;
  karmic_transitions_en: string; karmic_transitions_hi: string;
  life_chapters_en: string[]; life_chapters_hi: string[];
  transit_timing_indicators?: TransitTimingSection;
  dasha_gochara_timing?: DashaGochara;
  saturn_transit_death_indicator?: SaturnTransitDeath;
  moon_death_transit?: MoonDeathTransit;
  demise_timing_classical?: DemiseTiming;
  dasha_gochara_lagna_score?: DeathScore;
  lucky_time_estimate?: LuckyTimeEstimate;
  region_after_death?: { region_en: string; region_hi: string; narrative_en: string; narrative_hi: string; indicators: string[]; sloka_ref: string; };
  sloka_ref: string;
}

interface Props { kundliId: string; language: string; t: (key: string) => string; }

const PLANET_HI: Record<string, string> = { Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध', Jupiter: 'बृहस्पति', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु' };
const SEV_BADGE: Record<string, string> = { strong: 'bg-emerald-600 text-white', moderate: 'bg-amber-500 text-white', weak: 'bg-red-600 text-white', high: 'bg-red-600 text-white', low: 'bg-blue-500 text-white', unknown: 'bg-gray-400 text-white' };
const QUALITY_BADGE: Record<string, string> = { excellent: 'bg-emerald-600 text-white', good: 'bg-blue-600 text-white', neutral: 'bg-gray-400 text-white', challenging: 'bg-amber-600 text-white' };

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdWrapCls   = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';
const tdMuted     = 'p-1.5 text-xs text-muted-foreground border-t border-border align-top';

function SlokaRef({ ref: r, language }: { ref?: string; language: string }) {
  if (!r) return null;
  return (
    <div className="flex items-center gap-1.5 px-4 py-2 border-t border-border text-[11px] text-muted-foreground italic">
      <BookOpen className="w-3 h-3 shrink-0" />
      <SlokaHover slokaRef={r} language={language} />
    </div>
  );
}

export default function LongevityTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true); setError('');
    (async () => {
      try {
        const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/longevity-indicators`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || t('auto.genericError'));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) return <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-primary" /></div>;
  if (error)   return <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>;
  if (!data)   return null;

  const pn = (p: string) => isHi ? (PLANET_HI[p] || p) : p;

  return (
    <div className="space-y-4">

      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Clock3 className="w-6 h-6" />
          {t('auto.longevity')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.longevityDesc')}</p>
      </div>

      {/* Disclaimer */}
      <div className="rounded-lg border border-blue-300 bg-blue-50 px-4 py-3 flex items-start gap-2">
        <Info className="w-4 h-4 text-blue-700 shrink-0 mt-0.5" />
        <p className="text-xs text-blue-900 leading-relaxed">{t('auto.longevityDisclaimer')}</p>
      </div>

      {/* Overall Strength */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Heart className="w-4 h-4" />
          <span>{t('auto.overallLongevityStrength')}</span>
          <span className={`ml-auto text-[11px] font-bold px-2.5 py-0.5 rounded ${SEV_BADGE[data.overall_longevity_strength] ?? SEV_BADGE.moderate}`}>
            {t(`auto.longevity${data.overall_longevity_strength.charAt(0).toUpperCase() + data.overall_longevity_strength.slice(1)}`)}
          </span>
        </div>
      </div>

      {/* Maraka Planets */}
      {data.maraka_planets.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Sparkles className="w-4 h-4" />
            <span>{t('auto.marakaPlanets')}</span>
            <span className="ml-auto text-[12px] font-normal opacity-80">{data.maraka_planets.length}</span>
          </div>
          <div className="overflow-x-auto">
          <table style={{ tableLayout: 'fixed', minWidth: '480px', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '14%' }} />
              <col style={{ width: '20%' }} />
              <col style={{ width: '9%' }} />
              <col style={{ width: '12%' }} />
              <col style={{ width: '45%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'ग्रह' : 'Planet'}</th>
                <th className={thCls}>{isHi ? 'भूमिका' : 'Role'}</th>
                <th className={thCls}>{isHi ? 'भाव' : 'H'}</th>
                <th className={thCls}>{isHi ? 'बल' : 'Strength'}</th>
                <th className={thCls}>{isHi ? 'टिप्पणी' : 'Notes'}</th>
              </tr>
            </thead>
            <tbody>
              {data.maraka_planets.map((m, i) => (
                <tr key={i}>
                  <td className={`${tdCls} font-semibold`}>{pn(m.planet)}</td>
                  <td className={tdWrapCls}>{isHi && m.role_hi ? m.role_hi : m.role}</td>
                  <td className={tdCls}>{m.placement > 0 ? m.placement : '—'}</td>
                  <td className={tdCls}>
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${SEV_BADGE[m.strength] ?? SEV_BADGE.moderate}`}>
                      {m.strength}
                    </span>
                  </td>
                  <td className={tdWrapCls}>{isHi ? m.notes_hi : m.notes_en}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        </div>
      )}

      {/* 8th House + Saturn */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className={ohContainer}>
          <div className={ohHeader}>
            <MoonIcon className="w-4 h-4" />
            <span>{t('auto.eighthHouseAnalysis')}</span>
            {data.eighth_house_analysis.eighth_lord && (
              <span className="ml-auto text-[11px] font-normal bg-white/20 px-2 py-0.5 rounded">
                {pn(data.eighth_house_analysis.eighth_lord)} · H{data.eighth_house_analysis.eighth_lord_placement}
              </span>
            )}
          </div>
          {data.eighth_house_analysis.planets_in_8th.length > 0 && (
            <div className="px-4 pt-3 flex items-center gap-2 flex-wrap">
              <span className="text-[10px] text-muted-foreground font-semibold uppercase">{isHi ? '8वें भाव में:' : 'In 8th:'}</span>
              {data.eighth_house_analysis.planets_in_8th.map(p => (
                <span key={p} className="px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark text-[11px] font-medium">{pn(p)}</span>
              ))}
            </div>
          )}
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed">{isHi ? data.eighth_house_analysis.interpretation_hi : data.eighth_house_analysis.interpretation_en}</p>
          </div>
        </div>

        <div className={ohContainer}>
          <div className={ohHeader}>
            <Clock3 className="w-4 h-4" />
            <span>{t('auto.saturnLongevity')}</span>
            {data.saturn_longevity_assessment.saturn_placement > 0 && (
              <span className="ml-auto text-[11px] font-normal bg-white/20 px-2 py-0.5 rounded">
                H{data.saturn_longevity_assessment.saturn_placement}{data.saturn_longevity_assessment.saturn_sign ? ` · ${data.saturn_longevity_assessment.saturn_sign}` : ''}
              </span>
            )}
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed">{isHi ? data.saturn_longevity_assessment.interpretation_hi : data.saturn_longevity_assessment.interpretation_en}</p>
          </div>
        </div>
      </div>

      {/* Transit Timing Indicators */}
      {data.transit_timing_indicators && data.transit_timing_indicators.indicators.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Activity className="w-4 h-4" />
            <span>{isHi ? 'कर्म-संक्रमण गोचर संकेत' : 'Karmic Transition Transit Markers'}</span>
            <span className="ml-auto text-[12px] font-normal opacity-80">{data.transit_timing_indicators.indicators.length}</span>
          </div>
          {(data.transit_timing_indicators.summary_en || data.transit_timing_indicators.summary_hi) && (
            <div className="px-4 py-2 border-b border-border text-xs text-muted-foreground">
              {isHi ? data.transit_timing_indicators.summary_hi : data.transit_timing_indicators.summary_en}
            </div>
          )}
          <div className="overflow-x-auto">
          <table style={{ tableLayout: 'fixed', minWidth: '480px', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '18%' }} />
              <col style={{ width: '8%' }} />
              <col style={{ width: '11%' }} />
              <col style={{ width: '35%' }} />
              <col style={{ width: '28%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'ग्रह→राशि' : 'Planet→Sign'}</th>
                <th className={thCls}>{isHi ? 'भाव' : 'H'}</th>
                <th className={thCls}>{isHi ? 'तीव्रता' : 'Intensity'}</th>
                <th className={thCls}>{isHi ? 'महत्व' : 'Significance'}</th>
                <th className={thCls}>{isHi ? 'ध्यान काल' : 'Watch Period'}</th>
              </tr>
            </thead>
            <tbody>
              {data.transit_timing_indicators.indicators.map((ind, i) => (
                <tr key={i}>
                  <td className={`${tdCls} font-semibold`}>{pn(ind.planet_transit)} → {ind.target_sign}</td>
                  <td className={tdCls}>{ind.target_house}</td>
                  <td className={tdCls}>
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${SEV_BADGE[ind.intensity] ?? SEV_BADGE.moderate}`}>
                      {ind.intensity}
                    </span>
                  </td>
                  <td className={tdWrapCls}>{isHi ? ind.significance_hi : ind.significance_en}</td>
                  <td className={tdWrapCls}>
                    <div className="flex items-start gap-1">
                      <Eye className="w-3 h-3 text-muted-foreground shrink-0 mt-0.5" />
                      <span className="italic">{isHi ? ind.watch_period_hi : ind.watch_period_en}</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
          <SlokaRef ref={data.transit_timing_indicators.sloka_ref} language={language} />
        </div>
      )}

      {/* Dasha–Lagna Multi-Signal */}
      {data.dasha_gochara_timing && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Activity className="w-4 h-4" />
            <span>{isHi ? 'दशा–लग्न बहु-संकेत विश्लेषण' : 'Dasha–Lagna Multi-Signal Analysis'}</span>
            {data.dasha_gochara_timing.convergence && (
              <span className={`ml-auto text-[10px] font-bold px-2 py-0.5 rounded ${
                data.dasha_gochara_timing.convergence === 'high' ? 'bg-red-100 text-red-800' :
                data.dasha_gochara_timing.convergence === 'moderate' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'
              }`}>
                {data.dasha_gochara_timing.convergence}
              </span>
            )}
          </div>
          {data.dasha_gochara_timing.mahadasha_lord && (
            <div className="px-4 py-2 border-b border-border text-xs text-muted-foreground">
              {isHi ? 'महादशा' : 'Mahadasha'}: <strong className="text-foreground">{data.dasha_gochara_timing.mahadasha_lord}</strong>
              {data.dasha_gochara_timing.antardasha_lord && <> · {isHi ? 'अन्तर्दशा' : 'Antardasha'}: <strong className="text-foreground">{data.dasha_gochara_timing.antardasha_lord}</strong></>}
            </div>
          )}
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed mb-3">{isHi ? data.dasha_gochara_timing.summary_hi : data.dasha_gochara_timing.summary_en}</p>
            {data.dasha_gochara_timing.signals.length > 0 && (
              <div className="overflow-x-auto">
              <table style={{ tableLayout: 'fixed', minWidth: '320px', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
                <colgroup><col style={{ width: '18%' }} /><col style={{ width: '14%' }} /><col style={{ width: '68%' }} /></colgroup>
                <thead><tr>
                  <th className={thCls}>{isHi ? 'दशा' : 'Dasha'}</th>
                  <th className={thCls}>{isHi ? 'स्वामी' : 'Lord'}</th>
                  <th className={thCls}>{isHi ? 'विवरण' : 'Description'}</th>
                </tr></thead>
                <tbody>
                  {data.dasha_gochara_timing.signals.map((sig, i) => (
                    <tr key={i}>
                      <td className={`${tdCls} font-semibold`}>{sig.dasha}</td>
                      <td className={tdCls}>{pn(sig.lord)}</td>
                      <td className={tdWrapCls}>{isHi ? sig.hi : sig.en}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Combined Death Risk Score */}
      {data.dasha_gochara_lagna_score && (
        <div className={ohContainer}>
          <div className="bg-orange-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            <span>{isHi ? 'मृत्यु-काल बहु-संकेत अंक' : 'Combined Death Risk Score'}</span>
            <div className={`ml-auto w-9 h-9 rounded-full border-2 border-white/60 flex items-center justify-center font-bold text-base ${
              data.dasha_gochara_lagna_score.total >= 6 ? 'bg-red-700' : data.dasha_gochara_lagna_score.total >= 3 ? 'bg-orange-500' : 'bg-green-700'
            }`}>
              {data.dasha_gochara_lagna_score.total}
            </div>
          </div>
          <div className="px-4 py-2 border-b border-border flex items-start gap-2">
            <Info className="w-3.5 h-3.5 text-orange-700 shrink-0 mt-0.5" />
            <p className="text-[11px] text-orange-800 italic">{data.dasha_gochara_lagna_score.disclaimer_en}</p>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed mb-3">{isHi ? data.dasha_gochara_lagna_score.verdict_hi : data.dasha_gochara_lagna_score.verdict_en}</p>
            <div className="space-y-1.5">
              {data.dasha_gochara_lagna_score.signals.map((sig, i) => (
                <div key={i} className={`flex items-center gap-2 rounded px-3 py-2 text-xs ${sig.triggered ? 'bg-orange-50 border border-orange-200' : 'bg-gray-50 border border-gray-100'}`}>
                  {sig.triggered ? <CheckCircle2 className="w-3.5 h-3.5 text-orange-700 shrink-0" /> : <XCircle className="w-3.5 h-3.5 text-gray-300 shrink-0" />}
                  <span className={`flex-1 leading-relaxed ${sig.triggered ? 'text-orange-900 font-medium' : 'text-gray-400'}`}>{isHi ? sig.signal_hi : sig.signal_en}</span>
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded shrink-0 ${sig.triggered ? 'bg-orange-600 text-white' : 'bg-gray-200 text-gray-400'}`}>+{sig.points}</span>
                </div>
              ))}
            </div>
          </div>
          <SlokaRef ref={data.dasha_gochara_lagna_score.sloka_ref} language={language} />
        </div>
      )}

      {/* Saturn Transit Death Indicator */}
      {data.saturn_transit_death_indicator && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Clock3 className="w-4 h-4" />
            <span>{isHi ? 'शनि गोचर निधन-संकेत' : 'Saturn Transit Death Indicator'}</span>
            <span className={`ml-auto text-[10px] font-bold px-2 py-0.5 rounded ${SEV_BADGE[data.saturn_transit_death_indicator.severity] ?? SEV_BADGE.moderate}`}>
              {data.saturn_transit_death_indicator.severity}
            </span>
          </div>
          <div className="px-4 py-3">
            <div className="flex flex-wrap gap-2 mb-3">
              <span className="text-[11px] px-2 py-1 rounded bg-sacred-gold/10 text-sacred-gold-dark font-medium">
                {isHi ? `शनि भाव ${data.saturn_transit_death_indicator.saturn_house}` : `Saturn H${data.saturn_transit_death_indicator.saturn_house}`}
              </span>
              <span className="text-[11px] px-2 py-1 rounded bg-sacred-gold/10 text-sacred-gold-dark font-medium">
                {isHi ? `चंद्र से भाव ${data.saturn_transit_death_indicator.current_saturn_house_from_moon}` : `From Moon: H${data.saturn_transit_death_indicator.current_saturn_house_from_moon}`}
              </span>
              <span className={`text-[11px] px-2 py-1 rounded font-medium ${data.saturn_transit_death_indicator.is_8th_from_moon ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-600'}`}>
                {isHi ? `चंद्र से 8वें: ${data.saturn_transit_death_indicator.is_8th_from_moon ? 'हाँ' : 'नहीं'}` : `8th from Moon: ${data.saturn_transit_death_indicator.is_8th_from_moon ? 'Yes' : 'No'}`}
              </span>
            </div>
            <p className="text-sm text-foreground leading-relaxed">{isHi ? data.saturn_transit_death_indicator.interpretation_hi : data.saturn_transit_death_indicator.interpretation_en}</p>
          </div>
          <SlokaRef ref={data.saturn_transit_death_indicator.sloka_ref} language={language} />
        </div>
      )}

      {/* Classical Death Timing */}
      {(data.moon_death_transit?.janma_nakshatra || data.demise_timing_classical) && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <MoonIcon className="w-4 h-4" />
            <span>{isHi ? 'शास्त्रीय निधन-काल संकेत' : 'Classical Death Timing Indicators'}</span>
          </div>
          <div className="px-4 pt-3 pb-1 border-b border-border flex items-start gap-2">
            <Info className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
            <p className="text-[11px] text-blue-800 italic">
              {data.demise_timing_classical
                ? (isHi ? data.demise_timing_classical.disclaimer_hi : data.demise_timing_classical.disclaimer_en)
                : 'Classical philosophical indicators — NOT death predictions.'}
            </p>
          </div>
          <div className="overflow-x-auto">
          <table style={{ tableLayout: 'fixed', minWidth: '280px', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup><col style={{ width: '35%' }} /><col style={{ width: '65%' }} /></colgroup>
            <tbody>
              {data.moon_death_transit?.janma_nakshatra && <>
                <tr>
                  <td className={tdMuted}>{isHi ? 'जन्म नक्षत्र' : 'Janma Nakshatra'}</td>
                  <td className={tdWrapCls}><span className="font-semibold">{data.moon_death_transit.janma_nakshatra}</span></td>
                </tr>
                <tr>
                  <td className={tdMuted}>{isHi ? 'ध्यान दें' : 'Watch For'}</td>
                  <td className={tdWrapCls}>{isHi ? data.moon_death_transit.watch_for_hi : data.moon_death_transit.watch_for_en}</td>
                </tr>
                <tr>
                  <td className={tdMuted}>{isHi ? 'टिप्पणी' : 'Note'}</td>
                  <td className={tdWrapCls}>{isHi ? data.moon_death_transit.note_hi : data.moon_death_transit.note_en}</td>
                </tr>
              </>}
              {data.demise_timing_classical && <>
                <tr>
                  <td className={tdMuted}>{isHi ? 'संकेतक माह' : 'Indicated Month'}</td>
                  <td className={tdWrapCls}>
                    <span className="font-semibold">{isHi ? data.demise_timing_classical.likely_month_indicator.month_name_hi : data.demise_timing_classical.likely_month_indicator.month_name_en}</span>
                    {data.demise_timing_classical.likely_month_indicator.sign && <span className="text-muted-foreground ml-1">({data.demise_timing_classical.likely_month_indicator.sign})</span>}
                    <p className="text-muted-foreground mt-0.5">{isHi ? data.demise_timing_classical.likely_month_indicator.reason_hi : data.demise_timing_classical.likely_month_indicator.reason_en}</p>
                  </td>
                </tr>
                <tr>
                  <td className={tdMuted}>{isHi ? 'संकेतक लग्न' : 'Indicated Lagna'}</td>
                  <td className={tdWrapCls}>
                    <span className="font-semibold">{data.demise_timing_classical.likely_lagna_at_death.sign || '—'}</span>
                    <p className="text-muted-foreground mt-0.5">{isHi ? data.demise_timing_classical.likely_lagna_at_death.reason_hi : data.demise_timing_classical.likely_lagna_at_death.reason_en}</p>
                  </td>
                </tr>
              </>}
            </tbody>
          </table>
          </div>
          {data.moon_death_transit?.sloka_ref && <SlokaRef ref={data.moon_death_transit.sloka_ref} language={language} />}
        </div>
      )}

      {/* Peak Lucky Periods */}
      {data.lucky_time_estimate && data.lucky_time_estimate.peak_periods.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <TrendingUp className="w-4 h-4" />
            <span>{isHi ? 'सर्वोत्तम भाग्य काल' : 'Peak Lucky Periods'}</span>
            {data.lucky_time_estimate.current_mahadasha && (
              <span className={`ml-auto text-[10px] font-bold px-2 py-0.5 rounded ${QUALITY_BADGE[data.lucky_time_estimate.current_period_quality] ?? QUALITY_BADGE.neutral}`}>
                {data.lucky_time_estimate.current_mahadasha} · {data.lucky_time_estimate.current_period_quality}
              </span>
            )}
          </div>
          <div className="overflow-x-auto">
          <table style={{ tableLayout: 'fixed', minWidth: '400px', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup><col style={{ width: '12%' }} /><col style={{ width: '12%' }} /><col style={{ width: '20%' }} /><col style={{ width: '56%' }} /></colgroup>
            <thead><tr>
              <th className={thCls}>{isHi ? 'प्रकार' : 'Type'}</th>
              <th className={thCls}>{isHi ? 'गुणवत्ता' : 'Quality'}</th>
              <th className={thCls}>{isHi ? 'आयु' : 'Age Range'}</th>
              <th className={thCls}>{isHi ? 'विवरण' : 'Description'}</th>
            </tr></thead>
            <tbody>
              {data.lucky_time_estimate.peak_periods.map((p, i) => (
                <tr key={i}>
                  <td className={tdCls}>
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${p.period_type === 'dasha' ? 'bg-indigo-100 text-indigo-700' : 'bg-amber-100 text-amber-700'}`}>{p.period_type}</span>
                  </td>
                  <td className={tdCls}>
                    <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${QUALITY_BADGE[p.quality] ?? QUALITY_BADGE.neutral}`}>{p.quality}</span>
                  </td>
                  <td className={tdCls}>{p.approximate_age_range}</td>
                  <td className={tdWrapCls}>{isHi ? p.description_hi : p.description_en}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
          <SlokaRef ref={data.lucky_time_estimate.sloka_ref} language={language} />
        </div>
      )}

      {/* Region After Death */}
      {data.region_after_death && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Star className="w-4 h-4" />
            <span>{isHi ? 'मृत्यु पश्चात् क्षेत्र' : 'Region After Death'}</span>
            <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">
              {isHi ? data.region_after_death.region_hi : data.region_after_death.region_en}
            </span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed italic mb-3">{isHi ? data.region_after_death.narrative_hi : data.region_after_death.narrative_en}</p>
            {data.region_after_death.indicators.length > 0 && (
              <ul className="space-y-1">
                {data.region_after_death.indicators.map((ind, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-xs text-foreground">
                    <span className="text-sacred-gold-dark shrink-0 mt-0.5">•</span>{ind}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <SlokaRef ref={data.region_after_death.sloka_ref} language={language} />
        </div>
      )}

      {/* Karmic Transitions */}
      {(data.karmic_transitions_en || data.karmic_transitions_hi) && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Sparkles className="w-4 h-4" />
            <span>{t('auto.karmicTransitions')}</span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed italic">{isHi ? data.karmic_transitions_hi : data.karmic_transitions_en}</p>
          </div>
        </div>
      )}

      {/* Life Chapters */}
      {(isHi ? data.life_chapters_hi : data.life_chapters_en)?.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <BookOpen className="w-4 h-4" />
            <span>{t('auto.lifeChapters')}</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-border">
            {(isHi ? data.life_chapters_hi : data.life_chapters_en).map((chapter, i) => {
              const labels = isHi ? ['प्रारम्भिक', 'मध्य', 'उत्तर'] : ['Early Life', 'Middle Life', 'Later Life'];
              return (
                <div key={i} className="px-4 py-3">
                  <p className="text-[10px] font-semibold text-sacred-gold-dark uppercase tracking-wide mb-1">{labels[i] ?? `#${i+1}`}</p>
                  <p className="text-xs text-foreground leading-relaxed">{chapter}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Footer */}
      {data.sloka_ref && (
        <div className="flex items-center gap-1.5 pt-2 border-t border-border text-[11px] text-muted-foreground italic justify-center">
          <BookOpen className="w-3 h-3" /><span>{data.sloka_ref}</span>
        </div>
      )}
    </div>
  );
}
