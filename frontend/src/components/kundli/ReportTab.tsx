import { Loader2, X, Download, Printer, CheckCircle, Shield, ScrollText, ChevronDown } from 'lucide-react';
import { formatDate } from '@/lib/api';
import { Button } from '@/components/ui/button';
import InteractiveKundli, { ChartLegend, type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { DIVISIONAL_CHART_OPTIONS } from '@/components/kundli/kundli-utils';
import { calculateJaiminiKarakas } from '@/components/kundli/jhora-utils';
import LordshipsTab from '@/components/kundli/LordshipsTab';
import ConsolidatedReport from '@/components/kundli/ConsolidatedReport';
import JHoraKundliView from '@/components/kundli/JHoraKundliView';
import { translatePlanet, translateSign, translateLabel, translateName } from '@/lib/backend-translations';

interface ReportTabProps {
  result: any;
  planets: any[];
  formData: { name: string; date: string; time: string; place: string };
  language: string;
  t: (key: string) => string;
  doshaData: any;
  loadingDosha: boolean;
  dashaData: any;
  loadingDasha: boolean;
  extendedDashaData: any;
  loadingExtendedDasha: boolean;
  avakhadaData: any;
  loadingAvakhada: boolean;
  yogaDoshaData: any;
  loadingYogaDosha: boolean;
  ashtakvargaData: any;
  loadingAshtakvarga: boolean;
  shadbalaData: any;
  loadingShadbala: boolean;
  divisionalData: any;
  loadingDivisional: boolean;
  transitData: any;
  loadingTransit: boolean;
  d10Data: any;
  loadingD10: boolean;
  selectedDivision: string;
  reportLagnaShift: number;
  setReportLagnaShift: (v: number) => void;
  reportMoonShift: number;
  setReportMoonShift: (v: number) => void;
  reportGocharShift: number;
  setReportGocharShift: (v: number) => void;
  expandedMahadasha: string | null;
  setExpandedMahadasha: (v: string | null) => void;
  expandedAntardasha: string | null;
  setExpandedAntardasha: (v: string | null) => void;
  jhoraOpen: boolean;
  setJhoraOpen: (v: boolean) => void;
  reportOpen: boolean;
  setReportOpen: (v: boolean) => void;
  fetchTransit: () => void;
  fetchD10: () => void;
  fetchDasha: () => void;
  fetchExtendedDasha: () => void;
  changeDivision: (code: string) => void;
  handlePlanetClick: (planet: any) => void;
  handleHouseClick: (house: number, sign: string, planets: any[]) => void;
}

export default function ReportTab({
  result, planets, formData, language, t,
  doshaData, loadingDosha,
  dashaData, loadingDasha,
  extendedDashaData, loadingExtendedDasha,
  avakhadaData, loadingAvakhada,
  yogaDoshaData, loadingYogaDosha,
  ashtakvargaData, loadingAshtakvarga,
  shadbalaData, loadingShadbala,
  divisionalData, loadingDivisional,
  transitData, loadingTransit,
  d10Data, loadingD10,
  selectedDivision,
  reportLagnaShift, setReportLagnaShift,
  reportMoonShift, setReportMoonShift,
  reportGocharShift, setReportGocharShift,
  expandedMahadasha, setExpandedMahadasha,
  expandedAntardasha, setExpandedAntardasha,
  jhoraOpen, setJhoraOpen,
  reportOpen, setReportOpen,
  fetchTransit, fetchD10, fetchDasha, fetchExtendedDasha,
  changeDivision,
  handlePlanetClick, handleHouseClick,
}: ReportTabProps) {
  return (
            <div className="space-y-6">
              {/* View Buttons */}
              <div className="flex justify-center gap-3">
                <Button
                  size="lg"
                  className="bg-sacred-gold text-black hover:bg-sacred-gold-light px-8"
                  onClick={() => {
                    fetchTransit();
                    fetchD10();
                    fetchDasha();
                    fetchExtendedDasha();
                    setJhoraOpen(true);
                  }}
                >
                  <ScrollText className="w-5 h-5 mr-2" />
                  {t('kundli.jhoraView')}
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-sacred-gold text-sacred-gold hover:bg-gold-10 px-8"
                  onClick={() => {
                    fetchTransit();
                    setReportOpen(true);
                  }}
                >
                  <ScrollText className="w-5 h-5 mr-2" />
                  {t('kundli.fullReport')}
                </Button>
              </div>

              {/* JHora-style Fullscreen Overlay */}
              {jhoraOpen && (
                <div className="fixed inset-0 z-[9999] bg-parchment" style={{ width: '100vw', height: '100vh' }}>
                  <button onClick={() => setJhoraOpen(false)} className="absolute top-2 right-3 z-10 p-1.5 hover:bg-black rounded text-sacred-gold text-sm font-bold" title="Close">
                    <X className="w-5 h-5" />
                  </button>
                    <JHoraKundliView
                      result={result}
                      planets={planets}
                      dashaData={dashaData}
                      extendedDashaData={extendedDashaData}
                      avakhadaData={avakhadaData}
                      yogaDoshaData={yogaDoshaData}
                      ashtakvargaData={ashtakvargaData}
                      shadbalaData={shadbalaData}
                      divisionalData={divisionalData}
                      d10Data={d10Data}
                      transitData={transitData}
                      loadingDasha={loadingDasha}
                      loadingExtendedDasha={loadingExtendedDasha}
                      loadingAvakhada={loadingAvakhada}
                      loadingYogaDosha={loadingYogaDosha}
                      loadingAshtakvarga={loadingAshtakvarga}
                      loadingShadbala={loadingShadbala}
                      loadingDivisional={loadingDivisional}
                      loadingD10={loadingD10}
                      loadingTransit={loadingTransit}
                      onBack={() => setJhoraOpen(false)}
                      onDownloadPDF={async () => {}}
                    />
                </div>
              )}

              {/* Consolidated Report Popup */}
              <ConsolidatedReport
                open={reportOpen}
                onOpenChange={setReportOpen}
                result={result}
                planets={planets}
                dashaData={dashaData}
                avakhadaData={avakhadaData}
                yogaDoshaData={yogaDoshaData}
                ashtakvargaData={ashtakvargaData}
                shadbalaData={shadbalaData}
                divisionalData={divisionalData}
                loadingDasha={loadingDasha}
                loadingAvakhada={loadingAvakhada}
                loadingYogaDosha={loadingYogaDosha}
                loadingAshtakvarga={loadingAshtakvarga}
                loadingShadbala={loadingShadbala}
                loadingDivisional={loadingDivisional}
              />

              {/* Action bar */}
              <div className="flex flex-wrap gap-3 justify-end">
                <Button size="sm" className="btn-sacred" onClick={async () => {
                  try {
                    const token = localStorage.getItem('astrovedic_token');
                    const API_BASE = import.meta.env.VITE_API_URL || '';
                    const resp = await fetch(`${API_BASE}/api/kundli/${result.id}/pdf`, {
                      headers: token ? { Authorization: `Bearer ${token}` } : {},
                    });
                    if (!resp.ok) {
                      const err = await resp.json().catch(() => ({ detail: resp.statusText }));
                      throw new Error(err.detail || 'PDF download failed');
                    }
                    const blob = await resp.blob();
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `kundli-${result.person_name || 'report'}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                  } catch (e: any) {
                    console.error('PDF download error:', e);
                    alert(e.message || 'Failed to download PDF');
                  }
                }}>
                  <Download className="w-4 h-4 mr-1" />{t('common.downloadPDF')}
                </Button>
                <Button size="sm" variant="outline" className="border-sacred-gold text-sacred-brown" onClick={() => window.print()}>
                  <Printer className="w-4 h-4 mr-1" />{t('common.printReport')}
                </Button>
              </div>

              {/* Report title */}
              <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold rounded-xl p-5 border border-sacred-gold text-center">
                <h3 className="font-display font-bold text-xl text-sacred-brown">{t('section.consolidatedReport')}</h3>
                <p className="text-sm text-cosmic-text mt-1">{result.person_name} | {formatDate(result.birth_date)} | {result.birth_time} | {result.birth_place}</p>
              </div>

              {/* Charts row — Lagna, Moon, Gochar side by side */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 print:grid-cols-3">
                {/* 1. Lagna Chart (D1) — click house to rotate lagan */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">
                    {t('section.lagna')}
                  </h4>
                  <div className="flex justify-center">
                    {(() => {
                      const shift = reportLagnaShift;
                      const basePlanets = planets;
                      const baseHouses = result.chart_data?.houses;
                      const shiftedPlanets = shift
                        ? basePlanets.map((p: PlanetData) => ({
                            ...p,
                            house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                          }))
                        : basePlanets;
                      const shiftedHouses = shift && baseHouses
                        ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                        : baseHouses;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: shiftedPlanets, houses: shiftedHouses, ascendant: result.chart_data?.ascendant } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            setReportLagnaShift(orig - 1 === 0 ? 0 : orig - 1);
                          }}
                          compact
                        />
                      );
                    })()}
                  </div>
                  {reportLagnaShift > 0 && (
                    <button onClick={() => setReportLagnaShift(0)} className="block mx-auto mt-1 text-sm text-sacred-gold underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 2. Moon Chart — click house to rotate lagan */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">
                    {t('section.moon')}
                  </h4>
                  <div className="flex justify-center">
                    {(() => {
                      const moonPlanet = planets.find((p: PlanetData) => p.planet === 'Moon');
                      const moonHouse = moonPlanet?.house || 1;
                      const baseShift = moonHouse - 1;
                      const totalShift = baseShift + reportMoonShift;
                      const moonPlanets = planets.map((p: PlanetData) => ({
                        ...p,
                        house: ((((p.house || 1) - 1 - totalShift + 24) % 12) + 1),
                      }));
                      const moonHouses = result.chart_data?.houses
                        ? result.chart_data.houses.map((h: { number: number; sign: string }) => ({
                            number: ((h.number - 1 - totalShift + 24) % 12) + 1,
                            sign: h.sign,
                          }))
                        : undefined;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: moonPlanets, houses: moonHouses } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = totalShift ? ((house - 1 + totalShift) % 12) + 1 : house;
                            const newShift = ((orig - 1) - baseShift + 12) % 12;
                            setReportMoonShift(newShift);
                          }}
                          compact
                        />
                      );
                    })()}
                  </div>
                  {reportMoonShift > 0 && (
                    <button onClick={() => setReportMoonShift(0)} className="block mx-auto mt-1 text-sm text-sacred-gold underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 3. Gochar (Transit) Chart — click house to rotate lagan */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">
                    {t('section.gochar')} {transitData?.transit_date ? `(${transitData.transit_date})` : ''}
                    <span className="text-sm font-normal text-gray-500"> ({t('kundli.clickHouseToRotate')})</span>
                  </h4>
                  <div className="flex justify-center">
                    {loadingTransit ? (
                      <div className="flex items-center justify-center py-12"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                    ) : transitData?.transits ? (() => {
                      const shift = reportGocharShift;
                      const transitPlanets = transitData.transits.map((tr: any) => ({
                        planet: tr.planet,
                        sign: tr.current_sign || tr.sign || '',
                        house: tr.house || 1,
                        nakshatra: tr.nakshatra || '',
                        sign_degree: tr.sign_degree || tr.degree || 0,
                        status: tr.is_retrograde ? 'Retrograde' : '',
                        is_retrograde: tr.is_retrograde,
                      }));
                      const baseHouses = transitData.chart_data?.houses || result.chart_data?.houses;
                      const shiftedPlanets = shift
                        ? transitPlanets.map((p: any) => ({
                            ...p,
                            house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                          }))
                        : transitPlanets;
                      const shiftedHouses = shift && baseHouses
                        ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                        : baseHouses;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: shiftedPlanets, houses: shiftedHouses } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            setReportGocharShift(orig - 1 === 0 ? 0 : orig - 1);
                          }}
                          compact
                        />
                      );
                    })() : (
                      <p className="text-center text-cosmic-text py-12 text-sm">{t('common.loading')}</p>
                    )}
                  </div>
                  {reportGocharShift > 0 && (
                    <button onClick={() => setReportGocharShift(0)} className="block mx-auto mt-1 text-sm text-sacred-gold underline">{t('common.resetView')}</button>
                  )}
                </div>
              </div>

              {/* Chart Legend */}
              <ChartLegend />

              {/* Grid layout — 2 columns on desktop, 1 on mobile */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 print:grid-cols-2">

                {/* 2. Planet Details Table */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.detailedPlanetPositions')}</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-sacred-gold">
                        <tr>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.sign')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.house')}</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.nakshatra')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.degree')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.status')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {planets.map((planet: any, index: number) => (
                          <tr key={index} className="border-t border-sacred-gold hover:bg-sacred-gold">
                            <td className="p-2 text-sacred-brown font-medium">{translatePlanet(planet.planet, language)}</td>
                            <td className="p-2 text-cosmic-text">{translateSign(planet.sign, language)}</td>
                            <td className="p-2 text-center text-cosmic-text">{planet.house}</td>
                            <td className="p-2 text-cosmic-text">{planet.nakshatra || '\u2014'}</td>
                            <td className="p-2 text-center text-cosmic-text">{planet.sign_degree?.toFixed(1)}&deg;</td>
                            <td className="p-2 text-center">
                              <span className={`text-sm px-2.5 py-0.5 rounded-full font-medium ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-100 text-green-800' : 'text-cosmic-text'}`}>
                                {translateLabel(planet.status, language) || '\u2014'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* 3. Divisional Chart (D9 default, dropdown for all) */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-display font-semibold text-sacred-brown">{t('kundli.divisionalCharts')}</h4>
                    <select
                      value={selectedDivision}
                      onChange={(e) => changeDivision(e.target.value)}
                      className="bg-cosmic-surface border border-sacred-gold rounded-lg px-3 py-1.5 text-sacred-brown text-sm focus:border-sacred-gold focus:outline-none"
                    >
                      {DIVISIONAL_CHART_OPTIONS.map((c) => (
                        <option key={c.code} value={c.code}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  {loadingDivisional ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : divisionalData?.planet_positions ? (
                    <div className="flex justify-center">
                      <InteractiveKundli
                        chartData={{
                          planets: divisionalData.planet_positions.map((p: any) => ({
                            planet: p.planet,
                            sign: p.sign,
                            house: p.house,
                            nakshatra: p.nakshatra || '',
                            sign_degree: p.sign_degree || 0,
                            status: '',
                          })),
                          houses: divisionalData.houses || Array.from({ length: 12 }, (_, i) => ({
                            number: i + 1,
                            sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
                          })),
                        } as ChartData}
                        onPlanetClick={handlePlanetClick}
                        onHouseClick={handleHouseClick}
                      />
                    </div>
                  ) : (
                    <p className="text-center text-cosmic-text py-8 text-sm">{t('kundli.selectChart')}</p>
                  )}
                </div>

                {/* 4. Lordships */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.houseLordships')}</h4>
                  <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
                </div>

                {/* 5. Avakhada Chakra */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.avakhadaChakra')}</h4>
                  {loadingAvakhada ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : avakhadaData ? (
                    <div className="grid grid-cols-2 gap-2">
                      {[
                        { label: t('avakhada.ascendant'), value: avakhadaData.ascendant },
                        { label: t('avakhada.ascendantLord'), value: avakhadaData.ascendant_lord },
                        { label: t('avakhada.rashi'), value: avakhadaData.rashi },
                        { label: t('avakhada.rashiLord'), value: avakhadaData.rashi_lord },
                        { label: t('avakhada.nakshatra'), value: `${avakhadaData.nakshatra} (P${avakhadaData.nakshatra_pada})` },
                        { label: t('avakhada.yoga'), value: avakhadaData.yoga },
                        { label: t('avakhada.karana'), value: avakhadaData.karana },
                        { label: t('avakhada.yoni'), value: avakhadaData.yoni },
                        { label: t('avakhada.gana'), value: avakhadaData.gana },
                        { label: t('avakhada.nadi'), value: avakhadaData.nadi },
                        { label: t('avakhada.varna'), value: avakhadaData.varna },
                        { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
                        { label: t('avakhada.sunSign'), value: avakhadaData.sun_sign },
                      ].map((item) => (
                        <div key={item.label} className="rounded-lg p-2 bg-cosmic-card">
                          <p className="text-sm text-cosmic-text">{item.label}</p>
                          <p className="text-sm font-semibold text-sacred-brown">{item.value}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center text-cosmic-text py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 6. Vimshottari Dasha — with expandable AD/PD */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.vimshottariDasha')}</h4>
                  {(loadingDasha || loadingExtendedDasha) ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : (extendedDashaData || dashaData) ? (
                    <div className="space-y-2">
                      {/* Current dasha info */}
                      <div className="rounded-lg p-3 bg-gold-10">
                        <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{t('section.currentMahadasha')}</p>
                        <p className="text-sm font-display font-bold" style={{ color: 'var(--aged-gold)' }}>
                          {(extendedDashaData || dashaData).current_dasha}
                        </p>
                        {(extendedDashaData || dashaData).current_antardasha && (extendedDashaData || dashaData).current_antardasha !== 'Unknown' && (
                          <p className="text-sm" style={{ color: 'var(--aged-gold)' }}>
                            AD: {(extendedDashaData || dashaData).current_antardasha}
                            {extendedDashaData?.current_pratyantar && extendedDashaData.current_pratyantar !== 'Unknown' && ` / PD: ${extendedDashaData.current_pratyantar}`}
                          </p>
                        )}
                      </div>

                      {/* Expandable Mahadasha list */}
                      {extendedDashaData?.mahadasha ? (
                        <div className="space-y-1">
                          {extendedDashaData.mahadasha.map((md: any) => (
                            <div key={md.planet} className="border border-sacred-gold rounded-lg overflow-hidden">
                              <button
                                onClick={() => setExpandedMahadasha(expandedMahadasha === md.planet ? null : md.planet)}
                                className="w-full flex items-center justify-between p-2 text-sm transition-colors"
                                style={{ background: md.is_current ? 'rgba(184,134,11,0.12)' : 'transparent' }}
                              >
                                <span className="flex items-center gap-1.5">
                                  <ChevronDown className={`w-3 h-3 transition-transform ${expandedMahadasha === md.planet ? 'rotate-180' : ''}`} style={{ color: 'var(--aged-gold)' }} />
                                  <span className="font-semibold" style={{ color: md.is_current ? 'var(--aged-gold)' : 'var(--ink)' }}>
                                    {translatePlanet(md.planet, language)} {md.is_current ? '←' : ''}
                                  </span>
                                </span>
                                <span style={{ color: 'var(--ink-light)' }}>{md.start?.slice(0,10)} — {md.end?.slice(0,10)} ({md.years}y)</span>
                              </button>

                              {expandedMahadasha === md.planet && (md.antardasha || []).length > 0 && (
                                <div className="border-t border-sacred-gold">
                                  {md.antardasha.map((ad: any) => (
                                    <div key={`${md.planet}-${ad.planet}`}>
                                      <button
                                        onClick={() => setExpandedAntardasha(expandedAntardasha === `${md.planet}-${ad.planet}` ? null : `${md.planet}-${ad.planet}`)}
                                        className="w-full flex items-center justify-between px-4 py-1.5 text-sm"
                                        style={{ background: ad.is_current ? 'rgba(184,134,11,0.06)' : 'transparent' }}
                                      >
                                        <span className="flex items-center gap-1">
                                          {ad.pratyantar?.length > 0 && <ChevronDown className={`w-2.5 h-2.5 transition-transform ${expandedAntardasha === `${md.planet}-${ad.planet}` ? 'rotate-180' : ''}`} style={{ color: 'var(--ink-light)' }} />}
                                          <span style={{ color: ad.is_current ? 'var(--aged-gold)' : 'var(--ink)' }}>{translatePlanet(ad.planet, language)} AD {ad.is_current ? '*' : ''}</span>
                                        </span>
                                        <span style={{ color: 'var(--ink-light)', fontSize: 'var(--text-label, 0.875rem)' }}>{ad.start?.slice(0,10)} — {ad.end?.slice(0,10)}</span>
                                      </button>

                                      {expandedAntardasha === `${md.planet}-${ad.planet}` && (ad.pratyantar || []).length > 0 && (
                                        <div className="border-t border-sacred-gold">
                                          {ad.pratyantar.map((pt: any, idx: number) => (
                                            <div key={idx} className="flex items-center justify-between px-8 py-1 text-sm"
                                              style={{ background: pt.is_current ? 'rgba(184,134,11,0.04)' : 'transparent' }}>
                                              <span style={{ color: pt.is_current ? 'var(--aged-gold)' : 'var(--ink-light)' }}>
                                                {translatePlanet(pt.planet, language)} PD {pt.is_current ? '*' : ''}
                                              </span>
                                              <span style={{ color: 'var(--ink-light)', fontSize: 'var(--text-label, 0.875rem)' }}>{pt.start?.slice(0,10)} — {pt.end?.slice(0,10)}</span>
                                            </div>
                                          ))}
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : (
                        /* Fallback: simple table when extendedDashaData unavailable */
                        <div className="overflow-x-auto">
                          <table className="w-full text-sm">
                            <thead><tr className="bg-gold-10">
                              <th className="text-left p-2 font-medium" style={{ color: 'var(--aged-gold)' }}>{t('table.planet')}</th>
                              <th className="text-left p-2 font-medium" style={{ color: 'var(--aged-gold)' }}>{t('table.start')}</th>
                              <th className="text-left p-2 font-medium" style={{ color: 'var(--aged-gold)' }}>{t('table.end')}</th>
                              <th className="text-center p-2 font-medium" style={{ color: 'var(--aged-gold)' }}>{t('table.years')}</th>
                            </tr></thead>
                            <tbody>
                              {(dashaData.mahadasha_periods || []).map((p: any) => (
                                <tr key={p.planet} className="border-t border-sacred-gold" style={{ background: p.planet === dashaData.current_dasha ? 'rgba(184,134,11,0.1)' : 'transparent' }}>
                                  <td className="p-2" style={{ color: 'var(--ink)' }}>{translatePlanet(p.planet, language)}{p.planet === dashaData.current_dasha ? ' ←' : ''}</td>
                                  <td className="p-2" style={{ color: 'var(--ink-light)' }}>{p.start_date}</td>
                                  <td className="p-2" style={{ color: 'var(--ink-light)' }}>{p.end_date}</td>
                                  <td className="p-2 text-center" style={{ color: 'var(--ink-light)' }}>{p.years}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-center py-4 text-sm" style={{ color: 'var(--ink-light)' }}>{t('common.loading')}</p>
                  )}
                </div>

                {/* 6b. Jaimini Karakas — separate card */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.jaiminiKarakas')}</h4>
                  {(() => {
                    const karakas = calculateJaiminiKarakas(planets);
                    const karakaOrder = [
                      { key: 'AK', name: 'Atmakaraka' },
                      { key: 'AmK', name: 'Amatyakaraka' },
                      { key: 'BK', name: 'Bhratrikaraka' },
                      { key: 'MK', name: 'Matrikaraka' },
                      { key: 'PiK', name: 'Pitrikaraka' },
                      { key: 'GnK', name: 'Gnatikaraka' },
                      { key: 'DK', name: 'Darakaraka' },
                    ];
                    return (
                      <table className="w-full text-sm">
                        <thead><tr className="bg-sacred-gold">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.karaka')}</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                        </tr></thead>
                        <tbody>
                          {karakaOrder.map(({ key, name }) => {
                            const planet = Object.entries(karakas).find(([, v]) => v === key)?.[0] || '-';
                            return (
                              <tr key={key} className="border-t border-sacred-gold">
                                <td className="p-2 text-sacred-brown"><span className="font-semibold">{key}</span> <span className="text-sm text-cosmic-text">({name})</span></td>
                                <td className="p-2 font-semibold" style={{ color: 'var(--aged-gold-dim)' }}>{translatePlanet(planet, language)}</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    );
                  })()}
                </div>

                {/* 7. Yoga & Dosha */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4 lg:col-span-2">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.yogasAndDoshas')}</h4>
                  {loadingYogaDosha ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : yogaDoshaData ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <CheckCircle className="w-4 h-4 text-green-500" />
                          <h5 className="text-sm font-semibold text-sacred-brown">{t('section.yogas')}</h5>
                        </div>
                        <div className="space-y-1">
                          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).slice(0, 8).map((yoga: any, idx: number) => (
                            <div key={idx} className="rounded-lg p-2 text-sm border border-green-300 bg-green-500">
                              <div className="flex items-center justify-between">
                                <span className="font-medium text-sacred-brown">{translateName(yoga.name, language)}</span>
                                <span className="text-sm px-1.5 py-0.5 rounded-full bg-green-100 text-green-800">
                                  {t('common.present')}
                                </span>
                              </div>
                            </div>
                          ))}
                          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).length === 0 && (
                            <p className="text-sm text-cosmic-text py-2">{t('kundli.noYogasDetected')}</p>
                          )}
                        </div>
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <Shield className="w-4 h-4 text-red-500" />
                          <h5 className="text-sm font-semibold text-sacred-brown">{t('section.doshas')}</h5>
                        </div>
                        <div className="space-y-1">
                          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).slice(0, 8).map((dosha: any, idx: number) => (
                            <div key={idx} className="rounded-lg p-2 text-sm border border-red-300 bg-red-500">
                              <div className="flex items-center justify-between">
                                <span className="font-medium text-sacred-brown">{translateName(dosha.name, language)}</span>
                                <span className="text-sm px-1.5 py-0.5 rounded-full bg-red-100 text-red-800">
                                  {t('common.present')}
                                </span>
                              </div>
                            </div>
                          ))}
                          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).length === 0 && (
                            <p className="text-sm text-green-400 py-2">{t('kundli.noDoshasDetected')}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-cosmic-text py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 7b. Mangal / Kaal Sarp / Sade Sati Dosha */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4 lg:col-span-2">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.doshaAnalysis')}</h4>
                  {loadingDosha ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : doshaData ? (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {/* Mangal Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.mangal_dosha?.has_dosha ? 'border-red-300 bg-red-500' : 'border-green-300 bg-green-500'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">{translateName('Mangal Dosha', language)}</h5>
                          <span className={`text-sm px-2 py-0.5 rounded-full font-medium ${doshaData.mangal_dosha?.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaData.mangal_dosha?.has_dosha ? translateLabel(doshaData.mangal_dosha.severity, language) || t('common.present') : t('common.absent')}
                          </span>
                        </div>
                        <p className="text-sm text-cosmic-text">{doshaData.mangal_dosha?.description || t('kundli.noMangalDosha')}</p>
                      </div>
                      {/* Kaal Sarp Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.kaal_sarp_dosha?.has_dosha ? 'border-red-300 bg-red-500' : 'border-green-300 bg-green-500'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">{translateName('Kaal Sarp Dosha', language)}</h5>
                          <span className={`text-sm px-2 py-0.5 rounded-full font-medium ${doshaData.kaal_sarp_dosha?.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaData.kaal_sarp_dosha?.has_dosha ? translateLabel(doshaData.kaal_sarp_dosha.severity, language) || t('common.present') : t('common.absent')}
                          </span>
                        </div>
                        <p className="text-sm text-cosmic-text">{doshaData.kaal_sarp_dosha?.description || t('kundli.noKaalSarpDosha')}</p>
                      </div>
                      {/* Sade Sati */}
                      <div className={`rounded-lg p-3 border ${doshaData.sade_sati?.has_sade_sati ? 'border-orange-500 bg-orange-500' : 'border-green-300 bg-green-500'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">{translateName('Sade Sati', language)}</h5>
                          <span className={`text-sm px-2 py-0.5 rounded-full font-medium ${doshaData.sade_sati?.has_sade_sati ? 'bg-orange-100 text-orange-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaData.sade_sati?.has_sade_sati ? `${t('common.active')} - ${translateLabel(doshaData.sade_sati.phase, language)}` : t('common.inactive')}
                          </span>
                        </div>
                        <p className="text-sm text-cosmic-text">{doshaData.sade_sati?.description || t('kundli.sadeSatiNotActive')}</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-cosmic-text py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 8. Ashtakvarga SAV bar chart */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.sarvashtakvarga')}</h4>
                  {loadingAshtakvarga ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : ashtakvargaData ? (
                    <div>
                      <div className="flex items-end gap-1 h-36">
                        {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map((sign) => {
                          const points = ashtakvargaData.sarvashtakvarga?.[sign] || 0;
                          const maxPoints = 56;
                          const heightPct = Math.round((points / maxPoints) * 100);
                          const isStrong = points >= 28;
                          return (
                            <div key={sign} className="flex-1 flex flex-col items-center gap-0.5">
                              <span className="text-sm font-medium text-sacred-brown">{points}</span>
                              <div className="w-full bg-sacred-gold rounded-t-sm relative" style={{ height: '100px' }}>
                                <div
                                  className="absolute bottom-0 w-full rounded-t-sm"
                                  style={{ height: `${heightPct}%`, backgroundColor: isStrong ? 'var(--aged-gold-dim)' : 'var(--ink-light)' }}
                                />
                              </div>
                              <span className="text-sm text-cosmic-text">{sign.slice(0, 3)}</span>
                            </div>
                          );
                        })}
                      </div>
                      <div className="flex items-center gap-3 mt-2 text-sm text-cosmic-text">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />{t('kundli.strong')}</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--ink-light)' }} />{t('kundli.weak')}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-cosmic-text py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 9. Shadbala bar chart */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.shadbalaStrength')}</h4>
                  {loadingShadbala ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : shadbalaData?.planets ? (
                    <div className="space-y-2">
                      {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                        const data = shadbalaData.planets[planet];
                        if (!data) return null;
                        const pct = Math.min((data.total / data.required) * 100, 150);
                        const barColor = data.is_strong ? 'var(--aged-gold-dim)' : '#8B2332';
                        return (
                          <div key={planet} className="flex items-center gap-2">
                            <span className="w-12 text-sm font-medium text-sacred-brown">{translatePlanet(planet, language)}</span>
                            <div className="flex-1 bg-sacred-gold rounded-full h-4 overflow-hidden">
                              <div className="h-full rounded-full" style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }} />
                            </div>
                            <span className={`text-sm w-16 text-right font-medium ${data.is_strong ? 'text-sacred-gold-dark' : 'text-wax-red-deep'}`}>
                              {data.total}/{data.required}
                            </span>
                          </div>
                        );
                      })}
                      <div className="flex items-center gap-3 mt-1 text-sm text-cosmic-text">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />{t('kundli.strong')}</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#8B2332' }} />{t('kundli.weak')}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-cosmic-text py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

              </div>
            </div>
  );
}
