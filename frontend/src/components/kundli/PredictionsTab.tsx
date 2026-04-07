import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sparkles, Loader2, Calendar, CalendarDays, CalendarRange } from 'lucide-react';
import { isPuterAvailable } from '@/lib/puter-ai';

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
        <div key={idx} className="flex gap-2 mb-1.5 ml-2" style={{ fontFamily: 'serif', color: 'var(--ink)' }}>
          <span className="text-sacred-gold mt-0.5">•</span>
          <span className="leading-relaxed">{rendered}</span>
        </div>
      );
    }
    // Regular paragraph
    return <p key={idx} className="mb-3 leading-relaxed" style={{ fontFamily: 'serif', color: 'var(--ink)' }}>{rendered}</p>;
  });
}

type PredictionPeriod = 'general' | 'daily' | 'monthly' | 'yearly';

interface PredictionsTabProps {
  predictionsData: Record<string, any>;
  loadingPredictions: boolean;
  activePeriod: PredictionPeriod;
  onFetchPredictions: (period: PredictionPeriod) => void;
}

const PERIOD_TABS: { key: PredictionPeriod; label: string; icon: typeof Sparkles; description: string }[] = [
  { key: 'general', label: 'General', icon: Sparkles, description: 'Full birth chart analysis' },
  { key: 'daily', label: 'Daily', icon: Calendar, description: "Today's prediction" },
  { key: 'monthly', label: 'Monthly', icon: CalendarDays, description: "This month's forecast" },
  { key: 'yearly', label: 'Yearly', icon: CalendarRange, description: "This year's outlook" },
];

export default function PredictionsTab({
  predictionsData,
  loadingPredictions,
  activePeriod,
  onFetchPredictions,
}: PredictionsTabProps) {
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
                : 'bg-sacred-cream border border-sacred-gold/30 text-sacred-brown hover:bg-sacred-gold/10'
            } ${loadingPredictions ? 'opacity-60 cursor-not-allowed' : ''}`}
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
          <span className="ml-2 text-sacred-text-secondary">
            {activePeriod === 'daily' ? 'Reading today\'s stars...' :
             activePeriod === 'monthly' ? 'Analyzing this month\'s transits...' :
             activePeriod === 'yearly' ? 'Calculating yearly forecast...' :
             'Consulting the stars...'}
          </span>
        </div>
      )}

      {/* Prediction content */}
      {!loadingPredictions && currentData && (
        <div className="rounded-2xl p-6 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.25)' }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: 'rgba(184,134,11,0.15)' }}>
              <Sparkles className="w-5 h-5" style={{ color: 'var(--aged-gold-dim)' }} />
            </div>
            <div>
              <h4 className="font-display font-semibold text-xl text-sacred-brown">
                {activePeriod === 'daily' ? 'Daily Prediction' :
                 activePeriod === 'monthly' ? 'Monthly Prediction' :
                 activePeriod === 'yearly' ? 'Yearly Prediction' :
                 'AI Predictions'}
              </h4>
              <p className="text-xs text-sacred-text-secondary">
                {PERIOD_TABS.find(t => t.key === activePeriod)?.description}
              </p>
            </div>
            {currentData._puterFallback && (
              <span className="ml-auto text-xs px-2 py-1 rounded-full" style={{ backgroundColor: 'rgba(184,134,11,0.12)', color: 'var(--aged-gold-dim)', border: '1px solid rgba(184,134,11,0.3)' }}>
                Powered by Free AI
              </span>
            )}
          </div>
          <div className="max-w-none" style={{ color: 'var(--ink)' }}>
            {renderMarkdown(currentData.interpretation || currentData.response || currentData.text || 'Generating predictions...')}
            {currentData._streaming && <span className="inline-block w-1.5 h-4 ml-0.5 bg-sacred-gold animate-pulse align-middle" />}
          </div>
        </div>
      )}

      {/* Empty state — no prediction yet for this period */}
      {!loadingPredictions && !currentData && (
        <div className="text-center py-12">
          <Sparkles className="w-10 h-10 mx-auto mb-3" style={{ color: 'rgba(184,134,11,0.4)' }} />
          <p className="text-sacred-text-secondary mb-4">
            {activePeriod === 'daily' ? "Get today's personalized prediction" :
             activePeriod === 'monthly' ? "Get this month's detailed forecast" :
             activePeriod === 'yearly' ? "Get your yearly outlook" :
             'Get AI Predictions'}
          </p>
          <Button onClick={() => onFetchPredictions(activePeriod)} className="btn-sacred">
            <Sparkles className="w-4 h-4 mr-2" />
            {activePeriod === 'daily' ? "Today's Prediction" :
             activePeriod === 'monthly' ? 'Monthly Forecast' :
             activePeriod === 'yearly' ? 'Yearly Outlook' :
             'Get Predictions'}
          </Button>
          {isPuterAvailable() && (
            <p className="text-xs mt-3" style={{ color: 'var(--ink-light)' }}>Free AI available as backup if server is busy</p>
          )}
        </div>
      )}
    </div>
  );
}
