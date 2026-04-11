import { useState, useEffect, useCallback } from 'react';
import { X, Download, Printer, Loader2, CheckCircle, Shield } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { api, formatDate } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateNakshatra, translateName, translateRemedy, translateLabel, translateBackend } from '@/lib/backend-translations';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import LordshipsTab from '@/components/kundli/LordshipsTab';

interface ConsolidatedReportProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  result: any;
  planets: PlanetData[];
  // Pre-fetched data from parent
  dashaData: any;
  avakhadaData: any;
  yogaDoshaData: any;
  ashtakvargaData: any;
  shadbalaData: any;
  divisionalData: any;
  // Loading states
  loadingDasha: boolean;
  loadingAvakhada: boolean;
  loadingYogaDosha: boolean;
  loadingAshtakvarga: boolean;
  loadingShadbala: boolean;
  loadingDivisional: boolean;
}

export default function ConsolidatedReport({
  open,
  onOpenChange,
  result,
  planets,
  dashaData,
  avakhadaData,
  yogaDoshaData,
  ashtakvargaData,
  shadbalaData,
  divisionalData,
  loadingDasha,
  loadingAvakhada,
  loadingYogaDosha,
  loadingAshtakvarga,
  loadingShadbala,
  loadingDivisional,
}: ConsolidatedReportProps) {
  const { t, language } = useTranslation();

  // Local state for transit and D10
  const [transitData, setTransitData] = useState<any>(null);
  const [loadingTransit, setLoadingTransit] = useState(false);
  const [d10Data, setD10Data] = useState<any>(null);
  const [loadingD10, setLoadingD10] = useState(false);
  const [gocharShift, setGocharShift] = useState(0);
  const [d1Shift, setD1Shift] = useState(0);
  const [d9Shift, setD9Shift] = useState(0);
  const [d10Shift, setD10Shift] = useState(0);

  // New modules states
  const [yoginiData, setYoginiData] = useState<any>(null);
  const [loadingYogini, setLoadingYogini] = useState(false);

  const [sadesatiData, setSadesatiData] = useState<any>(null);
  const [loadingSadesati, setLoadingSadesati] = useState(false);

  const [kpData, setKpData] = useState<any>(null);
  const [loadingKp, setLoadingKp] = useState(false);

  const [varshphalData, setVarshphalData] = useState<any>(null);
  const [loadingVarshphal, setLoadingVarshphal] = useState(false);

  const [upagrahasData, setUpagrahasData] = useState<any>(null);
  const [loadingUpagrahas, setLoadingUpagrahas] = useState(false);

  const [sodashvargaData, setSodashvargaData] = useState<any>(null);
  const [loadingSodashvarga, setLoadingSodashvarga] = useState(false);

  const [aspectsData, setAspectsData] = useState<any>(null);
  const [loadingAspects, setLoadingAspects] = useState(false);

  const fetchTransit = useCallback(async () => {
    if (!result?.id || transitData) return;
    setLoadingTransit(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/transits`, {});
      setTransitData(data);
    } catch (e) { console.error(e); }
    setLoadingTransit(false);
  }, [result?.id, transitData]);

  const fetchD10 = useCallback(async () => {
    if (!result?.id || d10Data) return;
    setLoadingD10(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: 'D10' });
      setD10Data(data);
    } catch (e) { console.error(e); }
    setLoadingD10(false);
  }, [result?.id, d10Data]);

  const fetchYogini = useCallback(async () => {
    if (!result?.id || yoginiData) return;
    setLoadingYogini(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/yogini-dasha`);
      setYoginiData(data);
    } catch (e) { console.error(e); }
    setLoadingYogini(false);
  }, [result?.id, yoginiData]);

  const fetchSadesati = useCallback(async () => {
    if (!result?.id || sadesatiData) return;
    setLoadingSadesati(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/lifelong-sadesati`);
      setSadesatiData(data);
    } catch (e) { console.error(e); }
    setLoadingSadesati(false);
  }, [result?.id, sadesatiData]);

  const fetchKp = useCallback(async () => {
    if (!result?.id || kpData) return;
    setLoadingKp(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/kp-analysis`, {});
      setKpData(data);
    } catch (e) { console.error(e); }
    setLoadingKp(false);
  }, [result?.id, kpData]);

  const fetchVarshphal = useCallback(async () => {
    if (!result?.id || varshphalData) return;
    setLoadingVarshphal(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/varshphal`, {});
      setVarshphalData(data);
    } catch (e) { console.error(e); }
    setLoadingVarshphal(false);
  }, [result?.id, varshphalData]);

  const fetchUpagrahas = useCallback(async () => {
    if (!result?.id || upagrahasData) return;
    setLoadingUpagrahas(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/upagrahas`);
      setUpagrahasData(data);
    } catch (e) { console.error(e); }
    setLoadingUpagrahas(false);
  }, [result?.id, upagrahasData]);

  const fetchSodashvarga = useCallback(async () => {
    if (!result?.id || sodashvargaData) return;
    setLoadingSodashvarga(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/sodashvarga`);
      setSodashvargaData(data);
    } catch (e) { console.error(e); }
    setLoadingSodashvarga(false);
  }, [result?.id, sodashvargaData]);

  const fetchAspects = useCallback(async () => {
    if (!result?.id || aspectsData) return;
    setLoadingAspects(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/aspects`);
      setAspectsData(data);
    } catch (e) { console.error(e); }
    setLoadingAspects(false);
  }, [result?.id, aspectsData]);

  // Fetch transit, D10, and new modules when popup opens
  useEffect(() => {
    if (open && result?.id) {
      fetchTransit();
      fetchD10();
      fetchYogini();
      fetchSadesati();
      fetchKp();
      fetchVarshphal();
      fetchUpagrahas();
      fetchSodashvarga();
      fetchAspects();
    }
  }, [open, result?.id, fetchTransit, fetchD10, fetchYogini, fetchSadesati, fetchKp, fetchVarshphal, fetchUpagrahas, fetchSodashvarga, fetchAspects]);

  const handleDownloadPDF = async () => {
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
  };

  // Build transit chart data (include houses + ascendant for rotation)
  const ZODIAC = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  const transitChartDataRaw: ChartData | null = transitData?.transits
    ? (() => {
        const asc = transitData.chart_data?.ascendant || result?.chart_data?.ascendant;
        let houses = transitData.chart_data?.houses || result?.chart_data?.houses;
        // Generate houses from ascendant if missing
        if (!houses && asc?.sign) {
          const ascIdx = ZODIAC.indexOf(asc.sign);
          houses = Array.from({ length: 12 }, (_, i) => ({
            number: i + 1,
            sign: ZODIAC[(ascIdx + i) % 12],
          }));
        }
        return {
          planets: transitData.transits.map((tr: any) => ({
            planet: tr.planet,
            sign: tr.current_sign || tr.sign || 'Aries',
            house: tr.house_from_moon || tr.house || 1,
            nakshatra: tr.nakshatra || '',
            sign_degree: tr.degree || 0,
            status: tr.effect || '',
          })),
          houses,
          ascendant: asc,
        };
      })()
    : null;

  // Build D10 chart data
  const d10ChartData: ChartData | null = d10Data?.planet_positions
    ? {
        planets: d10Data.planet_positions.map((p: any) => ({
          planet: p.planet,
          sign: p.sign,
          house: p.house,
          nakshatra: p.nakshatra || '',
          sign_degree: p.sign_degree || 0,
          status: '',
        })),
        houses: Array.from({ length: 12 }, (_, i) => ({
          number: i + 1,
          sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
        })),
      }
    : null;

  // Build D9 chart data from divisionalData
  const d9ChartData: ChartData | null = divisionalData?.planet_positions
    ? {
        planets: divisionalData.planet_positions.map((p: any) => ({
          planet: p.planet,
          sign: p.sign,
          house: p.house,
          nakshatra: p.nakshatra || '',
          sign_degree: p.sign_degree || 0,
          status: '',
        })),
        houses: Array.from({ length: 12 }, (_, i) => ({
          number: i + 1,
          sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
        })),
      }
    : null;

  // Only present yogas
  const presentYogas = (yogaDoshaData?.yogas || []).filter((y: any) => y.present);
  // Only present doshas
  const presentDoshas = (yogaDoshaData?.doshas || []).filter((d: any) => d.present || d.has_dosha);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        className="max-w-[98vw] sm:max-w-[98vw] max-h-[95vh] w-full bg-cosmic-surface overflow-y-auto p-0 border-sacred-purple"
        showCloseButton={false}
      >
        {/* Print styles */}
        <style>{`
          @media print {
            @page { size: landscape; margin: 0.5cm; }
            body * { visibility: hidden; }
            [data-slot="dialog-content"], [data-slot="dialog-content"] * { visibility: visible; }
            [data-slot="dialog-content"] { position: fixed; left: 0; top: 0; width: 100%; max-width: 100%; max-height: none; transform: none; border: none; box-shadow: none; }
            .no-print { display: none !important; }
          }
        `}</style>

        {/* Header bar */}
        <div className="sticky top-0 z-10 bg-cosmic-surface border-b border-sacred-purple px-6 py-3 flex items-center justify-between no-print">
          <div className="flex items-center gap-3">
            <Button size="sm" onClick={handleDownloadPDF} className="bg-sacred-gold-dark text-white hover:bg-gray-50 dark text-sm h-8">
              <Download className="w-3.5 h-3.5 mr-1" />{t('common.downloadPDF')}
            </Button>
            <Button size="sm" variant="outline" onClick={() => window.print()} className="border-sacred-purple text-cosmic-text text-sm h-8">
              <Printer className="w-3.5 h-3.5 mr-1" />{t('common.printReport')}
            </Button>
          </div>
          <DialogTitle className="text-sm font-semibold text-sacred-gold-dark font-serif">
            {t('section.consolidatedReport')}
          </DialogTitle>
          <button onClick={() => onOpenChange(false)} className="p-1.5 hover:bg-sacred-purple rounded transition-colors">
            <X className="w-5 h-5 text-cosmic-text" />
          </button>
        </div>

        {/* Report content */}
        <div className="px-6 py-4 space-y-4" style={{ color: 'var(--ink)' }}>
          {/* Title block */}
          <div className="text-center border-b border-sacred-purple pb-3">
            <h2 className="text-lg font-bold font-serif" style={{ color: 'var(--aged-gold-dim)' }}>
              {result?.person_name} — {t('section.vedicBirthChart')}
            </h2>
            <p className="text-data text-cosmic-text mt-1">
              {result?.birth_date} | {result?.birth_time} | {result?.birth_place}
            </p>
          </div>

          {/* Row 1: Four charts */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-1">
            {/* Birth Chart (D1) */}
            <div className="border border-sacred-purple rounded-lg p-1">
              <h4 className="text-data font-bold text-center mb-1" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.rashiD1')} <span className="text-sm font-normal text-gray-500">{t('report.clickHouseLagan')}</span>
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '100%', margin: '0 auto' }}>
                {(() => {
                  const shift = d1Shift;
                  const basePlanets = planets;
                  const baseHouses = result?.chart_data?.houses;
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
                      chartData={{ planets: shiftedPlanets, houses: shiftedHouses, ascendant: result?.chart_data?.ascendant } as ChartData}
                      compact
                      onHouseClick={(house) => {
                        const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                        setD1Shift(orig - 1 === 0 ? 0 : orig - 1);
                      }}
                    />
                  );
                })()}
              </div>
              {d1Shift > 0 && (
                <button onClick={() => setD1Shift(0)} className="block mx-auto mt-1 text-sm text-sacred-gold-dark underline">{t('common.resetView')}</button>
              )}
            </div>

            {/* D9 Navamsha */}
            <div className="border border-sacred-purple rounded-lg p-1">
              <h4 className="text-data font-bold text-center mb-1" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.navamshaD9')} <span className="text-sm font-normal text-gray-500">{t('report.clickHouseLagan')}</span>
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '100%', margin: '0 auto' }}>
                {loadingDivisional ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
                ) : d9ChartData ? (() => {
                  const shift = d9Shift;
                  const shiftedPlanets = shift
                    ? d9ChartData.planets.map((p: PlanetData) => ({
                        ...p,
                        house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                      }))
                    : d9ChartData.planets;
                  const shiftedHouses = shift && d9ChartData.houses
                    ? d9ChartData.houses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                    : d9ChartData.houses;
                  return (
                    <InteractiveKundli
                      chartData={{ planets: shiftedPlanets, houses: shiftedHouses } as ChartData}
                      compact
                      onHouseClick={(house) => {
                        const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                        setD9Shift(orig - 1 === 0 ? 0 : orig - 1);
                      }}
                    />
                  );
                })() : (
                  <p className="text-sm text-center py-12 text-cosmic-text">{t('common.loading')}</p>
                )}
              </div>
              {d9Shift > 0 && (
                <button onClick={() => setD9Shift(0)} className="block mx-auto mt-1 text-sm text-sacred-gold-dark underline">{t('common.resetView')}</button>
              )}
            </div>

            {/* D10 Dashamsha */}
            <div className="border border-sacred-purple rounded-lg p-1">
              <h4 className="text-data font-bold text-center mb-1" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('kundli.d10')} <span className="text-sm font-normal text-gray-500">{t('report.clickHouseLagan')}</span>
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '100%', margin: '0 auto' }}>
                {loadingD10 ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
                ) : d10ChartData ? (() => {
                  const shift = d10Shift;
                  const shiftedPlanets = shift
                    ? d10ChartData.planets.map((p: PlanetData) => ({
                        ...p,
                        house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                      }))
                    : d10ChartData.planets;
                  const shiftedHouses = shift && d10ChartData.houses
                    ? d10ChartData.houses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                    : d10ChartData.houses;
                  return (
                    <InteractiveKundli
                      chartData={{ planets: shiftedPlanets, houses: shiftedHouses } as ChartData}
                      compact
                      onHouseClick={(house) => {
                        const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                        setD10Shift(orig - 1 === 0 ? 0 : orig - 1);
                      }}
                    />
                  );
                })() : (
                  <p className="text-sm text-center py-12 text-cosmic-text">{t('common.loading')}</p>
                )}
              </div>
              {d10Shift > 0 && (
                <button onClick={() => setD10Shift(0)} className="block mx-auto mt-1 text-sm text-sacred-gold-dark underline">{t('common.resetView')}</button>
              )}
            </div>

            {/* Gochar (Transit) — clickable */}
            <div className="border border-sacred-purple rounded-lg p-1">
              <h4 className="text-data font-bold text-center mb-1" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('kundli.gochar')} <span className="text-sm font-normal text-gray-500">{t('report.clickHouseLagan')}</span>
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '100%', margin: '0 auto' }}>
                {loadingTransit ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
                ) : transitChartDataRaw ? (() => {
                  const shift = gocharShift;
                  const shiftedPlanets = shift
                    ? transitChartDataRaw.planets.map((p: PlanetData) => ({
                        ...p,
                        house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                      }))
                    : transitChartDataRaw.planets;
                  const baseHouses = transitChartDataRaw.houses;
                  const shiftedHouses = shift && baseHouses
                    ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                    : baseHouses;
                  return (
                    <InteractiveKundli
                      chartData={{ planets: shiftedPlanets, houses: shiftedHouses, ascendant: transitChartDataRaw.ascendant }}
                      compact
                      onHouseClick={(house) => {
                        const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                        setGocharShift(orig - 1 === 0 ? 0 : orig - 1);
                      }}
                    />
                  );
                })() : (
                  <p className="text-sm text-center py-12 text-cosmic-text">{t('common.loading')}</p>
                )}
              </div>
              {gocharShift > 0 && (
                <button onClick={() => setGocharShift(0)} className="block mx-auto mt-1 text-sm text-sacred-gold-dark underline">{t('common.resetView')}</button>
              )}
            </div>
          </div>

          {/* Row 2: Planet Table (full width) */}
          <div className="border border-sacred-purple rounded-lg p-3">
            <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
              {t('section.detailedPlanetPositions')}
            </h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ backgroundColor: 'var(--aged-gold-dim)', color: 'white' }}>
                    <th className="text-left p-1.5 font-medium">{t('table.planet')}</th>
                    <th className="text-left p-1.5 font-medium">{t('table.sign')}</th>
                    <th className="text-center p-1.5 font-medium whitespace-nowrap">{t('table.degree')}</th>
                    <th className="text-left p-1.5 font-medium">{t('table.nakshatra')}</th>
                    <th className="text-center p-1.5 font-medium">{t('table.status')}</th>
                    <th className="text-center p-1.5 font-medium">{t('table.nature')}</th>
                    <th className="text-center p-1.5 font-medium">{t('table.house')}</th>
                  </tr>
                </thead>
                <tbody>
                  {planets.map((planet, index) => {
                    const isBenefic = ['Jupiter', 'Venus', 'Moon', 'Mercury'].includes(planet.planet);
                    return (
                      <tr key={index} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                        <td className="p-1.5 font-medium" style={{ color: 'var(--ink)' }}>{translatePlanet(planet.planet, language)}</td>
                        <td className="p-1.5" style={{ color: 'var(--ink)' }}>{translateSign(planet.sign, language)}</td>
                        <td className="p-1.5 text-center whitespace-nowrap">{(Number(planet.sign_degree) || 0).toFixed(1)}°</td>
                        <td className="p-1.5">{translateNakshatra(planet.nakshatra, language) || '\u2014'}</td>
                        <td className="p-1.5 text-center">
                          <span className={`text-sm px-1 py-0.5 rounded ${
                            planet.status === 'Exalted' || planet.status === 'Own Sign'
                              ? 'bg-green-100 text-green-800'
                              : planet.status === 'Debilitated'
                              ? 'bg-red-100 text-red-800'
                              : 'text-cosmic-text'
                          }`}>
                            {planet.status ? translateLabel(planet.status, language) : '\u2014'}
                          </span>
                        </td>
                        <td className="p-1.5 text-center">
                          <span className={`text-sm ${isBenefic ? 'text-green-400' : 'text-red-400'}`}>
                            {isBenefic ? t('kundli.benefic') : t('kundli.malefic')}
                          </span>
                        </td>
                        <td className="p-1.5 text-center">{planet.house}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Row 3: Avakhada Chakra + Vimshottari Dasha + Yogini Dasha */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {/* Avakhada Chakra */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('avakhada.title')}
              </h4>
              {loadingAvakhada ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : avakhadaData ? (
                <div className="grid grid-cols-2 gap-1.5">
                  {[
                    { label: t('avakhada.ascendant'), value: translateSign(avakhadaData.ascendant, language) },
                    { label: t('avakhada.ascendantLord'), value: translatePlanet(avakhadaData.ascendant_lord, language) },
                    { label: t('avakhada.rashi'), value: translateSign(avakhadaData.rashi, language) },
                    { label: t('avakhada.rashiLord'), value: translatePlanet(avakhadaData.rashi_lord, language) },
                    { label: t('avakhada.nakshatra'), value: `${translateNakshatra(avakhadaData.nakshatra, language)} (P${avakhadaData.nakshatra_pada})` },
                    { label: t('avakhada.yoga'), value: translateBackend(avakhadaData.yoga, language) },
                    { label: t('avakhada.karana'), value: translateBackend(avakhadaData.karana, language) },
                    { label: t('avakhada.yoni'), value: translateBackend(avakhadaData.yoni, language) },
                    { label: t('avakhada.gana'), value: translateBackend(avakhadaData.gana, language) },
                    { label: t('avakhada.nadi'), value: translateBackend(avakhadaData.nadi, language) },
                    { label: t('avakhada.varna'), value: translateBackend(avakhadaData.varna, language) },
                    { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
                  ].map((item) => (
                    <div key={item.label} className="bg-cosmic-bg rounded px-2 py-1">
                      <p className="text-sm text-cosmic-text">{item.label}</p>
                      <p className="text-sm font-semibold text-cosmic-text">{item.value || '\u2014'}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>

            {/* Vimshottari Dasha */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.vimshottariDasha')}
              </h4>
              {loadingDasha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : dashaData ? (
                <div>
                  <div className="bg-sacred-gold-dark rounded px-2 py-1.5 mb-2">
                    <p className="text-sm text-cosmic-text">{t('section.currentMahadasha')}</p>
                    <p className="text-data font-bold" style={{ color: 'var(--aged-gold-dim)' }}>{translatePlanet(dashaData.current_dasha, language)}</p>
                    {dashaData.current_antardasha && (
                      <p className="text-sm text-sacred-gold-dark">{t('report.adLabel')} {translatePlanet(dashaData.current_antardasha, language)}</p>
                    )}
                  </div>
                  <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ backgroundColor: 'var(--parchment)' }}>
                        <th className="text-left p-1 font-medium text-sacred-gold-dark">{t('table.planet')}</th>
                        <th className="text-left p-1 font-medium text-sacred-gold-dark">{t('table.start')}</th>
                        <th className="text-left p-1 font-medium text-sacred-gold-dark">{t('table.end')}</th>
                        <th className="text-center p-1 font-medium text-sacred-gold-dark">{t('table.years')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(dashaData.mahadasha_periods || []).map((p: any) => (
                        <tr key={p.planet} style={{
                          borderBottom: '1px solid var(--sacred-purple)',
                          backgroundColor: p.planet === dashaData.current_dasha ? 'var(--aged-gold-dim-10, rgba(180, 83, 9, 0.06))' : undefined,
                        }}>
                          <td className="p-1 font-medium">{translatePlanet(p.planet, language)}{p.planet === dashaData.current_dasha ? ' \u2190' : ''}</td>
                          <td className="p-1 text-cosmic-text">{p.start_date}</td>
                          <td className="p-1 text-cosmic-text">{p.end_date}</td>
                          <td className="p-1 text-center text-cosmic-text">{p.years}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>

            {/* Yogini Dasha */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.yoginiDasha')}
              </h4>
              {loadingYogini ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : yoginiData ? (
                <div>
                  <div className="bg-sacred-gold-dark rounded px-2 py-1.5 mb-2">
                    <p className="text-sm text-cosmic-text">{t('report.currentDasha')}</p>
                    <p className="text-data font-bold" style={{ color: 'var(--aged-gold-dim)' }}>{yoginiData.current_dasha?.planet ? translatePlanet(yoginiData.current_dasha.planet, language) : '\u2014'}</p>
                    {yoginiData.current_dasha?.planet && (
                      <p className="text-sm text-sacred-gold-dark">{t('report.untilLabel')} {yoginiData.current_dasha?.end_date}</p>
                    )}
                  </div>
                  <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ backgroundColor: 'var(--parchment)' }}>
                        <th className="text-left p-1 font-medium text-sacred-gold-dark">{t('table.yogini')}</th>
                        <th className="text-left p-1 font-medium text-sacred-gold-dark">{t('table.planet')}</th>
                        <th className="text-left p-1 font-medium text-sacred-gold-dark">{t('table.start')}</th>
                        <th className="text-left p-1 font-medium text-sacred-gold-dark">{t('table.end')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(yoginiData.periods || []).map((p: any) => (
                        <tr key={p.name + p.start_date} style={{
                          borderBottom: '1px solid var(--sacred-purple)',
                          backgroundColor: p.name === yoginiData.current_dasha?.name && p.start_date === yoginiData.current_dasha?.start_date ? 'var(--aged-gold-dim-10, rgba(180, 83, 9, 0.06))' : undefined,
                        }}>
                          <td className="p-1 font-medium">{translateName(p.name, language)}{p.name === yoginiData.current_dasha?.name && p.start_date === yoginiData.current_dasha?.start_date ? ' \u2190' : ''}</td>
                          <td className="p-1 text-cosmic-text">{translatePlanet(p.planet, language)} ({p.span}y)</td>
                          <td className="p-1 text-cosmic-text">{p.start_date}</td>
                          <td className="p-1 text-cosmic-text">{p.end_date}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 4: Yogas + Doshas + Lifelong Sade Sati + Lordships */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {/* Yogas (present only) */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2 flex items-center gap-1" style={{ color: 'var(--aged-gold-dim)' }}>
                <CheckCircle className="w-3 h-3 text-green-500" />
                {t('section.yogas')}
              </h4>
              {loadingYogaDosha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : presentYogas.length > 0 ? (
                <div className="space-y-1">
                  {presentYogas.map((yoga: any, idx: number) => (
                    <div key={idx} className="bg-green-500 border border-green-300 rounded px-2 py-1">
                      <span className="text-sm font-medium text-green-400">{translateName(yoga.name, language)}</span>
                      {yoga.description && (
                         <p className="text-sm text-green-400 mt-0.5">{translateBackend(yoga.description, language)}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-center py-4 text-cosmic-text">{t('yoga.noneDetected')}</p>
              )}
            </div>

            {/* Doshas (present only) */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2 flex items-center gap-1" style={{ color: 'var(--aged-gold-dim)' }}>
                <Shield className="w-3 h-3 text-red-500" />
                {t('section.doshas')}
              </h4>
              {loadingYogaDosha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : presentDoshas.length > 0 ? (
                <div className="space-y-1">
                  {presentDoshas.map((dosha: any, idx: number) => (
                    <div key={idx} className="bg-red-500 border border-red-300 rounded px-2 py-1">
                      <span className="text-sm font-medium text-red-400">{translateName(dosha.name, language)}</span>
                      {dosha.remedies && (
                        <p className="text-sm text-red-400 mt-0.5">{t('dosha.remedies')}: {translateRemedy(dosha.remedies, language)}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-center py-4 text-green-400">{t('dosha.nonePresent')}</p>
              )}
            </div>

            {/* Lifelong Sade Sati */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2 flex items-center gap-1" style={{ color: 'var(--aged-gold-dim)' }}>
                <Shield className="w-3 h-3 text-sacred-gold-dark" />
                {t('section.lifelongSadeSati')}
              </h4>
              {loadingSadesati ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : sadesatiData ? (
                <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
                  {sadesatiData.phases && sadesatiData.phases.length > 0 ? (
                    <div className="space-y-1.5">
                      {sadesatiData.phases.map((ph: any, idx: number) => (
                        <div key={idx} className="bg-cosmic-bg rounded px-2 py-1">
                          <p className="text-sm text-sacred-gold-dark font-medium">{translateLabel(ph.phase, language)} {t('report.phaseLabel')}</p>
                          <p className="text-sm text-cosmic-text">{ph.start_date} \u2192 {ph.end_date}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-center py-4 text-green-400">{t('sadesati.noPhases')}</p>
                  )}
                  {sadesatiData.remedies && sadesatiData.remedies.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-sacred-purple">
                      <p className="text-sm font-semibold text-sacred-gold-dark mb-1">{t('section.generalRemedies')}</p>
                      <ul className="list-disc pl-3 space-y-0.5 text-micro text-cosmic-text">
                        {sadesatiData.remedies.map((rem: string, idx: number) => (
                          <li key={idx}>{translateRemedy(rem, language)}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-sm text-center py-4 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>

            {/* Lordships */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.houseLordships')}
              </h4>
              <div className="text-sm">
                <LordshipsTab planets={planets} houses={result?.chart_data?.houses || {}} />
              </div>
            </div>
          </div>

          {/* Row 5: Ashtakvarga SAV + Shadbala */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            {/* Ashtakvarga SAV */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.sarvashtakvarga')}
              </h4>
              {loadingAshtakvarga ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : ashtakvargaData ? (
                <div>
                  <div className="flex items-end gap-0.5 h-28">
                    {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map((sign) => {
                      const points = ashtakvargaData.sarvashtakvarga?.[sign] || 0;
                      const maxPoints = 56;
                      const heightPct = Math.round((points / maxPoints) * 100);
                      const isStrong = points >= 28;
                      return (
                        <div key={sign} className="flex-1 flex flex-col items-center gap-0.5">
                          <span className="text-sm font-medium text-cosmic-text">{points}</span>
                          <div className="w-full bg-sacred-purple rounded-t-sm relative" style={{ height: '80px' }}>
                            <div
                              className="absolute bottom-0 w-full rounded-t-sm"
                              style={{ height: `${heightPct}%`, backgroundColor: isStrong ? 'var(--aged-gold-dim)' : 'var(--ink-light)' }}
                            />
                          </div>
                          <span className="text-micro text-cosmic-text">{(translateSign(sign, language) || sign || '').slice(0, 3)}</span>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-sm text-cosmic-text">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />{t('dignity.strong')}</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--ink-light)' }} />{t('dignity.weak')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>

            {/* Shadbala */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.shadbalaStrength')}
              </h4>
              {loadingShadbala ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : shadbalaData?.planets ? (
                <div className="space-y-1.5">
                  {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                    const data = shadbalaData.planets[planet];
                    if (!data) return null;
                    const pct = Math.min((data.total / data.required) * 100, 150);
                    const barColor = data.is_strong ? 'var(--aged-gold-dim)' : 'var(--wax-red)';
                    return (
                      <div key={planet} className="flex items-center gap-1.5">
                        <span className="w-10 text-sm font-medium text-cosmic-text">{translatePlanet(planet, language)}</span>
                        <div className="flex-1 bg-sacred-purple rounded-full h-3 overflow-hidden">
                          <div className="h-full rounded-full" style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }} />
                        </div>
                        <span className={`text-sm w-12 text-right font-medium ${data.is_strong ? 'text-sacred-gold-dark' : 'text-sacred-maroon'}`}>
                          {data.total}/{data.required}
                        </span>
                      </div>
                    );
                  })}
                  <div className="flex items-center gap-3 mt-1 text-sm text-cosmic-text">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />{t('dignity.strong')}</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--wax-red)' }} />{t('dignity.weak')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>
          </div>
          {/* Row 6: KP Analysis + Varshphal */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mt-3">
            {/* KP Analysis */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.kpAnalysis')}
              </h4>
              {loadingKp ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : kpData ? (
                <div className="space-y-4 max-h-64 overflow-y-auto pr-1">
                  <div>
                    <h5 className="text-sm font-semibold text-sacred-gold-dark mb-1">{t('section.planetarySignificators')}</h5>
                    <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                      <thead style={{ backgroundColor: 'var(--parchment)' }}>
                        <tr>
                          <th className="text-left p-1 text-cosmic-text-secondary">{t('table.planet')}</th>
                          <th className="text-left p-1 text-cosmic-text-secondary">{t('table.starLord')}</th>
                          <th className="text-left p-1 text-cosmic-text-secondary">{t('table.subLord')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(kpData.planets || []).map((p: any) => (
                          <tr key={p.planet} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                            <td className="p-1 text-cosmic-text">{translatePlanet(p.planet, language)}</td>
                            <td className="p-1 text-cosmic-text">{p.nakshatra_lord ? translatePlanet(p.nakshatra_lord, language) : '-'}</td>
                            <td className="p-1 text-cosmic-text">{p.sub_lord ? translatePlanet(p.sub_lord, language) : '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div>
                    <h5 className="text-sm font-semibold text-sacred-gold-dark mb-1">{t('section.houseCusps')}</h5>
                    <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                      <thead style={{ backgroundColor: 'var(--parchment)' }}>
                        <tr>
                          <th className="text-left p-1 text-cosmic-text-secondary">{t('table.cusp')}</th>
                          <th className="text-left p-1 text-cosmic-text-secondary">{t('table.starLord')}</th>
                          <th className="text-left p-1 text-cosmic-text-secondary">{t('table.subLord')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(kpData.houses || []).map((h: any) => (
                          <tr key={h.cusp} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                            <td className="p-1 text-cosmic-text">H{h.cusp}</td>
                            <td className="p-1 text-cosmic-text">{h.nakshatra_lord ? translatePlanet(h.nakshatra_lord, language) : '-'}</td>
                            <td className="p-1 text-cosmic-text">{h.sub_lord ? translatePlanet(h.sub_lord, language) : '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>

            {/* Varshphal (Annual Return) */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.varshphalCurrentYear')}
              </h4>
              {loadingVarshphal ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : varshphalData ? (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-cosmic-bg rounded px-2 py-1.5 border border-sacred-purple">
                      <p className="text-sm text-cosmic-text">{t('section.munthaSign')}</p>
                      <p className="text-data font-bold text-sacred-gold-dark">{varshphalData.muntha?.sign ? translateSign(varshphalData.muntha.sign, language) : 'N/A'}</p>
                    </div>
                    <div className="bg-cosmic-bg rounded px-2 py-1.5 border border-sacred-purple">
                      <p className="text-sm text-cosmic-text">{t('section.munthaLord')}</p>
                      <p className="text-data font-bold text-sacred-gold-dark">{varshphalData.muntha?.lord ? translatePlanet(varshphalData.muntha.lord, language) : 'N/A'}</p>
                    </div>
                    <div className="bg-cosmic-bg rounded px-2 py-1.5 border border-sacred-purple">
                      <p className="text-sm text-cosmic-text">{t('section.yearLord')}</p>
                      <p className="text-data font-bold text-sacred-gold-dark">{varshphalData.year_lord ? translatePlanet(varshphalData.year_lord, language) : 'N/A'}</p>
                    </div>
                  </div>
                  {varshphalData.mudda_dasha && (
                    <div>
                      <h5 className="text-sm font-semibold text-sacred-gold-dark mb-1">{t('section.muddaDasha')}</h5>
                      <div className="bg-cosmic-bg p-2 rounded max-h-32 overflow-y-auto w-full">
                        <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                           <tbody>
                             {varshphalData.mudda_dasha.map((md: any) => (
                               <tr key={md.planet} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                                 <td className="p-1 font-medium">{translatePlanet(md.planet, language)}</td>
                                 <td className="p-1 text-cosmic-text">{formatDate(md.start_date)} - {formatDate(md.end_date)}</td>
                               </tr>
                             ))}
                           </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 7: Upagrahas */}
          <div className="grid grid-cols-1 mt-3">
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.upagrahasTitle')}
              </h4>
              {loadingUpagrahas ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : upagrahasData?.upagrahas ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                    <thead style={{ backgroundColor: 'var(--parchment)' }}>
                      <tr>
                        <th className="text-left p-1.5 text-cosmic-text-secondary">{t('tab.upagrahas')}</th>
                        <th className="text-left p-1.5 text-cosmic-text-secondary">{t('table.longitude')}</th>
                        <th className="text-left p-1.5 text-cosmic-text-secondary">{t('table.sign')}</th>
                        <th className="text-left p-1.5 text-cosmic-text-secondary">{t('table.nakshatra')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {['Dhooma', 'Vyatipata', 'Parivesha', 'Indrachapa', 'Upaketu', 'Gulika', 'Mandi']
                        .filter(name => upagrahasData.upagrahas[name])
                        .map((name: string) => {
                        const u = upagrahasData.upagrahas[name];
                        return (
                          <tr key={name} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                            <td className="p-1.5 font-medium text-cosmic-text">{name}</td>
                            <td className="p-1.5 text-cosmic-text">{u.sign_degree?.toFixed(2)}°</td>
                            <td className="p-1.5 text-cosmic-text">{translateSign(u.sign, language)}</td>
                            <td className="p-1.5 text-cosmic-text">{translateNakshatra(u.nakshatra, language)} P{u.nakshatra_pada}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 8: Sodashvarga — By Sign (16 Divisional Charts Table) */}
          <div className="grid grid-cols-1 mt-3">
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.sodashvargaTitle')}
              </h4>
              {loadingSodashvarga ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : sodashvargaData?.varga_table ? (
                <div className="space-y-4">
                  {/* By Sign Table */}
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                      <thead>
                        <tr style={{ backgroundColor: 'var(--aged-gold-dim)', color: 'white' }}>
                          <th className="text-left p-1.5 font-medium sticky left-0" style={{ backgroundColor: 'var(--aged-gold-dim)', minWidth: '80px' }}>{t('table.varga')}</th>
                          {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'].map(p => (
                            <th key={p} className="text-center p-1.5 font-medium" style={{ minWidth: '50px' }}>{(translatePlanet(p, language) || p).slice(0, 3)}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {(sodashvargaData.varga_table || []).map((row: any) => (
                          <tr key={row.division} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                            <td className="p-1.5 font-medium text-sacred-gold-dark sticky left-0" style={{ backgroundColor: 'var(--cosmic-surface)' }}>
                              {row.name}
                            </td>
                            {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'].map(planet => {
                              const sign = row.planets?.[planet] || '-';
                              const dignity = sodashvargaData.by_sign?.[planet]?.[String(row.division)]?.dignity || '';
                              const dignityStyle = dignity === 'exalted'
                                ? { color: '#065f46', backgroundColor: '#d1fae5' }       // green bg + dark green text
                                : dignity === 'own' || dignity === 'moolatrikona'
                                ? { color: '#92400e', backgroundColor: '#fef3c7' }       // amber bg + dark amber text
                                : dignity === 'debilitated'
                                ? { color: '#991b1b', backgroundColor: '#fee2e2' }       // red bg + dark red text
                                : dignity === 'friend'
                                ? { color: '#1e40af', backgroundColor: '#dbeafe' }       // blue bg + dark blue text
                                : dignity === 'enemy'
                                ? { color: '#9a3412', backgroundColor: '#ffedd5' }       // orange bg + dark orange text
                                : { color: 'var(--ink)' };
                              return (
                                <td key={planet} className="p-1.5 text-center" style={dignityStyle} title={dignity ? translateLabel(dignity, language) : ''}>
                                  {sign === '-' ? '-' : (translateSign(sign, language) || (typeof sign === 'string' ? sign : '')).slice(0, 3)}
                                </td>
                              );
                            })}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  {/* Legend */}
                  <div className="flex flex-wrap gap-3 text-sm text-cosmic-text">
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#d1fae5', border: '1px solid #065f46' }} />{t('dignity.exalted')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#fef3c7', border: '1px solid #92400e' }} />{t('report.ownMT')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#dbeafe', border: '1px solid #1e40af' }} />{t('dignity.friend')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#ffedd5', border: '1px solid #9a3412' }} />{t('dignity.enemy')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#fee2e2', border: '1px solid #991b1b' }} />{t('dignity.debilitated')}</span>
                  </div>

                  {/* Vimshopak Bala (By Planet) */}
                  <div>
                    <h5 className="text-sm font-semibold text-sacred-gold-dark mb-2">{t('section.vimshopakBala')}</h5>
                    <div className="space-y-1">
                      {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
                        .filter(p => sodashvargaData.by_planet?.[p])
                        .map(planet => {
                          const data = sodashvargaData.by_planet[planet];
                          const pct = Math.min((data.vimshopak_bala / 20.0) * 100, 100);
                          const barColor = data.strength === 'Strong' ? 'var(--aged-gold-dim)' : data.strength === 'Medium' ? '#f59e0b' : 'var(--wax-red)';
                          return (
                            <div key={planet} className="flex items-center gap-1.5">
                              <span className="w-12 text-sm font-medium text-cosmic-text">{translatePlanet(planet, language)}</span>
                              <div className="flex-1 bg-sacred-purple rounded-full h-2.5 overflow-hidden">
                                <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: barColor }} />
                              </div>
                              <span className={`text-sm w-16 text-right font-medium`} style={{ color: barColor }}>
                                {data.vimshopak_bala} ({translateLabel(data.strength, language)})
                              </span>
                            </div>
                          );
                        })}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 9: Aspects on Planets + Aspects on Bhavas */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mt-3">
            {/* Aspects on Planets */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.aspectsOnPlanets')}
              </h4>
              {loadingAspects ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : aspectsData?.planet_aspects_summary ? (
                <div className="overflow-y-auto max-h-72 space-y-2">
                  {Object.entries(aspectsData.planet_aspects_summary).map(([planet, data]: [string, any]) => (
                    <div key={planet} className="bg-cosmic-bg rounded px-2 py-1.5 border border-sacred-purple">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-semibold text-cosmic-text">{translatePlanet(planet, language)} <span className="text-sm text-cosmic-text">(H{data.house})</span></span>
                        <div className="flex gap-2">
                          <span className="text-sm px-1.5 py-0.5 rounded bg-green-100 text-green-800">
                            {data.benefic_aspects} {t('report.beneficCount')}
                          </span>
                          <span className="text-sm px-1.5 py-0.5 rounded bg-red-100 text-red-800">
                            {data.malefic_aspects} {t('report.maleficCount')}
                          </span>
                        </div>
                      </div>
                      {data.aspected_by && data.aspected_by.length > 0 ? (
                        <div className="flex flex-wrap gap-1 mt-1">
                          {data.aspected_by.map((a: any, i: number) => {
                            const isBenefic = ['Jupiter', 'Venus', 'Moon', 'Mercury'].includes(a.planet);
                            return (
                              <span
                                key={i}
                                className="text-sm px-1.5 py-0.5 rounded"
                                style={{
                                  backgroundColor: isBenefic ? 'rgba(34,197,94,0.1)' : 'rgba(239,68,68,0.1)',
                                  color: isBenefic ? '#4ade80' : '#f87171',
                                }}
                              >
                                {translatePlanet(a.planet, language)} ({translateBackend(a.type, language)})
                              </span>
                            );
                          })}
                        </div>
                      ) : (
                        <p className="text-sm text-cosmic-text mt-0.5">{t('report.noAspectsReceived')}</p>
                      )}
                      {/* Houses this planet aspects */}
                      {data.aspects_to && data.aspects_to.length > 0 && (
                        <div className="mt-1 pt-1 border-t border-sacred-purple">
                          <span className="text-sm text-sacred-gold-dark">{t('report.aspectsTo')} </span>
                          {data.aspects_to.map((a: any, i: number) => (
                            <span key={i} className="text-sm text-cosmic-text">
                              H{a.house}
                              {a.planets_in_house && a.planets_in_house.length > 0 && (
                                <span className="text-sacred-gold-dark"> ({a.planets_in_house.map((p: string) => translatePlanet(p, language)).join(', ')})</span>
                              )}
                              {i < data.aspects_to.length - 1 ? ', ' : ''}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>

            {/* Aspects on Bhavas */}
            <div className="border border-sacred-purple rounded-lg p-3">
              <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                {t('section.aspectsOnBhavas')}
              </h4>
              {loadingAspects ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold-dark" /></div>
              ) : aspectsData?.bhava_summary ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ backgroundColor: 'var(--parchment)' }}>
                        <th className="text-left p-1.5 text-cosmic-text-secondary">{t('table.bhava')}</th>
                        <th className="text-left p-1.5 text-cosmic-text-secondary">{t('table.planets')}</th>
                        <th className="text-left p-1.5 text-cosmic-text-secondary">{t('table.aspectedBy')}</th>
                        <th className="text-center p-1.5 text-cosmic-text-secondary">B</th>
                        <th className="text-center p-1.5 text-cosmic-text-secondary">M</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(aspectsData.bhava_summary || []).map((bh: any) => (
                        <tr key={bh.house} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                          <td className="p-1.5 font-medium text-sacred-gold-dark">H{bh.house}</td>
                          <td className="p-1.5 text-cosmic-text">
                            {bh.planets_in_house && bh.planets_in_house.length > 0
                              ? bh.planets_in_house.map((p: string) => translatePlanet(p, language)).join(', ')
                              : <span className="text-cosmic-text">—</span>}
                          </td>
                          <td className="p-1.5 text-cosmic-text">
                            {bh.aspected_by && bh.aspected_by.length > 0
                              ? bh.aspected_by.map((p: string) => translatePlanet(p, language)).join(', ')
                              : <span className="text-cosmic-text">—</span>}
                          </td>
                          <td className="p-1.5 text-center">
                            <span className="text-green-400">{bh.benefic_aspects || 0}</span>
                          </td>
                          <td className="p-1.5 text-center">
                            <span className="text-red-400">{bh.malefic_aspects || 0}</span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  <div className="flex gap-3 mt-1 text-sm text-cosmic-text">
                    <span>{t('report.beneficAspectsLabel')}</span>
                    <span>{t('report.maleficAspectsLabel')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-cosmic-text">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 10: Bhinnashtakvarga Detail Table */}
          {ashtakvargaData?.planet_bindus && (
            <div className="grid grid-cols-1 mt-3">
              <div className="border border-sacred-purple rounded-lg p-3">
                <h4 className="text-data font-bold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                  {t('section.bhinnashtakvarga')}
                </h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm" style={{ borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ backgroundColor: 'var(--aged-gold-dim)', color: 'white' }}>
                        <th className="text-left p-1.5 font-medium">{t('table.planet')}</th>
                        {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map(s => (
                          <th key={s} className="text-center p-1 font-medium">{(translateSign(s, language) || s).slice(0, 3)}</th>
                        ))}
                        <th className="text-center p-1.5 font-medium">{t('table.total')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map(planet => {
                        const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                        const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
                        const total = signs.reduce((sum: number, s: string) => sum + (bindus[s] || 0), 0);
                        return (
                          <tr key={planet} style={{ borderBottom: '1px solid var(--sacred-purple)' }}>
                            <td className="p-1.5 font-medium text-cosmic-text">{translatePlanet(planet, language)}</td>
                            {signs.map(s => {
                              const val = bindus[s] || 0;
                              return (
                                <td key={s} className="text-center p-1">
                                  <span className={`inline-block w-5 h-5 rounded text-sm leading-5 ${
                                    val >= 5 ? 'bg-sacred-gold-dark text-white font-bold'
                                    : val <= 2 ? 'bg-red-10 text-sacred-maroon'
                                    : 'text-cosmic-text'
                                  }`}>
                                    {val}
                                  </span>
                                </td>
                              );
                            })}
                            <td className="text-center p-1.5 font-semibold text-sacred-gold-dark">{total}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="text-center border-t border-sacred-purple pt-3 pb-1 mt-2">
            <p className="text-sm text-cosmic-text">
              {t('section.generatedBy')} | {new Date().toLocaleDateString('en-IN', { day: '2-digit', month: '2-digit', year: 'numeric' })}
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
