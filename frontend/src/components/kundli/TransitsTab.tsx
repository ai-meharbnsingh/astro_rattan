import { useState, useEffect, useMemo } from 'react';
import { Loader2, CheckCircle, AlertTriangle, Calendar as CalendarIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import ConcentricChart from '@/components/kundli/ConcentricChart';
import RetrogradeStationsSection from '@/components/kundli/RetrogradeStationsSection';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';

interface TransitsTabProps {
  transitData: any;
  loadingTransit: boolean;
  transitHouseShift: number;
  setTransitHouseShift: (v: number) => void;
  transitDate: string;
  setTransitDate: (v: string) => void;
  transitTime: string;
  setTransitTime: (v: string) => void;
  result: any;
  language: string;
  t: (key: string) => string;
  refreshTransit: (date?: string, time?: string) => void;
  resetTransitFilters: () => void;
}

const _SIGN_NAMES = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

function TransitHeatMap({ kundliId, t, language }: { kundliId: string; t: any; language: string }) {
  const [forecast, setForecast] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.post(`/api/kundli/${kundliId}/transit-forecast`, {})
      .then(res => setForecast(res.forecast || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8 rounded-xl border border-sacred-gold/20 bg-transparent">
        <Loader2 className="w-5 h-5 animate-spin text-primary mr-2" />
        <p className="text-sm text-foreground">{t('transit.forecastLoading')}</p>
      </div>
    );
  }

  if (!forecast || forecast.length === 0) return null;

  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
        <CalendarIcon className="w-4 h-4" />
        <span>{t('transit.heatMapTitle')}</span>
      </div>
      <div className="p-4">
        <p className="text-sm text-foreground/70 mb-4">{t('transit.heatMapDesc')}</p>
        <div className="grid grid-cols-7 sm:grid-cols-10 md:grid-cols-15 lg:grid-cols-15 gap-2">
          {forecast.map((day, idx) => {
            const date = new Date(day.date);
            const dayNum = date.getDate();
            const month = date.toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-IN', { month: 'short' });
            let color = 'bg-red-500';
            if (day.score >= 70) color = 'bg-green-500';
            else if (day.score >= 40) color = 'bg-amber-400';
            return (
              <div key={idx} className="flex flex-col items-center gap-1 group relative">
                <div className={`w-full aspect-square rounded-md shadow-sm transition-transform hover:scale-110 cursor-help ${color}`} />
                <span className="text-[10px] text-foreground/50 font-bold">{dayNum}</span>
                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-50 pointer-events-none">
                  <div className="bg-black/90 text-white text-[10px] p-2 rounded whitespace-nowrap shadow-2xl border border-white/10 ring-1 ring-black">
                    <p className="font-bold border-b border-white/20 pb-1 mb-1">{dayNum} {month} {date.getFullYear()}</p>
                    <p>{t('transit.intensity')}: <span className="font-bold">{day.score}%</span></p>
                    <p className="mt-0.5 uppercase tracking-tighter opacity-80">{t(`transit.${day.summary.toLowerCase()}`)}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        <div className="flex items-center justify-end gap-4 mt-4 text-[10px] font-bold uppercase tracking-widest text-foreground/40">
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-sm bg-green-500" /> {t('transit.good')}</div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-sm bg-amber-400" /> {t('transit.average')}</div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-sm bg-red-500" /> {t('transit.challenging')}</div>
        </div>
      </div>
    </div>
  );
}

const MEMBER_STYLES: Record<string, { bg: string; border: string; text: string }> = {
  Father:   { bg: 'bg-amber-50',  border: 'border-amber-200',  text: 'text-amber-900'  },
  Mother:   { bg: 'bg-rose-50',   border: 'border-rose-200',   text: 'text-rose-900'   },
  Siblings: { bg: 'bg-blue-50',   border: 'border-blue-200',   text: 'text-blue-900'   },
  Spouse:   { bg: 'bg-violet-50', border: 'border-violet-200', text: 'text-violet-900' },
};

const INTENSITY_BADGE: Record<string, string> = {
  high:       'bg-red-100 text-red-800 border-red-300',
  moderate:   'bg-amber-100 text-amber-800 border-amber-300',
  low:        'bg-slate-100 text-slate-600 border-slate-300',
  supportive: 'bg-emerald-100 text-emerald-800 border-emerald-300',
};

function FamilyTimingSection({ kundliId, language, t }: { kundliId: string; language: string; t: (key: string) => string }) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/family-timing`)
      .then(res => { if (!cancelled) setData(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (!data) return null;

  const members: any[] = data.family_members || [];
  if (members.length === 0) return null;
  const hi = language === 'hi';

  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
        {hi ? 'परिवार के प्रमुख समय' : 'Family Timing Indicators'}
      </div>
      <div className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
        {members.map((fm: any) => {
          const style = MEMBER_STYLES[fm.member] || { bg: 'bg-slate-50', border: 'border-slate-200', text: 'text-slate-900' };
          const label = hi ? fm.member_hi : fm.member;
          const allIndicators = [...(fm.transit_indicators || []), ...(fm.protective_indicators || [])];
          return (
            <div key={fm.member} className={`rounded-lg border p-3 ${style.bg} ${style.border}`}>
              <div className="flex items-center justify-between mb-2">
                <p className={`text-xs font-bold uppercase tracking-wide ${style.text}`}>{label}</p>
                <span className="text-[10px] text-muted-foreground">
                  {hi ? 'भाव' : 'Bhava'} {fm.bhava} · {hi ? (fm.bhava_sign_hi || fm.bhava_sign) : fm.bhava_sign}
                </span>
              </div>
              {fm.bhava_lord && (
                <p className="text-[10px] text-muted-foreground mb-2">
                  {hi ? 'भाव स्वामी' : 'Lord'}: <span className="font-semibold">{translatePlanet(fm.bhava_lord, language)}</span>
                </p>
              )}
              <div className="space-y-1.5">
                {allIndicators.slice(0, 4).map((ind: any, i: number) => (
                  <div key={i} className="flex items-start gap-2">
                    <span className={`shrink-0 mt-0.5 px-1.5 py-0.5 rounded text-[9px] font-bold border ${INTENSITY_BADGE[ind.intensity] || INTENSITY_BADGE.low}`}>
                      {translatePlanet(ind.planet_transit, language)}
                    </span>
                    <p className="text-[11px] text-foreground/80 leading-snug">
                      {hi ? (ind.effect_hi || ind.effect_en) : ind.effect_en}
                    </p>
                  </div>
                ))}
              </div>
              {allIndicators.length === 0 && (
                <p className="text-[11px] text-muted-foreground italic">{hi ? 'कोई संकेत नहीं' : 'No active indicators'}</p>
              )}
            </div>
          );
        })}
      </div>
      {(data.summary_en || data.summary_hi) && (
        <div className="px-4 pb-4 text-xs text-muted-foreground italic">
          {hi ? (data.summary_hi || data.summary_en) : data.summary_en}
        </div>
      )}
    </div>
  );
}

export default function TransitsTab(props: TransitsTabProps) {
  const {
    transitData, loadingTransit,
    transitDate, setTransitDate,
    transitTime, setTransitTime,
    result, language, t,
    refreshTransit, resetTransitFilters,
  } = props;

  const [viewMode, setViewMode] = useState<'kundli' | 'concentric'>('kundli');

  const natalPlanets = useMemo(() => {
    if (!result?.chart_data?.planets) return [];
    return Object.entries(result.chart_data.planets).map(([planet, info]: [string, any]) => ({
      planet, sign: info.sign, longitude: info.longitude,
    }));
  }, [result]);

  const transitPlanets = useMemo(() => {
    if (!transitData?.transits) return [];
    return transitData.transits.map((tr: any) => {
      const signIdx = _SIGN_NAMES.indexOf(tr.current_sign);
      const lon = (signIdx * 30) + tr.sign_degree;
      return { planet: tr.planet, sign: tr.current_sign, longitude: lon, is_retrograde: tr.is_retrograde };
    });
  }, [transitData]);

  const ascendantSign = typeof result?.chart_data?.ascendant === 'string'
    ? result?.chart_data?.ascendant
    : result?.chart_data?.ascendant?.sign || '';

  return (
    <div className="space-y-6">
      {/* Date/Time Picker */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('section.gocharPredictions')}
        </div>
        <div className="p-4">
          <div className="flex flex-wrap items-end gap-3">
            <div>
              <label className="text-xs block mb-1 text-muted-foreground">{t('common.date')}</label>
              <input
                type="date"
                value={transitDate}
                onChange={(e) => setTransitDate(e.target.value)}
                className="px-3 py-1.5 rounded-lg text-sm border bg-card border-border/30 text-foreground"
              />
            </div>
            <div>
              <label className="text-xs block mb-1 text-muted-foreground">{t('common.time')}</label>
              <input
                type="time"
                value={transitTime}
                onChange={(e) => setTransitTime(e.target.value)}
                className="px-3 py-1.5 rounded-lg text-sm border bg-card border-border/30 text-foreground"
              />
            </div>
            <Button
              size="sm"
              onClick={() => refreshTransit(transitDate || undefined, transitTime ? `${transitTime}:00` : undefined)}
              className="px-4 bg-primary text-primary-foreground"
            >
              {transitDate ? t('transit.viewTransits') : t('transit.currentTransits')}
            </Button>
            {transitDate && (
              <button
                onClick={() => resetTransitFilters()}
                className="text-sm px-3 py-1.5 rounded-lg border border-border/30 text-muted-foreground"
              >
                {t('transit.resetToNow')}
              </button>
            )}
          </div>
          {transitData && (
            <div className="flex flex-wrap gap-4 text-sm mt-3">
              <span className="text-foreground"><strong>{t('transit.transitDate')}:</strong> {transitData.transit_date}</span>
              <span className="text-foreground"><strong>{t('transit.natalMoon')}:</strong> {translateSign(transitData.natal_moon_sign, language)}</span>
            </div>
          )}
        </div>
      </div>

      {loadingTransit ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{t('transit.loading')}</span>
        </div>
      ) : transitData ? (
        <div className="space-y-6">
          {/* Transit Chart + Table Side by Side */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
            {/* Transit Chart */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
                <span>{t('transit.chart')} ({transitData.transit_date})</span>
                <div className="flex bg-white/10 rounded-lg p-0.5 border border-white/20">
                  <button
                    onClick={() => setViewMode('kundli')}
                    className={`px-3 py-1 text-[10px] font-bold rounded-md transition-all ${viewMode === 'kundli' ? 'bg-white text-sacred-gold-dark' : 'text-white hover:bg-white/10'}`}
                  >
                    KUNDLI
                  </button>
                  <button
                    onClick={() => setViewMode('concentric')}
                    className={`px-3 py-1 text-[10px] font-bold rounded-md transition-all ${viewMode === 'concentric' ? 'bg-white text-sacred-gold-dark' : 'text-white hover:bg-white/10'}`}
                  >
                    CONCENTRIC
                  </button>
                </div>
              </div>
              <div className="flex justify-center p-4">
                {viewMode === 'kundli' ? (
                  <div className="w-full max-w-[480px] aspect-square animate-in fade-in zoom-in-95 duration-500">
                    <KundliChartSVG
                      planets={(transitData.transits || []).map((tr: any) => ({
                        planet: tr.planet,
                        sign: tr.current_sign,
                        sign_degree: tr.sign_degree || 0,
                        is_retrograde: !!tr.is_retrograde,
                      } as PlanetEntry))}
                      ascendantSign={ascendantSign}
                      language={language}
                      showHouseNumbers={false}
                      showRashiNumbers
                      rashiNumberPlacement="corner"
                      showAscendantMarker={false}
                    />
                  </div>
                ) : (
                  <div className="w-full animate-in fade-in zoom-in-95 duration-500">
                    <ConcentricChart
                      natalPlanets={natalPlanets}
                      transitPlanets={transitPlanets}
                      lagnaLongitude={result?.chart_data?.ascendant?.longitude || 0}
                    />
                  </div>
                )}
              </div>
              <div className="flex items-center justify-center gap-4 pb-3 text-xs text-foreground/60">
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full" style={{backgroundColor: 'var(--aged-gold)'}} /> {t('transit.benefic')}</span>
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full" style={{backgroundColor: 'var(--wax-red)'}} /> {t('transit.malefic')}</span>
              </div>
            </div>

            {/* Transit Table */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden h-fit">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {t('transit.transitDate')}: {transitData.transit_date}
              </div>
              <Table className="w-full text-xs table-fixed">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('table.planet')}</TableHead>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[28%]">{t('transit.currentSign')}</TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[22%]">{t('transit.houseFromMoon')}</TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('transit.effect')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {(transitData.transits || []).map((tr: any, idx: number) => (
                    <TableRow key={idx} className="border-t border-border">
                      <TableCell className="p-2 font-semibold text-foreground">{translatePlanet(tr.planet, language)}</TableCell>
                      <TableCell className="p-2 text-foreground">{translateSign(tr.current_sign, language)}</TableCell>
                      <TableCell className="p-2 text-center text-foreground">{tr.natal_house_from_moon}</TableCell>
                      <TableCell className="p-2 text-center">
                        <span className={`inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded-full font-semibold ${tr.effect === 'favorable' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {tr.effect === 'favorable' ? <CheckCircle className="w-2.5 h-2.5" /> : <AlertTriangle className="w-2.5 h-2.5" />}
                          {tr.effect === 'favorable' ? t('common.favorable') : t('common.unfavorable')}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* 30-Day Forecast Heat Map */}
          {result?.id && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
              <TransitHeatMap kundliId={result.id} t={t} language={language} />
            </div>
          )}

          {/* Detailed Transit Descriptions — table */}
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
              {t('transit.transitDate')}: {transitData.transit_date} — {language === 'hi' ? 'विस्तृत विवरण' : 'Detailed Analysis'}
            </div>
            <div className="overflow-x-auto">
              <Table className="w-full text-xs table-fixed">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[10%]">{t('table.planet')}</TableHead>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[11%]">{t('transit.currentSign')}</TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[10%]">{t('transit.effect')}</TableHead>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[14%]">{language === 'hi' ? 'विशेष' : 'Flags'}</TableHead>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[55%]">{language === 'hi' ? 'विवरण' : 'Description'}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {(transitData.transits || []).map((tr: any, idx: number) => {
                    const isCancelled = tr.vedha_active === true || tr.effect_final === 'cancelled';
                    return (
                      <TableRow key={idx} className="border-t border-border align-top">
                        <TableCell className="p-2 font-semibold text-foreground">{translatePlanet(tr.planet, language)}</TableCell>
                        <TableCell className="p-2 text-foreground">{translateSign(tr.current_sign, language)}</TableCell>
                        <TableCell className="p-2 text-center">
                          <span className={`inline-flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded-full font-semibold ${isCancelled ? 'bg-red-200 text-red-900 line-through' : tr.effect === 'favorable' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                            {tr.effect === 'favorable' ? <CheckCircle className="w-2.5 h-2.5" /> : <AlertTriangle className="w-2.5 h-2.5" />}
                            {tr.effect === 'favorable' ? t('common.favorable') : t('common.unfavorable')}
                          </span>
                        </TableCell>
                        <TableCell className="p-2">
                          <div className="flex flex-wrap gap-1">
                            {isCancelled && (
                              <span className="px-1 py-0.5 rounded text-[9px] font-bold bg-red-600 text-white">⊘ {t('auto.vedhaCancelled')}</span>
                            )}
                            {tr.is_retrograde && (
                              <span className="px-1 py-0.5 rounded text-[9px] font-bold bg-purple-100 text-purple-800">℞</span>
                            )}
                            {tr.latta_type === 'prishta' && (
                              <span className="px-1 py-0.5 rounded text-[9px] font-bold bg-emerald-100 text-emerald-800">↑ Latta</span>
                            )}
                            {tr.latta_type === 'pratyak' && (
                              <span className="px-1 py-0.5 rounded text-[9px] font-bold bg-orange-100 text-orange-800">↓ Latta</span>
                            )}
                            {tr.kaksha && (
                              <span className={`px-1 py-0.5 rounded text-[9px] font-bold border ${tr.kaksha.favorable ? 'bg-violet-50 text-violet-800 border-violet-200' : 'bg-gray-50 text-gray-600 border-gray-200'}`}>
                                ◈ K{tr.kaksha.kaksha_number}
                              </span>
                            )}
                          </div>
                        </TableCell>
                        <TableCell className="p-2 whitespace-normal break-words max-w-0">
                          <p className={`text-foreground/80 leading-snug ${isCancelled ? 'line-through opacity-60' : ''}`}>
                            {tr.description}
                          </p>
                          {tr.is_retrograde && (tr.retrograde_effect_en || tr.retrograde_effect_hi) && (
                            <p className="mt-1 italic text-purple-700 border-l-2 border-purple-300 pl-1.5">
                              {language === 'hi' ? (tr.retrograde_effect_hi || tr.retrograde_effect_en) : (tr.retrograde_effect_en || tr.retrograde_effect_hi)}
                            </p>
                          )}
                          {isCancelled && tr.vedha_by && (
                            <p className="mt-1 italic text-red-700">
                              {t('auto.cancelledBy')}: {translatePlanet(tr.vedha_by.planet, language)}
                              {' '}({language === 'hi' ? tr.vedha_by.description_hi : tr.vedha_by.description_en})
                            </p>
                          )}
                          {tr.latta_type && (
                            <p className={`mt-1 italic ${tr.latta_type === 'prishta' ? 'text-emerald-700' : 'text-orange-700'}`}>
                              {language === 'hi' ? tr.latta_description_hi : tr.latta_description_en}
                            </p>
                          )}
                          {tr.kaksha && (
                            <p className="mt-1 italic text-violet-700/80">
                              {language === 'hi' ? tr.kaksha.interpretation_hi : tr.kaksha.interpretation_en}
                            </p>
                          )}
                          {(tr.sloka_ref || tr.kaksha?.sloka_ref) && (
                            <p className="mt-1 opacity-50 italic">{tr.sloka_ref || tr.kaksha?.sloka_ref}</p>
                          )}
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
            <div className="px-4 py-2 border-t border-border bg-sacred-gold/5 text-[10px] text-muted-foreground space-y-0.5">
              <p>{t('auto.vedhaLegend')}</p>
              <p>{t('auto.lattaLegend')}</p>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-center text-foreground py-8">{t('transit.clickTab')}</p>
      )}

      {/* Family Timing Indicators */}
      {result?.id && <FamilyTimingSection kundliId={result.id} language={language} t={t} />}

      {/* Retrograde Station Dates */}
      {result?.id && <RetrogradeStationsSection kundliId={result.id} />}
    </div>
  );
}
