import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { Loader2, Star, BookOpen, CheckCircle2, XCircle, Gem } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import TimingTheorySection from '@/components/kundli/TimingTheorySection';

interface BilingualField { en: string; hi: string; }
interface DosDonts      { en: string; hi: string; }
interface Gemstone {
  name_en: string; name_hi: string;
  benefit_en: string; benefit_hi: string; // metal to wear it in
  finger_en?: string; finger_hi?: string;
  day_en?: string; day_hi?: string;
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

interface Props { kundliId: string; language?: string; }

const COLOR_SWATCH: Record<string, string> = {
  red: 'bg-red-400', blue: 'bg-blue-400', green: 'bg-green-400',
  yellow: 'bg-yellow-300', orange: 'bg-orange-400', purple: 'bg-purple-400',
  pink: 'bg-pink-400', white: 'bg-white border border-gray-300', black: 'bg-gray-900',
  gold: 'bg-amber-400', silver: 'bg-gray-300', brown: 'bg-amber-800',
  indigo: 'bg-indigo-500', violet: 'bg-violet-500', cyan: 'bg-cyan-400',
  teal: 'bg-teal-400', coral: 'bg-orange-300', maroon: 'bg-red-800',
};
function colorSwatch(en: string): string {
  return COLOR_SWATCH[en?.toLowerCase().trim()] ?? 'bg-sacred-gold';
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdLbl       = 'p-1.5 text-xs text-muted-foreground border-t border-border align-top w-[38%]';
const tdVal       = 'p-1.5 text-xs text-foreground font-medium border-t border-border align-top break-words overflow-hidden';

export default function TransitLuckyTab({ kundliId, language }: Props) {
  const { t } = useTranslation();
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
      .catch((err: any) => { if (!cancelled) setError(err?.message || t('auto.genericError')); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) return (
    <div className="flex items-center justify-center py-12">
      <Loader2 className="w-6 h-6 animate-spin text-primary" />
    </div>
  );
  if (error) return (
    <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
  );
  if (!data) return null;

  const luckyColor     = isHi ? data.lucky_color?.hi     : data.lucky_color?.en;
  const compatSign     = isHi ? data.compatible_sign?.hi : data.compatible_sign?.en;
  const mood           = isHi ? data.mood?.hi            : data.mood?.en;
  const luckyTime      = isHi ? data.lucky_time?.hi      : data.lucky_time?.en;
  const gemstoneName   = isHi ? data.gemstone?.name_hi   : data.gemstone?.name_en;
  const gemstoneBenefit= isHi ? data.gemstone?.benefit_hi: data.gemstone?.benefit_en;

  return (
    <div className="space-y-4">

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

      {/* Lucky facts table */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Star className="w-4 h-4" />
          <span>{isHi ? 'शुभ संकेतक' : 'Lucky Indicators'}</span>
        </div>
        <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '38%' }} />
            <col style={{ width: '62%' }} />
          </colgroup>
          <thead>
            <tr>
              <th className={thCls}>{isHi ? 'संकेतक' : 'Indicator'}</th>
              <th className={thCls}>{isHi ? 'मान' : 'Value'}</th>
            </tr>
          </thead>
          <tbody>
            {data.lucky_number != null && (
              <tr>
                <td className={tdLbl}>{isHi ? 'शुभ अंक' : 'Lucky Number'}</td>
                <td className={tdVal}>
                  <span className="text-2xl font-extrabold text-sacred-gold-dark">{data.lucky_number}</span>
                </td>
              </tr>
            )}
            {luckyColor && (
              <tr>
                <td className={tdLbl}>{isHi ? 'शुभ रंग' : 'Lucky Color'}</td>
                <td className={tdVal}>
                  <div className="flex items-center gap-2">
                    <div className={`w-4 h-4 rounded-full shrink-0 ${colorSwatch(data.lucky_color?.en ?? '')}`} />
                    {luckyColor}
                  </div>
                </td>
              </tr>
            )}
            {compatSign && (
              <tr>
                <td className={tdLbl}>{isHi ? 'अनुकूल राशि' : 'Compatible Sign'}</td>
                <td className={tdVal}>{compatSign}</td>
              </tr>
            )}
            {mood && (
              <tr>
                <td className={tdLbl}>{isHi ? 'मनोभाव' : 'Mood'}</td>
                <td className={tdVal}>{mood}</td>
              </tr>
            )}
            {luckyTime && (
              <tr>
                <td className={tdLbl}>{isHi ? 'शुभ समय' : 'Lucky Time'}</td>
                <td className={tdVal}>{luckyTime}</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Do's and Don'ts */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {(data.dos?.length ?? 0) > 0 && (
          <div className={ohContainer}>
            <div className="bg-emerald-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              <span>{isHi ? 'करें' : "Do's"}</span>
            </div>
            <ul className="divide-y divide-border">
              {data.dos.map((item, i) => (
                <li key={i} className="flex items-start gap-2 px-4 py-2.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 mt-0.5 shrink-0" />
                  <span className="text-xs text-foreground leading-relaxed">
                    {isHi ? item.hi : item.en}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {(data.donts?.length ?? 0) > 0 && (
          <div className={ohContainer}>
            <div className="bg-red-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
              <XCircle className="w-4 h-4" />
              <span>{isHi ? 'न करें' : "Don'ts"}</span>
            </div>
            <ul className="divide-y divide-border">
              {data.donts.map((item, i) => (
                <li key={i} className="flex items-start gap-2 px-4 py-2.5">
                  <XCircle className="w-3.5 h-3.5 text-red-500 mt-0.5 shrink-0" />
                  <span className="text-xs text-foreground leading-relaxed">
                    {isHi ? item.hi : item.en}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Gemstone wear details */}
      {data.gemstone && gemstoneName && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Gem className="w-4 h-4" />
            <span>{isHi ? 'शुभ रत्न — धारण विधि' : 'Lucky Gemstone — How to Wear'}</span>
            <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded text-amber-200">
              {gemstoneName}
            </span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '38%' }} />
              <col style={{ width: '62%' }} />
            </colgroup>
            <tbody>
              <tr>
                <td className={tdLbl}>{isHi ? 'रत्न' : 'Stone'}</td>
                <td className={tdVal}><span className="text-amber-700 font-semibold">{gemstoneName}</span></td>
              </tr>
              {(isHi ? data.gemstone.benefit_hi : data.gemstone.benefit_en) && (
                <tr>
                  <td className={tdLbl}>{isHi ? 'धातु' : 'Metal'}</td>
                  <td className={tdVal}>{isHi ? data.gemstone.benefit_hi : data.gemstone.benefit_en}</td>
                </tr>
              )}
              {(isHi ? data.gemstone.finger_hi : data.gemstone.finger_en) && (
                <tr>
                  <td className={tdLbl}>{isHi ? 'उँगली' : 'Finger'}</td>
                  <td className={tdVal}>{isHi ? data.gemstone.finger_hi : data.gemstone.finger_en}</td>
                </tr>
              )}
              {(isHi ? data.gemstone.day_hi : data.gemstone.day_en) && (
                <tr>
                  <td className={tdLbl}>{isHi ? 'धारण दिन' : 'Wear Day'}</td>
                  <td className={tdVal}>{isHi ? data.gemstone.day_hi : data.gemstone.day_en}</td>
                </tr>
              )}
            </tbody>
          </table>
          <div className="px-4 py-2 border-t border-border text-[11px] text-muted-foreground italic">
            {isHi ? 'चन्द्र राशि स्वामी के आधार पर चयनित' : 'Selected based on Moon sign ruling planet'}
          </div>
        </div>
      )}

      {/* Mantra */}
      {data.mantra && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <BookOpen className="w-4 h-4" />
            <span>{isHi ? 'मंत्र' : 'Mantra'}</span>
          </div>
          <div className="px-4 py-4 text-center">
            <p className="text-base font-semibold text-sacred-gold-dark italic leading-relaxed">
              {data.mantra}
            </p>
          </div>
        </div>
      )}
      <TimingTheorySection language={language || 'en'} tab="transit-lucky" />
    </div>
  );
}
