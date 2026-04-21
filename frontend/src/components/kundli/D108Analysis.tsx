import { useState, useEffect } from 'react';
import { Loader2, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface PlanetPosition {
  planet: string;
  sign: string;
  house: number;
  sign_degree: number;
  nakshatra?: string;
}

interface SpiritualIndicator {
  name: string;
  name_hi?: string;
  description: string;
  description_hi?: string;
  strength?: 'strong' | 'moderate' | 'weak';
}

interface PastLifeKarma {
  title: string;
  title_hi?: string;
  description: string;
  description_hi?: string;
  planet?: string;
  house?: number;
}

interface D108Data {
  chart_name?: string;
  division?: number;
  planet_positions: PlanetPosition[];
  planet_signs?: Record<string, string>;
  houses?: Array<{ number: number; sign: string }>;
  spiritual_indicators?: SpiritualIndicator[];
  moksha_potential?: {
    score: number;        // 0-100
    level: string;        // high/moderate/low
    level_hi?: string;
    description?: string;
    description_hi?: string;
  };
  past_life_karma?: PastLifeKarma[];
  interpretation?: string;
  interpretation_hi?: string;
}

interface D108AnalysisProps {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

/* ------------------------------------------------------------------ */
/*  Moksha gauge                                                       */
/* ------------------------------------------------------------------ */

function MokshaGauge({ score, level, description, language }: {
  score: number;
  level: string;
  description?: string;
  language: string;
}) {
  const hi = language === 'hi';
  // Clamp to 0-100
  const pct = Math.max(0, Math.min(100, score));

  // Color gradient based on score
  const barColor = pct >= 70
    ? 'bg-gradient-to-r from-green-400 to-green-600'
    : pct >= 40
      ? 'bg-gradient-to-r from-amber-400 to-amber-600'
      : 'bg-gradient-to-r from-red-400 to-red-600';

  const levelLabel = hi
    ? (level === 'high' ? 'उच्च' : level === 'moderate' ? 'मध्यम' : 'निम्न')
    : level;

  return (
    <div className="bg-white rounded-lg p-4 border border-border/20">
      <div className="flex items-center justify-between mb-2">
        <p className="font-semibold text-sm text-foreground">{hi ? 'मोक्ष संभावना' : 'Moksha Potential'}</p>
        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
          pct >= 70 ? 'bg-green-100 text-green-700 border border-green-200' :
          pct >= 40 ? 'bg-amber-100 text-amber-700 border border-amber-200' :
          'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {levelLabel}
        </span>
      </div>

      {/* Progress bar */}
      <div className="relative w-full h-5 bg-muted/30 rounded-full overflow-hidden border border-border/20">
        <div
          className={`h-full rounded-full transition-all duration-1000 ease-out ${barColor}`}
          style={{ width: `${pct}%` }}
        />
        <span className="absolute inset-0 flex items-center justify-center text-[11px] font-bold text-foreground">
          {pct}%
        </span>
      </div>

      {description && (
        <p className="text-xs text-foreground/70 mt-2 leading-relaxed">{description}</p>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function D108Analysis({ kundliId, language, t }: D108AnalysisProps) {
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const hi = language === 'hi';

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<D108Data | null>(null);

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(`/api/kundli/${kundliId}/d108-analysis`);

        // Normalize API response → component shape
        const SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];

        // d108_positions dict → planet_positions array
        const d108Pos = res.d108_positions || {};
        const planetPositions: PlanetPosition[] = Object.entries(d108Pos).map(([planet, info]: [string, any]) => ({
          planet,
          sign: info.sign,
          sign_degree: info.degree || 0,
          house: Math.max(1, SIGNS.indexOf(info.sign) + 1),
          nakshatra: '',
        }));

        // spiritual_indicators: {planet, condition, sign, meaning} → {name, description, strength}
        const spiritualIndicators: SpiritualIndicator[] = (res.spiritual_indicators || []).map((si: any) => ({
          name: `${si.planet} — ${si.condition === 'exalted' ? 'Exalted' : 'Own Sign'} in ${si.sign}`,
          name_hi: `${si.planet} — ${si.condition === 'exalted' ? 'उच्च राशि' : 'स्वराशि'} (${si.sign})`,
          description: si.meaning || '',
          description_hi: si.meaning || '',
          strength: (si.condition === 'exalted' ? 'strong' : 'moderate') as 'strong' | 'moderate' | 'weak',
        }));
        // append moksha factors as strong indicators
        ((res.moksha_potential?.factors || []) as string[]).forEach((f: string) => {
          spiritualIndicators.push({ name: f, name_hi: f, description: '', description_hi: '', strength: 'strong' });
        });

        // moksha_potential: {score, max, factors} → {score, level, description}
        const rawScore = res.moksha_potential?.score ?? 0;
        const mokshaLevel = rawScore >= 70 ? 'high' : rawScore >= 40 ? 'moderate' : 'low';
        const mokshaPotential = res.moksha_potential ? {
          score: rawScore,
          level: mokshaLevel,
          description: res.interpretation,
          description_hi: res.interpretation,
        } : undefined;

        // past_life_karma: {axis?, planet?, meaning} → {title, description, planet?}
        const pastLifeKarma: PastLifeKarma[] = (res.past_life_karma || []).map((k: any) => ({
          title: k.axis || k.planet || 'Karmic Pattern',
          title_hi: k.axis || k.planet || 'कर्म पैटर्न',
          description: k.meaning || '',
          description_hi: k.meaning || '',
          planet: k.planet,
        }));

        const normalized: D108Data = {
          planet_positions: planetPositions,
          spiritual_indicators: spiritualIndicators,
          moksha_potential: mokshaPotential,
          past_life_karma: pastLifeKarma,
          interpretation: res.interpretation,
        };

        if (!cancelled) setData(normalized);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load D108 analysis');
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchData();
    return () => { cancelled = true; };
  }, [kundliId]);

  /* ---------------------------------------------------------------- */
  /*  Loading / Error                                                  */
  /* ---------------------------------------------------------------- */

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">
          {l('Loading D108 Ashtottaramsha chart...', 'D108 अष्टोत्तरांश चार्ट लोड हो रहा है...')}
        </span>
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

  if (!data) {
    return (
      <p className="text-center text-foreground py-8">
        {l('No D108 data available', 'D108 डेटा उपलब्ध नहीं है')}
      </p>
    );
  }

  /* ---------------------------------------------------------------- */
  /*  Build chart data for KundliChartSVG (report-page style)         */
  /* ---------------------------------------------------------------- */

  const chartPlanets: PlanetEntry[] = (data.planet_positions || []).map((p) => ({
    planet: p.planet,
    sign: p.sign,
    sign_degree: p.sign_degree || 0,
  }));
  // Use Sun's D108 sign as the ascendant proxy (standard for D108 interpretation)
  const d108AscSign = data.planet_positions?.find((p) => p.planet === 'Sun')?.sign || 'Aries';

  /* ---------------------------------------------------------------- */
  /*  Render                                                           */
  /* ---------------------------------------------------------------- */

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {hi ? 'D108 अष्टोत्तरांश' : 'D108 Chart'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi ? 'गहन आध्यात्मिक और कर्म अंतर्दृष्टि के लिए दुर्लभ D108 चार्ट' : 'Rare D108 chart for deep spiritual & karmic insights'}
        </p>
      </div>
      {/* Title bar */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-3">
          <span>{l('D108 Ashtottaramsha Chart', 'D108 अष्टोत्तरांश चार्ट')}</span>
          <span className="text-[10px] px-2 py-0.5 bg-white/20 rounded uppercase font-bold tracking-tight">
            {l('SPIRITUAL', 'आध्यात्मिक')}
          </span>
        </div>
        <p className="text-sm text-foreground/70 px-4 py-2">
          {l(
            'The D108 chart reveals spiritual evolution, moksha potential, and past-life karmic connections.',
            'D108 चार्ट आध्यात्मिक विकास, मोक्ष की संभावना, और पूर्व जन्म के कर्म संबंधों को प्रकट करता है।'
          )}
        </p>
      </div>

      {/* Chart + Table side by side — report-page style */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        {/* Chart — same as ReportTab: KundliChartSVG in max-w-[340px] aspect-square */}
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold text-center">
            D108 {l('Chart', 'चार्ट')}
          </div>
          <div className="flex justify-center p-4">
            <div className="w-full max-w-[340px] aspect-square">
              <KundliChartSVG
                planets={chartPlanets}
                ascendantSign={d108AscSign}
                language={language}
                showHouseNumbers={false}
                showRashiNumbers
                rashiNumberPlacement="corner"
                showAscendantMarker={false}
              />
            </div>
          </div>
        </div>

        {/* Planet Positions Table */}
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('table.planet')} — {t('table.sign')} / {t('table.degree')}
          </div>
          <Table className="w-full text-xs table-fixed">
            <TableHeader>
              <TableRow>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[35%]">{t('table.planet')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[35%]">{t('table.sign')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[30%]">{t('table.degree')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(data.planet_positions || []).map((p) => (
                <TableRow key={p.planet} className="border-t border-border hover:bg-muted/5">
                  <TableCell className="p-2 text-foreground font-medium">{translatePlanet(p.planet, language)}</TableCell>
                  <TableCell className="p-2 text-foreground">{translateSign(p.sign, language)}</TableCell>
                  <TableCell className="p-2 text-foreground">{p.sign_degree?.toFixed(1) || '--'}&deg;</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Moksha Potential Gauge */}
      {data.moksha_potential && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {l('Moksha Potential', 'मोक्ष संभावना')}
          </div>
          <div className="p-4">
            <MokshaGauge
              score={data.moksha_potential.score}
              level={data.moksha_potential.level}
              description={hi ? data.moksha_potential.description_hi : data.moksha_potential.description}
              language={language}
            />
          </div>
        </div>
      )}

      {/* Spiritual Indicators */}
      {data.spiritual_indicators && data.spiritual_indicators.length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {l('Spiritual Indicators', 'आध्यात्मिक संकेतक')}
          </div>
          <Table className="w-full text-xs table-fixed">
            <TableHeader>
              <TableRow>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[40%]">{l('Indicator', 'संकेतक')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[45%]">{l('Description', 'विवरण')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[15%]">{l('Strength', 'बल')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.spiritual_indicators.map((ind, idx) => (
                <TableRow key={idx} className="border-t border-border hover:bg-muted/5 align-top">
                  <TableCell className="p-2 font-semibold text-foreground">{hi ? ind.name_hi : ind.name}</TableCell>
                  <TableCell className="p-2 whitespace-normal break-words max-w-0 text-foreground/70">
                    {hi ? ind.description_hi : ind.description}
                  </TableCell>
                  <TableCell className="p-2 text-center">
                    {ind.strength && (
                      <span className={`px-1.5 py-0.5 rounded-full text-[9px] font-bold uppercase ${
                        ind.strength === 'strong' ? 'bg-green-100 text-green-700' :
                        ind.strength === 'moderate' ? 'bg-amber-100 text-amber-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                        {hi ? (ind.strength === 'strong' ? 'बलवान' : ind.strength === 'moderate' ? 'मध्यम' : 'दुर्बल') : ind.strength}
                      </span>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      {/* Past Life Karma */}
      {data.past_life_karma && data.past_life_karma.length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {l('Past Life Karma', 'पूर्व जन्म के कर्म')}
          </div>
          <Table className="w-full text-xs table-fixed">
            <TableHeader>
              <TableRow>
                <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[8%]">#</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[22%]">{l('Topic', 'विषय')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[70%]">{l('Description', 'विवरण')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.past_life_karma.map((karma, idx) => (
                <TableRow key={idx} className="border-t border-border hover:bg-muted/5 align-top">
                  <TableCell className="p-2 text-center font-bold text-primary">{idx + 1}</TableCell>
                  <TableCell className="p-2 font-semibold text-foreground">
                    {hi ? karma.title_hi : karma.title}
                    {karma.planet && (
                      <span className="block text-[10px] text-foreground/50 font-normal mt-0.5">
                        {translatePlanet(karma.planet, language)}
                        {karma.house && ` · ${l('H', 'भाव')}${karma.house}`}
                      </span>
                    )}
                  </TableCell>
                  <TableCell className="p-2 whitespace-normal break-words max-w-0 text-foreground/70">
                    {hi ? karma.description_hi : karma.description}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      {/* Interpretation */}
      {data.interpretation && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {l('Interpretation', 'व्याख्या')}
          </div>
          <p className="text-xs text-foreground leading-relaxed whitespace-pre-line p-4">
            {hi ? data.interpretation_hi : data.interpretation}
          </p>
        </div>
      )}

      {/* Footer note */}
      <div className="p-3 bg-white/50 rounded-lg border border-border/10 text-xs text-foreground italic leading-relaxed">
        {l(
          'The D108 (Ashtottaramsha) is one of the highest divisional charts used to assess soul evolution and spiritual path. Results depend heavily on accurate birth time.',
          'D108 (अष्टोत्तरांश) उच्चतम विभागीय चार्टों में से एक है जो आत्मा के विकास और आध्यात्मिक मार्ग का आकलन करता है। परिणाम सटीक जन्म समय पर बहुत निर्भर करते हैं।'
        )}
      </div>

      {/* D108 Theory Section — General educational summary */}
      <D108TheorySection language={language} />
    </div>
  );
}

function D108TheorySection({ language }: { language: string }) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  return (
    <div className="mt-12 space-y-6 pb-10">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {l('Understanding the D108 (Moksha Chart)', 'D108 (मोक्ष चार्ट) को समझना')}
        </Heading>
        
        <p className="text-sm text-foreground/80 mb-6 leading-relaxed">
          {l(
            'The D108 chart, also known as Ashtottaramsha, is a highly specialized and rare divisional chart in Vedic Astrology. It divides the 360° zodiac into 108 equal parts of 3°20\' each. This number is sacred, matching the 108 beads of a Mala and the 108 padas of the 27 Nakshatras.',
            'D108 चार्ट, जिसे अष्टोत्तरांश के रूप में भी जाना जाता है, वैदिक ज्योतिष में एक अत्यधिक विशिष्ट और दुर्लभ विभागीय चार्ट है। यह 360° राशि चक्र को 3°20\' के 108 समान भागों में विभाजित करता है। यह संख्या पवित्र है, जो एक माला के 108 मनकों और 27 नक्षत्रों के 108 चरणों से मेल खाती है।'
          )}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Spiritual Evolution */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-primary border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('Soul Evolution & Moksha', 'आत्मा का विकास और मोक्ष')}
            </h4>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l(
                'While the main chart (D1) shows your physical life, D108 peers into the soul’s journey across lifetimes. It is used to judge your "Moksha Potential" — the likelihood of spiritual liberation and the depth of your connection to the divine.',
                'जबकि मुख्य चार्ट (D1) आपके भौतिक जीवन को दर्शाता है, D108 जन्मों-जन्मों की आत्मा की यात्रा को देखता है। इसका उपयोग आपकी "मोक्ष संभावना" — आध्यात्मिक मुक्ति की संभावना और ईश्वर के साथ आपके संबंध की गहराई को आंकने के लिए किया जाता है।'
              )}
            </p>
          </div>

          {/* Past Life Karma */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-primary border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('Unlocking Past Life Karma', 'पूर्व जन्म के कर्मों को समझना')}
            </h4>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l(
                'Planetary placements in D108 reveal specific karmic patterns carried from previous births. This chart helps identify why certain spiritual or emotional tendencies exist in your current personality that cannot be explained by D1 alone.',
                'D108 में ग्रहों की स्थिति पिछले जन्मों से लाए गए विशिष्ट कर्म पैटर्न को प्रकट करती है। यह चार्ट यह पहचानने में मदद करता है कि आपके वर्तमान व्यक्तित्व में कुछ आध्यात्मिक या भावनात्मक प्रवृत्तियां क्यों मौजूद हैं जिन्हें अकेले D1 द्वारा नहीं समझाया जा सकता है।'
              )}
            </p>
          </div>
        </div>

        <div className="mt-8 p-4 bg-sacred-gold-dark/[0.03] rounded-lg border border-sacred-gold/20">
          <h4 className="text-xs font-bold text-sacred-gold-dark uppercase mb-2">{l('How to Interpret the Score?', 'स्कोर की व्याख्या कैसे करें?')}</h4>
          <p className="text-xs text-foreground/80 leading-relaxed italic">
            {l(
              'A high Moksha Potential score (above 70%) indicates a highly evolved soul with strong spiritual merits (Punya). A moderate score suggests a balance between material duties and spiritual progress, while a low score means the focus is currently on fulfilling worldly karma.',
              'एक उच्च मोक्ष संभावना स्कोर (70% से ऊपर) एक अत्यधिक विकसित आत्मा को इंगित करता है जिसमें मजबूत आध्यात्मिक गुण (पुण्य) होते हैं। एक मध्यम स्कोर भौतिक कर्तव्यों और आध्यात्मिक प्रगति के बीच संतुलन का सुझाव देता है, जबकि एक कम स्कोर का अर्थ है कि ध्यान वर्तमान में सांसारिक कर्मों को पूरा करने पर है।'
            )}
          </p>
        </div>

        <div className="mt-8 pt-4 border-t border-sacred-gold/20">
          <p className="text-[11px] text-foreground/50 italic text-center">
            {l(
              'Note: D108 is extremely sensitive to birth time. Even a 1-minute difference can change the entire chart. Use this for spiritual contemplation rather than mundane predictions.',
              'नोट: D108 जन्म समय के प्रति अत्यधिक संवेदनशील है। 1 मिनट का अंतर भी पूरे चार्ट को बदल सकता है। इसका उपयोग सांसारिक भविष्यवाणियों के बजाय आध्यात्मिक चिंतन के लिए करें।'
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
