import { useState, useMemo, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import {
  Calendar,
  ArrowRight,
  Sparkles,
  Heart,
  Gift,
  Home,
  Zap,
} from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import type { LalKitabChartData } from './lalkitab-data';
import { PLANETS, REMEDIES, PLANET_EFFECTS_IN_HOUSES } from './lalkitab-data';

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

interface Props {
  chartData: LalKitabChartData;
  birthDate: string;
  apiResult?: any;
}

const typeIcons = {
  feeding: Heart,
  donation: Gift,
  household: Home,
  action: Zap,
} as const;

function getPlanetLabel(key: string, language: string): string {
  const planet = PLANETS.find((p) => p.key === key);
  if (!planet) return key;
  return language === 'hi' ? planet.hi : planet.en;
}

/** Build the current year and +/- 5 years range. */
function getYearRange(): number[] {
  const current = new Date().getFullYear();
  const years: number[] = [];
  for (let y = current - 5; y <= current + 5; y++) {
    years.push(y);
  }
  return years;
}

export default function LalKitabVarshphalTab({ chartData, birthDate, apiResult }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const currentYear = new Date().getFullYear();
  const [selectedYear, setSelectedYear] = useState<number>(currentYear);
  const yearRange = useMemo(() => getYearRange(), []);
  const birthYear = new Date(birthDate).getFullYear();

  // Compute annual planet positions: shift each planet by (selectedYear - birthYear) % 12 houses
  const annualPositions = useMemo(() => {
    const shift = ((selectedYear - birthYear) % 12 + 12) % 12; // always positive
    const positions: Record<string, number> = {};
    for (const planet of PLANETS) {
      const birthHouse = chartData.planetPositions[planet.key];
      if (birthHouse == null) continue;
      // Shift forward, wrap around 1-12
      positions[planet.key] = ((birthHouse - 1 + shift) % 12) + 1;
    }
    return positions;
  }, [selectedYear, birthYear, chartData.planetPositions]);

  // Build house-to-planets maps for mini charts
  const birthHousePlanets = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (let i = 1; i <= 12; i++) map[i] = [];
    for (const planet of PLANETS) {
      const h = chartData.planetPositions[planet.key];
      if (h != null) map[h].push(planet.key);
    }
    return map;
  }, [chartData.planetPositions]);

  const annualHousePlanets = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (let i = 1; i <= 12; i++) map[i] = [];
    for (const planet of PLANETS) {
      const h = annualPositions[planet.key];
      if (h != null) map[h].push(planet.key);
    }
    return map;
  }, [annualPositions]);

  // Planet comparison: birth house vs annual house
  const planetComparison = useMemo(() => {
    return PLANETS.map((planet) => {
      const birthHouse = chartData.planetPositions[planet.key] ?? null;
      const annualHouse = annualPositions[planet.key] ?? null;
      const changed = birthHouse !== annualHouse;
      const effects = annualHouse != null ? PLANET_EFFECTS_IN_HOUSES[planet.key]?.[annualHouse] : null;
      return { planet, birthHouse, annualHouse, changed, effects };
    }).filter((c) => c.birthHouse != null);
  }, [chartData.planetPositions, annualPositions]);

  // Yearly remedies — based on annual positions, pick 3-5 relevant ones
  const yearlyRemedies = useMemo(() => {
    const collected: { planet: string; house: number; remedy: any }[] = [];

    for (const planet of PLANETS) {
      const annualHouse = annualPositions[planet.key];
      if (annualHouse == null) continue;
      const planetRemedies = REMEDIES[planet.key]?.[annualHouse];
      if (!planetRemedies) continue;

      for (const r of planetRemedies) {
        collected.push({ planet: planet.key, house: annualHouse, remedy: r });
      }
    }

    // Prioritize urgent, then daily
    const priority: Record<string, number> = { urgent: 0, daily: 1, weekly: 2, general: 3 };
    collected.sort(
      (a, b) => (priority[a.remedy.category] ?? 9) - (priority[b.remedy.category] ?? 9),
    );

    return collected.slice(0, 5);
  }, [annualPositions]);

  // Build InteractiveKundli ChartData from house-to-planets map
  const buildChartData = useCallback((housePlanets: Record<number, string[]>): ChartData | null => {
    // Use API result for ascendant sign, or default to Aries (house 1)
    const asc = apiResult?.chart_data?.ascendant;
    const ascSign = asc?.sign || 'Aries';
    const ascIdx = ZODIAC_SIGNS.indexOf(ascSign);

    const houses = Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ZODIAC_SIGNS[(ascIdx + i) % 12],
    }));

    const planets: PlanetData[] = [];
    for (let h = 1; h <= 12; h++) {
      const pList = housePlanets[h] ?? [];
      for (const pKey of pList) {
        planets.push({
          planet: pKey,
          sign: houses[h - 1].sign,
          house: h,
          nakshatra: '',
          sign_degree: 15,
          status: '',
        });
      }
    }

    return { planets, houses, ascendant: asc ? { longitude: asc.longitude || 0, sign: ascSign } : undefined };
  }, [apiResult]);

  const birthChartData = useMemo(() => buildChartData(birthHousePlanets), [birthHousePlanets, buildChartData]);
  const annualChartData = useMemo(() => buildChartData(annualHousePlanets), [annualHousePlanets, buildChartData]);

  return (
    <div className="space-y-8">
      {/* ─── Header ─── */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-sans font-bold text-sacred-gold flex items-center justify-center gap-2">
          <Calendar className="w-6 h-6" />
          {t('lk.varshphal.title')}
        </h2>
        <p className="text-sm text-gray-600">{t('lk.varshphal.desc')}</p>
      </div>

      {/* ─── Year Selector ─── */}
      <div className="flex items-center justify-center gap-3">
        <label className="text-sm font-medium text-sacred-gold">
          {t('lk.varshphal.selectYear')}
        </label>
        <select
          value={selectedYear}
          onChange={(e) => setSelectedYear(Number(e.target.value))}
          className="rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text px-4 py-3 focus:outline-none focus:border-sacred-gold/50 transition-colors"
        >
          {yearRange.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      {/* ─── Side-by-side Comparison Charts (Diamond Kundli) ─── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
          <h4 className="font-sans text-base font-semibold text-sacred-gold mb-3 text-center">
            {t('lk.varshphal.birthChart')}
          </h4>
          {birthChartData ? (
            <InteractiveKundli chartData={birthChartData} compact />
          ) : (
            <p className="text-center text-sm text-gray-500 py-8">{isHi ? 'चार्ट उपलब्ध नहीं' : 'Chart not available'}</p>
          )}
        </div>
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
          <h4 className="font-sans text-base font-semibold text-sacred-gold mb-3 text-center">
            {t('lk.varshphal.annualChart')} — {selectedYear}
          </h4>
          {annualChartData ? (
            <InteractiveKundli chartData={annualChartData} compact />
          ) : (
            <p className="text-center text-sm text-gray-500 py-8">{isHi ? 'चार्ट उपलब्ध नहीं' : 'Chart not available'}</p>
          )}
        </div>
      </div>

      {/* ─── Yearly Predictions ─── */}
      <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20">
        <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4">
          {isHi ? 'वार्षिक फलादेश' : 'Yearly Predictions'} — {selectedYear}
        </h3>

        <div className="space-y-3">
          {planetComparison.map(({ planet, birthHouse, annualHouse, changed, effects }) => (
            <div
              key={planet.key}
              className={`rounded-xl p-4 border transition-all ${
                changed
                  ? 'bg-sacred-gold/10 border-sacred-gold/30'
                  : 'bg-cosmic-card/30 border-sacred-gold/10'
              }`}
            >
              {/* Planet row */}
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-cosmic-text">
                  {getPlanetLabel(planet.key, language)}
                </span>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <span>
                    {isHi ? 'भाव' : 'H'}{birthHouse}
                  </span>
                  <ArrowRight className="w-4 h-4 text-sacred-gold/60" />
                  <span
                    className={changed ? 'font-semibold text-sacred-gold' : ''}
                  >
                    {isHi ? 'भाव' : 'H'}{annualHouse}
                  </span>
                  {changed && (
                    <span className="px-2 py-0.5 rounded-full text-sm font-semibold bg-sacred-gold/20 text-sacred-gold">
                      {isHi ? 'बदलाव' : 'Changed'}
                    </span>
                  )}
                </div>
              </div>

              {/* Effects of annual position */}
              {effects && (
                <div className="mt-2 bg-sacred-gold/5 border border-sacred-gold/15 rounded-lg p-3">
                  <p className="text-sm font-semibold text-sacred-gold uppercase tracking-wide mb-1">
                    {isHi ? 'फल' : 'Effect'}
                  </p>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {isHi ? effects.hi : effects.en}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* ─── Yearly Remedies ─── */}
      <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20">
        <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('lk.varshphal.yearlyRemedies')}
        </h3>

        {yearlyRemedies.length === 0 ? (
          <p className="text-sm text-gray-600 italic text-center py-4">
            {isHi ? 'इस वर्ष के लिए कोई विशेष उपाय नहीं' : 'No specific remedies for this year'}
          </p>
        ) : (
          <div className="space-y-3">
            {yearlyRemedies.map((item, idx) => {
              const TypeIcon =
                typeIcons[item.remedy.type as keyof typeof typeIcons] ?? Sparkles;
              const remedyText = isHi ? item.remedy.hi : item.remedy.en;
              const planetLabel = getPlanetLabel(item.planet, language);

              return (
                <div
                  key={idx}
                  className="flex items-start gap-3 p-4 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10"
                >
                  <TypeIcon className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                  <div className="min-w-0">
                    <p className="text-sm text-sacred-gold font-medium mb-0.5">
                      {planetLabel} — {isHi ? 'भाव' : 'House'} {item.house}
                    </p>
                    <p className="text-sm text-cosmic-text/80 leading-snug">
                      {remedyText}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
