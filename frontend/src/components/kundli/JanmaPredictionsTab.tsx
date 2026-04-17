import { useState, useEffect } from 'react';
import {
  Loader2, User, Moon, Compass, Sparkles, BookOpen,
  CheckCircle2, AlertTriangle, Briefcase, Flame,
} from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface LagnaProfile {
  lagna_sign: string;
  lagna_sign_hi: string;
  body_type_en: string;
  body_type_hi: string;
  temperament_en: string;
  temperament_hi: string;
  fortune_en: string;
  fortune_hi: string;
  lucky_directions_en: string[];
  lucky_directions_hi: string[];
  sloka_ref: string;
}

interface MoonNakshatra {
  nakshatra: string;
  pada: number;
  deity_en: string;
  deity_hi: string;
  symbol_en: string;
  symbol_hi: string;
  character_en: string;
  character_hi: string;
  strengths_en: string[];
  strengths_hi: string[];
  vulnerabilities_en: string[];
  vulnerabilities_hi: string[];
  career_affinity_en: string[];
  career_affinity_hi: string[];
  sloka_ref: string;
}

interface JanmaData {
  kundli_id?: string;
  person_name?: string;
  lagna_profile: LagnaProfile;
  moon_nakshatra: MoonNakshatra;
  combined_narrative_en: string;
  combined_narrative_hi: string;
  sloka_ref: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

export default function JanmaPredictionsTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<JanmaData | null>(null);
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
        const res = await api.get<JanmaData>(`/api/kundli/${kundliId}/janma-predictions`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Janma Predictions');
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

  const lp = data.lagna_profile;
  const mn = data.moon_nakshatra;

  const lagnaName = isHi ? (lp.lagna_sign_hi || lp.lagna_sign) : lp.lagna_sign;
  const bodyType = isHi ? lp.body_type_hi : lp.body_type_en;
  const temperament = isHi ? lp.temperament_hi : lp.temperament_en;
  const fortune = isHi ? lp.fortune_hi : lp.fortune_en;
  const luckyDirs = isHi ? lp.lucky_directions_hi : lp.lucky_directions_en;

  const deity = isHi ? mn.deity_hi : mn.deity_en;
  const symbol = isHi ? mn.symbol_hi : mn.symbol_en;
  const character = isHi ? mn.character_hi : mn.character_en;
  const strengths = isHi ? mn.strengths_hi : mn.strengths_en;
  const vulns = isHi ? mn.vulnerabilities_hi : mn.vulnerabilities_en;
  const careers = isHi ? mn.career_affinity_hi : mn.career_affinity_en;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {t('auto.janmaPredictions')}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi
            ? 'फलदीपिका अध्याय 9 (लग्न फल) एवं अध्याय 10 (चन्द्र-नक्षत्र फल) पर आधारित जन्म-फल।'
            : 'Janma-phala from Phaladeepika Adhyaya 9 (Lagna profile) + Adhyaya 10 (Moon Nakshatra).'}
        </p>
      </div>

      {/* ── Section 1: Lagna Profile ── */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <User className="w-5 h-5" />
          {t('auto.lagnaProfile')}
          {lagnaName && (
            <span className="ml-2 text-sm font-normal text-muted-foreground">
              — {lagnaName}
            </span>
          )}
        </h3>

        {!lp.lagna_sign ? (
          <div className="p-4 rounded-lg bg-gray-50 border border-gray-200 text-gray-600 text-sm">
            {isHi ? 'लग्न उपलब्ध नहीं।' : 'Lagna not available.'}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
              <div className="flex items-center gap-2 text-sacred-gold-dark mb-2 text-sm font-semibold">
                <User className="w-4 h-4" />
                {t('auto.bodyType')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{bodyType}</p>
            </div>

            <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
              <div className="flex items-center gap-2 text-sacred-gold-dark mb-2 text-sm font-semibold">
                <Flame className="w-4 h-4" />
                {t('auto.temperament')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{temperament}</p>
            </div>

            <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5 md:col-span-2">
              <div className="flex items-center gap-2 text-sacred-gold-dark mb-2 text-sm font-semibold">
                <Sparkles className="w-4 h-4" />
                {t('auto.fortuneProfile')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{fortune}</p>
            </div>

            {luckyDirs && luckyDirs.length > 0 && (
              <div className="rounded-xl border-2 border-emerald-200 bg-emerald-50 p-5 md:col-span-2">
                <div className="flex items-center gap-2 text-emerald-800 mb-2 text-sm font-semibold">
                  <Compass className="w-4 h-4" />
                  {t('auto.luckyDirections')}
                </div>
                <div className="flex flex-wrap gap-2">
                  {luckyDirs.map((d, i) => (
                    <span
                      key={`${d}-${i}`}
                      className="text-xs font-medium px-3 py-1 rounded-full bg-emerald-200 text-emerald-900 border border-emerald-300"
                    >
                      {d}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {lp.sloka_ref && (
          <div className="flex items-center gap-1.5 mt-3 text-[11px] text-muted-foreground italic">
            <BookOpen className="w-3 h-3" />
            <span>{lp.sloka_ref}</span>
          </div>
        )}
      </section>

      {/* ── Section 2: Moon Nakshatra ── */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Moon className="w-5 h-5" />
          {t('auto.moonNakshatra')}
          {mn.nakshatra && (
            <span className="ml-2 text-sm font-normal text-muted-foreground">
              — {mn.nakshatra} · {t('auto.pada')} {mn.pada}
            </span>
          )}
        </h3>

        {!mn.nakshatra ? (
          <div className="p-4 rounded-lg bg-gray-50 border border-gray-200 text-gray-600 text-sm">
            {isHi ? 'चन्द्र का नक्षत्र उपलब्ध नहीं।' : 'Moon nakshatra not available.'}
          </div>
        ) : (
          <div className="space-y-4">
            {/* Deity + Symbol row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="rounded-xl border-2 border-indigo-200 bg-indigo-50 p-4">
                <div className="text-[11px] uppercase tracking-wider text-indigo-700 font-semibold mb-1">
                  {t('auto.deity')}
                </div>
                <div className="text-base font-bold text-indigo-900">{deity}</div>
              </div>
              <div className="rounded-xl border-2 border-purple-200 bg-purple-50 p-4">
                <div className="text-[11px] uppercase tracking-wider text-purple-700 font-semibold mb-1">
                  {t('auto.symbol')}
                </div>
                <div className="text-base font-bold text-purple-900">{symbol}</div>
              </div>
            </div>

            {/* Character */}
            <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
              <div className="flex items-center gap-2 text-sacred-gold-dark mb-2 text-sm font-semibold">
                <Moon className="w-4 h-4" />
                {t('auto.characterProfile')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{character}</p>
            </div>

            {/* Strengths — green */}
            {strengths && strengths.length > 0 && (
              <div className="rounded-xl border-2 border-emerald-200 bg-emerald-50 p-4">
                <div className="flex items-center gap-2 text-emerald-800 mb-2 text-sm font-semibold">
                  <CheckCircle2 className="w-4 h-4" />
                  {t('auto.strengthsList')}
                </div>
                <div className="flex flex-wrap gap-2">
                  {strengths.map((s, i) => (
                    <span
                      key={`str-${i}`}
                      className="text-xs font-medium px-3 py-1 rounded-full bg-emerald-200 text-emerald-900 border border-emerald-300"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Vulnerabilities — amber */}
            {vulns && vulns.length > 0 && (
              <div className="rounded-xl border-2 border-amber-200 bg-amber-50 p-4">
                <div className="flex items-center gap-2 text-amber-800 mb-2 text-sm font-semibold">
                  <AlertTriangle className="w-4 h-4" />
                  {t('auto.vulnerabilitiesList')}
                </div>
                <div className="flex flex-wrap gap-2">
                  {vulns.map((v, i) => (
                    <span
                      key={`vul-${i}`}
                      className="text-xs font-medium px-3 py-1 rounded-full bg-amber-200 text-amber-900 border border-amber-300"
                    >
                      {v}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Career affinity — blue */}
            {careers && careers.length > 0 && (
              <div className="rounded-xl border-2 border-blue-200 bg-blue-50 p-4">
                <div className="flex items-center gap-2 text-blue-800 mb-2 text-sm font-semibold">
                  <Briefcase className="w-4 h-4" />
                  {t('auto.careerAffinity')}
                </div>
                <div className="flex flex-wrap gap-2">
                  {careers.map((c, i) => (
                    <span
                      key={`car-${i}`}
                      className="text-xs font-medium px-3 py-1 rounded-full bg-blue-200 text-blue-900 border border-blue-300"
                    >
                      {c}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {mn.sloka_ref && (
          <div className="flex items-center gap-1.5 mt-3 text-[11px] text-muted-foreground italic">
            <BookOpen className="w-3 h-3" />
            <span>{mn.sloka_ref}</span>
          </div>
        )}
      </section>

      {/* Combined narrative */}
      {(data.combined_narrative_en || data.combined_narrative_hi) && (
        <section className="rounded-xl border-2 border-sacred-gold/40 bg-gradient-to-br from-sacred-gold/10 to-amber-50 p-5">
          <h3 className="text-base font-semibold text-sacred-gold-dark mb-2 flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            {isHi ? 'संयुक्त जन्म-फल' : 'Combined Janma Narrative'}
          </h3>
          <p className="text-sm text-foreground leading-relaxed">
            {isHi ? data.combined_narrative_hi : data.combined_narrative_en}
          </p>
        </section>
      )}

      {/* Footer sloka ref */}
      <div className="text-center text-xs text-muted-foreground italic pt-4 border-t border-sacred-gold/20">
        {data.sloka_ref}
      </div>
    </div>
  );
}
