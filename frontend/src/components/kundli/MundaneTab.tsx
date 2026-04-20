import { useState, useEffect, useCallback, useMemo } from 'react';
import { Loader2, ChevronDown, ChevronLeft, ChevronRight, AlertTriangle, TrendingUp, TrendingDown, Minus, Shield, Globe2, Building2, Landmark, Moon, Sun } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import type { Language } from '@/lib/i18n';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';

/* ────────────────────────────── Props ────────────────────────────── */

interface MundaneTabProps {
  language: string;
}

/* ────────────────────────────── Types ────────────────────────────── */

interface CountryOption {
  code: string;
  name: string;
  name_hi?: string;
  flag?: string;
}

interface IndicatorCard {
  label: string;
  label_hi: string;
  value: string;
  value_hi?: string;
  status: 'positive' | 'negative' | 'neutral';
}

interface PlanetPosition {
  planet: string;
  sign: string;
  house: number;
  degree: string;
  nakshatra?: string;
  retrograde?: boolean;
}

interface TransitImpact {
  planet: string;
  sign?: string;
  current_sign: string;
  sign_degree?: number;
  house: number;
  impact: string;
  impact_hi?: string;
  type: 'benefic' | 'malefic' | 'neutral';
  retrograde?: boolean;
}

interface HouseAnalysis {
  house: number;
  meaning: string;
  meaning_hi?: string;
  condition: string;
  condition_hi?: string;
  transiting_planets: string[];
  status: 'positive' | 'negative' | 'neutral';
}

interface RiskIndicator {
  title: string;
  title_hi?: string;
  description: string;
  description_hi?: string;
  severity: 'high' | 'medium' | 'low';
}

interface EclipseEntry {
  date: string;
  type: string;
  type_hi?: string;
  solar_lunar: string;
  affected_house: number;
  impact: string;
  impact_hi?: string;
}

interface IngressEntry {
  sign: string;
  date: string;
  theme: string;
  theme_hi?: string;
}

interface AnalysisData {
  country_name: string;
  country_name_hi?: string;
  independence_date?: string;
  independence_time?: string;
  independence_place?: string;
  indicators: IndicatorCard[];
  birth_chart: PlanetPosition[];
  birth_chart_ascendant?: { longitude: number; sign: string; sign_degree?: number };
  birth_chart_houses?: { number: number; sign: string }[];
  transits: TransitImpact[];
  houses: HouseAnalysis[];
  risks: RiskIndicator[];
  economic_analysis: {
    trend: 'growth' | 'pressure' | 'neutral';
    trend_hi?: string;
    description: string;
    description_hi?: string;
  };
  political_analysis: {
    stability: 'stable' | 'unstable' | 'pressured';
    stability_hi?: string;
    description: string;
    description_hi?: string;
  };
}

/* ────────────────────────────── i18n helpers ────────────────────────────── */

const T = {
  mundaneAstrology: (l: string) => l === 'hi' ? 'देशीय ज्योतिष' : 'Mundane Astrology',
  country: (l: string) => l === 'hi' ? 'देश' : 'Country',
  selectCountry: (l: string) => l === 'hi' ? 'देश चुनें' : 'Select Country',
  nationalMood: (l: string) => l === 'hi' ? 'राष्ट्रीय मनोदशा' : 'National Mood',
  govStability: (l: string) => l === 'hi' ? 'सरकार स्थिरता' : 'Government Stability',
  economyTrend: (l: string) => l === 'hi' ? 'अर्थव्यवस्था रुझान' : 'Economy Trend',
  riskLevel: (l: string) => l === 'hi' ? 'जोखिम स्तर' : 'Risk Level',
  countryBirthChart: (l: string) => l === 'hi' ? 'देश की जन्म कुंडली' : 'Country Birth Chart',
  currentTransits: (l: string) => l === 'hi' ? 'वर्तमान गोचर प्रभाव' : 'Current Transits Impact',
  houseAnalysis: (l: string) => l === 'hi' ? 'भाव विश्लेषण' : 'House Analysis',
  conflictIndicators: (l: string) => l === 'hi' ? 'संघर्ष संकेतक' : 'Conflict & Risk Indicators',
  economicAnalysis: (l: string) => l === 'hi' ? 'आर्थिक विश्लेषण' : 'Economic Analysis',
  politicalAnalysis: (l: string) => l === 'hi' ? 'राजनीतिक विश्लेषण' : 'Political Analysis',
  eclipseTracker: (l: string) => l === 'hi' ? 'ग्रहण ट्रैकर' : 'Eclipse Tracker',
  ingressDates: (l: string) => l === 'hi' ? 'संक्रांति तिथियां' : 'Ingress / Sankranti Dates',
  planet: (l: string) => l === 'hi' ? 'ग्रह' : 'Planet',
  sign: (l: string) => l === 'hi' ? 'राशि' : 'Sign',
  house: (l: string) => l === 'hi' ? 'भाव' : 'House',
  degree: (l: string) => l === 'hi' ? 'अंश' : 'Degree',
  impact: (l: string) => l === 'hi' ? 'प्रभाव' : 'Impact',
  currentSign: (l: string) => l === 'hi' ? 'वर्तमान राशि' : 'Current Sign',
  date: (l: string) => l === 'hi' ? 'तिथि' : 'Date',
  type: (l: string) => l === 'hi' ? 'प्रकार' : 'Type',
  solarLunar: (l: string) => l === 'hi' ? 'सूर्य/चंद्र' : 'Solar/Lunar',
  affectedHouse: (l: string) => l === 'hi' ? 'प्रभावित भाव' : 'Affected House',
  theme: (l: string) => l === 'hi' ? 'विषय' : 'Theme',
  loading: (l: string) => l === 'hi' ? 'लोड हो रहा है...' : 'Loading...',
  dataUnavailable: (l: string) => l === 'hi' ? 'डेटा उपलब्ध नहीं है' : 'Data unavailable',
  noRisks: (l: string) => l === 'hi' ? 'कोई सक्रिय जोखिम नहीं' : 'No active risks detected',
  independenceDate: (l: string) => l === 'hi' ? 'स्वतंत्रता तिथि' : 'Independence Date',
  time: (l: string) => l === 'hi' ? 'समय' : 'Time',
  place: (l: string) => l === 'hi' ? 'स्थान' : 'Place',
  condition: (l: string) => l === 'hi' ? 'स्थिति' : 'Condition',
  meaning: (l: string) => l === 'hi' ? 'अर्थ' : 'Meaning',
  transitingPlanets: (l: string) => l === 'hi' ? 'गोचर ग्रह' : 'Transiting Planets',
  growth: (l: string) => l === 'hi' ? 'विकास' : 'Growth',
  pressure: (l: string) => l === 'hi' ? 'दबाव' : 'Pressure',
  neutral: (l: string) => l === 'hi' ? 'सामान्य' : 'Neutral',
  stable: (l: string) => l === 'hi' ? 'स्थिर' : 'Stable',
  unstable: (l: string) => l === 'hi' ? 'अस्थिर' : 'Unstable',
  pressured: (l: string) => l === 'hi' ? 'दबाव में' : 'Pressured',
  positive: (l: string) => l === 'hi' ? 'सकारात्मक' : 'Positive',
  negative: (l: string) => l === 'hi' ? 'नकारात्मक' : 'Negative',
  low: (l: string) => l === 'hi' ? 'कम' : 'Low',
  medium: (l: string) => l === 'hi' ? 'मध्यम' : 'Medium',
  high: (l: string) => l === 'hi' ? 'उच्च' : 'High',
  year: (l: string) => l === 'hi' ? 'वर्ष' : 'Year',
  solar: (l: string) => l === 'hi' ? 'सूर्य ग्रहण' : 'Solar',
  lunar: (l: string) => l === 'hi' ? 'चंद्र ग्रहण' : 'Lunar',
  kundliChart: (l: string) => l === 'hi' ? 'कुंडली चार्ट' : 'Kundli Chart',
  gocharChart: (l: string) => l === 'hi' ? 'गोचर चार्ट' : 'Gochar (Transit) Chart',
};

/* ────────────────────────────── No hardcoded country fallback ────────────────────────────── */

/* ────────────────────────────── Sub-components ────────────────────────────── */

function StatusBadge({ status, lang }: { status: 'positive' | 'negative' | 'neutral'; lang: string }) {
  const config = {
    positive: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', dot: 'bg-emerald-500', label: T.positive(lang) },
    negative: { bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200', dot: 'bg-red-500', label: T.negative(lang) },
    neutral: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', dot: 'bg-amber-500', label: T.neutral(lang) },
  }[status] || {
    // fallback for undefined/unknown status
    bg: 'bg-amber-50',
    text: 'text-amber-700',
    border: 'border-amber-200',
    dot: 'bg-amber-500',
    label: T.neutral(lang)
  };

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-sm font-medium border ${config.bg} ${config.text} ${config.border}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
      {config.label}
    </span>
  );
}

function SeverityBadge({ severity, lang }: { severity: 'high' | 'medium' | 'low'; lang: string }) {
  const config = {
    high: { bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-300', label: T.high(lang) },
    medium: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-300', label: T.medium(lang) },
    low: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-300', label: T.low(lang) },
  }[severity] || {
    // fallback for undefined/unknown severity
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    border: 'border-emerald-300',
    label: T.low(lang)
  };

  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-sm font-semibold border ${config.bg} ${config.text} ${config.border}`}>
      {severity === 'high' && '\u26A0\uFE0F'} {config.label}
    </span>
  );
}

function LoadingSpinner({ lang }: { lang: string }) {
  return (
    <div className="flex items-center justify-center py-12">
      <Loader2 className="w-6 h-6 animate-spin text-primary" />
      <span className="ml-2 text-foreground">{T.loading(lang)}</span>
    </div>
  );
}

function DataUnavailable({ lang }: { lang: string }) {
  return (
    <p className="text-center text-foreground py-6 text-sm">{T.dataUnavailable(lang)}</p>
  );
}

/* ── Deep-flatten {en, hi} objects in API responses ── */
function flattenBilingual<T = unknown>(obj: unknown, lang: string): T {
  if (obj === null || obj === undefined) return obj;
  if (typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map((item) => flattenBilingual(item, lang)) as T;
  const record = obj as Record<string, unknown>;
  // If this object IS a bilingual pair, pick the right language
  const keys = Object.keys(record);
  if (keys.length <= 3 && keys.includes('en') && keys.includes('hi')) {
    return (lang === 'hi' ? (record.hi || record.en) : record.en) as T;
  }
  // Otherwise recurse into all values
  const result: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(record)) {
    result[k] = flattenBilingual(v, lang);
  }
  return result as T;
}

/* ────────────────────────────── Main Component ────────────────────────────── */

export default function MundaneTab({ language: languageProp }: MundaneTabProps) {
  const { t, language: contextLang } = useTranslation();
  const lang = (languageProp || contextLang) as Language;

  const currentYear = new Date().getFullYear();
  const [selectedCountry, setSelectedCountry] = useState('india');
  const [selectedYear, setSelectedYear] = useState(currentYear);
  const [countries, setCountries] = useState<CountryOption[]>([]);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [eclipseData, setEclipseData] = useState<EclipseEntry[] | null>(null);
  const [ingressData, setIngressData] = useState<IngressEntry[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingEclipse, setLoadingEclipse] = useState(false);
  const [loadingIngress, setLoadingIngress] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedHouses, setExpandedHouses] = useState<Set<number>>(new Set());
  /* ── fetch country list ── */
  useEffect(() => {
    let cancelled = false;
    async function fetchCountries() {
      try {
        const raw = await api.get('/api/mundane/countries');
        const list = Array.isArray(raw) ? raw : raw?.countries;
        if (!cancelled && Array.isArray(list) && list.length > 0) {
          const normalized: CountryOption[] = list.map((c) => {
            const country = c as Record<string, unknown>;
            const flat = flattenBilingual<Record<string, unknown>>(country, lang);
            const flatName = flat.name;
            const countryName = country.name;
            const key = country.key as string | undefined;
            return {
              code: key || (flat.code as string | undefined) || (country.code as string | undefined) || '',
              name: typeof flatName === 'string' ? flatName : (typeof countryName === 'object' && countryName ? (countryName as Record<string, string>).en : (countryName as string)) || key || '',
              name_hi: typeof countryName === 'object' && countryName ? (countryName as Record<string, string>).hi : (country.name_hi as string | undefined),
              flag: (flat.flag as string | undefined) || (country.flag as string | undefined),
            };
          });
          setCountries(normalized);
        }
      } catch {
        // API may not exist yet — keep defaults
      }
    }
    fetchCountries();
    return () => { cancelled = true; };
  }, [lang]);

  /* ── fetch main analysis ── */
  const fetchAnalysis = useCallback(async (country: string, year: number) => {
    setLoading(true);
    setError(null);
    setAnalysisData(null);
    try {
      const raw = await api.get(`/api/mundane/${country}/analysis?year=${year}`);
      const flat = flattenBilingual<Record<string, unknown>>(raw, lang);
      // Normalize API field names to match component expectations
      // Extract birth chart planets into flat array
      const rawBirthChart = raw?.birth_chart?.planets || raw?.birth_chart || {};
      const birthChartArr = typeof rawBirthChart === 'object' && !Array.isArray(rawBirthChart)
        ? Object.entries(rawBirthChart).map(([name, data]) => {
            const d = (data || {}) as Record<string, unknown>;
            return ({
            planet: name,
            sign: (d.sign as string) || '',
            degree: d.sign_degree != null ? Number(d.sign_degree).toFixed(2) + '\u00b0' : (d.longitude != null ? (Number(d.longitude) % 30).toFixed(2) + '\u00b0' : ''),
            house: (d.house as number) || 0,
            nakshatra: (d.nakshatra as string) || '',
            retrograde: Boolean(d.retrograde),
          });
        })
        : Array.isArray(rawBirthChart) ? rawBirthChart : [];

      // Extract transits
      const rawTransits = raw?.current_transits || [];
      const transitsArr = Array.isArray(rawTransits) ? rawTransits.map((t) => {
        const tr = (t || {}) as Record<string, unknown>;
        const houseMeaning = tr.house_meaning;
        const hm = typeof houseMeaning === 'object' && houseMeaning ? (houseMeaning as Record<string, string>) : null;
        return {
          planet: (tr.planet as string) || '',
          sign: (tr.sign as string) || '',
          current_sign: (tr.sign as string) || (tr.current_sign as string) || '',
          sign_degree: (tr.sign_degree as number) || 0,
          house: (tr.house_in_country_chart as number) || (tr.house as number) || 0,
          impact: hm ? (hm[lang] || hm.en || '') : ((tr.impact as string) || (tr.house_meaning as string) || ''),
          impact_hi: hm ? hm.hi : undefined,
          type: ((tr.type as TransitImpact['type']) || 'neutral'),
          retrograde: Boolean(tr.retrograde),
        };
      }) : [];

      // Preserve ascendant and houses from birth_chart for visual chart rendering
      const birthAscendant = raw?.birth_chart?.ascendant || null;
      const birthHouses = Array.isArray(raw?.birth_chart?.houses) ? raw.birth_chart.houses : null;

      const normalized = {
        ...flat,
        // country info → top-level
        independence_date: raw?.country?.independence_date || flat.independence_date,
        independence_time: raw?.country?.independence_time || flat.independence_time,
        independence_place: typeof raw?.country?.capital === 'object' ? (raw.country.capital[lang] || raw.country.capital.en) : (raw?.country?.capital || flat.independence_place),
        birth_chart: birthChartArr,
        birth_chart_ascendant: birthAscendant,
        birth_chart_houses: birthHouses,
        transits: transitsArr,
        houses: (raw?.house_analysis || flat.house_analysis || []).map((h: unknown) => {
          const house = (h || {}) as Record<string, unknown>;
          const mm = house.mundane_meaning;
          const meaning = typeof mm === 'object' && mm
            ? ((mm as Record<string, string>)[lang] || (mm as Record<string, string>).en || '')
            : (mm as string) || '';
          const cond = house.condition as string || '';
          const status = /positive|stable|growth|good/i.test(cond) ? 'positive'
            : /negative|unstable|pressure|risk|conflict/i.test(cond) ? 'negative'
            : 'neutral';
          return {
            ...house,
            meaning,
            transiting_planets: house.transit_planets || house.transiting_planets || [],
            status,
          };
        }),
        // build indicators from summary
        indicators: flat.indicators || (flat.summary ? [
          { label: T.nationalMood(lang), label_hi: T.nationalMood('hi'), value: flat.summary.national_mood || '-', status: flat.summary.national_mood === 'positive' ? 'positive' : flat.summary.national_mood === 'negative' ? 'negative' : 'neutral' },
          { label: T.govStability(lang), label_hi: T.govStability('hi'), value: flat.summary.government_stability || '-', status: flat.summary.government_stability === 'stable' ? 'positive' : flat.summary.government_stability === 'pressured' ? 'negative' : 'neutral' },
          { label: T.economyTrend(lang), label_hi: T.economyTrend('hi'), value: flat.economic_indicators?.trend || '-', status: flat.economic_indicators?.trend === 'growth' ? 'positive' : flat.economic_indicators?.trend === 'pressure' ? 'negative' : 'neutral' },
          { label: T.riskLevel(lang), label_hi: T.riskLevel('hi'), value: flat.health_indicators?.risk_level || flat.summary?.risk_level || '-', status: flat.health_indicators?.risk_level === 'low' ? 'positive' : flat.health_indicators?.risk_level === 'high' ? 'negative' : 'neutral' },
        ] : []),
        // risks from conflict_indicators
        risks: flat.risks || flat.conflict_indicators,
        // economic analysis
        economic_analysis: flat.economic_analysis || flat.economic_indicators,
        // political analysis — backend key is political_indicators
        political_analysis: (() => {
          const pi = flat.political_indicators as Record<string, unknown> | null | undefined;
          if (!pi) return null;
          const stability = (pi.government_stability as string) || '';
          const factors = pi.factors;
          const description = Array.isArray(factors)
            ? factors.map((f: unknown) => (typeof f === 'string' ? f : (f as Record<string,string>)?.en || '')).filter(Boolean).join('. ')
            : '';
          return { stability, description };
        })(),
      };
      setAnalysisData(normalized);
    } catch (err) {
      setAnalysisData(null);
      setError(err instanceof Error ? err.message : 'Failed to load analysis');
    }
    setLoading(false);
  }, [lang]);

  /* ── fetch eclipses ── */
  const fetchEclipses = useCallback(async (year: number, country: string) => {
    setLoadingEclipse(true);
    try {
      const raw = await api.get(`/api/mundane/eclipses?year=${year}&country=${country}`);
      const data = flattenBilingual<Record<string, unknown> | EclipseEntry[]>(raw, lang);
      setEclipseData(Array.isArray(data) ? data : (data as Record<string, unknown>)?.eclipses as EclipseEntry[] ?? null);
    } catch {
      setEclipseData(null);
    }
    setLoadingEclipse(false);
  }, [lang]);

  /* ── fetch ingress ── */
  const fetchIngress = useCallback(async (year: number) => {
    setLoadingIngress(true);
    try {
      const raw = await api.get(`/api/mundane/ingress?year=${year}`);
      const data = flattenBilingual<Record<string, unknown> | IngressEntry[]>(raw, lang);
      setIngressData(Array.isArray(data) ? data : (data as Record<string, unknown>)?.ingress as IngressEntry[] ?? null);
    } catch {
      setIngressData(null);
    }
    setLoadingIngress(false);
  }, [lang]);

  /* ── initial load + reload on country/year change ── */
  useEffect(() => {
    fetchAnalysis(selectedCountry, selectedYear);
    fetchEclipses(selectedYear, selectedCountry);
    fetchIngress(selectedYear);
  }, [selectedCountry, selectedYear, fetchAnalysis, fetchEclipses, fetchIngress]);

  /* ── house toggle ── */
  const toggleHouse = (house: number) => {
    setExpandedHouses(prev => {
      const next = new Set(prev);
      if (next.has(house)) { next.delete(house); } else { next.add(house); }
      return next;
    });
  };

  /* ── year navigation ── */
  const prevYear = () => setSelectedYear(y => y - 1);
  const nextYear = () => setSelectedYear(y => y + 1);

  /* ── helper: resolve localized text from API payload ── */
  const loc = (en: string | {en?: string; hi?: string} | undefined, hi: string | undefined): string => {
    // Handle bilingual object {en: "...", hi: "..."}
    if (en && typeof en === 'object') {
      if (lang === 'hi' && en.hi) return en.hi;
      return en.en || '';
    }
    // Handle separate en/hi params
    if (lang === 'hi' && hi) return hi;
    return (en as string) || '';
  };

  /* ── Indicator icon + color helpers ── */
  const indicatorEmoji = (idx: number, status: string) => {
    const icons = [
      // National Mood
      status === 'positive' ? '\uD83D\uDFE2' : status === 'negative' ? '\uD83D\uDD34' : '\uD83D\uDFE1',
      // Gov Stability
      status === 'positive' ? '\uD83D\uDFE2' : status === 'negative' ? '\uD83D\uDD34' : '\uD83D\uDFE1',
      // Economy
      status === 'positive' ? '\uD83D\uDCC8' : status === 'negative' ? '\uD83D\uDCC9' : '\u27A1\uFE0F',
      // Risk
      status === 'negative' ? '\u26A0\uFE0F' : status === 'neutral' ? '\u26A0\uFE0F' : '\u2705',
    ];
    return icons[idx] ?? '\u2139\uFE0F';
  };

  const indicatorBorderColor = (status: string) => {
    if (status === 'positive') return 'border-emerald-300';
    if (status === 'negative') return 'border-red-300';
    return 'border-amber-300';
  };

  /* ── Build PlanetEntry[] for KundliChartSVG (birth chart) ── */
  const birthChartPlanets: PlanetEntry[] | null = useMemo(() => {
    if (!analysisData?.birth_chart || analysisData.birth_chart.length === 0) return null;
    return analysisData.birth_chart.map(p => ({
      planet: p.planet,
      sign: p.sign,
      sign_degree: parseFloat(p.degree?.replace('\u00b0', '') || '0') || 0,
      status: p.retrograde ? 'Retrograde' : '',
      is_retrograde: !!p.retrograde,
    } as PlanetEntry));
  }, [analysisData]);

  /* ── Build PlanetEntry[] for KundliChartSVG (transit chart) ── */
  const transitChartPlanets: PlanetEntry[] | null = useMemo(() => {
    if (!analysisData?.transits || analysisData.transits.length === 0) return null;
    return analysisData.transits.map(t => ({
      planet: t.planet,
      sign: t.current_sign || t.sign || '',
      sign_degree: t.sign_degree || 0,
      status: t.retrograde ? 'Retrograde' : '',
      is_retrograde: !!t.retrograde,
    } as PlanetEntry));
  }, [analysisData]);

  /* ────────────────────────────── Render ────────────────────────────── */

  const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
  const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
  const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
  const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';
  const tdWrapCls   = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

  return (
    <div className="space-y-4">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Globe2 className="w-6 h-6" />
          {lang === 'hi' ? 'मुंडेन ज्योतिष — विश्व प्रभाव' : 'Mundane Astrology — Global Impact'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {lang === 'hi' ? 'प्राकृतिक आपदाओं, राजनीतिक परिवर्तनों एवं आर्थिक प्रवृत्तियों का ज्योतिषीय विश्लेषण' : 'Analysis of natural events, political shifts and economic trends'}
        </p>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-red-800">
                {t('auto.serverError')}
              </p>
              <p className="text-sm text-red-600 mt-1">
                {t('auto.failedToLoadDataPlea')}
              </p>
              <button
                onClick={() => fetchAnalysis(selectedCountry, selectedYear)}
                className="mt-2 px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 text-sm rounded-md transition-colors"
              >
                {t('auto.retry')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ── 1. Country Selector + Summary ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Globe2 className="w-4 h-4" />
          <span>{T.mundaneAstrology(lang)}</span>
        </div>
        <div className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">{T.selectCountry(lang)}</label>
            <select
              value={selectedCountry}
              onChange={e => setSelectedCountry(e.target.value)}
              className="w-full sm:w-64 rounded-lg border border-border bg-white px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {countries.map(c => (
                <option key={c.code} value={c.code}>
                  {c.flag ? `${c.flag} ` : ''}{lang === 'hi' && c.name_hi ? c.name_hi : c.name}
                </option>
              ))}
            </select>
          </div>
          {loading ? (
            <LoadingSpinner lang={lang} />
          ) : analysisData?.indicators && analysisData.indicators.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {analysisData.indicators.slice(0, 4).map((card, idx) => (
                <div key={idx} className={`rounded-xl border bg-white p-3 text-center ${indicatorBorderColor(card.status)}`}>
                  <div className="text-2xl mb-1">{indicatorEmoji(idx, card.status)}</div>
                  <div className="text-sm font-medium text-foreground mb-0.5">{loc(card.label, card.label_hi)}</div>
                  <div className="text-sm font-semibold text-foreground">{loc(card.value, card.value_hi)}</div>
                </div>
              ))}
            </div>
          ) : !loading && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { label: T.nationalMood(lang), emoji: '\uD83D\uDFE1' },
                { label: T.govStability(lang), emoji: '\uD83D\uDFE1' },
                { label: T.economyTrend(lang), emoji: '\u27A1\uFE0F' },
                { label: T.riskLevel(lang), emoji: '\u26A0\uFE0F' },
              ].map((card, idx) => (
                <div key={idx} className="rounded-xl border border-border bg-white p-3 text-center">
                  <div className="text-2xl mb-1">{card.emoji}</div>
                  <div className="text-sm font-medium text-foreground mb-0.5">{card.label}</div>
                  <div className="text-sm text-foreground italic">{T.dataUnavailable(lang)}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ── 2. Country Birth Chart ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Landmark className="w-4 h-4" />
          <span>{T.countryBirthChart(lang)}</span>
        </div>
        <div className="p-4">
          {loading ? (
            <LoadingSpinner lang={lang} />
          ) : analysisData ? (
            <>
              {(analysisData.independence_date || analysisData.independence_place) && (
                <div className="mb-4 text-xs space-y-1 text-foreground">
                  {analysisData.independence_date && <p><span className="font-medium">{T.independenceDate(lang)}:</span> {analysisData.independence_date}</p>}
                  {analysisData.independence_time && <p><span className="font-medium">{T.time(lang)}:</span> {analysisData.independence_time}</p>}
                  {analysisData.independence_place && <p><span className="font-medium">{T.place(lang)}:</span> {analysisData.independence_place}</p>}
                </div>
              )}
              {birthChartPlanets && analysisData.birth_chart && analysisData.birth_chart.length > 0 ? (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
                  <div className="flex flex-col items-center">
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">{T.kundliChart(lang)}</p>
                    <div className="w-full max-w-[340px] aspect-square">
                      <KundliChartSVG
                        planets={birthChartPlanets}
                        ascendantSign={analysisData.birth_chart_ascendant?.sign || ''}
                        language={lang}
                        showHouseNumbers={false}
                        showRashiNumbers
                        rashiNumberPlacement="corner"
                        showAscendantMarker={false}
                      />
                    </div>
                  </div>
                  <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
                    <colgroup>
                      <col style={{ width: '30%' }} /><col style={{ width: '30%' }} /><col style={{ width: '20%' }} /><col style={{ width: '20%' }} />
                    </colgroup>
                    <thead>
                      <tr>
                        <th className={thCls}>{T.planet(lang)}</th>
                        <th className={thCls}>{T.sign(lang)}</th>
                        <th className={thCls}>{T.house(lang)}</th>
                        <th className={thCls}>{T.degree(lang)}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysisData.birth_chart.map((p, idx) => (
                        <tr key={idx}>
                          <td className={`${tdCls} font-semibold`}>{translatePlanet(p.planet, lang)}</td>
                          <td className={tdCls}>{translateSign(p.sign, lang)}</td>
                          <td className={`${tdCls} text-center`}>{p.house}</td>
                          <td className={`${tdCls} font-mono`}>{p.degree}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <DataUnavailable lang={lang} />
              )}
            </>
          ) : (
            <DataUnavailable lang={lang} />
          )}
        </div>
      </div>

      {/* ── 3. Current Transits Impact ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <TrendingUp className="w-4 h-4" />
          <span>{T.currentTransits(lang)}</span>
        </div>
        <div className="p-4">
          {loading ? (
            <LoadingSpinner lang={lang} />
          ) : analysisData?.transits && analysisData.transits.length > 0 && transitChartPlanets ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
              <div className="flex flex-col items-center">
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">{T.gocharChart(lang)}</p>
                <div className="w-full max-w-[340px] aspect-square">
                  <KundliChartSVG
                    planets={transitChartPlanets}
                    ascendantSign={analysisData.birth_chart_ascendant?.sign || ''}
                    language={lang}
                    showHouseNumbers={false}
                    showRashiNumbers
                    rashiNumberPlacement="corner"
                    showAscendantMarker={false}
                  />
                </div>
              </div>
              <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
                <colgroup>
                  <col style={{ width: '22%' }} /><col style={{ width: '22%' }} /><col style={{ width: '12%' }} /><col style={{ width: '44%' }} />
                </colgroup>
                <thead>
                  <tr>
                    <th className={thCls}>{T.planet(lang)}</th>
                    <th className={thCls}>{T.currentSign(lang)}</th>
                    <th className={thCls}>{T.house(lang)}</th>
                    <th className={thCls}>{T.impact(lang)}</th>
                  </tr>
                </thead>
                <tbody>
                  {analysisData.transits.map((t_item, idx) => {
                    const rowCls = t_item.type === 'benefic' ? 'bg-emerald-50' : t_item.type === 'malefic' ? 'bg-red-50' : '';
                    const impCls = t_item.type === 'benefic' ? 'text-emerald-700' : t_item.type === 'malefic' ? 'text-red-700' : 'text-amber-700';
                    return (
                      <tr key={idx} className={rowCls}>
                        <td className={`${tdCls} font-semibold`}>{translatePlanet(t_item.planet, lang)}</td>
                        <td className={tdCls}>{translateSign(t_item.current_sign, lang)}</td>
                        <td className={`${tdCls} text-center`}>{t_item.house}</td>
                        <td className={`${tdWrapCls} ${impCls}`}>{loc(t_item.impact, t_item.impact_hi)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : !loading && (
            <DataUnavailable lang={lang} />
          )}
        </div>
      </div>

      {/* ── 4. House Analysis ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Building2 className="w-4 h-4" />
          <span>{T.houseAnalysis(lang)}</span>
        </div>
        <div className="p-4">
          {loading ? (
            <LoadingSpinner lang={lang} />
          ) : analysisData?.houses && analysisData.houses.length > 0 ? (
            <div className="space-y-2">
              {analysisData.houses.map(h => {
                const isExpanded = expandedHouses.has(h.house);
                return (
                  <div key={h.house} className="border border-border rounded-lg overflow-hidden">
                    <button
                      type="button"
                      onClick={() => toggleHouse(h.house)}
                      className="w-full flex items-center justify-between p-3 text-left hover:bg-muted/20 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-7 h-7 flex items-center justify-center rounded-full bg-sacred-gold-dark text-white font-bold text-xs">
                          {h.house}
                        </span>
                        <span className="text-sm text-foreground">
                          {(h.meaning as string) || '—'}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <StatusBadge status={h.status} lang={lang} />
                        <ChevronDown className={`w-4 h-4 text-muted-foreground transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                      </div>
                    </button>
                    {isExpanded && (
                      <div className="px-4 pb-3 border-t border-border pt-2 text-xs space-y-1.5">
                        <div>
                          <span className="font-semibold text-foreground uppercase tracking-wide">{T.condition(lang)}: </span>
                          <span className="text-foreground">{
                            typeof h.condition === 'object' && h.condition !== null
                              ? (() => { const c = h.condition as Record<string, string>; return (lang === 'hi' ? c.hi : c.en) || ''; })()
                              : loc(h.condition, h.condition_hi)
                          }</span>
                        </div>
                        {h.transiting_planets && h.transiting_planets.length > 0 && (
                          <div>
                            <span className="font-semibold text-foreground uppercase tracking-wide">{T.transitingPlanets(lang)}: </span>
                            <span className="text-foreground">{h.transiting_planets.map(p => translatePlanet(p, lang)).join(', ')}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <DataUnavailable lang={lang} />
          )}
        </div>
      </div>

      {/* ── 5. Conflict & Risk Indicators ── */}
      <div className={ohContainer}>
        <div className="bg-red-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          <span>{T.conflictIndicators(lang)}</span>
        </div>
        <div className="p-4">
          {loading ? (
            <LoadingSpinner lang={lang} />
          ) : analysisData?.risks && analysisData.risks.length > 0 ? (
            <div className="space-y-2">
              {analysisData.risks.map((risk, idx) => {
                const borderColor = risk.severity === 'high' ? 'border-l-red-500' : risk.severity === 'medium' ? 'border-l-amber-400' : 'border-l-emerald-400';
                const bgColor = risk.severity === 'high' ? 'bg-red-50' : risk.severity === 'medium' ? 'bg-amber-50' : 'bg-emerald-50';
                return (
                  <div key={idx} className={`border border-border border-l-4 ${borderColor} ${bgColor} rounded-lg p-3`}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold text-foreground">{loc(risk.title, risk.title_hi)}</span>
                      <SeverityBadge severity={risk.severity} lang={lang} />
                    </div>
                    <p className="text-xs text-foreground leading-relaxed">{loc(risk.description, risk.description_hi)}</p>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-6">
              <Shield className="w-8 h-8 mx-auto text-emerald-400 mb-2" />
              <p className="text-sm text-foreground">{T.noRisks(lang)}</p>
            </div>
          )}
        </div>
      </div>

      {/* ── 6. Economic Analysis ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <TrendingUp className="w-4 h-4" />
          <span>{T.economicAnalysis(lang)}</span>
        </div>
        <div className="p-4">
          {loading ? (
            <LoadingSpinner lang={lang} />
          ) : analysisData?.economic_analysis ? (
            <div className="flex items-start gap-4">
              <div className="shrink-0">
                {analysisData.economic_analysis.trend === 'growth' && (
                  <div className="w-10 h-10 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-emerald-600" />
                  </div>
                )}
                {analysisData.economic_analysis.trend === 'pressure' && (
                  <div className="w-10 h-10 rounded-full bg-red-50 border border-red-200 flex items-center justify-center">
                    <TrendingDown className="w-5 h-5 text-red-600" />
                  </div>
                )}
                {analysisData.economic_analysis.trend === 'neutral' && (
                  <div className="w-10 h-10 rounded-full bg-amber-50 border border-amber-200 flex items-center justify-center">
                    <Minus className="w-5 h-5 text-amber-600" />
                  </div>
                )}
              </div>
              <div>
                <p className="text-sm font-semibold text-foreground mb-1">
                  {analysisData.economic_analysis.trend === 'growth' ? T.growth(lang)
                    : analysisData.economic_analysis.trend === 'pressure' ? T.pressure(lang)
                    : T.neutral(lang)}
                </p>
                <p className="text-xs text-foreground leading-relaxed">
                  {loc(analysisData.economic_analysis.description, analysisData.economic_analysis.description_hi)}
                </p>
              </div>
            </div>
          ) : (
            <DataUnavailable lang={lang} />
          )}
        </div>
      </div>

      {/* ── 7. Political Analysis ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Landmark className="w-4 h-4" />
          <span>{T.politicalAnalysis(lang)}</span>
        </div>
        <div className="p-4">
          {loading ? (
            <LoadingSpinner lang={lang} />
          ) : analysisData?.political_analysis ? (
            <div className="flex items-start gap-4">
              <div className="shrink-0">
                {analysisData.political_analysis.stability === 'stable' && (
                  <div className="w-10 h-10 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center">
                    <Shield className="w-5 h-5 text-emerald-600" />
                  </div>
                )}
                {analysisData.political_analysis.stability === 'unstable' && (
                  <div className="w-10 h-10 rounded-full bg-red-50 border border-red-200 flex items-center justify-center">
                    <AlertTriangle className="w-5 h-5 text-red-600" />
                  </div>
                )}
                {analysisData.political_analysis.stability === 'pressured' && (
                  <div className="w-10 h-10 rounded-full bg-amber-50 border border-amber-200 flex items-center justify-center">
                    <AlertTriangle className="w-5 h-5 text-amber-600" />
                  </div>
                )}
              </div>
              <div>
                <p className="text-sm font-semibold text-foreground mb-1">
                  {analysisData.political_analysis.stability === 'stable' ? T.stable(lang)
                    : analysisData.political_analysis.stability === 'unstable' ? T.unstable(lang)
                    : T.pressured(lang)}
                </p>
                <p className="text-xs text-foreground leading-relaxed">
                  {loc(analysisData.political_analysis.description, analysisData.political_analysis.description_hi)}
                </p>
              </div>
            </div>
          ) : (
            <DataUnavailable lang={lang} />
          )}
        </div>
      </div>

      {/* ── 8. Eclipse Tracker ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Moon className="w-4 h-4" />
          <span>{T.eclipseTracker(lang)}</span>
        </div>
        <div className="p-4">
          <div className="flex items-center justify-center gap-4 mb-4">
            <button type="button" onClick={prevYear} className="p-1.5 rounded-lg border border-border hover:bg-muted/10 transition-colors" aria-label={t('auto.previousYear')}>
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-sm font-semibold min-w-[60px] text-center">{selectedYear}</span>
            <button type="button" onClick={nextYear} className="p-1.5 rounded-lg border border-border hover:bg-muted/10 transition-colors" aria-label={t('auto.nextYear')}>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          {loadingEclipse ? (
            <LoadingSpinner lang={lang} />
          ) : eclipseData && eclipseData.length > 0 ? (
            <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
              <colgroup>
                <col style={{ width: '16%' }} /><col style={{ width: '14%' }} /><col style={{ width: '14%' }} /><col style={{ width: '10%' }} /><col style={{ width: '46%' }} />
              </colgroup>
              <thead>
                <tr>
                  <th className={thCls}>{T.date(lang)}</th>
                  <th className={thCls}>{T.type(lang)}</th>
                  <th className={thCls}>{T.solarLunar(lang)}</th>
                  <th className={thCls}>{T.affectedHouse(lang)}</th>
                  <th className={thCls}>{T.impact(lang)}</th>
                </tr>
              </thead>
              <tbody>
                {eclipseData.map((e, idx) => (
                  <tr key={idx}>
                    <td className={`${tdCls} font-mono`}>{e.date}</td>
                    <td className={tdCls}>{loc(e.type, e.type_hi)}</td>
                    <td className={tdCls}>
                      {(e.type as string)?.toLowerCase() === 'solar'
                        ? <span className="inline-flex items-center gap-1"><Sun className="w-3 h-3 text-amber-500" />{T.solar(lang)}</span>
                        : <span className="inline-flex items-center gap-1"><Moon className="w-3 h-3 text-muted-foreground" />{T.lunar(lang)}</span>}
                    </td>
                    <td className={`${tdCls} text-center`}>{e.affected_house || '—'}</td>
                    <td className={tdWrapCls}>{loc(e.impact, e.impact_hi) || (e as any).affected_domain || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <DataUnavailable lang={lang} />
          )}
        </div>
      </div>

      {/* ── 9. Ingress / Sankranti Dates ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Sun className="w-4 h-4" />
          <span>{T.ingressDates(lang)}</span>
        </div>
        <div className="p-4">
          {loadingIngress ? (
            <LoadingSpinner lang={lang} />
          ) : ingressData && ingressData.length > 0 ? (
            <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
              <colgroup>
                <col style={{ width: '28%' }} /><col style={{ width: '22%' }} /><col style={{ width: '50%' }} />
              </colgroup>
              <thead>
                <tr>
                  <th className={thCls}>{T.sign(lang)}</th>
                  <th className={thCls}>{T.date(lang)}</th>
                  <th className={thCls}>{T.theme(lang)}</th>
                </tr>
              </thead>
              <tbody>
                {ingressData.map((entry, idx) => (
                  <tr key={idx}>
                    <td className={`${tdCls} font-semibold`}>{(entry as any).sign || '—'}</td>
                    <td className={`${tdCls} font-mono`}>{entry.date}</td>
                    <td className={tdWrapCls}>{(entry as any).sankranti || loc(entry.theme, entry.theme_hi) || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <DataUnavailable lang={lang} />
          )}
        </div>
      </div>
    </div>
  );
}
