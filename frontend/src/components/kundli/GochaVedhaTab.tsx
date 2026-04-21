import { useState, useEffect } from 'react';
import { Loader2, AlertTriangle, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { Heading } from '@/components/ui/heading';
import SlokaHover from './SlokaHover';
import TimingTheorySection from '@/components/kundli/TimingTheorySection';

interface TransitRow {
  planet: string;
  current_sign: string;
  current_house: number;
  house_from_moon: number;
  vedha_active: boolean;
  vedha_reason_en?: string;
  vedha_reason_hi?: string;
  latta_effect?: string;
  latta_direction_en?: string;
  latta_direction_hi?: string;
  net_result_en?: string;
  net_result_hi?: string;
  sloka_ref?: string;
}

interface GochaVedhaData {
  transits: TransitRow[];
}

interface Props {
  kundliId: string;
  language?: string;
}

const thCls = 'p-1 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const thCenterCls = 'p-1 text-center text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls = 'p-1 text-xs text-foreground border-t border-border align-top';
const tdWrapCls = 'p-1 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

export default function GochaVedhaTab({ kundliId, language }: Props) {
  const [data, setData] = useState<GochaVedhaData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api.get<GochaVedhaData>(`/api/kundli/${kundliId}/gochara-vedha`)
      .then(res => { if (!cancelled) setData(res); })
      .catch((err: any) => { if (!cancelled) setError(err?.message || 'Failed to load Gochara Vedha data'); })
      .finally(() => { if (!cancelled) setLoading(false); });
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
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
        {error}
      </div>
    );
  }

  if (!data) return null;

  const transits = data.transits ?? [];

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <AlertTriangle className="w-6 h-6" />
          {isHi ? 'गोचर वेध' : 'Gochara Vedha'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi ? 'अवरोध बिंदु जो लाभकारी गोचर को निष्प्रभावी करते हैं' : 'Obstruction points that neutralise a beneficial transit'}
        </p>
      </div>
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          <span>{isHi ? 'गोचर वेध — शास्त्रीय गोचर संशोधक' : 'Gochara Vedha — Classical Transit Modifiers'}</span>
        </div>

        {transits.length === 0 ? (
          <p className="text-center text-foreground text-sm py-8">
            {isHi ? 'कोई गोचर वेध डेटा उपलब्ध नहीं है' : 'No Gochara Vedha data available for this chart'}
          </p>
        ) : (
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '10%' }} />
              <col style={{ width: '10%' }} />
              <col style={{ width: '6%' }} />
              <col style={{ width: '6%' }} />
              <col style={{ width: '12%' }} />
              <col style={{ width: '20%' }} />
              <col style={{ width: '20%' }} />
              <col style={{ width: '16%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'ग्रह' : 'Planet'}</th>
                <th className={thCls}>{isHi ? 'राशि' : 'Sign'}</th>
                <th className={thCenterCls}>{isHi ? 'भाव' : 'House'}</th>
                <th className={thCenterCls}>{isHi ? 'चन्द्र से' : 'Moon'}</th>
                <th className={thCls}>{isHi ? 'वेध' : 'Vedha'}</th>
                <th className={thCls}>{isHi ? 'लट्ट प्रभाव' : 'Latta Effect'}</th>
                <th className={thCls}>{isHi ? 'शुद्ध फल' : 'Net Result'}</th>
                <th className={thCls}>{isHi ? 'श्लोक' : 'Sloka'}</th>
              </tr>
            </thead>
            <tbody>
              {transits.map((row, i) => {
                const vedhaReason = isHi ? row.vedha_reason_hi : row.vedha_reason_en;
                const lattaDir = isHi ? row.latta_direction_hi : row.latta_direction_en;
                const netResult = isHi ? row.net_result_hi : row.net_result_en;
                const isPositiveLatta = row.latta_effect?.toLowerCase().includes('benefic') ||
                  row.latta_effect?.toLowerCase().includes('good') ||
                  row.latta_effect?.toLowerCase().includes('शुभ');

                return (
                  <tr key={i}>
                    <td className={`${tdCls} font-semibold`}>
                      {translatePlanet(row.planet, language ?? 'en') ?? row.planet ?? '—'}
                    </td>
                    <td className={tdCls}>
                      {translateSign(row.current_sign, language ?? 'en') ?? row.current_sign ?? '—'}
                    </td>
                    <td className={`${tdCls} text-center`}>{row.current_house ?? '—'}</td>
                    <td className={`${tdCls} text-center`}>{row.house_from_moon ?? '—'}</td>
                    <td className={tdWrapCls}>
                      {row.vedha_active ? (
                        <div className="space-y-0.5">
                          <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-red-100 text-red-800">
                            <AlertTriangle className="w-2.5 h-2.5 shrink-0" />
                            {isHi ? 'वेध सक्रिय' : 'Vedha Active'}
                          </span>
                          {vedhaReason && (
                            <p className="text-[10px] text-muted-foreground leading-tight mt-0.5">{vedhaReason}</p>
                          )}
                        </div>
                      ) : (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                          {isHi ? 'स्पष्ट' : 'Clear'}
                        </span>
                      )}
                    </td>
                    <td className={tdWrapCls}>
                      {row.latta_effect ? (
                        <div className="space-y-0.5">
                          <p className={`text-[11px] font-medium leading-snug ${isPositiveLatta ? 'text-emerald-700' : 'text-amber-700'}`}>
                            {row.latta_effect}
                          </p>
                          {lattaDir && (
                            <p className="text-[10px] text-muted-foreground">{lattaDir}</p>
                          )}
                        </div>
                      ) : (
                        <span className="text-muted-foreground">—</span>
                      )}
                    </td>
                    <td className={tdWrapCls}>{netResult ?? '—'}</td>
                    <td className={tdWrapCls}>
                      {row.sloka_ref ? (
                        <SlokaHover slokaRef={row.sloka_ref} language={language} className="flex items-start gap-1 text-[10px] text-muted-foreground italic">
                          <BookOpen className="w-3 h-3 shrink-0 mt-0.5" />
                          <span>{row.sloka_ref}</span>
                        </SlokaHover>
                      ) : (
                        <span className="text-muted-foreground">—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Legend */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
          <BookOpen className="w-4 h-4" />
          <span>{isHi ? 'संदर्भ' : 'Reference'}</span>
        </div>
        <div className="p-3 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1.5">
            <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-red-100 text-red-800">
              <AlertTriangle className="w-2.5 h-2.5" />
              {isHi ? 'वेध सक्रिय' : 'Vedha Active'}
            </span>
            <span>{isHi ? '= गोचर फल निरस्त' : '= transit result nullified'}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <BookOpen className="w-3 h-3 text-sacred-gold-dark" />
            <SlokaHover slokaRef="Phaladeepika" language={language}>
              {isHi ? 'श्लोक संदर्भ — फलदीपिका' : 'Sloka references — Phaladeepika'}
            </SlokaHover>
          </div>
        </div>
      </div>
      <TimingTheorySection language={language || 'en'} tab="gochara-vedha" />
    </div>
  );
}
