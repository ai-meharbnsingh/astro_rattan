import { Loader2, CheckCircle, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import InteractiveKundli from '@/components/InteractiveKundli';
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

  return (
    <>
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
                {/* Transit Chart — clickable houses */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2">{t('transit.chart')} ({transitData.transit_date})</h4>
                  <p className="text-sm mb-3" style={{ color: 'var(--ink-light)' }}>{t('kundli.clickHouseToRotate')}</p>
                  <div className="w-full max-w-[600px] mx-auto">
                    {(() => {
                      const shift = transitHouseShift;
                      const transitPlanets = (transitData.transits || []).map((tr: any) => ({
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
                          chartData={{ planets: transitPlanets, houses: transitHouses }}
                          onPlanetClick={() => {}}
                          onHouseClick={(house) => {
                            // Clicking house X: shift so that house becomes house 1
                            const originalHouse = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            const newShift = originalHouse - 1;
                            setTransitHouseShift(newShift === 0 ? 0 : newShift);
                          }}
                        />
                      );
                    })()}
                  </div>
                  <div className="flex items-center justify-center gap-4 mt-2 text-sm text-cosmic-text">
                    <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: 'var(--aged-gold)'}} /> {t('transit.benefic')}</span>
                    <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: 'var(--wax-red)'}} /> {t('transit.malefic')}</span>
                    {transitHouseShift > 0 && (
                      <button onClick={() => setTransitHouseShift(0)} className="text-sm px-2 py-0.5 rounded border" style={{ borderColor: 'rgba(184,134,11,0.3)', color: 'var(--aged-gold)' }}>
                        {t('common.resetView')}
                      </button>
                    )}
                  </div>
                </div>

                {/* Transit Table */}
                <div className="rounded-xl border overflow-x-auto" style={{ borderColor: 'rgba(184,134,11,0.25)' }}>
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
                          className="border-t"
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

                {/* Detailed descriptions */}
                <div className="grid gap-3">
                  {(transitData.transits || []).map((tr: any, idx: number) => (
                    <div
                      key={idx}
                      className={`rounded-xl p-4 border ${tr.effect === 'favorable' ? 'border-green-300' : 'border-red-300'}`}
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
    </>
  );
}
