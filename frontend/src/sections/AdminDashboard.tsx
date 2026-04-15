import { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users, Star, Calendar, Activity, Shield, ChevronRight, ChevronLeft,
  ToggleLeft, ToggleRight, Zap, AlertTriangle, Clock, Radio,
  TrendingUp, Globe, User, RefreshCw, MessageSquare, CheckCircle2,
  ChevronDown, ChevronUp, Filter,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Heading } from '@/components/ui/heading';
import {
  Table, TableHeader, TableBody, TableRow, TableHead, TableCell,
} from '@/components/ui/table';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { api, formatDate } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';

// ── Types ────────────────────────────────────────────────────────────────────
interface Stats {
  counts: { users: number; kundlis: number; horoscopes: number; panchang_cached: number };
  recent_users: Array<{ id: string; email: string; name: string; role: string; created_at: string }>;
  recent_kundlis: Array<{ id: string; person_name: string; birth_date: string; created_at: string; email: string }>;
}

interface UserRow {
  id: string; email: string; name: string; role: string;
  phone: string | null; city: string | null; is_active: number; created_at: string;
}

interface ActiveUser {
  user_id: string; email: string; name: string;
  last_path: string; seconds_ago: number;
}

interface TopEndpoint {
  path: string; count: number; avg_ms: number;
}

interface LiveEntry {
  ts_iso: string; method: string; path: string;
  status: number; duration_ms: number; is_error: boolean; email: string | null;
}

interface LiveData {
  active_users: ActiveUser[];
  active_users_count: number;
  requests_1m: number;
  requests_5m: number;
  error_rate_1m: number;
  top_endpoints: TopEndpoint[];
  recent_activity: LiveEntry[];
  uptime_seconds: number;
}

interface AnalyticsData {
  total_views: number;
  total_sessions: number;
  today_views: number;
  today_sessions: number;
  week_views: number;
  week_sessions: number;
  month_views: number;
  top_pages: Array<{ path: string; views: number; visitors: number }>;
  hourly_today: Array<{ hour: number; views: number }>;
  daily_last_30: Array<{ day: string; views: number; visitors: number }>;
}

interface FeedbackItem {
  id: string;
  user_name: string;
  user_email: string;
  rating_interface: number | null;
  rating_reports: number | null;
  rating_calculations: number | null;
  feedback_text: string | null;
  status: 'open' | 'closed';
  action_taken: 'yes' | 'no' | 'NR';
  admin_remarks: string | null;
  created_at: string;
}

interface WordCloudWord { word: string; count: number; }

// ── Word cloud (open feedback only) ──────────────────────────────────────────
const CLOUD_COLORS = [
  'text-sacred-gold-dark', 'text-amber-500', 'text-orange-500',
  'text-blue-500', 'text-purple-500', 'text-teal-500',
  'text-rose-500', 'text-indigo-500', 'text-emerald-600',
];

function WordCloud({ words }: { words: WordCloudWord[] }) {
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  if (!words.length) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-muted-foreground text-sm gap-2">
        <MessageSquare className="w-6 h-6 text-gray-200" />
        <span>{l('Word cloud appears when users submit open feedback', 'जब उपयोगकर्ता खुला फीडबैक भेजते हैं तब वर्ड क्लाउड दिखेगा')}</span>
      </div>
    );
  }
  const maxCount = words[0]?.count || 1;
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-2 items-center justify-center px-6 py-5 min-h-[80px]">
      {words.map((w, i) => {
        const pct = w.count / maxCount;
        const size = Math.round(12 + pct * 28); // 12–40 px
        return (
          <span
            key={w.word}
            className={`font-medium cursor-default select-none transition-transform hover:scale-110 ${CLOUD_COLORS[i % CLOUD_COLORS.length]}`}
            style={{ fontSize: `${size}px`, opacity: 0.45 + pct * 0.55 }}
            title={language === 'hi' ? `"${w.word}" — ${w.count} उल्लेख` : `"${w.word}" — ${w.count} mention${w.count !== 1 ? 's' : ''}`}
          >
            {w.word}
          </span>
        );
      })}
    </div>
  );
}

// ── Inline-editable feedback row ──────────────────────────────────────────────
function FeedbackRow({
  item, onUpdated,
}: {
  item: FeedbackItem;
  onUpdated: (id: string, patch: Partial<FeedbackItem>) => void;
}) {
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const [remarks, setRemarks] = useState(item.admin_remarks ?? '');
  const [expanded, setExpanded] = useState(false);
  const hasLong = (item.feedback_text?.length ?? 0) > 100;

  const saveAction = async (action: string) => {
    try {
      await api.patch(`/api/admin/feedback/${item.id}`, { action_taken: action });
      onUpdated(item.id, { action_taken: action as FeedbackItem['action_taken'] });
    } catch { /* ignored */ }
  };

  const saveRemarks = async () => {
    const val = remarks.trim();
    if (val === (item.admin_remarks ?? '')) return;
    try {
      await api.patch(`/api/admin/feedback/${item.id}`, { admin_remarks: val });
      onUpdated(item.id, { admin_remarks: val });
    } catch { /* ignored */ }
  };

  const ratingCell = (v: number | null) =>
    v ? (
      <span className="inline-flex items-center gap-0.5">
        <Star className="w-3 h-3 text-sacred-gold-dark fill-current" />
        <span className="text-xs font-medium text-foreground">{v}</span>
      </span>
    ) : <span className="text-xs text-muted-foreground">—</span>;

  const actionStyle: Record<string, string> = {
    yes: 'text-green-700 bg-green-50 border-green-200',
    no:  'text-red-600 bg-red-50 border-red-200',
    NR:  'text-muted-foreground bg-gray-50 border-gray-200',
  };

  return (
    <tr className="border-b border-gray-50 hover:bg-sacred-gold/4 transition-colors align-top">
      {/* User */}
      <td className="py-3 px-4">
        <p className="text-sm font-medium text-foreground">{item.user_name}</p>
        <p className="text-xs text-muted-foreground">{item.user_email}</p>
      </td>

      {/* Ratings */}
      <td className="py-3 px-4">
        <div className="flex flex-col gap-1 text-xs text-muted-foreground">
          <span>{l('UI', 'इंटरफ़ेस')} {ratingCell(item.rating_interface)}</span>
          <span>{l('Rpt', 'रिपोर्ट')} {ratingCell(item.rating_reports)}</span>
          <span>{l('Calc', 'गणना')} {ratingCell(item.rating_calculations)}</span>
        </div>
      </td>

      {/* Feedback text */}
      <td className="py-3 px-4 max-w-[200px]">
        {item.feedback_text ? (
          <div>
            <p className={`text-xs text-muted-foreground leading-relaxed ${expanded ? '' : 'line-clamp-2'}`}>
              {item.feedback_text}
            </p>
            {hasLong && (
              <button
                onClick={() => setExpanded(v => !v)}
                className="flex items-center gap-0.5 text-[10px] text-sacred-gold-dark mt-0.5 hover:underline"
              >
                {expanded ? <><ChevronUp className="w-3 h-3" />{l('Less', 'कम')}</> : <><ChevronDown className="w-3 h-3" />{l('More', 'अधिक')}</>}
              </button>
            )}
          </div>
        ) : <span className="text-xs text-muted-foreground">—</span>}
      </td>

      {/* Status */}
      <td className="py-3 px-4 whitespace-nowrap">
        {item.status === 'closed' ? (
          <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-green-50 border border-green-200 text-green-700 font-medium">
            <CheckCircle2 className="w-3 h-3" /> {l('Resolved', 'सुलझा')}
          </span>
        ) : (
          <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-700 font-medium">
            <Clock className="w-3 h-3" /> {l('Open', 'खुला')}
          </span>
        )}
      </td>

      {/* Action Taken — inline select */}
      <td className="py-3 px-4 whitespace-nowrap">
        <select
          value={item.action_taken}
          onChange={e => saveAction(e.target.value)}
          className={`text-xs border rounded-lg px-2 py-1 font-medium cursor-pointer focus:outline-none ${actionStyle[item.action_taken]}`}
        >
          <option value="NR">{l('Not Reviewed', 'समीक्षा नहीं')}</option>
          <option value="yes">{l('Action Taken', 'कार्यवाही हुई')}</option>
          <option value="no">{l('No Action', 'कोई कार्यवाही नहीं')}</option>
        </select>
      </td>

      {/* Admin Remarks — inline text */}
      <td className="py-3 px-4 min-w-[160px]">
        <input
          value={remarks}
          onChange={e => setRemarks(e.target.value)}
          onBlur={saveRemarks}
          onKeyDown={e => { if (e.key === 'Enter') (e.target as HTMLInputElement).blur(); }}
          placeholder={l('Add remark…', 'टिप्पणी जोड़ें…')}
          className="w-full text-xs border border-sacred-gold/20 rounded-lg px-2 py-1.5 bg-white/80 text-foreground focus:outline-none focus:ring-1 focus:ring-sacred-gold/40 placeholder:text-muted-foreground"
        />
      </td>

      {/* Date */}
      <td className="py-3 px-4 whitespace-nowrap">
        <span className="text-xs text-muted-foreground">
          {new Date(item.created_at).toLocaleDateString('en-IN', {
            day: 'numeric', month: 'short', year: 'numeric',
          })}
        </span>
      </td>
    </tr>
  );
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function formatUptime(s: number): string {
  if (!s) return '—';
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m ${sec}s`;
  return `${sec}s`;
}

function timeAgo(seconds: number, language: string): string {
  if (language === 'hi') {
    if (seconds < 60) return `${seconds} से पहले`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)} मि पहले`;
    return `${Math.floor(seconds / 3600)} घं पहले`;
  }
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  return `${Math.floor(seconds / 3600)}h ago`;
}

function statusColor(status: number): string {
  if (status < 300) return 'text-green-600';
  if (status < 400) return 'text-blue-500';
  if (status < 500) return 'text-orange-500';
  return 'text-red-500';
}

function statusBg(status: number): string {
  if (status < 300) return 'bg-green-50 border-l-2 border-green-400';
  if (status < 400) return 'bg-blue-50 border-l-2 border-blue-400';
  if (status < 500) return 'bg-orange-50 border-l-2 border-orange-400';
  return 'bg-red-50 border-l-2 border-red-400';
}

function methodColor(method: string): string {
  if (method === 'GET') return 'text-blue-600 bg-blue-50';
  if (method === 'POST') return 'text-green-700 bg-green-50';
  if (method === 'PATCH' || method === 'PUT') return 'text-orange-600 bg-orange-50';
  if (method === 'DELETE') return 'text-red-600 bg-red-50';
  return 'text-muted-foreground bg-gray-50';
}

// ── Stat card ────────────────────────────────────────────────────────────────
function StatCard({
  icon: Icon, label, value, sub, highlight,
}: { icon: React.ElementType; label: string; value: string | number; sub?: string; highlight?: 'green' | 'amber' | 'red' | 'blue' }) {
  const accent = {
    green: 'border-green-300 bg-green-50/60 text-green-700',
    amber: 'border-sacred-gold bg-sacred-gold/5 text-sacred-gold-dark',
    red:   'border-red-300 bg-red-50/60 text-red-600',
    blue:  'border-blue-300 bg-blue-50/60 text-blue-700',
  }[highlight ?? 'amber'];

  return (
    <div className={`rounded-xl border p-4 ${accent}`}>
      <div className="flex items-center gap-2 mb-2">
        <Icon className="w-4 h-4 shrink-0" />
        <p className="text-xs font-medium uppercase tracking-wider opacity-80">{label}</p>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      {sub && <p className="text-xs opacity-60 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Main component ───────────────────────────────────────────────────────────
export default function AdminDashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const [tab, setTab] = useState<'overview' | 'users' | 'kundlis' | 'live' | 'analytics' | 'feedback'>('overview');

  // overview
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // users
  const [users, setUsers] = useState<UserRow[]>([]);
  const [userPage, setUserPage] = useState(1);
  const [userPages, setUserPages] = useState(1);
  const [userTotal, setUserTotal] = useState(0);

  // kundlis
  const [kundlis, setKundlis] = useState<any[]>([]);
  const [kundliPage, setKundliPage] = useState(1);
  const [kundliPages, setKundliPages] = useState(1);

  // analytics
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);

  // feedback
  const [feedbackItems, setFeedbackItems] = useState<FeedbackItem[]>([]);
  const [feedbackTotal, setFeedbackTotal] = useState(0);
  const [feedbackPage, setFeedbackPage] = useState(1);
  const [feedbackPages, setFeedbackPages] = useState(1);
  const [feedbackFilterStatus, setFeedbackFilterStatus] = useState('');
  const [feedbackFilterAction, setFeedbackFilterAction] = useState('');
  const [wordCloud, setWordCloud] = useState<WordCloudWord[]>([]);

  // live
  const [liveData, setLiveData] = useState<LiveData | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [_tickMs, _setTickMs] = useState(0);
  const liveInterval = useRef<ReturnType<typeof setInterval> | null>(null);
  const activityRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (user?.role !== 'admin') { navigate('/'); return; }
    fetchStats();
  }, [user]); // eslint-disable-line react-hooks/exhaustive-deps

  // Tick to update "Xs ago" on live panel without refetching
  useEffect(() => {
    const id = setInterval(() => _setTickMs(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const fetchStats = async () => {
    try {
      const data = await api.get('/api/admin/stats');
      setStats(data);
    } catch { setError(l('Failed to load stats', 'आंकड़े लोड नहीं हो सके')); }
    setLoading(false);
  };

  const fetchUsers = async (page = 1) => {
    try {
      const data = await api.get(`/api/admin/users?page=${page}&limit=15`);
      setUsers(data.users); setUserPage(data.page);
      setUserPages(data.pages); setUserTotal(data.total);
    } catch { /* ignored */ }
  };

  const fetchKundlis = async (page = 1) => {
    try {
      const data = await api.get(`/api/admin/kundlis?page=${page}&limit=15`);
      setKundlis(data.kundlis); setKundliPage(data.page); setKundliPages(data.pages);
    } catch { /* ignored */ }
  };

  const fetchAnalytics = async () => {
    try {
      const data = await api.get('/api/admin/analytics');
      setAnalyticsData(data);
    } catch { /* ignored */ }
  };

  const fetchFeedback = async (
    page = feedbackPage,
    status = feedbackFilterStatus,
    action = feedbackFilterAction,
  ) => {
    try {
      const params = new URLSearchParams({ page: String(page), limit: '20' });
      if (status) params.set('status', status);
      if (action) params.set('action_taken', action);
      const data = await api.get(`/api/admin/feedback?${params}`);
      setFeedbackItems(data.items);
      setFeedbackTotal(data.total);
      setFeedbackPage(data.page);
      setFeedbackPages(data.pages);
    } catch { /* ignored */ }
  };

  const fetchWordCloud = async () => {
    try {
      const data = await api.get('/api/admin/feedback/wordcloud');
      setWordCloud(data);
    } catch { /* ignored */ }
  };

  const fetchLive = useCallback(async () => {
    try {
      const data = await api.get('/api/admin/live');
      setLiveData(data);
      setLastUpdated(new Date());
    } catch { /* ignored */ }
  }, []);

  useEffect(() => {
    if (tab === 'users') fetchUsers();
    if (tab === 'kundlis') fetchKundlis();
    if (tab === 'analytics') fetchAnalytics();
    if (tab === 'feedback') { fetchFeedback(1, '', ''); fetchWordCloud(); }
    if (tab === 'live') {
      fetchLive();
      liveInterval.current = setInterval(fetchLive, 5000);
    }
    return () => {
      if (liveInterval.current) clearInterval(liveInterval.current);
    };
  }, [tab]); // eslint-disable-line react-hooks/exhaustive-deps

  const changeRole = async (userId: string, role: string) => {
    try { await api.patch(`/api/admin/users/${userId}/role`, { role }); fetchUsers(userPage); }
    catch { /* ignored */ }
  };

  const toggleActive = async (userId: string) => {
    try { await api.patch(`/api/admin/users/${userId}/toggle-active`, {}); fetchUsers(userPage); }
    catch { /* ignored */ }
  };

  const secondsSinceLast = lastUpdated ? Math.round((Date.now() - lastUpdated.getTime()) / 1000) : null;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sacred-gold" />
      </div>
    );
  }
  if (error) return <div className="text-center py-20 text-red-400">{error}</div>;

  const tabs = [
    { key: 'overview', label: l('Overview', 'अवलोकन') },
    { key: 'users', label: l('Users', 'उपयोगकर्ता') },
    { key: 'kundlis', label: l('Kundlis', 'कुंडलियां') },
    { key: 'live', label: l('Live', 'लाइव') },
    { key: 'analytics', label: l('Analytics', 'एनालिटिक्स') },
    { key: 'feedback', label: l('Feedback', 'फीडबैक') },
  ] as const;

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-7xl mx-auto">
      {/* Page header */}
      <div className="flex items-center gap-3 mb-8">
        <Shield className="w-8 h-8 text-sacred-gold-dark" />
        <div>
          <Heading as={1} variant={1}>{l('Admin Dashboard', 'एडमिन डैशबोर्ड')}</Heading>
          <p className="text-xs text-muted-foreground mt-0.5">{l('astrorattan.com management panel', 'astrorattan.com प्रबंधन पैनल')}</p>
        </div>
      </div>

      {/* Tab bar */}
      <div className="flex gap-1 mb-8 border-b border-sacred-gold/30 pb-0">
        {tabs.map(t => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`relative px-5 py-2.5 text-sm font-medium transition-all ${
              tab === t.key
                ? 'text-sacred-gold-dark border-b-2 border-sacred-gold -mb-px bg-sacred-gold/8 rounded-t-lg'
                : 'text-muted-foreground hover:text-foreground hover:bg-gray-50 rounded-t-lg'
            }`}
          >
            {t.key === 'live' && (
              <span className="inline-flex items-center gap-1.5">
                <span className="relative flex h-2 w-2">
                  <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${tab === 'live' ? 'bg-green-400' : 'bg-gray-400'}`} />
                  <span className={`relative inline-flex rounded-full h-2 w-2 ${tab === 'live' ? 'bg-green-500' : 'bg-gray-400'}`} />
                </span>
                {l('Live', 'लाइव')}
              </span>
            )}
            {t.key !== 'live' && t.label}
          </button>
        ))}
      </div>

      {/* ── OVERVIEW ─────────────────────────────────────────────────────── */}
      {tab === 'overview' && (
        <div>
          {!stats ? (
            <div className="text-center py-16 border border-dashed border-sacred-gold/40 rounded-xl">
              <Shield className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-foreground font-medium">{l('No data yet', 'अभी डेटा नहीं है')}</p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                {[
                  { label: l('Total Users', 'कुल उपयोगकर्ता'), value: stats.counts.users, icon: Users, h: 'amber' },
                  { label: l('Kundlis', 'कुंडलियां'), value: stats.counts.kundlis, icon: Star, h: 'blue' },
                  { label: l('Horoscopes', 'राशिफल'), value: stats.counts.horoscopes, icon: Calendar, h: 'green' },
                  { label: l('Panchang Cache', 'पंचांग कैश'), value: stats.counts.panchang_cached, icon: Activity, h: 'amber' },
                ].map(s => (
                  <StatCard key={s.label} icon={s.icon} label={s.label} value={s.value} highlight={s.h as any} />
                ))}
              </div>

              <div className="grid lg:grid-cols-2 gap-6">
                <div className="border border-sacred-gold/30 rounded-xl p-5 bg-white/60">
                  <Heading as={3} variant={6} className="text-sacred-gold-dark mb-4 uppercase tracking-wider flex items-center gap-2">
                    <Users className="w-4 h-4" /> {l('Recent Users', 'हाल के उपयोगकर्ता')}
                  </Heading>
                  <div className="space-y-2">
                    {stats.recent_users.map(u => (
                      <div key={u.id} className="flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0">
                        <div>
                          <p className="text-sm font-medium text-foreground">{u.name}</p>
                          <p className="text-xs text-muted-foreground">{u.email}</p>
                        </div>
                        <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${
                          u.role === 'admin' ? 'border-red-300 text-red-500 bg-red-50'
                          : u.role === 'astrologer' ? 'border-purple-300 text-purple-600 bg-purple-50'
                          : 'border-sacred-gold/40 text-sacred-gold-dark bg-sacred-gold/5'
                        }`}>{u.role}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border border-sacred-gold/30 rounded-xl p-5 bg-white/60">
                  <Heading as={3} variant={6} className="text-sacred-gold-dark mb-4 uppercase tracking-wider flex items-center gap-2">
                    <Star className="w-4 h-4" /> {l('Recent Kundlis', 'हाल की कुंडलियां')}
                  </Heading>
                  <div className="space-y-2">
                    {stats.recent_kundlis.map(k => (
                      <div key={k.id} className="flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0">
                        <div>
                          <p className="text-sm font-medium text-foreground">{k.person_name}</p>
                          <p className="text-xs text-muted-foreground">{formatDate(k.birth_date)} · {k.email}</p>
                        </div>
                        <span className="text-xs text-muted-foreground">{formatDate(k.created_at)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* ── USERS ────────────────────────────────────────────────────────── */}
      {tab === 'users' && (
        <div>
          <p className="text-sm text-muted-foreground mb-4">
            {userTotal} {l('total users', 'कुल उपयोगकर्ता')}
          </p>
          <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-sacred-gold/20 bg-sacred-gold/5 text-left text-xs text-muted-foreground uppercase tracking-wider">
                  <th className="py-3 px-4">{l('Name', 'नाम')}</th>
                  <th className="py-3 px-4">{l('Email', 'ईमेल')}</th>
                  <th className="py-3 px-4">{l('Role', 'भूमिका')}</th>
                  <th className="py-3 px-4">{l('Active', 'सक्रिय')}</th>
                  <th className="py-3 px-4">{l('Joined', 'जुड़ने की तारीख')}</th>
                  <th className="py-3 px-4">{l('Actions', 'कार्य')}</th>
                </tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id} className="border-b border-gray-100 hover:bg-sacred-gold/4 transition-colors">
                    <td className="py-3 px-4 text-foreground font-medium">{u.name}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs">{u.email}</td>
                    <td className="py-3 px-4">
                      <select
                        value={u.role}
                        onChange={e => changeRole(u.id, e.target.value)}
                        className="bg-white border border-sacred-gold/30 text-foreground text-xs px-2 py-1 rounded-lg"
                      >
                        <option value="user">{l('user', 'यूज़र')}</option>
                        <option value="astrologer">{l('astrologer', 'ज्योतिषी')}</option>
                        <option value="admin">{l('admin', 'एडमिन')}</option>
                      </select>
                    </td>
                    <td className="py-3 px-4">
                      <button onClick={() => toggleActive(u.id)}>
                        {u.is_active
                          ? <ToggleRight className="w-5 h-5 text-green-500" />
                          : <ToggleLeft className="w-5 h-5 text-muted-foreground" />}
                      </button>
                    </td>
                    <td className="py-3 px-4 text-muted-foreground text-xs">{formatDate(u.created_at)}</td>
                    <td className="py-3 px-4">
                      <button className="text-xs text-sacred-gold-dark hover:underline">{l('View', 'देखें')}</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {userPages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-6">
              <Button variant="outline" size="sm" disabled={userPage <= 1} onClick={() => fetchUsers(userPage - 1)} className="border-sacred-gold/40">
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="text-sm text-muted-foreground">{l('Page', 'पेज')} {userPage} {l('of', 'में से')} {userPages}</span>
              <Button variant="outline" size="sm" disabled={userPage >= userPages} onClick={() => fetchUsers(userPage + 1)} className="border-sacred-gold/40">
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          )}
        </div>
      )}

      {/* ── KUNDLIS ──────────────────────────────────────────────────────── */}
      {tab === 'kundlis' && (
        <div>
          <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-sacred-gold/20 bg-sacred-gold/5 text-left text-xs text-muted-foreground uppercase tracking-wider">
                  <th className="py-3 px-4">{l('Person', 'व्यक्ति')}</th>
                  <th className="py-3 px-4">{l('Birth Date', 'जन्म तिथि')}</th>
                  <th className="py-3 px-4">{l('Place', 'स्थान')}</th>
                  <th className="py-3 px-4">{l('User', 'उपयोगकर्ता')}</th>
                  <th className="py-3 px-4">{l('Created', 'निर्मित')}</th>
                </tr>
              </thead>
              <tbody>
                {kundlis.map(k => (
                  <tr key={k.id} className="border-b border-gray-100 hover:bg-sacred-gold/4 transition-colors">
                    <td className="py-3 px-4 text-foreground font-medium">{k.person_name}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs">{formatDate(k.birth_date)} {k.birth_time}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs">{k.birth_place}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs">{k.email}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs">{formatDate(k.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {kundliPages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-6">
              <Button variant="outline" size="sm" disabled={kundliPage <= 1} onClick={() => fetchKundlis(kundliPage - 1)} className="border-sacred-gold/40">
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="text-sm text-muted-foreground">{l('Page', 'पेज')} {kundliPage} {l('of', 'में से')} {kundliPages}</span>
              <Button variant="outline" size="sm" disabled={kundliPage >= kundliPages} onClick={() => fetchKundlis(kundliPage + 1)} className="border-sacred-gold/40">
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          )}
        </div>
      )}

      {/* ── LIVE ─────────────────────────────────────────────────────────── */}
      {tab === 'live' && (
        <div className="space-y-6">
          {/* Live header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500" />
              </span>
              <span className="text-sm font-semibold text-green-700">{l('Live Dashboard', 'लाइव डैशबोर्ड')}</span>
              <span className="text-xs text-muted-foreground ml-1">{l('· auto-refresh every 5s', '· हर 5 सेकंड में ऑटो-रिफ्रेश')}</span>
            </div>
            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              {secondsSinceLast !== null && (
                <span className="flex items-center gap-1">
                  <RefreshCw className="w-3 h-3" />
                  {l('Updated', 'अपडेट')} {secondsSinceLast}{l('s ago', ' सेकंड पहले')}
                </span>
              )}
              <button
                onClick={fetchLive}
                className="flex items-center gap-1 text-sacred-gold-dark hover:underline font-medium"
              >
                <RefreshCw className="w-3 h-3" /> {l('Refresh now', 'अभी रिफ्रेश करें')}
              </button>
            </div>
          </div>

          {/* Stat cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              icon={Users}
              label={l('Online Now', 'अभी ऑनलाइन')}
              value={liveData?.active_users_count ?? '—'}
              sub={l('active in last 5 min', 'पिछले 5 मिनट में सक्रिय')}
              highlight="green"
            />
            <StatCard
              icon={Zap}
              label={l('Req / min', 'रिक्वेस्ट / मिनट')}
              value={liveData?.requests_1m ?? '—'}
              sub={liveData ? `${liveData.requests_5m} ${l('in 5 min', 'पिछले 5 मिनट में')}` : undefined}
              highlight="blue"
            />
            <StatCard
              icon={AlertTriangle}
              label={l('Error Rate', 'त्रुटि दर')}
              value={liveData ? `${liveData.error_rate_1m}%` : '—'}
              sub={l('last 60 seconds', 'पिछले 60 सेकंड')}
              highlight={liveData && liveData.error_rate_1m > 5 ? 'red' : 'green'}
            />
            <StatCard
              icon={Clock}
              label={l('Uptime', 'अपटाइम')}
              value={liveData ? formatUptime(liveData.uptime_seconds) : '—'}
              sub={l('this worker process', 'इस वर्कर प्रोसेस का')}
              highlight="amber"
            />
          </div>

          {/* Active users + Top endpoints */}
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Active Users */}
            <div className="border border-sacred-gold/25 rounded-xl overflow-hidden bg-white/60">
              <div className="flex items-center gap-2 px-5 py-3.5 border-b border-sacred-gold/20 bg-sacred-gold/5">
                <User className="w-4 h-4 text-sacred-gold-dark" />
                <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wider">
                  {l('Active Users', 'सक्रिय उपयोगकर्ता')}
                  {liveData && (
                    <span className="ml-2 text-xs font-normal text-muted-foreground normal-case">
                      ({liveData.active_users_count} {l('online', 'ऑनलाइन')})
                    </span>
                  )}
                </h3>
              </div>
              <div className="divide-y divide-gray-100 max-h-64 overflow-y-auto">
                {!liveData || liveData.active_users.length === 0 ? (
                  <div className="py-8 text-center text-sm text-muted-foreground">
                    {l('No active users yet', 'अभी कोई सक्रिय उपयोगकर्ता नहीं')}
                  </div>
                ) : (
                  liveData.active_users.map(u => (
                    <div key={u.user_id} className="flex items-center justify-between px-5 py-3 hover:bg-sacred-gold/4 transition-colors">
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-foreground truncate">{u.name}</p>
                        <p className="text-xs text-muted-foreground truncate">{u.email}</p>
                        <p className="text-xs text-blue-500 truncate mt-0.5 font-mono">{u.last_path}</p>
                      </div>
                      <span className="ml-3 text-xs text-muted-foreground whitespace-nowrap shrink-0">
                        {timeAgo(u.seconds_ago, language)}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Top Endpoints */}
            <div className="border border-sacred-gold/25 rounded-xl overflow-hidden bg-white/60">
              <div className="flex items-center gap-2 px-5 py-3.5 border-b border-sacred-gold/20 bg-sacred-gold/5">
                <TrendingUp className="w-4 h-4 text-sacred-gold-dark" />
                <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wider">
                  {l('Top Endpoints', 'शीर्ष एंडपॉइंट')} <span className="text-xs font-normal text-muted-foreground normal-case">(5 min)</span>
                </h3>
              </div>
              <div className="divide-y divide-gray-100 max-h-64 overflow-y-auto">
                {!liveData || liveData.top_endpoints.length === 0 ? (
                  <div className="py-8 text-center text-sm text-muted-foreground">{l('No traffic yet', 'अभी ट्रैफिक नहीं है')}</div>
                ) : (
                  liveData.top_endpoints.map((ep, i) => (
                    <div key={ep.path} className="flex items-center gap-3 px-5 py-3 hover:bg-sacred-gold/4 transition-colors">
                      <span className="text-xs font-bold text-muted-foreground w-4 shrink-0">{i + 1}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-mono text-foreground truncate">{ep.path}</p>
                        <div className="flex items-center gap-2 mt-0.5">
                          <div
                            className="h-1 rounded-full bg-sacred-gold/60"
                            style={{ width: `${Math.min(100, (ep.count / (liveData.top_endpoints[0]?.count || 1)) * 100)}%`, maxWidth: '80px' }}
                          />
                          <span className="text-xs text-muted-foreground">{ep.count} {l('hits', 'हिट')} · {ep.avg_ms}ms {l('avg', 'औसत')}</span>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Activity Feed */}
          <div className="border border-sacred-gold/25 rounded-xl overflow-hidden bg-white/60">
            <div className="flex items-center justify-between px-5 py-3.5 border-b border-sacred-gold/20 bg-sacred-gold/5">
              <div className="flex items-center gap-2">
                <Radio className="w-4 h-4 text-sacred-gold-dark" />
                <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wider">
                  {l('Activity Feed', 'एक्टिविटी फीड')}
                </h3>
                <span className="text-xs font-normal text-muted-foreground normal-case">{l('latest 50 requests', 'हाल की 50 रिक्वेस्ट')}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-xs text-muted-foreground flex items-center gap-1">
                  <span className="inline-block w-2 h-2 rounded-sm bg-green-400" /> 2xx
                  <span className="inline-block w-2 h-2 rounded-sm bg-orange-400 ml-2" /> 4xx
                  <span className="inline-block w-2 h-2 rounded-sm bg-red-400 ml-2" /> 5xx
                </span>
              </div>
            </div>

            <div ref={activityRef} className="font-mono text-xs divide-y divide-gray-50 max-h-[420px] overflow-y-auto">
              {!liveData || liveData.recent_activity.length === 0 ? (
                <div className="py-10 text-center text-sm text-muted-foreground">{l('No requests recorded yet', 'अभी तक कोई रिक्वेस्ट दर्ज नहीं हुई')}</div>
              ) : (
                liveData.recent_activity.map((r, i) => (
                  <div key={i} className={`flex items-center gap-3 px-4 py-2 hover:brightness-95 transition-all ${statusBg(r.status)}`}>
                    <span className="text-muted-foreground w-16 shrink-0">{r.ts_iso}</span>
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase shrink-0 ${methodColor(r.method)}`}>
                      {r.method}
                    </span>
                    <span className="flex-1 truncate text-foreground">{r.path}</span>
                    <span className={`font-bold shrink-0 w-8 text-right ${statusColor(r.status)}`}>{r.status}</span>
                    <span className="text-muted-foreground shrink-0 w-14 text-right">{r.duration_ms}ms</span>
                    <span className="text-muted-foreground shrink-0 max-w-[130px] truncate text-right">
                      {r.email ? r.email.split('@')[0] : l('anon', 'अनाम')}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Worker note */}
          <p className="text-xs text-muted-foreground text-center">
            <Globe className="w-3 h-3 inline mr-1" />
            {l('Live data reflects traffic on this worker process. With 4 workers, each handles ~25% of total traffic.', 'लाइव डेटा इस वर्कर प्रोसेस का ट्रैफिक दिखाता है। 4 वर्कर होने पर हर एक लगभग 25% ट्रैफिक संभालता है।')}
          </p>
        </div>
      )}

      {/* ── ANALYTICS ────────────────────────────────────────────────── */}
      {tab === 'analytics' && (
        <div className="space-y-6">
          {/* Stat cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard icon={Activity}  label={l('Today Views', 'आज के व्यू')} value={analyticsData?.today_views ?? '—'} sub={`${analyticsData?.today_sessions ?? '—'} ${l('sessions', 'सेशन')}`} highlight="amber" />
            <StatCard icon={Users}     label={l('This Week', 'इस सप्ताह')} value={analyticsData?.week_views ?? '—'} sub={`${analyticsData?.week_sessions ?? '—'} ${l('sessions', 'सेशन')}`} highlight="blue" />
            <StatCard icon={Calendar}  label={l('This Month', 'इस माह')} value={analyticsData?.month_views ?? '—'} sub={l('page views', 'पेज व्यू')} highlight="green" />
            <StatCard icon={TrendingUp} label={l('All Time', 'कुल')} value={analyticsData?.total_views ?? '—'} sub={`${analyticsData?.total_sessions ?? '—'} ${l('sessions', 'सेशन')}`} highlight="amber" />
          </div>

          {/* Top pages */}
          <div className="border border-sacred-gold/25 rounded-xl overflow-hidden bg-white/60">
            <div className="flex items-center gap-2 px-5 py-3.5 border-b border-sacred-gold/20 bg-sacred-gold/5">
              <TrendingUp className="w-4 h-4 text-sacred-gold-dark" />
              <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wider">
                {l('Top Pages', 'शीर्ष पेज')} <span className="text-xs font-normal text-muted-foreground normal-case">{l('(last 30 days)', '(पिछले 30 दिन)')}</span>
              </h3>
            </div>
            {!analyticsData || analyticsData.top_pages.length === 0 ? (
              <div className="py-8 text-center text-sm text-muted-foreground">{l('No page views recorded yet', 'अभी तक कोई पेज व्यू दर्ज नहीं हुआ')}</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-sacred-gold/10 text-left text-xs text-muted-foreground uppercase tracking-wider">
                      <th className="py-2.5 px-5">{l('Path', 'पाथ')}</th>
                      <th className="py-2.5 px-4 text-right">{l('Views', 'व्यू')}</th>
                      <th className="py-2.5 px-4 text-right">{l('Visitors', 'विज़िटर')}</th>
                      <th className="py-2.5 px-5 w-32">{l('Bar', 'बार')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analyticsData.top_pages.map((p) => {
                      const maxViews = analyticsData.top_pages[0]?.views || 1;
                      const pct = Math.round((p.views / maxViews) * 100);
                      return (
                        <tr key={p.path} className="border-b border-gray-50 hover:bg-sacred-gold/4 transition-colors">
                          <td className="py-2.5 px-5 font-mono text-xs text-foreground truncate max-w-[220px]">{p.path}</td>
                          <td className="py-2.5 px-4 text-right text-sm font-medium text-foreground">{p.views.toLocaleString()}</td>
                          <td className="py-2.5 px-4 text-right text-sm text-muted-foreground">{p.visitors.toLocaleString()}</td>
                          <td className="py-2.5 px-5">
                            <div className="h-2 rounded-full bg-gray-100 overflow-hidden">
                              <div className="h-full rounded-full bg-sacred-gold/70" style={{ width: `${pct}%` }} />
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Hourly chart — today */}
          <div className="border border-sacred-gold/25 rounded-xl overflow-hidden bg-white/60">
            <div className="flex items-center gap-2 px-5 py-3.5 border-b border-sacred-gold/20 bg-sacred-gold/5">
              <Clock className="w-4 h-4 text-sacred-gold-dark" />
              <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wider">
                {l('Hourly Traffic', 'घंटावार ट्रैफिक')} <span className="text-xs font-normal text-muted-foreground normal-case">{l('(today, 24h)', '(आज, 24 घंटे)')}</span>
              </h3>
            </div>
            <div className="px-5 py-4">
              {!analyticsData ? (
                <div className="text-center text-sm text-muted-foreground py-4">{l('No data', 'कोई डेटा नहीं')}</div>
              ) : (() => {
                const maxH = Math.max(...analyticsData.hourly_today.map(h => h.views), 1);
                return (
                  <div className="flex items-end gap-0.5 h-24">
                    {analyticsData.hourly_today.map(h => (
                      <div key={h.hour} className="flex-1 flex flex-col items-center gap-0.5 group relative">
                        <div
                          className="w-full rounded-t bg-sacred-gold/60 group-hover:bg-sacred-gold transition-colors"
                          style={{ height: `${Math.round((h.views / maxH) * 80)}px`, minHeight: h.views > 0 ? '2px' : '0' }}
                        />
                        {h.hour % 6 === 0 && (
                          <span className="text-[9px] text-muted-foreground absolute -bottom-4">{h.hour}{t('auto.h')}</span>
                        )}
                      </div>
                    ))}
                  </div>
                );
              })()}
            </div>
          </div>

          {/* 30-day sparkline */}
          <div className="border border-sacred-gold/25 rounded-xl overflow-hidden bg-white/60">
            <div className="flex items-center gap-2 px-5 py-3.5 border-b border-sacred-gold/20 bg-sacred-gold/5">
              <TrendingUp className="w-4 h-4 text-sacred-gold-dark" />
              <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wider">
                {l('Daily Traffic', 'दैनिक ट्रैफिक')} <span className="text-xs font-normal text-muted-foreground normal-case">{l('(last 30 days)', '(पिछले 30 दिन)')}</span>
              </h3>
            </div>
            <div className="px-5 py-4">
              {!analyticsData || analyticsData.daily_last_30.length === 0 ? (
                <div className="text-center text-sm text-muted-foreground py-4">{l('No data yet', 'अभी डेटा नहीं है')}</div>
              ) : (() => {
                const maxD = Math.max(...analyticsData.daily_last_30.map(d => d.views), 1);
                return (
                  <div className="flex items-end gap-0.5 h-20">
                    {analyticsData.daily_last_30.map(d => (
                      <div key={d.day} className="flex-1 flex flex-col items-center group relative" title={`${d.day}: ${d.views} ${l('views', 'व्यू')}`}>
                        <div
                          className="w-full rounded-t bg-blue-400/60 group-hover:bg-blue-500 transition-colors"
                          style={{ height: `${Math.round((d.views / maxD) * 72)}px`, minHeight: d.views > 0 ? '2px' : '0' }}
                        />
                      </div>
                    ))}
                  </div>
                );
              })()}
              <div className="flex justify-between mt-2 text-[10px] text-muted-foreground">
                <span>{analyticsData?.daily_last_30?.[0]?.day ?? ''}</span>
                <span>{analyticsData?.daily_last_30?.[analyticsData.daily_last_30.length - 1]?.day ?? ''}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── FEEDBACK ─────────────────────────────────────────────────── */}
      {tab === 'feedback' && (
        <div className="space-y-6">

          {/* Word cloud — OPEN feedback only */}
          <div className="border border-sacred-gold/25 rounded-xl overflow-hidden bg-white/60">
            <div className="flex items-center justify-between px-5 py-3.5 border-b border-sacred-gold/20 bg-sacred-gold/5">
              <div className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4 text-sacred-gold-dark" />
                <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wider">
                  {l('Word Cloud', 'वर्ड क्लाउड')}
                </h3>
                <span className="text-xs font-normal text-amber-600 normal-case bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-full">
                  {l('Open issues only', 'केवल खुले मुद्दे')}
                </span>
              </div>
              <button
                onClick={fetchWordCloud}
                className="flex items-center gap-1 text-xs text-sacred-gold-dark hover:underline font-medium"
              >
                <RefreshCw className="w-3 h-3" /> {l('Refresh', 'रिफ्रेश')}
              </button>
            </div>
            <WordCloud words={wordCloud} />
          </div>

          {/* Filter bar */}
          <div className="flex flex-wrap items-center gap-3">
            <Filter className="w-4 h-4 text-muted-foreground shrink-0" />
            <div className="flex items-center gap-2">
              <label className="text-xs text-muted-foreground font-medium">{l('Status', 'स्थिति')}</label>
              <select
                value={feedbackFilterStatus}
                onChange={e => {
                  setFeedbackFilterStatus(e.target.value);
                  fetchFeedback(1, e.target.value, feedbackFilterAction);
                }}
                className="text-xs border border-sacred-gold/30 rounded-lg px-3 py-1.5 bg-white text-foreground focus:outline-none focus:ring-1 focus:ring-sacred-gold/40"
              >
                <option value="">{l('All', 'सभी')}</option>
                <option value="open">{l('Open', 'खुला')}</option>
                <option value="closed">{l('Resolved', 'सुलझा')}</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <label className="text-xs text-muted-foreground font-medium">{l('Action', 'कार्यवाही')}</label>
              <select
                value={feedbackFilterAction}
                onChange={e => {
                  setFeedbackFilterAction(e.target.value);
                  fetchFeedback(1, feedbackFilterStatus, e.target.value);
                }}
                className="text-xs border border-sacred-gold/30 rounded-lg px-3 py-1.5 bg-white text-foreground focus:outline-none focus:ring-1 focus:ring-sacred-gold/40"
              >
                <option value="">{l('All', 'सभी')}</option>
                <option value="NR">{l('Not Reviewed', 'समीक्षा नहीं')}</option>
                <option value="yes">{l('Action Taken', 'कार्यवाही हुई')}</option>
                <option value="no">{l('No Action', 'कोई कार्यवाही नहीं')}</option>
              </select>
            </div>
            <span className="text-xs text-muted-foreground ml-auto">
              {feedbackTotal} {l(feedbackTotal !== 1 ? 'results' : 'result', feedbackTotal !== 1 ? 'परिणाम' : 'परिणाम')}
            </span>
          </div>

          {/* Table */}
          <div className="border border-sacred-gold/20 rounded-xl overflow-hidden bg-white/60">
            {feedbackItems.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-muted-foreground">
                <MessageSquare className="w-8 h-8 text-gray-200 mb-3" />
                <p className="text-sm">{l('No feedback yet', 'अभी कोई फीडबैक नहीं')}</p>
                <p className="text-xs text-muted-foreground mt-1">{l('Submissions will appear here', 'सबमिशन यहां दिखेंगे')}</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-sacred-gold/20 bg-sacred-gold/5 text-left text-xs text-muted-foreground uppercase tracking-wider">
                      <th className="py-3 px-4">{l('User', 'उपयोगकर्ता')}</th>
                      <th className="py-3 px-4">{l('Ratings', 'रेटिंग्स')}</th>
                      <th className="py-3 px-4">{l('Feedback', 'फीडबैक')}</th>
                      <th className="py-3 px-4">{l('Status', 'स्थिति')}</th>
                      <th className="py-3 px-4">{l('Action Taken', 'कार्यवाही हुई')}</th>
                      <th className="py-3 px-4">{l('Admin Remarks', 'एडमिन टिप्पणी')}</th>
                      <th className="py-3 px-4">{l('Date', 'तिथि')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {feedbackItems.map(item => (
                      <FeedbackRow
                        key={item.id}
                        item={item}
                        onUpdated={(id, patch) =>
                          setFeedbackItems(prev =>
                            prev.map(f => f.id === id ? { ...f, ...patch } : f)
                          )
                        }
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Pagination */}
          {feedbackPages > 1 && (
            <div className="flex items-center justify-center gap-4">
              <Button variant="outline" size="sm" disabled={feedbackPage <= 1}
                onClick={() => fetchFeedback(feedbackPage - 1, feedbackFilterStatus, feedbackFilterAction)}
                className="border-sacred-gold/40">
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="text-sm text-muted-foreground">{l('Page', 'पेज')} {feedbackPage} {l('of', 'में से')} {feedbackPages}</span>
              <Button variant="outline" size="sm" disabled={feedbackPage >= feedbackPages}
                onClick={() => fetchFeedback(feedbackPage + 1, feedbackFilterStatus, feedbackFilterAction)}
                className="border-sacred-gold/40">
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
