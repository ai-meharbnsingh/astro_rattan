import { useState, useEffect } from 'react';
import { Loader2, Star, BookOpen, CheckCircle2, XCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface BilingualField {
  en: string;
  hi: string;
}

interface DosDonts {
  en: string;
  hi: string;
}

interface Gemstone {
  name_en: string;
  name_hi: string;
  benefit_en: string;
  benefit_hi: string;
}

interface TransitLuckyData {
  lucky_number: number;
  lucky_color: BilingualField;
  compatible_sign: BilingualField;
  mood: BilingualField;
  dos: DosDonts[];
  donts: DosDonts[];
  lucky_time: BilingualField;
  gemstone: Gemstone;
  mantra: string;
  sign: string;
  date: string;
}

interface Props {
  kundliId: string;
  language?: string;
}

// Map common color names to Tailwind swatch colors
const COLOR_SWATCH: Record<string, string> = {
  red: 'bg-red-400', blue: 'bg-blue-400', green: 'bg-green-400',
  yellow: 'bg-yellow-300', orange: 'bg-orange-400', purple: 'bg-purple-400',
  pink: 'bg-pink-400', white: 'bg-white border border-gray-300', black: 'bg-gray-900',
  gold: 'bg-amber-400', silver: 'bg-gray-300', brown: 'bg-amber-800',
  indigo: 'bg-indigo-500', violet: 'bg-violet-500', cyan: 'bg-cyan-400',
  teal: 'bg-teal-400', coral: 'bg-orange-300', maroon: 'bg-red-800',
};

function colorSwatch(colorEn: string): string {
  const key = colorEn?.toLowerCase().trim();
  return COLOR_SWATCH[key] ?? 'bg-sacred-gold';
}

export default function TransitLuckyTab({ kundliId, language }: Props) {
  const [data, setData] = useState<TransitLuckyData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api.get<TransitLuckyData>(`/api/kundli/${kundliId}/transit-lucky`)
      .then(res => { if (!cancelled) setData(res); })
      .catch((err: any) => { if (!cancelled) setError(err?.message || 'Failed to load Lucky Indicators'); })
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

  const luckyColor = isHi ? data.lucky_color?.hi : data.lucky_color?.en;
  const compatSign = isHi ? data.compatible_sign?.hi : data.compatible_sign?.en;
  const mood = isHi ? data.mood?.hi : data.mood?.en;
  const luckyTime = isHi ? data.lucky_time?.hi : data.lucky_time?.en;
  const gemstoneName = isHi ? data.gemstone?.name_hi : data.gemstone?.name_en;
  const gemstoneBenefit = isHi ? data.gemstone?.benefit_hi : data.gemstone?.benefit_en;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Star className="w-6 h-6" />
          {isHi ? 'आज के शुभ संकेतक' : "Today's Lucky Indicators"}
        </Heading>
        {data.date && (
          <p className="text-sm text-muted-foreground">
            {isHi ? `तिथि: ${data.date}` : `Date: ${data.date}`}
            {data.sign ? (isHi ? ` · राशि: ${data.sign}` : ` · Sign: ${data.sign}`) : ''}
          </p>
        )}
      </div>

      {/* Hero row — number, color, sign, mood, time */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
        {/* Lucky Number */}
        <div className="col-span-1 flex flex-col items-center justify-center p-5 rounded-xl border border-sacred-gold/40 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
            {isHi ? 'शुभ अंक' : 'Lucky Number'}
          </p>
          <span className="text-5xl font-extrabold text-sacred-gold-dark leading-none">
            {data.lucky_number ?? '—'}
          </span>
        </div>

        {/* Lucky Color */}
        <div className="flex flex-col items-center justify-center p-4 rounded-xl border border-sacred-gold/20 bg-white/50 gap-2">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide">
            {isHi ? 'शुभ रंग' : 'Lucky Color'}
          </p>
          <div className={`w-10 h-10 rounded-full shadow-sm ${colorSwatch(data.lucky_color?.en ?? '')}`} />
          <span className="text-sm font-semibold text-foreground text-center">{luckyColor ?? '—'}</span>
        </div>

        {/* Compatible Sign */}
        <div className="flex flex-col items-center justify-center p-4 rounded-xl border border-sacred-gold/20 bg-white/50 gap-1">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide">
            {isHi ? 'अनुकूल राशि' : 'Compatible Sign'}
          </p>
          <span className="text-2xl">♈</span>
          <span className="text-sm font-semibold text-foreground text-center">{compatSign ?? '—'}</span>
        </div>

        {/* Mood */}
        <div className="flex flex-col items-center justify-center p-4 rounded-xl border border-sacred-gold/20 bg-white/50 gap-1">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide">
            {isHi ? 'मनोभाव' : 'Mood'}
          </p>
          <span className="text-2xl">✨</span>
          <span className="text-sm font-semibold text-foreground text-center">{mood ?? '—'}</span>
        </div>

        {/* Lucky Time */}
        <div className="flex flex-col items-center justify-center p-4 rounded-xl border border-sacred-gold/20 bg-white/50 gap-1">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide">
            {isHi ? 'शुभ समय' : 'Lucky Time'}
          </p>
          <span className="text-2xl">🕐</span>
          <span className="text-sm font-semibold text-foreground text-center">{luckyTime ?? '—'}</span>
        </div>
      </div>

      {/* Do's and Don'ts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Do's */}
        <div className="p-5 rounded-xl border border-emerald-200 bg-emerald-50/40">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-700" />
            <h3 className="text-base font-semibold text-emerald-800">
              {isHi ? 'करें' : "Do's"}
            </h3>
          </div>
          {(data.dos?.length ?? 0) > 0 ? (
            <ul className="space-y-2">
              {data.dos.map((item, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 mt-0.5 shrink-0" />
                  <div>
                    <span className="text-sm text-foreground/90">
                      {isHi ? item.hi : item.en}
                    </span>
                    {!isHi && item.hi && (
                      <p className="text-[11px] text-muted-foreground">{item.hi}</p>
                    )}
                    {isHi && item.en && (
                      <p className="text-[11px] text-muted-foreground">{item.en}</p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-muted-foreground italic">—</p>
          )}
        </div>

        {/* Don'ts */}
        <div className="p-5 rounded-xl border border-red-200 bg-red-50/40">
          <div className="flex items-center gap-2 mb-3">
            <XCircle className="w-5 h-5 text-red-700" />
            <h3 className="text-base font-semibold text-red-800">
              {isHi ? 'न करें' : "Don'ts"}
            </h3>
          </div>
          {(data.donts?.length ?? 0) > 0 ? (
            <ul className="space-y-2">
              {data.donts.map((item, i) => (
                <li key={i} className="flex items-start gap-2">
                  <XCircle className="w-3.5 h-3.5 text-red-500 mt-0.5 shrink-0" />
                  <div>
                    <span className="text-sm text-foreground/90">
                      {isHi ? item.hi : item.en}
                    </span>
                    {!isHi && item.hi && (
                      <p className="text-[11px] text-muted-foreground">{item.hi}</p>
                    )}
                    {isHi && item.en && (
                      <p className="text-[11px] text-muted-foreground">{item.en}</p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-muted-foreground italic">—</p>
          )}
        </div>
      </div>

      {/* Gemstone card */}
      {data.gemstone && (
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-white shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Star className="w-5 h-5 text-sacred-gold-dark" />
            <h3 className="text-base font-semibold text-sacred-gold-dark">
              {isHi ? 'रत्न / Gemstone' : 'Gemstone'}
            </h3>
          </div>
          <div className="flex items-start gap-4">
            <div className="shrink-0 w-12 h-12 rounded-xl bg-sacred-gold/15 flex items-center justify-center text-2xl">
              💎
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-bold text-foreground text-lg">{gemstoneName ?? '—'}</p>
              {isHi && data.gemstone.name_en && (
                <p className="text-xs text-muted-foreground">{data.gemstone.name_en}</p>
              )}
              {!isHi && data.gemstone.name_hi && (
                <p className="text-xs text-muted-foreground">{data.gemstone.name_hi}</p>
              )}
              {gemstoneBenefit && (
                <p className="text-sm text-foreground/80 mt-2 leading-relaxed">{gemstoneBenefit}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Mantra highlight */}
      {data.mantra && (
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFF9F5] to-white text-center">
          <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-2">
            {isHi ? 'मंत्र' : 'Mantra'}
          </p>
          <div className="flex items-center justify-center gap-2">
            <BookOpen className="w-4 h-4 text-sacred-gold-dark shrink-0" />
            <p className="text-base font-semibold text-sacred-gold-dark italic leading-relaxed">
              {data.mantra}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
