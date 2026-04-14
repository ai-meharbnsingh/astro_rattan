import { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { HOUSE_MEANINGS, PLANET_EFFECTS_IN_HOUSES } from './lalkitab-data';
import { ChevronDown, ChevronUp, Home } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}

export default function LalKitabHousesTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const [expandedHouse, setExpandedHouse] = useState<number | null>(null);

  const toggleHouse = (houseNumber: number) => {
    setExpandedHouse((prev) => (prev === houseNumber ? null : houseNumber));
  };

  const getStrengthDot = (strength: 'strong' | 'weak' | 'empty') => {
    if (strength === 'strong') return 'bg-green-500';
    if (strength === 'weak') return 'bg-red-500';
    return 'bg-gray-500';
  };

  const getStrengthLabel = (strength: 'strong' | 'weak' | 'empty') => {
    if (strength === 'strong') return t('auto.strong');
    if (strength === 'weak') return t('auto.weak');
    return t('auto.empty');
  };

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-xl font-sans font-semibold text-sacred-gold mb-1">
          {t('lk.houses.title')}
        </h2>
        <p className="text-sm text-gray-500">
          {t('lk.houses.desc')}
        </p>
      </div>

      {/* House Cards */}
      <div className="grid gap-4">
        {chartData.houses.map((houseData) => {
          const houseIndex = houseData.house - 1;
          const meaning = HOUSE_MEANINGS[houseIndex];
          const isExpanded = expandedHouse === houseData.house;

          return (
            <div
              key={houseData.house}
              className="card-sacred rounded-xl border border-sacred-gold/20 overflow-hidden transition-all"
            >
              {/* Collapsed View */}
              <button
                type="button"
                onClick={() => toggleHouse(houseData.house)}
                className="w-full flex items-center justify-between p-4 text-left"
              >
                <div className="flex items-center gap-4">
                  {/* House Number */}
                  <div className="flex items-center gap-2">
                    <Home className="w-5 h-5 text-sacred-gold/60" />
                    <span className="text-2xl font-sans font-bold text-sacred-gold">
                      {houseData.house}
                    </span>
                  </div>

                  {/* General Meaning & Badges */}
                  <div className="flex flex-col gap-1">
                    <span className="text-sm text-cosmic-text">
                      {language === 'hi' ? meaning.hi : meaning.en}
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {meaning.lifeAreas.map((area, idx) => (
                        <span
                          key={idx}
                          className="bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20 px-2 py-0.5 rounded-full text-sm"
                        >
                          {language === 'hi' ? area.hi : area.en}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {/* Planets in house */}
                  {houseData.planets.length > 0 && (
                    <div className="flex gap-1">
                      {houseData.planets.map((planet, idx) => (
                        <span
                          key={idx}
                          className="bg-sacred-gold/10 text-sacred-gold px-2 py-0.5 rounded-full text-sm font-medium"
                        >
                          {planet}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Strength Indicator */}
                  <div className="flex items-center gap-1.5">
                    <span className={`w-2.5 h-2.5 rounded-full ${getStrengthDot(houseData.strength)}`} />
                    <span className="text-sm text-gray-600">
                      {getStrengthLabel(houseData.strength)}
                    </span>
                  </div>

                  {/* Chevron */}
                  {isExpanded ? (
                    <ChevronUp className="w-5 h-5 text-sacred-gold/60" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-sacred-gold/60" />
                  )}
                </div>
              </button>

              {/* Expanded View */}
              {isExpanded && (
                <div className="px-4 pb-4 space-y-4 border-t border-sacred-gold/10 pt-4">
                  {/* Meaning */}
                  <div>
                    <h4 className="text-sm font-semibold text-sacred-gold mb-1">
                      {t('lk.houses.meaning')}
                    </h4>
                    <p className="text-sm text-cosmic-text/80">
                      {language === 'hi' ? meaning.hi : meaning.en}
                    </p>
                  </div>

                  {/* Life Areas */}
                  <div>
                    <h4 className="text-sm font-semibold text-sacred-gold mb-2">
                      {t('lk.houses.lifeAreas')}
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {meaning.lifeAreas.map((area, idx) => (
                        <span
                          key={idx}
                          className="bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20 px-2 py-0.5 rounded-full text-sm"
                        >
                          {language === 'hi' ? area.hi : area.en}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Planet Effects */}
                  <div>
                    <h4 className="text-sm font-semibold text-sacred-gold mb-2">
                      {t('lk.houses.planetEffect')}
                    </h4>

                    {houseData.planets.length > 0 ? (
                      <div className="space-y-4">
                        {houseData.planets.map((planet) => {
                          const effects = PLANET_EFFECTS_IN_HOUSES[planet]?.[houseData.house];

                          return (
                            <div key={planet} className="space-y-3">
                              <h5 className="text-sm font-medium text-cosmic-text">
                                {planet}
                              </h5>

                              {effects ? (
                                <div className="bg-sacred-gold/5 border border-sacred-gold/20 rounded-xl p-4">
                                  <p className="text-sm text-cosmic-text/80 leading-relaxed">
                                    {language === 'hi' ? effects.hi : effects.en}
                                  </p>
                                </div>
                              ) : (
                                <p className="text-sm text-gray-600 italic">
                                  {t('auto.effectsNotAvailableF')}
                                </p>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-600 italic">
                        {t('auto.emptyHouseNoPlanetsP')}
                      </p>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
