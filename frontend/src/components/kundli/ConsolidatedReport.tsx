import { useState, useEffect, useCallback } from 'react';
import { X, Download, Printer, Loader2, CheckCircle, Shield } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { api, formatDate } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateNakshatra, translateName, translateRemedy, translateLabel, translateBackend, translateSignAbbr, translatePlanetAbbr } from '@/lib/backend-translations';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import LordshipsTab from '@/components/kundli/LordshipsTab';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

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
  const toFiniteNumber = (value: unknown): number | null => {
    if (typeof value === 'number') return Number.isFinite(value) ? value : null;
    if (typeof value === 'string') {
      const cleaned = value.replace('%', '').trim();
      if (!cleaned) return null;
      const parsed = Number.parseFloat(cleaned);
      return Number.isFinite(parsed) ? parsed : null;
    }
    return null;
  };
  const normalizePercent = (value: number): number => {
    if (!Number.isFinite(value)) return 0;
    const scaled = value > 0 && value <= 1 ? value * 100 : value;
    return Math.max(0, Math.min(100, scaled));
  };

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
    } catch { /* ignored */ }
    setLoadingTransit(false);
  }, [result?.id, transitData]);

  const fetchD10 = useCallback(async () => {
    if (!result?.id || d10Data) return;
    setLoadingD10(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: 'D10' });
      setD10Data(data);
    } catch { /* ignored */ }
    setLoadingD10(false);
  }, [result?.id, d10Data]);

  const fetchYogini = useCallback(async () => {
    if (!result?.id || yoginiData) return;
    setLoadingYogini(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/yogini-dasha`);
      setYoginiData(data);
    } catch { /* ignored */ }
    setLoadingYogini(false);
  }, [result?.id, yoginiData]);

  const fetchSadesati = useCallback(async () => {
    if (!result?.id || sadesatiData) return;
    setLoadingSadesati(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/lifelong-sadesati`);
      setSadesatiData(data);
    } catch { /* ignored */ }
    setLoadingSadesati(false);
  }, [result?.id, sadesatiData]);

  const fetchKp = useCallback(async () => {
    if (!result?.id || kpData) return;
    setLoadingKp(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/kp-analysis`, {});
      setKpData(data);
    } catch { /* ignored */ }
    setLoadingKp(false);
  }, [result?.id, kpData]);

  const fetchVarshphal = useCallback(async () => {
    if (!result?.id || varshphalData) return;
    setLoadingVarshphal(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/varshphal`, {});
      setVarshphalData(data);
    } catch { /* ignored */ }
    setLoadingVarshphal(false);
  }, [result?.id, varshphalData]);

  const fetchUpagrahas = useCallback(async () => {
    if (!result?.id || upagrahasData) return;
    setLoadingUpagrahas(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/upagrahas`);
      setUpagrahasData(data);
    } catch { /* ignored */ }
    setLoadingUpagrahas(false);
  }, [result?.id, upagrahasData]);

  const fetchSodashvarga = useCallback(async () => {
    if (!result?.id || sodashvargaData) return;
    setLoadingSodashvarga(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/sodashvarga`);
      setSodashvargaData(data);
    } catch { /* ignored */ }
    setLoadingSodashvarga(false);
  }, [result?.id, sodashvargaData]);

  const fetchAspects = useCallback(async () => {
    if (!result?.id || aspectsData) return;
    setLoadingAspects(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/aspects`);
      setAspectsData(data);
    } catch { /* ignored */ }
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
      const token = localStorage.getItem('astrorattan_token');
      const API_BASE = import.meta.env.VITE_API_URL || '';
      const resp = await fetch(`${API_BASE}/api/kundli/${result.id}/pdf?lang=${language}`, {
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
      /* PDF download failed — alert shown to user */
      alert(e.message || t('report.failedToDownloadPDF'));
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
        className="max-w-[98vw] sm:max-w-[98vw] max-h-[95vh] w-full bg-card overflow-y-auto p-0 border-border"
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
        <div className="sticky top-0 z-10 bg-card border-b border-border px-6 py-3 flex items-center justify-between no-print">
          <div className="flex items-center gap-3">
            {/* Download/Print buttons removed per user request */}
          </div>
          <DialogTitle className="text-sm font-semibold text-primary">
            {t('section.consolidatedReport')}
          </DialogTitle>
          <button onClick={() => onOpenChange(false)} className="p-1.5 hover:bg-muted rounded transition-colors">
            <X className="w-5 h-5 text-foreground" />
          </button>
        </div>

        {/* Report content */}
        <div className="px-6 py-4 space-y-4 text-foreground">
          {/* Title block */}
          <div className="text-center border-b border-border pb-3">
            <Heading as={2} variant={2}>
              {result?.person_name} — {t('section.vedicBirthChart')}
            </Heading>
            <p className="text-data text-foreground mt-1">
              {result?.birth_date} | {result?.birth_time} | {result?.birth_place}
            </p>
          </div>

          {/* Row 1: Four charts */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-1">
            {/* Birth Chart (D1) */}
            <div className="border border-sacred-gold/20 rounded-lg p-1">
              <Heading as={4} variant={4} className="text-data text-center mb-1">
                {t('section.rashiD1')} <span className="text-sm font-normal text-muted-foreground">{t('report.clickHouseLagan')}</span>
              </Heading>
              <div className="flex justify-center max-w-full mx-auto">
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
                <button onClick={() => setD1Shift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
              )}
            </div>

            {/* D9 Navamsha */}
            <div className="border border-sacred-gold/20 rounded-lg p-1">
              <Heading as={4} variant={4} className="text-data text-center mb-1">
                {t('section.navamshaD9')} <span className="text-sm font-normal text-muted-foreground">{t('report.clickHouseLagan')}</span>
              </Heading>
              <div className="flex justify-center max-w-full mx-auto">
                {loadingDivisional ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
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
                  <p className="text-sm text-center py-12 text-foreground">{t('common.loading')}</p>
                )}
              </div>
              {d9Shift > 0 && (
                <button onClick={() => setD9Shift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
              )}
            </div>

            {/* D10 Dashamsha */}
            <div className="border border-sacred-gold/20 rounded-lg p-1">
              <Heading as={4} variant={4} className="text-data text-center mb-1">
                {t('kundli.d10')} <span className="text-sm font-normal text-muted-foreground">{t('report.clickHouseLagan')}</span>
              </Heading>
              <div className="flex justify-center max-w-full mx-auto">
                {loadingD10 ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
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
                  <p className="text-sm text-center py-12 text-foreground">{t('common.loading')}</p>
                )}
              </div>
              {d10Shift > 0 && (
                <button onClick={() => setD10Shift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
              )}
            </div>

            {/* Gochar (Transit) — clickable */}
            <div className="border border-sacred-gold/20 rounded-lg p-1">
              <Heading as={4} variant={4} className="text-data text-center mb-1">
                {t('kundli.gochar')} <span className="text-sm font-normal text-muted-foreground">{t('report.clickHouseLagan')}</span>
              </Heading>
              <div className="flex justify-center max-w-full mx-auto">
                {loadingTransit ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
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
                  <p className="text-sm text-center py-12 text-foreground">{t('common.loading')}</p>
                )}
              </div>
              {gocharShift > 0 && (
                <button onClick={() => setGocharShift(0)} className="block mx-auto mt-1 text-sm text-primary underline">{t('common.resetView')}</button>
              )}
            </div>
          </div>

          {/* Row 2: Planet Table (full width) */}
          <div className="border border-sacred-gold/20 rounded-lg p-3">
            <Heading as={4} variant={4} className="text-data mb-2">
              {t('section.detailedPlanetPositions')}
            </Heading>
            <div className="overflow-x-auto">
              <Table className="w-full text-sm border-collapse">
                <TableHeader>
                  <TableRow className="bg-primary text-primary-foreground">
                    <TableHead className="text-left p-1.5 font-medium">{t('table.planet')}</TableHead>
                    <TableHead className="text-left p-1.5 font-medium">{t('table.sign')}</TableHead>
                    <TableHead className="text-center p-1.5 font-medium whitespace-nowrap">{t('table.degree')}</TableHead>
                    <TableHead className="text-left p-1.5 font-medium">{t('table.nakshatra')}</TableHead>
                    <TableHead className="text-center p-1.5 font-medium">{t('table.status')}</TableHead>
                    <TableHead className="text-center p-1.5 font-medium">{t('table.nature')}</TableHead>
                    <TableHead className="text-center p-1.5 font-medium">{t('table.house')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {planets.map((planet, index) => {
                    const isBenefic = ['Jupiter', 'Venus', 'Moon', 'Mercury'].includes(planet.planet);
                    return (
                      <TableRow key={index} className="border-b border-border">
                        <TableCell className="p-1.5 font-medium text-foreground">{translatePlanet(planet.planet, language)}</TableCell>
                        <TableCell className="p-1.5 text-foreground">{translateSign(planet.sign, language)}</TableCell>
                        <TableCell className="p-1.5 text-center whitespace-nowrap">{(Number(planet.sign_degree) || 0).toFixed(1)}°</TableCell>
                        <TableCell className="p-1.5">{translateNakshatra(planet.nakshatra, language) || '\u2014'}</TableCell>
                        <TableCell className="p-1.5 text-center">
                          <span className={`text-sm px-1 py-0.5 rounded ${
                            planet.status === 'Exalted' || planet.status === 'Own Sign'
                              ? 'bg-green-100 text-green-800'
                              : planet.status === 'Debilitated'
                              ? 'bg-red-100 text-red-800'
                              : 'text-foreground'
                          }`}>
                            {planet.status ? translateLabel(planet.status, language) : '\u2014'}
                          </span>
                        </TableCell>
                        <TableCell className="p-1.5 text-center">
                          <span className={`text-sm ${isBenefic ? 'text-green-400' : 'text-red-400'}`}>
                            {isBenefic ? t('kundli.benefic') : t('kundli.malefic')}
                          </span>
                        </TableCell>
                        <TableCell className="p-1.5 text-center">{planet.house}</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* Row 3: Avakhada Chakra + Vimshottari Dasha + Yogini Dasha */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {/* Avakhada Chakra */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('avakhada.title')}
              </Heading>
              {loadingAvakhada ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : avakhadaData ? (
                <div className="grid grid-cols-2 gap-1.5">
                    { [
                    { label: t('avakhada.ascendant'), value: translateSign(avakhadaData.ascendant, language) },
                    { label: t('avakhada.ascendantLord'), value: translatePlanet(avakhadaData.ascendant_lord, language) },
                    { label: t('avakhada.rashi'), value: translateSign(avakhadaData.rashi, language) },
                    { label: t('avakhada.rashiLord'), value: translatePlanet(avakhadaData.rashi_lord, language) },
                    { label: t('avakhada.nakshatra'), value: `${translateNakshatra(avakhadaData.nakshatra, language)} (${t('report.padaLabel')}${avakhadaData.nakshatra_pada})` },
                    { label: t('avakhada.yoga'), value: translateBackend(avakhadaData.yoga, language) },
                    { label: t('avakhada.karana'), value: translateBackend(avakhadaData.karana, language) },
                    { label: t('avakhada.yoni'), value: translateBackend(avakhadaData.yoni, language) },
                    { label: t('avakhada.gana'), value: translateBackend(avakhadaData.gana, language) },
                    { label: t('avakhada.nadi'), value: translateBackend(avakhadaData.nadi, language) },
                    { label: t('avakhada.varna'), value: translateBackend(avakhadaData.varna, language) },
                    { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
                  ].map((item) => (
                    <div key={item.label} className="bg-muted rounded px-2 py-1">
                      <p className="text-sm text-foreground">{item.label}</p>
                      <p className="text-sm font-semibold text-foreground">{item.value || '\u2014'}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>

            {/* Vimshottari Dasha */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.vimshottariDasha')}
              </Heading>
              {loadingDasha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : dashaData ? (
                <div>
                  <div className="bg-primary rounded px-2 py-1.5 mb-2">
                    <p className="text-sm text-foreground">{t('section.currentMahadasha')}</p>
                    <p className="text-data font-bold text-primary">{translatePlanet(dashaData.current_dasha, language)}</p>
                    {dashaData.current_antardasha && (
                      <p className="text-sm text-primary">{t('report.adLabel')} {translatePlanet(dashaData.current_antardasha, language)}</p>
                    )}
                  </div>
                  <Table className="w-full text-sm border-collapse">
                    <TableHeader>
                      <TableRow className="bg-muted">
                        <TableHead className="text-left p-1 font-medium text-primary">{t('table.planet')}</TableHead>
                        <TableHead className="text-left p-1 font-medium text-primary">{t('table.start')}</TableHead>
                        <TableHead className="text-left p-1 font-medium text-primary">{t('table.end')}</TableHead>
                        <TableHead className="text-center p-1 font-medium text-primary">{t('table.years')}</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {(dashaData.mahadasha_periods || []).map((p: any) => (
                        <TableRow key={p.planet} style={{
                          borderBottom: '1px solid hsl(var(--border))',
                          backgroundColor: p.planet === dashaData.current_dasha ? 'var(--aged-gold-dim-10, rgba(180, 83, 9, 0.06))' : undefined,
                        }}>
                          <TableCell className="p-1 font-medium">{translatePlanet(p.planet, language)}{p.planet === dashaData.current_dasha ? ' \u2190' : ''}</TableCell>
                          <TableCell className="p-1 text-foreground">{p.start_date}</TableCell>
                          <TableCell className="p-1 text-foreground">{p.end_date}</TableCell>
                          <TableCell className="p-1 text-center text-foreground">{p.years}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>

            {/* Yogini Dasha */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.yoginiDasha')}
              </Heading>
              {loadingYogini ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : yoginiData ? (
                <div>
                  <div className="bg-primary rounded px-2 py-1.5 mb-2">
                    <p className="text-sm text-foreground">{t('report.currentDasha')}</p>
                    <p className="text-data font-bold text-primary">{yoginiData.current_dasha?.planet ? translatePlanet(yoginiData.current_dasha.planet, language) : '\u2014'}</p>
                    {yoginiData.current_dasha?.planet && (
                      <p className="text-sm text-primary">{t('report.untilLabel')} {yoginiData.current_dasha?.end_date}</p>
                    )}
                  </div>
                  <Table className="w-full text-sm border-collapse">
                    <TableHeader>
                      <TableRow className="bg-muted">
                        <TableHead className="text-left p-1 font-medium text-primary">{t('table.yogini')}</TableHead>
                        <TableHead className="text-left p-1 font-medium text-primary">{t('table.planet')}</TableHead>
                        <TableHead className="text-left p-1 font-medium text-primary">{t('table.start')}</TableHead>
                        <TableHead className="text-left p-1 font-medium text-primary">{t('table.end')}</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {(yoginiData.periods || []).map((p: any) => (
                        <TableRow key={p.name + p.start_date} style={{
                          borderBottom: '1px solid hsl(var(--border))',
                          backgroundColor: p.name === yoginiData.current_dasha?.name && p.start_date === yoginiData.current_dasha?.start_date ? 'var(--aged-gold-dim-10, rgba(180, 83, 9, 0.06))' : undefined,
                        }}>
                          <TableCell className="p-1 font-medium">{translateName(p.name, language)}{p.name === yoginiData.current_dasha?.name && p.start_date === yoginiData.current_dasha?.start_date ? ' \u2190' : ''}</TableCell>
                          <TableCell className="p-1 text-foreground">{translatePlanet(p.planet, language)} ({p.span}{t('report.yearLabel')})</TableCell>
                          <TableCell className="p-1 text-foreground">{p.start_date}</TableCell>
                          <TableCell className="p-1 text-foreground">{p.end_date}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 4: Yogas + Doshas + Lifelong Sade Sati + Lordships */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {/* Yogas (present only) */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2 flex items-center gap-1">
                <CheckCircle className="w-3 h-3 text-green-500" />
                {t('section.yogas')}
              </Heading>
              {loadingYogaDosha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
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
                <p className="text-sm text-center py-4 text-foreground">{t('yoga.noneDetected')}</p>
              )}
            </div>

            {/* Doshas (present only) */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2 flex items-center gap-1">
                <Shield className="w-3 h-3 text-red-500" />
                {t('section.doshas')}
              </Heading>
              {loadingYogaDosha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
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
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2 flex items-center gap-1">
                <Shield className="w-3 h-3 text-primary" />
                {t('section.lifelongSadeSati')}
              </Heading>
              {loadingSadesati ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : sadesatiData ? (
                <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
                  {sadesatiData.phases && sadesatiData.phases.length > 0 ? (
                    <div className="space-y-1.5">
                      {sadesatiData.phases.map((ph: any, idx: number) => (
                        <div key={idx} className="bg-muted rounded px-2 py-1">
                          <p className="text-sm text-primary font-medium">{translateLabel(ph.phase, language)} {t('report.phaseLabel')}</p>
                          <p className="text-sm text-foreground">{ph.start_date} \u2192 {ph.end_date}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-center py-4 text-green-400">{t('sadesati.noPhases')}</p>
                  )}
                  {sadesatiData.remedies && sadesatiData.remedies.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-border">
                      <p className="text-sm font-semibold text-primary mb-1">{t('section.generalRemedies')}</p>
                      <ul className="list-disc pl-3 space-y-0.5 text-micro text-foreground">
                        {sadesatiData.remedies.map((rem: string, idx: number) => (
                          <li key={idx}>{translateRemedy(rem, language)}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-sm text-center py-4 text-foreground">{t('common.loading')}</p>
              )}
            </div>

            {/* Lordships */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.houseLordships')}
              </Heading>
              <div className="text-sm">
                <LordshipsTab planets={planets} houses={result?.chart_data?.houses || {}} />
              </div>
            </div>
          </div>

          {/* Row 5: Ashtakvarga SAV + Shadbala */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            {/* Ashtakvarga SAV */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.sarvashtakvarga')}
              </Heading>
              {loadingAshtakvarga ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
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
                          <span className="text-sm font-medium text-foreground">{points}</span>
                          <div className="w-full bg-muted rounded-t-sm relative h-[80px]">
                            <div
                              className="absolute bottom-0 w-full rounded-t-sm"
                              style={{ height: `${heightPct}%`, backgroundColor: isStrong ? 'var(--aged-gold-dim)' : 'var(--ink-light)' }}
                            />
                          </div>
                          <span className="text-micro text-foreground">{translateSignAbbr(sign, language)}</span>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-sm text-foreground">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />{t('dignity.strong')}</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--ink-light)' }} />{t('dignity.weak')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>

            {/* Shadbala */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.shadbalaStrength')}
              </Heading>
              {loadingShadbala ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : shadbalaData?.planets ? (
                <div className="space-y-1.5">
                  {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                    const data = shadbalaData.planets[planet];
                    if (!data) return null;
                    const pct = Math.min((data.total / data.required) * 100, 150);
                    const barColor = data.is_strong ? 'var(--aged-gold-dim)' : 'var(--wax-red)';
                    return (
                      <div key={planet} className="flex items-center gap-1.5">
                        <span className="w-10 text-sm font-medium text-foreground">{translatePlanet(planet, language)}</span>
                        <div className="flex-1 bg-muted rounded-full h-3 overflow-hidden">
                          <div className="h-full rounded-full" style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }} />
                        </div>
                        <span className={`text-sm w-12 text-right font-medium ${data.is_strong ? 'text-primary' : 'text-destructive'}`}>
                          {data.total}/{data.required}
                        </span>
                      </div>
                    );
                  })}
                  <div className="flex items-center gap-3 mt-1 text-sm text-foreground">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />{t('dignity.strong')}</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: 'var(--wax-red)' }} />{t('dignity.weak')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>
          </div>
          {/* Row 6: KP Analysis + Varshphal */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mt-3">
            {/* KP Analysis */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.kpAnalysis')}
              </Heading>
              {loadingKp ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : kpData ? (
                <div className="space-y-4 max-h-64 overflow-y-auto pr-1">
                  <div>
                    <Heading as={5} variant={5} className="text-primary mb-1">{t('section.planetarySignificators')}</Heading>
                    <Table className="w-full text-sm border-collapse">
                      <TableHeader>
                        <TableRow>
                          <TableHead className="text-left p-1 text-muted-foreground">{t('table.planet')}</TableHead>
                          <TableHead className="text-left p-1 text-muted-foreground">{t('table.starLord')}</TableHead>
                          <TableHead className="text-left p-1 text-muted-foreground">{t('table.subLord')}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {(kpData.planets || []).map((p: any) => (
                          <TableRow key={p.planet} className="border-b border-border">
                            <TableCell className="p-1 text-foreground">{translatePlanet(p.planet, language)}</TableCell>
                            <TableCell className="p-1 text-foreground">{p.nakshatra_lord ? translatePlanet(p.nakshatra_lord, language) : '-'}</TableCell>
                            <TableCell className="p-1 text-foreground">{p.sub_lord ? translatePlanet(p.sub_lord, language) : '-'}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                  <div>
                    <Heading as={5} variant={5} className="text-primary mb-1">{t('section.houseCusps')}</Heading>
                    <Table className="w-full text-sm border-collapse">
                      <TableHeader>
                        <TableRow>
                          <TableHead className="text-left p-1 text-muted-foreground">{t('table.cusp')}</TableHead>
                          <TableHead className="text-left p-1 text-muted-foreground">{t('table.starLord')}</TableHead>
                          <TableHead className="text-left p-1 text-muted-foreground">{t('table.subLord')}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {(kpData.houses || []).map((h: any) => (
                          <TableRow key={h.cusp} className="border-b border-border">
                            <TableCell className="p-1 text-foreground">{t('report.houseLabel')}{h.cusp}</TableCell>
                            <TableCell className="p-1 text-foreground">{h.nakshatra_lord ? translatePlanet(h.nakshatra_lord, language) : '-'}</TableCell>
                            <TableCell className="p-1 text-foreground">{h.sub_lord ? translatePlanet(h.sub_lord, language) : '-'}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>

            {/* Varshphal (Annual Return) */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.varshphalCurrentYear')}
              </Heading>
              {loadingVarshphal ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : varshphalData ? (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-muted rounded px-2 py-1.5 border border-border">
                      <p className="text-sm text-foreground">{t('section.munthaSign')}</p>
                      <p className="text-data font-bold text-primary">{varshphalData.muntha?.sign ? translateSign(varshphalData.muntha.sign, language) : t('report.notAvailable')}</p>
                    </div>
                    <div className="bg-muted rounded px-2 py-1.5 border border-border">
                      <p className="text-sm text-foreground">{t('section.munthaLord')}</p>
                      <p className="text-data font-bold text-primary">{varshphalData.muntha?.lord ? translatePlanet(varshphalData.muntha.lord, language) : t('report.notAvailable')}</p>
                    </div>
                    <div className="bg-muted rounded px-2 py-1.5 border border-border">
                      <p className="text-sm text-foreground">{t('section.yearLord')}</p>
                      <p className="text-data font-bold text-primary">{varshphalData.year_lord ? translatePlanet(varshphalData.year_lord, language) : t('report.notAvailable')}</p>
                    </div>
                  </div>
                  {varshphalData.mudda_dasha && (
                    <div>
                      <Heading as={5} variant={5} className="text-primary mb-1">{t('section.muddaDasha')}</Heading>
                      <div className="bg-muted p-2 rounded max-h-32 overflow-y-auto w-full">
                        <Table className="w-full text-sm border-collapse">
                           <TableBody>
                             {varshphalData.mudda_dasha.map((md: any) => (
                               <TableRow key={md.planet} className="border-b border-border">
                                 <TableCell className="p-1 font-medium">{translatePlanet(md.planet, language)}</TableCell>
                                 <TableCell className="p-1 text-foreground">{formatDate(md.start_date)} - {formatDate(md.end_date)}</TableCell>
                               </TableRow>
                             ))}
                           </TableBody>
                        </Table>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 7: Upagrahas */}
          <div className="grid grid-cols-1 mt-3">
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.upagrahasTitle')}
              </Heading>
              {loadingUpagrahas ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : upagrahasData?.upagrahas ? (
                <div className="overflow-x-auto">
                  <Table className="w-full text-sm border-collapse">
                    <TableHeader>
                      <TableRow>
                        <TableHead className="text-left p-1.5 text-muted-foreground">{t('tab.upagrahas')}</TableHead>
                        <TableHead className="text-left p-1.5 text-muted-foreground">{t('table.longitude')}</TableHead>
                        <TableHead className="text-left p-1.5 text-muted-foreground">{t('table.sign')}</TableHead>
                        <TableHead className="text-left p-1.5 text-muted-foreground">{t('table.nakshatra')}</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {['Dhooma', 'Vyatipata', 'Parivesha', 'Indrachapa', 'Upaketu', 'Gulika', 'Mandi']
                        .filter(name => upagrahasData.upagrahas[name])
                        .map((name: string) => {
                        const u = upagrahasData.upagrahas[name];
                        return (
                          <TableRow key={name} className="border-b border-border">
                            <TableCell className="p-1.5 font-medium text-foreground">{translateName(name, language)}</TableCell>
                            <TableCell className="p-1.5 text-foreground">{u.sign_degree?.toFixed(2)}°</TableCell>
                            <TableCell className="p-1.5 text-foreground">{translateSign(u.sign, language)}</TableCell>
                            <TableCell className="p-1.5 text-foreground">{translateNakshatra(u.nakshatra, language)} {t('report.padaLabel')}{u.nakshatra_pada}</TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 8: Sodashvarga — By Sign (16 Divisional Charts Table) */}
          <div className="grid grid-cols-1 mt-3">
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.sodashvargaTitle')}
              </Heading>
              {loadingSodashvarga ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : sodashvargaData?.varga_table ? (
                <div className="space-y-4">
                  {/* By Sign Table */}
                  <div className="overflow-x-auto">
                    <Table className="w-full text-sm border-collapse">
                      <TableHeader>
                        <TableRow className="bg-primary text-primary-foreground">
                          <TableHead className="text-left p-1.5 font-medium sticky left-0 bg-primary min-w-[80px]">{t('table.varga')}</TableHead>
                          {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'].map(p => (
                            <TableHead key={p} className="text-center p-1.5 font-medium min-w-[50px]">{translatePlanetAbbr(p, language)}</TableHead>
                          ))}
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {(sodashvargaData.varga_table || []).map((row: any) => (
                          <TableRow key={row.division} className="border-b border-border">
                            <TableCell className="p-1.5 font-medium text-primary sticky left-0 bg-card">
                              {row.name}
                            </TableCell>
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
                                <TableCell key={planet} className="p-1.5 text-center" style={dignityStyle} title={dignity ? translateLabel(dignity, language) : ''}>
                                  {sign === '-' ? '-' : translateSignAbbr(sign, language)}
                                </TableCell>
                              );
                            })}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                  {/* Legend */}
                  <div className="flex flex-wrap gap-3 text-sm text-foreground">
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#d1fae5', border: '1px solid #065f46' }} />{t('dignity.exalted')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#fef3c7', border: '1px solid #92400e' }} />{t('report.ownMT')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#dbeafe', border: '1px solid #1e40af' }} />{t('dignity.friend')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#ffedd5', border: '1px solid #9a3412' }} />{t('dignity.enemy')}</span>
                    <span className="flex items-center gap-1"><span className="w-4 h-3 rounded" style={{ backgroundColor: '#fee2e2', border: '1px solid #991b1b' }} />{t('dignity.debilitated')}</span>
                  </div>

                  {/* Vimshopak Bala (By Planet) */}
                  <div>
                    <Heading as={5} variant={5} className="text-primary mb-2">{t('section.vimshopakBala')}</Heading>
                    <div className="space-y-1">
                      {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
                        .filter(p => sodashvargaData.by_planet?.[p])
                        .map(planet => {
                          const data = sodashvargaData.by_planet[planet];
                          const score = toFiniteNumber(data?.vimshopak_bala);
                          const inputPercent = toFiniteNumber(data?.percentage);
                          const scoreBasedPercent = score != null ? (score / 20.0) * 100 : 0;
                          const pct = normalizePercent(inputPercent != null ? inputPercent : scoreBasedPercent);
                          const barColor = data.strength === 'Strong' ? 'var(--aged-gold-dim)' : data.strength === 'Medium' ? '#f59e0b' : 'var(--wax-red)';
                          return (
                            <div key={planet} className="flex items-center gap-1.5">
                              <span className="w-12 text-sm font-medium text-foreground">{translatePlanet(planet, language)}</span>
                              <div className="flex-1 bg-muted rounded-full h-2.5 overflow-hidden">
                                <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: barColor }} />
                              </div>
                              <span className={`text-sm w-16 text-right font-medium`} style={{ color: barColor }}>
                                {score != null ? score : data.vimshopak_bala} ({translateLabel(data.strength, language)})
                              </span>
                            </div>
                          );
                        })}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 9: Aspects on Planets + Aspects on Bhavas */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mt-3">
            {/* Aspects on Planets */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.aspectsOnPlanets')}
              </Heading>
              {loadingAspects ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : aspectsData?.planet_aspects_summary ? (
                <div className="overflow-y-auto max-h-72 space-y-2">
                  {Object.entries(aspectsData.planet_aspects_summary).map(([planet, data]: [string, any]) => (
                    <div key={planet} className="bg-muted rounded px-2 py-1.5 border border-border">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-semibold text-foreground">{translatePlanet(planet, language)} <span className="text-sm text-foreground">({t('report.houseLabel')}{data.house})</span></span>
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
                        <p className="text-sm text-foreground mt-0.5">{t('report.noAspectsReceived')}</p>
                      )}
                      {/* Houses this planet aspects */}
                      {data.aspects_to && data.aspects_to.length > 0 && (
                        <div className="mt-1 pt-1 border-t border-border">
                          <span className="text-sm text-primary">{t('report.aspectsTo')} </span>
                          {data.aspects_to.map((a: any, i: number) => (
                            <span key={i} className="text-sm text-foreground">
                              {t('report.houseLabel')}{a.house}
                              {a.planets_in_house && a.planets_in_house.length > 0 && (
                                <span className="text-primary"> ({a.planets_in_house.map((p: string) => translatePlanet(p, language)).join(', ')})</span>
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
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>

            {/* Aspects on Bhavas */}
            <div className="border border-sacred-gold/20 rounded-lg p-3">
              <Heading as={4} variant={4} className="text-data mb-2">
                {t('section.aspectsOnBhavas')}
              </Heading>
              {loadingAspects ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-primary" /></div>
              ) : aspectsData?.bhava_summary ? (
                <div className="overflow-x-auto">
                  <Table className="w-full text-sm border-collapse">
                    <TableHeader>
                      <TableRow className="bg-muted">
                        <TableHead className="text-left p-1.5 text-muted-foreground">{t('table.bhava')}</TableHead>
                        <TableHead className="text-left p-1.5 text-muted-foreground">{t('table.planets')}</TableHead>
                        <TableHead className="text-left p-1.5 text-muted-foreground">{t('table.aspectedBy')}</TableHead>
                        <TableHead className="text-center p-1.5 text-muted-foreground">{t('auto.b')}</TableHead>
                        <TableHead className="text-center p-1.5 text-muted-foreground">{t('auto.m')}</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {(aspectsData.bhava_summary || []).map((bh: any) => (
                        <TableRow key={bh.house} className="border-b border-border">
                          <TableCell className="p-1.5 font-medium text-primary">{t('report.houseLabel')}{bh.house}</TableCell>
                          <TableCell className="p-1.5 text-foreground">
                            {bh.planets_in_house && bh.planets_in_house.length > 0
                              ? bh.planets_in_house.map((p: string) => translatePlanet(p, language)).join(', ')
                              : <span className="text-foreground">—</span>}
                          </TableCell>
                          <TableCell className="p-1.5 text-foreground">
                            {bh.aspected_by && bh.aspected_by.length > 0
                              ? bh.aspected_by.map((p: string) => translatePlanet(p, language)).join(', ')
                              : <span className="text-foreground">—</span>}
                          </TableCell>
                          <TableCell className="p-1.5 text-center">
                            <span className="text-green-400">{bh.benefic_aspects || 0}</span>
                          </TableCell>
                          <TableCell className="p-1.5 text-center">
                            <span className="text-red-400">{bh.malefic_aspects || 0}</span>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  <div className="flex gap-3 mt-1 text-sm text-foreground">
                    <span>{t('report.beneficAspectsLabel')}</span>
                    <span>{t('report.maleficAspectsLabel')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-center py-6 text-foreground">{t('common.loading')}</p>
              )}
            </div>
          </div>

          {/* Row 10: Bhinnashtakvarga Detail Table */}
          {ashtakvargaData?.planet_bindus && (
            <div className="grid grid-cols-1 mt-3">
              <div className="border border-sacred-gold/20 rounded-lg p-3">
                <Heading as={4} variant={4} className="text-data mb-2">
                  {t('section.bhinnashtakvarga')}
                </Heading>
                <div className="overflow-x-auto">
                  <Table className="w-full text-sm border-collapse">
                    <TableHeader>
                      <TableRow className="bg-primary text-primary-foreground">
                        <TableHead className="text-left p-1.5 font-medium">{t('table.planet')}</TableHead>
                        {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map(s => (
                          <TableHead key={s} className="text-center p-1 font-medium">{translateSignAbbr(s, language)}</TableHead>
                        ))}
                        <TableHead className="text-center p-1.5 font-medium">{t('table.total')}</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map(planet => {
                        const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                        const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
                        const total = signs.reduce((sum: number, s: string) => sum + (bindus[s] || 0), 0);
                        return (
                          <TableRow key={planet} className="border-b border-border">
                            <TableCell className="p-1.5 font-medium text-foreground">{translatePlanet(planet, language)}</TableCell>
                            {signs.map(s => {
                              const val = bindus[s] || 0;
                              return (
                                <TableCell key={s} className="text-center p-1">
                                  <span className={`inline-block w-5 h-5 rounded text-sm leading-5 ${
                                    val >= 5 ? 'bg-primary text-white font-bold'
                                    : val <= 2 ? 'bg-red-10 text-destructive'
                                    : 'text-foreground'
                                  }`}>
                                    {val}
                                  </span>
                                </TableCell>
                              );
                            })}
                            <TableCell className="text-center p-1.5 font-semibold text-primary">{total}</TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </div>
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="text-center border-t border-border pt-3 pb-1 mt-2">
            <p className="text-sm text-foreground">
              {t('section.generatedBy')} | {new Date().toLocaleDateString('en-IN', { day: '2-digit', month: '2-digit', year: 'numeric' })}
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
