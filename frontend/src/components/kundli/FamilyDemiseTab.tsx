import { useState, useEffect } from 'react';
import { Loader2, Heart, BookOpen, Info, ShieldCheck } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface HealthIndicator {
  indicator_en: string;
  indicator_hi?: string;
  planet: string;
  strength?: 'strong' | 'moderate' | 'weak' | string;
}

interface FamilyMember {
  member_en: string;
  member_hi?: string;
  house: number;
  indicators: HealthIndicator[];
  overall_risk: 'high' | 'moderate' | 'low';
}

interface FamilyDemiseData {
  kundli_id?: string;
  person_name?: string;
  members: FamilyMember[];
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

const RISK_STYLE: Record<string, { card: string; badge: string; label: string; labelHi: string }> = {
  high:     { card: 'border-amber-300 bg-amber-50',   badge: 'bg-amber-600 text-white',  label: 'Needs Attention', labelHi: 'ध्यान आवश्यक' },
  moderate: { card: 'border-blue-200 bg-blue-50',      badge: 'bg-blue-500 text-white',   label: 'Moderate',        labelHi: 'मध्यम' },
  low:      { card: 'border-emerald-200 bg-emerald-50', badge: 'bg-emerald-600 text-white', label: 'Favourable',      labelHi: 'अनुकूल' },
};

const INDICATOR_STRENGTH: Record<string, string> = {
  strong:   'text-amber-700 font-semibold',
  moderate: 'text-blue-700',
  weak:     'text-gray-500',
};

export default function FamilyDemiseTab({ kundliId, language }: Props) {
  const [data, setData] = useState<FamilyDemiseData | null>(null);
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
        const res = await api.get(`/api/kundli/${kundliId}/family-demise-timing`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Family Health & Longevity analysis');
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
  const members = data.members || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Heart className="w-6 h-6" />
          {hi ? 'परिवार स्वास्थ्य एवं दीर्घायु विश्लेषण' : 'Family Member Health & Longevity Analysis'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'कुंडली में परिवार के सदस्यों के स्वास्थ्य एवं दीर्घायु से सम्बन्धित संकेत'
            : 'Astrological indicators related to family members\' health and longevity in the chart'}
        </p>
      </div>

      {/* Sensitivity disclaimer — prominent */}
      <div className="rounded-xl border-2 border-blue-300 bg-blue-50 p-4 flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-blue-700 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="text-sm font-semibold text-blue-900">
            {hi ? 'शास्त्रीय विश्लेषण — कोई भविष्यवाणी नहीं' : 'Classical Analysis — Not a Prediction'}
          </p>
          <p className="text-xs text-blue-800 leading-relaxed">
            {hi
              ? 'यह विश्लेषण पारम्परिक ज्योतिष-शास्त्र पर आधारित है। इसे किसी की मृत्यु या स्वास्थ्य की निश्चित भविष्यवाणी न समझें। सभी जीवन-घटनाएँ अनेक कारकों पर निर्भर करती हैं।'
              : 'This analysis is based on traditional Jyotish principles. It should not be interpreted as a definitive prediction of anyone\'s death or health outcome. Life events depend on many factors beyond astrological indicators.'}
          </p>
        </div>
      </div>

      {/* Summary */}
      {(data.summary_en || data.summary_hi) && (
        <div className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 px-4 py-3 flex items-start gap-2">
          <Info className="w-4 h-4 text-sacred-gold-dark shrink-0 mt-0.5" />
          <p className="text-sm text-foreground/85 leading-relaxed">
            {hi ? (data.summary_hi || data.summary_en) : data.summary_en}
          </p>
        </div>
      )}

      {/* Member cards */}
      {members.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {members.map((member, idx) => {
            const riskStyle = RISK_STYLE[member.overall_risk] || RISK_STYLE.moderate;
            const memberName = hi ? (member.member_hi || member.member_en) : member.member_en;

            return (
              <div
                key={idx}
                className={`rounded-xl border-2 p-5 space-y-3 ${riskStyle.card}`}
              >
                {/* Member header */}
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="font-bold text-sacred-brown text-base">{memberName}</h3>
                    {member.house > 0 && (
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {hi ? `भाव ${member.house} से सम्बन्धित` : `Signified by House ${member.house}`}
                      </p>
                    )}
                  </div>
                  <span className={`shrink-0 text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded ${riskStyle.badge}`}>
                    {hi ? riskStyle.labelHi : riskStyle.label}
                  </span>
                </div>

                {/* Indicators */}
                {member.indicators && member.indicators.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide">
                      {hi ? 'ज्योतिष संकेत' : 'Astrological Indicators'}
                    </p>
                    <div className="space-y-1.5">
                      {member.indicators.map((ind, i) => {
                        const indicatorText = hi ? (ind.indicator_hi || ind.indicator_en) : ind.indicator_en;
                        const strengthClass = ind.strength
                          ? (INDICATOR_STRENGTH[ind.strength] || INDICATOR_STRENGTH.moderate)
                          : 'text-foreground/80';

                        return (
                          <div
                            key={i}
                            className="flex items-start gap-2 rounded-lg bg-white/70 border border-white/50 px-3 py-2 text-xs"
                          >
                            {/* Planet chip */}
                            <span className="shrink-0 font-bold text-sacred-gold-dark bg-sacred-gold/10 border border-sacred-gold/20 px-1.5 py-0.5 rounded text-[10px]">
                              {planetName(ind.planet)}
                            </span>
                            {/* Indicator text */}
                            <span className={`leading-relaxed flex-1 ${strengthClass}`}>
                              {indicatorText}
                            </span>
                            {/* Strength badge */}
                            {ind.strength && (
                              <span className={`shrink-0 text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ml-1 ${
                                ind.strength === 'strong'   ? 'bg-amber-100 text-amber-800' :
                                ind.strength === 'moderate' ? 'bg-blue-100 text-blue-800'   :
                                'bg-gray-100 text-gray-600'
                              }`}>
                                {ind.strength === 'strong'   ? (hi ? 'बलवान' : 'Strong')   :
                                 ind.strength === 'moderate' ? (hi ? 'मध्यम' : 'Moderate') :
                                 (hi ? 'निर्बल' : 'Weak')}
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {(!member.indicators || member.indicators.length === 0) && (
                  <p className="text-xs text-muted-foreground italic">
                    {hi ? 'कोई विशेष संकेत नहीं।' : 'No specific indicators found.'}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="p-6 text-center text-muted-foreground text-sm italic">
          {hi ? 'परिवार स्वास्थ्य डेटा उपलब्ध नहीं।' : 'No family health data available.'}
        </div>
      )}

      {/* Risk legend */}
      <div className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 px-4 py-3">
        <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-2">
          {hi ? 'संकेत स्तर' : 'Indicator Levels'}
        </p>
        <div className="flex flex-wrap gap-2 text-xs">
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-100 border border-emerald-200 text-emerald-800">
            <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
            {hi ? 'अनुकूल — सुरक्षित संकेत' : 'Favourable — Protective indicators'}
          </span>
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-100 border border-blue-200 text-blue-800">
            <span className="w-2 h-2 rounded-full bg-blue-500 shrink-0" />
            {hi ? 'मध्यम — सावधानी अपेक्षित' : 'Moderate — Some caution advised'}
          </span>
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-100 border border-amber-200 text-amber-800">
            <span className="w-2 h-2 rounded-full bg-amber-500 shrink-0" />
            {hi ? 'ध्यान आवश्यक — एकाधिक तनाव-संकेत' : 'Needs Attention — Multiple stress indicators'}
          </span>
        </div>
      </div>

      {/* Footer sloka ref */}
      {data.sloka_ref && (
        <div className="flex items-center gap-2 pt-2 border-t border-sacred-gold/20 text-[11px] text-muted-foreground italic">
          <BookOpen className="w-3 h-3 text-sacred-gold-dark shrink-0" />
          <span>{data.sloka_ref}</span>
        </div>
      )}
    </div>
  );
}
