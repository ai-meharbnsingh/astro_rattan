import { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';

const WHATSAPP_NUMBER = '918076025521';

export default function WhatsAppWidget() {
  const [showTooltip, setShowTooltip] = useState(true);

  const handleClick = () => {
    const msg = encodeURIComponent('Hi, I want to know about my horoscope and kundli');
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${msg}`, '_blank');
  };

  return (
    <div className="fixed bottom-6 right-6 z-40 flex items-end gap-3 ai-chat-hide">
      {showTooltip && (
        <div className="relative bg-cosmic-card border border-sacred-gold rounded-2xl rounded-br-sm px-4 py-3 shadow-lg max-w-[200px] animate-fade-in">
          <button onClick={() => setShowTooltip(false)} className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-cosmic-surface border border-sacred-gold flex items-center justify-center text-cosmic-text hover:text-cosmic-text">
            <X className="w-3 h-3" />
          </button>
          <p className="text-sm text-cosmic-text-secondary">Chat with us on WhatsApp for instant astrology guidance!</p>
        </div>
      )}
      <button
        onClick={handleClick}
        className="w-14 h-14 rounded-full bg-whatsapp-green flex items-center justify-center shadow-lg hover:shadow-xl hover:scale-105 transition-all"
        aria-label="Chat on WhatsApp"
      >
        <MessageCircle className="w-7 h-7 text-cosmic-bg" fill="white" />
      </button>
    </div>
  );
}
