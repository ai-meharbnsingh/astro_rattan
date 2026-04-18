import { useState, useEffect } from 'react';
import { Loader2, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface InterpretationCategory {
  en: string;
  hi: string;
}

interface PlanetInterpretation {
  planet: string;
  house: number;
  interpretation: {
    general: InterpretationCategory;
    love: InterpretationCategory;
    career: InterpretationCategory;
    finance: InterpretationCategory;
    health: InterpretationCategory;
  };
}

interface TransitInterpretationsData {
  interpretations: PlanetInterpretation[];
}

interface Props {
  kundliId: string;
  language?: string;
}

const CATEGORY_LABELS: Record<string, { en: string; hi: string; emoji: string; color: string }> = {
  love: { en: 'Love & Relationships', hi: 'प्रेम व संबंध', emoji: '❤️', color: 'text-pink-600' },
  career: { en: 'Career & Work', hi: 'करियर व कार्य', emoji: '💼', color: 'text-blue-600' },
  finance: { en: 'Finance & Wealth', hi: 'धन व वित्त', emoji: '💰', color: 'text-amber-600' },
  health: { en: 'Health & Vitality', hi: 'स्वास्थ्य व जीवनशक्ति', emoji: '🌿', color: 'text-emerald-600' },
};

const PLANET_ICONS: Record<string, string> = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋',
};

function PlanetCard({
  item,
  isHi,
}: {
  item: PlanetInterpretation;
  isHi: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const interp = item.interpretation ?? {};
  const general = interp.general;
  const categories = (['love', 'career', 'finance', 'health'] as const).filter(
    k => interp[k]?.en || interp[k]?.hi
  );

  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-white/50 overflow-hidden">
      {/* Planet header */}
      <div className="p-4 bg-gradient-to-r from-[#FFF9F5] to-white border-b border-sacred-gold/10">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-sacred-gold/15 flex items-center justify-center text-xl font-bold text-sacred-gold-dark">
              {PLANET_ICONS[item.planet] ?? item.planet?.charAt(0)}
            </div>
            <div>
              <p className="font-bold text-foreground text-base">{item.planet ?? '—'}</p>
              {item.house > 0 && (
                <p className="text-xs text-muted-foreground">
                  {isHi ? `भाव ${item.house}` : `House ${item.house}`}
                </p>
              )}
            </div>
          </div>
          {categories.length > 0 && (
            <button
              onClick={() => setExpanded(prev => !prev)}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-sacred-gold/10 border border-sacred-gold/30 text-sacred-gold-dark text-xs font-medium hover:bg-sacred-gold/20 transition-colors"
              aria-expanded={expanded}
            >
              {expanded
                ? (isHi ? 'कम करें' : 'Less')
                : (isHi ? 'विस्तार' : 'More')}
              {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          )}
        </div>
      </div>

      {/* General interpretation — always visible */}
      {general && (
        <div className="p-4">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
            {isHi ? 'सामान्य फल' : 'General Interpretation'}
          </p>
          <p className="text-sm text-foreground/90 leading-relaxed">
            {isHi ? (general.hi || general.en) : general.en}
          </p>
          {!isHi && general.hi && (
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{general.hi}</p>
          )}
          {isHi && general.en && (
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{general.en}</p>
          )}
        </div>
      )}

      {/* Expandable sub-sections */}
      {expanded && categories.length > 0 && (
        <div className="border-t border-sacred-gold/10 divide-y divide-sacred-gold/10">
          {categories.map(key => {
            const cat = CATEGORY_LABELS[key];
            const catData = interp[key];
            return (
              <div key={key} className="p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-base">{cat.emoji}</span>
                  <span className={`text-xs font-semibold ${cat.color}`}>
                    {isHi ? cat.hi : cat.en}
                  </span>
                </div>
                <p className="text-sm text-foreground/80 leading-relaxed">
                  {isHi ? (catData?.hi || catData?.en) : catData?.en}
                </p>
                {!isHi && catData?.hi && (
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{catData.hi}</p>
                )}
                {isHi && catData?.en && (
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{catData.en}</p>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default function TransitInterpretationsTab({ kundliId, language }: Props) {
  const [data, setData] = useState<TransitInterpretationsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api.get<TransitInterpretationsData>(`/api/kundli/${kundliId}/transit-interpretations`)
      .then(res => { if (!cancelled) setData(res); })
      .catch((err: any) => { if (!cancelled) setError(err?.message || 'Failed to load Transit Interpretations'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
        {error}
      </div>
    );
  }

  if (!data) return null;

  const interpretations = data.interpretations ?? [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <BookOpen className="w-6 h-6" />
          {isHi ? 'गोचर व्याख्या' : 'Transit Interpretations'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi
            ? 'प्रत्येक गोचर ग्रह का प्रेम, करियर, धन व स्वास्थ्य पर प्रभाव'
            : 'Effect of each transiting planet on love, career, finance & health'}
        </p>
      </div>

      {interpretations.length === 0 ? (
        <div className="p-8 rounded-xl border border-sacred-gold/20 bg-white/50 text-center">
          <BookOpen className="w-10 h-10 text-sacred-gold/40 mx-auto mb-3" />
          <p className="text-sm text-muted-foreground">
            {isHi ? 'कोई गोचर व्याख्या उपलब्ध नहीं' : 'No transit interpretations available'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {interpretations.map((item, i) => (
            <PlanetCard key={i} item={item} isHi={isHi} />
          ))}
        </div>
      )}

      {/* Legend */}
      <div className="p-4 rounded-lg bg-sacred-gold/5 border border-sacred-gold/20 text-xs text-muted-foreground">
        <div className="flex flex-wrap gap-4">
          {Object.entries(CATEGORY_LABELS).map(([, cat]) => (
            <span key={cat.en} className="flex items-center gap-1">
              <span>{cat.emoji}</span>
              <span className="text-foreground/70">{isHi ? cat.hi : cat.en}</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
