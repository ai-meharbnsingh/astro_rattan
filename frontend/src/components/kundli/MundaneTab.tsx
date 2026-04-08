import { useState, useEffect, useCallback } from 'react';
import { Loader2, ChevronDown, ChevronLeft, ChevronRight, AlertTriangle, TrendingUp, TrendingDown, Minus, Shield, Globe2, Building2, Landmark, Moon, Sun } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import type { Language } from '@/lib/i18n';

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
}

interface TransitImpact {
  planet: string;
  current_sign: string;
  house: number;
  impact: string;
  impact_hi?: string;
  type: 'benefic' | 'malefic' | 'neutral';
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
};

/* ────────────────────────────── Mundane house meanings ────────────────────────────── */

const MUNDANE_HOUSE_MEANINGS: { en: string; hi: string }[] = [
  { en: 'Nation & People', hi: 'राष्ट्र और जनता' },
  { en: 'National Wealth & Economy', hi: 'राष्ट्रीय धन और अर्थव्यवस्था' },
  { en: 'Communication & Media', hi: 'संचार और मीडिया' },
  { en: 'Land, Agriculture & Opposition', hi: 'भूमि, कृषि और विपक्ष' },
  { en: 'Entertainment, Sports & Youth', hi: 'मनोरंजन, खेल और युवा' },
  { en: 'Public Health & Defence', hi: 'जन स्वास्थ्य और रक्षा' },
  { en: 'Foreign Affairs & War', hi: 'विदेश मामले और युद्ध' },
  { en: 'Death, Disasters & Taxes', hi: 'आपदाएं, कर और मृत्यु' },
  { en: 'Law, Religion & Higher Learning', hi: 'कानून, धर्म और उच्च शिक्षा' },
  { en: 'Government & Ruler', hi: 'सरकार और शासक' },
  { en: 'Parliament & Allies', hi: 'संसद और मित्र राष्ट्र' },
  { en: 'Enemies, Secrets & Expenditure', hi: 'शत्रु, रहस्य और व्यय' },
];

/* ────────────────────────────── Default fallback countries ────────────────────────────── */

const DEFAULT_COUNTRIES: CountryOption[] = [
  { code: 'india', name: 'India', name_hi: 'भारत', flag: '\uD83C\uDDEE\uD83C\uDDF3' },
  { code: 'usa', name: 'United States', name_hi: 'संयुक्त राज्य अमेरिका', flag: '\uD83C\uDDFA\uD83C\uDDF8' },
  { code: 'uk', name: 'United Kingdom', name_hi: 'यूनाइटेड किंगडम', flag: '\uD83C\uDDEC\uD83C\uDDE7' },
  { code: 'china', name: 'China', name_hi: 'चीन', flag: '\uD83C\uDDE8\uD83C\uDDF3' },
  { code: 'russia', name: 'Russia', name_hi: 'रूस', flag: '\uD83C\uDDF7\uD83C\uDDFA' },
  { code: 'japan', name: 'Japan', name_hi: 'जापान', flag: '\uD83C\uDDEF\uD83C\uDDF5' },
  { code: 'germany', name: 'Germany', name_hi: 'जर्मनी', flag: '\uD83C\uDDE9\uD83C\uDDEA' },
  { code: 'france', name: 'France', name_hi: 'फ्रांस', flag: '\uD83C\uDDEB\uD83C\uDDF7' },
  { code: 'pakistan', name: 'Pakistan', name_hi: 'पाकिस्तान', flag: '\uD83C\uDDF5\uD83C\uDDF0' },
  { code: 'israel', name: 'Israel', name_hi: 'इज़राइल', flag: '\uD83C\uDDEE\uD83C\uDDF1' },
];

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
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border ${config.bg} ${config.text} ${config.border}`}>
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
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold border ${config.bg} ${config.text} ${config.border}`}>
      {severity === 'high' && '\u26A0\uFE0F'} {config.label}
    </span>
  );
}

function SectionHeader({ icon, title }: { icon: React.ReactNode; title: string }) {
  return (
    <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2 text-base">
      {icon}
      {title}
    </h4>
  );
}

function LoadingSpinner({ lang }: { lang: string }) {
  return (
    <div className="flex items-center justify-center py-12">
      <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
      <span className="ml-2 text-cosmic-text/70">{T.loading(lang)}</span>
    </div>
  );
}

function DataUnavailable({ lang }: { lang: string }) {
  return (
    <p className="text-center text-cosmic-text/70 py-6 text-sm">{T.dataUnavailable(lang)}</p>
  );
}

/* ── Deep-flatten {en, hi} objects in API responses ── */
function flattenBilingual(obj: any, lang: string): any {
  if (obj === null || obj === undefined) return obj;
  if (typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map((item) => flattenBilingual(item, lang));
  // If this object IS a bilingual pair, pick the right language
  const keys = Object.keys(obj);
  if (keys.length <= 3 && keys.includes('en') && keys.includes('hi')) {
    return lang === 'hi' ? (obj.hi || obj.en) : obj.en;
  }
  // Otherwise recurse into all values
  const result: any = {};
  for (const [k, v] of Object.entries(obj)) {
    result[k] = flattenBilingual(v, lang);
  }
  return result;
}

/* ────────────────────────────── Main Component ────────────────────────────── */

export default function MundaneTab({ language: languageProp }: MundaneTabProps) {
  const { language: contextLang } = useTranslation();
  const lang = (languageProp || contextLang) as Language;

  const currentYear = new Date().getFullYear();
  const [selectedCountry, setSelectedCountry] = useState('india');
  const [selectedYear, setSelectedYear] = useState(currentYear);
  const [countries, setCountries] = useState<CountryOption[]>(DEFAULT_COUNTRIES);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [eclipseData, setEclipseData] = useState<EclipseEntry[] | null>(null);
  const [ingressData, setIngressData] = useState<IngressEntry[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingEclipse, setLoadingEclipse] = useState(false);
  const [loadingIngress, setLoadingIngress] = useState(false);
  const [expandedHouses, setExpandedHouses] = useState<Set<number>>(new Set());
  const [error, setError] = useState<string | null>(null);

  /* ── fetch country list ── */
  useEffect(() => {
    let cancelled = false;
    async function fetchCountries() {
      try {
        const raw = await api.get('/api/mundane/countries');
        const list = Array.isArray(raw) ? raw : raw?.countries;
        if (!cancelled && Array.isArray(list) && list.length > 0) {
          const normalized: CountryOption[] = list.map((c: any) => {
            const flat = flattenBilingual(c, lang);
            return {
              code: flat.code || c.code,
              name: typeof flat.name === 'string' ? flat.name : c.code,
              name_hi: typeof c.name === 'object' ? c.name.hi : c.name_hi,
              flag: flat.flag || c.flag,
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
  }, []);

  /* ── fetch main analysis ── */
  const fetchAnalysis = useCallback(async (country: string, year: number) => {
    setLoading(true);
    setAnalysisData(null);
    try {
      const raw = await api.get(`/api/mundane/${country}/analysis?year=${year}`);
      const flat = flattenBilingual(raw, lang);
      // Normalize API field names to match component expectations
      const normalized = {
        ...flat,
        // country info → top-level
        independence_date: flat.country?.independence_date || flat.independence_date,
        independence_time: flat.country?.independence_time || flat.independence_time,
        independence_place: flat.country?.capital || flat.independence_place,
        // field name mapping
        transits: flat.current_transits || flat.transits,
        houses: flat.house_analysis || flat.houses,
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
      };
      setAnalysisData(normalized);
    } catch {
      setAnalysisData(null);
    }
    setLoading(false);
  }, []);

  /* ── fetch eclipses ── */
  const fetchEclipses = useCallback(async (year: number) => {
    setLoadingEclipse(true);
    try {
      const raw = await api.get(`/api/mundane/eclipses?year=${year}`);
      const data = flattenBilingual(raw, lang);
      setEclipseData(Array.isArray(data) ? data : data?.eclipses ?? null);
    } catch {
      setEclipseData(null);
    }
    setLoadingEclipse(false);
  }, []);

  /* ── fetch ingress ── */
  const fetchIngress = useCallback(async (year: number) => {
    setLoadingIngress(true);
    try {
      const raw = await api.get(`/api/mundane/ingress?year=${year}`);
      const data = flattenBilingual(raw, lang);
      setIngressData(Array.isArray(data) ? data : data?.ingresses ?? null);
    } catch {
      setIngressData(null);
    }
    setLoadingIngress(false);
  }, []);

  /* ── initial load + reload on country/year change ── */
  useEffect(() => {
    fetchAnalysis(selectedCountry, selectedYear);
    fetchEclipses(selectedYear);
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
  const loc = (en: string | undefined, hi: string | undefined): string => {
    if (lang === 'hi' && hi) return hi;
    return en || '';
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

  /* ────────────────────────────── Render ────────────────────────────── */

  return (
    <div className="space-y-6">

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-red-800">
                {lang === 'hi' ? 'सर्वर त्रुटि' : 'Server Error'}
              </p>
              <p className="text-xs text-red-600 mt-1">
                {lang === 'hi' 
                  ? 'डेटा लोड करने में समस्या हुई। कृपया बाद में पुनः प्रयास करें।' 
                  : 'Failed to load data. Please try again later.'}
              </p>
              <button
                onClick={() => fetchAnalysis(selectedCountry, selectedYear)}
                className="mt-2 px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 text-xs rounded-md transition-colors"
              >
                {lang === 'hi' ? 'पुनः प्रयास करें' : 'Retry'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ══════════════════ 1. Country Selector + Summary Dashboard ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<Globe2 className="w-5 h-5 text-sacred-gold" />}
          title={T.mundaneAstrology(lang)}
        />

        {/* Country selector */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-sacred-brown mb-1">
            {T.selectCountry(lang)}
          </label>
          <select
            value={selectedCountry}
            onChange={e => setSelectedCountry(e.target.value)}
            className="w-full sm:w-64 rounded-lg border border-sacred-gold/30 bg-white px-3 py-2 text-sm text-sacred-text focus:outline-none focus:ring-2 focus:ring-sacred-gold/40"
          >
            {countries.map(c => (
              <option key={c.code} value={c.code}>
                {c.flag ? `${c.flag} ` : ''}{lang === 'hi' && c.name_hi ? c.name_hi : c.name}
              </option>
            ))}
          </select>
        </div>

        {/* Indicator cards */}
        {loading ? (
          <LoadingSpinner lang={lang} />
        ) : analysisData?.indicators && analysisData.indicators.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {analysisData.indicators.slice(0, 4).map((card, idx) => (
              <div
                key={idx}
                className={`rounded-xl border bg-white p-3 text-center ${indicatorBorderColor(card.status)}`}
              >
                <div className="text-2xl mb-1">{indicatorEmoji(idx, card.status)}</div>
                <div className="text-xs font-medium text-cosmic-text/70 mb-0.5">
                  {loc(card.label, card.label_hi)}
                </div>
                <div className="text-sm font-semibold text-sacred-text">
                  {loc(card.value, card.value_hi)}
                </div>
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
              <div key={idx} className="rounded-xl border border-sacred-gold/20 bg-white p-3 text-center">
                <div className="text-2xl mb-1">{card.emoji}</div>
                <div className="text-xs font-medium text-cosmic-text/70 mb-0.5">{card.label}</div>
                <div className="text-sm text-cosmic-text/70 italic">{T.dataUnavailable(lang)}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ══════════════════ 2. Country Birth Chart ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<Landmark className="w-5 h-5 text-sacred-gold" />}
          title={T.countryBirthChart(lang)}
        />

        {loading ? (
          <LoadingSpinner lang={lang} />
        ) : analysisData ? (
          <>
            {/* Independence metadata */}
            {(analysisData.independence_date || analysisData.independence_place) && (
              <div className="mb-4 text-sm space-y-1 text-cosmic-text/70">
                {analysisData.independence_date && (
                  <p><span className="font-medium text-sacred-brown">{T.independenceDate(lang)}:</span> {analysisData.independence_date}</p>
                )}
                {analysisData.independence_time && (
                  <p><span className="font-medium text-sacred-brown">{T.time(lang)}:</span> {analysisData.independence_time}</p>
                )}
                {analysisData.independence_place && (
                  <p><span className="font-medium text-sacred-brown">{T.place(lang)}:</span> {analysisData.independence_place}</p>
                )}
              </div>
            )}

            {/* Planet positions table */}
            {analysisData.birth_chart && analysisData.birth_chart.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-sacred-gold/10">
                      <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.planet(lang)}</th>
                      <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.sign(lang)}</th>
                      <th className="text-center p-2 font-medium text-sacred-gold-dark">{T.house(lang)}</th>
                      <th className="text-center p-2 font-medium text-sacred-gold-dark">{T.degree(lang)}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analysisData.birth_chart.map((p, idx) => (
                      <tr key={idx} className="border-b border-slate-100 hover:bg-slate-50/50">
                        <td className="p-2 font-semibold">{translatePlanet(p.planet, lang)}</td>
                        <td className="p-2">{translateSign(p.sign, lang)}</td>
                        <td className="p-2 text-center">{p.house}</td>
                        <td className="p-2 text-center font-mono text-xs">{p.degree}</td>
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

      {/* ══════════════════ 3. Current Transits Impact ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<TrendingUp className="w-5 h-5 text-sacred-gold" />}
          title={T.currentTransits(lang)}
        />

        {loading ? (
          <LoadingSpinner lang={lang} />
        ) : analysisData?.transits && analysisData.transits.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-sacred-gold/10">
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.planet(lang)}</th>
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.currentSign(lang)}</th>
                  <th className="text-center p-2 font-medium text-sacred-gold-dark">{T.house(lang)}</th>
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.impact(lang)}</th>
                </tr>
              </thead>
              <tbody>
                {analysisData.transits.map((t_item, idx) => {
                  const rowColor = t_item.type === 'benefic'
                    ? 'bg-emerald-50/60'
                    : t_item.type === 'malefic'
                    ? 'bg-red-50/60'
                    : 'bg-amber-50/60';
                  const textColor = t_item.type === 'benefic'
                    ? 'text-emerald-700'
                    : t_item.type === 'malefic'
                    ? 'text-red-700'
                    : 'text-amber-700';
                  return (
                    <tr key={idx} className={`border-b border-slate-100 ${rowColor}`}>
                      <td className="p-2 font-semibold">{translatePlanet(t_item.planet, lang)}</td>
                      <td className="p-2">{translateSign(t_item.current_sign, lang)}</td>
                      <td className="p-2 text-center">{t_item.house}</td>
                      <td className={`p-2 text-xs ${textColor}`}>{loc(t_item.impact, t_item.impact_hi)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <DataUnavailable lang={lang} />
        )}
      </div>

      {/* ══════════════════ 4. House Analysis (12 houses) ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<Building2 className="w-5 h-5 text-sacred-gold" />}
          title={T.houseAnalysis(lang)}
        />

        {loading ? (
          <LoadingSpinner lang={lang} />
        ) : analysisData?.houses && analysisData.houses.length > 0 ? (
          <div className="space-y-2">
            {analysisData.houses.map(h => {
              const isExpanded = expandedHouses.has(h.house);
              const fallbackMeaning = MUNDANE_HOUSE_MEANINGS[h.house - 1];
              return (
                <div key={h.house} className="border border-sacred-gold/15 rounded-lg bg-white overflow-hidden">
                  <button
                    type="button"
                    onClick={() => toggleHouse(h.house)}
                    className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-50/50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-8 h-8 flex items-center justify-center rounded-full bg-sacred-gold/10 text-sacred-gold-dark font-bold text-sm">
                        {h.house}
                      </span>
                      <div>
                        <span className="text-sm font-medium text-sacred-brown">
                          {lang === 'hi' ? `भाव ${h.house}` : `House ${h.house}`}
                        </span>
                        <span className="text-xs text-cosmic-text/70 ml-2">
                          {loc(h.meaning || fallbackMeaning?.en, h.meaning_hi || fallbackMeaning?.hi)}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <StatusBadge status={h.status} lang={lang} />
                      <ChevronDown className={`w-4 h-4 text-cosmic-text/70 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                    </div>
                  </button>

                  {isExpanded && (
                    <div className="px-3 pb-3 border-t border-sacred-gold/10 pt-2 text-sm space-y-2">
                      <div>
                        <span className="font-medium text-sacred-brown">{T.condition(lang)}: </span>
                        <span className="text-cosmic-text/70">{loc(h.condition, h.condition_hi)}</span>
                      </div>
                      {h.transiting_planets && h.transiting_planets.length > 0 && (
                        <div>
                          <span className="font-medium text-sacred-brown">{T.transitingPlanets(lang)}: </span>
                          <span className="text-cosmic-text/70">
                            {h.transiting_planets.map(p => translatePlanet(p, lang)).join(', ')}
                          </span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          /* fallback: show 12 houses from static meanings */
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {MUNDANE_HOUSE_MEANINGS.map((h, idx) => (
              <div key={idx} className="border border-sacred-gold/15 rounded-lg bg-white p-3 flex items-start gap-2">
                <span className="w-7 h-7 flex items-center justify-center rounded-full bg-sacred-gold/10 text-sacred-gold-dark font-bold text-xs shrink-0">
                  {idx + 1}
                </span>
                <span className="text-xs text-cosmic-text/70">{lang === 'hi' ? h.hi : h.en}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ══════════════════ 5. Conflict & Risk Indicators ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<AlertTriangle className="w-5 h-5 text-sacred-gold" />}
          title={T.conflictIndicators(lang)}
        />

        {loading ? (
          <LoadingSpinner lang={lang} />
        ) : analysisData?.risks && analysisData.risks.length > 0 ? (
          <div className="space-y-2">
            {analysisData.risks.map((risk, idx) => {
              const borderColor = risk.severity === 'high'
                ? 'border-l-red-500'
                : risk.severity === 'medium'
                ? 'border-l-amber-400'
                : 'border-l-emerald-400';
              const bgColor = risk.severity === 'high'
                ? 'bg-red-50/50'
                : risk.severity === 'medium'
                ? 'bg-amber-50/50'
                : 'bg-emerald-50/50';
              return (
                <div key={idx} className={`border border-sacred-gold/10 border-l-4 ${borderColor} ${bgColor} rounded-lg p-3`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-semibold text-sacred-brown">
                      {loc(risk.title, risk.title_hi)}
                    </span>
                    <SeverityBadge severity={risk.severity} lang={lang} />
                  </div>
                  <p className="text-xs text-cosmic-text/70 leading-relaxed">
                    {loc(risk.description, risk.description_hi)}
                  </p>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-6">
            <Shield className="w-8 h-8 mx-auto text-emerald-400 mb-2" />
            <p className="text-sm text-cosmic-text/70">{T.noRisks(lang)}</p>
          </div>
        )}
      </div>

      {/* ══════════════════ 6. Economic Analysis ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<TrendingUp className="w-5 h-5 text-sacred-gold" />}
          title={T.economicAnalysis(lang)}
        />

        {loading ? (
          <LoadingSpinner lang={lang} />
        ) : analysisData?.economic_analysis ? (
          <div className="flex items-start gap-4">
            <div className="shrink-0">
              {analysisData.economic_analysis.trend === 'growth' && (
                <div className="w-12 h-12 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-emerald-600" />
                </div>
              )}
              {analysisData.economic_analysis.trend === 'pressure' && (
                <div className="w-12 h-12 rounded-full bg-red-50 border border-red-200 flex items-center justify-center">
                  <TrendingDown className="w-6 h-6 text-red-600" />
                </div>
              )}
              {analysisData.economic_analysis.trend === 'neutral' && (
                <div className="w-12 h-12 rounded-full bg-amber-50 border border-amber-200 flex items-center justify-center">
                  <Minus className="w-6 h-6 text-amber-600" />
                </div>
              )}
            </div>
            <div>
              <p className="text-sm font-semibold text-sacred-brown mb-1">
                {analysisData.economic_analysis.trend === 'growth' ? T.growth(lang)
                  : analysisData.economic_analysis.trend === 'pressure' ? T.pressure(lang)
                  : T.neutral(lang)}
              </p>
              <p className="text-sm text-cosmic-text/70 leading-relaxed">
                {loc(analysisData.economic_analysis.description, analysisData.economic_analysis.description_hi)}
              </p>
            </div>
          </div>
        ) : (
          <DataUnavailable lang={lang} />
        )}
      </div>

      {/* ══════════════════ 7. Political Analysis ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<Landmark className="w-5 h-5 text-sacred-gold" />}
          title={T.politicalAnalysis(lang)}
        />

        {loading ? (
          <LoadingSpinner lang={lang} />
        ) : analysisData?.political_analysis ? (
          <div className="flex items-start gap-4">
            <div className="shrink-0">
              {analysisData.political_analysis.stability === 'stable' && (
                <div className="w-12 h-12 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center">
                  <Shield className="w-6 h-6 text-emerald-600" />
                </div>
              )}
              {analysisData.political_analysis.stability === 'unstable' && (
                <div className="w-12 h-12 rounded-full bg-red-50 border border-red-200 flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                </div>
              )}
              {analysisData.political_analysis.stability === 'pressured' && (
                <div className="w-12 h-12 rounded-full bg-amber-50 border border-amber-200 flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-amber-600" />
                </div>
              )}
            </div>
            <div>
              <p className="text-sm font-semibold text-sacred-brown mb-1">
                {analysisData.political_analysis.stability === 'stable' ? T.stable(lang)
                  : analysisData.political_analysis.stability === 'unstable' ? T.unstable(lang)
                  : T.pressured(lang)}
              </p>
              <p className="text-sm text-cosmic-text/70 leading-relaxed">
                {loc(analysisData.political_analysis.description, analysisData.political_analysis.description_hi)}
              </p>
            </div>
          </div>
        ) : (
          <DataUnavailable lang={lang} />
        )}
      </div>

      {/* ══════════════════ 8. Eclipse Tracker ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<Moon className="w-5 h-5 text-sacred-gold" />}
          title={T.eclipseTracker(lang)}
        />

        {/* Year navigation */}
        <div className="flex items-center justify-center gap-4 mb-4">
          <button
            type="button"
            onClick={prevYear}
            className="p-1.5 rounded-lg border border-sacred-gold/30 hover:bg-sacred-gold/10 text-sacred-brown transition-colors"
            aria-label="Previous year"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-sm font-semibold text-sacred-brown min-w-[60px] text-center">
            {selectedYear}
          </span>
          <button
            type="button"
            onClick={nextYear}
            className="p-1.5 rounded-lg border border-sacred-gold/30 hover:bg-sacred-gold/10 text-sacred-brown transition-colors"
            aria-label="Next year"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {loadingEclipse ? (
          <LoadingSpinner lang={lang} />
        ) : eclipseData && eclipseData.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-sacred-gold/10">
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.date(lang)}</th>
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.type(lang)}</th>
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.solarLunar(lang)}</th>
                  <th className="text-center p-2 font-medium text-sacred-gold-dark">{T.affectedHouse(lang)}</th>
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.impact(lang)}</th>
                </tr>
              </thead>
              <tbody>
                {eclipseData.map((e, idx) => (
                  <tr key={idx} className="border-b border-slate-100 hover:bg-slate-50/50">
                    <td className="p-2 font-mono text-xs">{e.date}</td>
                    <td className="p-2">{loc(e.type, e.type_hi)}</td>
                    <td className="p-2">
                      {e.solar_lunar === 'Solar' ? (
                        <span className="inline-flex items-center gap-1"><Sun className="w-3.5 h-3.5 text-amber-500" />{T.solar(lang)}</span>
                      ) : (
                        <span className="inline-flex items-center gap-1"><Moon className="w-3.5 h-3.5 text-slate-500" />{T.lunar(lang)}</span>
                      )}
                    </td>
                    <td className="p-2 text-center">{e.affected_house}</td>
                    <td className="p-2 text-xs text-cosmic-text/70">{loc(e.impact, e.impact_hi)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <DataUnavailable lang={lang} />
        )}
      </div>

      {/* ══════════════════ 9. Ingress / Sankranti Dates ══════════════════ */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <SectionHeader
          icon={<Sun className="w-5 h-5 text-sacred-gold" />}
          title={T.ingressDates(lang)}
        />

        {loadingIngress ? (
          <LoadingSpinner lang={lang} />
        ) : ingressData && ingressData.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-sacred-gold/10">
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.sign(lang)}</th>
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.date(lang)}</th>
                  <th className="text-left p-2 font-medium text-sacred-gold-dark">{T.theme(lang)}</th>
                </tr>
              </thead>
              <tbody>
                {ingressData.map((entry, idx) => (
                  <tr key={idx} className="border-b border-slate-100 hover:bg-slate-50/50">
                    <td className="p-2 font-semibold">{translateSign(entry.sign, lang)}</td>
                    <td className="p-2 font-mono text-xs">{entry.date}</td>
                    <td className="p-2 text-xs text-cosmic-text/70">{loc(entry.theme, entry.theme_hi)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <DataUnavailable lang={lang} />
        )}
      </div>
    </div>
  );
}
