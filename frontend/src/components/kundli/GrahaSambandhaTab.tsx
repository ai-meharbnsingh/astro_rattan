import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { Loader2, Link2, BookOpen, Info } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface GrahaRelationship {
  planet_a: string;
  planet_b: string;
  house_a?: number;
  house_b?: number;
  relationship_type_en: string;
  relationship_type_hi?: string;
  effect_en: string;
  effect_hi?: string;
  strength?: string;
  sloka_ref?: string;
}

interface GrahaSambandhaData {
  kundli_id?: string;
  person_name?: string;
  relationships: GrahaRelationship[];
  count?: number;
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

const SEV: Record<string, string> = {
  strong:   'bg-emerald-100 text-emerald-800',
  moderate: 'bg-amber-100 text-amber-800',
  weak:     'bg-red-100 text-red-800',
};

const REL_COLOR: Record<string, string> = {
  conjunction: 'bg-orange-100 text-orange-800',
  aspect:      'bg-blue-100 text-blue-800',
  exchange:    'bg-purple-100 text-purple-800',
  mutual:      'bg-pink-100 text-pink-800',
  opposition:  'bg-red-100 text-red-800',
  trine:       'bg-green-100 text-green-800',
};

function relColor(type: string): string {
  const lower = type.toLowerCase();
  for (const key of Object.keys(REL_COLOR)) {
    if (lower.includes(key)) return REL_COLOR[key];
  }
  return 'bg-sacred-gold/10 text-sacred-gold-dark';
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdWrapCls   = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

export default function GrahaSambandhaTab({ kundliId, language }: Props) {
  const { t } = useTranslation();
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
        if (!cancelled) setData(res as GrahaSambandhaData);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || t('auto.genericError'));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
    );
  }

  if (!data) return null;

  const pName = (p: string) => hi ? (PLANET_HI[p] || p) : p;
  const rels  = data.relationships ?? [];

  return (
    <div className="space-y-4">

      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Link2 className="w-6 h-6" />
          {hi ? 'ग्रह सम्बन्ध' : 'Graha Sambandha'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi ? 'ग्रहों के परस्पर सम्बन्ध एवं प्रभाव' : 'Planetary relationships and mutual influences'}
        </p>
      </div>

      {/* Summary */}
      {(data.summary_en || data.summary_hi) && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Info className="w-4 h-4" />
            <span>{hi ? 'सारांश' : 'Summary'}</span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed">
              {hi ? (data.summary_hi || data.summary_en) : data.summary_en}
            </p>
          </div>
        </div>
      )}

      {/* Relationships Table */}
      {rels.length > 0 ? (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Link2 className="w-4 h-4" />
            <span>{hi ? 'सम्बन्ध विश्लेषण' : 'Relationship Analysis'}</span>
            <span className="ml-auto text-[12px] font-normal opacity-80">{rels.length}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '18%' }} />
              <col style={{ width: '8%' }} />
              <col style={{ width: '16%' }} />
              <col style={{ width: '10%' }} />
              <col style={{ width: '48%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{hi ? 'ग्रह युग्म' : 'Planet Pair'}</th>
                <th className={thCls}>{hi ? 'भाव' : 'Houses'}</th>
                <th className={thCls}>{hi ? 'सम्बन्ध' : 'Type'}</th>
                <th className={thCls}>{hi ? 'बल' : 'Strength'}</th>
                <th className={thCls}>{hi ? 'फल' : 'Effect'}</th>
              </tr>
            </thead>
            <tbody>
              {rels.map((rel, i) => {
                const effect  = hi ? (rel.effect_hi || rel.effect_en) : rel.effect_en;
                const relType = hi ? (rel.relationship_type_hi || rel.relationship_type_en) : rel.relationship_type_en;
                const sev     = rel.strength?.toLowerCase() ?? 'moderate';
                return (
                  <tr key={i}>
                    <td className={`${tdCls} font-semibold`}>
                      <span className="text-foreground">{pName(rel.planet_a)}</span>
                      <span className="text-muted-foreground mx-0.5">↔</span>
                      <span className="text-foreground">{pName(rel.planet_b)}</span>
                    </td>
                    <td className={tdCls}>
                      {rel.house_a && rel.house_b
                        ? <span className="text-muted-foreground">{rel.house_a}↔{rel.house_b}</span>
                        : <span className="text-muted-foreground">—</span>}
                    </td>
                    <td className={tdWrapCls}>
                      <span className={`inline-block text-[10px] font-semibold px-1.5 py-0.5 rounded ${relColor(rel.relationship_type_en)}`}>
                        {relType}
                      </span>
                    </td>
                    <td className={tdCls}>
                      {rel.strength ? (
                        <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${SEV[sev] ?? SEV.moderate}`}>
                          {hi
                            ? sev === 'strong' ? 'बलवान' : sev === 'weak' ? 'निर्बल' : 'मध्यम'
                            : sev.charAt(0).toUpperCase() + sev.slice(1)}
                        </span>
                      ) : <span className="text-muted-foreground">—</span>}
                    </td>
                    <td className={tdWrapCls}>
                      <p>{effect || '—'}</p>
                      {rel.sloka_ref && (
                        <div className="flex items-center gap-1 mt-1 text-[10px] text-muted-foreground italic">
                          <BookOpen className="w-2.5 h-2.5 shrink-0" />
                          <span>{rel.sloka_ref}</span>
                        </div>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="p-6 text-center text-muted-foreground text-sm italic">
          {hi ? 'ग्रह सम्बन्ध डेटा उपलब्ध नहीं।' : 'No planetary relationship data available.'}
        </div>
      )}

      {/* Footer */}
      {data.sloka_ref && (
        <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground italic pt-2 border-t border-border">
          <BookOpen className="w-3 h-3" />
          <span>{data.sloka_ref}</span>
        </div>
      )}
    </div>
  );
}
