import { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import InteractiveKundli, { type ChartData } from '@/components/InteractiveKundli';
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
        <Heading as={5} variant={5}>
          {hi ? 'मोक्ष संभावना' : 'Moksha Potential'}
        </Heading>
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
        const res = await api.post('/api/kundli/divisional/d108', { kundli_id: kundliId });
        if (!cancelled) setData(res);
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
  /*  Build chart data for InteractiveKundli                           */
  /* ---------------------------------------------------------------- */

  const chartData: ChartData = {
    planets: (data.planet_positions || []).map((p) => ({
      planet: p.planet,
      sign: p.sign,
      house: p.house,
      nakshatra: p.nakshatra || '',
      sign_degree: p.sign_degree || 0,
      status: '',
    })),
    houses: data.houses || Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
    })),
  };

  /* ---------------------------------------------------------------- */
  /*  Render                                                           */
  /* ---------------------------------------------------------------- */

  return (
    <div className="space-y-6">
      {/* Title bar */}
      <div className="bg-gradient-to-r from-muted to-muted rounded-xl p-4 border border-border">
        <div className="flex items-center gap-2">
          <Heading as={4} variant={4}>
            {l('D108 Ashtottaramsha Chart', 'D108 अष्टोत्तरांश चार्ट')}
          </Heading>
          <span className="text-xs px-2 py-0.5 rounded-full bg-muted/10 text-primary border border-border/20 font-bold uppercase tracking-tighter">
            {l('SPIRITUAL', 'आध्यात्मिक')}
          </span>
        </div>
        <p className="text-sm text-foreground/70 mt-1">
          {l(
            'The D108 chart reveals spiritual evolution, moksha potential, and past-life karmic connections.',
            'D108 चार्ट आध्यात्मिक विकास, मोक्ष की संभावना, और पूर्व जन्म के कर्म संबंधों को प्रकट करता है।'
          )}
        </p>
      </div>

      {/* Chart + Table side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        {/* Chart */}
        <div className="flex justify-center">
          <div className="w-full max-w-[420px]">
            <InteractiveKundli chartData={chartData} compact />
          </div>
        </div>

        {/* Planet Positions Table */}
        <div className="rounded-xl border border-border h-fit">
          <Table className="w-full">
            <TableHeader className="bg-muted">
              <TableRow>
                <TableHead className="text-left p-3 text-primary font-medium text-sm">{t('table.planet')}</TableHead>
                <TableHead className="text-left p-3 text-primary font-medium text-sm">{t('table.sign')}</TableHead>
                <TableHead className="text-left p-3 text-primary font-medium text-sm">{t('table.degree')}</TableHead>
                <TableHead className="text-center p-3 text-primary font-medium text-sm">{l('House', 'भाव')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(data.planet_positions || []).map((p) => (
                <TableRow key={p.planet} className="border-t border-border hover:bg-muted/5">
                  <TableCell className="p-3 text-foreground font-medium text-sm">{translatePlanet(p.planet, language)}</TableCell>
                  <TableCell className="p-3 text-foreground text-sm">{translateSign(p.sign, language)}</TableCell>
                  <TableCell className="p-3 text-foreground text-sm">{p.sign_degree?.toFixed(1) || '--'}&deg;</TableCell>
                  <TableCell className="p-3 text-center text-primary font-bold text-sm">{p.house}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Moksha Potential Gauge */}
      {data.moksha_potential && (
        <MokshaGauge
          score={data.moksha_potential.score}
          level={data.moksha_potential.level}
          description={hi ? data.moksha_potential.description_hi : data.moksha_potential.description}
          language={language}
        />
      )}

      {/* Spiritual Indicators */}
      {data.spiritual_indicators && data.spiritual_indicators.length > 0 && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">
            {l('Spiritual Indicators', 'आध्यात्मिक संकेतक')}
          </Heading>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {data.spiritual_indicators.map((ind, idx) => (
              <div
                key={idx}
                className={`bg-white rounded-lg p-3 border ${
                  ind.strength === 'strong' ? 'border-green-200' :
                  ind.strength === 'moderate' ? 'border-amber-200' :
                  ind.strength === 'weak' ? 'border-red-200' :
                  'border-border/20'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <Heading as={6} variant={6}>
                    {hi ? ind.name_hi : ind.name}
                  </Heading>
                  {ind.strength && (
                    <span className={`px-1.5 py-0.5 rounded-full text-[9px] font-bold uppercase ${
                      ind.strength === 'strong' ? 'bg-green-100 text-green-700' :
                      ind.strength === 'moderate' ? 'bg-amber-100 text-amber-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {hi
                        ? (ind.strength === 'strong' ? 'बलवान' : ind.strength === 'moderate' ? 'मध्यम' : 'दुर्बल')
                        : ind.strength}
                    </span>
                  )}
                </div>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {hi ? ind.description_hi : ind.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Past Life Karma Cards */}
      {data.past_life_karma && data.past_life_karma.length > 0 && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">
            {l('Past Life Karma', 'पूर्व जन्म के कर्म')}
          </Heading>
          <div className="space-y-3">
            {data.past_life_karma.map((karma, idx) => (
              <div key={idx} className="bg-white p-4 rounded-lg border border-border/20">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 text-primary font-bold text-sm">
                    {idx + 1}
                  </div>
                  <div className="flex-1">
                    <Heading as={6} variant={6} className="text-primary mb-1">
                      {hi ? karma.title_hi : karma.title}
                    </Heading>
                    {karma.planet && (
                      <p className="text-xs text-foreground/50 mb-1">
                        {translatePlanet(karma.planet, language)}
                        {karma.house && ` - ${l('House', 'भाव')} ${karma.house}`}
                      </p>
                    )}
                    <p className="text-xs text-foreground/70 leading-relaxed">
                      {hi ? karma.description_hi : karma.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Interpretation text */}
      {data.interpretation && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">
            {l('Interpretation', 'व्याख्या')}
          </Heading>
          <div className="text-sm text-foreground leading-relaxed whitespace-pre-line">
            {hi ? data.interpretation_hi : data.interpretation}
          </div>
        </div>
      )}

      {/* Footer note */}
      <div className="p-3 bg-white/50 rounded-lg border border-border/10 text-xs text-foreground italic leading-relaxed">
        {l(
          'The D108 (Ashtottaramsha) is one of the highest divisional charts used to assess soul evolution and spiritual path. Results depend heavily on accurate birth time.',
          'D108 (अष्टोत्तरांश) उच्चतम विभागीय चार्टों में से एक है जो आत्मा के विकास और आध्यात्मिक मार्ग का आकलन करता है। परिणाम सटीक जन्म समय पर बहुत निर्भर करते हैं।'
        )}
      </div>
    </div>
  );
}
