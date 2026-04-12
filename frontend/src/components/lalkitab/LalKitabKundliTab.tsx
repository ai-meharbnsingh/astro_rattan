import { useMemo } from 'react';
import { LayoutGrid, Home, ShieldCheck, ShieldAlert } from 'lucide-react';
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
        <h2 className="text-2xl font-sans font-bold text-sacred-gold flex items-center justify-center gap-2">
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
          {language === 'hi' ? 'कुंडली चार्ट डेटा उपलब्ध नहीं है' : 'Chart data not available'}
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Empty Houses */}
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <Home className="w-6 h-6 text-sacred-gold/50 mx-auto" />
          <p className="text-sm text-gray-600">{t('lk.kundli.emptyHouses')}</p>
          <p className="text-3xl font-sans font-bold text-cosmic-text">{counts.empty}</p>
        </div>

        {/* Strong Houses */}
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <ShieldCheck className="w-6 h-6 text-green-400 mx-auto" />
          <p className="text-sm text-gray-600">{t('lk.kundli.strongHouses')}</p>
          <p className="text-3xl font-sans font-bold text-green-400">{counts.strong}</p>
        </div>

        {/* Weak Houses */}
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <ShieldAlert className="w-6 h-6 text-red-400 mx-auto" />
          <p className="text-sm text-gray-600">{t('lk.kundli.weakHouses')}</p>
          <p className="text-3xl font-sans font-bold text-red-400">{counts.weak}</p>
        </div>
      </div>
    </div>
  );
}
