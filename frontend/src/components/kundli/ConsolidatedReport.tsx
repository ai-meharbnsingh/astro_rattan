import { useState, useEffect, useCallback } from 'react';
import { X, Download, Printer, Loader2, CheckCircle, Shield } from 'lucide-react';
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
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
  const { t } = useTranslation();

  // Local state for transit and D10
  const [transitData, setTransitData] = useState<any>(null);
  const [loadingTransit, setLoadingTransit] = useState(false);
  const [d10Data, setD10Data] = useState<any>(null);
  const [loadingD10, setLoadingD10] = useState(false);

  const fetchTransit = useCallback(async () => {
    if (!result?.id || transitData) return;
    setLoadingTransit(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/transits`, {});
      setTransitData(data);
    } catch { /* fallback */ }
    setLoadingTransit(false);
  }, [result?.id, transitData]);

  const fetchD10 = useCallback(async () => {
    if (!result?.id || d10Data) return;
    setLoadingD10(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: 'D10' });
      setD10Data(data);
    } catch { /* fallback */ }
    setLoadingD10(false);
  }, [result?.id, d10Data]);

  // Fetch transit and D10 when popup opens
  useEffect(() => {
    if (open && result?.id) {
      fetchTransit();
      fetchD10();
    }
  }, [open, result?.id, fetchTransit, fetchD10]);

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

  // Build transit chart data
  const transitChartData: ChartData | null = transitData?.transits
    ? {
        planets: transitData.transits.map((tr: any) => ({
          planet: tr.planet,
          sign: tr.current_sign || tr.sign || 'Aries',
          house: tr.house_from_moon || tr.house || 1,
          nakshatra: tr.nakshatra || '',
          sign_degree: tr.degree || 0,
          status: tr.effect || '',
        })),
      }
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
        className="max-w-[95vw] max-h-[95vh] w-full bg-white overflow-y-auto p-0 border-[#E8E0D4]"
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
        <div className="sticky top-0 z-10 bg-white border-b border-[#E8E0D4] px-6 py-3 flex items-center justify-between no-print">
          <div className="flex items-center gap-3">
            <Button size="sm" onClick={handleDownloadPDF} className="bg-[#B8860B] text-white hover:bg-[#9A7B0A] text-xs h-8">
              <Download className="w-3.5 h-3.5 mr-1" />{t('kundli.downloadPDF')}
            </Button>
            <Button size="sm" variant="outline" onClick={() => window.print()} className="border-[#E8E0D4] text-[#1a1a2e] text-xs h-8">
              <Printer className="w-3.5 h-3.5 mr-1" />{t('kundli.printReport')}
            </Button>
          </div>
          <DialogTitle className="text-sm font-semibold text-[#B8860B] font-serif">
            {t('kundli.consolidatedReport')}
          </DialogTitle>
          <button onClick={() => onOpenChange(false)} className="p-1.5 hover:bg-[#E8E0D4] rounded transition-colors">
            <X className="w-5 h-5 text-[#1a1a2e]" />
          </button>
        </div>

        {/* Report content */}
        <div className="px-6 py-4 space-y-4" style={{ color: '#1a1a2e' }}>
          {/* Title block */}
          <div className="text-center border-b border-[#E8E0D4] pb-3">
            <h2 className="text-lg font-bold font-serif" style={{ color: '#B8860B' }}>
              {result?.person_name}&apos;s Vedic Birth Chart
            </h2>
            <p className="text-[11px] text-[#1a1a2e]/60 mt-1">
              {result?.birth_date} | {result?.birth_time} | {result?.birth_place}
            </p>
          </div>

          {/* Row 1: Four charts */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {/* Birth Chart (D1) */}
            <div className="border border-[#E8E0D4] rounded-lg p-2">
              <h4 className="text-[11px] font-bold text-center mb-1" style={{ color: '#B8860B' }}>
                Rashi (D1)
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '250px', margin: '0 auto' }}>
                <InteractiveKundli
                  chartData={{ planets, houses: result?.chart_data?.houses } as ChartData}
                  compact
                />
              </div>
            </div>

            {/* D9 Navamsha */}
            <div className="border border-[#E8E0D4] rounded-lg p-2">
              <h4 className="text-[11px] font-bold text-center mb-1" style={{ color: '#B8860B' }}>
                Navamsha (D9)
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '250px', margin: '0 auto' }}>
                {loadingDivisional ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
                ) : d9ChartData ? (
                  <InteractiveKundli chartData={d9ChartData} compact />
                ) : (
                  <p className="text-[10px] text-center py-12 text-[#1a1a2e]/40">Loading...</p>
                )}
              </div>
            </div>

            {/* D10 Dashamsha */}
            <div className="border border-[#E8E0D4] rounded-lg p-2">
              <h4 className="text-[11px] font-bold text-center mb-1" style={{ color: '#B8860B' }}>
                {t('kundli.d10')}
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '250px', margin: '0 auto' }}>
                {loadingD10 ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
                ) : d10ChartData ? (
                  <InteractiveKundli chartData={d10ChartData} compact />
                ) : (
                  <p className="text-[10px] text-center py-12 text-[#1a1a2e]/40">Loading...</p>
                )}
              </div>
            </div>

            {/* Gochar (Transit) */}
            <div className="border border-[#E8E0D4] rounded-lg p-2">
              <h4 className="text-[11px] font-bold text-center mb-1" style={{ color: '#B8860B' }}>
                {t('kundli.gochar')}
              </h4>
              <div className="flex justify-center" style={{ maxWidth: '250px', margin: '0 auto' }}>
                {loadingTransit ? (
                  <div className="flex items-center justify-center py-12"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
                ) : transitChartData ? (
                  <InteractiveKundli chartData={transitChartData} compact />
                ) : (
                  <p className="text-[10px] text-center py-12 text-[#1a1a2e]/40">Loading...</p>
                )}
              </div>
            </div>
          </div>

          {/* Row 2: Planet Table (full width) */}
          <div className="border border-[#E8E0D4] rounded-lg p-3">
            <h4 className="text-[11px] font-bold mb-2" style={{ color: '#B8860B' }}>
              {t('kundli.birthDetailsTable')}
            </h4>
            <div className="overflow-x-auto">
              <table className="w-full text-[10px]" style={{ borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ backgroundColor: '#B8860B', color: 'white' }}>
                    <th className="text-left p-1.5 font-medium">Planet</th>
                    <th className="text-left p-1.5 font-medium">{t('kundli.sign')}</th>
                    <th className="text-center p-1.5 font-medium">{t('kundli.degree')}</th>
                    <th className="text-left p-1.5 font-medium">{t('kundli.nakshatra')}</th>
                    <th className="text-center p-1.5 font-medium">Status</th>
                    <th className="text-center p-1.5 font-medium">{t('kundli.nature')}</th>
                    <th className="text-center p-1.5 font-medium">{t('kundli.house')}</th>
                  </tr>
                </thead>
                <tbody>
                  {planets.map((planet, index) => {
                    const isBenefic = ['Jupiter', 'Venus', 'Moon', 'Mercury'].includes(planet.planet);
                    return (
                      <tr key={index} style={{ borderBottom: '1px solid #E8E0D4' }}>
                        <td className="p-1.5 font-medium" style={{ color: '#1a1a2e' }}>{planet.planet}</td>
                        <td className="p-1.5" style={{ color: '#1a1a2e' }}>{planet.sign}</td>
                        <td className="p-1.5 text-center">{planet.sign_degree?.toFixed(1)}&deg;</td>
                        <td className="p-1.5">{planet.nakshatra || '\u2014'}</td>
                        <td className="p-1.5 text-center">
                          <span className={`text-[9px] px-1 py-0.5 rounded ${
                            planet.status === 'Exalted' || planet.status === 'Own Sign'
                              ? 'bg-green-100 text-green-700'
                              : planet.status === 'Debilitated'
                              ? 'bg-red-100 text-red-700'
                              : 'text-[#1a1a2e]/60'
                          }`}>
                            {planet.status || '\u2014'}
                          </span>
                        </td>
                        <td className="p-1.5 text-center">
                          <span className={`text-[9px] ${isBenefic ? 'text-green-600' : 'text-red-600'}`}>
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

          {/* Row 3: Avakhada Chakra + Vimshottari Dasha */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            {/* Avakhada Chakra */}
            <div className="border border-[#E8E0D4] rounded-lg p-3">
              <h4 className="text-[11px] font-bold mb-2" style={{ color: '#B8860B' }}>
                {t('avakhada.title')}
              </h4>
              {loadingAvakhada ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
              ) : avakhadaData ? (
                <div className="grid grid-cols-2 gap-1.5">
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
                  ].map((item) => (
                    <div key={item.label} className="bg-[#F5F0E8] rounded px-2 py-1">
                      <p className="text-[9px] text-[#1a1a2e]/50">{item.label}</p>
                      <p className="text-[10px] font-semibold text-[#1a1a2e]">{item.value || '\u2014'}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-[10px] text-center py-6 text-[#1a1a2e]/40">Loading...</p>
              )}
            </div>

            {/* Vimshottari Dasha */}
            <div className="border border-[#E8E0D4] rounded-lg p-3">
              <h4 className="text-[11px] font-bold mb-2" style={{ color: '#B8860B' }}>
                Vimshottari {t('kundli.dasha')}
              </h4>
              {loadingDasha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
              ) : dashaData ? (
                <div>
                  <div className="bg-[#B8860B]/10 rounded px-2 py-1.5 mb-2">
                    <p className="text-[9px] text-[#1a1a2e]/50">Current Mahadasha</p>
                    <p className="text-[11px] font-bold" style={{ color: '#B8860B' }}>{dashaData.current_dasha}</p>
                    {dashaData.current_antardasha && (
                      <p className="text-[9px] text-[#B8860B]">AD: {dashaData.current_antardasha}</p>
                    )}
                  </div>
                  <table className="w-full text-[10px]" style={{ borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ backgroundColor: '#F5F0E8' }}>
                        <th className="text-left p-1 font-medium text-[#B8860B]">Planet</th>
                        <th className="text-left p-1 font-medium text-[#B8860B]">Start</th>
                        <th className="text-left p-1 font-medium text-[#B8860B]">End</th>
                        <th className="text-center p-1 font-medium text-[#B8860B]">Yrs</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(dashaData.mahadasha_periods || []).map((p: any) => (
                        <tr key={p.planet} style={{
                          borderBottom: '1px solid #E8E0D4',
                          backgroundColor: p.planet === dashaData.current_dasha ? '#B8860B10' : undefined,
                        }}>
                          <td className="p-1 font-medium">{p.planet}{p.planet === dashaData.current_dasha ? ' \u2190' : ''}</td>
                          <td className="p-1 text-[#1a1a2e]/60">{p.start_date}</td>
                          <td className="p-1 text-[#1a1a2e]/60">{p.end_date}</td>
                          <td className="p-1 text-center text-[#1a1a2e]/60">{p.years}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-[10px] text-center py-6 text-[#1a1a2e]/40">Loading...</p>
              )}
            </div>
          </div>

          {/* Row 4: Yogas + Doshas + Lordships */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
            {/* Yogas (present only) */}
            <div className="border border-[#E8E0D4] rounded-lg p-3">
              <h4 className="text-[11px] font-bold mb-2 flex items-center gap-1" style={{ color: '#B8860B' }}>
                <CheckCircle className="w-3 h-3 text-green-500" />
                {t('yoga.title')}
              </h4>
              {loadingYogaDosha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
              ) : presentYogas.length > 0 ? (
                <div className="space-y-1">
                  {presentYogas.map((yoga: any, idx: number) => (
                    <div key={idx} className="bg-green-50 border border-green-200 rounded px-2 py-1">
                      <span className="text-[10px] font-medium text-green-800">{yoga.name}</span>
                      {yoga.description && (
                        <p className="text-[9px] text-green-600 mt-0.5">{yoga.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-[10px] text-center py-4 text-[#1a1a2e]/40">No yogas detected</p>
              )}
            </div>

            {/* Doshas (present only) */}
            <div className="border border-[#E8E0D4] rounded-lg p-3">
              <h4 className="text-[11px] font-bold mb-2 flex items-center gap-1" style={{ color: '#B8860B' }}>
                <Shield className="w-3 h-3 text-red-500" />
                {t('dosha.extended.title')}
              </h4>
              {loadingYogaDosha ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
              ) : presentDoshas.length > 0 ? (
                <div className="space-y-1">
                  {presentDoshas.map((dosha: any, idx: number) => (
                    <div key={idx} className="bg-red-50 border border-red-200 rounded px-2 py-1">
                      <span className="text-[10px] font-medium text-red-800">{dosha.name}</span>
                      {dosha.remedies && (
                        <p className="text-[9px] text-red-600 mt-0.5">{t('dosha.remedies')}: {dosha.remedies}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-[10px] text-center py-4 text-green-600">No doshas present</p>
              )}
            </div>

            {/* Lordships */}
            <div className="border border-[#E8E0D4] rounded-lg p-3">
              <h4 className="text-[11px] font-bold mb-2" style={{ color: '#B8860B' }}>
                {t('kundli.houseLordships')}
              </h4>
              <div className="text-[10px]">
                <LordshipsTab planets={planets} houses={result?.chart_data?.houses || {}} />
              </div>
            </div>
          </div>

          {/* Row 5: Ashtakvarga SAV + Shadbala */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            {/* Ashtakvarga SAV */}
            <div className="border border-[#E8E0D4] rounded-lg p-3">
              <h4 className="text-[11px] font-bold mb-2" style={{ color: '#B8860B' }}>
                {t('kundli.sarvashtakvarga')}
              </h4>
              {loadingAshtakvarga ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
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
                          <span className="text-[8px] font-medium text-[#1a1a2e]">{points}</span>
                          <div className="w-full bg-[#E8E0D4] rounded-t-sm relative" style={{ height: '80px' }}>
                            <div
                              className="absolute bottom-0 w-full rounded-t-sm"
                              style={{ height: `${heightPct}%`, backgroundColor: isStrong ? '#B8860B' : '#8B7355' }}
                            />
                          </div>
                          <span className="text-[7px] text-[#1a1a2e]/50">{sign.slice(0, 3)}</span>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-[9px] text-[#1a1a2e]/50">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#B8860B' }} />{t('kundli.strong')}</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#8B7355' }} />{t('kundli.weak')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-[10px] text-center py-6 text-[#1a1a2e]/40">Loading...</p>
              )}
            </div>

            {/* Shadbala */}
            <div className="border border-[#E8E0D4] rounded-lg p-3">
              <h4 className="text-[11px] font-bold mb-2" style={{ color: '#B8860B' }}>
                {t('kundli.shadbalaTitle')}
              </h4>
              {loadingShadbala ? (
                <div className="flex items-center justify-center py-6"><Loader2 className="w-4 h-4 animate-spin text-[#B8860B]" /></div>
              ) : shadbalaData?.planets ? (
                <div className="space-y-1.5">
                  {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                    const data = shadbalaData.planets[planet];
                    if (!data) return null;
                    const pct = Math.min((data.total / data.required) * 100, 150);
                    const barColor = data.is_strong ? '#B8860B' : '#8B2332';
                    return (
                      <div key={planet} className="flex items-center gap-1.5">
                        <span className="w-10 text-[10px] font-medium text-[#1a1a2e]">{planet}</span>
                        <div className="flex-1 bg-[#E8E0D4] rounded-full h-3 overflow-hidden">
                          <div className="h-full rounded-full" style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }} />
                        </div>
                        <span className={`text-[9px] w-12 text-right font-medium ${data.is_strong ? 'text-[#B8860B]' : 'text-[#8B2332]'}`}>
                          {data.total}/{data.required}
                        </span>
                      </div>
                    );
                  })}
                  <div className="flex items-center gap-3 mt-1 text-[9px] text-[#1a1a2e]/50">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#B8860B' }} />{t('kundli.strong')}</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#8B2332' }} />{t('kundli.weak')}</span>
                  </div>
                </div>
              ) : (
                <p className="text-[10px] text-center py-6 text-[#1a1a2e]/40">Loading...</p>
              )}
            </div>
          </div>

          {/* Footer */}
          <div className="text-center border-t border-[#E8E0D4] pt-2 pb-1">
            <p className="text-[9px] text-[#1a1a2e]/40">
              Generated by Astro Rattan | {new Date().toLocaleDateString()}
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
