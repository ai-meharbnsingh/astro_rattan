import type { PlanetData } from '@/components/InteractiveKundli';

// JHora-style planet colors
export const PLANET_COLORS: Record<string, string> = {
  Sun: '#E65100',
  Moon: '#1565C0',
  Mars: '#C62828',
  Mercury: '#2E7D32',
  Jupiter: '#F9A825',
  Venus: '#E91E63',
  Saturn: '#1565C0',
  Rahu: '#616161',
  Ketu: '#795548',
  Ascendant: '#B8860B',
  Lagna: '#B8860B',
};

// Jaimini Karaka names in order (highest degree to lowest)
const KARAKA_NAMES = ['AK', 'AmK', 'BK', 'MK', 'PiK', 'GnK', 'DK'];

/**
 * Calculate Jaimini Karakas from planet data.
 * Sort 7 planets (Sun through Saturn, exclude Rahu/Ketu) by sign_degree descending.
 * Highest degree = Atmakaraka (AK), next = Amatya (AmK), etc.
 */
export function calculateJaiminiKarakas(planets: PlanetData[]): Record<string, string> {
  const jaiminiPlanets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
  const eligible = planets
    .filter((p) => jaiminiPlanets.includes(p.planet))
    .sort((a, b) => (b.sign_degree || 0) - (a.sign_degree || 0));

  const result: Record<string, string> = {};
  eligible.forEach((p, i) => {
    if (i < KARAKA_NAMES.length) {
      result[p.planet] = KARAKA_NAMES[i];
    }
  });
  return result;
}

/**
 * Get planet color for JHora-style rendering
 */
export function getPlanetColor(planet: string): string {
  return PLANET_COLORS[planet] || '#666666';
}
