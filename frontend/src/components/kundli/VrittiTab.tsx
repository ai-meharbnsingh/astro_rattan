import { useState, useEffect } from 'react';
import { Loader2, Briefcase, BookOpen, Sun, Moon, Compass, CheckCircle2, XCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface PrimaryVocation {
  vocation_en: string;
  vocation_hi: string;
  derivation: string;
  sloka_ref: string;
}

interface TenthLordInfo {
  planet: string;
  navamsa_sign: string;
  navamsa_lord: string;
  placement_house: number;
  placement_sign: string;
  placement_effect_en: string;
  placement_effect_hi: string;
  sloka_ref?: string;
}

interface LuminaryStrength {
  strongest: string;
  sun_score: number;
  moon_score: number;
  lagna_score: number;
  lagna_lord?: string;
  reasoning_en: string;
  reasoning_hi: string;
  implication_en?: string;
  implication_hi?: string;
  sloka_ref?: string;
}

interface VrittiData {
  primary_vocation: PrimaryVocation;
  tenth_lord_info: TenthLordInfo;
  luminary_strength: LuminaryStrength;
  recommended_fields_en: string[];
  recommended_fields_hi: string[];
  avoid_fields_en: string[];
  avoid_fields_hi: string[];
  sloka_ref: string;
  kundli_id?: string;
  person_name?: string;
}

interface NavamshaData {
  d9_10th_lord?: string;
  element?: string;
  career_en?: string;
  career_hi?: string;
  suited_fields?: string[];
  sloka_ref?: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

export default function VrittiTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<VrittiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [navamsha, setNavamsha] = useState<NavamshaData | null>(null);
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const res = await api.get<VrittiData>(`/api/kundli/${kundliId}/vritti`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Vritti analysis');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<NavamshaData>(`/api/kundli/${kundliId}/navamsha-profession`)
      .then(res => { if (!cancelled) setNavamsha(res); })
      .catch(() => {});
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

  const pv = data.primary_vocation;
  const t10 = data.tenth_lord_info;
  const lum = data.luminary_strength;

  const vocation = isHi ? pv.vocation_hi : pv.vocation_en;
  const placementEffect = isHi ? t10.placement_effect_hi : t10.placement_effect_en;
  const implication = isHi ? lum.implication_hi : lum.implication_en;
  const reasoning = isHi ? lum.reasoning_hi : lum.reasoning_en;
  const recommended = isHi ? data.recommended_fields_hi : data.recommended_fields_en;
  const avoid = isHi ? data.avoid_fields_hi : data.avoid_fields_en;

  const maxScore = Math.max(lum.sun_score, lum.moon_score, lum.lagna_score, 1);
  const pct = (v: number) => Math.round((v / maxScore) * 100);

  const strongestKey =
    lum.strongest === 'sun'
      ? t('auto.sunStrongest')
      : lum.strongest === 'moon'
        ? t('auto.moonStrongest')
        : t('auto.lagnaStrongest');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Briefcase className="w-6 h-6" />
          {t('auto.vritti')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.vrittiDesc')}</p>
      </div>

      {/* Hero card — primary vocation */}
      <div className="p-6 rounded-xl border border-sacred-gold/40 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm">
        <div className="flex items-start gap-4">
          <div className="shrink-0 w-14 h-14 rounded-xl bg-sacred-gold/15 flex items-center justify-center">
            <Briefcase className="w-8 h-8 text-sacred-gold-dark" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
              {t('auto.primaryVocation')}
            </p>
            <p className="text-base md:text-lg text-foreground leading-relaxed">{vocation}</p>
            {pv.derivation && (
              <p className="text-xs text-muted-foreground mt-2 font-mono">
                {pv.derivation}
              </p>
            )}
            {pv.sloka_ref && (
              <div className="flex items-center gap-1.5 pt-3 mt-3 border-t border-sacred-gold/15 text-[11px] text-muted-foreground">
                <BookOpen className="w-3 h-3" />
                <span className="italic">{pv.sloka_ref}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 10th lord + luminary strength (2-column on md+) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 10th lord info */}
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-white shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Compass className="w-5 h-5 text-sacred-gold-dark" />
            <h3 className="text-base font-semibold text-sacred-gold-dark">
              {t('auto.tenthLord')}
            </h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">{t('auto.tenthLord')}</span>
              <span className="font-semibold text-foreground">{t10.planet || '—'}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">{t('auto.navamsaPlacement')}</span>
              <span className="font-semibold text-foreground">
                {t10.navamsa_sign || '—'}
                {t10.navamsa_lord ? ` (${t10.navamsa_lord})` : ''}
              </span>
            </div>
            {t10.placement_house > 0 && (
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">House</span>
                <span className="font-semibold text-foreground">
                  {t10.placement_house} ({t10.placement_sign})
                </span>
              </div>
            )}
            {placementEffect && (
              <p className="text-sm text-foreground/90 leading-relaxed pt-3 border-t border-sacred-gold/15">
                {placementEffect}
              </p>
            )}
            {t10.sloka_ref && (
              <div className="flex items-center gap-1.5 pt-2 text-[11px] text-muted-foreground">
                <BookOpen className="w-3 h-3" />
                <span className="italic">{t10.sloka_ref}</span>
              </div>
            )}
          </div>
        </div>

        {/* Luminary strength */}
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-white shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Sun className="w-5 h-5 text-sacred-gold-dark" />
            <h3 className="text-base font-semibold text-sacred-gold-dark">
              {t('auto.luminaryStrength')}
            </h3>
          </div>
          {/* Winner badge */}
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-sacred-gold/10 border border-sacred-gold/30 mb-3">
            <span className="text-base font-bold text-sacred-gold-dark">{strongestKey}</span>
            {lum.lagna_lord && lum.strongest === 'lagna' && (
              <span className="text-xs text-muted-foreground">({lum.lagna_lord})</span>
            )}
          </div>
          <div className="space-y-3">
            {[
              { key: 'sun', label: 'Sun / सूर्य', icon: Sun, score: lum.sun_score },
              { key: 'moon', label: 'Moon / चन्द्र', icon: Moon, score: lum.moon_score },
              { key: 'lagna', label: 'Lagna / लग्न', icon: Compass, score: lum.lagna_score },
            ].map(({ key, label, icon: Icon, score }) => {
              const isWinner = lum.strongest === key;
              return (
                <div key={key}>
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className={`flex items-center gap-1.5 ${isWinner ? 'font-bold text-sacred-gold-dark' : 'text-muted-foreground'}`}>
                      <Icon className="w-3.5 h-3.5" />
                      {label}
                    </span>
                    <span className={isWinner ? 'font-bold text-sacred-gold-dark' : 'text-muted-foreground'}>
                      {score}
                    </span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-gray-200 overflow-hidden">
                    <div
                      className={`h-full transition-all ${isWinner ? 'bg-sacred-gold' : 'bg-sacred-gold/40'}`}
                      style={{ width: `${pct(score)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
          <div className="mt-3 pt-3 border-t border-sacred-gold/15">
            {implication && (
              <p className="text-sm text-foreground/90 leading-relaxed">{implication}</p>
            )}
            {reasoning && (
              <div className="mt-2">
                <p className="text-[10px] text-muted-foreground font-semibold uppercase tracking-wide mb-0.5">
                  {isHi ? 'बल-स्कोर विश्लेषण' : 'Strength Analysis'}
                </p>
                <p className="text-[11px] text-muted-foreground font-mono">{reasoning}</p>
              </div>
            )}
            {lum.sloka_ref && (
              <div className="flex items-center gap-1.5 pt-2 mt-2 text-[11px] text-muted-foreground">
                <BookOpen className="w-3 h-3" />
                <span className="italic">{lum.sloka_ref}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recommended + Avoid fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-xl border border-emerald-200 bg-emerald-50/40">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-700" />
            <h3 className="text-base font-semibold text-emerald-800">
              {t('auto.recommendedFields')}
            </h3>
          </div>
          {recommended.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {recommended.map((f, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded-full bg-emerald-100 border border-emerald-200 text-emerald-800 text-xs font-medium"
                >
                  {f}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-xs text-muted-foreground italic">—</p>
          )}
        </div>

        <div className="p-5 rounded-xl border border-red-200 bg-red-50/40">
          <div className="flex items-center gap-2 mb-3">
            <XCircle className="w-5 h-5 text-red-700" />
            <h3 className="text-base font-semibold text-red-800">
              {t('auto.avoidFields')}
            </h3>
          </div>
          {avoid.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {avoid.map((f, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded-full bg-red-100 border border-red-200 text-red-800 text-xs font-medium"
                >
                  {f}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-xs text-muted-foreground italic">—</p>
          )}
        </div>
      </div>

      {/* Navamsha Profession (D9) */}
      {navamsha && (
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-white shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Compass className="w-5 h-5 text-sacred-gold-dark" />
            <h3 className="text-base font-semibold text-sacred-gold-dark">
              {isHi ? 'नवांश वृत्ति (D9)' : 'Navamsha Profession (D9)'}
            </h3>
          </div>
          <div className="flex flex-wrap items-center gap-3 mb-3 text-sm">
            {navamsha.d9_10th_lord && (
              <div>
                <span className="text-muted-foreground">{isHi ? 'D9 दशम स्वामी:' : 'D9 10th Lord:'}</span>
                <span className="ml-1 font-semibold text-foreground">{navamsha.d9_10th_lord}</span>
              </div>
            )}
            {navamsha.element && (
              <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                navamsha.element === 'fire' ? 'bg-red-100 text-red-700' :
                navamsha.element === 'earth' ? 'bg-green-100 text-green-700' :
                navamsha.element === 'water' ? 'bg-blue-100 text-blue-700' :
                'bg-amber-100 text-amber-700'
              }`}>
                {navamsha.element.charAt(0).toUpperCase() + navamsha.element.slice(1)}
              </span>
            )}
          </div>
          {(navamsha.career_en || navamsha.career_hi) && (
            <p className="text-sm text-foreground/90 leading-relaxed mb-3">
              {isHi ? (navamsha.career_hi || navamsha.career_en) : navamsha.career_en}
            </p>
          )}
          {navamsha.suited_fields && navamsha.suited_fields.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {navamsha.suited_fields.map((f, i) => (
                <span key={i} className="px-2.5 py-1 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 text-sacred-gold-dark text-xs font-medium">
                  {f}
                </span>
              ))}
            </div>
          )}
          {navamsha.sloka_ref && (
            <div className="flex items-center gap-1.5 pt-3 mt-3 border-t border-sacred-gold/15 text-[11px] text-muted-foreground">
              <BookOpen className="w-3 h-3" />
              <span className="italic">{navamsha.sloka_ref}</span>
            </div>
          )}
        </div>
      )}

      {/* Career guidance footer */}
      <div className="p-4 rounded-lg bg-sacred-gold/5 border border-sacred-gold/20 text-xs text-muted-foreground flex items-start gap-2">
        <BookOpen className="w-4 h-4 text-sacred-gold-dark shrink-0 mt-0.5" />
        <div>
          <span className="font-semibold text-foreground">{t('auto.careerGuidance')}:</span>
          {' '}
          <span className="italic">{data.sloka_ref}</span>
        </div>
      </div>
    </div>
  );
}
