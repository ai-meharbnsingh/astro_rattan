import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import {
  PLANETS,
  MIRROR_HOUSES,
  PLANET_EFFECTS_IN_HOUSES,
} from './lalkitab-data';
import { BookOpen, Layers, Eye } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}



export default function LalKitabRulesTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const getPlanetLabel = (key: string) => {
    const planet = PLANETS.find((p) => p.key === key);
    if (!planet) return key;
    return isHi ? planet.hi : planet.en;
  };

  // Build a house-to-planets map for quick lookup
  const housePlanets = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (let h = 1; h <= 12; h++) map[h] = [];
    for (const [planet, house] of Object.entries(chartData.planetPositions)) {
      if (house != null && map[house]) {
        map[house].push(planet);
      }
    }
    return map;
  }, [chartData.planetPositions]);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="font-sans text-2xl text-sacred-gold flex items-center gap-2">
          <BookOpen className="w-6 h-6" />
          {t('lk.rules.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.rules.desc')}</p>
      </div>

      {/* Mirror House Axis */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4">
          {t('lk.rules.mirrorAxis')}
        </h3>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {MIRROR_HOUSES.map(([h1, h2]) => {
            const planetsH1 = housePlanets[h1] ?? [];
            const planetsH2 = housePlanets[h2] ?? [];
            const hasMutual = planetsH1.length > 0 && planetsH2.length > 0;

            return (
              <div
                key={`${h1}-${h2}`}
                className={`card-sacred rounded-xl border transition-all ${
                  hasMutual
                    ? 'border-sacred-gold/40 bg-sacred-gold/5'
                    : 'border-sacred-gold/20'
                }`}
              >
                {/* Two halves with arrow in center */}
                <div className="flex items-stretch">
                  {/* Left house */}
                  <div className="flex-1 p-4 text-center">
                    <p className="text-sm text-gray-600 mb-1">
                      {t('auto.house')}
                    </p>
                    <p className="text-2xl font-sans font-bold text-sacred-gold">
                      {h1}
                    </p>
                    <div className="mt-2 space-y-1">
                      {planetsH1.length > 0 ? (
                        planetsH1.map((p) => (
                          <span
                            key={p}
                            className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mr-1"
                          >
                            {getPlanetLabel(p)}
                          </span>
                        ))
                      ) : (
                        <span className="text-sm text-gray-500 italic">
                          {t('auto.empty')}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Center arrow */}
                  <div className="flex items-center justify-center px-2">
                    <span className="text-sacred-gold/60 text-xl">&#10231;</span>
                  </div>

                  {/* Right house */}
                  <div className="flex-1 p-4 text-center">
                    <p className="text-sm text-gray-600 mb-1">
                      {t('auto.house')}
                    </p>
                    <p className="text-2xl font-sans font-bold text-sacred-gold">
                      {h2}
                    </p>
                    <div className="mt-2 space-y-1">
                      {planetsH2.length > 0 ? (
                        planetsH2.map((p) => (
                          <span
                            key={p}
                            className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mr-1"
                          >
                            {getPlanetLabel(p)}
                          </span>
                        ))
                      ) : (
                        <span className="text-sm text-gray-500 italic">
                          {t('auto.empty')}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Explanation */}
                <div className="border-t border-sacred-gold/10 p-3">
                  {hasMutual ? (
                    <p className="text-sm text-sacred-gold/80 text-center">
                      {t('auto.planetsInHouseH1AndH')}
                    </p>
                  ) : (
                    <p className="text-sm text-gray-500 text-center">
                      {t('auto.planetInHouseH1Affec')}
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Separator */}
      <div className="border-t border-sacred-gold/10" />

      {/* Hidden Influence */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4 flex items-center gap-2">
          <Eye className="w-5 h-5" />
          {t('lk.rules.hiddenInfluence')}
        </h3>

        <div className="grid gap-3 sm:grid-cols-2">
          {Array.from({ length: 6 }, (_, i) => i + 1).map((idx) => (
            <div
              key={idx}
              className="card-sacred rounded-xl p-4 border border-sacred-gold/20"
            >
              <p className="text-sm text-foreground/80">
                {t('lk.rules.hidden.' + idx)}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Separator */}
      <div className="border-t border-sacred-gold/10" />

      {/* Cross-House Effects */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5" />
          {t('lk.rules.crossEffect')}
        </h3>

        <div className="space-y-4">
          {[
            { fromHouse: 1, toHouse: 7 },
            { fromHouse: 4, toHouse: 10 },
            { fromHouse: 5, toHouse: 9 },
            { fromHouse: 2, toHouse: 8 },
            { fromHouse: 3, toHouse: 9 },
            { fromHouse: 6, toHouse: 12 },
            { fromHouse: 7, toHouse: 1 },
            { fromHouse: 10, toHouse: 4 },
          ].map((rule, idx) => {
            const planetsFrom = housePlanets[rule.fromHouse] ?? [];
            const hasPlanets = planetsFrom.length > 0;

            return (
              <div
                key={idx}
                className={`card-sacred rounded-xl p-4 border border-sacred-gold/20 ${
                  hasPlanets ? 'bg-sacred-gold/5' : ''
                }`}
              >
                {/* House labels */}
                <div className="flex items-center gap-3 mb-2 flex-wrap">
                  <span className="px-2.5 py-1 rounded-lg bg-sacred-gold/10 text-sacred-gold text-sm font-sans font-medium">
                    {t('auto.house')} {rule.fromHouse}
                  </span>
                  <span className="text-sacred-gold/40">&#10230;</span>
                  <span className="px-2.5 py-1 rounded-lg bg-sacred-gold/10 text-sacred-gold text-sm font-sans font-medium">
                    {t('auto.house')} {rule.toHouse}
                  </span>
                  <span className="text-sm text-gray-500">
                    ({t('lk.rules.cross.domain.' + (idx + 1))})
                  </span>
                </div>

                {/* Rule text */}
                <p className="text-sm text-gray-600">
                  {t('lk.rules.cross.' + (idx + 1))}
                </p>

                {/* Applied chart data */}
                {hasPlanets && (
                  <div className="mt-3 pt-3 border-t border-sacred-gold/10">
                    <p className="text-sm text-gray-600 mb-1.5">
                      {t('auto.currentPlanetsInHous')}
                    </p>
                    <div className="flex gap-2 flex-wrap">
                      {planetsFrom.map((p) => {
                        const effect =
                          PLANET_EFFECTS_IN_HOUSES[p]?.[rule.fromHouse];
                        return (
                          <div key={p} className="flex-1 min-w-[200px]">
                            <span className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/15 text-sacred-gold text-sm font-medium mb-1">
                              {getPlanetLabel(p)}
                            </span>
                            {effect && (
                              <p className="text-sm text-gray-500">
                                {isHi ? effect.hi : effect.en}
                              </p>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
