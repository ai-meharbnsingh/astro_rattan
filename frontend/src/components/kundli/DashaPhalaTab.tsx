import React, { useEffect, useState } from 'react';
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet } from '@/lib/backend-translations';
import { Heading } from '@/components/ui/heading';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

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

interface DashaPhalaResponse {
  as_of: string;
  kundli_id?: string;
  person_name?: string;
  error?: string;
  mahadasha: MahadashaRecord | null;
  antardasha: AntardashaRecord | null;
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
    </div>
  );
}
