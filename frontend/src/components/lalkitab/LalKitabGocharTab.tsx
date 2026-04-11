import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { APPROX_TRANSITS_2026, GOCHAR_ALERTS, PLANETS } from './lalkitab-data';
import { Navigation, AlertTriangle, Info, Zap } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
  apiResult?: any;
}

const speedColors: Record<string, string> = {
  slow: 'bg-purple-500/10 text-purple-700 border-purple-300/30',
  medium: 'bg-orange-500/10 text-orange-700 border-orange-300/30',
  fast: 'bg-blue-500/10 text-blue-700 border-blue-300/30',
};

const speedDots: Record<string, string> = {
  slow: 'bg-purple-500',
  medium: 'bg-orange-400',
  fast: 'bg-blue-400',
};

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me',
  Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
};

function getPlanetLabel(key: string, language: string): string {
  const p = PLANETS.find((pl) => pl.key === key);
  if (!p) return key;
  return language === 'hi' ? p.hi : p.en;
}

export default function LalKitabGocharTab({ chartData, apiResult }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  // Lagna sign number (0 = Aries … 11 = Pisces)
  const lagnaSignNum = useMemo(() => {
    const asc =
      apiResult?.chart_data?.ascendant?.sign_number ??
      apiResult?.ascendant?.sign_number ??
      null;
    return typeof asc === 'number' ? asc : null;
  }, [apiResult]);

  /**
   * Convert global LK house (1–12) to natal house from lagna.
   * e.g. if lagna = Cancer (sign 3, index 3), then global house 3 = natal house 1
   */
  function globalToNatal(globalHouse: number): number | null {
    if (lagnaSignNum === null || globalHouse === 0) return null;
    return ((globalHouse - 1 - lagnaSignNum + 12) % 12) + 1;
  }

  // Map transit planet → natal planets sharing that natal house
  const activatedHouses = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (const transit of APPROX_TRANSITS_2026) {
      if (transit.lkHouse === 0) continue;
      const natalH = lagnaSignNum !== null ? globalToNatal(transit.lkHouse) : transit.lkHouse;
      if (!natalH) continue;
      const planetsInHouse = Object.entries(chartData.planetPositions)
        .filter(([, h]) => h === natalH)
        .map(([p]) => p);
      if (!map[natalH]) map[natalH] = [];
      if (!map[natalH].includes(transit.planet)) map[natalH].push(transit.planet);
    }
    return map;
  }, [chartData, lagnaSignNum]);

  const houseLabel = (n: number) => (isHi ? `${n}वाँ भाव` : `House ${n}`);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Navigation className="w-5 h-5" />
          {t('lk.gochar.title')}
        </h2>
        <p className="text-sm text-gray-500">{t('lk.gochar.desc')}</p>
      </div>

      {/* Disclaimer */}
      <div className="flex items-start gap-3 p-4 rounded-xl border border-blue-300/30 bg-blue-500/5">
        <Info className="w-4 h-4 text-blue-500 mt-0.5 shrink-0" />
        <p className="text-xs text-blue-700">{t('lk.gochar.disclaimer')}</p>
      </div>

      {/* Transit Alerts */}
      <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
        <h3 className="font-sans font-semibold text-sacred-gold mb-4 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          {t('lk.gochar.alerts')}
        </h3>
        <div className="space-y-3">
          {GOCHAR_ALERTS.map((alert, idx) => (
            <div
              key={idx}
              className="flex items-start gap-3 p-3 rounded-xl bg-orange-500/5 border border-orange-300/20"
            >
              <Zap className="w-4 h-4 text-orange-500 mt-0.5 shrink-0" />
              <p className="text-sm text-cosmic-text/80 leading-snug">
                {isHi ? alert.hi : alert.en}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Current Transits table */}
      <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
        <h3 className="font-sans font-semibold text-sacred-gold mb-4">
          {t('lk.gochar.currentTransits')}
        </h3>
        <div className="space-y-3">
          {APPROX_TRANSITS_2026.map((transit) => {
            const natalH = lagnaSignNum !== null && transit.lkHouse > 0
              ? globalToNatal(transit.lkHouse)
              : transit.lkHouse > 0 ? transit.lkHouse : null;
            const natalPlanets = natalH
              ? Object.entries(chartData.planetPositions)
                  .filter(([, h]) => h === natalH)
                  .map(([p]) => p)
              : [];

            return (
              <div
                key={transit.planet}
                className="rounded-xl border border-sacred-gold/10 bg-sacred-gold/3 overflow-hidden"
              >
                <div className="flex items-center gap-3 p-3">
                  {/* Speed dot */}
                  <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${speedDots[transit.speedNote]}`} />

                  {/* Planet name */}
                  <div className="min-w-[70px]">
                    <p className="text-sm font-semibold text-cosmic-text">
                      {getPlanetLabel(transit.planet, language)}
                    </p>
                    <span
                      className={`inline-block text-xs px-1.5 py-0.5 rounded-full border ${speedColors[transit.speedNote]}`}
                    >
                      {t(`lk.gochar.${transit.speedNote}`)}
                    </span>
                  </div>

                  {/* House info */}
                  <div className="flex-1 min-w-0">
                    {transit.lkHouse > 0 ? (
                      <div className="flex flex-wrap gap-x-4 gap-y-0.5">
                        <span className="text-xs text-gray-500">
                          <span className="font-medium text-sacred-gold-dark">
                            {t('lk.gochar.globalHouse')}:
                          </span>{' '}
                          {houseLabel(transit.lkHouse)}
                        </span>
                        {natalH && (
                          <span className="text-xs text-gray-500">
                            <span className="font-medium text-sacred-gold-dark">
                              {t('lk.gochar.natalHouse')}:
                            </span>{' '}
                            {houseLabel(natalH)}
                          </span>
                        )}
                      </div>
                    ) : (
                      <span className="text-xs text-gray-400 italic">
                        {isHi ? 'परिवर्तनशील' : 'Variable'}
                      </span>
                    )}

                    <p className="text-xs text-gray-500 mt-1 leading-snug">
                      {isHi ? transit.hi : transit.en}
                    </p>

                    {/* Natal planets in this house */}
                    {natalPlanets.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-1.5">
                        {natalPlanets.map((p) => (
                          <span
                            key={p}
                            className="text-xs px-1.5 py-0.5 rounded bg-sacred-gold/15 text-sacred-gold-dark font-medium"
                          >
                            {PLANET_ABBR[p] || p.slice(0, 2)} {isHi ? '(जन्म)' : '(natal)'}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Activated Natal Houses summary */}
      {Object.keys(activatedHouses).length > 0 && (
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
          <h3 className="font-sans font-semibold text-sacred-gold mb-4">
            {t('lk.gochar.activatedHouses')}
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {Array.from({ length: 12 }, (_, i) => i + 1).map((h) => {
              const transitingPlanets = activatedHouses[h];
              const natalPlanets = Object.entries(chartData.planetPositions)
                .filter(([, hn]) => hn === h)
                .map(([p]) => p);
              if (!transitingPlanets?.length && !natalPlanets.length) return null;
              return (
                <div
                  key={h}
                  className={`p-3 rounded-xl border text-center ${
                    transitingPlanets?.length
                      ? 'border-sacred-gold/30 bg-sacred-gold/8'
                      : 'border-gray-200/50 bg-white/20'
                  }`}
                >
                  <p className="text-sm font-bold text-sacred-gold mb-1">{houseLabel(h)}</p>
                  {transitingPlanets?.length ? (
                    <div className="flex flex-wrap justify-center gap-1">
                      {transitingPlanets.map((p) => (
                        <span
                          key={p}
                          className="text-xs px-1.5 py-0.5 rounded bg-orange-400/20 text-orange-700 font-medium"
                        >
                          {getPlanetLabel(p, language)}
                        </span>
                      ))}
                      <span className="text-xs text-gray-400 w-full mt-1">
                        {isHi ? 'गोचर' : 'Transit'}
                      </span>
                    </div>
                  ) : (
                    <p className="text-xs text-gray-400">{t('lk.gochar.noNatalPlanets')}</p>
                  )}
                </div>
              );
            }).filter(Boolean)}
          </div>
        </div>
      )}
    </div>
  );
}
