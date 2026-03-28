// Shared constants and helpers for Kundli sub-components

// Sign -> Lord mapping
export const SIGN_LORD: Record<string, string> = {
  Aries: 'Mars', Taurus: 'Venus', Gemini: 'Mercury', Cancer: 'Moon',
  Leo: 'Sun', Virgo: 'Mercury', Libra: 'Venus', Scorpio: 'Mars',
  Sagittarius: 'Jupiter', Capricorn: 'Saturn', Aquarius: 'Saturn', Pisces: 'Jupiter',
};

// Sign -> Element
export const SIGN_ELEMENT: Record<string, string> = {
  Aries: 'Fire', Leo: 'Fire', Sagittarius: 'Fire',
  Taurus: 'Earth', Virgo: 'Earth', Capricorn: 'Earth',
  Gemini: 'Air', Libra: 'Air', Aquarius: 'Air',
  Cancer: 'Water', Scorpio: 'Water', Pisces: 'Water',
};

// Sign -> Sign Type
export const SIGN_TYPE: Record<string, string> = {
  Aries: 'Moveable', Cancer: 'Moveable', Libra: 'Moveable', Capricorn: 'Moveable',
  Taurus: 'Fixed', Leo: 'Fixed', Scorpio: 'Fixed', Aquarius: 'Fixed',
  Gemini: 'Dual', Virgo: 'Dual', Sagittarius: 'Dual', Pisces: 'Dual',
};

// Planet nature
export const PLANET_NATURE: Record<string, string> = {
  Sun: 'Malefic', Moon: 'Benefic', Mars: 'Malefic', Mercury: 'Benefic',
  Jupiter: 'Benefic', Venus: 'Benefic', Saturn: 'Malefic', Rahu: 'Malefic', Ketu: 'Malefic',
};

// Planet aspects
export const PLANET_ASPECTS: Record<string, number[]> = {
  Sun: [7], Moon: [7], Mercury: [7], Venus: [7],
  Mars: [4, 7, 8], Jupiter: [5, 7, 9], Saturn: [3, 7, 10],
  Rahu: [5, 7, 9], Ketu: [5, 7, 9],
};

// Dignity calculation
const dignityMap: Record<string, { exalted: string[]; debilitated: string[]; own: string[] }> = {
  Sun: { exalted: ['Aries'], debilitated: ['Libra'], own: ['Leo'] },
  Moon: { exalted: ['Taurus'], debilitated: ['Scorpio'], own: ['Cancer'] },
  Mars: { exalted: ['Capricorn'], debilitated: ['Cancer'], own: ['Aries', 'Scorpio'] },
  Mercury: { exalted: ['Virgo'], debilitated: ['Pisces'], own: ['Gemini', 'Virgo'] },
  Jupiter: { exalted: ['Cancer'], debilitated: ['Capricorn'], own: ['Sagittarius', 'Pisces'] },
  Venus: { exalted: ['Pisces'], debilitated: ['Virgo'], own: ['Taurus', 'Libra'] },
  Saturn: { exalted: ['Libra'], debilitated: ['Aries'], own: ['Capricorn', 'Aquarius'] },
  Rahu: { exalted: ['Gemini', 'Taurus'], debilitated: ['Sagittarius', 'Scorpio'], own: [] },
  Ketu: { exalted: ['Sagittarius', 'Scorpio'], debilitated: ['Gemini', 'Taurus'], own: [] },
};

export function getDignity(planet: string, sign: string, t: (key: string) => string): string {
  const d = dignityMap[planet];
  if (!d) return t('kundli.neutral');
  if (d.exalted.includes(sign)) return t('kundli.exalted');
  if (d.debilitated.includes(sign)) return t('kundli.debilitated');
  if (d.own.includes(sign)) return t('kundli.ownSign');
  return t('kundli.neutral');
}

// House significance — needs t() so we return a factory
export function getHouseSignificance(t: (key: string) => string): Record<number, string> {
  return {
    1: t('kundli.house1'),
    2: t('kundli.house2'),
    3: t('kundli.house3'),
    4: t('kundli.house4'),
    5: t('kundli.house5'),
    6: t('kundli.house6'),
    7: t('kundli.house7'),
    8: t('kundli.house8'),
    9: t('kundli.house9'),
    10: t('kundli.house10'),
    11: t('kundli.house11'),
    12: t('kundli.house12'),
  };
}

// Divisional chart options
export const DIVISIONAL_CHART_OPTIONS = [
  { code: 'D1', name: 'Rashi (D1)' },
  { code: 'D2', name: 'Hora (D2)' },
  { code: 'D3', name: 'Drekkana (D3)' },
  { code: 'D4', name: 'Chaturthamsha (D4)' },
  { code: 'D7', name: 'Saptamsha (D7)' },
  { code: 'D9', name: 'Navamsha (D9)' },
  { code: 'D10', name: 'Dashamsha (D10)' },
  { code: 'D12', name: 'Dwadashamsha (D12)' },
  { code: 'D16', name: 'Shodashamsha (D16)' },
  { code: 'D20', name: 'Vimshamsha (D20)' },
  { code: 'D24', name: 'Chaturvimshamsha (D24)' },
  { code: 'D27', name: 'Bhamsha (D27)' },
  { code: 'D30', name: 'Trimshamsha (D30)' },
  { code: 'D40', name: 'Khavedamsha (D40)' },
  { code: 'D45', name: 'Akshavedamsha (D45)' },
  { code: 'D60', name: 'Shashtiamsha (D60)' },
];
