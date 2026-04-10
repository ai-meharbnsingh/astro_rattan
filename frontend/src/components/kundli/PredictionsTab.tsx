import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sparkles, Loader2, Calendar, CalendarDays, CalendarRange } from 'lucide-react';
import { isPuterAvailable } from '@/lib/puter-ai';
import { useTranslation } from '@/lib/i18n';

// Simple markdown-to-JSX renderer for prediction text
function renderMarkdown(text: string) {
  return text.split('\n').filter(l => l.trim()).map((line, idx) => {
    // Bold: **text**
    const parts = line.split(/\*\*(.*?)\*\*/g);
    const rendered = parts.map((part, i) =>
      i % 2 === 1 ? <strong key={i} style={{ color: 'var(--aged-gold)' }}>{part}</strong> : part
    );

    // Heading lines
    if (line.startsWith('## ')) {
      return <h3 key={idx} className="font-display font-bold text-lg mt-4 mb-2" style={{ color: '#3D2B1F' }}>{rendered}</h3>;
    }
    // List items
    if (line.trimStart().startsWith('- ')) {
      return (
        <div key={idx} className="flex gap-2 mb-1.5 ml-2" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)', color: 'var(--ink)' }}>
          <span className="text-sacred-gold mt-0.5">•</span>
          <span className="leading-relaxed">{rendered}</span>
        </div>
      );
    }
    // Regular paragraph
    return <p key={idx} className="mb-3 leading-relaxed" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)', color: 'var(--ink)' }}>{rendered}</p>;
  });
}

type PredictionPeriod = 'general' | 'daily' | 'monthly' | 'yearly';

interface PredictionsTabProps {
  predictionsData: Record<string, any>;
  loadingPredictions: boolean;
  activePeriod: PredictionPeriod;
  onFetchPredictions: (period: PredictionPeriod) => void;
}

const PERIOD_TABS_EN: { key: PredictionPeriod; label: string; icon: typeof Sparkles; description: string }[] = [
  { key: 'general', label: 'General', icon: Sparkles, description: 'Full birth chart analysis' },
  { key: 'daily', label: 'Daily', icon: Calendar, description: "Today's prediction" },
  { key: 'monthly', label: 'Monthly', icon: CalendarDays, description: "This month's forecast" },
  { key: 'yearly', label: 'Yearly', icon: CalendarRange, description: "This year's outlook" },
];

const PERIOD_TABS_HI: { key: PredictionPeriod; label: string; icon: typeof Sparkles; description: string }[] = [
  { key: 'general', label: 'सामान्य', icon: Sparkles, description: 'पूर्ण जन्म कुंडली विश्लेषण' },
  { key: 'daily', label: 'दैनिक', icon: Calendar, description: 'आज का फल' },
  { key: 'monthly', label: 'मासिक', icon: CalendarDays, description: 'इस माह का फल' },
  { key: 'yearly', label: 'वार्षिक', icon: CalendarRange, description: 'इस वर्ष का फल' },
];

export default function PredictionsTab({
  predictionsData,
  loadingPredictions,
  activePeriod,
  onFetchPredictions,
}: PredictionsTabProps) {
  const { language } = useTranslation();
  const PERIOD_TABS = language === 'hi' ? PERIOD_TABS_HI : PERIOD_TABS_EN;
  const currentData = predictionsData[activePeriod];

  return (
    <div className="space-y-4">
      {/* Period selector tabs */}
      <div className="flex gap-2 flex-wrap">
        {PERIOD_TABS.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => onFetchPredictions(key)}
            disabled={loadingPredictions}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activePeriod === key
                ? 'bg-sacred-gold-dark text-white shadow-md'
                : 'bg-sacred-cream border border-sacred-gold text-sacred-brown hover:bg-sacred-gold'
            } ${loadingPredictions ? 'opacity-75 cursor-not-allowed' : ''}`}
          >
            <Icon className="w-4 h-4" />
            {label}
            {predictionsData[key] && key !== activePeriod && (
              <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
            )}
          </button>
        ))}
      </div>

      {/* Loading state */}
      {loadingPredictions && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
          <span className="ml-2 text-cosmic-text">
            {language === 'hi'
              ? (activePeriod === 'daily' ? 'आज के सितारे पढ़ रहे हैं...' :
                 activePeriod === 'monthly' ? 'इस माह के ग्रह गोचर का विश्लेषण...' :
                 activePeriod === 'yearly' ? 'वार्षिक फल की गणना...' :
                 'सितारों से परामर्श...')
              : (activePeriod === 'daily' ? 'Reading today\'s stars...' :
                 activePeriod === 'monthly' ? 'Analyzing this month\'s transits...' :
                 activePeriod === 'yearly' ? 'Calculating yearly forecast...' :
                 'Consulting the stars...')}
          </span>
        </div>
      )}

      {/* Prediction content */}
      {!loadingPredictions && currentData && (
        <div className="rounded-xl p-6 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.25)' }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: 'rgba(184,134,11,0.15)' }}>
              <Sparkles className="w-5 h-5" style={{ color: 'var(--aged-gold-dim)' }} />
            </div>
            <div>
              <h4 className="font-display font-semibold text-xl text-sacred-brown">
                {language === 'hi'
                  ? (activePeriod === 'daily' ? 'दैनिक फल' :
                     activePeriod === 'monthly' ? 'मासिक फल' :
                     activePeriod === 'yearly' ? 'वार्षिक फल' :
                     'AI भविष्यवाणी')
                  : (activePeriod === 'daily' ? 'Daily Prediction' :
                     activePeriod === 'monthly' ? 'Monthly Prediction' :
                     activePeriod === 'yearly' ? 'Yearly Prediction' :
                     'AI Predictions')}
              </h4>
              <p className="text-sm text-cosmic-text">
                {PERIOD_TABS.find(t => t.key === activePeriod)?.description}
              </p>
            </div>
            {currentData._puterFallback && (
              <span className="ml-auto text-sm px-2 py-1 rounded-full" style={{ backgroundColor: 'rgba(184,134,11,0.12)', color: 'var(--aged-gold-dim)', border: '1px solid rgba(184,134,11,0.3)' }}>
                {language === 'hi' ? 'निःशुल्क AI द्वारा संचालित' : 'Powered by Free AI'}
              </span>
            )}
          </div>
          <div className="max-w-none" style={{ color: 'var(--ink)' }}>
            {renderMarkdown(currentData.interpretation || currentData.response || currentData.text || (language === 'hi' ? 'भविष्यवाणी तैयार हो रही है...' : 'Generating predictions...'))}
            {currentData._streaming && <span className="inline-block w-1.5 h-4 ml-0.5 bg-sacred-gold animate-pulse align-middle" />}
          </div>
        </div>
      )}

      {/* Empty state — no prediction yet for this period */}
      {!loadingPredictions && !currentData && (
        <div className="text-center py-12">
          <Sparkles className="w-10 h-10 mx-auto mb-3" style={{ color: 'rgba(184,134,11,0.4)' }} />
          <p className="text-cosmic-text mb-4">
            {language === 'hi'
              ? (activePeriod === 'daily' ? 'आज का व्यक्तिगत फल प्राप्त करें' :
                 activePeriod === 'monthly' ? 'इस माह का विस्तृत फल प्राप्त करें' :
                 activePeriod === 'yearly' ? 'अपना वार्षिक फल प्राप्त करें' :
                 'AI भविष्यवाणी प्राप्त करें')
              : (activePeriod === 'daily' ? "Get today's personalized prediction" :
                 activePeriod === 'monthly' ? "Get this month's detailed forecast" :
                 activePeriod === 'yearly' ? "Get your yearly outlook" :
                 'Get AI Predictions')}
          </p>
          <Button onClick={() => onFetchPredictions(activePeriod)} className="btn-sacred">
            <Sparkles className="w-4 h-4 mr-2" />
            {language === 'hi'
              ? (activePeriod === 'daily' ? 'आज का फल' :
                 activePeriod === 'monthly' ? 'मासिक फल' :
                 activePeriod === 'yearly' ? 'वार्षिक फल' :
                 'भविष्यवाणी प्राप्त करें')
              : (activePeriod === 'daily' ? "Today's Prediction" :
                 activePeriod === 'monthly' ? 'Monthly Forecast' :
                 activePeriod === 'yearly' ? 'Yearly Outlook' :
                 'Get Predictions')}
          </Button>
          {isPuterAvailable() && (
            <p className="text-sm mt-3" style={{ color: 'var(--ink-light)' }}>{language === 'hi' ? 'सर्वर व्यस्त होने पर निःशुल्क AI बैकअप उपलब्ध' : 'Free AI available as backup if server is busy'}</p>
          )}
        </div>
      )}
    </div>
  );
}
