import { useState, useEffect, useCallback } from 'react';
import { Loader2, Map, ChevronDown, ChevronUp, Briefcase, Heart, Activity } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

// Backend shape: city_analysis is a dict { cityName: { ascendant, planet_houses, strengths, cautions, overall_score } }
// best_cities is { career: [[name,score,reason],...], relationships: [...], wealth: [...], health: [...], spiritual: [...] }
interface CityDetail {
  city: string;
  ascendant?: { sign: string; degree: number };
  planet_houses?: Record<string, { house: number; sign: string; longitude: number }>;
  strengths: string[];
  cautions: string[];
  overall_score: number;
}

interface AstroMapData {
  city_analysis: Record<string, Omit<CityDetail, 'city'>>;
  best_cities: Record<string, [string, number, string][]>;
  planetary_lines?: unknown;
}

interface Props {
  kundliId: string;
  kundliData?: any;
  language?: string;
}

type LifeArea = 'career' | 'love' | 'health';

// Frontend area → backend key mapping
const AREA_KEY: Record<LifeArea, string> = {
  career: 'career',
  love: 'relationships',
  health: 'health',
};

const AREA_CONFIG: Record<LifeArea, { label_en: string; label_hi: string; icon: React.ElementType; color: string; bg: string; border: string }> = {
  career: {
    label_en: 'Career', label_hi: 'करियर',
    icon: Briefcase,
    color: 'text-blue-700', bg: 'bg-blue-50', border: 'border-blue-200',
  },
  love: {
    label_en: 'Love & Relationships', label_hi: 'प्रेम व संबंध',
    icon: Heart,
    color: 'text-pink-700', bg: 'bg-pink-50', border: 'border-pink-200',
  },
  health: {
    label_en: 'Health', label_hi: 'स्वास्थ्य',
    icon: Activity,
    color: 'text-emerald-700', bg: 'bg-emerald-50', border: 'border-emerald-200',
  },
};

function ScoreBadge({ score }: { score: number }) {
  const pct = Math.min(Math.max(Math.round(score), 0), 100);
  const color =
    pct >= 75 ? 'bg-emerald-100 border-emerald-300 text-emerald-800' :
    pct >= 50 ? 'bg-amber-100 border-amber-300 text-amber-800' :
                'bg-red-100 border-red-300 text-red-700';
  return (
    <span className={`inline-flex px-2 py-0.5 rounded-full border text-xs font-bold ${color}`}>
      {pct}
    </span>
  );
}

function CityRow({ city, isHi, defaultOpen }: { city: CityDetail; isHi: boolean; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen ?? false);

  return (
    <div className="border-b border-sacred-gold/10 last:border-0">
      <button
        onClick={() => setOpen(prev => !prev)}
        className="w-full flex items-center justify-between gap-3 px-4 py-3 hover:bg-sacred-gold/[0.03] transition-colors text-left"
      >
        <span className="font-semibold text-foreground text-sm">{city.city}</span>
        <div className="flex items-center gap-2 shrink-0">
          <ScoreBadge score={city.overall_score} />
          {open ? <ChevronUp className="w-4 h-4 text-muted-foreground" /> : <ChevronDown className="w-4 h-4 text-muted-foreground" />}
        </div>
      </button>

      {open && (
        <div className="px-4 pb-4 space-y-3">
          {/* Score bar */}
          <div>
            <div className="flex items-center justify-between text-[10px] text-muted-foreground mb-1">
              <span>{isHi ? 'स्कोर' : 'Score'}</span>
              <span>{Math.round(city.overall_score)}/100</span>
            </div>
            <div className="w-full h-2 rounded-full bg-gray-200 overflow-hidden">
              <div
                className={`h-full transition-all ${
                  city.overall_score >= 75 ? 'bg-emerald-500' :
                  city.overall_score >= 50 ? 'bg-amber-400' : 'bg-red-400'
                }`}
                style={{ width: `${Math.min(city.overall_score, 100)}%` }}
              />
            </div>
          </div>

          {/* Strengths */}
          {(city.strengths?.length ?? 0) > 0 && (
            <div>
              <p className="text-[10px] font-semibold text-emerald-700 uppercase tracking-wide mb-1">
                {isHi ? 'शक्ति' : 'Strengths'}
              </p>
              <ul className="space-y-1">
                {city.strengths.map((s, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-xs text-foreground/80">
                    <span className="text-emerald-500 mt-0.5">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Cautions */}
          {(city.cautions?.length ?? 0) > 0 && (
            <div>
              <p className="text-[10px] font-semibold text-amber-700 uppercase tracking-wide mb-1">
                {isHi ? 'सावधानी' : 'Cautions'}
              </p>
              <ul className="space-y-1">
                {city.cautions.map((c, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-xs text-foreground/80">
                    <span className="text-amber-500 mt-0.5">⚠</span>
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Planet houses */}
          {city.planet_houses && Object.keys(city.planet_houses).length > 0 && (
            <div>
              <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                {isHi ? 'ग्रह-भाव स्थान' : 'House Placements'}
              </p>
              <div className="flex flex-wrap gap-1.5">
                {Object.entries(city.planet_houses).map(([planet, info]) => (
                  <span
                    key={planet}
                    className="px-2 py-0.5 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 text-sacred-gold-dark text-[10px] font-medium"
                  >
                    {planet}: H{info.house}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Ascendant */}
          {city.ascendant && (
            <p className="text-[10px] text-muted-foreground">
              {isHi ? 'लग्न:' : 'Ascendant:'} {city.ascendant.sign} ({city.ascendant.degree?.toFixed(1)}°)
            </p>
          )}
        </div>
      )}
    </div>
  );
}

type SortKey = 'score' | 'city';

export default function AstroMapTab({ kundliId, kundliData, language }: Props) {
  const [data, setData] = useState<AstroMapData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeArea, setActiveArea] = useState<LifeArea>('career');
  const [sortKey, setSortKey] = useState<SortKey>('score');
  const [sortAsc, setSortAsc] = useState(false);
  const isHi = language === 'hi';

  const fetchData = useCallback(() => {
    if (!kundliData) return;
    const planets = kundliData.chart_data?.planets ?? kundliData.planets ?? {};
    const longitudes: Record<string, number> = {};
    Object.entries(planets).forEach(([name, info]: [string, any]) => {
      if (info?.longitude !== undefined) longitudes[name] = info.longitude;
    });

    setLoading(true);
    setError(null);
    api.post<AstroMapData>('/api/astro-map', {
      birth_date: kundliData.birth_date,
      birth_time: kundliData.birth_time ?? '12:00:00',
      tz_offset: kundliData.timezone_offset ?? 5.5,
      planet_longitudes: longitudes,
    })
      .then(res => setData(res))
      .catch((err: any) => setError(err?.message || 'Failed to load Astro Map'))
      .finally(() => setLoading(false));
  }, [kundliData]);

  useEffect(() => { fetchData(); }, [fetchData]);

  if (!kundliData) {
    return (
      <div className="p-6 rounded-xl border border-amber-200 bg-amber-50/40 text-center">
        <Map className="w-10 h-10 text-amber-400 mx-auto mb-3" />
        <p className="text-sm text-amber-800 font-medium">
          {isHi ? 'कुंडली डेटा उपलब्ध नहीं' : 'Kundli data not available — cannot load Astro Map'}
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-3">
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
        <button
          onClick={fetchData}
          className="px-4 py-2 rounded-lg bg-sacred-gold/10 border border-sacred-gold/30 text-sacred-gold-dark text-sm font-medium hover:bg-sacred-gold/20 transition-colors"
        >
          {isHi ? 'पुनः प्रयास करें' : 'Retry'}
        </button>
      </div>
    );
  }

  if (!data) return null;

  // city_analysis is a dict { cityName: {...} } — convert to array
  const cityArray: CityDetail[] = Object.entries(data.city_analysis ?? {}).map(([name, d]) => ({
    city: name,
    ...d,
  }));

  const sortedCities = [...cityArray].sort((a, b) => {
    if (sortKey === 'score') {
      return sortAsc ? (a.overall_score ?? 0) - (b.overall_score ?? 0) : (b.overall_score ?? 0) - (a.overall_score ?? 0);
    }
    return sortAsc ? a.city.localeCompare(b.city) : b.city.localeCompare(a.city);
  });

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) setSortAsc(prev => !prev);
    else { setSortKey(key); setSortAsc(key === 'city'); }
  };

  // best_cities entries are tuples [name, score, reason]
  const bestCities = data.best_cities ?? {};
  const getAreaCities = (area: LifeArea): [string, number, string][] => {
    const key = AREA_KEY[area];
    const raw = bestCities[key];
    return Array.isArray(raw) ? raw : [];
  };

  const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
  const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';

  return (
    <div className="space-y-4">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Map className="w-6 h-6" />
          {isHi ? 'एस्ट्रो मैप — भौगोलिक ज्योतिष' : 'Astro Map — Geographic Astrology'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi
            ? 'जन्म कुंडली के ग्रहों की स्थिति के आधार पर विश्व के सर्वश्रेष्ठ स्थानों का विश्लेषण'
            : 'Best world locations based on planetary positions in your birth chart'}
        </p>
      </div>

      {/* Best Cities by Life Area */}
      <div>
        <h3 className="text-sm font-semibold text-foreground mb-3">
          {isHi ? 'जीवन क्षेत्र अनुसार सर्वश्रेष्ठ शहर' : 'Best Cities by Life Area'}
        </h3>

        {/* Area tabs */}
        <div className="flex gap-2 mb-4 flex-wrap">
          {(Object.keys(AREA_CONFIG) as LifeArea[]).map(area => {
            const cfg = AREA_CONFIG[area];
            const IconComp = cfg.icon;
            const isActive = activeArea === area;
            return (
              <button
                key={area}
                onClick={() => setActiveArea(area)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors ${
                  isActive
                    ? `${cfg.bg} ${cfg.border} ${cfg.color}`
                    : 'bg-white border-sacred-gold/20 text-muted-foreground hover:bg-sacred-gold/5'
                }`}
              >
                <IconComp className="w-3.5 h-3.5" />
                {isHi ? cfg.label_hi : cfg.label_en}
              </button>
            );
          })}
        </div>

        {/* Top 3 cities for active area */}
        <div className={`p-4 rounded-xl border ${AREA_CONFIG[activeArea].border} ${AREA_CONFIG[activeArea].bg}`}>
          {getAreaCities(activeArea).length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-2">
              {isHi ? 'कोई शहर उपलब्ध नहीं' : 'No cities available'}
            </p>
          ) : (
            <div className="space-y-2">
              {getAreaCities(activeArea).slice(0, 3).map(([cityName, score, reason], i) => (
                <div key={i} className="flex items-start gap-3">
                  <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                    i === 0 ? 'bg-amber-400 text-white' :
                    i === 1 ? 'bg-gray-300 text-gray-800' :
                               'bg-orange-300 text-white'
                  }`}>
                    {i + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-semibold ${AREA_CONFIG[activeArea].color}`}>{cityName}</span>
                      <ScoreBadge score={score * 10} />
                    </div>
                    {reason && <p className="text-[11px] text-muted-foreground mt-0.5 leading-relaxed">{reason}</p>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* All cities sortable list */}
      {sortedCities.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-foreground">
              {isHi ? `सभी शहर (${sortedCities.length})` : `All Cities (${sortedCities.length})`}
            </h3>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <span>{isHi ? 'क्रमबद्ध:' : 'Sort by:'}</span>
              <button
                onClick={() => toggleSort('score')}
                className={`px-2 py-1 rounded border text-xs ${sortKey === 'score' ? 'border-sacred-gold/40 bg-sacred-gold/10 text-sacred-gold-dark font-semibold' : 'border-gray-200 hover:border-sacred-gold/20'}`}
              >
                {isHi ? 'स्कोर' : 'Score'} {sortKey === 'score' ? (sortAsc ? '↑' : '↓') : ''}
              </button>
              <button
                onClick={() => toggleSort('city')}
                className={`px-2 py-1 rounded border text-xs ${sortKey === 'city' ? 'border-sacred-gold/40 bg-sacred-gold/10 text-sacred-gold-dark font-semibold' : 'border-gray-200 hover:border-sacred-gold/20'}`}
              >
                {isHi ? 'शहर' : 'City'} {sortKey === 'city' ? (sortAsc ? '↑' : '↓') : ''}
              </button>
            </div>
          </div>

          <div className={ohContainer}>
            {sortedCities.map((city, i) => (
              <CityRow key={`${city.city}-${i}`} city={city} isHi={isHi} defaultOpen={i === 0} />
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="p-4 rounded-lg bg-sacred-gold/5 border border-sacred-gold/20 text-xs text-muted-foreground flex items-start gap-2">
        <Map className="w-4 h-4 text-sacred-gold-dark shrink-0 mt-0.5" />
        <span>
          {isHi
            ? 'एस्ट्रोकार्टोग्राफी — जन्म कुंडली के ग्रहों के संचरण के आधार पर भौगोलिक ऊर्जा मानचित्र'
            : 'Astrocartography — geographic energy map based on planetary crossings from your natal chart'}
        </span>
      </div>
    </div>
  );
}
