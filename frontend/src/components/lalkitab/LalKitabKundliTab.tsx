import { useMemo } from 'react';
import { LayoutGrid, AlertTriangle } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { useLalKitab } from './LalKitabContext';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { toLkPlanetList } from './lalkitab-core';

export default function LalKitabKundliTab() {
  const { t, language } = useTranslation();
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

  const planets: PlanetEntry[] = useMemo(() => {
    const planetsRaw = apiResult?.chart_data?.planets;
    if (!planetsRaw) return [];
    return toLkPlanetList(planetsRaw).map(p => ({
      ...p,
      // Ensure house is used for placement since we force Aries Lagna
      house: p.house, 
    }));
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
        {planets.length > 0 ? (
          <div className="max-w-[420px] mx-auto aspect-square">
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
        ) : (
          <div className="text-center text-sm text-muted-foreground py-10">
            {t('auto.chartDataNotAvailable')}
          </div>
        )}
      </div>
    </div>
  );
}
