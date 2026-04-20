import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Calendar } from 'lucide-react';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { toLkPlanetList } from './lalkitab-core';
import { Heading } from '@/components/ui/heading';

/** Build the current year and +/- 5 years range. */
function getYearRange(): number[] {
  const current = new Date().getFullYear();
  const years: number[] = [];
  for (let y = current - 5; y <= current + 5; y++) {
    years.push(y);
  }
  return years;
}

export default function LalKitabVarshphalTab() {
  const { t, language } = useTranslation();
  const { kundliId } = useLalKitab();
  const isHi = language === 'hi';

  const currentYear = new Date().getFullYear();
  const [selectedYear, setSelectedYear] = useState<number>(currentYear);
  const yearRange = useMemo(() => getYearRange(), []);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [data, setData] = useState<any | null>(null);

  const load = async () => {
    if (!kundliId) return;
    setLoading(true);
    setError('');
    try {
      const res = await api.post(`/api/kundli/${kundliId}/varshphal`, { year: selectedYear });
      setData(res);
    } catch (e: any) {
      setData(null);
      setError(isHi ? 'वर्षफल लोड नहीं हो पाया।' : 'Failed to load Varshphal.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Auto-load on first render when we have a kundli id.
    if (!kundliId) return;
    if (data) return;
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [kundliId]);

  const planets: PlanetEntry[] = useMemo(() => {
    const planetsRaw = data?.chart_data?.planets;
    if (!planetsRaw) return [];
    return toLkPlanetList(planetsRaw).map(p => ({
      ...p,
      house: p.house,
    }));
  }, [data]);

  return (
    <div className="space-y-8">
      {/* ─── Header ─── */}
      <div className="text-center space-y-2">
        <Heading as={2} variant={2} className="text-sacred-gold-dark flex items-center justify-center gap-2">
          <Calendar className="w-6 h-6" />
          {t('lk.varshphal.title')}
        </Heading>
        <p className="text-sm text-gray-600">{t('lk.varshphal.desc')}</p>
      </div>

      {/* ─── Year Selector ─── */}
      <div className="flex items-center justify-center gap-3">
        <label className="text-sm font-medium text-sacred-gold">
          {t('lk.varshphal.selectYear')}
        </label>
        <select
          value={selectedYear}
          onChange={(e) => setSelectedYear(Number(e.target.value))}
          className="rounded-xl bg-card border border-sacred-gold/20 text-foreground px-4 py-3 focus:outline-none focus:border-sacred-gold/50 transition-colors"
          disabled={!kundliId || loading}
        >
          {yearRange.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
        <button
          onClick={load}
          disabled={!kundliId || loading}
          className="px-4 py-3 rounded-xl bg-sacred-gold text-white font-semibold text-sm disabled:opacity-60"
        >
          {loading ? (isHi ? 'गणना...' : 'Calculating...') : (isHi ? 'वर्षफल देखें' : 'View Varshphal')}
        </button>
      </div>

      {!kundliId && (
        <div className="p-6 text-center border border-amber-200 bg-amber-50 rounded-xl text-amber-900">
          {isHi ? 'वर्षफल देखने के लिए पहले एक कुंडली लोड करें।' : 'Load a Kundli first to view Varshphal.'}
        </div>
      )}

      {!!error && (
        <div className="p-4 text-center border border-red-200 bg-red-50 rounded-xl text-red-800 text-sm">
          {error}
        </div>
      )}

      {data && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="rounded-xl border border-sacred-gold/20 bg-sacred-gold/5 p-4">
              <div className="text-xs text-muted-foreground">{isHi ? 'सोलर रिटर्न' : 'Solar Return'}</div>
              <div className="text-sm font-semibold text-foreground mt-1">
                    {data?.solar_return?.date || (isHi ? 'उपलब्ध नहीं' : 'Not Available')} {data?.solar_return?.time || ''}
              </div>
            </div>
            <div className="rounded-xl border border-sacred-gold/20 bg-sacred-gold/5 p-4">
              <div className="text-xs text-muted-foreground">{isHi ? 'मुनथा' : 'Muntha'}</div>
              <div className="text-sm font-semibold text-foreground mt-1">
                {isHi ? 'भाव' : 'House'} {isNaN(Number(data?.muntha?.house)) ? 0 : data?.muntha?.house}
                {data?.muntha?.favorable ? (isHi ? ' (अनुकूल)' : ' (favorable)') : (isHi ? ' (सावधानी)' : ' (caution)')}
              </div>
            </div>
            <div className="rounded-xl border border-sacred-gold/20 bg-sacred-gold/5 p-4">
              <div className="text-xs text-muted-foreground">{isHi ? 'वर्षेश' : 'Year Lord'}</div>
              <div className="text-sm font-semibold text-foreground mt-1">
                {String(data?.year_lord || '')}
              </div>
            </div>
          </div>

          {planets.length > 0 && (
            <div className="rounded-xl border border-sacred-gold/20 bg-white p-4">
              <div className="text-sm font-semibold text-sacred-gold mb-3">
                {t('lk.varshphal.annualChart')}
              </div>
              <div className="flex justify-center">
                <div className="w-full max-w-[420px] aspect-square">
                  <KundliChartSVG
                    planets={planets}
                    ascendantSign="Aries" // Lal Kitab is ALWAYS fixed to Aries Lagna
                    language={language}
                    showRashiNumbers={true}
                    showHouseNumbers={false}
                    rashiNumberPlacement="center"
                    showAscendantMarker={false}
                  />
                </div>
              </div>
            </div>
          )}

          {!!data?.mudda_dasha?.length && (
            <div className="rounded-xl border border-sacred-gold/20 bg-white p-4">
              <div className="text-sm font-semibold text-sacred-gold mb-3">
                {isHi ? 'मुद्दा दशा' : 'Mudda Dasha'}
              </div>
              <div className="space-y-2">
                {data.mudda_dasha.map((md: any) => {
                  const isCurrent = md.planet === data.current_mudda_dasha;
                  return (
                    <div key={`${md.planet}-${md.start_date}`} className={`rounded-lg border p-3 ${isCurrent ? 'border-sacred-gold bg-sacred-gold/10' : 'border-border bg-card'}`}>
                      <div className="flex items-center justify-between">
                        <div className="font-semibold text-foreground">{md.planet}{isCurrent ? (isHi ? ' (वर्तमान)' : ' (current)') : ''}</div>
                        <div className="text-xs text-muted-foreground">{md.start_date} → {md.end_date}</div>
                      </div>
                      <div className="text-xs text-muted-foreground mt-1">
                        {isHi ? 'दिन' : 'Days'}: {md.days}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
