import { useMemo } from 'react';
import { LayoutGrid, Home, ShieldCheck, ShieldAlert, Info, AlertTriangle } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import type { LalKitabChartData } from './lalkitab-data';

interface Props {
  chartData: LalKitabChartData;
  apiResult?: any;
}

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

export default function LalKitabKundliTab({ chartData, apiResult }: Props) {
  const { t, language } = useTranslation();

  const counts = useMemo(() => {
    let empty = 0;
    let strong = 0;
    let weak = 0;
    for (const h of chartData.houses) {
      if (h.strength === 'empty') empty++;
      else if (h.strength === 'strong') strong++;
      else if (h.strength === 'weak') weak++;
    }
    return { empty, strong, weak };
  }, [chartData.houses]);

  // Convert API result to InteractiveKundli ChartData format
  const interactiveChartData: ChartData | null = useMemo(() => {
    const planetsRaw = apiResult?.chart_data?.planets;
    if (!planetsRaw) return null;

    const planets: PlanetData[] = Array.isArray(planetsRaw)
      ? planetsRaw.map((p: any) => ({
          planet: p.planet,
          sign: p.sign || 'Unknown',
          house: p.house || 0,
          nakshatra: p.nakshatra || '',
          sign_degree: p.sign_degree || 0,
          status: p.status || '',
          is_retrograde: p.is_retrograde || false,
          is_combust: p.is_combust || false,
          is_vargottama: p.is_vargottama || false,
        }))
      : Object.entries(planetsRaw).map(([name, data]: [string, any]) => ({
          planet: name,
          sign: data?.sign || 'Unknown',
          house: data?.house || 0,
          nakshatra: data?.nakshatra || '',
          sign_degree: data?.sign_degree || 0,
          status: data?.status || '',
          is_retrograde: data?.is_retrograde || false,
          is_combust: data?.is_combust || false,
          is_vargottama: data?.is_vargottama || false,
        }));

    const asc = apiResult.chart_data?.ascendant;
    const ascSign = asc?.sign || 'Aries';
    const ascIdx = ZODIAC_SIGNS.indexOf(ascSign);
    const houses = Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ZODIAC_SIGNS[(ascIdx + i) % 12],
    }));

    return {
      planets,
      houses,
      ascendant: asc ? { longitude: asc.longitude || 0, sign: ascSign, sign_degree: asc.sign_degree } : undefined,
    };
  }, [apiResult]);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-semibold text-sacred-gold flex items-center justify-center gap-2">
          <LayoutGrid className="w-6 h-6" />
          {t('lk.kundli.title')}
        </h2>
        <p className="text-sm text-gray-600">{t('lk.kundli.desc')}</p>
      </div>

      {/* North Indian Kundli Chart via InteractiveKundli */}
      {interactiveChartData ? (
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20 flex justify-center">
          <div className="w-1/2">
            <InteractiveKundli chartData={interactiveChartData} compact />
          </div>
        </div>
      ) : (
        <div className="text-center text-gray-600 py-12 text-sm">
          {t('auto.chartDataNotAvailabl')}
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Empty Houses */}
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <Home className="w-6 h-6 text-sacred-gold/50 mx-auto" />
          <p className="text-sm text-gray-600">{t('lk.kundli.emptyHouses')}</p>
          <p className="text-3xl font-bold text-foreground">{counts.empty}</p>
        </div>

        {/* Strong Houses */}
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <ShieldCheck className="w-6 h-6 text-green-400 mx-auto" />
          <p className="text-sm text-gray-600">{t('lk.kundli.strongHouses')}</p>
          <p className="text-3xl font-bold text-green-400">{counts.strong}</p>
        </div>

        {/* Weak Houses */}
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <ShieldAlert className="w-6 h-6 text-red-400 mx-auto" />
          <p className="text-sm text-gray-600">{t('lk.kundli.weakHouses')}</p>
          <p className="text-3xl font-bold text-red-400">{counts.weak}</p>
        </div>
      </div>

      {/* Calculation Chain — shows only when engine/ayanamsa data is present */}
      {(apiResult?._engine || apiResult?.ayanamsa_system) && (() => {
        const engine = apiResult._engine as string | undefined;
        const ayanamsaSystem = (apiResult.ayanamsa_system as string | undefined) || 'lahiri';
        const ayanamsaVal = apiResult._debug_ayanamsa as number | undefined;
        const julianDay = apiResult._debug_julian_day as number | undefined;
        const isFallback = engine === 'fallback';
        const engineLabel = isFallback
          ? (language === 'hi' ? 'फॉलबैक इंजन' : 'Fallback Engine')
          : 'Swiss Ephemeris';
        const ayanamsaLabel = ayanamsaSystem.charAt(0).toUpperCase() + ayanamsaSystem.slice(1);

        return (
          <div className="rounded-xl border border-gray-200 bg-gray-50/60 p-3 space-y-2">
            {/* Header row */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <Info className="w-3.5 h-3.5 text-gray-400" />
                <span className="text-xs font-semibold text-gray-500">
                  {language === 'hi' ? 'गणना श्रृंखला' : 'Calculation Chain'}
                </span>
              </div>
            </div>

            {/* Fallback warning */}
            {isFallback && (
              <div className="flex items-center gap-1.5 text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-2 py-1">
                <AlertTriangle className="w-3 h-3 shrink-0" />
                <span>
                  {language === 'hi'
                    ? 'अनुमानित स्थिति — Swiss Ephemeris उपलब्ध नहीं'
                    : 'Approximate positions (Swiss Ephemeris not available)'}
                </span>
              </div>
            )}

            {/* Engine + Ayanamsa row */}
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-gray-500">
              <span>
                <span className="font-medium text-gray-600">
                  {language === 'hi' ? 'इंजन:' : 'Engine:'}
                </span>{' '}
                {engineLabel}{!isFallback && <span className="text-green-600 ml-0.5">✓</span>}
              </span>
              <span className="text-gray-300">|</span>
              <span>
                <span className="font-medium text-gray-600">
                  {language === 'hi' ? 'अयनांश:' : 'Ayanamsa:'}
                </span>{' '}
                {ayanamsaLabel}
              </span>
            </div>

            {/* Chain line */}
            {ayanamsaVal !== undefined && (
              <div className="text-xs text-gray-400 font-mono">
                Tropical → -{ayanamsaVal.toFixed(4)}° → Sidereal ({ayanamsaLabel})
              </div>
            )}

            {/* Julian Day */}
            {julianDay !== undefined && (
              <div className="text-xs text-gray-400 font-mono">
                Julian Day: {julianDay.toFixed(1)}
              </div>
            )}
          </div>
        );
      })()}
    </div>
  );
}
