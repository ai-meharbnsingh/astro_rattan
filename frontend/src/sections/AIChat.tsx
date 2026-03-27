import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Send, User, Bot, Sun, Heart, Briefcase, Coins, Users, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Message { id: string; type: 'user' | 'ai'; content: string; timestamp: Date; }

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
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => scrollToBottom(), [messages]);

  const handleSend = async (text: string = input) => {
    if (!text.trim()) return;
    const lowerText = text.toLowerCase();
    const isGita = lowerText.includes('gita') || lowerText.includes('krishna') || lowerText.includes('dharma');
    if (!isGita && !isAuthenticated) {
      setMessages(prev => [...prev, { id: Date.now().toString(), type: 'ai', content: 'Please sign in to use personalized AI astrology chat. Gita wisdom is available without login.', timestamp: new Date() }]);
      setInput('');
      return;
    }
    const userMessage: Message = { id: Date.now().toString(), type: 'user', content: text, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);
    try {
      const endpoint = isGita ? '/api/ai/gita' : '/api/ai/ask';
      const data = await api.post(endpoint, { question: text });
      const aiContent = data.answer || data.response || data.content || data.text || 'I appreciate your question. Let me consult the stars for deeper insight.';
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), type: 'ai', content: aiContent, timestamp: new Date() }]);
    } catch {
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), type: 'ai', content: 'I apologize, but I am unable to connect to the cosmic server at the moment. Please try again shortly.', timestamp: new Date() }]);
    } finally { setIsTyping(false); }
  };

  return (
    <div className="fixed inset-0 pt-16 pb-0 px-4 flex flex-col z-30 bg-cosmic-bg">
      <div className="flex flex-col flex-1 min-h-0 max-w-4xl mx-auto w-full card-sacred rounded-t-2xl overflow-hidden border border-sacred-gold/20 border-b-0">
        <div className="flex items-center gap-3 p-4 border-b border-sacred-gold/15">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shadow-glow-gold">
            <Sparkles className="w-5 h-5 text-cosmic-bg" />
          </div>
          <div>
            <h3 className="font-sacred font-semibold text-base sm:text-lg text-cosmic-text">AI Astrologer</h3>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs text-cosmic-text-secondary">Online</span>
            </div>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex gap-3 ${message.type === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${message.type === 'user' ? 'bg-sacred-purple/40 border border-sacred-violet/30' : 'bg-gradient-to-br from-sacred-gold to-sacred-saffron'}`}>
                {message.type === 'user' ? <User className="w-4 h-4 text-sacred-violet" /> : <Bot className="w-4 h-4 text-cosmic-bg" />}
              </div>
              <div className={`max-w-[80%] ${message.type === 'user' ? 'text-right' : ''}`}>
                <div className={`inline-block p-4 rounded-2xl text-left ${message.type === 'user' ? 'bg-sacred-purple/30 border border-sacred-violet/20 text-cosmic-text' : 'bg-cosmic-card border border-sacred-gold/10 text-cosmic-text'}`}>
                  <div className="whitespace-pre-line text-sm">{message.content}</div>
                </div>
              </div>
            </div>
          ))}
          {isTyping && (
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
        <div className="p-4 border-t border-sacred-gold/15">
          {!isAuthenticated && (
            <div className="mb-3 text-xs text-cosmic-text-muted">
              Personalized astrology chat requires <Link to="/login" className="text-sacred-gold hover:underline">sign in</Link>. Gita Q&A works without login.
            </div>
          )}
          <div className="flex gap-3">
            <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} placeholder="Ask anything about astrology..." className="flex-1 input-sacred" />
            <Button onClick={() => handleSend()} disabled={!input.trim() || isTyping} className="btn-sacred disabled:opacity-50">
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
