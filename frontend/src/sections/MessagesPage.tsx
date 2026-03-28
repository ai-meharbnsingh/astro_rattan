import { useState, useEffect, useRef, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare, Send, ArrowLeft, Loader2, User, Star } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/lib/api';

interface Conversation {
  consultation_id: string;
  astrologer_name: string;
  consultation_type: string;
  consultation_status: string;
  last_message?: string;
  last_message_at?: string;
  unread_count?: number;
}

interface Message {
  id: string;
  consultation_id: string;
  sender_id: string;
  sender_name?: string;
  content: string;
  message_type: string;
  created_at: string;
}

export default function MessagesPage() {
  const { isAuthenticated, user } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loadingConversations, setLoadingConversations] = useState(true);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const currentUserId = user?.sub || user?.id || '';

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Fetch conversations (derive from consultations list)
  useEffect(() => {
    if (!isAuthenticated) {
      setLoadingConversations(false);
      return;
    }

    const fetchConversations = async () => {
      setLoadingConversations(true);
      try {
        const data = await api.get('/api/consultations');
        const list = Array.isArray(data) ? data : data.consultations || [];
        const convos: Conversation[] = list
          .filter((c: Record<string, unknown>) => {
            const status = String(c.status ?? '');
            return ['accepted', 'active', 'completed'].includes(status);
          })
          .map((c: Record<string, unknown>) => ({
            consultation_id: String(c.id ?? ''),
            astrologer_name: String(c.astrologer_name ?? c.display_name ?? 'Astrologer'),
            consultation_type: String(c.type ?? 'chat'),
            consultation_status: String(c.status ?? ''),
            last_message: undefined,
            last_message_at: typeof c.created_at === 'string' ? c.created_at : undefined,
            unread_count: 0,
          }));
        setConversations(convos);
      } catch {
        /* empty */
      }
      setLoadingConversations(false);
    };
    fetchConversations();
  }, [isAuthenticated]);

  // Connect WebSocket when opening a conversation
  useEffect(() => {
    if (!activeConversation) return;

    const token = localStorage.getItem('astrovedic_token');
    if (!token) return;

    const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8028';
    const wsBase = apiBase.replace(/^http/, 'ws');
    const wsUrl = `${wsBase}/ws/consultation/${activeConversation.consultation_id}?token=${token}`;

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data) as Message;
        if (msg.id && msg.content) {
          setMessages((prev) => {
            // Avoid duplicates
            if (prev.some((m) => m.id === msg.id)) return prev;
            return [...prev, msg];
          });
        }
      } catch {
        /* ignore parse errors */
      }
    };

    ws.onerror = () => {
      /* silent */
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [activeConversation]);

  const openConversation = async (convo: Conversation) => {
    setActiveConversation(convo);
    setMessages([]);
    setLoadingMessages(true);
    try {
      // Try to fetch existing messages via REST; fall back gracefully if endpoint not available
      const data = await api.get(`/api/messages/${convo.consultation_id}`);
      const list = Array.isArray(data) ? data : data.messages || [];
      setMessages(
        list.map((m: Record<string, unknown>) => ({
          id: String(m.id ?? ''),
          consultation_id: String(m.consultation_id ?? convo.consultation_id),
          sender_id: String(m.sender_id ?? ''),
          sender_name: typeof m.sender_name === 'string' ? m.sender_name : undefined,
          content: String(m.content ?? ''),
          message_type: String(m.message_type ?? m.type ?? 'text'),
          created_at: String(m.created_at ?? ''),
        })),
      );
    } catch {
      // Endpoint might not exist; messages will come via WebSocket
    }
    setLoadingMessages(false);
  };

  const handleSend = async () => {
    const text = input.trim();
    if (!text || !activeConversation) return;

    setSending(true);
    setInput('');

    // Try WebSocket first, fall back to REST
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ content: text, type: 'text' }));
    } else {
      try {
        await api.post(`/api/messages/${activeConversation.consultation_id}`, {
          content: text,
          type: 'text',
        });
      } catch {
        // If REST also fails, add message optimistically
        const optimistic: Message = {
          id: `temp-${Date.now()}`,
          consultation_id: activeConversation.consultation_id,
          sender_id: currentUserId,
          sender_name: 'You',
          content: text,
          message_type: 'text',
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, optimistic]);
      }
    }
    setSending(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTimestamp = (dateStr: string) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 1) {
      return 'Yesterday ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays < 7) {
      return date.toLocaleDateString([], { weekday: 'short' }) + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' }) + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const isOwnMessage = (msg: Message) => msg.sender_id === currentUserId;

  if (!isAuthenticated) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4">
        <div className="card-sacred rounded-2xl border border-sacred-gold/20 p-12 text-center">
          <MessageSquare className="w-12 h-12 text-sacred-gold mx-auto mb-4" />
          <h2 className="text-xl font-display font-semibold text-cosmic-text mb-2">Sign in to view messages</h2>
          <p className="text-cosmic-text-secondary">Please sign in to chat with your astrologers.</p>
        </div>
      </div>
    );
  }

  // Chat thread view
  if (activeConversation) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4">
        <div className="flex flex-col h-[75vh] card-sacred rounded-2xl overflow-hidden border border-sacred-gold/20">
          {/* Header */}
          <div className="flex items-center gap-3 p-4 border-b border-sacred-gold/15 bg-cosmic-bg/50">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setActiveConversation(null);
                setMessages([]);
              }}
              className="text-cosmic-text hover:bg-sacred-gold/10"
            >
              <ArrowLeft className="w-4 h-4" />
            </Button>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shadow-glow-gold">
              <Star className="w-5 h-5 text-cosmic-bg" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-display font-semibold text-cosmic-text truncate">
                {activeConversation.astrologer_name}
              </h3>
              <p className="text-xs text-cosmic-text-secondary capitalize">
                {activeConversation.consultation_type} consultation
                <span className="mx-1.5">&middot;</span>
                <span className={
                  activeConversation.consultation_status === 'active'
                    ? 'text-green-400'
                    : 'text-cosmic-text-muted'
                }>
                  {activeConversation.consultation_status}
                </span>
              </p>
            </div>
          </div>

          {/* Messages area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {loadingMessages ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 text-sacred-gold animate-spin" />
              </div>
            ) : messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-cosmic-text-secondary">
                <MessageSquare className="w-10 h-10 text-cosmic-text-muted mb-3" />
                <p className="text-sm">No messages yet. Start the conversation!</p>
              </div>
            ) : (
              messages.map((msg) => {
                const own = isOwnMessage(msg);
                return (
                  <div key={msg.id} className={`flex ${own ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[75%] ${own ? 'order-last' : ''}`}>
                      <div
                        className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                          own
                            ? 'bg-sacred-purple/30 border border-sacred-violet/20 text-cosmic-text rounded-br-md'
                            : 'bg-sacred-gold/10 border border-sacred-gold/20 text-cosmic-text rounded-bl-md'
                        }`}
                      >
                        {!own && msg.sender_name && (
                          <p className="text-xs font-semibold text-sacred-gold mb-1">{msg.sender_name}</p>
                        )}
                        <p className="whitespace-pre-line">{msg.content}</p>
                      </div>
                      <p className={`text-[10px] text-cosmic-text-muted mt-1 px-1 ${own ? 'text-right' : 'text-left'}`}>
                        {formatTimestamp(msg.created_at)}
                      </p>
                    </div>
                  </div>
                );
              })
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <div className="p-4 border-t border-sacred-gold/15 bg-cosmic-bg/50">
            {activeConversation.consultation_status === 'completed' ? (
              <p className="text-center text-sm text-cosmic-text-muted py-1">
                This consultation has ended. Messages are read-only.
              </p>
            ) : (
              <div className="flex gap-2">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your message..."
                  className="flex-1 bg-cosmic-card border-sacred-gold/15 text-cosmic-text placeholder:text-cosmic-text-muted focus:border-sacred-gold/40"
                />
                <Button
                  onClick={handleSend}
                  disabled={!input.trim() || sending}
                  className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark disabled:opacity-40"
                >
                  {sending ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Conversations list view
  return (
    <div className="max-w-4xl mx-auto py-24 px-4">
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-4">
          <MessageSquare className="w-4 h-4" />
          Messages
        </div>
        <h2 className="text-3xl sm:text-4xl font-display font-bold text-cosmic-text mb-2">
          Chat with <span className="text-gradient-indigo">Your Astrologers</span>
        </h2>
        <p className="text-cosmic-text-secondary">Continue your consultation conversations</p>
      </div>

      <div className="card-sacred rounded-2xl border border-sacred-gold/20 overflow-hidden">
        {loadingConversations ? (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="w-8 h-8 text-sacred-gold animate-spin" />
          </div>
        ) : conversations.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-cosmic-text-secondary">
            <MessageSquare className="w-12 h-12 text-cosmic-text-muted mb-4" />
            <p className="text-lg font-medium text-cosmic-text mb-1">No conversations yet</p>
            <p className="text-sm">Book a consultation to start chatting with an astrologer.</p>
          </div>
        ) : (
          <div className="divide-y divide-sacred-gold/10">
            {conversations.map((convo) => (
              <button
                key={convo.consultation_id}
                onClick={() => openConversation(convo)}
                className="w-full flex items-center gap-4 p-4 hover:bg-sacred-gold/5 transition-colors text-left"
              >
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shrink-0 shadow-glow-gold">
                  <span className="text-cosmic-bg font-bold text-lg">
                    {convo.astrologer_name.charAt(0)}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <h4 className="font-display font-semibold text-cosmic-text truncate">
                      {convo.astrologer_name}
                    </h4>
                    {convo.last_message_at && (
                      <span className="text-[11px] text-cosmic-text-muted shrink-0">
                        {formatTimestamp(convo.last_message_at)}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-cosmic-text-secondary truncate capitalize">
                    {convo.consultation_type} consultation
                    <span className="mx-1.5">&middot;</span>
                    <span className={
                      convo.consultation_status === 'active'
                        ? 'text-green-400'
                        : convo.consultation_status === 'completed'
                        ? 'text-cosmic-text-muted'
                        : 'text-blue-400'
                    }>
                      {convo.consultation_status}
                    </span>
                  </p>
                  {convo.last_message && (
                    <p className="text-xs text-cosmic-text-muted truncate mt-0.5">{convo.last_message}</p>
                  )}
                </div>
                <ArrowLeft className="w-4 h-4 text-cosmic-text-muted rotate-180 shrink-0" />
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
