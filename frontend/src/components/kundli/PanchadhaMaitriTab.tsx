import { useState, useEffect } from 'react';
import { Loader2, Users, BookOpen, Info } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface PanchadhaMaitri {
  planet_a: string;
  planet_b: string;
  natural_relation: string;
  temporary_relation: string;
  combined_relation_en: string;
  combined_relation_hi?: string;
  effect_en: string;
  effect_hi?: string;
}

interface PanchadhaMaitriData {
  kundli_id?: string;
  person_name?: string;
  friendships: PanchadhaMaitri[];
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

// Style for combined relationship quality
const COMBINED_STYLE: Record<string, { row: string; badge: string }> = {
  'great friend':   { row: 'bg-emerald-50 border-emerald-200',   badge: 'bg-emerald-600 text-white' },
  'friend':         { row: 'bg-green-50 border-green-200',        badge: 'bg-green-600 text-white' },
  'neutral':        { row: 'bg-gray-50 border-gray-200',          badge: 'bg-gray-400 text-white' },
  'enemy':          { row: 'bg-red-50 border-red-200',            badge: 'bg-red-600 text-white' },
  'great enemy':    { row: 'bg-red-100 border-red-300',           badge: 'bg-red-800 text-white' },
};

function combinedStyle(combined: string): { row: string; badge: string } {
  const lower = combined.toLowerCase();
  for (const key of Object.keys(COMBINED_STYLE)) {
    if (lower.includes(key)) return COMBINED_STYLE[key];
  }
  return { row: 'bg-white border-sacred-gold/20', badge: 'bg-sacred-gold-dark text-white' };
}

const RELATION_BADGE: Record<string, string> = {
  friend:   'bg-green-100 text-green-800',
  neutral:  'bg-gray-100 text-gray-700',
  enemy:    'bg-red-100 text-red-800',
};

function relationBadge(rel: string): string {
  const lower = rel.toLowerCase();
  if (lower.includes('friend')) return RELATION_BADGE.friend;
  if (lower.includes('enemy')) return RELATION_BADGE.enemy;
  return RELATION_BADGE.neutral;
}

export default function PanchadhaMaitriTab({ kundliId, language }: Props) {
  const [data, setData] = useState<PanchadhaMaitriData | null>(null);
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
        const res = await api.get(`/api/kundli/${kundliId}/panchadha-maitri`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Panchadha Maitri');
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
  const friendships = data.friendships || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Users className="w-6 h-6" />
          {hi ? 'पंचधा मैत्री' : 'Panchadha Maitri'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'नैसर्गिक, तात्कालिक एवं पांचधा सम्मिश्रित मित्रता-विश्लेषण'
            : 'Natural, temporary, and five-fold combined planetary friendship analysis'}
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

      {/* Legend */}
      <div className="flex flex-wrap gap-3 text-xs">
        <div className="flex items-center gap-1.5 font-medium text-muted-foreground uppercase tracking-wide">
          {hi ? 'संयुक्त सम्बन्ध:' : 'Combined:'}
        </div>
        {[
          { label: hi ? 'महामित्र' : 'Great Friend', style: 'bg-emerald-100 text-emerald-800' },
          { label: hi ? 'मित्र' : 'Friend',          style: 'bg-green-100 text-green-800' },
          { label: hi ? 'सम' : 'Neutral',            style: 'bg-gray-100 text-gray-700' },
          { label: hi ? 'शत्रु' : 'Enemy',           style: 'bg-red-100 text-red-800' },
          { label: hi ? 'महाशत्रु' : 'Great Enemy',  style: 'bg-red-200 text-red-900' },
        ].map(item => (
          <span key={item.label} className={`px-2 py-0.5 rounded-full ${item.style}`}>
            {item.label}
          </span>
        ))}
      </div>

      {/* Table (desktop) / cards (mobile) */}
      {friendships.length > 0 ? (
        <>
          {/* Desktop table */}
          <div className="hidden md:block rounded-xl border border-sacred-gold/20 overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-sacred-gold/10 text-sacred-brown">
                  <th className="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wide">
                    {hi ? 'ग्रह A' : 'Planet A'}
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wide">
                    {hi ? 'ग्रह B' : 'Planet B'}
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wide">
                    {hi ? 'नैसर्गिक' : 'Natural'}
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wide">
                    {hi ? 'तात्कालिक' : 'Temporary'}
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wide">
                    {hi ? 'पंचधा' : 'Combined'}
                  </th>
                  <th className="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wide">
                    {hi ? 'प्रभाव' : 'Effect'}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-sacred-gold/10">
                {friendships.map((f, idx) => {
                  const cs = combinedStyle(f.combined_relation_en || '');
                  const combinedLabel = hi
                    ? (f.combined_relation_hi || f.combined_relation_en)
                    : f.combined_relation_en;
                  const effect = hi ? (f.effect_hi || f.effect_en) : f.effect_en;
                  return (
                    <tr key={idx} className={`border-l-2 ${cs.row}`}>
                      <td className="px-4 py-3 font-semibold text-sacred-brown">
                        {planetName(f.planet_a)}
                      </td>
                      <td className="px-4 py-3 font-semibold text-sacred-brown">
                        {planetName(f.planet_b)}
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${relationBadge(f.natural_relation)}`}>
                          {f.natural_relation || '—'}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${relationBadge(f.temporary_relation)}`}>
                          {f.temporary_relation || '—'}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${cs.badge}`}>
                          {combinedLabel || '—'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-xs text-foreground/75 leading-relaxed max-w-xs">
                        {effect || '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Mobile cards */}
          <div className="md:hidden space-y-3">
            {friendships.map((f, idx) => {
              const cs = combinedStyle(f.combined_relation_en || '');
              const combinedLabel = hi ? (f.combined_relation_hi || f.combined_relation_en) : f.combined_relation_en;
              const effect = hi ? (f.effect_hi || f.effect_en) : f.effect_en;
              return (
                <div key={idx} className={`rounded-xl border-2 p-4 space-y-2 ${cs.row}`}>
                  {/* Planet pair */}
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sacred-brown">
                      {planetName(f.planet_a)} × {planetName(f.planet_b)}
                    </span>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded ${cs.badge}`}>
                      {combinedLabel}
                    </span>
                  </div>
                  {/* Relation row */}
                  <div className="flex gap-2 flex-wrap text-xs">
                    <span className="text-muted-foreground">{hi ? 'नैसर्गिक:' : 'Natural:'}</span>
                    <span className={`px-1.5 py-0.5 rounded font-medium ${relationBadge(f.natural_relation)}`}>
                      {f.natural_relation || '—'}
                    </span>
                    <span className="text-muted-foreground">{hi ? 'तात्कालिक:' : 'Temp:'}</span>
                    <span className={`px-1.5 py-0.5 rounded font-medium ${relationBadge(f.temporary_relation)}`}>
                      {f.temporary_relation || '—'}
                    </span>
                  </div>
                  {effect && (
                    <p className="text-xs text-foreground/75 leading-relaxed">{effect}</p>
                  )}
                </div>
              );
            })}
          </div>
        </>
      ) : (
        <div className="p-6 text-center text-muted-foreground text-sm italic">
          {hi ? 'पंचधा मैत्री डेटा उपलब्ध नहीं।' : 'No Panchadha Maitri data available.'}
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
