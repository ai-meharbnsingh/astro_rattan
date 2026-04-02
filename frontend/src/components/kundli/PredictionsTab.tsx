import { Button } from '@/components/ui/button';
import { Sparkles, Loader2 } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { isPuterAvailable } from '@/lib/puter-ai';

// Simple markdown-to-JSX renderer for prediction text
function renderMarkdown(text: string) {
  return text.split('\n').filter(l => l.trim()).map((line, idx) => {
    // Bold: **text**
    const parts = line.split(/\*\*(.*?)\*\*/g);
    const rendered = parts.map((part, i) =>
      i % 2 === 1 ? <strong key={i} style={{ color: '#5D4037' }}>{part}</strong> : part
    );

    // Heading lines
    if (line.startsWith('## ')) {
      return <h3 key={idx} className="font-display font-bold text-lg mt-4 mb-2" style={{ color: '#3D2B1F' }}>{rendered}</h3>;
    }
    // List items
    if (line.trimStart().startsWith('- ')) {
      return (
        <div key={idx} className="flex gap-2 mb-1.5 ml-2" style={{ fontFamily: 'serif', color: '#1a1a2e' }}>
          <span className="text-sacred-gold mt-0.5">•</span>
          <span className="leading-relaxed">{rendered}</span>
        </div>
      );
    }
    // Regular paragraph
    return <p key={idx} className="mb-3 leading-relaxed" style={{ fontFamily: 'serif', color: '#1a1a2e' }}>{rendered}</p>;
  });
}

interface PredictionsTabProps {
  predictionsData: any;
  loadingPredictions: boolean;
  onFetchPredictions: () => void;
}

export default function PredictionsTab({
  predictionsData,
  loadingPredictions,
  onFetchPredictions,
}: PredictionsTabProps) {
  const { t } = useTranslation();

  if (loadingPredictions) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingPredictions')}</span>
      </div>
    );
  }

  if (predictionsData) {
    return (
      <div className="space-y-4">
        <div className="rounded-2xl p-6 border" style={{ backgroundColor: '#F5F0E8', borderColor: 'rgba(139,115,85,0.2)' }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: 'rgba(184,134,11,0.15)' }}>
              <Sparkles className="w-5 h-5" style={{ color: '#B8860B' }} />
            </div>
            <h4 className="font-display font-semibold text-xl text-sacred-brown">{t('kundli.aiPredictions')}</h4>
            {predictionsData._puterFallback && (
              <span className="ml-auto text-xs px-2 py-1 rounded-full" style={{ backgroundColor: 'rgba(184,134,11,0.12)', color: '#B8860B', border: '1px solid rgba(184,134,11,0.3)' }}>
                {t('kundli.poweredByFreeAI')}
              </span>
            )}
          </div>
          <div className="max-w-none" style={{ color: '#1a1a2e' }}>
            {renderMarkdown(predictionsData.interpretation || predictionsData.response || predictionsData.text || JSON.stringify(predictionsData))}
            {predictionsData._streaming && <span className="inline-block w-1.5 h-4 ml-0.5 bg-sacred-gold animate-pulse align-middle" />}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="text-center py-12">
      <Sparkles className="w-10 h-10 mx-auto mb-3" style={{ color: 'rgba(184,134,11,0.4)' }} />
      <p className="text-sacred-text-secondary mb-4">{t('kundli.getPredictions')}</p>
      <Button onClick={onFetchPredictions} className="btn-sacred">
        <Sparkles className="w-4 h-4 mr-2" />{t('kundli.predictions')}
      </Button>
      {isPuterAvailable() && (
        <p className="text-xs mt-3" style={{ color: '#8B7355' }}>{t('kundli.freeAIFallback')}</p>
      )}
    </div>
  );
}
