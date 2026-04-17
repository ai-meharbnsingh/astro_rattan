import { Heart, Briefcase, Activity, Wallet, Sparkles, CalendarDays, Calendar } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";
import ScoreBar from './ScoreBar';
import LuckyMetadataCard from './LuckyMetadataCard';
import DosAndDonts from './DosAndDonts';

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

interface MonthlyData extends SignMeta {
  period: string;
  month_start: string;
  sections: Record<string, string>;
  source: string;
  scores?: { overall: number; love: number; career: number; finance: number; health: number };
  mood?: { en: string; hi: string };
  lucky?: { number: number; color: { en: string; hi: string }; time: { en: string; hi: string }; compatible_sign: { en: string; hi: string }; gemstone: { en: string; hi: string }; mantra: string };
  dos?: Array<{ en: string; hi: string }>;
  donts?: Array<{ en: string; hi: string }>;
  phases?: Array<{ range: string; summary: { en: string; hi: string }; score: number }>;
  key_dates?: Array<{ date: string; event: { en: string; hi: string } }>;
}

interface Props {
  data: MonthlyData | null;
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

function formatMonthStart(dateStr: string): string {
  if (!dateStr) return '';
  const d = new Date(dateStr + 'T12:00:00');
  return d.toLocaleDateString('en-IN', { month: 'long', year: 'numeric' });
}

function txt(v: unknown, lang: string): string {
  if (typeof v === 'string') return v;
  if (v && typeof v === 'object' && 'en' in v) return (lang === 'hi' ? (v as any).hi : (v as any).en) || '';
  return String(v ?? '');
}

export default function MonthlyTab({ data, loading, language, t }: Props) {
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
      <div className="text-center py-12 text-muted-foreground">
        {t('auto.selectSignMonthly')}
      </div>
    );
  }

  const sections = SECTION_CONFIG.filter(({ key }) => data.sections?.[key]);

  return (
    <div className="space-y-3">
      {/* Sign Header Card */}
      <Card className="py-4">
        <CardContent className="p-4">
          <div className="flex items-center gap-3 mb-2">
            <img
              src={`/images/zodiac-orange/zodiac-${data.sign}-orange.png`}
              alt={data.sign}
              className="w-14 h-14 object-contain rounded-lg"
            />
            <div>
              <Heading as={3} variant={3}>
                {language === 'hi' ? data.sign_hindi : data.sign.charAt(0).toUpperCase() + data.sign.slice(1)}
                <Text variant="muted" as="span">
                  {t('auto.monthlyHoroscope')}
                </Text>
              </Heading>
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground mt-0.5">
                <CalendarDays className="w-3.5 h-3.5" />
                <span>{formatMonthStart(data.month_start)}</span>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-2">
            <div className="rounded-lg bg-sacred-gold/10 px-3 py-1.5">
              <Text variant="small" as="span">{t('auto.rulingPlanet')}</Text>
              <p className="text-sm font-medium text-foreground">{language === 'hi' ? data.ruling_planet_hindi : data.ruling_planet}</p>
            </div>
            <div className="rounded-lg bg-sacred-gold/10 px-3 py-1.5">
              <Text variant="small" as="span">{t('auto.element')}</Text>
              <p className="text-sm font-medium text-foreground">{language === 'hi' ? data.element_hindi : data.element.charAt(0).toUpperCase() + data.element.slice(1)}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Score Bars */}
      {data.scores && (
        <Card className="py-4">
          <CardContent className="p-4 space-y-2.5">
            <ScoreBar label={t('auto.overallScore')} score={data.scores.overall} color="amber" />
            <ScoreBar label={t('horoscope.score.love')} score={data.scores.love} color="pink" />
            <ScoreBar label={t('horoscope.score.career')} score={data.scores.career} color="blue" />
            <ScoreBar label={t('horoscope.score.finance')} score={data.scores.finance} color="purple" />
            <ScoreBar label={t('horoscope.score.health')} score={data.scores.health} color="green" />
          </CardContent>
        </Card>
      )}

      {/* Mood */}
      {data.mood && (
        <div className="rounded-xl border bg-card px-4 py-2.5 flex items-center gap-2">
          <Text variant="small" as="span">{t('auto.mood')}:</Text>
          <span className="text-sm font-medium text-foreground">{language === 'hi' ? data.mood.hi : data.mood.en}</span>
        </div>
      )}

      {/* Lucky Metadata */}
      {data.lucky && (
        <LuckyMetadataCard lucky={data.lucky} language={language} t={t} />
      )}

      {/* Section Cards — column grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {sections.map(({ key, icon: Icon, color, bg, border }) => {
          const text = data.sections[key];
          const sectionKey = key === 'general' ? 'generalOutlook' : key;
          return (
            <div key={key} className={`rounded-xl border ${border} ${bg} p-4`}>
              <div className="flex items-center gap-2 mb-2">
                <Icon className={`w-4 h-4 ${color}`} />
                <h4 className={`text-sm font-semibold ${color}`}>
                  {t('horoscope.section.' + sectionKey)}
                </h4>
              </div>
              <p className="text-sm text-foreground leading-relaxed">{txt(text, language)}</p>
            </div>
          );
        })}
      </div>

      {/* Phase Breakdown */}
      {data.phases && data.phases.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-foreground mb-2">{t('auto.phases')}</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {data.phases.map((phase, i) => (
              <div key={i} className="rounded-xl border border-border bg-card p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-muted-foreground">{phase.range}</span>
                  <span className="rounded-full bg-sacred-gold/20 text-sacred-gold-dark px-2 py-0.5 text-xs font-semibold">
                    {phase.score}/10
                  </span>
                </div>
                <p className="text-sm text-foreground leading-relaxed">
                  {language === 'hi' ? phase.summary.hi : phase.summary.en}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Dates */}
      {data.key_dates && data.key_dates.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-foreground mb-2">{t('auto.keyDates')}</h3>
          <div className="rounded-xl border border-border bg-card divide-y divide-border">
            {data.key_dates.map((kd, i) => (
              <div key={i} className="flex items-start gap-3 px-4 py-3">
                <div className="flex items-center gap-1.5 shrink-0 mt-0.5">
                  <Calendar className="w-3.5 h-3.5 text-sacred-gold-dark" />
                  <span className="text-xs font-semibold text-sacred-gold-dark whitespace-nowrap">{kd.date}</span>
                </div>
                <p className="text-sm text-foreground">
                  {language === 'hi' ? kd.event.hi : kd.event.en}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Dos and Donts */}
      {data.dos && data.donts && data.dos.length > 0 && data.donts.length > 0 && (
        <DosAndDonts dos={data.dos} donts={data.donts} language={language} t={t} />
      )}
    </div>
  );
}
