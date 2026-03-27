import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Bell, Check, CheckCheck, ExternalLink } from 'lucide-react';
import { api } from '../lib/api';
import { useAuth } from '../hooks/useAuth';

interface Notification {
  id: string;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  link: string | null;
  created_at: string;
}

const TYPE_ICONS: Record<string, string> = {
  transit: 'planet',
  muhurat: 'clock',
  festival: 'sparkles',
  streak: 'flame',
  content: 'book',
};

const TYPE_COLORS: Record<string, string> = {
  transit: 'text-blue-400',
  muhurat: 'text-green-400',
  festival: 'text-sacred-gold',
  streak: 'text-orange-400',
  content: 'text-purple-400',
};

function timeAgo(dateStr: string): string {
  const now = new Date();
  const past = new Date(dateStr + 'Z');
  const diffMs = now.getTime() - past.getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d ago`;
  return past.toLocaleDateString();
}

export default function NotificationBell() {
  const { isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isAuthenticated) return;
    fetchUnreadCount();
    const interval = setInterval(fetchUnreadCount, 30000);
    return () => clearInterval(interval);
  }, [isAuthenticated]);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  async function fetchUnreadCount() {
    try {
      const data = await api.get('/api/notifications/unread-count');
      setUnreadCount(data.unread_count);
    } catch {
      // silently fail
    }
  }

  async function fetchNotifications() {
    setLoading(true);
    try {
      const data = await api.get('/api/notifications?limit=10');
      setNotifications(data.notifications || []);
    } catch {
      // silently fail
    } finally {
      setLoading(false);
    }
  }

  async function handleToggle() {
    if (!isOpen) {
      await fetchNotifications();
    }
    setIsOpen(!isOpen);
  }

  async function markAsRead(id: string) {
    try {
      await api.patch(`/api/notifications/${id}/read`, {});
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
      setUnreadCount((c) => Math.max(0, c - 1));
    } catch {
      // silently fail
    }
  }

  async function markAllRead() {
    try {
      await api.patch('/api/notifications/read-all', {});
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch {
      // silently fail
    }
  }

  if (!isAuthenticated) return null;

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={handleToggle}
        className="relative p-2 text-sacred-brown hover:text-sacred-gold transition-colors"
        aria-label="Notifications"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] flex items-center justify-center rounded-full bg-red-500 text-white text-[10px] font-bold px-1 animate-pulse">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-80 sm:w-96 card-sacred rounded-xl shadow-2xl border border-sacred-gold/20 z-50 max-h-[70vh] flex flex-col overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-sacred-gold/20">
            <h3 className="font-sacred font-semibold text-sacred-gold text-sm">Notifications</h3>
            {unreadCount > 0 && (
              <button
                onClick={markAllRead}
                className="flex items-center gap-1 text-xs text-sacred-gold/70 hover:text-sacred-gold transition-colors"
              >
                <CheckCheck className="w-3.5 h-3.5" />
                Mark all read
              </button>
            )}
          </div>

          {/* Notification list */}
          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <div className="w-6 h-6 border-2 border-sacred-gold/30 border-t-sacred-gold rounded-full animate-spin" />
              </div>
            ) : notifications.length === 0 ? (
              <div className="py-8 text-center text-cosmic-text/50 text-sm">
                No notifications yet
              </div>
            ) : (
              notifications.map((n) => (
                <div
                  key={n.id}
                  className={`px-4 py-3 border-b border-sacred-gold/10 hover:bg-sacred-gold/5 transition-colors cursor-pointer ${
                    !n.is_read ? 'bg-sacred-gold/5' : ''
                  }`}
                  onClick={() => !n.is_read && markAsRead(n.id)}
                >
                  <div className="flex items-start gap-3">
                    <div className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${n.is_read ? 'bg-transparent' : 'bg-sacred-gold'}`} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className={`text-xs font-medium uppercase tracking-wide ${TYPE_COLORS[n.type] || 'text-cosmic-text/60'}`}>
                          {n.type}
                        </span>
                        <span className="text-[10px] text-cosmic-text/40">{timeAgo(n.created_at)}</span>
                      </div>
                      <p className="text-sm font-medium text-cosmic-text mt-0.5 truncate">{n.title}</p>
                      <p className="text-xs text-cosmic-text/60 mt-0.5 line-clamp-2">{n.message}</p>
                      {n.link && (
                        <Link
                          to={n.link}
                          onClick={() => setIsOpen(false)}
                          className="inline-flex items-center gap-1 mt-1 text-xs text-sacred-gold hover:text-sacred-gold/80 transition-colors"
                        >
                          View details <ExternalLink className="w-3 h-3" />
                        </Link>
                      )}
                    </div>
                    {!n.is_read && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          markAsRead(n.id);
                        }}
                        className="mt-1 p-1 text-cosmic-text/40 hover:text-sacred-gold transition-colors"
                        title="Mark as read"
                      >
                        <Check className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          {notifications.length > 0 && (
            <div className="px-4 py-2 border-t border-sacred-gold/20 text-center">
              <Link
                to="/cosmic-calendar"
                onClick={() => setIsOpen(false)}
                className="text-xs text-sacred-gold hover:text-sacred-gold/80 transition-colors"
              >
                View Cosmic Calendar
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
