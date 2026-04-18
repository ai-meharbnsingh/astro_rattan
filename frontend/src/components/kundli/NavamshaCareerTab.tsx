import { useState, useEffect } from 'react';
import { Loader2, Briefcase, BookOpen, CheckCircle2, XCircle, Compass, Sun, Moon } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface PrimaryVocation {
  vocation_en: string;
  vocation_hi: string;
  derivation?: string;
  sloka_ref?: string;
}

interface TenthLordInfo {
  planet: string;
  navamsa_sign: string;
  navamsa_lord: string;
  placement_house?: number;
  placement_sign?: string;
  placement_effect_en?: string;
  placement_effect_hi?: string;
  sloka_ref?: string;
}

interface LuminaryStrength {
  strongest: string;
  sun_score?: number;
  moon_score?: number;
  lagna_score?: number;
  lagna_lord?: string;
  reasoning_en?: string;
  reasoning_hi?: string;
  implication_en?: string;
  implication_hi?: string;
  sloka_ref?: string;
}

interface NavamshaCareerData {
  kundli_id?: string;
  person_name?: string;
  primary_vocation: PrimaryVocation;
  tenth_lord_info: TenthLordInfo;
  luminary_strength: LuminaryStrength;
  recommended_fields_en: string[];
  recommended_fields_hi: string[];
  avoid_fields_en: string[];
  avoid_fields_hi: string[];
  sloka_ref?: string;
}

interface Props {
  kundliId: string;
  language?: string;
}

export default function NavamshaCareerTab({ kundliId, language }: Props) {
  const [data, setData] = useState<NavamshaCareerData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    (async () => {
      try {
        const res = await api.get(`/api/kundli/${kundliId}/navamsha-profession`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Navamsha Career analysis');
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

  const pv = data.primary_vocation;
  const t10 = data.tenth_lord_info;
  const lum = data.luminary_strength;

  const vocation = hi ? pv.vocation_hi : pv.vocation_en;
  const recommended = hi ? (data.recommended_fields_hi || []) : (data.recommended_fields_en || []);
  const avoid = hi ? (data.avoid_fields_hi || []) : (data.avoid_fields_en || []);
  const placementEffect = hi ? t10.placement_effect_hi : t10.placement_effect_en;
  const implication = hi ? lum.implication_hi : lum.implication_en;

  const sunScore = lum.sun_score ?? 0;
  const moonScore = lum.moon_score ?? 0;
  const lagnaScore = lum.lagna_score ?? 0;
  const maxScore = Math.max(sunScore, moonScore, lagnaScore, 1);
  const pct = (v: number) => Math.round((v / maxScore) * 100);

  const strongestLabel =
    lum.strongest === 'sun' ? (hi ? 'सूर्य प्रधान' : 'Sun Dominant') :
    lum.strongest === 'moon' ? (hi ? 'चन्द्र प्रधान' : 'Moon Dominant') :
    (hi ? 'लग्न प्रधान' : 'Lagna Dominant');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Briefcase className="w-6 h-6" />
          {hi ? 'नवांश वृत्ति विश्लेषण' : 'Navamsha Career Analysis'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'D9 (नवांश) चार्ट पर आधारित जीविका एवं व्यवसाय विश्लेषण'
            : 'Vocation and profession analysis based on the D9 (Navamsha) chart'}
        </p>
      </div>

      {/* Hero card — primary vocation */}
      <div className="p-6 rounded-xl border border-sacred-gold/40 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm">
        <div className="flex items-start gap-4">
          <div className="shrink-0 w-14 h-14 rounded-xl bg-sacred-gold/15 flex items-center justify-center">
            <Briefcase className="w-8 h-8 text-sacred-gold-dark" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
              {hi ? 'मुख्य वृत्ति' : 'Primary Vocation'}
            </p>
            <p className="text-base md:text-lg text-foreground leading-relaxed font-medium">
              {vocation || '—'}
            </p>
            {pv.derivation && (
              <p className="text-xs text-muted-foreground mt-2 font-mono">{pv.derivation}</p>
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

      {/* 10th lord + luminary strength */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 10th lord */}
        <div className="p-5 rounded-xl border border-sacred-gold/30 bg-white shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Compass className="w-5 h-5 text-sacred-gold-dark" />
            <h3 className="text-base font-semibold text-sacred-gold-dark">
              {hi ? 'दशम स्वामी (D9)' : '10th Lord in D9'}
            </h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">{hi ? 'ग्रह' : 'Planet'}</span>
              <span className="font-semibold text-foreground">{t10.planet || '—'}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">{hi ? 'नवांश राशि' : 'Navamsha Sign'}</span>
              <span className="font-semibold text-foreground">
                {t10.navamsa_sign || '—'}
                {t10.navamsa_lord ? ` (${t10.navamsa_lord})` : ''}
              </span>
            </div>
            {(t10.placement_house ?? 0) > 0 && (
              <div className="flex items-center justify-between">
                <span className="text-muted-foreground">{hi ? 'भाव' : 'House'}</span>
                <span className="font-semibold text-foreground">
                  {t10.placement_house}
                  {t10.placement_sign ? ` (${t10.placement_sign})` : ''}
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
              {hi ? 'ज्योतिष बल' : 'Luminary Strength'}
            </h3>
          </div>
          {/* Winner badge */}
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-sacred-gold/10 border border-sacred-gold/30 mb-3">
            <span className="text-sm font-bold text-sacred-gold-dark">{strongestLabel}</span>
            {lum.lagna_lord && lum.strongest === 'lagna' && (
              <span className="text-xs text-muted-foreground">({lum.lagna_lord})</span>
            )}
          </div>
          <div className="space-y-3">
            {([
              { key: 'sun', label: hi ? 'सूर्य' : 'Sun', icon: Sun, score: sunScore },
              { key: 'moon', label: hi ? 'चन्द्र' : 'Moon', icon: Moon, score: moonScore },
              { key: 'lagna', label: hi ? 'लग्न' : 'Lagna', icon: Compass, score: lagnaScore },
            ] as const).map(({ key, label, icon: Icon, score }) => {
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
          {(implication || lum.reasoning_en) && (
            <div className="mt-3 pt-3 border-t border-sacred-gold/15">
              {implication && (
                <p className="text-sm text-foreground/90 leading-relaxed">{implication}</p>
              )}
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

      {/* Recommended + Avoid fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-xl border border-emerald-200 bg-emerald-50/40">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-700" />
            <h3 className="text-base font-semibold text-emerald-800">
              {hi ? 'अनुशंसित क्षेत्र' : 'Recommended Fields'}
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
              {hi ? 'परिहार्य क्षेत्र' : 'Fields to Avoid'}
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

      {/* Footer sloka ref */}
      {data.sloka_ref && (
        <div className="flex items-center gap-2 pt-2 border-t border-sacred-gold/20 text-[11px] text-muted-foreground italic">
          <BookOpen className="w-3 h-3 text-sacred-gold-dark shrink-0" />
          <span>{data.sloka_ref}</span>
        </div>
      )}
    </div>
  );
}
