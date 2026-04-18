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


// ─────────────────────────────────────────────────────────────
// LK-context planet normalization (Sprint C-1)
// ─────────────────────────────────────────────────────────────
//
// Lal Kitab tabs (Kundli / Teva / Varshphal) each needed the same
// transform from raw chart_data.planets to PlanetData[]:
//   - strip Vedic-only status tokens (Combust / Sandhi) so LK
//     surfaces never display Vedic concepts that don't apply;
//   - force `is_combust: false` for the same reason.
//
// Each tab previously duplicated this logic. `toLkPlanetData` /
// `toLkPlanetList` is the single source of truth — call once, get
// the LK-safe shape.
import { lkStatusString } from './safe-render';

/** Loose LK-safe PlanetData shape — structurally compatible with
 *  `@/components/InteractiveKundli`'s PlanetData interface. */
export interface LkPlanetData {
  planet: string;
  sign: string;
  house: number;
  nakshatra: string;
  sign_degree: number;
  status: string;
  is_retrograde: boolean;
  is_combust: boolean;      // always false in LK context
  is_vargottama: boolean;
}

/** Normalise one raw planet object from chart_data. */
export function toLkPlanetData(raw: any, planetName?: string): LkPlanetData {
  const r = raw || {};
  return {
    planet: typeof r.planet === 'string' ? r.planet : (planetName ?? ''),
    sign: r.sign || 'Unknown',
    house: typeof r.house === 'number' ? r.house : 0,
    nakshatra: r.nakshatra || '',
    sign_degree: typeof r.sign_degree === 'number' ? r.sign_degree : 0,
    status: lkStatusString(r.status || ''),       // strip Combust / Sandhi
    is_retrograde: Boolean(r.retrograde || r.is_retrograde),
    is_combust: false,                             // hard-enforced for LK
    is_vargottama: Boolean(r.vargottama || r.is_vargottama),
  };
}

/** Normalise a raw `chart_data.planets` (list or name→data record)
 *  into a consistent LK-safe PlanetData[] array. */
export function toLkPlanetList(planetsRaw: any): LkPlanetData[] {
  if (!planetsRaw) return [];
  if (Array.isArray(planetsRaw)) {
    return planetsRaw.map((p: any) => toLkPlanetData(p));
  }
  if (typeof planetsRaw === 'object') {
    return Object.entries(planetsRaw).map(
      ([name, data]: [string, any]) => toLkPlanetData(data, name),
    );
  }
  return [];
}

