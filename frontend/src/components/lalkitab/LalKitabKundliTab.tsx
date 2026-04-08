import { useMemo } from 'react';
import { LayoutGrid, Home, ShieldCheck, ShieldAlert } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { PLANETS, PAKKA_GHAR } from './lalkitab-data';

interface Props {
  chartData: LalKitabChartData;
}

/**
 * North-Indian style 4x4 grid layout.
 * Houses map to grid positions (row, col, rowSpan, colSpan).
 * The center 2x2 block is reserved for the chart title.
 */
const HOUSE_GRID: Record<
  number,
  { row: number; col: number; rowSpan?: number; colSpan?: number }
> = {
  12: { row: 1, col: 1 },
  1:  { row: 1, col: 2 },
  2:  { row: 1, col: 3 },
  3:  { row: 1, col: 4 },
  11: { row: 2, col: 1 },
  4:  { row: 2, col: 4 },
  10: { row: 3, col: 1 },
  5:  { row: 3, col: 4 },
  9:  { row: 4, col: 1 },
  8:  { row: 4, col: 2 },
  7:  { row: 4, col: 3 },
  6:  { row: 4, col: 4 },
};

function getPlanetLabel(key: string, language: string): string {
  const planet = PLANETS.find((p) => p.key === key);
  if (!planet) return key;
  return language === 'hi' ? planet.hi : planet.en;
}

export default function LalKitabKundliTab({ chartData }: Props) {
  const { t, language } = useTranslation();

  const houseMap = useMemo(() => {
    const map = new Map<number, (typeof chartData.houses)[number]>();
    for (const h of chartData.houses) {
      map.set(h.house, h);
    }
    return map;
  }, [chartData.houses]);

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

  const cellClass = (strength: string | undefined) => {
    if (strength === 'strong') return 'border-green-500/50 bg-green-500/5';
    if (strength === 'weak') return 'border-red-500/50 bg-red-500/5';
    return 'border-sacred-gold/10 bg-cosmic-card/50';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-sacred font-bold text-sacred-gold flex items-center justify-center gap-2">
          <LayoutGrid className="w-6 h-6" />
          {t('lk.kundli.title')}
        </h2>
        <p className="text-sm text-cosmic-text/70">{t('lk.kundli.desc')}</p>
      </div>

      {/* Visual Kundli Chart */}
      <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
        <div className="grid grid-cols-4 gap-1 max-w-2xl mx-auto">
          {/* Render 12 houses */}
          {[12, 1, 2, 3, 11, 4, 10, 5, 9, 8, 7, 6].map((houseNum) => {
            const pos = HOUSE_GRID[houseNum];
            const house = houseMap.get(houseNum);
            const strength = house?.strength;
            const planets = house?.planets ?? [];

            return (
              <div
                key={houseNum}
                className={`border rounded-lg min-h-[80px] p-2 flex flex-col items-center justify-center text-center transition-colors ${cellClass(strength)} border-sacred-gold/30`}
                style={{
                  gridRow: `${pos.row} / span ${pos.rowSpan ?? 1}`,
                  gridColumn: `${pos.col} / span ${pos.colSpan ?? 1}`,
                }}
              >
                <span className="text-[10px] font-medium text-sacred-gold-dark/70 uppercase tracking-wide">
                  {t('lk.kundli.house')} {houseNum}
                </span>
                {planets.length > 0 ? (
                  <div className="mt-1 flex flex-wrap gap-1 justify-center">
                    {planets.map((pKey) => (
                      <span
                        key={pKey}
                        className="text-xs font-semibold text-cosmic-text bg-sacred-gold/10 rounded px-1.5 py-0.5"
                      >
                        {getPlanetLabel(pKey, language)}
                      </span>
                    ))}
                  </div>
                ) : (
                  <span className="mt-1 text-[11px] text-cosmic-text/60 italic">
                    {t('lk.kundli.empty')}
                  </span>
                )}
                {strength && strength !== 'empty' && (
                  <span
                    className={`mt-1 text-[10px] font-medium ${
                      strength === 'strong' ? 'text-green-400' : 'text-red-400'
                    }`}
                  >
                    {strength === 'strong' ? t('lk.kundli.strong') : t('lk.kundli.weak')}
                  </span>
                )}
              </div>
            );
          })}

          {/* Center 2x2 block — chart title */}
          <div
            className="flex flex-col items-center justify-center rounded-lg border border-sacred-gold/20 bg-sacred-gold/5"
            style={{ gridRow: '2 / span 2', gridColumn: '2 / span 2' }}
          >
            <span className="font-sacred text-lg font-bold text-sacred-gold">
              {language === 'hi' ? 'लाल किताब' : 'Lal Kitab'}
            </span>
            <span className="text-[11px] text-cosmic-text/60">
              {language === 'hi' ? 'कुंडली' : 'Kundli'}
            </span>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Empty Houses */}
        <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <Home className="w-6 h-6 text-sacred-gold/50 mx-auto" />
          <p className="text-sm text-cosmic-text/70">{t('lk.kundli.emptyHouses')}</p>
          <p className="text-3xl font-sacred font-bold text-cosmic-text">{counts.empty}</p>
        </div>

        {/* Strong Houses */}
        <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <ShieldCheck className="w-6 h-6 text-green-400 mx-auto" />
          <p className="text-sm text-cosmic-text/70">{t('lk.kundli.strongHouses')}</p>
          <p className="text-3xl font-sacred font-bold text-green-400">{counts.strong}</p>
        </div>

        {/* Weak Houses */}
        <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20 text-center space-y-2">
          <ShieldAlert className="w-6 h-6 text-red-400 mx-auto" />
          <p className="text-sm text-cosmic-text/70">{t('lk.kundli.weakHouses')}</p>
          <p className="text-3xl font-sacred font-bold text-red-400">{counts.weak}</p>
        </div>
      </div>
    </div>
  );
}
