import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Star, Calendar, Activity, Shield, ChevronRight, ChevronLeft, ToggleLeft, ToggleRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Stats {
  counts: { users: number; kundlis: number; horoscopes: number; panchang_cached: number };
  recent_users: Array<{ id: string; email: string; name: string; role: string; created_at: string }>;
  recent_kundlis: Array<{ id: string; person_name: string; birth_date: string; created_at: string; email: string }>;
}

interface UserRow {
  id: string; email: string; name: string; role: string; phone: string | null;
  city: string | null; is_active: number; created_at: string;
}

export default function AdminDashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [tab, setTab] = useState<'overview' | 'users' | 'kundlis'>('overview');
  const [stats, setStats] = useState<Stats | null>(null);
  const [users, setUsers] = useState<UserRow[]>([]);
  const [userPage, setUserPage] = useState(1);
  const [userPages, setUserPages] = useState(1);
  const [userTotal, setUserTotal] = useState(0);
  const [kundlis, setKundlis] = useState<any[]>([]);
  const [kundliPage, setKundliPage] = useState(1);
  const [kundliPages, setKundliPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user?.role !== 'admin') { navigate('/'); return; }
    fetchStats();
  }, [user]);

  const fetchStats = async () => {
    try {
      const data = await api.get('/api/admin/stats');
      setStats(data);
    } catch (e) { setError('Failed to load stats'); console.error(e); }
    setLoading(false);
  };

  const fetchUsers = async (page = 1) => {
    try {
      const data = await api.get(`/api/admin/users?page=${page}&limit=15`);
      setUsers(data.users);
      setUserPage(data.page);
      setUserPages(data.pages);
      setUserTotal(data.total);
    } catch (e) { console.error(e); }
  };

  const fetchKundlis = async (page = 1) => {
    try {
      const data = await api.get(`/api/admin/kundlis?page=${page}&limit=15`);
      setKundlis(data.kundlis);
      setKundliPage(data.page);
      setKundliPages(data.pages);
    } catch (e) { console.error(e); }
  };

  const changeRole = async (userId: string, role: string) => {
    try {
      await api.patch(`/api/admin/users/${userId}/role`, { role });
      fetchUsers(userPage);
    } catch (e) { console.error(e); }
  };

  const toggleActive = async (userId: string) => {
    try {
      await api.patch(`/api/admin/users/${userId}/toggle-active`, {});
      fetchUsers(userPage);
    } catch (e) { console.error(e); }
  };

  useEffect(() => {
    if (tab === 'users') fetchUsers();
    if (tab === 'kundlis') fetchKundlis();
  }, [tab]);

  if (loading) return <div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-600" /></div>;
  if (error) return <div className="text-center py-20 text-red-400">{error}</div>;

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-7xl mx-auto">
      <div className="flex items-center gap-3 mb-8">
        <Shield className="w-8 h-8 text-sacred-gold-dark" />
        <h1 className="text-3xl font-cinzel text-cosmic-text">Admin Dashboard</h1>
      </div>

      {/* Tab bar */}
      <div className="flex gap-2 mb-8 border-b border-sacred-gold/20 pb-2">
        {(['overview', 'users', 'kundlis'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-cinzel uppercase tracking-wider transition-colors ${tab === t ? 'text-sacred-gold-dark border-b-2 border-sacred-gold' : 'text-cosmic-text/70 hover:text-cosmic-text/80'}`}>
            {t}
          </button>
        ))}
      </div>

      {/* Overview */}
      {tab === 'overview' && stats && (
        <div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {[
              { label: 'Users', value: stats.counts.users, icon: Users },
              { label: 'Kundlis', value: stats.counts.kundlis, icon: Star },
              { label: 'Horoscopes', value: stats.counts.horoscopes, icon: Calendar },
              { label: 'Panchang Cached', value: stats.counts.panchang_cached, icon: Activity },
            ].map(s => (
              <div key={s.label} className="border border-sacred-gold/20 p-5 bg-cosmic-bg">
                <s.icon className="w-5 h-5 text-sacred-gold-dark mb-2" />
                <p className="text-2xl font-cinzel text-sacred-gold-dark">{s.value}</p>
                <p className="text-xs text-cosmic-text/70 uppercase tracking-wider">{s.label}</p>
              </div>
            ))}
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            <div className="border border-sacred-gold/20 p-5">
              <h3 className="font-cinzel text-sacred-gold-dark mb-4 uppercase text-sm tracking-wider">Recent Users</h3>
              <div className="space-y-2">
                {stats.recent_users.map(u => (
                  <div key={u.id} className="flex items-center justify-between py-2 border-b border-sacred-gold/10 last:border-0">
                    <div>
                      <p className="text-sm text-cosmic-text">{u.name}</p>
                      <p className="text-xs text-cosmic-text/70">{u.email}</p>
                    </div>
                    <span className={`text-xs px-2 py-0.5 border ${u.role === 'admin' ? 'border-red-500/30 text-red-400' : u.role === 'astrologer' ? 'border-purple-500/30 text-purple-400' : 'border-sacred-gold/30 text-sacred-gold-dark'}`}>
                      {u.role}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="border border-sacred-gold/20 p-5">
              <h3 className="font-cinzel text-sacred-gold-dark mb-4 uppercase text-sm tracking-wider">Recent Kundlis</h3>
              <div className="space-y-2">
                {stats.recent_kundlis.map(k => (
                  <div key={k.id} className="flex items-center justify-between py-2 border-b border-sacred-gold/10 last:border-0">
                    <div>
                      <p className="text-sm text-cosmic-text">{k.person_name}</p>
                      <p className="text-xs text-cosmic-text/70">{k.birth_date} &middot; {k.email}</p>
                    </div>
                    <span className="text-xs text-cosmic-text/60">{new Date(k.created_at).toLocaleDateString()}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Users */}
      {tab === 'users' && (
        <div>
          <p className="text-sm text-cosmic-text/70 mb-4">{userTotal} total users</p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-sacred-gold/20 text-left text-xs text-cosmic-text/70 uppercase tracking-wider">
                  <th className="py-3 pr-4">Name</th>
                  <th className="py-3 pr-4">Email</th>
                  <th className="py-3 pr-4">Role</th>
                  <th className="py-3 pr-4">Active</th>
                  <th className="py-3 pr-4">Joined</th>
                  <th className="py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id} className="border-b border-sacred-gold/10 hover:bg-sacred-gold-dark/5">
                    <td className="py-3 pr-4 text-cosmic-text">{u.name}</td>
                    <td className="py-3 pr-4 text-cosmic-text/70">{u.email}</td>
                    <td className="py-3 pr-4">
                      <select value={u.role} onChange={e => changeRole(u.id, e.target.value)}
                        className="bg-transparent border border-sacred-gold/20 text-cosmic-text text-xs px-2 py-1">
                        <option value="user">user</option>
                        <option value="astrologer">astrologer</option>
                        <option value="admin">admin</option>
                      </select>
                    </td>
                    <td className="py-3 pr-4">
                      <button onClick={() => toggleActive(u.id)} className="text-cosmic-text/60 hover:text-sacred-gold-dark">
                        {u.is_active ? <ToggleRight className="w-5 h-5 text-green-500" /> : <ToggleLeft className="w-5 h-5 text-red-400" />}
                      </button>
                    </td>
                    <td className="py-3 pr-4 text-cosmic-text/70 text-xs">{new Date(u.created_at).toLocaleDateString()}</td>
                    <td className="py-3">
                      <button onClick={() => {}} className="text-xs text-sacred-gold-dark hover:underline">View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {userPages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-6">
              <Button variant="outline" size="sm" disabled={userPage <= 1} onClick={() => fetchUsers(userPage - 1)} className="border-sacred-gold/20">
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="text-sm text-cosmic-text/60">Page {userPage} of {userPages}</span>
              <Button variant="outline" size="sm" disabled={userPage >= userPages} onClick={() => fetchUsers(userPage + 1)} className="border-sacred-gold/20">
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          )}
        </div>
      )}

      {/* Kundlis */}
      {tab === 'kundlis' && (
        <div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-sacred-gold/20 text-left text-xs text-cosmic-text/70 uppercase tracking-wider">
                  <th className="py-3 pr-4">Person</th>
                  <th className="py-3 pr-4">Birth Date</th>
                  <th className="py-3 pr-4">Place</th>
                  <th className="py-3 pr-4">User</th>
                  <th className="py-3">Created</th>
                </tr>
              </thead>
              <tbody>
                {kundlis.map(k => (
                  <tr key={k.id} className="border-b border-sacred-gold/10 hover:bg-sacred-gold-dark/5">
                    <td className="py-3 pr-4 text-cosmic-text">{k.person_name}</td>
                    <td className="py-3 pr-4 text-cosmic-text/70">{k.birth_date} {k.birth_time}</td>
                    <td className="py-3 pr-4 text-cosmic-text/70 text-xs">{k.birth_place}</td>
                    <td className="py-3 pr-4 text-cosmic-text/70 text-xs">{k.email}</td>
                    <td className="py-3 text-cosmic-text/70 text-xs">{new Date(k.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {kundliPages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-6">
              <Button variant="outline" size="sm" disabled={kundliPage <= 1} onClick={() => fetchKundlis(kundliPage - 1)} className="border-sacred-gold/20">
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="text-sm text-cosmic-text/60">Page {kundliPage} of {kundliPages}</span>
              <Button variant="outline" size="sm" disabled={kundliPage >= kundliPages} onClick={() => fetchKundlis(kundliPage + 1)} className="border-sacred-gold/20">
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
