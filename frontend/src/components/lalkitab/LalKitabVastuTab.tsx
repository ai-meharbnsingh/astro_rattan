import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Loader2, Home, AlertTriangle, CheckCircle2, MapPin, Compass } from 'lucide-react';

// ─── Types ───────────────────────────────────────────────────────────────────

interface DirectionEntry {
  house: number;
  direction: { en: string; hi: string };
  zone: { en: string; hi: string };
  planets: string[];
  is_empty: boolean;
}

interface PlanetWarning {
  planet: string;
  house: number;
  direction: { en: string; hi: string };
  zone: { en: string; hi: string };
  warning: { en: string; hi: string };
  fix: { en: string; hi: string };
  is_critical: boolean;
}

interface VastuData {
  directional_map: DirectionEntry[];
  planet_warnings: PlanetWarning[];
  priority_fixes: PlanetWarning[];
  general_layout: { house: number; direction: { en: string; hi: string }; tip: { en: string; hi: string } }[];
  total_warnings: number;
  critical_count: number;
}

interface Props { kundliId?: string; language: string; }

// ─── Constants ────────────────────────────────────────────────────────────────

const PLANET_COLOR: Record<string, string> = {
  Sun: 'text-orange-500', Moon: 'text-blue-400', Mars: 'text-red-500',
  Mercury: 'text-green-600', Jupiter: 'text-yellow-600', Venus: 'text-pink-500',
  Saturn: 'text-gray-600', Rahu: 'text-purple-600', Ketu: 'text-amber-700',
};

const DIRECTION_ICON: Record<string, string> = {
  East: '→', West: '←', North: '↑', South: '↓',
  'South-East': '↘', 'South-West': '↙', 'North-East': '↗', 'North-West': '↖',
};

function getDirectionIcon(dir: string): string {
  for (const [key, icon] of Object.entries(DIRECTION_ICON)) {
    if (dir.startsWith(key)) return icon;
  }
  return '•';
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function LalKitabVastuTab({ kundliId, language }: Props) {
  const hi = language === 'hi';
  const [data, setData] = useState<VastuData | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeSection, setActiveSection] = useState<'warnings' | 'map' | 'layout'>('warnings');

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/lalkitab/vastu/${kundliId}`)
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'वास्तु विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to view Vastu diagnosis.'}
    </div>
  );

  if (loading) return (
    <div className="flex justify-center py-16">
      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
    </div>
  );

  if (!data) return null;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center shrink-0">
          <Home className="w-5 h-5 text-green-700" />
        </div>
        <div>
          <h3 className="font-bold text-foreground text-base">
            {hi ? 'मकान वास्तु — दिशा विश्लेषण' : 'Makaan Vastu — Directional Analysis'}
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            {hi
              ? 'आपके ग्रहों के आधार पर घर की दिशाओं का स्वचालित निदान'
              : 'Auto-generated home direction diagnosis based on your planetary positions'}
          </p>
        </div>
      </div>

      {/* Summary badges */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-red-100 text-red-700">
          <AlertTriangle className="w-3 h-3" />
          {data.critical_count} {hi ? 'गंभीर' : 'critical'}
        </span>
        <span className="flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-yellow-100 text-yellow-700">
          {data.total_warnings} {hi ? 'कुल चेतावनी' : 'warnings'}
        </span>
        <span className="flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-green-100 text-green-700">
          <CheckCircle2 className="w-3 h-3" />
          {12 - data.total_warnings} {hi ? 'सुरक्षित क्षेत्र' : 'clear zones'}
        </span>
      </div>

      {/* Section tabs */}
      <div className="flex gap-1 bg-muted/30 rounded-xl p-1">
        {([
          ['warnings', hi ? 'ग्रह चेतावनी' : 'Planet Warnings'],
          ['map', hi ? 'दिशा मानचित्र' : 'Direction Map'],
          ['layout', hi ? 'सामान्य सुझाव' : 'Layout Tips'],
        ] as const).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setActiveSection(key)}
            className={`flex-1 text-xs font-semibold py-1.5 rounded-lg transition-all ${
              activeSection === key ? 'bg-white shadow text-foreground' : 'text-muted-foreground'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* WARNINGS section */}
      {activeSection === 'warnings' && (
        <div className="space-y-3">
          {data.planet_warnings.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground text-sm">
              <CheckCircle2 className="w-8 h-8 text-green-500 mx-auto mb-2" />
              {hi ? 'कोई गंभीर वास्तु चेतावनी नहीं।' : 'No planet-specific Vastu warnings for this chart.'}
            </div>
          ) : (
            data.planet_warnings.map((w, i) => (
              <div
                key={i}
                className={`rounded-xl p-4 border ${
                  w.is_critical
                    ? 'border-red-200 bg-red-50'
                    : 'border-yellow-200 bg-yellow-50'
                }`}
              >
                <div className="flex items-start gap-2 mb-2">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-sm font-bold shrink-0 ${
                    w.is_critical ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {w.house}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className={`font-bold text-sm ${PLANET_COLOR[w.planet] ?? 'text-foreground'}`}>
                        {w.planet}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {hi ? 'भाव' : 'House'} {w.house}
                      </span>
                      <span className="text-xs font-medium text-foreground">
                        {getDirectionIcon(w.direction.en)} {hi ? w.direction.hi : w.direction.en}
                      </span>
                      {w.is_critical && (
                        <span className="text-xs font-bold text-red-600 uppercase">
                          {hi ? 'गंभीर' : 'Critical'}
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-muted-foreground mt-0.5 capitalize">
                      {hi ? w.zone.hi : w.zone.en}
                    </div>
                  </div>
                </div>
                <p className="text-xs text-foreground/80 mb-2">
                  {hi ? w.warning.hi : w.warning.en}
                </p>
                <div className="bg-white/70 rounded-lg p-2">
                  <div className="text-xs font-semibold text-green-700 mb-1">
                    {hi ? '✓ उपाय:' : '✓ Fix:'}
                  </div>
                  <p className="text-xs text-green-800">{hi ? w.fix.hi : w.fix.en}</p>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* DIRECTION MAP section */}
      {activeSection === 'map' && (
        <div className="space-y-2">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {data.directional_map.map((entry) => (
              <div
                key={entry.house}
                className={`rounded-xl border p-3 ${
                  entry.is_empty
                    ? 'border-border bg-muted/20'
                    : 'border-sacred-gold/20 bg-sacred-gold/5'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-1.5">
                    <span className="w-6 h-6 rounded-md bg-sacred-gold/10 text-sacred-gold text-xs font-bold flex items-center justify-center">
                      {entry.house}
                    </span>
                    <span className="text-xs font-semibold text-foreground">
                      {getDirectionIcon(entry.direction.en)} {hi ? entry.direction.hi : entry.direction.en}
                    </span>
                  </div>
                  {entry.is_empty && (
                    <span className="text-xs text-muted-foreground/60">
                      {hi ? 'खाली' : 'empty'}
                    </span>
                  )}
                </div>
                <div className="text-xs text-muted-foreground mb-1.5">
                  <MapPin className="w-3 h-3 inline mr-0.5" />
                  {hi ? entry.zone.hi : entry.zone.en}
                </div>
                {entry.planets.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {entry.planets.map(p => (
                      <span key={p} className={`text-xs font-semibold ${PLANET_COLOR[p] ?? 'text-foreground'}`}>
                        {p}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* LAYOUT TIPS section */}
      {activeSection === 'layout' && (
        <div className="space-y-2">
          {data.general_layout.map((item) => (
            <div key={item.house} className="flex gap-3 p-3 rounded-xl border border-border bg-card">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-muted text-xs font-bold text-foreground shrink-0">
                {item.house}
              </div>
              <div>
                <div className="flex items-center gap-1 text-xs font-semibold text-foreground mb-0.5">
                  <Compass className="w-3 h-3" />
                  {getDirectionIcon(item.direction.en)} {hi ? item.direction.hi : item.direction.en}
                </div>
                <p className="text-xs text-muted-foreground">{hi ? item.tip.hi : item.tip.en}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
