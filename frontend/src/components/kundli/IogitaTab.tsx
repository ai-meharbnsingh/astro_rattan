import { Loader2, Sparkles, TrendingUp, AlertTriangle, Eye, Flame, BookOpen, Star } from 'lucide-react';
import { Heading } from '@/components/ui/heading';

interface IogitaTabProps {
  iogitaData: any;
  loadingIogita: boolean;
  language: string;
  t: (key: string) => string;
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';

const LABELS_EN: Record<string, string> = {
  DHARMA: 'Righteousness & Duty', SATYA: 'Truth & Honesty', TYAGA: 'Selflessness',
  AHANKAR: 'Self-Confidence', ATMA: 'Inner Awareness', MOKSHA: 'Spiritual Liberation',
  KULA: 'Family & Tradition', RAJYA: 'Leadership & Authority', NYAYA: 'Justice & Fairness',
  KRODHA: 'Drive & Determination', NITI: 'Strategy & Wisdom', SHAKTI: 'Power & Energy',
  BHAKTI: 'Devotion & Faith', KAAM: 'Desire & Passion', LOBH: 'Ambition', MOH: 'Attachment & Love',
};
const LABELS_HI: Record<string, string> = {
  DHARMA: 'धर्म और कर्तव्य', SATYA: 'सत्य और ईमानदारी', TYAGA: 'निःस्वार्थता',
  AHANKAR: 'आत्मविश्वास', ATMA: 'आंतरिक जागरूकता', MOKSHA: 'आध्यात्मिक मुक्ति',
  KULA: 'परिवार और परंपरा', RAJYA: 'नेतृत्व और अधिकार', NYAYA: 'न्याय और निष्पक्षता',
  KRODHA: 'दृढ़ संकल्प', NITI: 'रणनीति और बुद्धि', SHAKTI: 'शक्ति और ऊर्जा',
  BHAKTI: 'भक्ति और श्रद्धा', KAAM: 'इच्छा और जुनून', LOBH: 'महत्वाकांक्षा', MOH: 'लगाव और प्रेम',
};
const NEG_LABELS_EN: Record<string, string> = {
  DHARMA: 'Following your duty', SATYA: 'Being truthful', TYAGA: 'Letting go of attachments',
  KRODHA: 'Managing anger', LOBH: 'Controlling greed', MOH: 'Detaching from illusions',
  KAAM: 'Moderating desires', AHANKAR: 'Ego management', BHAKTI: 'Developing devotion',
  SHAKTI: 'Building inner strength', MOKSHA: 'Spiritual growth', ATMA: 'Self-awareness',
};
const NEG_LABELS_HI: Record<string, string> = {
  DHARMA: 'अपने कर्तव्य का पालन', SATYA: 'सत्यनिष्ठा', TYAGA: 'आसक्तियों को छोड़ना',
  KRODHA: 'क्रोध प्रबंधन', LOBH: 'लोभ पर नियंत्रण', MOH: 'भ्रम से मुक्ति',
  KAAM: 'इच्छाओं पर संयम', AHANKAR: 'अहंकार प्रबंधन', BHAKTI: 'भक्ति का विकास',
  SHAKTI: 'आंतरिक शक्ति का निर्माण', MOKSHA: 'आध्यात्मिक विकास', ATMA: 'आत्म-जागरूकता',
};

const BAR_COLORS = ['#b8860b', '#d4a017', '#c8982a'];

export default function IogitaTab({ iogitaData, loadingIogita, language, t }: IogitaTabProps) {
  const isHi = language === 'hi';

  if (loadingIogita) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.analyzingLifePath')}</span>
      </div>
    );
  }

  if (iogitaData?.basin) {
    const basin   = iogitaData.basin;
    const labels  = isHi ? LABELS_HI  : LABELS_EN;
    const negLbls = isHi ? NEG_LABELS_HI : NEG_LABELS_EN;

    return (
      <div className="space-y-4">

        {/* Header */}
        <div>
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
            <Sparkles className="w-6 h-6" />
            {isHi ? 'io-gita जीवन पाठ' : 'io-gita Life Reading'}
          </Heading>
          <p className="text-sm text-muted-foreground">
            {isHi ? 'आत्मिक पैटर्न · शक्तियाँ · मार्गदर्शन' : 'Soul Pattern · Strengths · Guidance'}
          </p>
        </div>

        {/* 1 — Life Pattern Summary */}
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Star className="w-4 h-4" />
            <span>{t('iogita.yourLifePattern')}</span>
            {basin.name && (
              <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">{basin.name}</span>
            )}
          </div>
          <div className="px-4 py-3">
            <p className="text-sm leading-relaxed text-foreground">{basin.description}</p>
          </div>
        </div>

        {/* 2 — Strongest Qualities */}
        {(basin.top_3_atoms || []).length > 0 && (
          <div className={ohContainer}>
            <div className={ohHeader}>
              <TrendingUp className="w-4 h-4" />
              <span>{t('iogita.strongestQualities')}</span>
            </div>
            <div className="px-4 py-3 space-y-3">
              {(basin.top_3_atoms as [string, number][]).map(([name, val], idx) => (
                <div key={name} className="flex items-center gap-3">
                  <span className="text-base font-bold w-5 shrink-0" style={{ color: BAR_COLORS[idx] }}>{idx + 1}</span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold text-foreground">{labels[name] || name}</span>
                      <span className="text-xs text-muted-foreground">{Math.round(Math.abs(val) * 100)}%</span>
                    </div>
                    <div className="h-2 rounded-full overflow-hidden bg-sacred-gold/15">
                      <div
                        className="h-full rounded-full transition-all"
                        style={{ width: `${Math.abs(val) * 100}%`, background: BAR_COLORS[idx] }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 3 — Area Needing Attention */}
        {basin.top_negative && (
          <div className={ohContainer}>
            <div className="bg-red-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              <span>{t('iogita.areaNeedsAttention')}</span>
              {basin.top_negative[0] && (
                <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">
                  {labels[basin.top_negative[0]] || basin.top_negative[0]}
                </span>
              )}
            </div>
            <div className="px-4 py-3">
              <p className="text-sm text-red-700 leading-relaxed">
                {negLbls[basin.top_negative[0]]
                  ? (isHi ? `${negLbls[basin.top_negative[0]]} पर ध्यान देने की आवश्यकता है।` : `Focus area: ${negLbls[basin.top_negative[0]]}.`)
                  : basin.top_negative[0]}
              </p>
            </div>
          </div>
        )}

        {/* 4 — Guidance (Warning + Growth path) */}
        {(basin.warning || basin.escape_trigger) && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {basin.warning && (
              <div className={ohContainer}>
                <div className="bg-amber-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
                  <Eye className="w-4 h-4" />
                  <span>{t('iogita.beMindfulOf')}</span>
                </div>
                <div className="px-4 py-3">
                  <p className="text-sm leading-relaxed text-foreground">{basin.warning}</p>
                </div>
              </div>
            )}
            {basin.escape_trigger && (
              <div className={ohContainer}>
                <div className="bg-emerald-700 text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
                  <Flame className="w-4 h-4" />
                  <span>{t('iogita.pathToGrowth')}</span>
                </div>
                <div className="px-4 py-3">
                  <p className="text-sm leading-relaxed text-foreground">{basin.escape_trigger}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* 5 — Overall Life Reading */}
        {iogitaData.iogita_insight && (
          <div className={ohContainer}>
            <div className={ohHeader}>
              <Sparkles className="w-4 h-4" />
              <span>{t('iogita.overallLifeReading')}</span>
            </div>
            <div className="px-4 py-3">
              <p className="text-sm leading-relaxed text-foreground">{iogitaData.iogita_insight}</p>
            </div>
          </div>
        )}

        {/* 6 — Kundli Summary */}
        {iogitaData.normal_astrology?.length > 0 && (
          <div className={ohContainer}>
            <div className={ohHeader}>
              <BookOpen className="w-4 h-4" />
              <span>{t('iogita.kundliSummary')}</span>
              <span className="ml-auto text-[12px] font-normal opacity-80">{iogitaData.normal_astrology.length}</span>
            </div>
            <div className="px-4 py-3 space-y-1.5">
              {(iogitaData.normal_astrology as string[]).map((point, idx) => (
                <div key={idx} className="flex gap-2 text-sm text-foreground">
                  <span className="text-sacred-gold-dark shrink-0 mt-0.5">•</span>
                  <span className="leading-relaxed">{point}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  if (iogitaData) {
    return <p className="text-center py-8 text-muted-foreground">{t('iogita.partialData')}</p>;
  }

  return <p className="text-center py-8 text-muted-foreground">{t('iogita.clickTab')}</p>;
}
