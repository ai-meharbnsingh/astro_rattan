import { useMemo } from 'react';
import { LayoutGrid, AlertTriangle } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { useLalKitab } from './LalKitabContext';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

export default function LalKitabKundliTab() {
  const { t } = useTranslation();
  const { apiResult, fullData } = useLalKitab();

  const emptyHouses = useMemo(() => {
    const byHouse: Record<number, number> = {};
    for (let h = 1; h <= 12; h++) byHouse[h] = 0;
    for (const p of (fullData?.positions || [])) {
      const h = Number(p?.house || 0);
      if (h >= 1 && h <= 12) byHouse[h] += 1;
    }
    return Object.values(byHouse).filter((n) => n === 0).length;
  }, [fullData]);

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

    const asc = apiResult?.chart_data?.ascendant;
    const ascSign = asc?.sign || 'Aries';
    const ascIdx = ZODIAC_SIGNS.indexOf(ascSign);
    const houses = Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ZODIAC_SIGNS[(ascIdx >= 0 ? ascIdx : 0 + i) % 12],
    }));

    return { planets, houses, ascendant: asc ? { longitude: asc.longitude || 0, sign: ascSign, sign_degree: asc.sign_degree } : undefined };
  }, [apiResult]);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <LayoutGrid className="w-5 h-5 text-sacred-gold" />
        <h3 className="font-sans text-lg font-semibold text-sacred-gold">{t('auto.chart')}</h3>
      </div>

      {fullData?.positions?.length === 0 && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-800 text-sm flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
          <div>
            <div className="font-semibold">{t('lk.chart.incompleteWarning')}</div>
            <div className="text-xs opacity-80">{t('auto.chartNotAvailable')}</div>
          </div>
        </div>
      )}

      <div className="rounded-xl border border-sacred-gold/20 bg-card p-4">
        <div className="text-xs text-muted-foreground mb-3">
          {t('lk.kundli.empty')}: {emptyHouses}
        </div>
        {interactiveChartData ? (
          <div className="max-w-[520px] mx-auto">
            <InteractiveKundli chartData={interactiveChartData} compact />
          </div>
        ) : (
          <div className="text-center text-sm text-muted-foreground py-10">
            {t('auto.chartDataNotAvailabl')}
          </div>
        )}
      </div>
    </div>
  );
}

