import { Loader2, Sparkles } from 'lucide-react';

interface IogitaTabProps {
  iogitaData: any;
  loadingIogita: boolean;
  language: string;
  t: (key: string) => string;
}

export default function IogitaTab({ iogitaData, loadingIogita, language, t }: IogitaTabProps) {
  if (loadingIogita) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.analyzingLifePath')}</span></div>
    );
  }

  if (iogitaData?.basin) {
    return (
      <div className="space-y-6">
        {/* Overall Summary Card */}
        <div className="rounded-2xl p-6 border border-sacred-gold" style={{ background: 'linear-gradient(135deg, rgba(255,153,51,0.06) 0%, rgba(248,250,252,1) 100%)' }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-sacred-gold flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-sacred-gold" />
            </div>
            <div>
              <h4 className="font-display font-bold text-xl" style={{ color: 'var(--aged-gold)' }}>{t('iogita.yourLifePattern')}: {iogitaData.basin.name}</h4>
              <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{t('iogita.basedOnPositions')}</p>
            </div>
          </div>
          <p className="text-sm leading-relaxed mb-4" style={{ color: 'var(--ink)' }}>{iogitaData.basin.description}</p>
        </div>

        {/* Strengths — Top Forces */}
        <div className="rounded-xl p-5 border border-sacred-gold bg-sacred-cream">
          <h4 className="font-display font-semibold mb-4" style={{ color: 'var(--aged-gold-dim)' }}>{t('iogita.strongestQualities')}</h4>
          <div className="space-y-3">
            {(iogitaData.basin.top_3_atoms || []).map(([name, val]: [string, number], idx: number) => {
              const labelsEn: Record<string, string> = {
                DHARMA: 'Righteousness & Duty', SATYA: 'Truth & Honesty', TYAGA: 'Selflessness',
                AHANKAR: 'Self-Confidence', ATMA: 'Inner Awareness', MOKSHA: 'Spiritual Liberation',
                KULA: 'Family & Tradition', RAJYA: 'Leadership & Authority', NYAYA: 'Justice & Fairness',
                KRODHA: 'Drive & Determination', NITI: 'Strategy & Wisdom', SHAKTI: 'Power & Energy',
                BHAKTI: 'Devotion & Faith', KAAM: 'Desire & Passion', LOBH: 'Ambition', MOH: 'Attachment & Love',
              };
              const labelsHi: Record<string, string> = {
                DHARMA: 'धर्म और कर्तव्य', SATYA: 'सत्य और ईमानदारी', TYAGA: 'निःस्वार्थता',
                AHANKAR: 'आत्मविश्वास', ATMA: 'आंतरिक जागरूकता', MOKSHA: 'आध्यात्मिक मुक्ति',
                KULA: 'परिवार और परंपरा', RAJYA: 'नेतृत्व और अधिकार', NYAYA: 'न्याय और निष्पक्षता',
                KRODHA: 'दृढ़ संकल्प', NITI: 'रणनीति और बुद्धि', SHAKTI: 'शक्ति और ऊर्जा',
                BHAKTI: 'भक्ति और श्रद्धा', KAAM: 'इच्छा और जुनून', LOBH: 'महत्वाकांक्षा', MOH: 'लगाव और प्रेम',
              };
              const labels = language === 'hi' ? labelsHi : labelsEn;
              const colors = ['var(--aged-gold)', 'var(--aged-gold-light)', 'var(--aged-gold-dim)'];
              return (
                <div key={name} className="flex items-center gap-3">
                  <span className="text-lg font-bold w-6" style={{ color: colors[idx] }}>{idx + 1}</span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold" style={{ color: 'var(--ink)' }}>{labels[name] || name}</span>
                      <span className="text-xs" style={{ color: 'var(--ink-light)' }}>{Math.round(Math.abs(val) * 100)}%</span>
                    </div>
                    <div className="h-2 rounded-full overflow-hidden" style={{ background: 'rgba(184,134,11,0.15)' }}>
                      <div className="h-full rounded-full" style={{ width: `${Math.abs(val) * 100}%`, background: colors[idx] }} />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Area to Improve */}
        {iogitaData.basin.top_negative && (
          <div className="rounded-xl p-5 border border-red-200 bg-red-50">
            <h4 className="font-display font-semibold mb-2 text-red-700">{t('iogita.areaNeedsAttention')}</h4>
            {(() => {
              const negLabelsEn: Record<string, string> = {
                DHARMA: 'Following your duty', SATYA: 'Being truthful', TYAGA: 'Letting go of attachments',
                KRODHA: 'Managing anger', LOBH: 'Controlling greed', MOH: 'Detaching from illusions',
                KAAM: 'Moderating desires', AHANKAR: 'Ego management',
                BHAKTI: 'Developing devotion', SHAKTI: 'Building inner strength',
                MOKSHA: 'Spiritual growth', ATMA: 'Self-awareness',
              };
              const negLabelsHi: Record<string, string> = {
                DHARMA: 'अपने कर्तव्य का पालन', SATYA: 'सत्यनिष्ठा', TYAGA: 'आसक्तियों को छोड़ना',
                KRODHA: 'क्रोध प्रबंधन', LOBH: 'लोभ पर नियंत्रण', MOH: 'भ्रम से मुक्ति',
                KAAM: 'इच्छाओं पर संयम', AHANKAR: 'अहंकार प्रबंधन',
                BHAKTI: 'भक्ति का विकास', SHAKTI: 'आंतरिक शक्ति का निर्माण',
                MOKSHA: 'आध्यात्मिक विकास', ATMA: 'आत्म-जागरूकता',
              };
              const negLabels = language === 'hi' ? negLabelsHi : negLabelsEn;
              const name = iogitaData.basin.top_negative[0];
              const suppressedMsg = language === 'hi'
                ? `${negLabels[name] || name} — यह क्षेत्र आपकी कुंडली में दबा हुआ है। संतुलित जीवन के लिए इसे विकसित करें।`
                : `${negLabels[name] || name} — this area is suppressed in your chart. Focus on developing it for a more balanced life.`;
              return <p className="text-sm text-red-600">{suppressedMsg}</p>;
            })()}
          </div>
        )}

        {/* Guidance Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="rounded-xl p-5 border border-amber-200 bg-amber-50">
            <h4 className="font-display font-semibold mb-2 text-amber-700">{t('iogita.beMindfulOf')}</h4>
            <p className="text-sm leading-relaxed text-amber-600">{iogitaData.basin.warning}</p>
          </div>
          <div className="rounded-xl p-5 border border-emerald-200 bg-emerald-50">
            <h4 className="font-display font-semibold mb-2 text-emerald-700">{t('iogita.pathToGrowth')}</h4>
            <p className="text-sm leading-relaxed text-emerald-600">{iogitaData.basin.escape_trigger}</p>
          </div>
        </div>

        {/* Overall Insight */}
        {iogitaData.iogita_insight && (
          <div className="rounded-xl p-5 border border-sacred-gold bg-sacred-cream">
            <h4 className="font-display font-semibold mb-3" style={{ color: 'var(--aged-gold-dim)' }}>{t('iogita.overallLifeReading')}</h4>
            <p className="text-sm leading-relaxed" style={{ color: 'var(--ink)' }}>{iogitaData.iogita_insight}</p>
          </div>
        )}

        {/* Normal Astrology Insights */}
        {iogitaData.normal_astrology && iogitaData.normal_astrology.length > 0 && (
          <div className="rounded-xl p-5 border border-sacred-gold bg-sacred-cream">
            <h4 className="font-display font-semibold mb-3" style={{ color: 'var(--aged-gold-dim)' }}>{t('iogita.kundliSummary')}</h4>
            <div className="space-y-2">
              {iogitaData.normal_astrology.map((point: string, idx: number) => (
                <div key={idx} className="flex gap-2 text-sm" style={{ color: 'var(--ink)' }}>
                  <span style={{ color: 'var(--aged-gold)' }}>•</span>
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
    return <p className="text-center py-8" style={{ color: 'var(--ink-light)' }}>{t('iogita.partialData')}</p>;
  }

  return <p className="text-center py-8" style={{ color: 'var(--ink-light)' }}>{t('iogita.clickTab')}</p>;
}
