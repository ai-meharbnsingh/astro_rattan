import { useState, useEffect } from 'react';
import { Loader2, Clock, ChevronDown, ChevronRight, BookOpen, Info } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import TimingTheorySection from '@/components/kundli/TimingTheorySection';

interface Antardasha {
  planet: string;
  start: string;
  end: string;
  years: number;
}

interface KalachakraPeriod {
  period_name: string;
  planet: string;
  start_date: string;
  end_date: string;
  duration_years: number;
  antardashas?: Antardasha[];
}

interface KalachakraData {
  kundli_id?: string;
  person_name?: string;
  deha_sign: string;
  jeeva_sign: string;
  cycle_info?: string;
  periods: KalachakraPeriod[];
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

const PLANET_COLORS: Record<string, string> = {
  Sun: 'bg-orange-100 text-orange-800 border-orange-200',
  Moon: 'bg-blue-100 text-blue-800 border-blue-200',
  Mars: 'bg-red-100 text-red-800 border-red-200',
  Mercury: 'bg-green-100 text-green-800 border-green-200',
  Jupiter: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  Venus: 'bg-pink-100 text-pink-800 border-pink-200',
  Saturn: 'bg-indigo-100 text-indigo-800 border-indigo-200',
  Rahu: 'bg-gray-100 text-gray-800 border-gray-300',
  Ketu: 'bg-purple-100 text-purple-800 border-purple-200',
};

function formatDate(dateStr?: string): string {
  if (!dateStr) return '—';
  try {
    return new Date(dateStr).toLocaleDateString('en-IN', { year: 'numeric', month: 'short' });
  } catch {
    return dateStr;
  }
}

export default function KalachakraTab({ kundliId, language }: Props) {
  const [data, setData] = useState<KalachakraData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Set<number>>(new Set([0]));
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    (async () => {
      try {
        const res = await api.get(`/api/kundli/${kundliId}/kalachakra-dasha`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Kalachakra Dasha');
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
  const planetColor = (p: string) => PLANET_COLORS[p] || 'bg-sacred-gold/10 text-sacred-brown border-sacred-gold/20';

  const toggleExpand = (idx: number) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Clock className="w-6 h-6" />
          {hi ? 'कालचक्र दशा' : 'Kalachakra Dasha'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'नक्षत्र-आधारित काल-चक्र दशा प्रणाली'
            : 'Nakshatra-based cyclic dasha system'}
        </p>
      </div>

      {/* Deha / Jeeva signs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-sacred-gold/20 flex items-center justify-center shrink-0">
            <span className="text-sacred-gold-dark font-bold text-sm">देह</span>
          </div>
          <div>
            <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide">
              {hi ? 'देह राशि' : 'Deha Sign'}
            </p>
            <p className="font-bold text-sacred-brown text-base">{data.deha_sign || '—'}</p>
          </div>
        </div>
        <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-sacred-gold/20 flex items-center justify-center shrink-0">
            <span className="text-sacred-gold-dark font-bold text-sm">जीव</span>
          </div>
          <div>
            <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide">
              {hi ? 'जीव राशि' : 'Jeeva Sign'}
            </p>
            <p className="font-bold text-sacred-brown text-base">{data.jeeva_sign || '—'}</p>
          </div>
        </div>
      </div>

      {/* Cycle info */}
      {data.cycle_info && (
        <div className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 px-4 py-3 flex items-start gap-2">
          <Info className="w-4 h-4 text-sacred-gold-dark shrink-0 mt-0.5" />
          <p className="text-sm text-foreground/80 leading-relaxed">{data.cycle_info}</p>
        </div>
      )}

      {/* Summary */}
      {(data.summary_en || data.summary_hi) && (
        <p className="text-sm text-foreground/80 leading-relaxed italic">
          {hi ? (data.summary_hi || data.summary_en) : data.summary_en}
        </p>
      )}

      {/* Periods timeline */}
      <div className="space-y-3">
        {(data.periods || []).map((period, idx) => {
          const isOpen = expanded.has(idx);
          const colorClass = planetColor(period.planet);
          return (
            <div
              key={idx}
              className="rounded-xl border border-sacred-gold/20 bg-white/50 overflow-hidden"
            >
              {/* Period header row — clickable */}
              <button
                className="w-full text-left px-4 py-3 flex items-center gap-3 hover:bg-sacred-gold/5 transition-colors"
                onClick={() => toggleExpand(idx)}
                aria-expanded={isOpen}
              >
                {/* Expand toggle */}
                <span className="shrink-0 text-sacred-gold-dark">
                  {isOpen
                    ? <ChevronDown className="w-4 h-4" />
                    : <ChevronRight className="w-4 h-4" />}
                </span>

                {/* Planet badge */}
                <span className={`shrink-0 text-[11px] font-bold px-2 py-0.5 rounded-full border ${colorClass}`}>
                  {planetName(period.planet)}
                </span>

                {/* Period name */}
                <span className="flex-1 font-semibold text-sacred-brown text-sm">
                  {period.period_name || planetName(period.planet)}
                </span>

                {/* Duration */}
                <span className="shrink-0 text-xs text-muted-foreground">
                  {period.duration_years != null ? `${period.duration_years} yr` : ''}
                </span>

                {/* Date range */}
                <span className="shrink-0 text-xs text-muted-foreground hidden sm:block">
                  {formatDate(period.start_date)} – {formatDate(period.end_date)}
                </span>
              </button>

              {/* Antardashas */}
              {isOpen && period.antardashas && period.antardashas.length > 0 && (
                <div className="border-t border-sacred-gold/15 px-4 py-3 space-y-2">
                  <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                    {hi ? 'अन्तर्दशाएँ' : 'Antardashas'}
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {period.antardashas.map((ad, ai) => (
                      <div
                        key={ai}
                        className="flex items-center gap-2 rounded-lg bg-gray-50 border border-gray-100 px-3 py-2 text-xs"
                      >
                        <span className={`shrink-0 text-[10px] font-bold px-1.5 py-0.5 rounded border ${planetColor(ad.planet)}`}>
                          {planetName(ad.planet)}
                        </span>
                        <span className="flex-1 text-foreground/80">
                          {formatDate(ad.start)} – {formatDate(ad.end)}
                        </span>
                        {ad.years != null && (
                          <span className="text-muted-foreground shrink-0">{ad.years}y</span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Open but no antardashas */}
              {isOpen && (!period.antardashas || period.antardashas.length === 0) && (
                <div className="border-t border-sacred-gold/15 px-4 py-3">
                  <p className="text-xs text-muted-foreground italic">
                    {hi ? 'अन्तर्दशा उपलब्ध नहीं।' : 'No antardasha data available.'}
                  </p>
                </div>
              )}
            </div>
          );
        })}

        {data.periods?.length === 0 && (
          <div className="p-6 text-center text-muted-foreground text-sm italic">
            {hi ? 'कालचक्र दशा डेटा उपलब्ध नहीं।' : 'No Kalachakra Dasha periods available.'}
          </div>
        )}
      </div>

      {/* Sloka ref footer */}
      {data.sloka_ref && (
        <div className="flex items-center gap-2 pt-2 border-t border-sacred-gold/20 text-[11px] text-muted-foreground italic">
          <BookOpen className="w-3 h-3 text-sacred-gold-dark shrink-0" />
          <span>{data.sloka_ref}</span>
        </div>
      )}
      <TimingTheorySection language={language || 'en'} tab="kalachakra" />
    </div>
  );
}
