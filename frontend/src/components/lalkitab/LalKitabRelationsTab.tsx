import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import {
  PLANETS,
  PLANET_FRIENDS,
  PLANET_ENEMIES,
  PAKKA_GHAR,
} from './lalkitab-data';
import { Users, Eye, AlertTriangle, CheckCircle } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}

interface Conjunction {
  house: number;
  planets: string[];
}

interface AspectEntry {
  planet: string;
  fromHouse: number;
  aspectHouses: number[];
}

// Lal Kitab special aspects (additional aspects beyond the universal 7th)
const SPECIAL_ASPECTS: Record<string, number[]> = {
  Mars: [4, 8],
  Jupiter: [5, 9],
  Saturn: [3, 10],
  Rahu: [5, 9],
};

export default function LalKitabRelationsTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const getPlanetLabel = (key: string) => {
    const planet = PLANETS.find((p) => p.key === key);
    if (!planet) return key;
    return isHi ? planet.hi : planet.en;
  };

  // Find conjunctions: planets sharing the same house
  const conjunctions = useMemo<Conjunction[]>(() => {
    const houseMap: Record<number, string[]> = {};
    for (const [planet, house] of Object.entries(chartData.planetPositions)) {
      if (house == null) continue;
      if (!houseMap[house]) houseMap[house] = [];
      houseMap[house].push(planet);
    }
    return Object.entries(houseMap)
      .filter(([, planets]) => planets.length >= 2)
      .map(([house, planets]) => ({ house: Number(house), planets }));
  }, [chartData.planetPositions]);

  // Calculate aspects for each planet
  const aspects = useMemo<AspectEntry[]>(() => {
    const entries: AspectEntry[] = [];
    for (const planet of PLANETS) {
      const fromHouse = chartData.planetPositions[planet.key];
      if (fromHouse == null) continue;

      const aspectHouses: number[] = [];

      // Universal 7th house aspect
      aspectHouses.push(((fromHouse - 1 + 6) % 12) + 1);

      // Special aspects
      const special = SPECIAL_ASPECTS[planet.key];
      if (special) {
        for (const offset of special) {
          aspectHouses.push(((fromHouse - 1 + offset - 1) % 12) + 1);
        }
      }

      entries.push({ planet: planet.key, fromHouse, aspectHouses });
    }
    return entries;
  }, [chartData.planetPositions]);

  // Check friendship/enmity
  const areFriends = (p1: string, p2: string) =>
    PLANET_FRIENDS[p1]?.includes(p2) ?? false;

  const areEnemies = (p1: string, p2: string) =>
    PLANET_ENEMIES[p1]?.includes(p2) ?? false;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="font-sans text-2xl text-sacred-gold flex items-center gap-2">
          <Users className="w-6 h-6" />
          {t('lk.relations.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.relations.desc')}</p>
      </div>

      {/* Conjunctions (Yuti) */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4">
          {t('lk.relations.conjunction')} ({isHi ? 'युति' : 'Yuti'})
        </h3>

        {conjunctions.length === 0 ? (
          <p className="text-sm text-cosmic-text/70 italic">
            {isHi ? 'कोई युति नहीं पाई गई।' : 'No conjunctions found.'}
          </p>
        ) : (
          <div className="space-y-4">
            {conjunctions.map((conj) => {
              // Check for clashes in this conjunction
              const clashes: [string, string][] = [];
              const friendships: [string, string][] = [];

              for (let i = 0; i < conj.planets.length; i++) {
                for (let j = i + 1; j < conj.planets.length; j++) {
                  const p1 = conj.planets[i];
                  const p2 = conj.planets[j];
                  if (areEnemies(p1, p2) || areEnemies(p2, p1)) {
                    clashes.push([p1, p2]);
                  } else if (areFriends(p1, p2) || areFriends(p2, p1)) {
                    friendships.push([p1, p2]);
                  }
                }
              }

              const hasClash = clashes.length > 0;

              return (
                <div
                  key={conj.house}
                  className={`rounded-xl p-5 border transition-all ${
                    hasClash
                      ? 'border-red-300/30 bg-red-500/5'
                      : 'border-blue-500/20 bg-blue-500/5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <span className="text-sm text-cosmic-text/70">
                        {isHi ? 'भाव' : 'House'} {conj.house}
                      </span>
                      <div className="flex items-center gap-2 mt-1 flex-wrap">
                        {conj.planets.map((planet) => (
                          <span
                            key={planet}
                            className="px-2.5 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium"
                          >
                            {getPlanetLabel(planet)}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Clash / no-clash indicators */}
                  {clashes.map(([p1, p2]) => (
                    <div
                      key={`${p1}-${p2}`}
                      className="flex items-center gap-2 mt-2 text-sm text-red-500"
                    >
                      <AlertTriangle className="w-4 h-4 shrink-0" />
                      <span>
                        {t('lk.relations.clash')}: {getPlanetLabel(p1)} &{' '}
                        {getPlanetLabel(p2)}
                      </span>
                    </div>
                  ))}

                  {friendships.map(([p1, p2]) => (
                    <div
                      key={`${p1}-${p2}`}
                      className="flex items-center gap-2 mt-2 text-sm text-green-500"
                    >
                      <CheckCircle className="w-4 h-4 shrink-0" />
                      <span>
                        {t('lk.relations.noClash')}: {getPlanetLabel(p1)} &{' '}
                        {getPlanetLabel(p2)}
                      </span>
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Separator */}
      <div className="border-t border-sacred-gold/10" />

      {/* Aspects (Drishti) */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4 flex items-center gap-2">
          <Eye className="w-5 h-5" />
          {isHi ? 'दृष्टि (Aspects)' : 'Aspects (Drishti)'}
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b border-sacred-gold/10">
                <th className="text-left py-2 px-3 text-sacred-gold/70 font-sans font-medium">
                  {isHi ? 'ग्रह' : 'Planet'}
                </th>
                <th className="text-left py-2 px-3 text-sacred-gold/70 font-sans font-medium">
                  {isHi ? 'स्थित भाव' : 'In House'}
                </th>
                <th className="text-left py-2 px-3 text-sacred-gold/70 font-sans font-medium">
                  {isHi ? 'दृष्टि भाव' : 'Aspects Houses'}
                </th>
              </tr>
            </thead>
            <tbody>
              {aspects.map((entry) => (
                <tr
                  key={entry.planet}
                  className="border-b border-sacred-gold/10 last:border-b-0"
                >
                  <td className="py-2.5 px-3 text-cosmic-text font-medium">
                    {getPlanetLabel(entry.planet)}
                  </td>
                  <td className="py-2.5 px-3 text-cosmic-text/70">
                    {entry.fromHouse}
                  </td>
                  <td className="py-2.5 px-3">
                    <div className="flex gap-1.5 flex-wrap">
                      {entry.aspectHouses.map((h) => (
                        <span
                          key={h}
                          className="px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold text-sm font-medium"
                        >
                          {h}
                        </span>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Separator */}
      <div className="border-t border-sacred-gold/10" />

      {/* Clash Detection Summary */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4">
          {isHi ? 'टकराव विश्लेषण' : 'Clash Analysis'}
        </h3>

        {conjunctions.length === 0 ? (
          <div className="flex items-center gap-2 text-sm text-green-500">
            <CheckCircle className="w-5 h-5" />
            <span>
              {isHi
                ? 'कोई ग्रह युति नहीं, टकराव नहीं।'
                : 'No planetary conjunctions, no clashes.'}
            </span>
          </div>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {conjunctions.map((conj) => {
              const hasClash = conj.planets.some((p1) =>
                conj.planets.some(
                  (p2) => p1 !== p2 && (areEnemies(p1, p2) || areEnemies(p2, p1))
                )
              );

              return (
                <div
                  key={conj.house}
                  className={`rounded-xl p-4 border ${
                    hasClash
                      ? 'border-red-300/30 bg-red-500/5'
                      : 'border-green-300/30 bg-green-500/5'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {hasClash ? (
                      <AlertTriangle className="w-5 h-5 text-red-500 shrink-0" />
                    ) : (
                      <CheckCircle className="w-5 h-5 text-green-500 shrink-0" />
                    )}
                    <div>
                      <p className="text-sm font-medium text-cosmic-text">
                        {isHi ? 'भाव' : 'House'} {conj.house}:{' '}
                        {conj.planets.map(getPlanetLabel).join(', ')}
                      </p>
                      <p
                        className={`text-sm mt-0.5 ${
                          hasClash ? 'text-red-500' : 'text-green-500'
                        }`}
                      >
                        {hasClash
                          ? t('lk.relations.clash')
                          : t('lk.relations.noClash')}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
