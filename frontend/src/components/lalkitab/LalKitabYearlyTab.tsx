import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import {
  AGE_PLANET_ACTIVATION,
  PLANETS,
  PLANET_EFFECTS_IN_HOUSES,
} from './lalkitab-data';
import { Calendar, Star } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
  birthDate: string;
}

export default function LalKitabYearlyTab({ chartData, birthDate }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const currentAge = useMemo(() => {
    if (!birthDate) return 0;
    const birth = new Date(birthDate);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return Math.max(0, age);
  }, [birthDate]);

  const activePeriod = useMemo(
    () =>
      AGE_PLANET_ACTIVATION.find(
        (p) => currentAge >= p.ageStart && currentAge <= p.ageEnd
      ) ?? null,
    [currentAge]
  );

  const getPlanetLabel = (key: string) => {
    const planet = PLANETS.find((p) => p.key === key);
    if (!planet) return key;
    return isHi ? planet.hi : planet.en;
  };

  const getActivePrediction = () => {
    if (!activePeriod) return null;
    const house = chartData.planetPositions[activePeriod.planet];
    if (house == null) return null;
    return PLANET_EFFECTS_IN_HOUSES[activePeriod.planet]?.[house] ?? null;
  };

  const prediction = getActivePrediction();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="font-sans text-2xl text-sacred-gold flex items-center gap-2">
          <Calendar className="w-6 h-6" />
          {t('lk.yearly.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.yearly.desc')}</p>
      </div>

      {/* Current age display */}
      <div className="rounded-xl p-6 border border-sacred-gold/20 bg-sacred-gold/5 text-center">
        <p className="text-sm text-sacred-gold/70 mb-1">{t('lk.yearly.currentAge')}</p>
        <p className="text-5xl font-sans font-bold text-sacred-gold">{currentAge}</p>
        {activePeriod && (
          <p className="text-sm text-gray-500 mt-2">
            {t('auto.activePlanet')}:{' '}
            <span className="text-sacred-gold font-medium">
              {getPlanetLabel(activePeriod.planet)}
            </span>
          </p>
        )}
      </div>

      {/* Active period prediction */}
      {activePeriod && prediction && (
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/30 bg-sacred-gold/5">
          <div className="flex items-start gap-3">
            <Star className="w-5 h-5 text-sacred-gold mt-0.5 shrink-0" />
            <div>
              <h3 className="font-sans text-lg text-sacred-gold mb-1">
                {getPlanetLabel(activePeriod.planet)} —{' '}
                {t('auto.house')} {chartData.planetPositions[activePeriod.planet]}
              </h3>
              <p className="text-sm text-foreground/80">
                {isHi ? prediction.hi : prediction.en}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Timeline visualization */}
      <div className="relative">
        {AGE_PLANET_ACTIVATION.map((period, idx) => {
          const isActive =
            currentAge >= period.ageStart && currentAge <= period.ageEnd;
          const isLast = idx === AGE_PLANET_ACTIVATION.length - 1;
          const house = chartData.planetPositions[period.planet];
          const effect =
            house != null
              ? PLANET_EFFECTS_IN_HOUSES[period.planet]?.[house]
              : null;

          return (
            <div key={period.planet} className="relative flex gap-4">
              {/* Timeline line and node */}
              <div className="flex flex-col items-center">
                {/* Node */}
                <div
                  className={`w-4 h-4 rounded-full shrink-0 z-10 ${
                    isActive
                      ? 'bg-sacred-gold shadow-lg shadow-sacred-gold/30'
                      : 'bg-card border border-sacred-gold/20'
                  }`}
                />
                {/* Connecting line */}
                {!isLast && (
                  <div
                    className={`w-0.5 flex-1 min-h-[2rem] ${
                      isActive ? 'bg-sacred-gold/40' : 'bg-sacred-gold/10'
                    }`}
                  />
                )}
              </div>

              {/* Content */}
              <div
                className={`pb-6 flex-1 rounded-xl px-4 py-3 mb-2 transition-all ${
                  isActive
                    ? 'border border-sacred-gold/30 bg-sacred-gold/5'
                    : 'border border-transparent'
                }`}
              >
                <div className="flex items-center gap-2 flex-wrap">
                  <span
                    className={`font-sans text-base font-semibold ${
                      isActive ? 'text-sacred-gold' : 'text-gray-600'
                    }`}
                  >
                    {getPlanetLabel(period.planet)}
                  </span>
                  <span
                    className={`text-sm px-2 py-0.5 rounded-full ${
                      isActive
                        ? 'bg-sacred-gold/20 text-sacred-gold'
                        : 'bg-card text-gray-600'
                    }`}
                  >
                    {t('lk.yearly.ageRange')}: {period.ageStart}–{period.ageEnd}
                  </span>
                  {isActive && (
                    <span className="text-sm px-2 py-0.5 rounded-full bg-green-500/15 text-green-500 font-medium">
                      {t('auto.active')}
                    </span>
                  )}
                </div>

                {/* Show effect text for active period */}
                {isActive && effect && (
                  <p className="text-sm text-gray-600 mt-2">
                    {isHi ? effect.hi : effect.en}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
