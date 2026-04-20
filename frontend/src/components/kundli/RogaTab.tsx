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

const SEV: Record<string, string> = {
  low:      'bg-emerald-100 text-emerald-800',
  moderate: 'bg-amber-100 text-amber-800',
  severe:   'bg-red-100 text-red-800',
  chronic:  'bg-red-200 text-red-900',
  high:     'bg-red-100 text-red-800',
};
const SEV_KEY: Record<string, string> = {
  low:      'auto.severityLow',
  moderate: 'auto.severityModerate',
  severe:   'auto.severitySevere',
  chronic:  'auto.severityChronic',
  high:     'auto.severitySevere',
};

const AFFLICTION_LABEL: Record<string, { en: string; hi: string }> = {
  debilitated:         { en: 'Debilitated',    hi: 'नीच राशि में' },
  combust:             { en: 'Combust',         hi: 'अस्त' },
  aspected_by_malefic: { en: 'Malefic Aspect', hi: 'पाप ग्रह की दृष्टि' },
};

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const thCenterCls = 'p-1.5 text-center text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdWrapCls   = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

function extractDateRange(text: string): { raw: string; label: string } | null {
  // "2025–2027" / "2025-2027" / "2025 to 2027"
  const range = text.match(/\b(20\d\d)\s*[-–—to]+\s*(20\d\d)\b/);
  if (range) return { raw: range[0], label: `${range[1]}–${range[2]}` };
  // "during 2026" / "in 2025"
  const single = text.match(/\b(20\d\d)\b/);
  if (single) return { raw: single[0], label: single[1] };
  // dasha period like "Sun–Moon dasha" or "Saturn dasha"
  const dasha = text.match(/\b(\w+[\s–\-]+(?:\w+\s+)?dasha)\b/i);
  if (dasha) return { raw: dasha[0], label: dasha[1] };
  return null;
}

function Points({ text }: { text: string }) {
  if (!text) return null;
  const pts = text.split(/[.;]\s+/).map(s => s.replace(/[.;]$/, '').trim()).filter(Boolean);
  if (pts.length <= 1) return <span>{text}</span>;
  return (
    <ul className="space-y-0.5">
      {pts.map((p, i) => (
        <li key={i} className="flex items-start gap-1">
          <span className="text-sacred-gold-dark mt-0.5 shrink-0">•</span>
          <span>{p}</span>
        </li>
      ))}
    </ul>
  );
}

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
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-sm text-foreground">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1">
          {isHi ? 'रोग विश्लेषण' : 'Disease Analysis'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi ? 'कुंडली से स्वास्थ्य कमजोरियाँ और रोग प्रवृत्तियाँ' : 'Health vulnerabilities and disease tendencies from chart'}
        </p>
      </div>

      {/* Header */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <HeartPulse className="w-4 h-4" />
          <span>{t('auto.rogaAnalysis')}</span>
        </div>
        <div className="px-4 py-2 flex items-start gap-2 text-xs text-blue-700 bg-blue-50 border-t border-blue-100">
          <Info className="w-3.5 h-3.5 shrink-0 mt-0.5" />
          <p>{t('auto.disclaimerHealth')}</p>
        </div>
      </div>

      {/* Special Yogas */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <AlertTriangle className="w-4 h-4" />
          <span>{t('auto.specialDiseaseYogas')}</span>
          <span className="ml-auto text-[12px] font-normal opacity-80">{data.special_yogas_detected.length}</span>
        </div>
        {data.special_yogas_detected.length === 0 ? (
          <div className="px-4 py-3 text-sm text-emerald-700">{t('auto.noRogaYogas')}</div>
        ) : (
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '20%' }} />
              <col style={{ width: '30%' }} />
              <col style={{ width: '30%' }} />
              <col style={{ width: '20%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'योग' : 'Yoga'}</th>
                <th className={thCls}>{isHi ? 'कारण' : 'Trigger'}</th>
                <th className={thCls}>{isHi ? 'उपाय' : 'Remedy'}</th>
                <th className={thCenterCls}>{isHi ? 'प्रभाव' : 'Impact'}</th>
              </tr>
            </thead>
            <tbody>
              {data.special_yogas_detected.map((y, i) => (
                <tr key={`${y.key}-${i}`}>
                  <td className={tdWrapCls}>
                    <p className="font-semibold text-foreground">{isHi ? y.name_hi : y.name_en}</p>
                    {y.sloka_ref && (
                      <div className="flex items-center gap-1 mt-1 text-[10px] text-muted-foreground italic">
                        <BookOpen className="w-2.5 h-2.5 shrink-0" />
                        <span>{y.sloka_ref}</span>
                      </div>
                    )}
                  </td>
                  <td className={tdWrapCls}><Points text={isHi ? y.trigger_hi : y.trigger_en} /></td>
                  <td className={tdWrapCls}><Points text={isHi ? y.remedy_hi : y.remedy_en} /></td>
                  <td className={`${tdCls} text-center`}>
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${SEV[y.severity] || SEV.moderate}`}>
                      {t(SEV_KEY[y.severity] || 'auto.severityModerate')}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* General Tendencies */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Activity className="w-4 h-4" />
          <span>{t('auto.diseaseTendencies')}</span>
          <span className="ml-auto text-[12px] font-normal opacity-80">{data.general_tendencies.length}</span>
        </div>
        {data.general_tendencies.length === 0 ? (
          <div className="px-4 py-3 text-sm text-muted-foreground">{t('auto.noMajorTendencies')}</div>
        ) : (
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '12%' }} />
              <col style={{ width: '8%' }} />
              <col style={{ width: '22%' }} />
              <col style={{ width: '42%' }} />
              <col style={{ width: '16%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'ग्रह' : 'Planet'}</th>
                <th className={thCls}>{isHi ? 'भाव' : 'H'}</th>
                <th className={thCls}>{isHi ? 'अंग' : 'Body Part'}</th>
                <th className={thCls}>{isHi ? 'रोग' : 'Diseases'}</th>
                <th className={thCenterCls}>{isHi ? 'गंभीरता' : 'Severity'}</th>
              </tr>
            </thead>
            <tbody>
              {data.general_tendencies.map((g, i) => (
                <tr key={`${g.planet}-${i}`}>
                  <td className={`${tdCls} font-semibold`}>{g.planet}</td>
                  <td className={tdCls}>{g.house}</td>
                  <td className={tdWrapCls}>{isHi ? g.body_part_hi : g.body_part_en}</td>
                  <td className={tdWrapCls}>{(isHi ? g.diseases_hi : g.diseases_en).join(', ')}</td>
                  <td className={`${tdCls} text-center`}>
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${SEV[g.severity] || SEV.moderate}`}>
                      {t(SEV_KEY[g.severity] || 'auto.severityModerate')}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Planet Affliction Disease Matrix */}
      {data.afflicted_planet_diseases && data.afflicted_planet_diseases.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <ShieldAlert className="w-4 h-4" />
            <span>{isHi ? 'नौ ग्रह रोग विश्लेषण' : 'Planet Affliction Disease Matrix'}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '14%' }} />
              <col style={{ width: '22%' }} />
              <col style={{ width: '48%' }} />
              <col style={{ width: '16%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'ग्रह' : 'Planet'}</th>
                <th className={thCls}>{isHi ? 'पीड़ा' : 'Affliction'}</th>
                <th className={thCls}>{isHi ? 'संभावित रोग' : 'Diseases'}</th>
                <th className={thCenterCls}>{isHi ? 'गंभीरता' : 'Severity'}</th>
              </tr>
            </thead>
            <tbody>
              {data.afflicted_planet_diseases.map((apd, i) => {
                const aLabel = AFFLICTION_LABEL[apd.affliction_type] || { en: apd.affliction_type, hi: apd.affliction_type };
                const diseases = isHi ? apd.diseases_hi : apd.diseases_en;
                return (
                  <tr key={i}>
                    <td className={`${tdCls} font-semibold`}>{apd.planet}</td>
                    <td className={tdCls}>
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-orange-100 text-orange-800">
                        {isHi ? aLabel.hi : aLabel.en}
                      </span>
                    </td>
                    <td className={tdWrapCls}>
                      {diseases.slice(0, 3).join(', ')}
                      {diseases.length > 3 && <span className="text-muted-foreground"> +{diseases.length - 3}</span>}
                    </td>
                    <td className={`${tdCls} text-center`}>
                      <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${SEV[apd.severity] || SEV.moderate}`}>
                        {t(SEV_KEY[apd.severity] || 'auto.severityModerate')}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* 6th House Disease Profile */}
      {data.sixth_house_disease_profile && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Home className="w-4 h-4" />
            <span>{isHi ? 'षष्ठ भाव रोग प्रवृत्ति' : '6th House Disease Profile'}</span>
            <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">
              {data.sixth_house_disease_profile.sign}
            </span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed mb-3">
              {isHi ? data.sixth_house_disease_profile.note_hi : data.sixth_house_disease_profile.note_en}
            </p>
            <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wide mb-2">
              {isHi ? 'प्रवृत्त क्षेत्र' : 'Prone Areas'}
            </p>
            <div className="flex flex-wrap gap-2">
              {(isHi ? data.sixth_house_disease_profile.prone_areas_hi : data.sixth_house_disease_profile.prone_areas_en).map((area, i) => (
                <span key={i} className="px-2 py-0.5 rounded text-xs bg-red-50 text-red-800 border border-red-200">
                  {area}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Body Parts Affected */}
      {data.body_parts_affected.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <MapPin className="w-4 h-4" />
            <span>{t('auto.bodyPartsAffected')}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '10%' }} />
              <col style={{ width: '35%' }} />
              <col style={{ width: '55%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'भाव' : 'H'}</th>
                <th className={thCls}>{isHi ? 'अंग' : 'Body Part'}</th>
                <th className={thCls}>{isHi ? 'कारण' : 'Due To'}</th>
              </tr>
            </thead>
            <tbody>
              {data.body_parts_affected.map((b, i) => (
                <tr key={i}>
                  <td className={`${tdCls} font-semibold`}>{b.house}</td>
                  <td className={tdCls}>{isHi ? b.part_hi : b.part_en}</td>
                  <td className={tdWrapCls}>{isHi ? b.due_to_hi : b.due_to_en}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Timing Indicators */}
      {data.timing_indicators.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Clock className="w-4 h-4" />
            <span>{t('auto.timingIndicators')}</span>
          </div>
          <div className="divide-y divide-border">
            {data.timing_indicators.map((ti, i) => {
              const text = isHi ? ti.hi : ti.en;
              const range = extractDateRange(text);
              const rest = range ? text.replace(range.raw, '').replace(/^\s*[:\-–—]\s*/, '').trim() : text;
              return (
                <div key={i} className="flex items-start gap-3 px-4 py-2.5">
                  {range ? (
                    <span className="shrink-0 text-[11px] font-bold px-2 py-0.5 rounded bg-sacred-gold-dark text-white whitespace-nowrap">
                      {range.label}
                    </span>
                  ) : (
                    <Clock className="w-3.5 h-3.5 text-muted-foreground shrink-0 mt-0.5" />
                  )}
                  <span className="text-xs text-foreground leading-relaxed">{rest || text}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Sloka footer */}
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground pt-2 border-t border-border">
        <BookOpen className="w-3 h-3" />
        <span className="italic">{data.sloka_ref}</span>
      </div>
    </div>
  );
}
