import { useState, useEffect } from 'react';
import { Loader2, Sparkles, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface NadiInsight {
  house: number | null;
  title_en: string;
  title_hi: string;
  desc_en: string;
  desc_hi: string;
  planets: string[];
  type?: string;
  houses?: number[];
}

interface NadiAnalysisData {
  kundli_id?: string;
  person_name?: string;
  insights: NadiInsight[];
}

interface Props {
  kundliId: string;
  language?: string;
}

const PLANET_COLORS: Record<string, string> = {
  Sun:     'bg-amber-100 border-amber-300 text-amber-800',
  Moon:    'bg-blue-100 border-blue-300 text-blue-700',
  Mars:    'bg-red-100 border-red-300 text-red-700',
  Mercury: 'bg-green-100 border-green-300 text-green-700',
  Jupiter: 'bg-yellow-100 border-yellow-300 text-yellow-800',
  Venus:   'bg-pink-100 border-pink-300 text-pink-700',
  Saturn:  'bg-gray-100 border-gray-300 text-gray-700',
  Rahu:    'bg-purple-100 border-purple-300 text-purple-700',
  Ketu:    'bg-orange-100 border-orange-300 text-orange-700',
};

const TYPE_BADGE: Record<string, { en: string; hi: string; cls: string }> = {
  conjunction:   { en: 'Conjunction',   hi: 'युति',         cls: 'bg-indigo-100 text-indigo-800' },
  placement:     { en: 'Placement',     hi: 'स्थान फल',    cls: 'bg-teal-100 text-teal-800' },
  mutual_aspect: { en: 'Mutual Aspect', hi: 'परस्पर दृष्टि', cls: 'bg-purple-100 text-purple-800' },
  cluster:       { en: 'Cluster',       hi: 'समूह',         cls: 'bg-gray-100 text-gray-700' },
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

export default function NadiAnalysisTab({ kundliId, language }: Props) {
  const [data, setData] = useState<NadiAnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api.get<NadiAnalysisData>(`/api/kundli/${kundliId}/nadi-analysis`)
      .then(res => { if (!cancelled) setData(res); })
      .catch((err: any) => { if (!cancelled) setError(err?.message || 'Failed to load Nadi Analysis'); })
      .finally(() => { if (!cancelled) setLoading(false); });
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

  const insights = data.insights ?? [];

  return (
    <div className="space-y-4">

      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {isHi ? 'नाड़ी विश्लेषण' : 'Nadi Analysis'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi
            ? 'नाड़ी ग्रह-युति के आधार पर शास्त्रीय योग-फल का विश्लेषण'
            : 'Classical Nadi Yoga analysis based on planetary conjunctions'}
        </p>
        {data.person_name && (
          <p className="text-xs text-muted-foreground mt-0.5 font-medium">{data.person_name}</p>
        )}
      </div>

      {insights.length === 0 ? (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Sparkles className="w-4 h-4" />
            <span>{isHi ? 'नाड़ी योग' : 'Nadi Yogas'}</span>
          </div>
          <div className="px-4 py-8 text-center text-sm text-muted-foreground">
            {isHi ? 'इस कुंडली में कोई नाड़ी ग्रह-युति नहीं मिली' : 'No Nadi conjunctions found in this chart'}
          </div>
        </div>
      ) : (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Sparkles className="w-4 h-4" />
            <span>{isHi ? 'नाड़ी योग विश्लेषण' : 'Nadi Yoga Analysis'}</span>
            <span className="ml-auto text-[12px] font-normal opacity-80">{insights.length}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '9%' }} />
              <col style={{ width: '14%' }} />
              <col style={{ width: '19%' }} />
              <col style={{ width: '18%' }} />
              <col style={{ width: '40%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'भाव' : 'House'}</th>
                <th className={thCls}>{isHi ? 'प्रकार' : 'Type'}</th>
                <th className={thCls}>{isHi ? 'योग नाम' : 'Yoga'}</th>
                <th className={thCls}>{isHi ? 'ग्रह' : 'Planets'}</th>
                <th className={thCls}>{isHi ? 'फल' : 'Effect'}</th>
              </tr>
            </thead>
            <tbody>
              {insights.map((insight, i) => {
                const title = isHi ? insight.title_hi : insight.title_en;
                const desc  = isHi ? insight.desc_hi  : insight.desc_en;
                const tb    = insight.type ? TYPE_BADGE[insight.type] : null;

                const houseCell = insight.type === 'mutual_aspect' && (insight.houses?.length ?? 0) >= 2
                  ? `H${insight.houses![0]}↔H${insight.houses![1]}`
                  : insight.house ? `H${insight.house}` : '—';

                return (
                  <tr key={i}>
                    <td className={`${tdCls} font-semibold text-center`}>
                      <span className="px-1.5 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark text-[11px] font-bold">
                        {houseCell}
                      </span>
                    </td>
                    <td className={tdCls}>
                      {tb ? (
                        <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${tb.cls}`}>
                          {isHi ? tb.hi : tb.en}
                        </span>
                      ) : '—'}
                    </td>
                    <td className={tdWrapCls}>
                      <p className="font-semibold text-foreground">{title}</p>
                    </td>
                    <td className={tdCls}>
                      <div className="flex flex-wrap gap-1">
                        {(insight.planets ?? []).map((p, j) => (
                          <span
                            key={j}
                            className={`px-1.5 py-0.5 rounded-full border text-[10px] font-semibold ${PLANET_COLORS[p] ?? 'bg-sacred-gold/10 border-sacred-gold/30 text-sacred-gold-dark'}`}
                          >
                            {isHi ? (PLANET_HI[p] || p) : p}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className={tdWrapCls}>{desc || '—'}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Footer */}
      <div className="flex items-start gap-2 px-1 text-[11px] text-muted-foreground">
        <BookOpen className="w-3 h-3 shrink-0 mt-0.5" />
        <span className="italic">
          {isHi
            ? 'नाड़ी ज्योतिष — ग्रहों की युति-स्थिति के आधार पर सूक्ष्म फल-कथन की प्राचीन विधि'
            : 'Nadi Jyotisha — ancient predictive method based on planetary conjunction positions'}
        </span>
      </div>
    </div>
  );
}
