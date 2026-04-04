import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Send, User, Bot, Sun, Heart, Briefcase, Coins, Users, BookOpen, Zap } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { isPuterAvailable, puterChatStream, VEDIC_SYSTEM_PROMPT } from '@/lib/puter-ai';

interface Message { id: string; type: 'user' | 'ai'; content: string; timestamp: Date; streaming?: boolean; }

const quickQuestions = [
  { icon: Heart, text: 'Tell me about my love life', category: 'love' },
  { icon: Briefcase, text: 'Career prospects for 2025', category: 'career' },
  { icon: Coins, text: 'Financial predictions', category: 'finance' },
  { icon: Users, text: 'When will I get married?', category: 'marriage' },
  { icon: Sun, text: 'Daily horoscope', category: 'horoscope' },
  { icon: BookOpen, text: 'Gita wisdom', category: 'gita' },
];

export default function AIChat() {
  const { isAuthenticated } = useAuth();
  const [messages, setMessages] = useState<Message[]>([{
    id: '1', type: 'ai',
    content: `Namaste! I am your AI Astrologer.\n\nI can help you with:\n\u2022 Daily horoscope and predictions\n\u2022 Career and financial guidance\n\u2022 Love and relationship insights\n\u2022 Spiritual wisdom from the Gita\n\nHow may I assist you today?`,
    timestamp: new Date(),
  }]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [aiProvider, setAiProvider] = useState<'puter' | 'backend'>(isPuterAvailable() ? 'puter' : 'backend');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => scrollToBottom(), [messages]);

  // Re-check Puter availability when switching (in case it loaded late)
  const toggleProvider = () => {
    setAiProvider(prev => {
      if (prev === 'backend' && isPuterAvailable()) return 'puter';
      if (prev === 'backend') return 'backend'; // Puter not available
      return 'backend';
    });
  };

  /** Try Puter.js streaming first, fall back to backend API. */
  const sendViaPuter = async (text: string): Promise<boolean> => {
    if (!isPuterAvailable()) return false;
    const aiMsgId = (Date.now() + 1).toString();
    // Insert a placeholder message that will be updated with streamed content
    setMessages(prev => [...prev, { id: aiMsgId, type: 'ai', content: '', timestamp: new Date(), streaming: true }]);
    try {
      const fullText = await puterChatStream(text, VEDIC_SYSTEM_PROMPT, (accumulated) => {
        setMessages(prev => prev.map(m => m.id === aiMsgId ? { ...m, content: accumulated } : m));
      });
      // Mark streaming complete
      setMessages(prev => prev.map(m => m.id === aiMsgId ? { ...m, content: fullText || 'I appreciate your question. Let me consult the stars for deeper insight.', streaming: false } : m));
      return true;
    } catch {
      // Remove the placeholder on failure so backend can try
      setMessages(prev => prev.filter(m => m.id !== aiMsgId));
      return false;
    }
  };

  const sendViaBackend = async (text: string, isGita: boolean) => {
    try {
      const endpoint = isGita ? '/api/ai/gita' : '/api/ai/ask';
      const data = await api.post(endpoint, { question: text });
      const aiContent = data.answer || data.response || data.content || data.text || 'I appreciate your question. Let me consult the stars for deeper insight.';
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), type: 'ai', content: aiContent, timestamp: new Date() }]);
    } catch {
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), type: 'ai', content: 'I apologize, but I am unable to connect to the cosmic server at the moment. Please try again shortly.', timestamp: new Date() }]);
    }
  };

  const handleSend = async (text: string = input) => {
    if (!text.trim()) return;
    const lowerText = text.toLowerCase();
    const isGita = lowerText.includes('gita') || lowerText.includes('krishna') || lowerText.includes('dharma');
    if (!isGita && !isAuthenticated && aiProvider === 'backend') {
      setMessages(prev => [...prev, { id: Date.now().toString(), type: 'ai', content: 'Please sign in to use personalized AI astrology chat. Gita wisdom is available without login.', timestamp: new Date() }]);
      setInput('');
      return;
    }
    const userMessage: Message = { id: Date.now().toString(), type: 'user', content: text, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    if (aiProvider === 'puter') {
      const ok = await sendViaPuter(text);
      if (!ok) {
        // Puter failed — fall back to backend
        await sendViaBackend(text, isGita);
      }
    } else {
      await sendViaBackend(text, isGita);
    }
    setIsTyping(false);
  };

  // Hide WhatsApp widget on AI chat page
  useEffect(() => {
    const widgets = document.querySelectorAll('.ai-chat-hide');
    widgets.forEach(w => (w as HTMLElement).style.display = 'none');
    return () => { widgets.forEach(w => (w as HTMLElement).style.display = ''); };
  }, []);

  return (
    <div className="fixed inset-0 pt-16 pb-0 px-2 sm:px-4 flex flex-col z-30 bg-cosmic-bg">
      <div className="flex flex-col flex-1 min-h-0 max-w-4xl mx-auto w-full card-sacred rounded-t-2xl overflow-hidden border border-sacred-gold/20 border-b-0">
        <div className="flex items-center gap-3 p-4 border-b border-sacred-gold/15">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shadow-glow-gold">
            <Sparkles className="w-5 h-5 text-cosmic-bg" />
          </div>
          <div className="flex-1">
            <h3 className="font-sacred font-semibold text-base sm:text-lg text-cosmic-text">AI Astrologer</h3>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs text-cosmic-text-secondary">Online</span>
            </div>
          </div>
          <button
            onClick={toggleProvider}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs border transition-colors"
            style={{
              backgroundColor: aiProvider === 'puter' ? 'rgba(184,134,11,0.12)' : 'rgba(139,115,85,0.08)',
              borderColor: aiProvider === 'puter' ? 'rgba(184,134,11,0.35)' : 'rgba(139,115,85,0.2)',
              color: aiProvider === 'puter' ? '#B8860B' : '#8B7355',
            }}
            title={aiProvider === 'puter' ? 'Using free Puter.js AI (click to switch to backend)' : 'Using backend AI (click to switch to free Puter.js)'}
          >
            <Zap className="w-3 h-3" />
            {aiProvider === 'puter' ? 'Free AI' : 'Backend'}
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex gap-3 ${message.type === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${message.type === 'user' ? 'bg-sacred-purple/40 border border-sacred-violet/30' : 'bg-gradient-to-br from-sacred-gold to-sacred-saffron'}`}>
                {message.type === 'user' ? <User className="w-4 h-4 text-sacred-violet" /> : <Bot className="w-4 h-4 text-cosmic-bg" />}
              </div>
              <div className={`max-w-[80%] ${message.type === 'user' ? 'text-right' : ''}`}>
                <div className={`inline-block p-4 rounded-2xl text-left ${message.type === 'user' ? 'bg-sacred-purple/30 border border-sacred-violet/20 text-cosmic-text' : 'bg-cosmic-card border border-sacred-gold/10 text-cosmic-text'}`}>
                  <div className="whitespace-pre-line text-sm">{message.content}{message.streaming && <span className="inline-block w-1.5 h-4 ml-0.5 bg-sacred-gold animate-pulse align-middle" />}</div>
                </div>
              </div>
            </div>
          ))}
          {isTyping && !messages.some(m => m.streaming) && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-cosmic-bg" />
              </div>
              <div className="bg-cosmic-card border border-sacred-gold/10 p-4 rounded-2xl">
                <div className="flex gap-2">
                  <span className="w-2 h-2 rounded-full bg-sacred-gold animate-bounce" />
                  <span className="w-2 h-2 rounded-full bg-sacred-gold animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-sacred-gold animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        {messages.length < 3 && (
          <div className="px-4 py-3 border-t border-sacred-gold/10">
            <p className="text-xs text-cosmic-text-muted mb-2">Quick Questions:</p>
            <div className="flex gap-2 overflow-x-auto">
              {quickQuestions.map((q, i) => (
                <button key={i} onClick={() => handleSend(q.text)} className="flex items-center gap-2 px-3 py-2 rounded-full bg-cosmic-card border border-sacred-gold/15 text-xs text-cosmic-text-secondary hover:text-sacred-gold hover:border-sacred-gold/30 whitespace-nowrap transition-colors">
                  <q.icon className="w-3 h-3" />{q.text}
                </button>
              ))}
            </div>
          </div>
        )}
        <div className="p-3 sm:p-4 border-t border-sacred-gold/15 pb-safe">
          {!isAuthenticated && aiProvider === 'backend' && (
            <div className="mb-2 text-xs text-cosmic-text-muted">
              Backend AI requires <Link to="/login" className="text-sacred-gold hover:underline">sign in</Link>. Switch to Free AI or ask about Gita.
            </div>
          )}
          <div className="flex gap-2">
            <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && !isTyping && handleSend()} placeholder="Ask about astrology..." className="flex-1 input-sacred text-base" style={{ fontSize: '16px' }} />
            <Button onClick={() => handleSend()} disabled={!input.trim() || isTyping} className="btn-sacred disabled:opacity-50 shrink-0 w-12 h-12 p-0 flex items-center justify-center rounded-xl" style={{ backgroundColor: input.trim() && !isTyping ? '#B8860B' : undefined, color: input.trim() && !isTyping ? '#1a1a2e' : undefined }}>
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
