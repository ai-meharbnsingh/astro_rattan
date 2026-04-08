/**
 * TypeScript interfaces for Kundli API response types.
 *
 * Derived from backend route handlers in app/routes/kundli.py
 * and their corresponding engine modules.
 */

// ── Planet & Chart primitives ──────────────────────────────────

export interface PlanetPosition {
  longitude: number;
  sign: string;
  sign_degree: number;
  nakshatra: string;
  nakshatra_pada: number;
  house: number;
  retrograde: boolean;
  is_combust: boolean;
  is_vargottama: boolean;
  status: string;
}

/** Backend planets dict: keys are planet names (Sun, Moon, etc.) */
export type PlanetsMap = Record<string, PlanetPosition>;

export interface Ascendant {
  longitude: number;
  sign: string;
  sign_degree: number;
}

export interface HouseInfo {
  number: number;
  sign: string;
}

export interface ChartDataResponse {
  planets: PlanetsMap;
  ascendant: Ascendant;
  houses: HouseInfo[];
  placidus_cusps?: Record<string, number>;
}

// ── /api/kundli/generate  (POST 201) ──────────────────────────

export interface KundliResult {
  id: string;
  person_name: string;
  birth_date: string;
  birth_time: string;
  birth_place: string;
  latitude?: number;
  longitude?: number;
  timezone_offset?: number;
  ayanamsa?: string;
  chart_data: ChartDataResponse;
  iogita_analysis?: Record<string, unknown> | null;
  created_at?: string;
}

// ── /api/kundli/{id}/dosha  (POST) ────────────────────────────

export interface MangalDosha {
  has_dosha: boolean;
  severity: string;
  description: string;
  remedies: string[];
}

export interface KaalSarpDosha {
  has_dosha: boolean;
  dosha_type: string;
  description: string;
  affected_planets: string[];
  remedies: string[];
}

export interface SadeSati {
  has_sade_sati: boolean;
  phase: string;
  description: string;
  severity: string;
  remedies: string[];
}

export interface GemstoneRecommendation {
  planet: string;
  reason: string;
  gemstone: string;
  gemstone_hi: string;
  metal: string;
  finger: string;
  day: string;
  priority: 'primary' | 'secondary';
}

export interface DoshaData {
  kundli_id: string;
  person_name: string;
  mangal_dosha: MangalDosha;
  kaal_sarp_dosha: KaalSarpDosha;
  sade_sati: SadeSati;
  gemstone_recommendations: GemstoneRecommendation[];
}

// ── /api/kundli/{id}/dasha  (GET/POST) ────────────────────────

export interface MahadashaPeriod {
  planet: string;
  start_date: string;
  end_date: string;
  years: number;
}

export interface DashaData {
  kundli_id: string;
  person_name: string;
  mahadasha_periods: MahadashaPeriod[];
  current_dasha: string;
  current_antardasha: string;
  error?: string;
}

// ── /api/kundli/{id}/extended-dasha  (POST) ───────────────────

export interface PratyantarPeriod {
  planet: string;
  start: string;
  end: string;
  days: number;
  is_current: boolean;
}

export interface AntardashaPeriod {
  planet: string;
  start: string;
  end: string;
  years: number;
  is_current: boolean;
  pratyantar: PratyantarPeriod[];
}

export interface ExtendedMahadasha {
  planet: string;
  start: string;
  end: string;
  years: number;
  is_current: boolean;
  antardasha: AntardashaPeriod[];
}

export interface ExtendedDashaData {
  kundli_id: string;
  person_name: string;
  mahadasha: ExtendedMahadasha[];
  current_dasha: string;
  current_antardasha: string;
  current_pratyantar: string;
  error?: string;
}

// ── /api/kundli/{id}/ashtakvarga  (POST) ──────────────────────

export interface AshtakvargaPlanetDetail {
  contributors: Record<string, Record<string, number>>;
  totals: Record<string, number>;
}

export interface AshtakvargaData {
  kundli_id: string;
  person_name: string;
  planet_bindus: Record<string, Record<string, number>>;
  sarvashtakvarga: Record<string, number>;
  planet_details: Record<string, AshtakvargaPlanetDetail>;
}

// ── /api/kundli/{id}/shadbala  (POST) ─────────────────────────

export interface ShadbalaEntry {
  sthana: number;
  dig: number;
  kala: number;
  cheshta: number;
  naisargika: number;
  drik: number;
  total: number;
  required: number;
  ratio: number;
  is_strong: boolean;
}

export interface ShadbalaData {
  kundli_id: string;
  person_name: string;
  planets: Record<string, ShadbalaEntry>;
}

// ── /api/kundli/{id}/avakhada  (GET) ──────────────────────────

export interface AvakhadaData {
  kundli_id: string;
  person_name: string;
  ascendant: string;
  ascendant_lord: string;
  rashi: string;
  rashi_lord: string;
  nakshatra: string;
  nakshatra_pada: number;
  yoga: string;
  karana: string;
  yoni: string;
  gana: string;
  nadi: string;
  varna: string;
  naamakshar: string;
  sun_sign: string;
  moon_degree: number;
  sun_degree: number;
  tithi: string;
  tithi_paksha: string;
  tithi_lord: string;
  vaar: string;
  vaar_lord: string;
  paya_nakshatra: string;
  paya_chandra: string;
}

// ── /api/kundli/{id}/yogas-doshas  (POST) ─────────────────────

export interface YogaEntry {
  name: string;
  description: string;
  present: boolean;
  planets_involved?: string[];
}

export interface DoshaEntry {
  name: string;
  description: string;
  present: boolean;
  severity: string;
  remedies: string[];
}

export interface YogaDoshaData {
  kundli_id: string;
  person_name: string;
  yogas: YogaEntry[];
  doshas: DoshaEntry[];
}

// ── /api/kundli/{id}/divisional  (POST) ───────────────────────

export interface DivisionalPlanet {
  planet: string;
  sign: string;
  sign_degree: number;
  house: number;
  nakshatra: string;
  longitude: number;
}

export interface DivisionalHouse {
  number: number;
  sign: string;
}

export interface DivisionalData {
  kundli_id: string;
  person_name: string;
  chart_type: string;
  chart_name: string;
  division: number;
  planet_signs: Record<string, string>;
  planet_positions: DivisionalPlanet[];
  houses: DivisionalHouse[];
}

// ── /api/kundli/{id}/transits  (POST) ─────────────────────────

export interface TransitPlanet {
  planet: string;
  current_sign: string;
  sign_degree: number;
  house: number;
  nakshatra: string;
  is_retrograde: boolean;
  natal_house_from_moon: number;
  effect: string;
  description: string;
}

export interface TransitSadeSati {
  active: boolean;
  phase: string;
  description: string;
}

export interface TransitData {
  transits: TransitPlanet[];
  sade_sati: TransitSadeSati;
  transit_date: string;
  natal_moon_sign: string;
  chart_data?: {
    ascendant?: Ascendant;
    houses?: HouseInfo[];
  };
}

// ── /api/kundli/{id}/sodashvarga  (GET) ───────────────────────

export interface VargaTableRow {
  division: number;
  name: string;
  planets: Record<string, string>;
}

export interface SodashvargaData {
  kundli_id: string;
  person_name: string;
  by_sign: Record<string, Record<number, string[]>>;
  by_planet: Record<string, Record<number, string>>;
  varga_table: VargaTableRow[];
}

// ── /api/kundli/{id}/jaimini  (GET) ───────────────────────────

export interface CharaKaraka {
  planet: string;
  karaka: string;
  degree: number;
  sign: string;
}

export interface SpecialLagna {
  sign: string;
  house: number;
  description_en: string;
  description_hi: string;
  atmakaraka?: string;
}

export interface CharaDashaPeriod {
  sign: string;
  years: number;
  start_date: string;
  end_date: string;
}

export interface CharaDasha {
  periods: CharaDashaPeriod[];
  current_period_index: number;
  total_years: number;
}

export interface InduLagna {
  indu_lagna_sign: string;
  indu_lagna_house: number;
  ninth_lord_lagna: string;
  ninth_lord_moon: string;
  kaksha_sum: number;
  remainder: number;
}

export interface ArgalaEntry {
  type: string;
  from_house: number;
  planets: string[];
  virodha_house: number;
  virodha_planets: string[];
  blocked: boolean;
  status: string;
}

export interface HouseArgala {
  house: number;
  argalas: ArgalaEntry[];
}

export interface JaiminiYoga {
  name: string;
  present: boolean;
  description_en: string;
  description_hi: string;
  planets_involved?: string[];
}

export interface JaiminiLongevity {
  category: string;
  description_en: string;
  description_hi: string;
  lagna_sign: string;
  lagna_modality: string;
  eighth_lord: string;
  eighth_lord_sign: string;
  eighth_modality: string;
  note_en: string;
  note_hi: string;
}

export interface JaiminiData {
  kundli_id: string;
  person_name: string;
  chara_karakas: CharaKaraka[];
  special_lagnas: Record<string, SpecialLagna>;
  jaimini_drishti: { sign_aspects: Record<string, string[]> };
  chara_dasha: CharaDasha;
  indu_lagna: InduLagna;
  argala: { house_argalas: HouseArgala[] };
  jaimini_yogas: JaiminiYoga[];
  longevity: JaiminiLongevity;
}

// ── /api/kundli/{id}/varshphal  (POST) ────────────────────────

export interface MuddaDashaPeriod {
  planet: string;
  start_date: string;
  end_date: string;
  days: number;
}

export interface Muntha {
  sign: string;
  sign_index: number;
  degree: number;
  lord: string;
  house: number;
  favorable: boolean;
}

export interface VarshphalData {
  year: number;
  completed_years: number;
  solar_return: {
    date: string;
    time: string;
    julian_day: number;
  };
  chart_data: ChartDataResponse;
  muntha: Muntha;
  year_lord: string;
  mudda_dasha: MuddaDashaPeriod[];
  current_mudda?: string | null;
}

// ── /api/kundli/{id}/yogini-dasha  (GET) ──────────────────────

export interface YoginiDashaPeriod {
  yogini: string;
  planet: string;
  start: string;
  end: string;
  years: number;
  is_current?: boolean;
}

export interface YoginiData {
  periods: YoginiDashaPeriod[];
  current_yogini?: string;
}

// ── /api/kundli/{id}/upagrahas  (GET) ─────────────────────────

export interface UpagrahaEntry {
  name: string;
  longitude: number;
  sign: string;
  sign_degree: number;
  house?: number;
}

export interface UpagrahasData {
  kundli_id: string;
  person_name: string;
  upagrahas: UpagrahaEntry[];
}

// ── /api/kundli/{id}/aspects  (GET) ───────────────────────────

export interface AspectEntry {
  planet: string;
  aspected_houses: number[];
  aspected_planets: string[];
  aspect_type?: string;
}

export interface AspectsData {
  kundli_id: string;
  person_name: string;
  planet_aspects?: AspectEntry[];
  house_aspects?: Record<string, string[]>;
  [key: string]: unknown;
}

// ── /api/kundli/{id}/western-aspects  (GET) ───────────────────

export interface WesternAspectEntry {
  planet1: string;
  planet2: string;
  aspect: string;
  orb: number;
  exact_degree?: number;
}

export interface WesternAspectsData {
  kundli_id: string;
  person_name: string;
  aspects?: WesternAspectEntry[];
  [key: string]: unknown;
}

// ── /api/kundli/{id}/kp-analysis  (POST) ──────────────────────

export interface KpCuspalEntry {
  house: number;
  cusp_degree: number;
  sign: string;
  sign_lord: string;
  star_lord: string;
  sub_lord: string;
}

export interface KpData {
  kundli_id?: string;
  cusps?: KpCuspalEntry[];
  [key: string]: unknown;
}

// ── /api/kundli/{id}/lifelong-sadesati  (GET) ─────────────────

export interface SadesatiPeriod {
  start_year: number;
  end_year: number;
  phase: string;
  saturn_sign: string;
}

export interface SadesatiData {
  kundli_id: string;
  person_name: string;
  moon_sign: string;
  periods: SadesatiPeriod[];
  [key: string]: unknown;
}

// ── /api/kundli/list  (GET) ───────────────────────────────────

export interface KundliListItem {
  id: string;
  person_name: string;
  birth_date: string;
  birth_time: string;
  birth_place: string;
  created_at: string;
}
