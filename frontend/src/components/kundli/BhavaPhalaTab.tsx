import { useState, useEffect } from 'react';
import { Loader2, Home, Star, BookOpen, Sparkles, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface PlanetPlacement {
  planet: string;
  house: number;
  sign: string;
  effect_en: string;
  effect_hi: string;
  sloka_ref: string;
}

interface BhavaGeneral {
  house: number;
  name_en: string;
  name_hi: string;
  general_en: string;
  general_hi: string;
  sloka_ref: string;
  status: 'strong' | 'weak' | 'neutral';
}

interface ApiResponse {
  kundli_id?: string;
  person_name?: string;
  planet_placements: PlanetPlacement[];
  bhava_generals: BhavaGeneral[];
  sloka_ref: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const STATUS_STYLE: Record<string, { card: string; badge: string; Icon: typeof TrendingUp; key: string }> = {
  strong:  { card: 'border-emerald-300 bg-emerald-50', badge: 'bg-emerald-600 text-white', Icon: TrendingUp,   key: 'auto.bhavaStrong' },
  weak:    { card: 'border-red-300 bg-red-50',          badge: 'bg-red-600 text-white',     Icon: TrendingDown, key: 'auto.bhavaWeak' },
  neutral: { card: 'border-sacred-gold/30 bg-sacred-gold/5', badge: 'bg-sacred-gold-dark text-white', Icon: Minus, key: 'auto.bhavaNeutral' },
};

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'बृहस्पति', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

export default function BhavaPhalaTab({ kundliId, language, t }: Props) {
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
        const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/bhava-phala`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Bhava Phala');
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
          {t('auto.bhavaPhala')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.bhavaPhalaDesc')}</p>
      </div>

      {/* Section 1: Planet in House */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Star className="w-5 h-5" />
          {t('auto.planetInHouse')}
        </h3>
        {data.planet_placements.length === 0 ? (
          <div className="p-4 rounded-lg bg-gray-50 border border-gray-200 text-gray-600 text-sm">
            {isHi ? 'कोई ग्रह-स्थापना नहीं मिली।' : 'No planet placements available.'}
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {data.planet_placements.map((pp, i) => {
              const effect = isHi ? pp.effect_hi : pp.effect_en;
              const planetName = isHi ? (PLANET_HI[pp.planet] || pp.planet) : pp.planet;
              return (
                <div
                  key={`${pp.planet}-${i}`}
                  className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5"
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                      <h4 className="text-lg font-bold text-foreground">{planetName}</h4>
                      <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                        <span>{isHi ? 'भाव' : 'House'} {pp.house}</span>
                        <span>•</span>
                        <span>{pp.sign}</span>
                      </div>
                    </div>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-sacred-gold-dark text-white">
                      {isHi ? 'भाव' : 'H'} {pp.house}
                    </span>
                  </div>
                  <p className="text-sm text-foreground leading-relaxed mb-3">{effect}</p>
                  <div className="flex items-center gap-1.5 pt-2 border-t border-sacred-gold/20 text-[11px] text-muted-foreground">
                    <BookOpen className="w-3 h-3" />
                    <span className="italic">{pp.sloka_ref}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Section 2: House-wise Status */}
      <section>
        <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Home className="w-5 h-5" />
          {t('auto.houseStatus')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.bhava_generals.map((b) => {
            const style = STATUS_STYLE[b.status] || STATUS_STYLE.neutral;
            const StatusIcon = style.Icon;
            const name = isHi ? b.name_hi : b.name_en;
            const general = isHi ? b.general_hi : b.general_en;
            const localizedBhava = t(`auto.bhava${b.house}`);
            return (
              <div
                key={b.house}
                className={`rounded-xl border-2 p-4 ${style.card}`}
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <div className="text-xs font-semibold text-muted-foreground">
                      {isHi ? 'भाव' : 'Bhava'} {b.house}
                    </div>
                    <h4 className="text-base font-bold text-foreground leading-tight">
                      {localizedBhava || name}
                    </h4>
                  </div>
                  <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded inline-flex items-center gap-1 ${style.badge}`}>
                    <StatusIcon className="w-3 h-3" />
                    {t(style.key)}
                  </span>
                </div>
                <p className="text-xs text-foreground/80 leading-relaxed mb-2">{general}</p>
                <div className="flex items-center gap-1.5 pt-2 border-t border-current/10 text-[10px] text-muted-foreground">
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
