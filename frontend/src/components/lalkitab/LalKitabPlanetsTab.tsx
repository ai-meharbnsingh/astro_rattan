import { useState, useEffect } from 'react';
import { Star, ChevronDown, ChevronUp, Moon, ShieldCheck, Zap } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import type { LalKitabChartData } from './lalkitab-data';
import {
  PLANETS,
  PAKKA_GHAR,
  PLANET_FRIENDS,
  PLANET_ENEMIES,
  PLANET_EFFECTS_IN_HOUSES,
} from './lalkitab-data';

interface Props {
  chartData: LalKitabChartData;
  kundliId?: string;
}

export default function LalKitabPlanetsTab({ chartData, kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const [expandedPlanet, setExpandedPlanet] = useState<string | null>(null);
  const [advancedData, setAdvancedData] = useState<any>(null);

  useEffect(() => {
    if (kundliId) {
      api.get(`/api/lalkitab/advanced/${kundliId}`)
        .then(setAdvancedData)
        .catch(console.error);
    }
  }, [kundliId]);

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
        <p className="text-gray-600 text-sm">
          {t('lk.planets.desc')}
        </p>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap justify-center gap-4 py-2 border-y border-sacred-gold/10">
        <div className="flex items-center gap-1.5 text-xs text-cosmic-text/70">
          <Zap className="w-3.5 h-3.5 text-green-500" />
          <span>{t('lk.planets.active')}</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-cosmic-text/70">
          <Moon className="w-3.5 h-3.5 text-orange-500" />
          <span>{t('lk.planets.sleeping')}</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-cosmic-text/70">
          <ShieldCheck className="w-3.5 h-3.5 text-sacred-gold" />
          <span>{t('lk.planets.stable')}</span>
        </div>
      </div>

      {/* Planet Cards Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {PLANETS.map((planet) => {
          const house = chartData.planetPositions[planet.key];
          const pakkaGhar = PAKKA_GHAR[planet.key];
          const isExpanded = expandedPlanet === planet.key;
          const friends = PLANET_FRIENDS[planet.key] || [];
          const enemies = PLANET_ENEMIES[planet.key] || [];
          const effect = house
            ? PLANET_EFFECTS_IN_HOUSES[planet.key]?.[house]
            : null;

          // Advanced statuses
          const isSleeping = advancedData?.sleeping?.sleeping_planets?.find((p: any) => p.planet === planet.key);
          const isKayam = advancedData?.kayam?.includes(planet.key);

          return (
            <div
              key={planet.key}
              onClick={() => togglePlanet(planet.key)}
              className={`card-sacred rounded-xl p-5 border transition-all cursor-pointer hover:shadow-md ${
                isExpanded ? 'border-sacred-gold/50 bg-sacred-gold/5' : 'border-sacred-gold/20'
              }`}
            >
              {/* Collapsed View */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Star className={`w-5 h-5 ${isKayam ? 'text-sacred-gold fill-sacred-gold/20' : 'text-sacred-gold/40'}`} />
                  <div>
                    <h3 className="font-sans text-sacred-gold text-lg">
                      {getPlanetName(planet)}
                    </h3>
                    <p className="text-gray-500 text-xs">
                      {t('lk.planets.housePlacement')}: {house ?? '—'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="flex flex-col items-end">
                    {isSleeping ? (
                      <span className="flex items-center gap-1 text-[10px] font-bold text-orange-600 bg-orange-50 px-1.5 py-0.5 rounded border border-orange-100">
                        <Moon className="w-2.5 h-2.5" />
                        {t('auto.sLEEPING')}
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-[10px] font-bold text-green-600 bg-green-50 px-1.5 py-0.5 rounded border border-green-100">
                        <Zap className="w-2.5 h-2.5" />
                        {t('auto.aCTIVE')}
                      </span>
                    )}
                    {isKayam && (
                      <span className="mt-1 flex items-center gap-1 text-[10px] font-bold text-sacred-gold-dark bg-sacred-gold/10 px-1.5 py-0.5 rounded border border-sacred-gold/20">
                        <ShieldCheck className="w-2.5 h-2.5" />
                        {t('auto.kAYAM')}
                      </span>
                    )}
                  </div>
                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-sacred-gold/60 ml-1" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-sacred-gold/60 ml-1" />
                  )}
                </div>
              </div>

              {/* Expanded View */}
              {isExpanded && (
                <div className="mt-4 space-y-4 border-t border-sacred-gold/10 pt-4">
                  {/* Status Badges with Explanation */}
                  <div className="grid grid-cols-2 gap-2">
                    <div className={`p-2 rounded-lg border ${isSleeping ? 'bg-orange-50 border-orange-100' : 'bg-green-50 border-green-100'}`}>
                      <p className={`text-[10px] font-bold uppercase tracking-widest ${isSleeping ? 'text-orange-700' : 'text-green-700'}`}>
                        {isSleeping ? t('lk.planets.sleeping') : t('lk.planets.active')}
                      </p>
                      <p className="text-[10px] text-cosmic-text/60 mt-1">
                        {isSleeping 
                          ? (isHi ? isSleeping.reason.hi : isSleeping.reason.en)
                          : (t('auto.selfActivatedAndFrui'))}
                      </p>
                    </div>
                    <div className={`p-2 rounded-lg border ${isKayam ? 'bg-sacred-gold/10 border-sacred-gold/30' : 'bg-gray-50 border-gray-200'}`}>
                      <p className={`text-[10px] font-bold uppercase tracking-widest ${isKayam ? 'text-sacred-gold-dark' : 'text-gray-500'}`}>
                        {isKayam ? t('lk.planets.stable') : t('lk.planets.unstable')}
                      </p>
                      <p className="text-[10px] text-cosmic-text/60 mt-1">
                        {isKayam ? t('lk.planets.kayamDesc') : (t('auto.underInfluenceOfEnem'))}
                      </p>
                    </div>
                  </div>

                  {/* Pakka Ghar */}
                  <div>
                    <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                      {t('lk.planets.pakkaGhar')}
                    </span>
                    <p className="text-sacred-gold font-sans text-sm mt-0.5">
                      {t('auto.housePakkaGhar')}
                    </p>
                  </div>

                  {/* Friendly / Enemies */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                        {t('lk.planets.friends')}
                      </span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {friends.map((f) => (
                          <span key={f} className="text-[10px] text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded">
                            {getFriendName(f)}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                        {t('lk.planets.enemies')}
                      </span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {enemies.map((e) => (
                          <span key={e} className="text-[10px] text-red-600 bg-red-50 px-1.5 py-0.5 rounded">
                            {getFriendName(e)}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Effect */}
                  {effect && (
                    <div className="bg-white/60 p-3 rounded-lg border border-sacred-gold/10 shadow-inner">
                      <span className="text-[10px] font-bold text-sacred-gold uppercase tracking-widest">
                        {t('lk.planets.effect')}
                      </span>
                      <p className="text-sm text-cosmic-text mt-1 leading-relaxed italic">
                        "{language === 'hi' ? effect.hi : effect.en}"
                      </p>
                    </div>
                  )}

                  {/* Lal Kitab Aspects */}
                  {advancedData?.aspects?.[planet.key] && advancedData.aspects[planet.key].length > 0 && (
                    <div>
                      <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                        {t('auto.lalKitabAspects')}
                      </span>
                      <div className="space-y-1.5 mt-1.5">
                        {advancedData.aspects[planet.key].map((asp: any, idx: number) => (
                          <div key={idx} className="flex items-center justify-between text-xs p-2 rounded bg-sacred-gold/5 border border-sacred-gold/10">
                            <span className="font-medium text-cosmic-text">
                              {t('auto.aspects')} {getFriendName(asp.aspects_to)}
                            </span>
                            <span className="text-sacred-gold-dark font-bold">
                              {asp.strength * 100}% {t('auto.power')}
                            </span>
                          </div>
                        ))}
                      </div>
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
