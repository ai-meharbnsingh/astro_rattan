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
  d9_lagna?: string;
  d9_lagna_hi?: string;
  d9_10th_house_sign?: string;
  d9_10th_house_sign_hi?: string;
  d9_10th_lord?: string;
  d9_10th_lord_sign?: string;
  d9_10th_lord_sign_hi?: string;
  profession_type_en?: string;
  profession_type_hi?: string;
  detailed_interpretation_en?: string;
  detailed_interpretation_hi?: string;
  supporting_planets_en?: string;
  supporting_planets_hi?: string;
  career_examples_en?: string[];
  career_examples_hi?: string[];
  sloka_ref?: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdMuted     = 'p-1.5 text-xs text-muted-foreground border-t border-border align-top w-[40%]';
const tdVal       = 'p-1.5 text-xs font-medium text-foreground border-t border-border align-top';

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

  const pv  = data.primary_vocation;
  const t10 = data.tenth_lord_info;
  const lum = data.luminary_strength;

  const vocation        = isHi ? pv.vocation_hi : pv.vocation_en;
  const placementEffect = isHi ? t10.placement_effect_hi : t10.placement_effect_en;
  const implication     = isHi ? lum.implication_hi : lum.implication_en;
  const reasoning       = isHi ? lum.reasoning_hi : lum.reasoning_en;
  const recommended     = isHi ? data.recommended_fields_hi : data.recommended_fields_en;
  const avoid           = isHi ? data.avoid_fields_hi : data.avoid_fields_en;

  const maxScore = Math.max(lum.sun_score, lum.moon_score, lum.lagna_score, 1);
  const pct = (v: number) => Math.round((v / maxScore) * 100);

  const strongestKey =
    lum.strongest === 'sun'   ? t('auto.sunStrongest') :
    lum.strongest === 'moon'  ? t('auto.moonStrongest') :
                                t('auto.lagnaStrongest');

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

      {/* Primary Vocation */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Briefcase className="w-4 h-4" />
          <span>{t('auto.primaryVocation')}</span>
        </div>
        <div className="px-4 py-3">
          <p className="text-base font-semibold text-foreground leading-relaxed mb-2">{vocation}</p>
          {pv.derivation && (
            <p className="text-xs text-muted-foreground font-mono mb-2">{pv.derivation}</p>
          )}
          {pv.sloka_ref && (
            <div className="flex items-center gap-1.5 pt-2 border-t border-border text-[11px] text-muted-foreground">
              <BookOpen className="w-3 h-3" />
              <span className="italic">{pv.sloka_ref}</span>
            </div>
          )}
        </div>
      </div>

      {/* 10th Lord + Luminary side by side */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {/* 10th Lord */}
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Compass className="w-4 h-4" />
            <span>{t('auto.tenthLord')}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '45%' }} />
              <col style={{ width: '55%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'विषय' : 'Factor'}</th>
                <th className={thCls}>{isHi ? 'विवरण' : 'Value'}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className={tdMuted}>{t('auto.tenthLord')}</td>
                <td className={tdVal}>{t10.planet || '—'}</td>
              </tr>
              <tr>
                <td className={tdMuted}>{t('auto.navamsaPlacement')}</td>
                <td className={tdVal}>{t10.navamsa_sign || '—'}{t10.navamsa_lord ? ` (${t10.navamsa_lord})` : ''}</td>
              </tr>
              {t10.placement_house > 0 && (
                <tr>
                  <td className={tdMuted}>{isHi ? 'भाव स्थिति' : 'Placement'}</td>
                  <td className={tdVal}>{t('auto.house')} {t10.placement_house} · {t10.placement_sign}</td>
                </tr>
              )}
            </tbody>
          </table>
          {placementEffect && (
            <div className="px-3 py-2 border-t border-border">
              <p className="text-xs text-foreground/80 leading-relaxed">{placementEffect}</p>
              {t10.sloka_ref && (
                <div className="flex items-center gap-1 mt-2 text-[10px] text-muted-foreground italic">
                  <BookOpen className="w-2.5 h-2.5" />
                  <span>{t10.sloka_ref}</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Luminary Strength */}
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Sun className="w-4 h-4" />
            <span>{t('auto.luminaryStrength')}</span>
            <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">{strongestKey}</span>
          </div>
          <div className="px-4 py-3 space-y-3">
            {[
              { key: 'sun',   label: isHi ? 'सूर्य' : 'Sun',   Icon: Sun,     score: lum.sun_score },
              { key: 'moon',  label: isHi ? 'चन्द्र' : 'Moon', Icon: Moon,    score: lum.moon_score },
              { key: 'lagna', label: isHi ? 'लग्न' : 'Lagna',  Icon: Compass, score: lum.lagna_score },
            ].map(({ key, label, Icon, score }) => {
              const isWinner = lum.strongest === key;
              return (
                <div key={key}>
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className={`flex items-center gap-1.5 ${isWinner ? 'font-bold text-sacred-gold-dark' : 'text-muted-foreground'}`}>
                      <Icon className="w-3.5 h-3.5" />
                      {label}
                      {key === 'lagna' && lum.lagna_lord && isWinner && (
                        <span className="font-normal text-muted-foreground">({lum.lagna_lord})</span>
                      )}
                    </span>
                    <span className={isWinner ? 'font-bold text-sacred-gold-dark' : 'text-muted-foreground'}>{score}</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-border overflow-hidden">
                    <div
                      className={`h-full transition-all ${isWinner ? 'bg-sacred-gold' : 'bg-sacred-gold/30'}`}
                      style={{ width: `${pct(score)}%` }}
                    />
                  </div>
                </div>
              );
            })}
            {(implication || reasoning) && (
              <div className="pt-3 border-t border-border space-y-1">
                {implication && <p className="text-xs text-foreground/80 leading-relaxed">{implication}</p>}
                {reasoning && <p className="text-[10px] text-muted-foreground font-mono">{reasoning}</p>}
              </div>
            )}
            {lum.sloka_ref && (
              <div className="flex items-center gap-1 text-[10px] text-muted-foreground italic">
                <BookOpen className="w-2.5 h-2.5" />
                <span>{lum.sloka_ref}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recommended + Avoid fields */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Briefcase className="w-4 h-4" />
          <span>{isHi ? 'उचित एवं अनुचित क्षेत्र' : 'Recommended & Avoid Fields'}</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-border">
          <div className="px-4 py-3">
            <div className="flex items-center gap-1.5 mb-2">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <p className="text-xs font-semibold text-emerald-700">{t('auto.recommendedFields')}</p>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {recommended.length > 0 ? recommended.map((f, i) => (
                <span key={i} className="px-2 py-0.5 rounded-full text-xs bg-emerald-100 text-emerald-800 border border-emerald-200">{f}</span>
              )) : <span className="text-xs text-muted-foreground">—</span>}
            </div>
          </div>
          <div className="px-4 py-3">
            <div className="flex items-center gap-1.5 mb-2">
              <XCircle className="w-3.5 h-3.5 text-red-600" />
              <p className="text-xs font-semibold text-red-700">{t('auto.avoidFields')}</p>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {avoid.length > 0 ? avoid.map((f, i) => (
                <span key={i} className="px-2 py-0.5 rounded-full text-xs bg-red-100 text-red-800 border border-red-200">{f}</span>
              )) : <span className="text-xs text-muted-foreground">—</span>}
            </div>
          </div>
        </div>
      </div>

      {/* Navamsha Profession (D9) */}
      {navamsha && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Compass className="w-4 h-4" />
            <span>{isHi ? 'नवांश वृत्ति (D9)' : 'Navamsha Profession (D9)'}</span>
            {navamsha.profession_type_en && (
              <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">
                {isHi ? navamsha.profession_type_hi : navamsha.profession_type_en}
              </span>
            )}
          </div>
          {/* Key facts table */}
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '40%' }} />
              <col style={{ width: '60%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'विषय' : 'Factor'}</th>
                <th className={thCls}>{isHi ? 'विवरण' : 'Value'}</th>
              </tr>
            </thead>
            <tbody>
              {navamsha.d9_lagna && (
                <tr>
                  <td className={tdMuted}>{isHi ? 'D9 लग्न' : 'D9 Lagna'}</td>
                  <td className={tdVal}>{isHi ? (navamsha.d9_lagna_hi || navamsha.d9_lagna) : navamsha.d9_lagna}</td>
                </tr>
              )}
              {navamsha.d9_10th_house_sign && (
                <tr>
                  <td className={tdMuted}>{isHi ? 'D9 दशम राशि' : 'D9 10th Sign'}</td>
                  <td className={tdVal}>{isHi ? (navamsha.d9_10th_house_sign_hi || navamsha.d9_10th_house_sign) : navamsha.d9_10th_house_sign}</td>
                </tr>
              )}
              {navamsha.d9_10th_lord && (
                <tr>
                  <td className={tdMuted}>{isHi ? 'D9 दशम स्वामी' : 'D9 10th Lord'}</td>
                  <td className={tdVal}>{navamsha.d9_10th_lord}{navamsha.d9_10th_lord_sign ? ` · ${isHi ? (navamsha.d9_10th_lord_sign_hi || navamsha.d9_10th_lord_sign) : navamsha.d9_10th_lord_sign}` : ''}</td>
                </tr>
              )}
            </tbody>
          </table>
          <div className="px-3 py-3 border-t border-border space-y-2">
            {(navamsha.detailed_interpretation_en || navamsha.detailed_interpretation_hi) && (
              <p className="text-xs text-foreground/80 leading-relaxed">
                {isHi ? (navamsha.detailed_interpretation_hi || navamsha.detailed_interpretation_en) : navamsha.detailed_interpretation_en}
              </p>
            )}
            {(navamsha.supporting_planets_en || navamsha.supporting_planets_hi) && (
              <p className="text-xs text-muted-foreground italic">
                {isHi ? (navamsha.supporting_planets_hi || navamsha.supporting_planets_en) : navamsha.supporting_planets_en}
              </p>
            )}
            {(() => {
              const examples = isHi ? navamsha.career_examples_hi : navamsha.career_examples_en;
              return examples && examples.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {examples.map((f, i) => (
                    <span key={i} className="px-2 py-0.5 rounded-full text-xs bg-amber-100 text-amber-800 border border-amber-200">{f}</span>
                  ))}
                </div>
              ) : null;
            })()}
            {navamsha.sloka_ref && (
              <div className="flex items-center gap-1 pt-1 border-t border-border text-[10px] text-muted-foreground italic">
                <BookOpen className="w-2.5 h-2.5" />
                <span>{navamsha.sloka_ref}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground italic pt-2 border-t border-border">
        <BookOpen className="w-3 h-3" />
        <span>{data.sloka_ref}</span>
      </div>
    </div>
  );
}
