import { useTranslation } from '@/lib/i18n';
import { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Plus, Search, BookOpen, ChevronRight, User, Star, BarChart3 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
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
  const [fetchError, setFetchError] = useState<string | null>(null);

  // Admin state
  const [adminStats, setAdminStats] = useState<AdminStats | null>(null);

  // Debounce ref for search
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();

  const fetchClients = useCallback(async (q = '') => {
    setLoading(true);
    setFetchError(null);
    try {
      const data = await api.get(`/api/clients?search=${encodeURIComponent(q)}`);
      setClients(data);
    } catch (e: unknown) {
      console.error(e);
      const msg = e instanceof Error ? e.message : '';
      setFetchError(msg === 'Not authenticated' ? t('dashboard.sessionExpired') : t('dashboard.loadFailed'));
    }
    setLoading(false);
  }, [t]);

  const fetchAdminStats = useCallback(async () => {
    try {
      const data = await api.get('/api/admin/stats');
      setAdminStats(data);
    } catch (e: unknown) {
      console.error(e);
      const msg = e instanceof Error ? e.message : '';
      setFetchError(msg || t('dashboard.adminStatsLoadFailed'));
    }
  }, [t]);

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return; }
    if (isAdmin) {
      fetchAdminStats();
    }
    fetchClients();
  }, [isAuthenticated, isAdmin, navigate, fetchAdminStats, fetchClients]);

  const handleSearch = (val: string) => {
    setSearch(val);
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => fetchClients(val), 300);
  };

  // ─── ADMIN DASHBOARD ─────────────────────────────────────
  if (isAdmin && adminStats) {
    return (
      <div className="min-h-screen pt-28 pb-16 px-4 max-w-6xl mx-auto">
        <div className="flex items-center justify-end mb-8">
          <div className="flex gap-2">
            <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold-dark text-cosmic-bg hover:bg-gray-50 text-sm font-sans uppercase tracking-wider px-4 py-2 rounded-lg">
              <Plus className="w-4 h-4 mr-1" /> {t('dashboard.newKundli')}
            </Button>
            <Button onClick={() => navigate('/admin')} variant="outline" className="border-sacred-gold text-sacred-gold-dark text-sm font-sans uppercase tracking-wider px-4 py-2 rounded-lg">
              <BarChart3 className="w-4 h-4 mr-1" /> {t('dashboard.fullAdmin')}
            </Button>
          </div>
        </div>

        {/* Summary Boxes */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { label: t('dashboard.stats.astrologers'), value: adminStats.counts.astrologers, icon: Star, color: 'text-amber-500' },
            { label: t('dashboard.stats.clientsAdded'), value: adminStats.counts.clients, icon: Users, color: 'text-blue-500' },
            { label: t('dashboard.stats.totalKundlis'), value: adminStats.counts.kundlis, icon: BarChart3, color: 'text-green-500' },
            { label: t('dashboard.stats.registeredUsers'), value: adminStats.counts.users, icon: User, color: 'text-purple-500' },
          ].map(s => (
            <div key={s.label} className="border border-sacred-gold p-5 bg-cosmic-bg">
              <s.icon className={`w-5 h-5 ${s.color} mb-2`} />
              <p className="text-3xl font-sans text-cosmic-text font-bold">{s.value}</p>
              <p className="text-sm text-cosmic-text uppercase tracking-wider mt-1">{s.label}</p>
            </div>
          ))}
        </div>

        {/* Astrologers List */}
        <h2 className="text-sm font-sans text-cosmic-text uppercase tracking-wider mb-4">{t('dashboard.astrologersAndTheirClients')}</h2>
        <div className="space-y-3 mb-10">
          {adminStats.astrologers.map(astro => (
            <div key={astro.id} className="border border-sacred-gold p-4 bg-cosmic-bg">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-sacred-gold-dark border border-sacred-gold flex items-center justify-center">
                    <Star className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-cosmic-text">{astro.name}</p>
                    <p className="text-sm text-cosmic-text">{astro.email}</p>
                  </div>
                </div>
                <div className="flex gap-6 text-right">
                  <div>
                    <p className="text-lg font-sans text-cosmic-text font-bold">{astro.client_count}</p>
                    <p className="text-sm text-cosmic-text">{t('dashboard.clients')}</p>
                  </div>
                  <div>
                    <p className="text-lg font-sans text-cosmic-text font-bold">{astro.kundli_count}</p>
                    <p className="text-sm text-cosmic-text">{t('dashboard.kundlis')}</p>
                  </div>
                  <span className={`self-center text-sm px-2 py-0.5 border ${astro.role === 'admin' ? 'border-red-300 text-red-500' : 'border-purple-500 text-purple-500'}`}>
                    {astro.role}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Admin's own clients below */}
        <h2 className="text-sm font-sans text-cosmic-text uppercase tracking-wider mb-4">{t('dashboard.myClients')}</h2>
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cosmic-text" />
          <Input type="text" value={search} onChange={e => handleSearch(e.target.value)}
            placeholder={t('dashboard.searchPlaceholder')} className="pl-10 bg-cosmic-bg border-sacred-gold text-cosmic-text rounded-lg" />
        </div>
        {renderClientList()}
      </div>
    );
  }

  // ─── ASTROLOGER DASHBOARD ────────────────────────────────
  function renderClientList() {
    if (loading) {
      return (
        <div className="space-y-3 py-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="flex items-center gap-4 p-4 border border-sacred-gold">
              <div className="w-10 h-10 animate-pulse bg-sacred-gold/15 rounded" />
              <div className="flex-1 space-y-2">
                <div className="h-4 w-32 animate-pulse bg-sacred-gold/15 rounded" />
                <div className="h-3 w-48 animate-pulse bg-sacred-gold/15 rounded" />
              </div>
              <div className="h-4 w-16 animate-pulse bg-sacred-gold/15 rounded" />
            </div>
          ))}
        </div>
      );
    }
    if (fetchError) {
      return (
        <div className="text-center py-12">
          <div className="w-12 h-12 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-3"><span className="text-2xl">!</span></div>
          <p className="text-red-700 mb-2">{fetchError}</p>
          <button onClick={() => fetchClients(search)} className="px-4 py-2 bg-sacred-gold-dark text-white rounded-lg text-sm hover:opacity-90">{t('common.retry')}</button>
        </div>
      );
    }
    if (clients.length === 0) {
      return (
        <div className="text-center py-16 border border-dashed border-sacred-gold">
          <User className="w-12 h-12 text-cosmic-text mx-auto mb-4" />
          <p className="text-cosmic-text mb-2">{t('dashboard.noClients')}</p>
          <p className="text-sm text-cosmic-text mb-6">{t('dashboard.createPrompt')}</p>
          <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold-dark text-cosmic-bg hover:bg-gray-50 text-sm font-sans uppercase tracking-wider rounded-lg">
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
                <User className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm font-medium text-cosmic-text">{client.name}</p>
                <p className="text-sm text-cosmic-text">
                  {client.birth_date || t('common.noData')} {client.birth_place ? ` · ${client.birth_place}` : ''}
                  {client.phone ? ` · ${client.phone}` : ''}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-cosmic-text">{client.kundli_count} {client.kundli_count !== 1 ? t('dashboard.charts') : t('dashboard.chart')}</span>
              <ChevronRight className="w-4 h-4 text-cosmic-text group-hover:text-sacred-gold-dark transition-colors" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-28 pb-16 px-4 max-w-6xl mx-auto">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-8">
        <div>
          <h1 className="text-2xl font-sans text-cosmic-text">
            {user?.name ? `${t('dashboard.welcome')}, ${user.name}` : t('nav.dashboard')}
          </h1>
          <p className="text-sm text-cosmic-text mt-1">{clients.length} {t('dashboard.clientsRegistered')}</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold-dark text-cosmic-bg hover:bg-gray-50 text-sm font-sans uppercase tracking-wider px-4 py-2 rounded-lg whitespace-nowrap">
            <Plus className="w-4 h-4 mr-1" /> {t('dashboard.newKundli')}
          </Button>
          <Button onClick={() => navigate('/lal-kitab')} variant="outline" className="border-sacred-gold text-sacred-gold-dark text-sm font-sans uppercase tracking-wider px-4 py-2 rounded-lg whitespace-nowrap">
            <BookOpen className="w-4 h-4 mr-1" /> {t('nav.lalKitab')}
          </Button>
        </div>
      </div>

      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cosmic-text" />
        <Input type="text" value={search} onChange={e => handleSearch(e.target.value)}
          placeholder={t('dashboard.searchPlaceholder')} className="pl-10 bg-cosmic-bg border-sacred-gold text-cosmic-text rounded-lg" />
      </div>

      {renderClientList()}
    </div>
  );
}
