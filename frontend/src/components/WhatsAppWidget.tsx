import { useState, useEffect } from 'react';
import { MessageCircle, X } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

const WHATSAPP_NUMBER = '918076025521';

export default function WhatsAppWidget() {
  const { t } = useTranslation();
  const [showTooltip, setShowTooltip] = useState(() => window.innerWidth >= 640);

  useEffect(() => {
    if (window.innerWidth >= 640) {
      const timer = setTimeout(() => setShowTooltip(false), 5000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleClick = () => {
    const msg = encodeURIComponent(t('whatsapp.prefill'));
    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${msg}`;
    // noopener,noreferrer required for security; fallback to location.href
    // handles Instagram/FB in-app browsers that block window.open popups.
    const w = window.open(url, '_blank', 'noopener,noreferrer');
    if (!w) window.location.href = url;
  };

  return (
    <div className="fixed bottom-[calc(1.5rem+env(safe-area-inset-bottom))] right-4 sm:right-6 z-30 flex items-end gap-3 ai-chat-hide">
      {showTooltip && (
        <div className="relative bg-card border border-sacred-gold rounded-xl rounded-br-sm px-4 py-3 shadow-lg max-w-[200px] animate-fade-in">
          <button onClick={() => setShowTooltip(false)} aria-label={t('common.close')} className="absolute -top-3 -right-3 w-11 h-11 rounded-full bg-secondary border border-sacred-gold flex items-center justify-center text-foreground hover:text-foreground">
            <X className="w-4 h-4" />
          </button>
          <p className="text-sm text-muted-foreground">{t('whatsapp.tooltip')}</p>
        </div>
      )}
      <button
        onClick={handleClick}
        className="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-whatsapp-green flex items-center justify-center shadow-lg hover:shadow-xl hover:scale-105 transition-all"
        aria-label={t('whatsapp.aria')}
      >
        <MessageCircle className="w-7 h-7 text-background" fill="white" />
      </button>
    </div>
  );
}
