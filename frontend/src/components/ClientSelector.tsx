import { useState, useEffect, useRef } from 'react';
import { Users, UserPlus, Search, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';

export interface ClientData {
  id: string;
  name: string;
  phone?: string | null;
  birth_date?: string | null;
  birth_time?: string | null;
  birth_place?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  timezone_offset?: number | null;
  gender?: string | null;
}

interface ClientSelectorProps {
  onSelectClient: (client: ClientData | null) => void;
  /** Whether "New Client" is selected (parent controls this) */
  isNewClient: boolean;
  onToggle: (isNew: boolean) => void;
}

export default function ClientSelector({ onSelectClient, isNewClient, onToggle }: ClientSelectorProps) {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [clients, setClients] = useState<ClientData[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [selectedName, setSelectedName] = useState('');

  const isVisible = !!user && user.role === 'astrologer';

  const fetchClients = async (query: string = '') => {
    setLoading(true);
    try {
      const params = query ? `?search=${encodeURIComponent(query)}` : '';
      const data = await api.get(`/api/clients${params}`);
      setClients(Array.isArray(data) ? data : []);
    } catch {
      setClients([]);
    }
    setLoading(false);
  };

  // Fetch clients on mount and when search changes
  useEffect(() => {
    if (isVisible && !isNewClient) {
      fetchClients(search);
    }
  }, [isVisible, isNewClient, search]);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // Only render for astrologers
  if (!isVisible) return null;

  const handleSelectClient = (client: ClientData) => {
    setSelectedName(client.name);
    setSearch('');
    setShowDropdown(false);
    onSelectClient(client);
  };

  return (
    <div className="mb-6 rounded-xl border border-sacred-gold/30 p-4 bg-card/50">
      <p className="text-sm font-medium text-sacred-gold mb-3">{t('clientSelector.clientType')}</p>
      <div className="grid grid-cols-2 gap-3 mb-3">
        <button
          type="button"
          onClick={() => { onToggle(false); setSelectedName(''); onSelectClient(null); }}
          className={`flex items-center justify-center gap-2 p-3 rounded-xl border text-sm font-medium transition-colors ${
            !isNewClient
              ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold'
              : 'border-sacred-gold/20 text-muted-foreground hover:border-sacred-gold/40'
          }`}
        >
          <Users className="w-4 h-4" />
          {t('clientSelector.existingClient')}
        </button>
        <button
          type="button"
          onClick={() => { onToggle(true); setSelectedName(''); onSelectClient(null); }}
          className={`flex items-center justify-center gap-2 p-3 rounded-xl border text-sm font-medium transition-colors ${
            isNewClient
              ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold'
              : 'border-sacred-gold/20 text-muted-foreground hover:border-sacred-gold/40'
          }`}
        >
          <UserPlus className="w-4 h-4" />
          {t('clientSelector.newClient')}
        </button>
      </div>

      {!isNewClient && (
        <div ref={wrapperRef} className="relative">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/40" />
            <input
              type="text"
              value={search || selectedName}
              onChange={(e) => { setSearch(e.target.value); setSelectedName(''); setShowDropdown(true); onSelectClient(null); }}
              onFocus={() => { if (!selectedName) setShowDropdown(true); }}
              placeholder={t('clientSelector.searchByName')}
              className="w-full rounded-xl bg-card border border-sacred-gold/20 text-foreground px-4 py-2.5 pl-10 text-sm focus:outline-none focus:border-sacred-gold/50 transition-colors"
            />
            {loading && <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 animate-spin text-sacred-gold" />}
          </div>

          {showDropdown && !selectedName && (
            <div className="absolute z-50 left-0 right-0 mt-1 bg-background border border-sacred-gold/30 rounded-xl shadow-lg max-h-60 overflow-y-auto">
              {clients.length === 0 && !loading && (
                <div className="px-4 py-3 text-sm text-muted-foreground text-center">
                  {search ? t('clientSelector.noClientsFound') : t('dashboard.noClients')}
                </div>
              )}
              {clients.map((c) => (
                <button
                  key={c.id}
                  type="button"
                  onClick={() => handleSelectClient(c)}
                  className="w-full text-left px-4 py-3 hover:bg-sacred-gold/10 transition-colors border-b border-sacred-gold/10 last:border-b-0"
                >
                  <p className="text-sm font-medium text-foreground">{c.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {[c.phone, c.birth_date, c.birth_place].filter(Boolean).join(' | ') || t('common.noData')}
                  </p>
                </button>
              ))}
            </div>
          )}

          {selectedName && (
            <p className="text-sm text-green-400 mt-1 px-1">{t('clientSelector.selected')}: {selectedName}</p>
          )}
        </div>
      )}
    </div>
  );
}

/**
 * Helper to auto-register a new client under the astrologer after successful form submission.
 * Checks for duplicates (same name + birth_date) before creating.
 */
export async function autoRegisterClient(params: {
  name: string;
  phone?: string;
  birth_date?: string;
  birth_time?: string;
  birth_place?: string;
  latitude?: number;
  longitude?: number;
  timezone_offset?: number;
  gender?: string;
}): Promise<void> {
  try {
    // Check if client already exists (fetch and search by name)
    const existing = await api.get(`/api/clients?search=${encodeURIComponent(params.name)}`);
    if (Array.isArray(existing)) {
      const dupe = existing.find(
        (c: any) => c.name === params.name && c.birth_date === params.birth_date
      );
      if (dupe) return; // Already exists, skip
    }
    // Create the client
    await api.post('/api/clients', {
      name: params.name,
      phone: params.phone || null,
      birth_date: params.birth_date || null,
      birth_time: params.birth_time || null,
      birth_place: params.birth_place || null,
      latitude: params.latitude || null,
      longitude: params.longitude || null,
      timezone_offset: params.timezone_offset || 5.5,
      gender: params.gender || 'male',
    });
  } catch (err) {
    /* non-critical — auto-register failed silently */
  }
}
