import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Plus, Search, Star, BookOpen, Calendar, ChevronRight, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Client {
  id: string;
  name: string;
  phone: string | null;
  birth_date: string | null;
  birth_time: string | null;
  birth_place: string | null;
  gender: string | null;
  kundli_count: number;
  created_at: string;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [clients, setClients] = useState<Client[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return; }
    fetchClients();
  }, [isAuthenticated]);

  const fetchClients = async (q = '') => {
    setLoading(true);
    try {
      const data = await api.get(`/api/clients?search=${encodeURIComponent(q)}`);
      setClients(data);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleSearch = (val: string) => {
    setSearch(val);
    fetchClients(val);
  };

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-cinzel text-cosmic-text">
            {user?.name ? `Welcome, ${user.name}` : 'Dashboard'}
          </h1>
          <p className="text-sm text-cosmic-text/50 mt-1">{clients.length} clients registered</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => navigate('/kundli')}
            className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold text-xs font-cinzel uppercase tracking-wider px-4 py-2 rounded-none">
            <Plus className="w-4 h-4 mr-1" /> New Kundli
          </Button>
          <Button onClick={() => navigate('/lal-kitab')} variant="outline"
            className="border-sacred-gold/30 text-sacred-gold-dark text-xs font-cinzel uppercase tracking-wider px-4 py-2 rounded-none">
            <BookOpen className="w-4 h-4 mr-1" /> Lal Kitab
          </Button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        {[
          { label: 'Kundli', icon: Star, route: '/kundli', color: 'text-amber-500' },
          { label: 'Panchang', icon: Calendar, route: '/panchang', color: 'text-blue-400' },
          { label: 'Lal Kitab', icon: BookOpen, route: '/lal-kitab', color: 'text-orange-400' },
          { label: 'Numerology', icon: Users, route: '/numerology', color: 'text-purple-400' },
        ].map(a => (
          <button key={a.label} onClick={() => navigate(a.route)}
            className="border border-sacred-gold/20 p-4 text-left hover:border-sacred-gold/50 transition-colors bg-cosmic-bg">
            <a.icon className={`w-5 h-5 ${a.color} mb-2`} />
            <p className="text-sm font-cinzel text-cosmic-text">{a.label}</p>
          </button>
        ))}
      </div>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cosmic-text/40" />
        <Input
          type="text" value={search} onChange={e => handleSearch(e.target.value)}
          placeholder="Search clients by name..."
          className="pl-10 bg-cosmic-bg border-sacred-gold/20 text-cosmic-text rounded-none"
        />
      </div>

      {/* Client List */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-600" />
        </div>
      ) : clients.length === 0 ? (
        <div className="text-center py-16 border border-dashed border-sacred-gold/20">
          <User className="w-12 h-12 text-cosmic-text/20 mx-auto mb-4" />
          <p className="text-cosmic-text/50 mb-2">No clients yet</p>
          <p className="text-xs text-cosmic-text/30 mb-6">Create a kundli to auto-register your first client</p>
          <Button onClick={() => navigate('/kundli')}
            className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold text-xs font-cinzel uppercase tracking-wider rounded-none">
            <Plus className="w-4 h-4 mr-1" /> Create First Kundli
          </Button>
        </div>
      ) : (
        <div className="space-y-2">
          {clients.map(client => (
            <div key={client.id}
              className="flex items-center justify-between p-4 border border-sacred-gold/15 hover:border-sacred-gold/40 transition-colors bg-cosmic-bg cursor-pointer group"
              onClick={() => navigate(`/client/${client.id}`)}
            >
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 bg-sacred-gold-dark/10 border border-sacred-gold/20 flex items-center justify-center shrink-0">
                  <User className="w-5 h-5 text-sacred-gold-dark" />
                </div>
                <div>
                  <p className="text-sm font-medium text-cosmic-text">{client.name}</p>
                  <p className="text-xs text-cosmic-text/40">
                    {client.birth_date || 'No birth date'} {client.birth_place ? `· ${client.birth_place}` : ''}
                    {client.phone ? ` · ${client.phone}` : ''}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-xs text-cosmic-text/40">{client.kundli_count} chart{client.kundli_count !== 1 ? 's' : ''}</span>
                <ChevronRight className="w-4 h-4 text-cosmic-text/20 group-hover:text-sacred-gold-dark transition-colors" />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
