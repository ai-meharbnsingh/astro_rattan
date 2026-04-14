import { Heart, Briefcase, Activity, Wallet, Sparkles } from 'lucide-react';

interface SignMeta {
  sign: string;
  sign_hindi: string;
  emoji: string;
  dates: string;
  ruling_planet: string;
  ruling_planet_hindi: string;
  element: string;
  element_hindi: string;
}

interface DailyData extends SignMeta {
  period: string;
  date: string;
  sections: Record<string, string>;
  source: string;
}

interface Props {
  data: DailyData | null;
  loading: boolean;
  language: string;
  t: (key: string) => string;
}

const SECTION_CONFIG = [
  { key: 'general', icon: Sparkles, color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200' },
  { key: 'love', icon: Heart, color: 'text-pink-600', bg: 'bg-pink-50', border: 'border-pink-200' },
  { key: 'career', icon: Briefcase, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200' },
  { key: 'health', icon: Activity, color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200' },
  { key: 'finance', icon: Wallet, color: 'text-purple-600', bg: 'bg-purple-50', border: 'border-purple-200' },
];

const SECTION_LABELS: Record<string, { en: string; hi: string }> = {
  general: { en: 'General', hi: 'सामान्य' },
  love: { en: 'Love & Relationships', hi: 'प्रेम एवं संबंध' },
  career: { en: 'Career & Work', hi: 'करियर एवं कार्य' },
  health: { en: 'Health & Wellness', hi: 'स्वास्थ्य' },
  finance: { en: 'Finance & Wealth', hi: 'धन एवं वित्त' },
};

export default function DailyTab({ data, loading, language, t }: Props) {
  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3, 4, 5].map(i => (
          <div key={i} className="h-24 animate-pulse bg-gray-200 rounded-xl" />
        ))}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-cosmic-text-secondary">
        {t('auto.selectASignToViewYou')}
      </div>
    );
  }

  const sections = SECTION_CONFIG.filter(({ key }) => data.sections?.[key]);

  return (
    <div className="space-y-3">
      {/* Sign Header Card */}
      <div className="rounded-xl border border-cosmic-border bg-cosmic-card p-4">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl">{data.emoji}</span>
          <div>
            <h3 className="text-lg font-semibold text-cosmic-text">
              {language === 'hi' ? data.sign_hindi : data.sign.charAt(0).toUpperCase() + data.sign.slice(1)}
            </h3>
            <p className="text-xs text-cosmic-text-secondary">{data.dates}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2 mt-2">
          <div className="rounded-lg bg-sacred-gold/10 px-3 py-1.5">
            <span className="text-xs text-cosmic-text-secondary">{t('auto.rulingPlanet')}</span>
            <p className="text-sm font-medium text-cosmic-text">{language === 'hi' ? data.ruling_planet_hindi : data.ruling_planet}</p>
          </div>
          <div className="rounded-lg bg-sacred-gold/10 px-3 py-1.5">
            <span className="text-xs text-cosmic-text-secondary">{t('auto.element')}</span>
            <p className="text-sm font-medium text-cosmic-text">{language === 'hi' ? data.element_hindi : data.element.charAt(0).toUpperCase() + data.element.slice(1)}</p>
          </div>
        </div>
      </div>

      {/* Section Cards — column grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {sections.map(({ key, icon: Icon, color, bg, border }) => {
          const text = data.sections[key];
          const label = SECTION_LABELS[key] || { en: key, hi: key };
          return (
            <div key={key} className={`rounded-xl border ${border} ${bg} p-4`}>
              <div className="flex items-center gap-2 mb-2">
                <Icon className={`w-4 h-4 ${color}`} />
                <h4 className={`text-sm font-semibold ${color}`}>
                  {language === 'hi' ? label.hi : label.en}
                </h4>
              </div>
              <p className="text-sm text-gray-700 leading-relaxed">{text}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
