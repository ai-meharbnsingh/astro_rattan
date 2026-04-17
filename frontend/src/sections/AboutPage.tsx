import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';

export default function AboutPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background pt-28 pb-16 px-4">
      <div className="max-w-5xl mx-auto space-y-10">
        <div className="text-center space-y-3">
          <Heading as={1} variant={1} className="text-sacred-gold">
            {t('about.title')}
          </Heading>
          <p className="text-foreground/80 max-w-2xl mx-auto">
            {t('about.subtitle')}
          </p>
        </div>

        <div className="rounded-2xl border border-sacred-gold/20 bg-sacred-gold/5 p-6 md:p-8 space-y-4">
          <Heading as={3} variant={3} className="text-sacred-gold-dark">
            {t('about.heading')}
          </Heading>
          <p className="text-sm md:text-base text-foreground/80 leading-relaxed">
            {t('about.p1')}
          </p>
          <p className="text-sm md:text-base text-foreground/80 leading-relaxed">
            {t('about.p2')}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            {
              title: t('about.card.reliable.title'),
              body: t('about.card.reliable.body'),
            },
            {
              title: t('about.card.bilingual.title'),
              body: t('about.card.bilingual.body'),
            },
            {
              title: t('about.card.remedies.title'),
              body: t('about.card.remedies.body'),
            },
          ].map((c) => (
            <div key={c.title} className="rounded-2xl border border-border bg-card p-5">
              <div className="font-semibold text-foreground">{c.title}</div>
              <div className="text-sm text-foreground/70 mt-2 leading-relaxed">{c.body}</div>
            </div>
          ))}
        </div>

        <div className="flex items-center justify-center">
          <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold text-background hover:bg-sacred-gold/90">
            {t('about.learnMore')}
          </Button>
        </div>
      </div>
    </div>
  );
}
