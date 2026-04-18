import { useState, useEffect } from 'react';
import { Loader2, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface NadiInsight {
  house: number;
  title_en: string;
  title_hi: string;
  desc_en: string;
  desc_hi: string;
  planets: string[];
}

interface NadiAnalysisData {
  insights: NadiInsight[];
}

interface Props {
  kundliId: string;
  language?: string;
}

const HOUSE_LABELS: Record<number, string> = {
  1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th',
  7: '7th', 8: '8th', 9: '9th', 10: '10th', 11: '11th', 12: '12th',
};

const HOUSE_LABELS_HI: Record<number, string> = {
  1: 'प्रथम', 2: 'द्वितीय', 3: 'तृतीय', 4: 'चतुर्थ', 5: 'पञ्चम', 6: 'षष्ठ',
  7: 'सप्तम', 8: 'अष्टम', 9: 'नवम', 10: 'दशम', 11: 'एकादश', 12: 'द्वादश',
};

const PLANET_COLORS: Record<string, string> = {
  Sun: 'bg-amber-100 border-amber-300 text-amber-800',
  Moon: 'bg-blue-100 border-blue-300 text-blue-700',
  Mars: 'bg-red-100 border-red-300 text-red-700',
  Mercury: 'bg-green-100 border-green-300 text-green-700',
  Jupiter: 'bg-yellow-100 border-yellow-300 text-yellow-800',
  Venus: 'bg-pink-100 border-pink-300 text-pink-700',
  Saturn: 'bg-gray-100 border-gray-300 text-gray-700',
  Rahu: 'bg-purple-100 border-purple-300 text-purple-700',
  Ketu: 'bg-orange-100 border-orange-300 text-orange-700',
};

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

  const insights = data.insights ?? [];

  return (
    <div className="space-y-6">
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
      </div>

      {insights.length === 0 ? (
        <div className="p-8 rounded-xl border border-sacred-gold/20 bg-white/50 text-center">
          <Sparkles className="w-10 h-10 text-sacred-gold/40 mx-auto mb-3" />
          <p className="text-sm text-muted-foreground">
            {isHi
              ? 'इस कुंडली में कोई नाड़ी ग्रह-युति नहीं मिली'
              : 'No Nadi planetary conjunctions found in this chart'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {insights.map((insight, i) => {
            const title = isHi ? insight.title_hi : insight.title_en;
            const desc = isHi ? insight.desc_hi : insight.desc_en;
            const houseLabel = isHi
              ? (HOUSE_LABELS_HI[insight.house] ?? `${insight.house}`)
              : (HOUSE_LABELS[insight.house] ?? `${insight.house}`);

            return (
              <div
                key={i}
                className="rounded-xl border border-sacred-gold/20 bg-white/50 p-4 space-y-3"
              >
                {/* Card header */}
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-sacred-gold-dark text-base leading-tight">
                      {title}
                    </h3>
                    {/* Bilingual title toggle */}
                    {!isHi && insight.title_hi && (
                      <p className="text-xs text-muted-foreground mt-0.5">{insight.title_hi}</p>
                    )}
                    {isHi && insight.title_en && (
                      <p className="text-xs text-muted-foreground mt-0.5">{insight.title_en}</p>
                    )}
                  </div>
                  {insight.house > 0 && (
                    <span className="shrink-0 px-2.5 py-1 rounded-lg bg-sacred-gold/10 border border-sacred-gold/30 text-sacred-gold-dark text-xs font-semibold">
                      {isHi ? `${houseLabel} भाव` : `${houseLabel} House`}
                    </span>
                  )}
                </div>

                {/* Planets as badges */}
                {(insight.planets?.length ?? 0) > 0 && (
                  <div className="flex flex-wrap gap-1.5">
                    {insight.planets.map((planet, j) => (
                      <span
                        key={j}
                        className={`px-2.5 py-0.5 rounded-full border text-xs font-semibold ${
                          PLANET_COLORS[planet] ?? 'bg-sacred-gold/10 border-sacred-gold/30 text-sacred-gold-dark'
                        }`}
                      >
                        {planet}
                      </span>
                    ))}
                  </div>
                )}

                {/* Description */}
                {desc && (
                  <div className="pt-2 border-t border-sacred-gold/10 space-y-1">
                    <p className="text-sm text-foreground/90 leading-relaxed">{desc}</p>
                    {/* Secondary language description */}
                    {!isHi && insight.desc_hi && (
                      <p className="text-xs text-muted-foreground leading-relaxed">{insight.desc_hi}</p>
                    )}
                    {isHi && insight.desc_en && (
                      <p className="text-xs text-muted-foreground leading-relaxed">{insight.desc_en}</p>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Footer note */}
      <div className="p-4 rounded-lg bg-sacred-gold/5 border border-sacred-gold/20 text-xs text-muted-foreground flex items-start gap-2">
        <Sparkles className="w-4 h-4 text-sacred-gold-dark shrink-0 mt-0.5" />
        <span>
          {isHi
            ? 'नाड़ी ज्योतिष — ग्रहों की युति-स्थिति के आधार पर सूक्ष्म फल-कथन की प्राचीन विधि'
            : 'Nadi Jyotisha — ancient predictive method based on planetary conjunction positions'}
        </span>
      </div>
    </div>
  );
}
