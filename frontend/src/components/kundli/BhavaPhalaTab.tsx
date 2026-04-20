import { useState, useEffect } from 'react';
import { Loader2, Home, Star, BookOpen, Sparkles, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface PlanetPlacement {
  planet: string;
  house: number;
  sign: string;
  effect_en: string;
  effect_hi: string;
  sloka_ref: string;
  sign_lord_modifier_en?: string;
  sign_lord_modifier_hi?: string;
}

interface BhavaGeneral {
  house: number;
  name_en: string;
  name_hi: string;
  general_en: string;
  general_hi: string;
  sloka_ref: string;
  status: 'strong' | 'weak' | 'neutral';
  mooltrikona_note_en?: string;
  mooltrikona_note_hi?: string;
}

interface ApiResponse {
  kundli_id?: string;
  person_name?: string;
  planet_placements: PlanetPlacement[];
  bhava_generals: BhavaGeneral[];
  sloka_ref: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const STATUS_STYLE: Record<string, { badge: string; Icon: typeof TrendingUp; key: string }> = {
  strong:  { badge: 'bg-emerald-100 text-emerald-800', Icon: TrendingUp,   key: 'auto.bhavaStrong' },
  weak:    { badge: 'bg-red-100 text-red-800',          Icon: TrendingDown, key: 'auto.bhavaWeak' },
  neutral: { badge: 'bg-amber-100 text-amber-800',      Icon: Minus,        key: 'auto.bhavaNeutral' },
};

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'बृहस्पति', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdWrapCls   = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

function PlacementTable({ rows, isHi, t }: { rows: PlanetPlacement[]; isHi: boolean; t: (k: string) => string }) {
  if (rows.length === 0) {
    return (
      <div className="px-4 py-3 text-xs text-muted-foreground">
        {isHi ? 'इस खंड में कोई ग्रह नहीं' : 'No planets in this range'}
      </div>
    );
  }
  return (
    <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
      <colgroup>
        <col style={{ width: '13%' }} />
        <col style={{ width: '5%' }} />
        <col style={{ width: '12%' }} />
        <col style={{ width: '55%' }} />
        <col style={{ width: '15%' }} />
      </colgroup>
      <thead>
        <tr>
          <th className={thCls}>{isHi ? 'ग्रह' : 'Planet'}</th>
          <th className={thCls}>{isHi ? 'भाव' : 'H'}</th>
          <th className={thCls}>{isHi ? 'राशि' : 'Sign'}</th>
          <th className={thCls}>{isHi ? 'फल' : 'Effect'}</th>
          <th className={thCls}>{isHi ? 'श्लोक' : 'Sloka'}</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((pp, i) => {
          const effect = isHi ? pp.effect_hi : pp.effect_en;
          const modifier = isHi ? pp.sign_lord_modifier_hi : pp.sign_lord_modifier_en;
          const planetName = isHi ? (PLANET_HI[pp.planet] || pp.planet) : pp.planet;
          return (
            <tr key={`${pp.planet}-${i}`}>
              <td className={`${tdCls} font-semibold`}>{planetName}</td>
              <td className={tdCls}>{pp.house}</td>
              <td className={tdWrapCls}>{pp.sign}</td>
              <td className={tdWrapCls}>
                <p>{effect}</p>
                {modifier && (
                  <p className="mt-1 text-[10px] text-blue-700 italic">
                    {isHi ? 'राशि-स्वामी: ' : 'Sign Lord: '}{modifier}
                  </p>
                )}
              </td>
              <td className={tdWrapCls}>
                <div className="flex items-start gap-1 text-[10px] text-muted-foreground italic">
                  <BookOpen className="w-2.5 h-2.5 shrink-0 mt-0.5" />
                  <span>{pp.sloka_ref}</span>
                </div>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default function BhavaPhalaTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/bhava-phala`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Bhava Phala');
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
        <span className="ml-2 text-sm text-foreground">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {t('auto.bhavaPhala')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.bhavaPhalaDesc')}</p>
      </div>

      {/* Planet in House */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Star className="w-4 h-4" />
          <span>{t('auto.planetInHouse')}</span>
          <span className="ml-auto text-[12px] font-normal opacity-80">{data.planet_placements.length}</span>
        </div>
        <PlacementTable rows={data.planet_placements} isHi={isHi} t={t} />
      </div>

      {/* House-wise Status */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Home className="w-4 h-4" />
          <span>{t('auto.houseStatus')}</span>
        </div>
        <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '5%' }} />
            <col style={{ width: '18%' }} />
            <col style={{ width: '12%' }} />
            <col style={{ width: '50%' }} />
            <col style={{ width: '15%' }} />
          </colgroup>
          <thead>
            <tr>
              <th className={thCls}>{isHi ? 'भाव' : 'H'}</th>
              <th className={thCls}>{isHi ? 'नाम' : 'Name'}</th>
              <th className={thCls}>{isHi ? 'स्थिति' : 'Status'}</th>
              <th className={thCls}>{isHi ? 'फलादेश' : 'Result'}</th>
              <th className={thCls}>{isHi ? 'श्लोक' : 'Sloka'}</th>
            </tr>
          </thead>
          <tbody>
            {data.bhava_generals.map((b) => {
              const style = STATUS_STYLE[b.status] || STATUS_STYLE.neutral;
              const StatusIcon = style.Icon;
              const name = isHi ? b.name_hi : b.name_en;
              const general = isHi ? b.general_hi : b.general_en;
              const localizedBhava = t(`auto.bhava${b.house}`);
              const moolt = isHi ? b.mooltrikona_note_hi : b.mooltrikona_note_en;
              return (
                <tr key={b.house}>
                  <td className={`${tdCls} font-semibold text-center`}>{b.house}</td>
                  <td className={tdCls}>{localizedBhava || name}</td>
                  <td className={tdCls}>
                    <span className={`inline-flex items-center gap-1 text-[10px] font-semibold px-1.5 py-0.5 rounded ${style.badge}`}>
                      <StatusIcon className="w-2.5 h-2.5" />
                      {t(style.key)}
                    </span>
                  </td>
                  <td className={tdWrapCls}>
                    <p>{general}</p>
                    {moolt && (
                      <p className="mt-1 text-[10px] text-amber-700 italic">
                        {isHi ? 'मूलत्रिकोण: ' : 'Mooltrikona: '}{moolt}
                      </p>
                    )}
                  </td>
                  <td className={tdWrapCls}>
                    <div className="flex items-start gap-1 text-[10px] text-muted-foreground italic">
                      <BookOpen className="w-2.5 h-2.5 shrink-0 mt-0.5" />
                      <span>{b.sloka_ref}</span>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Sloka footer */}
      <div className="text-center text-xs text-muted-foreground italic pt-2 border-t border-sacred-gold/20">
        {data.sloka_ref}
      </div>
    </div>
  );
}
