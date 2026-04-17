import { useState, useEffect } from 'react';
import { Loader2, Activity, AlertTriangle, Clock, MapPin, HeartPulse, Info, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface GeneralTendency {
  planet: string;
  house: number;
  severity: 'low' | 'moderate' | 'severe' | 'chronic';
  diseases_en: string[];
  diseases_hi: string[];
  body_part_en: string;
  body_part_hi: string;
  reason_en: string;
  reason_hi: string;
}

interface SpecialYoga {
  key: string;
  name_en: string;
  name_hi: string;
  trigger_en: string;
  trigger_hi: string;
  severity: 'low' | 'moderate' | 'severe';
  remedy_en: string;
  remedy_hi: string;
  sloka_ref: string;
}

interface BodyPart {
  house: number;
  part_en: string;
  part_hi: string;
  due_to_en: string;
  due_to_hi: string;
}

interface TimingIndicator {
  en: string;
  hi: string;
}

interface RemedySuggestion {
  for_en: string;
  for_hi: string;
  remedy_en: string;
  remedy_hi: string;
}

interface RogaData {
  kundli_id?: string;
  person_name?: string;
  general_tendencies: GeneralTendency[];
  special_yogas_detected: SpecialYoga[];
  timing_indicators: TimingIndicator[];
  body_parts_affected: BodyPart[];
  remedy_suggestions: RemedySuggestion[];
  sloka_ref: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const SEVERITY_COLOR: Record<string, string> = {
  low: 'bg-emerald-100 text-emerald-800 border-emerald-300',
  moderate: 'bg-amber-100 text-amber-800 border-amber-300',
  severe: 'bg-red-100 text-red-800 border-red-300',
  chronic: 'bg-red-200 text-red-900 border-red-400',
};

const SEVERITY_KEY: Record<string, string> = {
  low: 'auto.severityLow',
  moderate: 'auto.severityModerate',
  severe: 'auto.severitySevere',
  chronic: 'auto.severityChronic',
};

export default function RogaTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<RogaData | null>(null);
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
        const res = await api.get<RogaData>(`/api/kundli/${kundliId}/roga-analysis`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load disease analysis');
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <HeartPulse className="w-6 h-6" />
          {t('auto.rogaAnalysis')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.rogaDesc')}</p>
      </div>

      {/* Disclaimer */}
      <div className="p-3 rounded-lg bg-blue-50 border border-blue-200 text-blue-800 text-xs flex items-start gap-2">
        <Info className="w-4 h-4 shrink-0 mt-0.5" />
        <p>{t('auto.disclaimerHealth')}</p>
      </div>

      {/* Special Yogas */}
      <section>
        <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5" />
          {t('auto.specialDiseaseYogas')}
        </h3>
        {data.special_yogas_detected.length === 0 ? (
          <div className="p-4 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm">
            {t('auto.noRogaYogas')}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {data.special_yogas_detected.map((y, i) => (
              <div
                key={`${y.key}-${i}`}
                className={`rounded-xl border-2 p-4 ${SEVERITY_COLOR[y.severity] || SEVERITY_COLOR.moderate}`}
              >
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h4 className="font-bold">{isHi ? y.name_hi : y.name_en}</h4>
                  <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-white/60">
                    {t(SEVERITY_KEY[y.severity] || 'auto.severityModerate')}
                  </span>
                </div>
                <p className="text-xs leading-relaxed mb-2 opacity-90">
                  <span className="font-semibold">{isHi ? 'ट्रिगर' : 'Trigger'}:</span>{' '}
                  {isHi ? y.trigger_hi : y.trigger_en}
                </p>
                <p className="text-xs leading-relaxed mb-2">
                  <span className="font-semibold">{isHi ? 'उपाय' : 'Remedy'}:</span>{' '}
                  {isHi ? y.remedy_hi : y.remedy_en}
                </p>
                <div className="flex items-center gap-1.5 mt-2 pt-2 border-t border-current/15 text-[10px] opacity-70">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{y.sloka_ref}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* General tendencies */}
      <section>
        <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Activity className="w-5 h-5" />
          {t('auto.diseaseTendencies')}
        </h3>
        {data.general_tendencies.length === 0 ? (
          <div className="p-4 rounded-lg bg-gray-50 border border-gray-200 text-gray-700 text-sm">
            {isHi ? 'कोई मुख्य प्रवृत्ति नहीं' : 'No major tendencies detected'}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {data.general_tendencies.map((g, i) => (
              <div
                key={`${g.planet}-${i}`}
                className={`rounded-xl border-2 p-4 ${SEVERITY_COLOR[g.severity] || SEVERITY_COLOR.moderate}`}
              >
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div>
                    <p className="font-bold">
                      {g.planet} — {isHi ? 'भाव' : 'House'} {g.house}
                    </p>
                    <p className="text-[11px] opacity-80">
                      {isHi ? g.body_part_hi : g.body_part_en}
                    </p>
                  </div>
                  <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-white/60">
                    {t(SEVERITY_KEY[g.severity] || 'auto.severityModerate')}
                  </span>
                </div>
                <ul className="list-disc pl-4 text-xs space-y-0.5">
                  {(isHi ? g.diseases_hi : g.diseases_en).map((d, di) => (
                    <li key={di}>{d}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Body parts */}
      {data.body_parts_affected.length > 0 && (
        <section>
          <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <MapPin className="w-5 h-5" />
            {t('auto.bodyPartsAffected')}
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
            {data.body_parts_affected.map((b, i) => (
              <div
                key={i}
                className="p-3 rounded-lg border border-sacred-gold/25 bg-sacred-gold/5 text-sm"
              >
                <p className="font-semibold text-foreground">
                  {isHi ? 'भाव' : 'House'} {b.house}: {isHi ? b.part_hi : b.part_en}
                </p>
                <p className="text-[11px] text-muted-foreground mt-0.5">
                  {isHi ? 'कारण' : 'Due to'}: {isHi ? b.due_to_hi : b.due_to_en}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Timing */}
      {data.timing_indicators.length > 0 && (
        <section>
          <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <Clock className="w-5 h-5" />
            {t('auto.timingIndicators')}
          </h3>
          <ul className="space-y-1.5">
            {data.timing_indicators.map((ti, i) => (
              <li
                key={i}
                className="flex items-start gap-2 text-sm p-3 rounded-lg border border-sacred-gold/20 bg-white"
              >
                <Clock className="w-3.5 h-3.5 text-sacred-gold-dark shrink-0 mt-0.5" />
                <span>{isHi ? ti.hi : ti.en}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Sloka ref footer */}
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground pt-2 border-t border-sacred-gold/15">
        <BookOpen className="w-3 h-3" />
        <span className="italic">{data.sloka_ref}</span>
      </div>
    </div>
  );
}
