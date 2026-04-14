import { Sparkles } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import NumerologyTabs from '@/components/numerology/NumerologyTabs';

export default function NumerologyTarot() {
  const { t } = useTranslation();

  return (
    <section className="max-w-4xl mx-auto py-24 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold-dark text-white text-sm font-medium mb-4">
          <Sparkles className="w-4 h-4" />{t('numerology.badge')}
        </div>
        <h2 className="text-3xl sm:text-4xl font-sans font-bold text-cosmic-text mb-2">
          {t('numerology.heading')}<span className="text-gradient-indigo"> {t('numerology.headingHighlight')}</span>
        </h2>
        <p className="text-cosmic-text-secondary">{t('numerology.subtitle')}</p>
      </div>

      <NumerologyTabs />
    </section>
  );
}
