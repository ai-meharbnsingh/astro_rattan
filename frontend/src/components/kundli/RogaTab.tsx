import { useState, useEffect } from 'react';
import { Loader2, Activity, AlertTriangle, Clock, MapPin, HeartPulse, Info, BookOpen, ShieldAlert, Home } from 'lucide-react';
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

interface AfflictedPlanetDisease {
  planet: string;
  affliction_type: 'debilitated' | 'combust' | 'aspected_by_malefic';
  diseases_en: string[];
  diseases_hi: string[];
  severity: 'high' | 'moderate' | 'low';
}

interface SixthHouseProfile {
  sign: string;
  prone_areas_en: string[];
  prone_areas_hi: string[];
  note_en: string;
  note_hi: string;
}

interface RogaData {
  kundli_id?: string;
  person_name?: string;
  general_tendencies: GeneralTendency[];
  special_yogas_detected: SpecialYoga[];
  timing_indicators: TimingIndicator[];
  body_parts_affected: BodyPart[];
  remedy_suggestions: RemedySuggestion[];
  afflicted_planet_diseases?: AfflictedPlanetDisease[];
  sixth_house_disease_profile?: SixthHouseProfile | null;
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
                  <span className="font-semibold">{t('auto.trigger')}:</span>{' '}
                  {isHi ? y.trigger_hi : y.trigger_en}
                </p>
                <p className="text-xs leading-relaxed mb-2">
                  <span className="font-semibold">{t('auto.remedy')}:</span>{' '}
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
            {t('auto.noMajorTendencies')}
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
                      {g.planet} — {t('auto.house')} {g.house}
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

      {/* 9-Planet Disease Matrix */}
      {data.afflicted_planet_diseases && data.afflicted_planet_diseases.length > 0 && (
        <section>
          <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5" />
            {isHi ? 'नौ ग्रह रोग विश्लेषण' : 'Planet Affliction Disease Matrix'}
          </h3>
          <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-muted/30">
                  <th className="text-left p-3 text-sacred-gold-dark font-bold border-b border-sacred-gold/15">{isHi ? 'ग्रह' : 'Planet'}</th>
                  <th className="text-left p-3 text-sacred-gold-dark font-bold border-b border-sacred-gold/15">{isHi ? 'पीड़ा का प्रकार' : 'Affliction'}</th>
                  <th className="text-left p-3 text-sacred-gold-dark font-bold border-b border-sacred-gold/15">{isHi ? 'संभावित रोग' : 'Potential Diseases'}</th>
                  <th className="text-center p-3 text-sacred-gold-dark font-bold border-b border-sacred-gold/15">{isHi ? 'गंभीरता' : 'Severity'}</th>
                </tr>
              </thead>
              <tbody>
                {data.afflicted_planet_diseases.map((apd, i) => {
                  const afflictionLabel: Record<string, { en: string; hi: string }> = {
                    debilitated:         { en: 'Debilitated',       hi: 'नीच राशि में' },
                    combust:             { en: 'Combust',            hi: 'अस्त' },
                    aspected_by_malefic: { en: 'Malefic Aspect',    hi: 'पाप ग्रह की दृष्टि' },
                  };
                  const aLabel = afflictionLabel[apd.affliction_type] || { en: apd.affliction_type, hi: apd.affliction_type };
                  const diseases = isHi ? apd.diseases_hi : apd.diseases_en;
                  return (
                    <tr key={i} className="border-t border-sacred-gold/10 hover:bg-muted/20">
                      <td className="p-3 font-bold text-foreground">{apd.planet}</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded text-[10px] font-black uppercase bg-orange-100 text-orange-800 border border-orange-300">
                          {isHi ? aLabel.hi : aLabel.en}
                        </span>
                      </td>
                      <td className="p-3 text-foreground text-xs leading-relaxed">
                        {diseases.slice(0, 3).join(', ')}
                        {diseases.length > 3 && <span className="text-muted-foreground"> +{diseases.length - 3} more</span>}
                      </td>
                      <td className="p-3 text-center">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase border ${SEVERITY_COLOR[apd.severity] || SEVERITY_COLOR.moderate}`}>
                          {t(SEVERITY_KEY[apd.severity] || 'auto.severityModerate')}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {/* 6th House Disease Profile */}
      {data.sixth_house_disease_profile && (
        <section>
          <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <Home className="w-5 h-5" />
            {isHi ? 'षष्ठ भाव रोग प्रवृत्ति' : '6th House Disease Profile'}
          </h3>
          <div className="p-4 rounded-xl border border-sacred-gold/25 bg-sacred-gold/5">
            <div className="flex items-center gap-2 mb-3">
              <span className="font-bold text-sacred-gold-dark text-lg">
                {isHi ? 'षष्ठ भाव राशि' : '6th House Sign'}:
              </span>
              <span className="px-3 py-1 rounded-full bg-sacred-gold/20 border border-sacred-gold/40 font-bold text-sacred-gold-dark">
                {data.sixth_house_disease_profile.sign}
              </span>
            </div>
            <p className="text-sm text-foreground mb-3 leading-relaxed">
              {isHi ? data.sixth_house_disease_profile.note_hi : data.sixth_house_disease_profile.note_en}
            </p>
            <div>
              <p className="text-xs font-semibold text-foreground/70 mb-1 uppercase tracking-wide">
                {isHi ? 'प्रवृत्त क्षेत्र' : 'Prone Areas'}
              </p>
              <div className="flex flex-wrap gap-2">
                {(isHi ? data.sixth_house_disease_profile.prone_areas_hi : data.sixth_house_disease_profile.prone_areas_en).map((area, i) => (
                  <span key={i} className="px-2 py-0.5 rounded-full text-xs bg-red-50 text-red-800 border border-red-200">
                    {area}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

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
