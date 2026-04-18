import { useState, useEffect } from 'react';
import { Loader2, Link2, BookOpen, Info } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface GrahaRelationship {
  planet_a: string;
  planet_b: string;
  relationship_type_en: string;
  relationship_type_hi?: string;
  effect_en: string;
  effect_hi?: string;
  strength?: 'strong' | 'moderate' | 'weak' | string;
}

interface GrahaSambandhaData {
  kundli_id?: string;
  person_name?: string;
  relationships: GrahaRelationship[];
  summary_en?: string;
  summary_hi?: string;
  sloka_ref?: string;
}

interface Props {
  kundliId: string;
  language?: string;
}

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'बृहस्पति', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const STRENGTH_STYLE: Record<string, { badge: string; label: string; labelHi: string }> = {
  strong:   { badge: 'bg-emerald-100 text-emerald-800 border-emerald-200', label: 'Strong',   labelHi: 'बलवान' },
  moderate: { badge: 'bg-amber-100 text-amber-800 border-amber-200',       label: 'Moderate', labelHi: 'मध्यम' },
  weak:     { badge: 'bg-red-100 text-red-800 border-red-200',             label: 'Weak',     labelHi: 'निर्बल' },
};

const REL_TYPE_COLOR: Record<string, string> = {
  conjunction:  'bg-orange-100 text-orange-800 border-orange-200',
  aspect:       'bg-blue-100 text-blue-800 border-blue-200',
  exchange:     'bg-purple-100 text-purple-800 border-purple-200',
  mutual:       'bg-pink-100 text-pink-800 border-pink-200',
  opposition:   'bg-red-100 text-red-800 border-red-200',
  trine:        'bg-green-100 text-green-800 border-green-200',
  default:      'bg-sacred-gold/10 text-sacred-brown border-sacred-gold/20',
};

function relTypeColor(type: string): string {
  const lower = type.toLowerCase();
  for (const key of Object.keys(REL_TYPE_COLOR)) {
    if (lower.includes(key)) return REL_TYPE_COLOR[key];
  }
  return REL_TYPE_COLOR.default;
}

// Group relationships by type
function groupByType(relationships: GrahaRelationship[]): Record<string, GrahaRelationship[]> {
  const groups: Record<string, GrahaRelationship[]> = {};
  for (const rel of relationships) {
    const key = rel.relationship_type_en || 'Other';
    if (!groups[key]) groups[key] = [];
    groups[key].push(rel);
  }
  return groups;
}

export default function GrahaSambandhaTab({ kundliId, language }: Props) {
  const [data, setData] = useState<GrahaSambandhaData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    (async () => {
      try {
        const res = await api.get(`/api/kundli/${kundliId}/graha-sambandha`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Graha Sambandha');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
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

  const planetName = (p: string) => hi ? (PLANET_HI[p] || p) : p;
  const groups = groupByType(data.relationships || []);
  const groupKeys = Object.keys(groups);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Link2 className="w-6 h-6" />
          {hi ? 'ग्रह सम्बन्ध' : 'Graha Sambandha'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'कुंडली में ग्रहों के परस्पर सम्बन्ध एवं प्रभाव'
            : 'Planetary relationships and mutual influences in the chart'}
        </p>
      </div>

      {/* Summary */}
      {(data.summary_en || data.summary_hi) && (
        <div className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 px-4 py-3 flex items-start gap-2">
          <Info className="w-4 h-4 text-sacred-gold-dark shrink-0 mt-0.5" />
          <p className="text-sm text-foreground/85 leading-relaxed">
            {hi ? (data.summary_hi || data.summary_en) : data.summary_en}
          </p>
        </div>
      )}

      {/* Grouped relationship sections */}
      {groupKeys.length > 0 ? (
        <div className="space-y-6">
          {groupKeys.map(typeKey => {
            const rels = groups[typeKey];
            const firstRel = rels[0];
            const typeLabel = hi
              ? (firstRel.relationship_type_hi || typeKey)
              : typeKey;
            const colorClass = relTypeColor(typeKey);

            return (
              <section key={typeKey}>
                {/* Section heading */}
                <div className="flex items-center gap-2 mb-3">
                  <span className={`text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full border ${colorClass}`}>
                    {typeLabel}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    ({rels.length})
                  </span>
                </div>

                {/* Relationship cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {rels.map((rel, idx) => {
                    const strengthStyle = rel.strength
                      ? (STRENGTH_STYLE[rel.strength] || STRENGTH_STYLE.moderate)
                      : null;
                    const effect = hi ? (rel.effect_hi || rel.effect_en) : rel.effect_en;

                    return (
                      <div
                        key={idx}
                        className="rounded-xl border border-sacred-gold/20 bg-white/50 p-4 space-y-2"
                      >
                        {/* Planet pair header */}
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-bold text-sacred-brown text-sm">
                            {planetName(rel.planet_a)}
                          </span>
                          <Link2 className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                          <span className="font-bold text-sacred-brown text-sm">
                            {planetName(rel.planet_b)}
                          </span>
                          {strengthStyle && (
                            <span className={`ml-auto text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded border ${strengthStyle.badge}`}>
                              {hi ? strengthStyle.labelHi : strengthStyle.label}
                            </span>
                          )}
                        </div>

                        {/* Effect description */}
                        {effect && (
                          <p className="text-xs text-foreground/80 leading-relaxed">{effect}</p>
                        )}
                      </div>
                    );
                  })}
                </div>
              </section>
            );
          })}
        </div>
      ) : (
        <div className="p-6 text-center text-muted-foreground text-sm italic">
          {hi ? 'ग्रह सम्बन्ध डेटा उपलब्ध नहीं।' : 'No planetary relationship data available.'}
        </div>
      )}

      {/* Footer sloka ref */}
      {data.sloka_ref && (
        <div className="flex items-center gap-2 pt-2 border-t border-sacred-gold/20 text-[11px] text-muted-foreground italic">
          <BookOpen className="w-3 h-3 text-sacred-gold-dark shrink-0" />
          <span>{data.sloka_ref}</span>
        </div>
      )}
    </div>
  );
}
