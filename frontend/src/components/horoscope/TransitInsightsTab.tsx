import { ArrowRight } from 'lucide-react';

interface Transit {
  planet: string;
  planet_hindi: string;
  current_sign: string;
  current_sign_hindi: string;
}

interface SignEffect {
  sign: string;
  sign_hindi: string;
  emoji: string;
  ruling_planet: string;
  ruling_planet_hindi: string;
  ruler_current_sign: string;
  ruler_current_sign_hindi: string;
  dignity: string;
  strength: string;
}

interface TransitData {
  date: string;
  transits: Transit[];
  sign_effects: SignEffect[];
}

interface Props {
  data: TransitData | null;
  loading: boolean;
  language: string;
  t: (key: string) => string;
}

const STRENGTH_LABELS: Record<string, { en: string; hi: string; color: string; bg: string }> = {
  very_strong: { en: 'Very Strong', hi: 'अत्यंत बलवान', color: 'text-emerald-700', bg: 'bg-emerald-100' },
  strong: { en: 'Strong', hi: 'बलवान', color: 'text-green-700', bg: 'bg-green-100' },
  moderate: { en: 'Moderate', hi: 'सामान्य', color: 'text-amber-700', bg: 'bg-amber-100' },
  weak: { en: 'Weak', hi: 'दुर्बल', color: 'text-red-700', bg: 'bg-red-100' },
};

const DIGNITY_LABELS: Record<string, { en: string; hi: string }> = {
  exalted: { en: 'Exalted', hi: 'उच्च' },
  own_sign: { en: 'Own Sign', hi: 'स्वराशि' },
  neutral: { en: 'Neutral', hi: 'सम' },
  debilitated: { en: 'Debilitated', hi: 'नीच' },
};

export default function TransitInsightsTab({ data, loading, language, t }: Props) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="h-64 animate-pulse bg-gray-200 rounded-xl" />
        <div className="h-64 animate-pulse bg-gray-200 rounded-xl" />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-cosmic-text-secondary">
        {t('auto.transitDataUnavailab')}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-start">
      {/* Current Planetary Positions */}
      <div className="rounded-xl border border-cosmic-border bg-cosmic-card p-3">
        <h3 className="text-sm font-semibold text-sacred-gold-dark mb-2">
          {t('auto.currentPlanetaryPosi')}
        </h3>
        <div className="rounded-lg border border-cosmic-border overflow-hidden">
          <table className="w-full table-fixed text-xs sm:text-sm">
            <thead>
              <tr className="bg-sacred-gold/15">
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[40%]">
                  {t('auto.planet')}
                </th>
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[15%]" />
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[45%]">
                  {t('auto.currentSign')}
                </th>
              </tr>
            </thead>
            <tbody>
              {data.transits.map((tr) => (
                <tr key={tr.planet} className="border-b border-cosmic-border/50 last:border-0">
                  <td className="px-2 py-1.5 font-medium text-cosmic-text">
                    {language === 'hi' ? tr.planet_hindi : tr.planet}
                  </td>
                  <td className="px-2 py-1.5 text-cosmic-text-secondary">
                    <ArrowRight className="w-3 h-3" />
                  </td>
                  <td className="px-2 py-1.5 text-cosmic-text">
                    {language === 'hi' ? tr.current_sign_hindi : tr.current_sign}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Sign-wise Effects */}
      <div className="rounded-xl border border-cosmic-border bg-cosmic-card p-3">
        <h3 className="text-sm font-semibold text-sacred-gold-dark mb-2">
          {t('auto.signWiseTransitEffec')}
        </h3>
        <div className="rounded-lg border border-cosmic-border overflow-hidden">
          <table className="w-full table-fixed text-xs sm:text-sm">
            <thead>
              <tr className="bg-sacred-gold/15">
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[20%]">
                  {t('auto.sign')}
                </th>
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[20%]">
                  {t('auto.ruler')}
                </th>
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[22%]">
                  {t('auto.rulerIn')}
                </th>
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[18%]">
                  {t('auto.dignity')}
                </th>
                <th className="text-left px-2 py-1.5 text-sacred-gold-dark font-semibold w-[20%]">
                  {t('auto.strength')}
                </th>
              </tr>
            </thead>
            <tbody>
              {data.sign_effects.map((effect) => {
                const strengthInfo = STRENGTH_LABELS[effect.strength] || STRENGTH_LABELS.moderate;
                const dignityInfo = DIGNITY_LABELS[effect.dignity] || DIGNITY_LABELS.neutral;
                return (
                  <tr key={effect.sign} className="border-b border-cosmic-border/50 last:border-0 align-middle">
                    <td className="px-2 py-1.5 font-medium text-cosmic-text">
                      <span className="mr-1">{effect.emoji}</span>
                      {language === 'hi' ? effect.sign_hindi : effect.sign.charAt(0).toUpperCase() + effect.sign.slice(1)}
                    </td>
                    <td className="px-2 py-1.5 text-cosmic-text-secondary">
                      {language === 'hi' ? effect.ruling_planet_hindi : effect.ruling_planet}
                    </td>
                    <td className="px-2 py-1.5 text-cosmic-text">
                      {language === 'hi' ? effect.ruler_current_sign_hindi : effect.ruler_current_sign}
                    </td>
                    <td className="px-2 py-1.5 text-cosmic-text-secondary text-xs">
                      {language === 'hi' ? dignityInfo.hi : dignityInfo.en}
                    </td>
                    <td className="px-2 py-1.5">
                      <span className={`text-[10px] px-1.5 py-0.5 rounded ${strengthInfo.bg} ${strengthInfo.color} font-medium`}>
                        {language === 'hi' ? strengthInfo.hi : strengthInfo.en}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
