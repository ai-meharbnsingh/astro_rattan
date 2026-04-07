import { useTranslation } from '@/lib/i18n';

export default function LanguageSwitcher() {
  const { language, setLanguage } = useTranslation();

  return (
    <button
      onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
      className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-sacred-gold/30 hover:border-sacred-gold/60 bg-cosmic-card/50 text-sm font-medium transition-colors"
      title={language === 'en' ? 'हिंदी में बदलें' : 'Switch to English'}
    >
      <span className={language === 'en' ? 'text-sacred-gold' : 'text-cosmic-text-secondary'}>EN</span>
      <span className="text-cosmic-text-muted">/</span>
      <span className={language === 'hi' ? 'text-sacred-gold' : 'text-cosmic-text-secondary'}>हिं</span>
    </button>
  );
}
