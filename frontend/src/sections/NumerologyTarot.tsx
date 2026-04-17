import { Sparkles } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import NumerologyTabs from '@/components/numerology/NumerologyTabs';
import { Heading } from '@/components/ui/heading';

export default function NumerologyTarot() {
  const { t } = useTranslation();

  return (
    <section className="max-w-7xl mx-auto py-24 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold-dark text-white text-sm font-medium mb-4">
          <Sparkles className="w-4 h-4" />{t('numerology.badge')}
        </div>
        <Heading as={1} variant={1} className="mb-2">
          {t('numerology.heading')}<span className="text-gradient-indigo"> {t('numerology.headingHighlight')}</span>
        </Heading>
        <p className="text-muted-foreground">{t('numerology.subtitle')}</p>
      </div>

      <NumerologyTabs />
    </section>
  );
}
