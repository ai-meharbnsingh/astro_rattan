import React, { useEffect, useState } from 'react';
import { Clock3, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
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

import { Sparkles, Clock, Calendar } from 'lucide-react';

function DashaTheorySection({ language }: { language: string }) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  const levels = [
    {
      name: l('Mahadasha (Major Period)', 'महादशा (मुख्य अवधि)'),
      duration: l('Years', 'वर्षों तक'),
      desc: l('The "Season" of your life. It sets the primary theme and background for a long period.', 'आपके जीवन का "सीजन"। यह एक लंबी अवधि के लिए प्राथमिक विषय और पृष्ठभूमि निर्धारित करता है।'),
    },
    {
      name: l('Antardasha (Sub-Period)', 'अंतर्दशा (उप-अवधि)'),
      duration: l('Months', 'महीनों तक'),
      desc: l('The "Weather" within the season. It fine-tunes the results and shows specific events.', 'सीजन के भीतर का "मौसम"। यह परिणामों को और अधिक सटीक बनाता है और विशिष्ट घटनाओं को दर्शाता है।'),
    },
    {
      name: l('Pratyantar (Sub-sub-period)', 'प्रत्यंतर दशा (सूक्ष्म अवधि)'),
      duration: l('Days', 'दिनों तक'),
      desc: l('The "Daily Forecast". It highlights the immediate focus and mood of shorter intervals.', ' "दैनिक पूर्वानुमान"। यह छोटे अंतराल के तत्काल फोकस और मूड को उजागर करता है।'),
    },
  ];

  return (
    <div className="mt-8 space-y-6 pb-6">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5" />
          {l('Understanding Life Timing (The Seasons Metaphor)', 'जीवन के समय को समझना (सीजन का रूपक)')}
        </Heading>
        
        <p className="text-sm text-foreground/80 mb-6 leading-relaxed">
          {l(
            'While your birth chart shows "what" is in your destiny, the Dasha system reveals "when" it will happen. In Vedic Astrology, life is divided into cycles ruled by different planets. This is called the Vimshottari Dasha — a 120-year cycle that governs the unfolding of your karma.',
            'जबकि आपकी जन्म कुंडली बताती है कि आपके भाग्य में "क्या" है, दशा प्रणाली यह प्रकट करती है कि वह "कब" होगा। वैदिक ज्योतिष में, जीवन को विभिन्न ग्रहों द्वारा शासित चक्रों में विभाजित किया गया है। इसे विंशोत्तरी दशा कहा जाता है — एक 120 साल का चक्र जो आपके कर्मों के प्रकट होने को नियंत्रित करता है।'
          )}
        </p>

        {/* Metaphor Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {levels.map((level, idx) => (
            <div key={idx} className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
              <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-1">{level.name}</h5>
              <p className="text-[10px] font-bold text-primary mb-2 italic">[{level.duration}]</p>
              <p className="text-xs text-foreground/70 leading-relaxed">
                {level.desc}
              </p>
            </div>
          ))}
        </div>

        <div className="space-y-6">
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-primary flex items-center gap-2 border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('How the Planets Shape Your Time', 'ग्रह आपके समय को कैसे आकार देते हैं')}
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4">
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Sun Dasha (6 yrs):', 'सूर्य दशा (6 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Focus on career, authority, father, and self-realization.', 'करियर, अधिकार, पिता और आत्म-साक्षात्कार पर ध्यान।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Moon Dasha (10 yrs):', 'चंद्र दशा (10 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Focus on emotions, home, mother, and mental peace.', 'भावनाओं, घर, माता और मानसिक शांति पर ध्यान।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Mars Dasha (7 yrs):', 'मंगल दशा (7 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Period of high energy, courage, properties, or conflicts.', 'उच्च ऊर्जा, साहस, संपत्ति या संघर्ष की अवधि।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Rahu Dasha (18 yrs):', 'राहु दशा (18 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Obsessive growth, foreign travels, illusions, or sudden gains.', 'जुनूनी विकास, विदेश यात्रा, भ्रम या अचानक लाभ।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Jupiter Dasha (16 yrs):', 'गुरु दशा (16 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Wisdom, expansion, children, wealth, and spiritual progress.', 'ज्ञान, विस्तार, संतान, धन और आध्यात्मिक प्रगति।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Saturn Dasha (19 yrs):', 'शनि दशा (19 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Hard work, discipline, delays, and fulfilling karmic duties.', 'कड़ी मेहनत, अनुशासन, देरी और कर्मिक कर्तव्यों की पूर्ति।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Mercury Dasha (17 yrs):', 'बुध दशा (17 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Intellect, business, learning, and communication events.', 'बुद्धि, व्यवसाय, सीखने और संचार की घटनाएं।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Ketu Dasha (7 yrs):', 'केतु दशा (7 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Detachment, spiritual insights, and resolving past karma.', 'वैराग्य, आध्यात्मिक अंतर्दृष्टि और पिछले कर्मों का समाधान।')}</span>
              </div>
              <div className="text-xs">
                <span className="font-bold text-sacred-gold-dark">{l('Venus Dasha (20 yrs):', 'शुक्र दशा (20 वर्ष):')}</span>{' '}
                <span className="text-foreground/70">{l('Luxury, love, marriage, arts, and worldly comforts.', 'विलासिता, प्रेम, विवाह, कला और सांसारिक सुख।')}</span>
              </div>
            </div>
          </div>

          <div className="p-4 bg-sacred-gold-dark/[0.03] rounded-lg border border-sacred-gold/20 text-center">
            <p className="text-xs text-foreground/80 leading-relaxed italic">
              {l(
                'Note: A planet’s results depend on its placement in your birth chart. A well-placed "Boss" (planet) brings growth, while a weak one brings challenges.',
                'नोट: एक ग्रह का परिणाम आपकी जन्म कुंडली में उसकी स्थिति पर निर्भर करता है। एक अच्छी तरह से स्थित "बॉस" (ग्रह) विकास लाता है, जबकि एक कमजोर बॉस चुनौतियां लाता है।'
              )}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function DashaPhalaTab({ kundliId, language, t }: DashaPhalaTabProps) {
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const hi = language === 'hi';

  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <Clock3 className="w-6 h-6" />
        {hi ? 'दशा फल' : 'Dasha Effects'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {hi
          ? 'वर्तमान सक्रिय दशा अवधियों के लिए व्याख्यात्मक परिणाम और मार्गदर्शन।'
          : 'Interpretive results and guidance for currently active dasha periods.'}
      </p>
    </div>
  );

  const [data, setData] = useState<DashaPhalaResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [asOf, setAsOf] = useState<string>('');

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
      <div className="space-y-4">
        {header}
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{l('Loading dasha phala...', 'दशा फल लोड हो रहा है...')}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        {header}
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
          {error}
        </div>
      </div>
    );
  }

  if (!data || (!data.mahadasha && !data.antardasha)) {
    return (
      <div className="space-y-4">
        {header}
        <div className="bg-muted rounded-xl border border-border p-6 text-center text-foreground/70">
          {data?.error || l('No dasha phala available', 'दशा फल उपलब्ध नहीं')}
        </div>
      </div>
    );
  }

  const md = data.mahadasha;
  const ad = data.antardasha;

  return (
    <div className="space-y-6">
      {header}
      {/* Intro */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('auto.dashaPhala')}
        </div>
        <div className="p-4">
          <p className="text-sm text-foreground/70">{t('auto.dashaPhalaDesc')}</p>
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
      </div>

      {/* Current Mahadasha */}
      {md && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.currentMahadasha')}
          </div>
          <div className="p-5">
            <div className="flex flex-wrap items-center gap-3 mb-3">
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

            {(md.analysis.general_en || md.analysis.when_strong_en || md.analysis.when_weak_en) && (
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
        </div>
      )}

      {/* Current Antardasha */}
      {ad && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.currentAntardasha')}
          </div>
          <div className="p-5">
            <div className="flex flex-wrap items-center gap-3 mb-3">
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
        </div>
      )}

      {/* Transit-Dasha Correlation */}
      {data?.transit_correlation && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className={`px-4 py-2 text-[15px] font-semibold flex flex-wrap items-center gap-2 ${
            data.transit_correlation.intensified
              ? 'bg-amber-600 text-white'
              : 'bg-sacred-gold-dark text-white'
          }`}>
            <span>{l('Transit-Dasha Correlation', 'गोचर-दशा सहसंबंध')}</span>
            {data.transit_correlation.intensified && (
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/20 text-white border border-white/30">
                {l('Intensified', 'तीव्र')}
              </span>
            )}
            <span className="text-[10px] font-normal ml-auto opacity-80">
              {l('Orb', 'कोण')}: {data.transit_correlation.orb_degrees}°
            </span>
          </div>
          <div className="p-4">
            <p className="text-xs text-foreground/80 leading-relaxed">
              {hi ? data.transit_correlation.note_hi : data.transit_correlation.note_en}
            </p>
            <div className="mt-2 flex flex-wrap gap-3 text-[10px] text-foreground/60">
              <span>{l('Natal', 'जन्म')}: {data.transit_correlation.natal_sign} ({data.transit_correlation.natal_longitude}°)</span>
              <span>{l('Transit', 'गोचर')}: {data.transit_correlation.transit_sign} ({data.transit_correlation.transit_longitude}°)</span>
            </div>
          </div>
        </div>
      )}

      {/* Dasha Timing Rule */}
      <DashaTimingSection kundliId={kundliId} language={language} l={l} hi={hi} />

      {/* Dasha Theory Section — General educational summary */}
      <DashaTheorySection language={language} />
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
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get<TimingData>(`/api/kundli/${kundliId}/dasha-timing-rule`)
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [kundliId]);

  const PLANET_ORDER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];

  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-3">
        <span>{l('Dasha Timing Rule', 'दशा फल-काल नियम')}</span>
        <span className="text-[10px] italic opacity-70">{l('Phaladeepika Adh. 19-21', 'फलदीपिका अ. 19-21')}</span>
      </div>

      <div className="p-4 space-y-4">
        {loading && (
          <div className="flex items-center gap-2 py-4 text-sm text-foreground/60">
            <Loader2 className="w-4 h-4 animate-spin" />
            {l('Loading…', 'लोड हो रहा है…')}
          </div>
        )}

        {data && (
          <>
            {/* Summary chips */}
            <div className="space-y-2">
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
            <div className="overflow-x-auto">
              <Table className="w-full text-xs table-fixed">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{l('Planet', 'ग्रह')}</TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{l('House', 'भाव')}</TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{l('Strength', 'बल')}</TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[12%]">{l('Years', 'वर्ष')}</TableHead>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[34%]">{l('Results Peak', 'फल-काल')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {PLANET_ORDER.map(planet => {
                    const e = data.planets[planet];
                    if (!e) return null;
                    const isFirst = e.timing_phase === 'first_half';
                    return (
                      <TableRow key={planet} className="border-t border-border">
                        <TableCell className="p-2 font-semibold text-foreground">{translatePlanet(planet, language)}</TableCell>
                        <TableCell className="p-2 text-center text-foreground">
                          H{e.house}
                          <span className="ml-1 text-[9px] text-foreground/50">({hi ? e.house_area_hi : e.house_area_en})</span>
                        </TableCell>
                        <TableCell className="p-2 text-center">
                          <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${
                            e.strength === 'strong' ? 'bg-emerald-100 text-emerald-800' :
                            e.strength === 'weak' ? 'bg-rose-100 text-rose-800' :
                            'bg-slate-100 text-slate-600'
                          }`}>
                            {e.is_exalted ? l('Exalted', 'उच्च') : e.is_debilitated ? l('Debil.', 'नीच') : e.is_own_sign ? l('Own', 'स्व') : l('Neutral', 'सम')}
                          </span>
                        </TableCell>
                        <TableCell className="p-2 text-center text-foreground font-medium">{e.dasha_years}y</TableCell>
                        <TableCell className="p-2 whitespace-normal break-words max-w-0">
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
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>

            <p className="text-[10px] italic text-foreground/40 text-right">{data.sloka_ref}</p>
          </>
        )}
      </div>
    </div>
  );
}
