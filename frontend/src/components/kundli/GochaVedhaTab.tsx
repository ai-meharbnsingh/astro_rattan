import { useState, useEffect } from 'react';
import { Loader2, AlertTriangle, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

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

  const transits = data.transits ?? [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <AlertTriangle className="w-6 h-6" />
          {isHi ? 'गोचर वेध — शास्त्रीय गोचर संशोधक' : 'Gochara Vedha — Classical Transit Modifiers'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi
            ? 'गोचर फल में वेध और लट्ट प्रभाव का शास्त्रीय विश्लेषण (फलदीपिका आधारित)'
            : 'Classical Vedha and Latta modifiers on transit results based on Phaladeepika'}
        </p>
      </div>

      {transits.length === 0 ? (
        <div className="p-6 rounded-xl border border-sacred-gold/20 bg-white/50 text-center text-sm text-muted-foreground">
          {isHi ? 'कोई गोचर वेध डेटा उपलब्ध नहीं है' : 'No Gochara Vedha data available for this chart'}
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-white/50">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-sacred-gold/20 bg-sacred-gold/5">
                <th className="px-4 py-3 text-left font-semibold text-sacred-gold-dark">
                  {isHi ? 'ग्रह' : 'Planet'}
                </th>
                <th className="px-4 py-3 text-left font-semibold text-sacred-gold-dark">
                  {isHi ? 'वर्तमान राशि' : 'Current Sign'}
                </th>
                <th className="px-4 py-3 text-center font-semibold text-sacred-gold-dark">
                  {isHi ? 'भाव' : 'House'}
                </th>
                <th className="px-4 py-3 text-center font-semibold text-sacred-gold-dark">
                  {isHi ? 'चन्द्र से' : 'From Moon'}
                </th>
                <th className="px-4 py-3 text-center font-semibold text-sacred-gold-dark">
                  {isHi ? 'वेध' : 'Vedha'}
                </th>
                <th className="px-4 py-3 text-left font-semibold text-sacred-gold-dark">
                  {isHi ? 'लट्ट प्रभाव' : 'Latta Effect'}
                </th>
                <th className="px-4 py-3 text-left font-semibold text-sacred-gold-dark">
                  {isHi ? 'शुद्ध फल' : 'Net Result'}
                </th>
                <th className="px-4 py-3 text-left font-semibold text-sacred-gold-dark">
                  {isHi ? 'श्लोक' : 'Sloka'}
                </th>
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
                  <tr
                    key={i}
                    className={`border-b border-sacred-gold/10 last:border-0 ${i % 2 === 0 ? 'bg-white' : 'bg-sacred-gold/[0.02]'}`}
                  >
                    <td className="px-4 py-3 font-semibold text-foreground">{row.planet ?? '—'}</td>
                    <td className="px-4 py-3 text-foreground/80">{row.current_sign ?? '—'}</td>
                    <td className="px-4 py-3 text-center text-foreground/80">{row.current_house ?? '—'}</td>
                    <td className="px-4 py-3 text-center text-foreground/80">{row.house_from_moon ?? '—'}</td>
                    <td className="px-4 py-3 text-center">
                      {row.vedha_active ? (
                        <div className="flex flex-col items-center gap-1">
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-100 border border-red-300 text-red-700 text-xs font-semibold">
                            <AlertTriangle className="w-3 h-3" />
                            {isHi ? 'वेध सक्रिय' : 'Vedha Active'}
                          </span>
                          {vedhaReason && (
                            <span className="text-[10px] text-red-600 text-center leading-tight max-w-[120px]">
                              {vedhaReason}
                            </span>
                          )}
                        </div>
                      ) : (
                        <span className="inline-flex px-2 py-0.5 rounded-full bg-emerald-100 border border-emerald-200 text-emerald-700 text-xs font-medium">
                          {isHi ? 'स्पष्ट' : 'Clear'}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      {row.latta_effect ? (
                        <div className="space-y-0.5">
                          <span className={`text-xs font-medium ${isPositiveLatta ? 'text-emerald-700' : 'text-amber-700'}`}>
                            {row.latta_effect}
                          </span>
                          {lattaDir && (
                            <p className="text-[10px] text-muted-foreground">{lattaDir}</p>
                          )}
                        </div>
                      ) : (
                        <span className="text-muted-foreground text-xs">—</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-xs text-foreground/80 max-w-[180px]">
                      {netResult ?? '—'}
                    </td>
                    <td className="px-4 py-3">
                      {row.sloka_ref ? (
                        <div className="flex items-center gap-1 text-[10px] text-muted-foreground italic">
                          <BookOpen className="w-3 h-3 shrink-0" />
                          <span>{row.sloka_ref}</span>
                        </div>
                      ) : (
                        <span className="text-muted-foreground text-xs">—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Legend */}
      <div className="p-4 rounded-lg bg-sacred-gold/5 border border-sacred-gold/20 text-xs text-muted-foreground flex flex-wrap items-start gap-4">
        <div className="flex items-center gap-1.5">
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-100 border border-red-300 text-red-700 text-[10px] font-semibold">
            <AlertTriangle className="w-2.5 h-2.5" />
            {isHi ? 'वेध सक्रिय' : 'Vedha Active'}
          </span>
          <span>{isHi ? '= गोचर फल निरस्त' : '= transit result nullified'}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <BookOpen className="w-3 h-3 text-sacred-gold-dark" />
          <span>{isHi ? 'श्लोक संदर्भ — फलदीपिका' : 'Sloka references — Phaladeepika'}</span>
        </div>
      </div>
    </div>
  );
}
