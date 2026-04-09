import { useState } from 'react';
import { Star, ChevronDown, ChevronUp } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import {
  PLANETS,
  PAKKA_GHAR,
  PLANET_FRIENDS,
  PLANET_ENEMIES,
  getPlanetStatus,
  PLANET_EFFECTS_IN_HOUSES,
} from './lalkitab-data';

interface Props {
  chartData: LalKitabChartData;
}

export default function LalKitabPlanetsTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const [expandedPlanet, setExpandedPlanet] = useState<string | null>(null);

  const togglePlanet = (key: string) => {
    setExpandedPlanet((prev) => (prev === key ? null : key));
  };

  const getPlanetName = (planet: (typeof PLANETS)[number]) => {
    return language === 'hi' ? planet.hi : planet.en;
  };

  const getFriendName = (key: string) => {
    const planet = PLANETS.find((p) => p.key === key);
    if (!planet) return key;
    return language === 'hi' ? planet.hi : planet.en;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-sans text-sacred-gold">
          {t('lk.planets.title')}
        </h2>
        <p className="text-cosmic-text/70 text-sm">
          {t('lk.planets.desc')}
        </p>
      </div>

      {/* Planet Cards Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {PLANETS.map((planet) => {
          const house = chartData.planetPositions[planet.key];
          const pakkaGhar = PAKKA_GHAR[planet.key];
          const status = getPlanetStatus(planet.key, chartData);
          const isExpanded = expandedPlanet === planet.key;
          const friends = PLANET_FRIENDS[planet.key] || [];
          const enemies = PLANET_ENEMIES[planet.key] || [];
          const effect = house
            ? PLANET_EFFECTS_IN_HOUSES[planet.key]?.[house]
            : null;

          return (
            <div
              key={planet.key}
              onClick={() => togglePlanet(planet.key)}
              className="card-sacred rounded-2xl p-5 border border-sacred-gold/20 cursor-pointer hover:border-sacred-gold/40 transition-all"
            >
              {/* Collapsed View — always visible */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Star className="w-5 h-5 text-sacred-gold" />
                  <div>
                    <h3 className="font-sans text-sacred-gold text-lg">
                      {getPlanetName(planet)}
                    </h3>
                    <p className="text-cosmic-text/60 text-sm">
                      {t('lk.planets.housePlacement')}: {house ?? '—'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {status === 'active' ? (
                    <span className="bg-green-500/20 text-green-600 px-2 py-0.5 rounded-full text-sm">
                      {t('lk.planets.active')}
                    </span>
                  ) : (
                    <span className="bg-orange-500/20 text-orange-600 px-2 py-0.5 rounded-full text-sm">
                      {t('lk.planets.sleeping')}
                    </span>
                  )}
                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-sacred-gold/60" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-sacred-gold/60" />
                  )}
                </div>
              </div>

              {/* Expanded View */}
              {isExpanded && (
                <div className="mt-4 space-y-4 border-t border-sacred-gold/10 pt-4">
                  {/* Pakka Ghar */}
                  <div>
                    <span className="text-sm text-cosmic-text/70 uppercase tracking-wide">
                      {t('lk.planets.pakkaGhar')}
                    </span>
                    <p className="text-sacred-gold font-sans text-sm mt-0.5">
                      {language === 'hi' ? `भाव ${pakkaGhar}` : `House ${pakkaGhar}`}
                    </p>
                  </div>

                  {/* Friendly Planets */}
                  <div>
                    <span className="text-sm text-cosmic-text/70 uppercase tracking-wide">
                      {t('lk.planets.friends')}
                    </span>
                    <div className="flex flex-wrap gap-1.5 mt-1.5">
                      {friends.map((f) => (
                        <span
                          key={f}
                          className="bg-blue-500/10 text-blue-600 border border-blue-500/20 px-2 py-0.5 rounded-full text-sm"
                        >
                          {getFriendName(f)}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Enemy Planets */}
                  <div>
                    <span className="text-sm text-cosmic-text/70 uppercase tracking-wide">
                      {t('lk.planets.enemies')}
                    </span>
                    <div className="flex flex-wrap gap-1.5 mt-1.5">
                      {enemies.map((e) => (
                        <span
                          key={e}
                          className="bg-red-500/10 text-red-600 border border-red-500/20 px-2 py-0.5 rounded-full text-sm"
                        >
                          {getFriendName(e)}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Effect */}
                  {effect && (
                    <div>
                      <span className="text-sm text-cosmic-text/70 uppercase tracking-wide">
                        {t('lk.planets.effect')}
                      </span>
                      <p className="text-cosmic-text text-sm mt-1 leading-relaxed">
                        {language === 'hi' ? effect.hi : effect.en}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
