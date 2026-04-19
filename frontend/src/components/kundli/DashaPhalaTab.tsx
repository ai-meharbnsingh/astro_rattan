import React, { useEffect, useState } from 'react';
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet } from '@/lib/backend-translations';
import { Heading } from '@/components/ui/heading';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface DashaQuality {
  tag: string;
  tag_hi: string;
  label_en: string;
  label_hi: string;
  reasons: string[];
  sloka_ref: string;
}

interface MahadashaAnalysis {
  planet: string;
  strength: 'strong' | 'weak' | 'neutral';
  factors: string[];
  effect_en: string;
  effect_hi: string;
  general_en?: string;
  general_hi?: string;
  when_strong_en?: string;
  when_strong_hi?: string;
  when_weak_en?: string;
  when_weak_hi?: string;
  sloka_ref: string;
  dignity_modifier?: 'excellent' | 'challenged' | 'obstructed' | 'neutral';
  dignity_note_en?: string;
  dignity_note_hi?: string;
  dasha_quality?: DashaQuality;
}

interface AntardashaAnalysis {
  mahadasha: string;
  bhukti: string;
  effect_en: string;
  effect_hi: string;
  sloka_ref: string;
  severity: 'favorable' | 'mixed' | 'challenging';
  severity_factors: string[];
}

interface MahadashaRecord {
  planet: string;
  start: string;
  end: string;
  years: number;
  analysis: MahadashaAnalysis;
}

interface AntardashaRecord {
  planet: string;
  start: string;
  end: string;
  analysis: AntardashaAnalysis;
}

interface TransitCorrelation {
  md_planet: string;
  natal_longitude: number;
  transit_longitude: number;
  orb_degrees: number;
  natal_sign: string;
  transit_sign: string;
  intensified: boolean;
  note_en: string;
  note_hi: string;
}

interface DashaPhalaResponse {
  as_of: string;
  kundli_id?: string;
  person_name?: string;
  error?: string;
  mahadasha: MahadashaRecord | null;
  antardasha: AntardashaRecord | null;
  transit_correlation?: TransitCorrelation | null;
}

interface DashaPhalaTabProps {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

function strengthClasses(strength: string): { badge: string; label: string } {
  switch (strength) {
    case 'strong':
      return { badge: 'bg-emerald-100 text-emerald-800 border-emerald-300', label: 'mdStrong' };
    case 'weak':
      return { badge: 'bg-rose-100 text-rose-800 border-rose-300', label: 'mdWeak' };
    default:
      return { badge: 'bg-amber-100 text-amber-800 border-amber-300', label: 'mdNeutral' };
  }
}

function severityClasses(sev: string): { badge: string; label: string } {
  switch (sev) {
    case 'favorable':
      return { badge: 'bg-emerald-100 text-emerald-800 border-emerald-300', label: 'severityFavorable' };
    case 'challenging':
      return { badge: 'bg-rose-100 text-rose-800 border-rose-300', label: 'severityChallenging' };
    default:
      return { badge: 'bg-amber-100 text-amber-800 border-amber-300', label: 'severityMixed' };
  }
}

function dignityBadge(modifier?: string): { classes: string; labelEn: string; labelHi: string } | null {
  if (!modifier) return null;
  switch (modifier) {
    case 'excellent':
      return {
        classes: 'bg-green-100 text-green-800 border-green-300',
        labelEn: 'Excellent',
        labelHi: 'उत्कृष्ट',
      };
    case 'challenged':
      return {
        classes: 'bg-orange-100 text-orange-800 border-orange-300',
        labelEn: 'Challenged',
        labelHi: 'चुनौतीपूर्ण',
      };
    case 'obstructed':
      return {
        classes: 'bg-red-100 text-red-800 border-red-300',
        labelEn: 'Obstructed',
        labelHi: 'अवरुद्ध',
      };
    case 'neutral':
    default:
      return {
        classes: 'bg-slate-100 text-slate-600 border-slate-300',
        labelEn: 'Neutral',
        labelHi: 'मध्यम',
      };
  }
}

function dashaQualityBadgeClasses(tag: string): string {
  const lower = tag.toLowerCase();
  if (lower.includes('auspicious') || lower.includes('shubha')) {
    return 'bg-green-100 text-green-800 border-green-300';
  }
  if (lower.includes('challenging') || lower.includes('ashubha') || lower.includes('difficult')) {
    return 'bg-red-100 text-red-800 border-red-300';
  }
  return 'bg-slate-100 text-slate-600 border-slate-300';
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function DashaPhalaTab({ kundliId, language, t }: DashaPhalaTabProps) {
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const hi = language === 'hi';

  const [data, setData] = useState<DashaPhalaResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [asOf, setAsOf] = useState<string>('');
  const [showVariants, setShowVariants] = useState(false);

  const fetchDashaPhala = async (as_of?: string) => {
    if (!kundliId) return;
    setLoading(true);
    setError(null);
    try {
      const qs = as_of ? `?as_of=${as_of}` : '';
      const res = await api.get(`/api/kundli/${kundliId}/dasha-phala${qs}`);
      setData(res);
    } catch (err: any) {
      setError(err?.message || 'Failed to load dasha phala');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashaPhala();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{l('Loading dasha phala...', 'दशा फल लोड हो रहा है...')}</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
        {error}
      </div>
    );
  }

  if (!data || (!data.mahadasha && !data.antardasha)) {
    return (
      <div className="bg-muted rounded-xl border border-border p-6 text-center text-foreground/70">
        {data?.error || l('No dasha phala available', 'दशा फल उपलब्ध नहीं')}
      </div>
    );
  }

  const md = data.mahadasha;
  const ad = data.antardasha;

  return (
    <div className="space-y-6">
      {/* Intro */}
      <div className="bg-muted rounded-xl border border-border p-4">
        <Heading as={3} variant={3}>{t('auto.dashaPhala')}</Heading>
        <p className="text-sm text-foreground/70 mt-1">{t('auto.dashaPhalaDesc')}</p>

        <div className="mt-3 flex flex-wrap items-center gap-2 text-xs">
          <label className="text-foreground/70">{l('As of', 'तिथि')}:</label>
          <input
            type="date"
            value={asOf}
            onChange={(e) => setAsOf(e.target.value)}
            className="bg-background border border-border rounded px-2 py-1 text-xs"
          />
          <button
            className="px-3 py-1 bg-primary text-white rounded text-xs font-medium hover:bg-primary/90"
            onClick={() => fetchDashaPhala(asOf || undefined)}
          >
            {l('Check', 'देखें')}
          </button>
          {data?.as_of && (
            <span className="ml-auto text-foreground/60">
              {l('Showing for', 'प्रभावी तिथि')}: <span className="font-semibold">{data.as_of}</span>
            </span>
          )}
        </div>
      </div>

      {/* Current Mahadasha */}
      {md && (
        <div className="bg-muted rounded-xl border border-border p-5">
          <div className="flex flex-wrap items-center gap-3 mb-3">
            <Heading as={4} variant={4} className="uppercase tracking-wide">
              {t('auto.currentMahadasha')}
            </Heading>
            <span className="text-lg font-bold text-primary">
              {translatePlanet(md.planet, language) || md.planet}
            </span>
            <span
              className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${strengthClasses(md.analysis.strength).badge}`}
            >
              {t(`auto.${strengthClasses(md.analysis.strength).label}`)}
            </span>
            {(() => {
              const db = dignityBadge(md.analysis.dignity_modifier);
              return db ? (
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${db.classes}`}
                  title={hi ? md.analysis.dignity_note_hi : md.analysis.dignity_note_en}
                >
                  {hi ? db.labelHi : db.labelEn}
                </span>
              ) : null;
            })()}
            <span className="text-xs text-foreground/60 ml-auto">
              {md.start} → {md.end} · {md.years} {l('yrs', 'वर्ष')}
            </span>
          </div>

          <p className="text-sm text-foreground leading-relaxed">
            {hi ? md.analysis.effect_hi : md.analysis.effect_en}
          </p>

          {/* Dignity note */}
          {md.analysis.dignity_modifier && md.analysis.dignity_modifier !== 'neutral' && (
            <div className={`mt-2 px-3 py-2 rounded-lg text-xs ${
              md.analysis.dignity_modifier === 'excellent'
                ? 'bg-green-50 text-green-800 border border-green-200'
                : md.analysis.dignity_modifier === 'obstructed'
                  ? 'bg-red-50 text-red-800 border border-red-200'
                  : 'bg-orange-50 text-orange-800 border border-orange-200'
            }`}>
              {hi ? md.analysis.dignity_note_hi : md.analysis.dignity_note_en}
            </div>
          )}

          {/* Dasha Quality */}
          {md.analysis.dasha_quality && (
            <div className="mt-3 rounded-lg border border-border bg-background p-3 space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${dashaQualityBadgeClasses(md.analysis.dasha_quality.tag)}`}>
                  {hi ? md.analysis.dasha_quality.tag_hi : md.analysis.dasha_quality.tag}
                </span>
                <span className="text-xs text-foreground/80">
                  {hi ? md.analysis.dasha_quality.label_hi : md.analysis.dasha_quality.label_en}
                </span>
              </div>
              {md.analysis.dasha_quality.reasons.length > 0 && (
                <ul className="list-disc list-inside space-y-0.5">
                  {md.analysis.dasha_quality.reasons.map((reason, idx) => (
                    <li key={idx} className="text-xs text-foreground/70">{reason}</li>
                  ))}
                </ul>
              )}
              {md.analysis.dasha_quality.sloka_ref && (
                <p className="text-[10px] italic text-foreground/50">{md.analysis.dasha_quality.sloka_ref}</p>
              )}
            </div>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-2 text-[10px]">
            {md.analysis.factors.map((f) => (
              <span
                key={f}
                className="px-1.5 py-0.5 rounded bg-background border border-border text-foreground/70 uppercase"
              >
                {f.replace('_', ' ')}
              </span>
            ))}
            {md.analysis.sloka_ref && (
              <span className="ml-auto text-foreground/50 italic">{md.analysis.sloka_ref}</span>
            )}
          </div>

          {/* Expandable variants */}
          <button
            className="mt-3 text-xs text-primary hover:underline flex items-center gap-1"
            onClick={() => setShowVariants(!showVariants)}
          >
            {showVariants
              ? <ChevronDown className="w-3 h-3" />
              : <ChevronRight className="w-3 h-3" />}
            {l('All effect variants', 'सभी फल-रूप')}
          </button>

          {showVariants && (
            <div className="mt-3 space-y-2 text-xs border-t border-border pt-3">
              {md.analysis.general_en && (
                <div>
                  <div className="font-semibold text-foreground">{t('auto.generalEffect')}</div>
                  <p className="text-foreground/80">{hi ? md.analysis.general_hi : md.analysis.general_en}</p>
                </div>
              )}
              {md.analysis.when_strong_en && (
                <div>
                  <div className="font-semibold text-emerald-700">{t('auto.whenStrong')}</div>
                  <p className="text-foreground/80">{hi ? md.analysis.when_strong_hi : md.analysis.when_strong_en}</p>
                </div>
              )}
              {md.analysis.when_weak_en && (
                <div>
                  <div className="font-semibold text-rose-700">{t('auto.whenWeak')}</div>
                  <p className="text-foreground/80">{hi ? md.analysis.when_weak_hi : md.analysis.when_weak_en}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Current Antardasha */}
      {ad && (
        <div className="bg-muted rounded-xl border border-border p-5">
          <div className="flex flex-wrap items-center gap-3 mb-3">
            <Heading as={4} variant={4} className="uppercase tracking-wide">
              {t('auto.currentAntardasha')}
            </Heading>
            <span className="text-lg font-bold text-primary">
              {translatePlanet(ad.analysis.mahadasha, language) || ad.analysis.mahadasha}
              {' - '}
              {translatePlanet(ad.analysis.bhukti, language) || ad.analysis.bhukti}
            </span>
            <span
              className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${severityClasses(ad.analysis.severity).badge}`}
            >
              {t(`auto.${severityClasses(ad.analysis.severity).label}`)}
            </span>
            <span className="text-xs text-foreground/60 ml-auto">
              {ad.start} → {ad.end}
            </span>
          </div>

          <p className="text-sm text-foreground leading-relaxed">
            {hi ? ad.analysis.effect_hi : ad.analysis.effect_en}
          </p>

          <div className="mt-3 flex flex-wrap items-center gap-2 text-[10px]">
            {ad.analysis.severity_factors.map((f) => (
              <span
                key={f}
                className="px-1.5 py-0.5 rounded bg-background border border-border text-foreground/70 uppercase"
              >
                {f.replace('_', ' ')}
              </span>
            ))}
            {ad.analysis.sloka_ref && (
              <span className="ml-auto text-foreground/50 italic">{ad.analysis.sloka_ref}</span>
            )}
          </div>
        </div>
      )}

      {/* Transit-Dasha Correlation */}
      {data?.transit_correlation && (
        <div className={`rounded-xl border p-4 ${
          data.transit_correlation.intensified
            ? 'border-amber-400/50 bg-amber-50/30'
            : 'border-border bg-muted'
        }`}>
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <span className="text-xs font-bold text-foreground uppercase tracking-wide">
              {l('Transit-Dasha Correlation', 'गोचर-दशा सहसंबंध')}
            </span>
            {data.transit_correlation.intensified && (
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
                {l('Intensified', 'तीव्र')}
              </span>
            )}
            <span className="text-[10px] text-foreground/60 ml-auto">
              {l('Orb', 'कोण')}: {data.transit_correlation.orb_degrees}°
            </span>
          </div>
          <p className="text-xs text-foreground/80 leading-relaxed">
            {hi ? data.transit_correlation.note_hi : data.transit_correlation.note_en}
          </p>
          <div className="mt-2 flex flex-wrap gap-3 text-[10px] text-foreground/60">
            <span>{l('Natal', 'जन्म')}: {data.transit_correlation.natal_sign} ({data.transit_correlation.natal_longitude}°)</span>
            <span>{l('Transit', 'गोचर')}: {data.transit_correlation.transit_sign} ({data.transit_correlation.transit_longitude}°)</span>
          </div>
        </div>
      )}

      {/* Dasha Timing Rule */}
      <DashaTimingSection kundliId={kundliId} language={language} l={l} hi={hi} />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Dasha Timing Rule sub-component (Phaladeepika Adh. 19-21)         */
/* ------------------------------------------------------------------ */

interface TimingEntry {
  planet: string;
  house: number;
  house_area_en: string;
  house_area_hi: string;
  house_type: string;
  strength: string;
  is_exalted: boolean;
  is_debilitated: boolean;
  is_own_sign: boolean;
  timing_phase: 'first_half' | 'second_half';
  timing_phase_label_en: string;
  timing_phase_label_hi: string;
  timing_en: string;
  timing_hi: string;
  dasha_years: number;
  sloka_ref: string;
}

interface TimingData {
  planets: Record<string, TimingEntry>;
  first_half_planets: string[];
  second_half_planets: string[];
  summary_en: string;
  summary_hi: string;
  sloka_ref: string;
}

function DashaTimingSection({
  kundliId, language, l, hi,
}: {
  kundliId: string;
  language: string;
  l: (en: string, hi: string) => string;
  hi: boolean;
}) {
  const [data, setData] = React.useState<TimingData | null>(null);
  const [expanded, setExpanded] = React.useState(false);
  const [loaded, setLoaded] = React.useState(false);

  const load = () => {
    if (loaded || !kundliId) return;
    setLoaded(true);
    api.get<TimingData>(`/api/kundli/${kundliId}/dasha-timing-rule`)
      .then(setData)
      .catch(() => {});
  };

  const toggle = () => {
    if (!expanded) load();
    setExpanded(e => !e);
  };

  const PLANET_ORDER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];

  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <button
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-muted/10 transition-colors"
        onClick={toggle}
      >
        <div className="flex items-center gap-2">
          <span className="text-sm font-bold text-foreground uppercase tracking-wide">
            {l('Dasha Timing Rule', 'दशा फल-काल नियम')}
          </span>
          <span className="text-[10px] italic text-foreground/50">{l('Phaladeepika Adh. 19-21', 'फलदीपिका अ. 19-21')}</span>
        </div>
        {expanded ? <ChevronDown className="w-4 h-4 text-primary" /> : <ChevronRight className="w-4 h-4 text-primary" />}
      </button>

      {expanded && (
        <div className="px-4 pb-4 space-y-4">
          {!data && (
            <div className="flex items-center gap-2 py-4 text-sm text-foreground/60">
              <Loader2 className="w-4 h-4 animate-spin" />
              {l('Loading…', 'लोड हो रहा है…')}
            </div>
          )}

          {data && (
            <>
              {/* Summary chips */}
              <div className="space-y-2 pt-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-semibold text-foreground/70 uppercase tracking-wide">
                    {l('First Half', 'प्रथम अर्ध')}:
                  </span>
                  {data.first_half_planets.map(p => (
                    <span key={p} className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                      {translatePlanet(p, language)}
                    </span>
                  ))}
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-semibold text-foreground/70 uppercase tracking-wide">
                    {l('Second Half', 'द्वितीय अर्ध')}:
                  </span>
                  {data.second_half_planets.map(p => (
                    <span key={p} className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-300">
                      {translatePlanet(p, language)}
                    </span>
                  ))}
                </div>
              </div>

              {/* Per-planet table */}
              <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
                <table className="table-sacred w-full text-xs border-collapse">
                  <thead>
                    <tr className="bg-muted/50">
                      <th className="text-left p-2 text-primary font-medium">{l('Planet', 'ग्रह')}</th>
                      <th className="text-center p-2 text-primary font-medium">{l('House', 'भाव')}</th>
                      <th className="text-center p-2 text-primary font-medium">{l('Strength', 'बल')}</th>
                      <th className="text-center p-2 text-primary font-medium">{l('Years', 'वर्ष')}</th>
                      <th className="text-left p-2 text-primary font-medium">{l('Results Peak', 'फल-काल')}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border/30">
                    {PLANET_ORDER.map(planet => {
                      const e = data.planets[planet];
                      if (!e) return null;
                      const isFirst = e.timing_phase === 'first_half';
                      return (
                        <tr key={planet} className="hover:bg-muted/5 transition-colors">
                          <td className="p-2 font-semibold text-foreground">{translatePlanet(planet, language)}</td>
                          <td className="p-2 text-center text-foreground">
                            H{e.house}
                            <span className="ml-1 text-[9px] text-foreground/50">({hi ? e.house_area_hi : e.house_area_en})</span>
                          </td>
                          <td className="p-2 text-center">
                            <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${
                              e.strength === 'strong' ? 'bg-emerald-100 text-emerald-800' :
                              e.strength === 'weak' ? 'bg-rose-100 text-rose-800' :
                              'bg-slate-100 text-slate-600'
                            }`}>
                              {e.is_exalted ? l('Exalted', 'उच्च') : e.is_debilitated ? l('Debil.', 'नीच') : e.is_own_sign ? l('Own', 'स्व') : l('Neutral', 'सम')}
                            </span>
                          </td>
                          <td className="p-2 text-center text-foreground font-medium">{e.dasha_years}y</td>
                          <td className="p-2">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                              isFirst
                                ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                                : 'bg-rose-50 text-rose-800 border-rose-300'
                            }`}>
                              {isFirst ? l('1st Half', 'प्रथम') : l('2nd Half', 'द्वितीय')}
                            </span>
                            <span className="ml-2 text-[10px] text-foreground/60 italic">
                              {hi ? e.house_area_hi : e.house_area_en}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              <p className="text-[10px] italic text-foreground/40 text-right">{data.sloka_ref}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
