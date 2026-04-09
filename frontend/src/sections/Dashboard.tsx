import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Plus, Search, BookOpen, ChevronRight, User, Shield, Star, BarChart3 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api, formatDate } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Client {
  id: string;
  name: string;
  phone: string | null;
  birth_date: string | null;
  birth_place: string | null;
  kundli_count: number;
}

interface AdminStats {
  counts: { users: number; astrologers: number; clients: number; kundlis: number };
  astrologers: Array<{ id: string; name: string; email: string; role: string; client_count: number; kundli_count: number; created_at: string }>;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const { t } = useTranslation();
  const isAdmin = user?.role === 'admin';

  // Astrologer state
  const [clients, setClients] = useState<Client[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  // Admin state
  const [adminStats, setAdminStats] = useState<AdminStats | null>(null);

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return; }
    if (isAdmin) {
      fetchAdminStats();
    }
    fetchClients();
  }, [isAuthenticated, isAdmin]);

  const fetchClients = async (q = '') => {
    setLoading(true);
    try {
      const data = await api.get(`/api/clients?search=${encodeURIComponent(q)}`);
      setClients(data);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const fetchAdminStats = async () => {
    try {
      const data = await api.get('/api/admin/stats');
      setAdminStats(data);
    } catch (e) { console.error(e); }
  };

  const handleSearch = (val: string) => {
    setSearch(val);
    fetchClients(val);
  };

  // ─── ADMIN DASHBOARD ─────────────────────────────────────
  if (isAdmin && adminStats) {
    return (
      <div className="min-h-screen pt-24 pb-16 px-4 max-w-6xl mx-auto">
        <div className="flex items-center justify-end mb-8">
          <div className="flex gap-2">
            <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold text-xs font-cinzel uppercase tracking-wider px-4 py-2 rounded-none">
              <Plus className="w-4 h-4 mr-1" /> New Kundli
            </Button>
            <Button onClick={() => navigate('/admin')} variant="outline" className="border-sacred-gold text-sacred-gold-dark text-xs font-cinzel uppercase tracking-wider px-4 py-2 rounded-none">
              <BarChart3 className="w-4 h-4 mr-1" /> Full Admin
            </Button>
          </div>
        </div>

        {/* Summary Boxes */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Astrologers', value: adminStats.counts.astrologers, icon: Star, color: 'text-amber-500' },
            { label: 'Clients Added', value: adminStats.counts.clients, icon: Users, color: 'text-blue-500' },
            { label: 'Total Kundlis', value: adminStats.counts.kundlis, icon: BarChart3, color: 'text-green-500' },
            { label: 'Registered Users', value: adminStats.counts.users, icon: User, color: 'text-purple-500' },
          ].map(s => (
            <div key={s.label} className="border border-sacred-gold p-5 bg-cosmic-bg">
              <s.icon className={`w-5 h-5 ${s.color} mb-2`} />
              <p className="text-3xl font-cinzel text-cosmic-text font-bold">{s.value}</p>
              <p className="text-xs text-cosmic-text uppercase tracking-wider mt-1">{s.label}</p>
            </div>
          ))}
        </div>

        {/* Astrologers List */}
        <h2 className="text-sm font-cinzel text-cosmic-text uppercase tracking-wider mb-4">Astrologers & Their Clients</h2>
        <div className="space-y-3 mb-10">
          {adminStats.astrologers.map(astro => (
            <div key={astro.id} className="border border-sacred-gold/20 p-4 bg-cosmic-bg">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-sacred-gold-dark border border-sacred-gold flex items-center justify-center">
                    <Star className="w-5 h-5 text-sacred-gold-dark" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-cosmic-text">{astro.name}</p>
                    <p className="text-xs text-cosmic-text">{astro.email}</p>
                  </div>
                </div>
                <div className="flex gap-6 text-right">
                  <div>
                    <p className="text-lg font-cinzel text-cosmic-text font-bold">{astro.client_count}</p>
                    <p className="text-xs text-cosmic-text">Clients</p>
                  </div>
                  <div>
                    <p className="text-lg font-cinzel text-cosmic-text font-bold">{astro.kundli_count}</p>
                    <p className="text-xs text-cosmic-text">Kundlis</p>
                  </div>
                  <span className={`self-center text-xs px-2 py-0.5 border ${astro.role === 'admin' ? 'border-red-500 text-red-500' : 'border-purple-500 text-purple-500'}`}>
                    {astro.role}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Admin's own clients below */}
        <h2 className="text-sm font-cinzel text-cosmic-text uppercase tracking-wider mb-4">My Clients</h2>
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cosmic-text" />
          <Input type="text" value={search} onChange={e => handleSearch(e.target.value)}
            placeholder={t('dashboard.searchPlaceholder')} className="pl-10 bg-cosmic-bg border-sacred-gold/20 text-cosmic-text rounded-none" />
        </div>
        {renderClientList()}
      </div>
    );
  }

  // ─── ASTROLOGER DASHBOARD ────────────────────────────────
  function renderClientList() {
    if (loading) {
      return <div className="flex justify-center py-12"><div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-600" /></div>;
    }
    if (clients.length === 0) {
      return (
        <div className="text-center py-16 border border-dashed border-sacred-gold">
          <User className="w-12 h-12 text-cosmic-text mx-auto mb-4" />
          <p className="text-cosmic-text mb-2">{t('dashboard.noClients')}</p>
          <p className="text-xs text-cosmic-text mb-6">{t('dashboard.createPrompt')}</p>
          <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold text-xs font-cinzel uppercase tracking-wider rounded-none">
            <Plus className="w-4 h-4 mr-1" /> {t('dashboard.createFirst')}
          </Button>
        </div>
      );
    }
    return (
      <div className="space-y-2">
        {clients.map(client => (
          <div key={client.id}
            className="flex items-center justify-between p-4 border border-sacred-gold hover:border-sacred-gold-dark transition-colors bg-cosmic-bg cursor-pointer group"
            onClick={() => navigate(`/client/${client.id}`)}>
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-sacred-gold-dark border border-sacred-gold flex items-center justify-center shrink-0">
                <User className="w-5 h-5 text-sacred-gold-dark" />
              </div>
              <div>
                <p className="text-sm font-medium text-cosmic-text">{client.name}</p>
                <p className="text-xs text-cosmic-text">
                  {client.birth_date || t('common.noData')} {client.birth_place ? `· ${client.birth_place}` : ''}
                  {client.phone ? ` · ${client.phone}` : ''}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-xs text-cosmic-text">{client.kundli_count} chart{client.kundli_count !== 1 ? 's' : ''}</span>
              <ChevronRight className="w-4 h-4 text-cosmic-text group-hover:text-sacred-gold-dark transition-colors" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-cinzel text-cosmic-text">
            {user?.name ? `${t('dashboard.welcome')}, ${user.name}` : 'Dashboard'}
          </h1>
          <p className="text-sm text-cosmic-text mt-1">{clients.length} {t('dashboard.clientsRegistered')}</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold text-xs font-cinzel uppercase tracking-wider px-4 py-2 rounded-none">
            <Plus className="w-4 h-4 mr-1" /> New Kundli
          </Button>
          <Button onClick={() => navigate('/lal-kitab')} variant="outline" className="border-sacred-gold/30 text-sacred-gold-dark text-xs font-cinzel uppercase tracking-wider px-4 py-2 rounded-none">
            <BookOpen className="w-4 h-4 mr-1" /> Lal Kitab
          </Button>
        </div>
      </div>

      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cosmic-text" />
        <Input type="text" value={search} onChange={e => handleSearch(e.target.value)}
          placeholder={t('dashboard.searchPlaceholder')} className="pl-10 bg-cosmic-bg border-sacred-gold/20 text-cosmic-text rounded-none" />
      </div>

      {renderClientList()}
    </div>
  );
}
