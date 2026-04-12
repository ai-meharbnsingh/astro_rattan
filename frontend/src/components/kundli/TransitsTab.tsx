import { useState, useEffect, useMemo } from 'react';
import { Loader2, CheckCircle, AlertTriangle, Calendar as CalendarIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import InteractiveKundli from '@/components/InteractiveKundli';
import ConcentricChart from '@/components/kundli/ConcentricChart';
import RetrogradeStationsSection from '@/components/kundli/RetrogradeStationsSection';
import { translatePlanet, translateSign, translateLabel } from '@/lib/backend-translations';

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
    api.post(`/${kundliId}/transit-forecast`)
      .then(res => setForecast(res.forecast || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8 bg-sacred-cream rounded-xl border border-sacred-gold">
        <Loader2 className="w-5 h-5 animate-spin text-sacred-gold mr-2" />
        <p className="text-sm text-cosmic-text">{t('transit.forecastLoading')}</p>
      </div>
    );
  }

  if (!forecast || forecast.length === 0) return null;

  return (
    <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold shadow-sm">
      <div className="flex items-center gap-2 mb-2">
        <CalendarIcon className="w-5 h-5 text-sacred-gold" />
        <h4 className="text-lg font-bold text-sacred-brown">{t('transit.heatMapTitle')}</h4>
      </div>
      <p className="text-sm text-cosmic-text/70 mb-6">{t('transit.heatMapDesc')}</p>

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
              <div 
                className={`w-full aspect-square rounded-md shadow-sm transition-transform hover:scale-110 cursor-help ${color}`}
              />
              <span className="text-[10px] text-cosmic-text/50 font-bold">{dayNum}</span>
              
              {/* Tooltip */}
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

      <div className="flex items-center justify-end gap-4 mt-6 text-[10px] font-bold uppercase tracking-widest text-cosmic-text/40">
        <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-sm bg-green-500" /> {t('transit.good')}</div>
        <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-sm bg-amber-400" /> {t('transit.average')}</div>
        <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-sm bg-red-500" /> {t('transit.challenging')}</div>
      </div>
    </div>
  );
}

export default function TransitsTab(props: TransitsTabProps) {
  const {
    transitData,
    loadingTransit,
    transitHouseShift,
    setTransitHouseShift,
    transitDate,
    setTransitDate,
    transitTime,
    setTransitTime,
    result,
    language,
    t,
    refreshTransit,
    resetTransitFilters,
  } = props;

  const [viewMode, setViewMode] = useState<'diamond' | 'concentric'>('diamond');

  const natalPlanets = useMemo(() => {
    if (!result?.chart_data?.planets) return [];
    return Object.entries(result.chart_data.planets).map(([planet, info]: [string, any]) => ({
      planet,
      sign: info.sign,
      longitude: info.longitude,
    }));
  }, [result]);

  const transitPlanets = useMemo(() => {
    if (!transitData?.transits) return [];
    return transitData.transits.map((tr: any) => {
      const signIdx = _SIGN_NAMES.indexOf(tr.current_sign);
      const lon = (signIdx * 30) + tr.sign_degree;
      return {
        planet: tr.planet,
        sign: tr.current_sign,
        longitude: lon,
        is_retrograde: tr.is_retrograde
      };
    });
  }, [transitData]);

  return (
    <div className="space-y-6">
            {/* Date/Time Picker — always visible */}
            <div className="rounded-xl p-4 mb-4 border" style={{ backgroundColor: 'rgba(184,134,11,0.04)', borderColor: 'rgba(184,134,11,0.25)' }}>
              <h4 className="font-display font-bold text-lg mb-3" style={{ color: 'var(--aged-gold)' }}>{t('section.gocharPredictions')}</h4>
              <div className="flex flex-wrap items-end gap-3">
                <div>
                  <label className="text-sm block mb-1" style={{ color: 'var(--ink-light)' }}>{t('common.date')}</label>
                  <input
                    type="date"
                    value={transitDate}
                    onChange={(e) => setTransitDate(e.target.value)}
                    className="px-3 py-1.5 rounded-lg text-sm border"
                    style={{ backgroundColor: 'var(--cosmic-surface)', borderColor: 'rgba(184,134,11,0.3)', color: 'var(--ink)' }}
                  />
                </div>
                <div>
                  <label className="text-sm block mb-1" style={{ color: 'var(--ink-light)' }}>{t('common.time')}</label>
                  <input
                    type="time"
                    value={transitTime}
                    onChange={(e) => setTransitTime(e.target.value)}
                    className="px-3 py-1.5 rounded-lg text-sm border"
                    style={{ backgroundColor: 'var(--cosmic-surface)', borderColor: 'rgba(184,134,11,0.3)', color: 'var(--ink)' }}
                  />
                </div>
                <Button
                  size="sm"
                  onClick={() => {
                    refreshTransit(transitDate || undefined, transitTime ? `${transitTime}:00` : undefined);
                  }}
                  className="px-4"
                  style={{ backgroundColor: 'var(--aged-gold)', color: 'var(--parchment)' }}
                >
                  {transitDate ? t('transit.viewTransits') : t('transit.currentTransits')}
                </Button>
                {transitDate && (
                  <button
                    onClick={() => { resetTransitFilters(); }}
                    className="text-sm px-3 py-1.5 rounded-lg border"
                    style={{ borderColor: 'rgba(184,134,11,0.3)', color: 'var(--ink-light)' }}
                  >
                    {t('transit.resetToNow')}
                  </button>
                )}
              </div>
              {transitData && (
                <div className="flex flex-wrap gap-4 text-sm mt-3">
                  <span style={{ color: 'var(--ink)' }}><strong>{t('transit.transitDate')}:</strong> {transitData.transit_date}</span>
                  <span style={{ color: 'var(--ink)' }}><strong>{t('transit.natalMoon')}:</strong> {translateSign(transitData.natal_moon_sign, language)}</span>
                </div>
              )}
            </div>

            {loadingTransit ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-cosmic-text">{t('transit.loading')}</span>
              </div>
            ) : transitData ? (
              <div className="space-y-6">
                {/* 30-Day Forecast Heat Map */}
                {result?.id && (
                  <div className="mb-2 animate-in fade-in slide-in-from-top-4 duration-700">
                    <TransitHeatMap kundliId={result.id} t={t} language={language} />
                  </div>
                )}

                {/* Transit Chart + Table Side by Side */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
                  {/* Transit Chart — with view toggle */}
                  <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold shadow-sm">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="font-display font-semibold text-sacred-brown">{t('transit.chart')} ({transitData.transit_date})</h4>
                      <div className="flex bg-white rounded-lg p-1 border border-sacred-gold/30">
                        <button 
                          onClick={() => setViewMode('diamond')}
                          className={`px-3 py-1 text-[10px] font-bold rounded-md transition-all ${viewMode === 'diamond' ? 'bg-sacred-gold text-white' : 'text-sacred-gold-dark hover:bg-sacred-gold/10'}`}
                        >
                          DIAMOND
                        </button>
                        <button 
                          onClick={() => setViewMode('concentric')}
                          className={`px-3 py-1 text-[10px] font-bold rounded-md transition-all ${viewMode === 'concentric' ? 'bg-sacred-gold text-white' : 'text-sacred-gold-dark hover:bg-sacred-gold/10'}`}
                        >
                          CONCENTRIC
                        </button>
                      </div>
                    </div>

                    <div className="w-full max-w-[450px] mx-auto min-h-[400px] flex items-center justify-center">
                      {viewMode === 'diamond' ? (
                        <div className="w-full animate-in fade-in zoom-in-95 duration-500">
                          <p className="text-sm mb-3 text-center" style={{ color: 'var(--ink-light)' }}>{t('kundli.clickHouseToRotate')}</p>
                          {(() => {
                            const shift = transitHouseShift;
                            const transitPlanetsMap = (transitData.transits || []).map((tr: any) => ({
                              planet: tr.planet,
                              sign: tr.current_sign,
                              house: shift ? ((((tr.house || 1) - 1 - shift + 12) % 12) + 1) : (tr.house || 1),
                              nakshatra: tr.nakshatra || '',
                              sign_degree: tr.sign_degree || 0,
                              status: tr.is_retrograde ? 'Retrograde' : (tr.effect === 'favorable' ? 'Benefic' : 'Malefic'),
                              is_retrograde: !!tr.is_retrograde,
                            }));
                            const baseHouses = transitData.chart_data?.houses || result?.chart_data?.houses;
                            const transitHouses = shift && baseHouses
                              ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                              : baseHouses;
                            return (
                              <InteractiveKundli
                                chartData={{ planets: transitPlanetsMap, houses: transitHouses }}
                                onPlanetClick={() => {}}
                                onHouseClick={(house) => {
                                  const originalHouse = shift ? ((house - 1 + shift) % 12) + 1 : house;
                                  const newShift = originalHouse - 1;
                                  setTransitHouseShift(newShift === 0 ? 0 : newShift);
                                }}
                              />
                            );
                          })()}
                        </div>
                      ) : (
                        <div className="w-full animate-in fade-in zoom-in-95 duration-500">
                          <ConcentricChart natalPlanets={natalPlanets} transitPlanets={transitPlanets} />
                        </div>
                      )}
                    </div>
                    <div className="flex items-center justify-center gap-4 mt-4 text-sm text-cosmic-text">
                      <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: 'var(--aged-gold)'}} /> {t('transit.benefic')}</span>
                      <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: 'var(--wax-red)'}} /> {t('transit.malefic')}</span>
                      {transitHouseShift > 0 && viewMode === 'diamond' && (
                        <button onClick={() => setTransitHouseShift(0)} className="text-sm px-2 py-0.5 rounded border" style={{ borderColor: 'rgba(184,134,11,0.3)', color: 'var(--aged-gold)' }}>
                          {t('common.resetView')}
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Transit Table */}
                  <div className="rounded-xl border overflow-hidden shadow-sm h-fit" style={{ borderColor: 'rgba(184,134,11,0.25)', backgroundColor: 'white' }}>
                    <table className="w-full text-sm">
                      <thead>
                        <tr style={{ backgroundColor: 'rgba(184,134,11,0.08)' }}>
                          <th className="text-left p-3 font-display font-semibold" style={{ color: 'var(--ink)' }}>{t('table.planet')}</th>
                          <th className="text-left p-3 font-display font-semibold" style={{ color: 'var(--ink)' }}>{t('transit.currentSign')}</th>
                          <th className="text-center p-3 font-display font-semibold" style={{ color: 'var(--ink)' }}>{t('transit.houseFromMoon')}</th>
                          <th className="text-center p-3 font-display font-semibold" style={{ color: 'var(--ink)' }}>{t('transit.effect')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(transitData.transits || []).map((tr: any, idx: number) => (
                          <tr
                            key={idx}
                            className="border-t hover:bg-sacred-gold/5 transition-colors"
                            style={{ borderColor: 'rgba(184,134,11,0.15)', backgroundColor: idx % 2 === 0 ? 'transparent' : 'rgba(184,134,11,0.02)' }}
                          >
                            <td className="p-3 font-medium" style={{ color: 'var(--ink)' }}>{translatePlanet(tr.planet, language)}</td>
                            <td className="p-3" style={{ color: 'var(--ink-light)' }}>{translateSign(tr.current_sign, language)}</td>
                            <td className="p-3 text-center" style={{ color: 'var(--ink-light)' }}>{tr.natal_house_from_moon}</td>
                            <td className="p-3 text-center">
                              <span className={`inline-flex items-center gap-1 text-sm px-2 py-1 rounded-full font-medium ${tr.effect === 'favorable' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                {tr.effect === 'favorable' ? <CheckCircle className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
                                {tr.effect === 'favorable' ? t('common.favorable') : t('common.unfavorable')}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Detailed descriptions */}
                <div className="grid gap-3">
                  {(transitData.transits || []).map((tr: any, idx: number) => (
                    <div
                      key={idx}
                      className={`rounded-xl p-4 border shadow-sm transition-all hover:shadow-md ${tr.effect === 'favorable' ? 'border-green-300' : 'border-red-300'}`}
                      style={{ backgroundColor: tr.effect === 'favorable' ? 'rgba(34,197,94,0.03)' : 'rgba(239,68,68,0.03)' }}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-display font-semibold" style={{ color: 'var(--ink)' }}>{translatePlanet(tr.planet, language)}</span>
                        <span className="text-sm" style={{ color: 'var(--ink-light)' }}>{translateSign(tr.current_sign, language)}</span>
                        <span className={`text-sm px-1.5 py-0.5 rounded-full ${tr.effect === 'favorable' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {tr.effect === 'favorable' ? t('common.favorable') : t('common.unfavorable')}
                        </span>
                      </div>
                      <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{tr.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-center text-cosmic-text py-8">{t('transit.clickTab')}</p>
            )}

            {/* Retrograde Station Dates */}
            {result?.id && <RetrogradeStationsSection kundliId={result.id} />}
    </div>
  );
}
