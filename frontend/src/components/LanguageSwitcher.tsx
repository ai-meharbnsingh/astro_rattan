import { useTranslation } from '@/lib/i18n';
import { Globe } from 'lucide-react';

export default function LanguageSwitcher() {
  const { language, setLanguage } = useTranslation();

  return (
    <button
      onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
      className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-200 bg-sacred-gold/10 border border-sacred-gold/20 text-sacred-brown hover:bg-sacred-gold/20 hover:border-sacred-gold/40"
      title={language === 'en' ? 'Switch to Hindi' : 'Switch to English'}
    >
      <Globe className="w-4 h-4 text-sacred-gold" />
      <span>{language === 'en' ? 'हिन्दी' : 'EN'}</span>
    </button>
  );
}
