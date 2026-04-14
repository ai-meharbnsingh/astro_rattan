import { Heart, Briefcase, Activity, Wallet, Sparkles, CalendarDays } from 'lucide-react';

interface WeeklyData {
  sign: string;
  sign_hindi: string;
  emoji: string;
  dates: string;
  ruling_planet: string;
  ruling_planet_hindi: string;
  element: string;
  element_hindi: string;
  period: string;
  week_start: string;
  week_end: string;
  sections: Record<string, string>;
  source: string;
}

interface Props {
  data: WeeklyData | null;
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
  general: { en: 'General Outlook', hi: 'सामान्य दृष्टिकोण' },
  love: { en: 'Love & Relationships', hi: 'प्रेम एवं संबंध' },
  career: { en: 'Career & Work', hi: 'करियर एवं कार्य' },
  health: { en: 'Health & Wellness', hi: 'स्वास्थ्य' },
  finance: { en: 'Finance & Wealth', hi: 'धन एवं वित्त' },
};

function formatDate(dateStr: string, _lang: string): string {
  if (!dateStr) return '';
  const d = new Date(dateStr + 'T12:00:00');
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
}

export default function WeeklyTab({ data, loading, language, t }: Props) {
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
        {t('auto.selectASignToViewWee')}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Week Header */}
      <div className="rounded-xl border border-cosmic-border bg-cosmic-card p-4">
        <div className="flex items-center gap-3 mb-2">
          <img
            src={`/images/zodiac-purple/zodiac-${data.sign}.png`}
            alt={data.sign}
            className="w-14 h-14 object-contain rounded-lg"
          />
          <div>
            <h3 className="text-lg font-semibold text-cosmic-text">
              {language === 'hi' ? data.sign_hindi : data.sign.charAt(0).toUpperCase() + data.sign.slice(1)}
              <span className="text-sm font-normal text-cosmic-text-secondary ml-2">
                {t('auto.weeklyHoroscope')}
              </span>
            </h3>
            <div className="flex items-center gap-1.5 text-xs text-cosmic-text-secondary mt-0.5">
              <CalendarDays className="w-3.5 h-3.5" />
              <span>{formatDate(data.week_start, language)} — {formatDate(data.week_end, language)}</span>
            </div>
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
        {SECTION_CONFIG.map(({ key, icon: Icon, color, bg, border }) => {
          const text = data.sections?.[key];
          if (!text) return null;
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
