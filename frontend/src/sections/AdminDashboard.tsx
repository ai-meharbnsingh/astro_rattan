import { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users, Star, Calendar, Activity, Shield, ChevronRight, ChevronLeft,
  ToggleLeft, ToggleRight, Zap, AlertTriangle, Clock, Radio,
  TrendingUp, Globe, User, RefreshCw,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api, formatDate } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

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

function timeAgo(seconds: number): string {
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
  return 'text-gray-600 bg-gray-50';
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
  const [tab, setTab] = useState<'overview' | 'users' | 'kundlis' | 'live'>('overview');

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

  // live
  const [liveData, setLiveData] = useState<LiveData | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [tickMs, setTickMs] = useState(0);
  const liveInterval = useRef<ReturnType<typeof setInterval> | null>(null);
  const activityRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (user?.role !== 'admin') { navigate('/'); return; }
    fetchStats();
  }, [user]);

  // Tick to update "Xs ago" on live panel without refetching
  useEffect(() => {
    const id = setInterval(() => setTickMs(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const fetchStats = async () => {
    try {
      const data = await api.get('/api/admin/stats');
      setStats(data);
    } catch (e) { setError('Failed to load stats'); }
    setLoading(false);
  };

  const fetchUsers = async (page = 1) => {
    try {
      const data = await api.get(`/api/admin/users?page=${page}&limit=15`);
      setUsers(data.users); setUserPage(data.page);
      setUserPages(data.pages); setUserTotal(data.total);
    } catch (e) { console.error(e); }
  };

  const fetchKundlis = async (page = 1) => {
    try {
      const data = await api.get(`/api/admin/kundlis?page=${page}&limit=15`);
      setKundlis(data.kundlis); setKundliPage(data.page); setKundliPages(data.pages);
    } catch (e) { console.error(e); }
  };

  const fetchLive = useCallback(async () => {
    try {
      const data = await api.get('/api/admin/live');
      setLiveData(data);
      setLastUpdated(new Date());
    } catch (e) { console.error(e); }
  }, []);

  useEffect(() => {
    if (tab === 'users') fetchUsers();
    if (tab === 'kundlis') fetchKundlis();
    if (tab === 'live') {
      fetchLive();
      liveInterval.current = setInterval(fetchLive, 5000);
    }
    return () => {
      if (liveInterval.current) clearInterval(liveInterval.current);
    };
  }, [tab]);

  const changeRole = async (userId: string, role: string) => {
    try { await api.patch(`/api/admin/users/${userId}/role`, { role }); fetchUsers(userPage); }
    catch (e) { console.error(e); }
  };

  const toggleActive = async (userId: string) => {
    try { await api.patch(`/api/admin/users/${userId}/toggle-active`, {}); fetchUsers(userPage); }
    catch (e) { console.error(e); }
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
    { key: 'overview', label: 'Overview' },
    { key: 'users',    label: 'Users' },
    { key: 'kundlis',  label: 'Kundlis' },
    { key: 'live',     label: 'Live' },
  ] as const;

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-7xl mx-auto">
      {/* Page header */}
      <div className="flex items-center gap-3 mb-8">
        <Shield className="w-8 h-8 text-sacred-gold-dark" />
        <div>
          <h1 className="text-2xl font-sans font-semibold text-cosmic-text">Admin Dashboard</h1>
          <p className="text-xs text-gray-500 mt-0.5">astrorattan.com management panel</p>
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
                : 'text-gray-500 hover:text-cosmic-text hover:bg-gray-50 rounded-t-lg'
            }`}
          >
            {t.label === 'Live' && (
              <span className="inline-flex items-center gap-1.5">
                <span className="relative flex h-2 w-2">
                  <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${tab === 'live' ? 'bg-green-400' : 'bg-gray-400'}`} />
                  <span className={`relative inline-flex rounded-full h-2 w-2 ${tab === 'live' ? 'bg-green-500' : 'bg-gray-400'}`} />
                </span>
                Live
              </span>
            )}
            {t.label !== 'Live' && t.label}
          </button>
        ))}
      </div>

      {/* ── OVERVIEW ─────────────────────────────────────────────────────── */}
      {tab === 'overview' && (
        <div>
          {!stats ? (
            <div className="text-center py-16 border border-dashed border-sacred-gold/40 rounded-xl">
              <Shield className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-cosmic-text font-medium">No data yet</p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                {[
                  { label: 'Total Users',  value: stats.counts.users,           icon: Users,    h: 'amber' },
                  { label: 'Kundlis',      value: stats.counts.kundlis,          icon: Star,     h: 'blue' },
                  { label: 'Horoscopes',   value: stats.counts.horoscopes,       icon: Calendar, h: 'green' },
                  { label: 'Panchang Cache', value: stats.counts.panchang_cached, icon: Activity, h: 'amber' },
                ].map(s => (
                  <StatCard key={s.label} icon={s.icon} label={s.label} value={s.value} highlight={s.h as any} />
                ))}
              </div>

              <div className="grid lg:grid-cols-2 gap-6">
                <div className="border border-sacred-gold/30 rounded-xl p-5 bg-white/60">
                  <h3 className="font-semibold text-sacred-gold-dark mb-4 text-sm uppercase tracking-wider flex items-center gap-2">
                    <Users className="w-4 h-4" /> Recent Users
                  </h3>
                  <div className="space-y-2">
                    {stats.recent_users.map(u => (
                      <div key={u.id} className="flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0">
                        <div>
                          <p className="text-sm font-medium text-cosmic-text">{u.name}</p>
                          <p className="text-xs text-gray-400">{u.email}</p>
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
                  <h3 className="font-semibold text-sacred-gold-dark mb-4 text-sm uppercase tracking-wider flex items-center gap-2">
                    <Star className="w-4 h-4" /> Recent Kundlis
                  </h3>
                  <div className="space-y-2">
                    {stats.recent_kundlis.map(k => (
                      <div key={k.id} className="flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0">
                        <div>
                          <p className="text-sm font-medium text-cosmic-text">{k.person_name}</p>
                          <p className="text-xs text-gray-400">{formatDate(k.birth_date)} · {k.email}</p>
                        </div>
                        <span className="text-xs text-gray-400">{formatDate(k.created_at)}</span>
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
          <p className="text-sm text-gray-500 mb-4">{userTotal} total users</p>
          <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-sacred-gold/20 bg-sacred-gold/5 text-left text-xs text-gray-500 uppercase tracking-wider">
                  <th className="py-3 px-4">Name</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Active</th>
                  <th className="py-3 px-4">Joined</th>
                  <th className="py-3 px-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id} className="border-b border-gray-100 hover:bg-sacred-gold/4 transition-colors">
                    <td className="py-3 px-4 text-cosmic-text font-medium">{u.name}</td>
                    <td className="py-3 px-4 text-gray-500 text-xs">{u.email}</td>
                    <td className="py-3 px-4">
                      <select
                        value={u.role}
                        onChange={e => changeRole(u.id, e.target.value)}
                        className="bg-white border border-sacred-gold/30 text-cosmic-text text-xs px-2 py-1 rounded-lg"
                      >
                        <option value="user">user</option>
                        <option value="astrologer">astrologer</option>
                        <option value="admin">admin</option>
                      </select>
                    </td>
                    <td className="py-3 px-4">
                      <button onClick={() => toggleActive(u.id)}>
                        {u.is_active
                          ? <ToggleRight className="w-5 h-5 text-green-500" />
                          : <ToggleLeft className="w-5 h-5 text-gray-300" />}
                      </button>
                    </td>
                    <td className="py-3 px-4 text-gray-400 text-xs">{formatDate(u.created_at)}</td>
                    <td className="py-3 px-4">
                      <button className="text-xs text-sacred-gold-dark hover:underline">View</button>
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
              <span className="text-sm text-gray-500">Page {userPage} of {userPages}</span>
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
                <tr className="border-b border-sacred-gold/20 bg-sacred-gold/5 text-left text-xs text-gray-500 uppercase tracking-wider">
                  <th className="py-3 px-4">Person</th>
                  <th className="py-3 px-4">Birth Date</th>
                  <th className="py-3 px-4">Place</th>
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Created</th>
                </tr>
              </thead>
              <tbody>
                {kundlis.map(k => (
                  <tr key={k.id} className="border-b border-gray-100 hover:bg-sacred-gold/4 transition-colors">
                    <td className="py-3 px-4 text-cosmic-text font-medium">{k.person_name}</td>
                    <td className="py-3 px-4 text-gray-500 text-xs">{formatDate(k.birth_date)} {k.birth_time}</td>
                    <td className="py-3 px-4 text-gray-500 text-xs">{k.birth_place}</td>
                    <td className="py-3 px-4 text-gray-500 text-xs">{k.email}</td>
                    <td className="py-3 px-4 text-gray-400 text-xs">{formatDate(k.created_at)}</td>
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
              <span className="text-sm text-gray-500">Page {kundliPage} of {kundliPages}</span>
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
              <span className="text-sm font-semibold text-green-700">Live Dashboard</span>
              <span className="text-xs text-gray-400 ml-1">· auto-refresh every 5s</span>
            </div>
            <div className="flex items-center gap-3 text-xs text-gray-400">
              {secondsSinceLast !== null && (
                <span className="flex items-center gap-1">
                  <RefreshCw className="w-3 h-3" />
                  Updated {secondsSinceLast}s ago
                </span>
              )}
              <button
                onClick={fetchLive}
                className="flex items-center gap-1 text-sacred-gold-dark hover:underline font-medium"
              >
                <RefreshCw className="w-3 h-3" /> Refresh now
              </button>
            </div>
          </div>

          {/* Stat cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              icon={Users}
              label="Online Now"
              value={liveData?.active_users_count ?? '—'}
              sub="active in last 5 min"
              highlight="green"
            />
            <StatCard
              icon={Zap}
              label="Req / min"
              value={liveData?.requests_1m ?? '—'}
              sub={liveData ? `${liveData.requests_5m} in 5 min` : undefined}
              highlight="blue"
            />
            <StatCard
              icon={AlertTriangle}
              label="Error Rate"
              value={liveData ? `${liveData.error_rate_1m}%` : '—'}
              sub="last 60 seconds"
              highlight={liveData && liveData.error_rate_1m > 5 ? 'red' : 'green'}
            />
            <StatCard
              icon={Clock}
              label="Uptime"
              value={liveData ? formatUptime(liveData.uptime_seconds) : '—'}
              sub="this worker process"
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
                  Active Users
                  {liveData && (
                    <span className="ml-2 text-xs font-normal text-gray-400 normal-case">
                      ({liveData.active_users_count} online)
                    </span>
                  )}
                </h3>
              </div>
              <div className="divide-y divide-gray-100 max-h-64 overflow-y-auto">
                {!liveData || liveData.active_users.length === 0 ? (
                  <div className="py-8 text-center text-sm text-gray-400">
                    No active users yet
                  </div>
                ) : (
                  liveData.active_users.map(u => (
                    <div key={u.user_id} className="flex items-center justify-between px-5 py-3 hover:bg-sacred-gold/4 transition-colors">
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-cosmic-text truncate">{u.name}</p>
                        <p className="text-xs text-gray-400 truncate">{u.email}</p>
                        <p className="text-xs text-blue-500 truncate mt-0.5 font-mono">{u.last_path}</p>
                      </div>
                      <span className="ml-3 text-xs text-gray-400 whitespace-nowrap shrink-0">
                        {timeAgo(u.seconds_ago)}
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
                  Top Endpoints <span className="text-xs font-normal text-gray-400 normal-case">(5 min)</span>
                </h3>
              </div>
              <div className="divide-y divide-gray-100 max-h-64 overflow-y-auto">
                {!liveData || liveData.top_endpoints.length === 0 ? (
                  <div className="py-8 text-center text-sm text-gray-400">No traffic yet</div>
                ) : (
                  liveData.top_endpoints.map((ep, i) => (
                    <div key={ep.path} className="flex items-center gap-3 px-5 py-3 hover:bg-sacred-gold/4 transition-colors">
                      <span className="text-xs font-bold text-gray-300 w-4 shrink-0">{i + 1}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-mono text-cosmic-text truncate">{ep.path}</p>
                        <div className="flex items-center gap-2 mt-0.5">
                          <div
                            className="h-1 rounded-full bg-sacred-gold/60"
                            style={{ width: `${Math.min(100, (ep.count / (liveData.top_endpoints[0]?.count || 1)) * 100)}%`, maxWidth: '80px' }}
                          />
                          <span className="text-xs text-gray-400">{ep.count} hits · {ep.avg_ms}ms avg</span>
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
                  Activity Feed
                </h3>
                <span className="text-xs font-normal text-gray-400 normal-case">latest 50 requests</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-xs text-gray-400 flex items-center gap-1">
                  <span className="inline-block w-2 h-2 rounded-sm bg-green-400" /> 2xx
                  <span className="inline-block w-2 h-2 rounded-sm bg-orange-400 ml-2" /> 4xx
                  <span className="inline-block w-2 h-2 rounded-sm bg-red-400 ml-2" /> 5xx
                </span>
              </div>
            </div>

            <div ref={activityRef} className="font-mono text-xs divide-y divide-gray-50 max-h-[420px] overflow-y-auto">
              {!liveData || liveData.recent_activity.length === 0 ? (
                <div className="py-10 text-center text-sm text-gray-400">No requests recorded yet</div>
              ) : (
                liveData.recent_activity.map((r, i) => (
                  <div key={i} className={`flex items-center gap-3 px-4 py-2 hover:brightness-95 transition-all ${statusBg(r.status)}`}>
                    <span className="text-gray-400 w-16 shrink-0">{r.ts_iso}</span>
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase shrink-0 ${methodColor(r.method)}`}>
                      {r.method}
                    </span>
                    <span className="flex-1 truncate text-cosmic-text">{r.path}</span>
                    <span className={`font-bold shrink-0 w-8 text-right ${statusColor(r.status)}`}>{r.status}</span>
                    <span className="text-gray-400 shrink-0 w-14 text-right">{r.duration_ms}ms</span>
                    <span className="text-gray-400 shrink-0 max-w-[130px] truncate text-right">
                      {r.email ? r.email.split('@')[0] : 'anon'}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Worker note */}
          <p className="text-xs text-gray-400 text-center">
            <Globe className="w-3 h-3 inline mr-1" />
            Live data reflects traffic on this worker process. With 4 workers, each handles ~25% of total traffic.
          </p>
        </div>
      )}
    </div>
  );
}
