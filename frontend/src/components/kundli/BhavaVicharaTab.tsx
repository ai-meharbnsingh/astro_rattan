import { useState, useEffect } from 'react';
import { Loader2, Sparkles, BookOpen, Shield, AlertTriangle, Home } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface BhavaAssessment {
  house: number;
  name_en: string;
  name_hi: string;
  lord: string;
  lord_placement: number;
  karaka: string;
  flourishing: boolean;
  destruction_risk: boolean;
  reasons_en: string[];
  reasons_hi: string[];
  karaka_as_lagna_analysis_en: string;
  karaka_as_lagna_analysis_hi: string;
  sloka_ref: string;
}

interface ApiResponse {
  kundli_id?: string;
  person_name?: string;
  bhava_assessments: BhavaAssessment[];
  overall_strongest: number[];
  overall_weakest: number[];
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

function localizePlanet(name: string, isHi: boolean): string {
  if (!isHi) return name;
  // Handle compound karakas like "Mars/Saturn"
  if (name.includes('/')) {
    return name.split('/').map((n) => PLANET_HI[n.trim()] || n.trim()).join(' / ');
  }
  return PLANET_HI[name] || name;
}

export default function BhavaVicharaTab({ kundliId, language, t }: Props) {
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
        const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/bhava-vichara`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Bhava Vichara');
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

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {t('auto.bhavaVichara')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.bhavaVicharaDesc')}</p>
      </div>

      {/* Summary: Strongest & Weakest */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border-2 border-emerald-300 bg-emerald-50 p-4">
          <div className="flex items-center gap-2 mb-2 text-emerald-800">
            <Shield className="w-5 h-5" />
            <h3 className="font-semibold">{t('auto.strongestHouses')}</h3>
          </div>
          {data.overall_strongest.length === 0 ? (
            <p className="text-xs text-emerald-700 italic">
              {isHi ? 'कोई भाव वर्तमान में स्पष्ट रूप से प्रबल नहीं।' : 'No house is clearly flourishing.'}
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {data.overall_strongest.map((h) => (
                <span key={h} className="text-xs font-semibold px-2 py-1 rounded bg-emerald-600 text-white">
                  {isHi ? 'भाव' : 'H'} {h}
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-xl border-2 border-red-300 bg-red-50 p-4">
          <div className="flex items-center gap-2 mb-2 text-red-800">
            <AlertTriangle className="w-5 h-5" />
            <h3 className="font-semibold">{t('auto.weakestHouses')}</h3>
          </div>
          {data.overall_weakest.length === 0 ? (
            <p className="text-xs text-red-700 italic">
              {isHi ? 'कोई भाव दबाव में नहीं।' : 'No house is under destruction-pattern pressure.'}
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {data.overall_weakest.map((h) => (
                <span key={h} className="text-xs font-semibold px-2 py-1 rounded bg-red-600 text-white">
                  {isHi ? 'भाव' : 'H'} {h}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 12 House Cards */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Home className="w-5 h-5" />
          {t('auto.houseStatus')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.bhava_assessments.map((b) => {
            const name = isHi ? b.name_hi : b.name_en;
            const reasons = isHi ? b.reasons_hi : b.reasons_en;
            const karakaNarr = isHi ? b.karaka_as_lagna_analysis_hi : b.karaka_as_lagna_analysis_en;
            const cardClass = b.destruction_risk
              ? 'border-red-300 bg-red-50'
              : b.flourishing
                ? 'border-emerald-300 bg-emerald-50'
                : 'border-sacred-gold/30 bg-sacred-gold/5';

            return (
              <div key={b.house} className={`rounded-xl border-2 p-5 ${cardClass}`}>
                {/* Title row */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <div className="text-xs font-semibold text-muted-foreground">
                      {isHi ? 'भाव' : 'Bhava'} {b.house}
                    </div>
                    <h4 className="text-base font-bold text-foreground leading-tight">{name}</h4>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    {b.flourishing && (
                      <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded inline-flex items-center gap-1 bg-emerald-600 text-white">
                        <Shield className="w-3 h-3" />
                        {t('auto.bhavaFlourishing')}
                      </span>
                    )}
                    {b.destruction_risk && (
                      <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded inline-flex items-center gap-1 bg-red-600 text-white">
                        <AlertTriangle className="w-3 h-3" />
                        {t('auto.bhavaDestructionRisk')}
                      </span>
                    )}
                  </div>
                </div>

                {/* Lord + Karaka */}
                <div className="grid grid-cols-2 gap-2 mb-3 text-xs">
                  <div className="rounded bg-white/60 px-2 py-1">
                    <div className="text-[10px] uppercase tracking-wide text-muted-foreground">
                      {t('auto.bhavaLord')}
                    </div>
                    <div className="font-semibold text-foreground">
                      {b.lord ? localizePlanet(b.lord, isHi) : '—'}
                      {b.lord_placement > 0 && (
                        <span className="font-normal text-muted-foreground ml-1">
                          ({isHi ? 'भाव' : 'H'} {b.lord_placement})
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="rounded bg-white/60 px-2 py-1">
                    <div className="text-[10px] uppercase tracking-wide text-muted-foreground">
                      {t('auto.bhavaKaraka')}
                    </div>
                    <div className="font-semibold text-foreground">
                      {b.karaka ? localizePlanet(b.karaka, isHi) : '—'}
                    </div>
                  </div>
                </div>

                {/* Reasons */}
                {reasons.length > 0 && (
                  <ul className="text-xs space-y-1 mb-3 list-disc list-inside text-foreground/80">
                    {reasons.map((r, i) => (
                      <li key={i} className="leading-relaxed">{r}</li>
                    ))}
                  </ul>
                )}

                {/* Karaka-as-Lagna narrative */}
                <div className="mt-2 pt-2 border-t border-current/10">
                  <div className="text-[10px] uppercase tracking-wide text-muted-foreground mb-1">
                    {t('auto.karakaAsLagna')}
                  </div>
                  <p className="text-xs text-foreground/80 leading-relaxed italic">{karakaNarr}</p>
                </div>

                {/* Sloka ref */}
                <div className="flex items-center gap-1.5 pt-2 mt-2 border-t border-current/10 text-[10px] text-muted-foreground">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{b.sloka_ref}</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Footer sloka ref */}
      <div className="text-center text-xs text-muted-foreground italic pt-4 border-t border-sacred-gold/20">
        {data.sloka_ref}
      </div>
    </div>
  );
}
