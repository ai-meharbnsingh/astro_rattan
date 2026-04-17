// Lal Kitab frontend core helpers (STRICT MODE)
//
// This file intentionally contains ONLY:
// - Minimal types
// - Pure extraction helpers from backend kundli payloads
//
// It must NOT contain interpretation tables, remedies text, scoring rules,
// or any domain "prediction" logic. Those must come from backend APIs.

export const LK_PLANETS = [
  'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu',
] as const;

export type LKPlanet = (typeof LK_PLANETS)[number];

export interface LalKitabHouseLite {
  house: number;
  planets: LKPlanet[];
}

export interface LalKitabChartLite {
  planetPositions: Record<LKPlanet, number>;      // 1..12, 0 when unknown
  planetLongitudes: Record<LKPlanet, number>;     // NaN when unknown
  houses: LalKitabHouseLite[];                    // occupancy only (no strength)
  isIncomplete: boolean;
  missingPlanets: LKPlanet[];
}

function asNumber(v: any): number | null {
  if (typeof v === 'number' && Number.isFinite(v)) return v;
  if (typeof v === 'string' && v.trim()) {
    const n = Number(v);
    if (Number.isFinite(n)) return n;
  }
  return null;
}

export function buildLalKitabChartLite(apiData: any): LalKitabChartLite {
  const planetPositions = Object.fromEntries(LK_PLANETS.map((p) => [p, 0])) as Record<LKPlanet, number>;
  const planetLongitudes = Object.fromEntries(LK_PLANETS.map((p) => [p, Number.NaN])) as Record<LKPlanet, number>;
  const missingPlanets: LKPlanet[] = [];

  const chartPlanets = apiData?.chart_data?.planets || apiData?.planets || {};

  for (const p of LK_PLANETS) {
    const info = chartPlanets?.[p];
    if (!info || typeof info !== 'object') {
      missingPlanets.push(p);
      continue;
    }
    const houseRaw = asNumber((info as any).house ?? (info as any).House);
    const lonRaw = asNumber((info as any).longitude ?? (info as any).degree);
    const house = houseRaw != null ? Math.trunc(houseRaw) : null;
    if (house != null && house >= 1 && house <= 12) {
      planetPositions[p] = house;
    } else {
      // If house is not available, do NOT fabricate.
      missingPlanets.push(p);
    }
    if (lonRaw != null) {
      planetLongitudes[p] = lonRaw;
    }
  }

  const houses: LalKitabHouseLite[] = Array.from({ length: 12 }, (_, i) => {
    const h = i + 1;
    const planetsIn = LK_PLANETS.filter((p) => planetPositions[p] === h);
    return { house: h, planets: planetsIn as LKPlanet[] };
  });

  return {
    planetPositions,
    planetLongitudes,
    houses,
    isIncomplete: missingPlanets.length > 0,
    missingPlanets,
  };
}

