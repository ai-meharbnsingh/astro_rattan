import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { Loader2, Users, BookOpen, Info, ThumbsUp, ThumbsDown } from 'lucide-react';
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
  sloka_ref?: string;
}

interface PanchadhaMaitriData {
  kundli_id?: string;
  person_name?: string;
  friendships: PanchadhaMaitri[];
  strongest_ally_pairs?: PanchadhaMaitri[];
  conflict_pairs?: PanchadhaMaitri[];
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

const COMBINED_BADGE: Record<string, string> = {
  'great friend':  'bg-emerald-600 text-white',
  'adhimitra':     'bg-emerald-600 text-white',
  'friend':        'bg-green-600 text-white',
  'mitra':         'bg-green-600 text-white',
  'neutral':       'bg-gray-400 text-white',
  'sama':          'bg-gray-400 text-white',
  'enemy':         'bg-red-600 text-white',
  'shatru':        'bg-red-600 text-white',
  'great enemy':   'bg-red-800 text-white',
  'adhishatru':    'bg-red-800 text-white',
};

const RELATION_BADGE: Record<string, string> = {
  friend:  'bg-green-100 text-green-800',
  enemy:   'bg-red-100 text-red-800',
  neutral: 'bg-gray-100 text-gray-700',
};

function combBadge(r: string): string {
  const lower = r.toLowerCase();
  for (const key of Object.keys(COMBINED_BADGE)) {
    if (lower.includes(key)) return COMBINED_BADGE[key];
  }
  return 'bg-sacred-gold-dark text-white';
}

function relBadge(r: string): string {
  const lower = r.toLowerCase();
  if (lower.includes('friend')) return RELATION_BADGE.friend;
  if (lower.includes('enemy'))  return RELATION_BADGE.enemy;
  return RELATION_BADGE.neutral;
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdWrapCls   = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

export default function PanchadhaMaitriTab({ kundliId, language }: Props) {
  const { t } = useTranslation();
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
        if (!cancelled) setData(res as PanchadhaMaitriData);
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

  const pName      = (p: string) => hi ? (PLANET_HI[p] || p) : p;
  const friendships = data.friendships ?? [];
  const allies      = data.strongest_ally_pairs ?? [];
  const conflicts   = data.conflict_pairs ?? [];

  return (
    <div className="space-y-4">

      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Users className="w-6 h-6" />
          {hi ? 'पंचधा मैत्री' : 'Panchadha Maitri'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'नैसर्गिक, तात्कालिक एवं पंचधा सम्मिश्रित मित्रता-विश्लेषण'
            : 'Natural, temporary & five-fold combined planetary friendship analysis'}
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

      {/* Allies + Conflicts row */}
      {(allies.length > 0 || conflicts.length > 0) && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {allies.length > 0 && (
            <div className={ohContainer}>
              <div className="bg-emerald-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
                <ThumbsUp className="w-4 h-4" />
                <span>{hi ? 'श्रेष्ठ मित्र युग्म' : 'Strongest Ally Pairs'}</span>
              </div>
              <div className="px-4 py-3 flex flex-wrap gap-2">
                {allies.map((pair, i) => (
                  <span key={i} className="px-2.5 py-1 rounded-full bg-emerald-100 border border-emerald-200 text-emerald-800 text-xs font-medium">
                    {pName(pair.planet_a)} ↔ {pName(pair.planet_b)}
                  </span>
                ))}
              </div>
            </div>
          )}
          {conflicts.length > 0 && (
            <div className={ohContainer}>
              <div className="bg-red-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
                <ThumbsDown className="w-4 h-4" />
                <span>{hi ? 'संघर्ष युग्म' : 'Conflict Pairs'}</span>
              </div>
              <div className="px-4 py-3 flex flex-wrap gap-2">
                {conflicts.map((pair, i) => (
                  <span key={i} className="px-2.5 py-1 rounded-full bg-red-100 border border-red-200 text-red-800 text-xs font-medium">
                    {pName(pair.planet_a)} ↔ {pName(pair.planet_b)}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Main Table */}
      {friendships.length > 0 ? (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Users className="w-4 h-4" />
            <span>{hi ? 'पंचधा विश्लेषण' : 'Five-fold Analysis'}</span>
            <span className="ml-auto text-[12px] font-normal opacity-80">{friendships.length}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '16%' }} />
              <col style={{ width: '13%' }} />
              <col style={{ width: '13%' }} />
              <col style={{ width: '14%' }} />
              <col style={{ width: '44%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{hi ? 'ग्रह युग्म' : 'Pair'}</th>
                <th className={thCls}>{hi ? 'नैसर्गिक' : 'Natural'}</th>
                <th className={thCls}>{hi ? 'तात्कालिक' : 'Temporary'}</th>
                <th className={thCls}>{hi ? 'पंचधा' : 'Combined'}</th>
                <th className={thCls}>{hi ? 'प्रभाव' : 'Effect'}</th>
              </tr>
            </thead>
            <tbody>
              {friendships.map((f, i) => {
                const combinedLabel = hi ? (f.combined_relation_hi || f.combined_relation_en) : f.combined_relation_en;
                const effect = hi ? (f.effect_hi || f.effect_en) : f.effect_en;
                return (
                  <tr key={i}>
                    <td className={`${tdCls} font-semibold`}>
                      {pName(f.planet_a)}
                      <span className="text-muted-foreground mx-0.5">↔</span>
                      {pName(f.planet_b)}
                    </td>
                    <td className={tdCls}>
                      <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${relBadge(f.natural_relation)}`}>
                        {f.natural_relation || '—'}
                      </span>
                    </td>
                    <td className={tdCls}>
                      <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${relBadge(f.temporary_relation)}`}>
                        {f.temporary_relation || '—'}
                      </span>
                    </td>
                    <td className={tdCls}>
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${combBadge(f.combined_relation_en || '')}`}>
                        {combinedLabel || '—'}
                      </span>
                    </td>
                    <td className={tdWrapCls}>
                      <p>{effect || '—'}</p>
                      {f.sloka_ref && (
                        <div className="flex items-center gap-1 mt-1 text-[10px] text-muted-foreground italic">
                          <BookOpen className="w-2.5 h-2.5 shrink-0" />
                          <span>{f.sloka_ref}</span>
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
          {hi ? 'पंचधा मैत्री डेटा उपलब्ध नहीं।' : 'No Panchadha Maitri data available.'}
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
