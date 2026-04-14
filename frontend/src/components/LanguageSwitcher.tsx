import { useTranslation } from '@/lib/i18n';

export default function LanguageSwitcher() {
  const { language, setLanguage, t } = useTranslation();

  return (
    <button
      onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
      className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-sacred-gold hover:border-sacred-gold bg-cosmic-card text-sm font-medium transition-colors"
      title={language === 'en' ? t('language.switchToHindi') : t('language.switchToEnglish')}
    >
      <span className={language === 'en' ? 'text-sacred-gold' : 'text-cosmic-text-secondary'}>EN</span>
      <span className="text-cosmic-text">/</span>
      <span className={t('auto.textCosmicTextSecond')}>हिं</span>
    </button>
  );
}
