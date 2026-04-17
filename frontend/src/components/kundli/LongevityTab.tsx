import { useState, useEffect } from 'react';
import { Loader2, Info, BookOpen, Heart, Clock3, Moon as MoonIcon, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface MarakaPlanet {
  planet: string;
  role: string;
  role_hi?: string;
  placement: number;
  strength: 'strong' | 'moderate' | 'weak' | 'unknown';
  notes_en: string;
  notes_hi: string;
}

interface EighthHouseAnalysis {
  eighth_lord: string;
  eighth_lord_placement: number;
  eighth_lord_strength: string;
  planets_in_8th: string[];
  interpretation_en: string;
  interpretation_hi: string;
}

interface SaturnAssessment {
  saturn_placement: number;
  saturn_sign?: string;
  saturn_strength: string;
  interpretation_en: string;
  interpretation_hi: string;
}

interface ApiResponse {
  kundli_id?: string;
  person_name?: string;
  overall_longevity_strength: 'strong' | 'moderate' | 'weak';
  maraka_planets: MarakaPlanet[];
  eighth_house_analysis: EighthHouseAnalysis;
  saturn_longevity_assessment: SaturnAssessment;
  karmic_transitions_en: string;
  karmic_transitions_hi: string;
  life_chapters_en: string[];
  life_chapters_hi: string[];
  sloka_ref: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'बृहस्पति', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const STRENGTH_STYLE: Record<string, { card: string; badge: string; key: string }> = {
  strong:   { card: 'border-emerald-300 bg-emerald-50', badge: 'bg-emerald-600 text-white', key: 'auto.longevityStrong' },
  moderate: { card: 'border-sacred-gold/30 bg-sacred-gold/5', badge: 'bg-sacred-gold-dark text-white', key: 'auto.longevityModerate' },
  weak:     { card: 'border-amber-300 bg-amber-50', badge: 'bg-amber-600 text-white', key: 'auto.longevityWeak' },
};

export default function LongevityTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<ApiResponse | null>(null);
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
        const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/longevity-indicators`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load longevity indicators');
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

  const overallStyle = STRENGTH_STYLE[data.overall_longevity_strength] || STRENGTH_STYLE.moderate;
  const planetName = (p: string) => (isHi ? (PLANET_HI[p] || p) : p);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Clock3 className="w-6 h-6" />
          {t('auto.longevity')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.longevityDesc')}</p>
      </div>

      {/* Disclaimer banner */}
      <div className="rounded-lg border-2 border-blue-300 bg-blue-50 p-4 flex items-start gap-3">
        <Info className="w-5 h-5 text-blue-700 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-blue-900 leading-relaxed">
          {t('auto.longevityDisclaimer')}
        </p>
      </div>

      {/* Overall strength card */}
      <div className={`rounded-xl border-2 p-5 ${overallStyle.card}`}>
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Heart className="w-5 h-5" />
            <h3 className="font-semibold text-foreground">
              {t('auto.overallLongevityStrength')}
            </h3>
          </div>
          <span className={`text-xs font-semibold uppercase tracking-wider px-3 py-1 rounded ${overallStyle.badge}`}>
            {t(overallStyle.key)}
          </span>
        </div>
      </div>

      {/* Maraka planets */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('auto.marakaPlanets')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.maraka_planets.map((m, i) => {
            const notes = isHi ? m.notes_hi : m.notes_en;
            const role = isHi && m.role_hi ? m.role_hi : m.role;
            const style = STRENGTH_STYLE[m.strength] || STRENGTH_STYLE.moderate;
            return (
              <div key={`${m.planet}-${i}`} className={`rounded-xl border-2 p-4 ${style.card}`}>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <h4 className="font-bold text-foreground">{planetName(m.planet)}</h4>
                    <div className="text-xs text-muted-foreground">{role}</div>
                  </div>
                  <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded ${style.badge}`}>
                    {t(style.key)}
                  </span>
                </div>
                <p className="text-xs text-foreground/80 leading-relaxed">{notes}</p>
              </div>
            );
          })}
          {data.maraka_planets.length === 0 && (
            <div className="md:col-span-2 p-4 rounded-lg bg-gray-50 border border-gray-200 text-sm text-gray-600 italic">
              {t('auto.marakaDataNotAvailable')}
            </div>
          )}
        </div>
      </section>

      {/* 8th house + Saturn side-by-side */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
          <h3 className="font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <MoonIcon className="w-5 h-5" />
            {t('auto.eighthHouseAnalysis')}
          </h3>
          <div className="text-xs text-muted-foreground mb-2">
            {t('auto.eighthLord')}:{' '}
            <span className="font-semibold text-foreground">
              {data.eighth_house_analysis.eighth_lord
                ? planetName(data.eighth_house_analysis.eighth_lord)
                : '—'}
            </span>
            {data.eighth_house_analysis.eighth_lord_placement > 0 && (
              <span className="ml-1">
                ({t('auto.bhavaShort')} {data.eighth_house_analysis.eighth_lord_placement})
              </span>
            )}
          </div>
          {data.eighth_house_analysis.planets_in_8th.length > 0 && (
            <div className="text-xs text-muted-foreground mb-3">
              {t('auto.planetsIn8th')}:{' '}
              <span className="text-foreground">
                {data.eighth_house_analysis.planets_in_8th.map(planetName).join(', ')}
              </span>
            </div>
          )}
          <p className="text-sm text-foreground/90 leading-relaxed">
            {isHi ? data.eighth_house_analysis.interpretation_hi : data.eighth_house_analysis.interpretation_en}
          </p>
        </div>

        <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
          <h3 className="font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <Clock3 className="w-5 h-5" />
            {t('auto.saturnLongevity')}
          </h3>
          <div className="text-xs text-muted-foreground mb-3">
            {t('auto.placement')}:{' '}
            <span className="font-semibold text-foreground">
              {data.saturn_longevity_assessment.saturn_placement > 0
                ? `${t('auto.bhavaShort')} ${data.saturn_longevity_assessment.saturn_placement}`
                : '—'}
            </span>
            {data.saturn_longevity_assessment.saturn_sign && (
              <span className="ml-2">({data.saturn_longevity_assessment.saturn_sign})</span>
            )}
          </div>
          <p className="text-sm text-foreground/90 leading-relaxed">
            {isHi
              ? data.saturn_longevity_assessment.interpretation_hi
              : data.saturn_longevity_assessment.interpretation_en}
          </p>
        </div>
      </section>

      {/* Karmic transitions */}
      <section className="rounded-xl border-2 border-purple-200 bg-purple-50 p-5">
        <h3 className="font-semibold text-purple-900 mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('auto.karmicTransitions')}
        </h3>
        <p className="text-sm text-purple-900/90 leading-relaxed italic">
          {isHi ? data.karmic_transitions_hi : data.karmic_transitions_en}
        </p>
      </section>

      {/* Life chapters */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3">
          {t('auto.lifeChapters')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(isHi ? data.life_chapters_hi : data.life_chapters_en).map((chapter, i) => {
            const titles = isHi
              ? ['प्रारम्भिक', 'मध्य', 'उत्तर']
              : ['Early', 'Middle', 'Later'];
            return (
              <div
                key={i}
                className="rounded-xl border-2 border-sacred-gold/30 bg-gradient-to-br from-sacred-gold/5 to-transparent p-4"
              >
                <div className="text-[10px] uppercase tracking-widest text-sacred-gold-dark font-semibold mb-2">
                  {titles[i] || `#${i + 1}`}
                </div>
                <p className="text-sm text-foreground/90 leading-relaxed">{chapter}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Footer sloka ref */}
      <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground italic pt-4 border-t border-sacred-gold/20">
        <BookOpen className="w-3 h-3" />
        <span>{data.sloka_ref}</span>
      </div>
    </div>
  );
}
