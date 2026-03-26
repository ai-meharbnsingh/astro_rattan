import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Send, User, Bot, Sun, Heart, Briefcase, Coins, Users, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

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
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'ai',
      content: `Namaste! I am your AI Astrologer.\n\nI can help you with:\n\u2022 Daily horoscope and predictions\n\u2022 Career and financial guidance\n\u2022 Love and relationship insights\n\u2022 Spiritual wisdom from the Gita\n\nHow may I assist you today?`,
      timestamp: new Date(),
    },
  ]);
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
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        type: 'ai',
        content: 'Please sign in to use personalized AI astrology chat. Gita wisdom is available without login.',
        timestamp: new Date(),
      }]);
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
      const aiMessage: Message = { id: (Date.now() + 1).toString(), type: 'ai', content: aiContent, timestamp: new Date() };
      setMessages(prev => [...prev, aiMessage]);
    } catch {
      const fallbackMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: 'I apologize, but I am unable to connect to the cosmic server at the moment. Please try again shortly.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, fallbackMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-24 px-4">
      <div className="flex flex-col h-[70vh] bg-white rounded-2xl shadow-soft border border-minimal-gray-100 overflow-hidden">
        <div className="flex items-center gap-3 p-4 border-b border-minimal-gray-200">
          <div className="w-10 h-10 rounded-full bg-minimal-indigo flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-display font-semibold text-base sm:text-lg text-minimal-gray-900">AI Astrologer</h3>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs text-minimal-gray-500">Online</span>
            </div>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex gap-3 ${message.type === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${message.type === 'user' ? 'bg-minimal-violet/20' : 'bg-minimal-indigo'}`}>
                {message.type === 'user' ? <User className="w-4 h-4 text-minimal-violet" /> : <Bot className="w-4 h-4 text-white" />}
              </div>
              <div className={`max-w-[80%] ${message.type === 'user' ? 'text-right' : ''}`}>
                <div className={`inline-block p-4 rounded-2xl text-left ${message.type === 'user' ? 'bg-minimal-violet/20 text-minimal-gray-900' : 'bg-minimal-gray-100 text-minimal-gray-900'}`}>
                  <div className="whitespace-pre-line text-sm">{message.content}</div>
                </div>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-minimal-indigo flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="bg-minimal-gray-100 p-4 rounded-2xl">
                <div className="flex gap-2">
                  <span className="w-2 h-2 rounded-full bg-minimal-indigo animate-bounce" />
                  <span className="w-2 h-2 rounded-full bg-minimal-indigo animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-minimal-indigo animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        {messages.length < 3 && (
          <div className="px-4 py-3 border-t border-minimal-gray-200">
            <p className="text-xs text-minimal-gray-400 mb-2">Quick Questions:</p>
            <div className="flex gap-2 overflow-x-auto">
              {quickQuestions.map((q, i) => (
                <button key={i} onClick={() => handleSend(q.text)} className="flex items-center gap-2 px-3 py-2 rounded-full bg-minimal-gray-100 text-xs text-minimal-gray-600 hover:text-minimal-indigo whitespace-nowrap">
                  <q.icon className="w-3 h-3" />{q.text}
                </button>
              ))}
            </div>
          </div>
        )}
        <div className="p-4 border-t border-minimal-gray-200">
          {!isAuthenticated && (
            <div className="mb-3 text-xs text-minimal-gray-500">
              Personalized astrology chat requires <Link to="/login" className="text-minimal-indigo hover:underline">sign in</Link>. Gita Q&A works without login.
            </div>
          )}
          <div className="flex gap-3">
            <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} placeholder="Ask anything about astrology..." className="flex-1 bg-minimal-gray-50 border-minimal-gray-200 text-minimal-gray-900" />
            <Button onClick={() => handleSend()} disabled={!input.trim() || isTyping} className="bg-minimal-indigo text-white hover:bg-minimal-violet disabled:opacity-50">
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
