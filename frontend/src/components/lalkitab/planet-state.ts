/**
 * planet-state.ts — P1.1 Modified Analytical Tewa.
 *
 * Classifies each planet into ONE dominant LK state so the Tewa chart
 * can render a single colour per planet. Precedence (highest first):
 *
 *   1. ANDHE     — Blind (LK 2.12, 4.14). Most severe — affects remedies.
 *   2. MASNUI    — Artificial planet, part of a Masnui pair.
 *   3. SOYE      — Sleeping (reduced expression).
 *   4. KAYAM     — Fixed (locked in its significations).
 *   5. JAGE      — Awake (fully expressive). Default positive state.
 *   6. NORMAL    — No special LK state; renders with default planet colour.
 *
 * The classifier is deliberately declarative — it reads the shape of
 * the `/api/lalkitab/advanced/{id}` response and produces a
 * `Record<planetName, PlanetStateTag>` map that can be passed to any
 * chart renderer without coupling to engine internals.
 */

export type LKPlanetState =
  | 'andhe'
  | 'masnui'
  | 'soye'
  | 'kayam'
  | 'jage'
  | 'normal';

export interface PlanetStateTag {
  state: LKPlanetState;
  /** Tailwind text class for the planet letter/abbreviation on the chart. */
  textClass: string;
  /** Tailwind background class for the planet badge / chip. */
  bgClass: string;
  /** Tailwind border class for the planet badge / chip. */
  borderClass: string;
  /** CSS hex colour — used by SVG renderers that don't accept classes. */
  hexColour: string;
  /** Bilingual label for tooltips / legend. */
  labelEn: string;
  labelHi: string;
  /** One-line bilingual explanation of why this state applies. */
  descEn: string;
  descHi: string;
}

/**
 * Colour palette. Chosen to harmonise with existing LK tab styling:
 *   - andhe  → red     (danger — remedy risk)
 *   - masnui → amber   (caution — not real, synthetic)
 *   - soye   → slate   (muted — dormant expression)
 *   - kayam  → emerald (locked — structurally fixed)
 *   - jage   → sacred-gold (flourishing — native LK positive)
 *   - normal → inherit (no special state)
 */
const PALETTE: Record<LKPlanetState, Omit<PlanetStateTag, 'state' | 'labelEn' | 'labelHi' | 'descEn' | 'descHi'>> = {
  andhe: {
    textClass: 'text-red-700',
    bgClass: 'bg-red-500/15',
    borderClass: 'border-red-500/60',
    hexColour: '#DC2626',
  },
  masnui: {
    textClass: 'text-amber-700',
    bgClass: 'bg-amber-400/15',
    borderClass: 'border-amber-500/60',
    hexColour: '#D97706',
  },
  soye: {
    textClass: 'text-slate-600',
    bgClass: 'bg-slate-300/30',
    borderClass: 'border-slate-400/60',
    hexColour: '#64748B',
  },
  kayam: {
    textClass: 'text-emerald-700',
    bgClass: 'bg-emerald-400/15',
    borderClass: 'border-emerald-500/50',
    hexColour: '#047857',
  },
  jage: {
    textClass: 'text-sacred-gold-dark',
    bgClass: 'bg-sacred-gold/15',
    borderClass: 'border-sacred-gold/60',
    hexColour: '#B8860B',
  },
  normal: {
    textClass: 'text-foreground',
    bgClass: 'bg-transparent',
    borderClass: 'border-transparent',
    hexColour: '#1F2937',
  },
};

const LABELS: Record<LKPlanetState, { en: string; hi: string; descEn: string; descHi: string }> = {
  andhe: {
    en: 'Blind',
    hi: 'अंधा',
    descEn: 'Blind planet (Andhe Grah) — cannot deliver results; remedies near it can backfire (LK 2.12 / 4.14).',
    descHi: 'अंधा ग्रह — फल देने में असमर्थ; पास के उपाय उलटा असर कर सकते हैं (लाल किताब 2.12 / 4.14)।',
  },
  masnui: {
    en: 'Artificial',
    hi: 'मसनुई',
    descEn: 'Part of a Masnui pair — forms an artificial synthetic planet; reading is indirect.',
    descHi: 'मसनुई जोड़ी का भाग — कृत्रिम ग्रह बनाता है; फल प्रत्यक्ष नहीं।',
  },
  soye: {
    en: 'Sleeping',
    hi: 'सोया',
    descEn: 'Sleeping planet (Soye Grah) — significations dormant; waits for a waking trigger.',
    descHi: 'सोया ग्रह — फल सुप्त; जागरण ट्रिगर की प्रतीक्षा।',
  },
  kayam: {
    en: 'Fixed',
    hi: 'कायम',
    descEn: 'Fixed planet (Kayam Grah) — entrenched in its house; resistant to remedy or transit shift.',
    descHi: 'कायम ग्रह — भाव में स्थिर; उपाय या गोचर से शीघ्र हिलता नहीं।',
  },
  jage: {
    en: 'Awake',
    hi: 'जागा',
    descEn: 'Awake planet (Jage Grah) — fully expressive; delivers its significations directly.',
    descHi: 'जागा ग्रह — पूर्ण अभिव्यक्ति; अपने फल सीधे देता है।',
  },
  normal: {
    en: 'Normal',
    hi: 'सामान्य',
    descEn: 'No special LK state — native expression.',
    descHi: 'कोई विशेष लाल किताब अवस्था नहीं — सहज अभिव्यक्ति।',
  },
};

function makeTag(state: LKPlanetState): PlanetStateTag {
  const p = PALETTE[state];
  const l = LABELS[state];
  return { state, ...p, labelEn: l.en, labelHi: l.hi, descEn: l.descEn, descHi: l.descHi };
}

/**
 * Shape of the relevant portions of `/api/lalkitab/advanced/{id}`.
 * Only the fields the classifier consults. All fields optional — the
 * classifier tolerates a partial response and falls back to 'normal'.
 */
export interface AdvancedPayloadLite {
  andhe?: {
    per_planet?: Record<string, { is_blind?: boolean }>;
    blind_planets?: string[];
  };
  masnui_planets?: {
    masnui_planets?: Array<{ formed_by?: string[] }>;
  };
  sleeping?: {
    sleeping_planets?: string[];
    per_planet?: Record<string, unknown>;
  };
  kayam?: string[];
  jage?: string[];
}

/**
 * Canonical 9-planet list in the order LK charts expect.
 */
export const LK_PLANETS = [
  'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter',
  'Venus', 'Saturn', 'Rahu', 'Ketu',
] as const;

/**
 * Return one PlanetStateTag per planet — the dominant state after
 * precedence resolution. Always returns all 9 LK planets even if some
 * are absent from the payload (those get `normal`).
 */
export function classifyPlanetStates(
  advanced: AdvancedPayloadLite | null | undefined,
): Record<string, PlanetStateTag> {
  const result: Record<string, PlanetStateTag> = {};

  const blindSet = new Set<string>();
  const masnuiSet = new Set<string>();
  const soyeSet = new Set<string>();
  const kayamSet = new Set<string>();
  const jageSet = new Set<string>();

  if (advanced) {
    // Andhe — per_planet dict (richer) OR blind_planets list fallback.
    const perPlanet = advanced.andhe?.per_planet ?? {};
    for (const [name, info] of Object.entries(perPlanet)) {
      if (info && (info as { is_blind?: boolean }).is_blind) blindSet.add(name);
    }
    for (const name of advanced.andhe?.blind_planets ?? []) blindSet.add(name);

    // Masnui — every planet in any formed_by list.
    for (const m of advanced.masnui_planets?.masnui_planets ?? []) {
      for (const p of m.formed_by ?? []) masnuiSet.add(p);
    }

    // Soye — sleeping_planets list.
    for (const name of advanced.sleeping?.sleeping_planets ?? []) soyeSet.add(name);

    // Kayam — list of planet names.
    for (const name of advanced.kayam ?? []) kayamSet.add(name);

    // Jage — explicit list if backend emits one; otherwise we infer later.
    for (const name of advanced.jage ?? []) jageSet.add(name);
  }

  for (const planet of LK_PLANETS) {
    let state: LKPlanetState = 'normal';
    if (blindSet.has(planet)) state = 'andhe';
    else if (masnuiSet.has(planet)) state = 'masnui';
    else if (soyeSet.has(planet)) state = 'soye';
    else if (kayamSet.has(planet)) state = 'kayam';
    else if (jageSet.has(planet)) state = 'jage';
    result[planet] = makeTag(state);
  }
  return result;
}

/**
 * Convenience: all 6 states as an ordered array for rendering a legend.
 */
export function legendEntries(): PlanetStateTag[] {
  return (Object.keys(PALETTE) as LKPlanetState[])
    .filter((s) => s !== 'normal')
    .map(makeTag);
}
