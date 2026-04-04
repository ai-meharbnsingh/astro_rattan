import { useState, useEffect, useRef, useCallback } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  Star, Search, Plus, ArrowLeft, Loader2, Phone, Mail, MapPin,
  Calendar, User, X, ChevronRight
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import InteractiveKundli, { type PlanetData } from '@/components/InteractiveKundli';

// ── Types ──────────────────────────────────────────────────────
interface ClientSummary {
  id: string;
  client_name: string;
  client_phone?: string;
  client_email?: string;
  birth_date?: string;
  birth_place?: string;
  created_at: string;
}

interface ClientFull {
  id: string;
  client_name: string;
  client_phone?: string;
  client_email?: string;
  birth_date?: string;
  birth_time?: string;
  birth_place?: string;
  latitude?: number;
  longitude?: number;
  timezone_offset?: number;
  gender?: string;
  notes?: string;
  kundli_id?: string;
  chart_data?: any;
  ayanamsa?: string;
  iogita_analysis?: any;
  created_at: string;
  updated_at: string;
}

interface GeocodeResult {
  name: string;
  lat: number;
  lon: number;
}

// ── Geocode Hook ───────────────────────────────────────────────
function useGeocodeAutocomplete() {
  const [suggestions, setSuggestions] = useState<GeocodeResult[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const search = (query: string) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (query.length < 3) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }
    timerRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const results = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(query)}`);
        setSuggestions(Array.isArray(results) ? results : []);
        setShowDropdown(true);
      } catch {
        setSuggestions([]);
      }
      setLoading(false);
    }, 300);
  };

  const close = () => setShowDropdown(false);

  return { suggestions, showDropdown, loading, search, close };
}

// ── Add Client Form ────────────────────────────────────────────
interface AddClientFormProps {
  onSaved: (client: any) => void;
  onCancel: () => void;
}

function AddClientForm({ onSaved, onCancel }: AddClientFormProps) {
  const { t } = useTranslation();
  const geocode = useGeocodeAutocomplete();
  const placeRef = useRef<HTMLDivElement>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    client_name: '',
    client_phone: '',
    client_email: '',
    birth_date: '',
    birth_time: '',
    birth_place: '',
    latitude: 28.6139,
    longitude: 77.209,
    timezone_offset: 5.5,
    gender: 'male',
    notes: '',
  });

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (placeRef.current && !placeRef.current.contains(e.target as Node)) {
        geocode.close();
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [geocode]);

  const handleSave = async () => {
    if (!form.client_name.trim()) { setError('Client name is required'); return; }
    setSaving(true);
    setError('');
    try {
      const payload: any = { client_name: form.client_name.trim() };
      if (form.client_phone) payload.client_phone = form.client_phone;
      if (form.client_email) payload.client_email = form.client_email;
      if (form.birth_date) payload.birth_date = form.birth_date;
      if (form.birth_time) payload.birth_time = form.birth_time;
      if (form.birth_place) payload.birth_place = form.birth_place;
      payload.latitude = form.latitude;
      payload.longitude = form.longitude;
      payload.timezone_offset = form.timezone_offset;
      payload.gender = form.gender;
      if (form.notes) payload.notes = form.notes;

      const result = await api.post('/api/astrologer/clients', payload);
      onSaved(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save client');
    }
    setSaving(false);
  };

  return (
    <div className="max-w-lg mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Button variant="outline" size="sm" onClick={onCancel} className="border-[#B8860B]/30 text-[#b8b0a4]">
          <ArrowLeft className="w-4 h-4 mr-1" />{t('astrologer.backToClients')}
        </Button>
        <h3 className="text-xl font-display font-bold text-[#e8e0d4]">{t('astrologer.addClient')}</h3>
      </div>

      {error && <div className="mb-4 p-3 bg-red-500/10 border border-red-200 text-red-700 text-sm rounded">{error}</div>}

      <div className="space-y-4">
        {/* Name */}
        <div>
          <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">{t('astrologer.clientName')} *</label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#B8860B]" />
            <Input value={form.client_name} onChange={(e) => setForm({ ...form, client_name: e.target.value })}
              placeholder="Full Name" className="pl-10 bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
          </div>
        </div>

        {/* Phone + Email row */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">{t('astrologer.clientPhone')}</label>
            <div className="relative">
              <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#B8860B]" />
              <Input value={form.client_phone} onChange={(e) => setForm({ ...form, client_phone: e.target.value })}
                placeholder="+91..." className="pl-10 bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
            </div>
          </div>
          <div>
            <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">{t('astrologer.clientEmail')}</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#B8860B]" />
              <Input type="email" value={form.client_email} onChange={(e) => setForm({ ...form, client_email: e.target.value })}
                placeholder="email@example.com" className="pl-10 bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
            </div>
          </div>
        </div>

        {/* Gender */}
        <div>
          <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">Gender</label>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => setForm({ ...form, gender: 'male' })}
              className={`p-2.5 border text-sm transition-colors ${form.gender === 'male' ? 'border-[#B8860B] bg-[#B8860B]/10 text-[#B8860B]' : 'border-[#B8860B]/15 text-[#b8b0a4]'}`}>
              Male
            </button>
            <button onClick={() => setForm({ ...form, gender: 'female' })}
              className={`p-2.5 border text-sm transition-colors ${form.gender === 'female' ? 'border-[#B8860B] bg-[#B8860B]/10 text-[#B8860B]' : 'border-[#B8860B]/15 text-[#b8b0a4]'}`}>
              Female
            </button>
          </div>
        </div>

        {/* Birth Date + Time */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">Birth Date</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#B8860B]" />
              <Input type="date" value={form.birth_date} onChange={(e) => setForm({ ...form, birth_date: e.target.value })}
                className="pl-10 bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
            </div>
          </div>
          <div>
            <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">Birth Time</label>
            <Input type="time" step="1" value={form.birth_time} onChange={(e) => setForm({ ...form, birth_time: e.target.value })}
              className="bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
          </div>
        </div>

        {/* Birth Place with geocode */}
        <div ref={placeRef} className="relative">
          <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">Birth Place</label>
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#B8860B]" />
            <Input value={form.birth_place}
              onChange={(e) => { setForm({ ...form, birth_place: e.target.value }); geocode.search(e.target.value); }}
              placeholder="City, Country" className="pl-10 bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
            {geocode.loading && <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#B8860B] animate-spin" />}
          </div>
          {geocode.showDropdown && geocode.suggestions.length > 0 && (
            <div className="absolute z-20 left-0 right-0 mt-1 bg-[#1a1a2e] border border-[#B8860B]/20 shadow-lg max-h-48 overflow-y-auto">
              {geocode.suggestions.map((s, i) => (
                <button key={i} onClick={() => {
                  setForm({ ...form, birth_place: s.name.split(',').slice(0, 2).join(','), latitude: s.lat, longitude: s.lon });
                  geocode.close();
                }} className="block w-full text-left px-3 py-2 text-sm text-[#e8e0d4] hover:bg-[#B8860B]/10 truncate">
                  {s.name}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Lat/Lon/Tz row */}
        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="text-xs font-medium text-[#b8b0a4] mb-1 block">Latitude</label>
            <Input type="number" step="0.0001" value={form.latitude}
              onChange={(e) => setForm({ ...form, latitude: parseFloat(e.target.value) || 0 })}
              className="bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4] text-sm" />
          </div>
          <div>
            <label className="text-xs font-medium text-[#b8b0a4] mb-1 block">Longitude</label>
            <Input type="number" step="0.0001" value={form.longitude}
              onChange={(e) => setForm({ ...form, longitude: parseFloat(e.target.value) || 0 })}
              className="bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4] text-sm" />
          </div>
          <div>
            <label className="text-xs font-medium text-[#b8b0a4] mb-1 block">TZ Offset</label>
            <Input type="number" step="0.5" value={form.timezone_offset}
              onChange={(e) => setForm({ ...form, timezone_offset: parseFloat(e.target.value) || 5.5 })}
              className="bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4] text-sm" />
          </div>
        </div>

        {/* Notes */}
        <div>
          <label className="text-sm font-medium text-[#e8e0d4] mb-1 block">{t('astrologer.notes')}</label>
          <Textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })}
            placeholder="Consultation notes, observations..." rows={3}
            className="bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
        </div>

        <Button onClick={handleSave} disabled={saving || !form.client_name.trim()}
          className="w-full bg-[#B8860B] text-[#1a1a2e] hover:bg-[#9A7B0A] font-semibold py-3 disabled:opacity-50">
          {saving ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Plus className="w-4 h-4 mr-2" />}
          {t('astrologer.generateSave')}
        </Button>
      </div>
    </div>
  );
}


// ── Client Kundli View ─────────────────────────────────────────
interface ClientKundliViewProps {
  client: ClientFull;
  onBack: () => void;
  onNotesUpdate: (notes: string) => void;
}

function ClientKundliView({ client, onBack, onNotesUpdate }: ClientKundliViewProps) {
  const { t } = useTranslation();
  const [editingNotes, setEditingNotes] = useState(false);
  const [notes, setNotes] = useState(client.notes || '');
  const [savingNotes, setSavingNotes] = useState(false);
  const [kundliData, setKundliData] = useState<any>(null);
  const [loadingKundli, setLoadingKundli] = useState(false);

  useEffect(() => {
    if (client.kundli_id) {
      setLoadingKundli(true);
      api.get(`/api/astrologer/clients/${client.id}/kundli`)
        .then(setKundliData)
        .catch(() => {})
        .finally(() => setLoadingKundli(false));
    }
  }, [client.id, client.kundli_id]);

  const saveNotes = async () => {
    setSavingNotes(true);
    try {
      await api.put(`/api/astrologer/clients/${client.id}`, { notes });
      onNotesUpdate(notes);
      setEditingNotes(false);
    } catch { /* empty */ }
    setSavingNotes(false);
  };

  // Build chart data for InteractiveKundli
  const chartData = kundliData?.chart_data;
  const planets: PlanetData[] = chartData?.planets
    ? Object.entries(chartData.planets).map(([name, info]: [string, any]) => ({
        planet: name,
        sign: info.sign || '',
        sign_degree: info.degree || 0,
        house: info.house || 1,
        nakshatra: info.nakshatra || '',
        status: info.retrograde ? 'Retrograde' : (info.dignity || ''),
      }))
    : [];

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <Button variant="outline" size="sm" onClick={onBack} className="border-[#B8860B]/30 text-[#b8b0a4]">
          <ArrowLeft className="w-4 h-4 mr-1" />{t('astrologer.backToClients')}
        </Button>
      </div>

      {/* Client Info Card */}
      <Card className="bg-[#2a2a4e] border-0 shadow-sm mb-6">
        <CardContent className="p-5">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <h3 className="text-xl font-display font-bold text-[#e8e0d4]">{client.client_name}</h3>
              <div className="flex flex-wrap gap-3 mt-1 text-sm text-[#b8b0a4]">
                {client.client_phone && (
                  <span className="flex items-center gap-1"><Phone className="w-3.5 h-3.5" />{client.client_phone}</span>
                )}
                {client.client_email && (
                  <span className="flex items-center gap-1"><Mail className="w-3.5 h-3.5" />{client.client_email}</span>
                )}
                {client.birth_place && (
                  <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5" />{client.birth_place}</span>
                )}
              </div>
              {client.birth_date && (
                <p className="text-sm text-[#b8b0a4] mt-1">
                  Born: {client.birth_date} {client.birth_time ? `at ${client.birth_time}` : ''}
                </p>
              )}
            </div>
            <div className="text-sm text-[#b8b0a4]">
              Added {new Date(client.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notes Section */}
      <Card className="bg-[#2a2a4e] border-0 shadow-sm mb-6">
        <CardContent className="p-5">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium text-[#e8e0d4]">{t('astrologer.notes')}</h4>
            {!editingNotes ? (
              <Button variant="outline" size="sm" onClick={() => setEditingNotes(true)}
                className="border-[#B8860B]/30 text-[#b8b0a4] text-xs">
                Edit
              </Button>
            ) : (
              <div className="flex gap-2">
                <Button size="sm" onClick={saveNotes} disabled={savingNotes}
                  className="bg-[#B8860B] text-[#1a1a2e] text-xs">
                  {savingNotes ? 'Saving...' : 'Save'}
                </Button>
                <Button variant="outline" size="sm" onClick={() => { setEditingNotes(false); setNotes(client.notes || ''); }}
                  className="border-[#B8860B]/30 text-[#b8b0a4] text-xs">
                  Cancel
                </Button>
              </div>
            )}
          </div>
          {editingNotes ? (
            <Textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={3}
              className="bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]" />
          ) : (
            <p className="text-sm text-[#b8b0a4]">{client.notes || 'No notes yet.'}</p>
          )}
        </CardContent>
      </Card>

      {/* Kundli Chart */}
      {loadingKundli ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="w-8 h-8 text-[#B8860B] animate-spin" />
        </div>
      ) : kundliData && chartData ? (
        <div>
          <h4 className="text-lg font-display font-semibold text-[#e8e0d4] mb-4">{t('astrologer.viewKundli')}</h4>
          <InteractiveKundli
            chartData={{ planets }}
            onPlanetClick={() => {}}
            onHouseClick={() => {}}
          />

          {/* Planet positions table */}
          {planets.length > 0 && (
            <Card className="bg-[#2a2a4e] border-0 shadow-sm mt-6">
              <CardContent className="p-5">
                <h4 className="font-medium text-[#e8e0d4] mb-3">Planet Positions</h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-[#B8860B]/20">
                        <th className="text-left py-2 px-2 text-[#b8b0a4] font-medium">Planet</th>
                        <th className="text-left py-2 px-2 text-[#b8b0a4] font-medium">Sign</th>
                        <th className="text-left py-2 px-2 text-[#b8b0a4] font-medium">House</th>
                        <th className="text-left py-2 px-2 text-[#b8b0a4] font-medium">Degree</th>
                        <th className="text-left py-2 px-2 text-[#b8b0a4] font-medium">Nakshatra</th>
                      </tr>
                    </thead>
                    <tbody>
                      {planets.map((p) => (
                        <tr key={p.planet} className="border-b border-[#B8860B]/10">
                          <td className="py-2 px-2 text-[#e8e0d4] font-medium">{p.planet}{p.status === 'Retrograde' ? ' (R)' : ''}</td>
                          <td className="py-2 px-2 text-[#e8e0d4]">{p.sign}</td>
                          <td className="py-2 px-2 text-[#e8e0d4]">{p.house}</td>
                          <td className="py-2 px-2 text-[#e8e0d4]">{typeof p.sign_degree === 'number' ? p.sign_degree.toFixed(2) : p.sign_degree}</td>
                          <td className="py-2 px-2 text-[#e8e0d4]">{p.nakshatra}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      ) : !client.kundli_id ? (
        <div className="text-center py-12">
          <Calendar className="w-12 h-12 text-[#b8b0a4]/40 mx-auto mb-3" />
          <p className="text-[#b8b0a4]">No kundli generated. Update client birth details to generate one.</p>
        </div>
      ) : null}
    </div>
  );
}


// ── Main Panel ─────────────────────────────────────────────────
export default function AstrologerPanel() {
  const { user } = useAuth();
  const { t } = useTranslation();
  const [view, setView] = useState<'list' | 'add' | 'detail'>('list');
  const [clients, setClients] = useState<ClientSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchDebounce, setSearchDebounce] = useState('');
  const [selectedClient, setSelectedClient] = useState<ClientFull | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const searchTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Debounced search
  useEffect(() => {
    if (searchTimerRef.current) clearTimeout(searchTimerRef.current);
    searchTimerRef.current = setTimeout(() => {
      setSearchDebounce(searchQuery);
    }, 300);
    return () => { if (searchTimerRef.current) clearTimeout(searchTimerRef.current); };
  }, [searchQuery]);

  const fetchClients = useCallback(async (search?: string) => {
    setLoading(true);
    try {
      const url = search ? `/api/astrologer/clients?search=${encodeURIComponent(search)}` : '/api/astrologer/clients';
      const data = await api.get(url);
      setClients(Array.isArray(data) ? data : []);
    } catch { setClients([]); }
    setLoading(false);
  }, []);

  useEffect(() => {
    if (user?.role === 'astrologer' || user?.role === 'admin') {
      fetchClients(searchDebounce || undefined);
    } else {
      setLoading(false);
    }
  }, [user?.role, searchDebounce, fetchClients]);

  const openClientDetail = async (clientId: string) => {
    setLoadingDetail(true);
    try {
      const data = await api.get(`/api/astrologer/clients/${clientId}`);
      setSelectedClient(data);
      setView('detail');
    } catch { /* empty */ }
    setLoadingDetail(false);
  };

  const handleClientSaved = (client: any) => {
    // After saving, go to the detail view of new client
    setSelectedClient(client);
    setView('detail');
    fetchClients();
  };

  const handleDeleteClient = async (clientId: string) => {
    try {
      await api.delete(`/api/astrologer/clients/${clientId}`);
      setClients((prev) => prev.filter((c) => c.id !== clientId));
      if (selectedClient?.id === clientId) {
        setSelectedClient(null);
        setView('list');
      }
    } catch { /* empty */ }
  };

  if (user?.role !== 'astrologer' && user?.role !== 'admin') {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <Star className="w-16 h-16 text-[#b8b0a4]/40 mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-[#e8e0d4] mb-2">Astrologer Access Required</h2>
        <p className="text-[#b8b0a4]">This panel is only accessible to verified astrologers.</p>
      </div>
    );
  }

  return (
    <section className="max-w-6xl mx-auto py-24 px-4">
      {/* Panel Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 rounded-full bg-[#B8860B] flex items-center justify-center">
          <Star className="w-5 h-5 text-[#e8e0d4]" />
        </div>
        <div>
          <h2 className="text-2xl font-display font-bold text-[#e8e0d4]">{t('astrologer.panel')}</h2>
          <p className="text-sm text-[#b8b0a4]">{t('astrologer.clients')}</p>
        </div>
      </div>

      {/* ── List View ─────────────────────────────────── */}
      {view === 'list' && (
        <>
          {/* Search + Add */}
          <div className="flex flex-col sm:flex-row gap-3 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#B8860B]" />
              <Input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={t('astrologer.searchClients')}
                className="pl-10 bg-[#1a1a2e] border-[#B8860B]/15 text-[#e8e0d4]"
              />
              {searchQuery && (
                <button onClick={() => setSearchQuery('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#b8b0a4] hover:text-[#e8e0d4]">
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
            <Button onClick={() => setView('add')}
              className="bg-[#B8860B] text-[#1a1a2e] hover:bg-[#9A7B0A] font-semibold shrink-0">
              <Plus className="w-4 h-4 mr-2" />{t('astrologer.addClient')}
            </Button>
          </div>

          {/* Client Cards */}
          {loading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-8 h-8 text-[#B8860B] animate-spin" />
            </div>
          ) : clients.length === 0 ? (
            <div className="text-center py-16">
              <User className="w-16 h-16 text-[#b8b0a4]/30 mx-auto mb-4" />
              <p className="text-lg text-[#b8b0a4] mb-1">{t('astrologer.noClients')}</p>
              <p className="text-sm text-[#b8b0a4]/70 mb-4">Add your first client to get started</p>
              <Button onClick={() => setView('add')}
                className="bg-[#B8860B] text-[#1a1a2e] hover:bg-[#9A7B0A]">
                <Plus className="w-4 h-4 mr-2" />{t('astrologer.addClient')}
              </Button>
            </div>
          ) : (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {clients.map((client) => (
                <Card key={client.id}
                  className="bg-[#2a2a4e] border-0 shadow-sm hover:shadow-md transition-shadow cursor-pointer group"
                  onClick={() => openClientDetail(client.id)}>
                  <CardContent className="p-5">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <div className="w-9 h-9 rounded-full bg-[#B8860B]/15 flex items-center justify-center">
                          <User className="w-4 h-4 text-[#B8860B]" />
                        </div>
                        <div>
                          <h4 className="font-display font-semibold text-[#e8e0d4] group-hover:text-[#B8860B] transition-colors">
                            {client.client_name}
                          </h4>
                          {client.client_phone && (
                            <p className="text-xs text-[#b8b0a4] flex items-center gap-1">
                              <Phone className="w-3 h-3" />{client.client_phone}
                            </p>
                          )}
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-[#b8b0a4]/50 group-hover:text-[#B8860B] transition-colors mt-1" />
                    </div>
                    <div className="text-xs text-[#b8b0a4] space-y-1">
                      {client.birth_date && (
                        <p className="flex items-center gap-1"><Calendar className="w-3 h-3" />{client.birth_date}</p>
                      )}
                      {client.birth_place && (
                        <p className="flex items-center gap-1"><MapPin className="w-3 h-3" />{client.birth_place}</p>
                      )}
                      <p className="text-[#b8b0a4]/50 mt-2">
                        {new Date(client.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {loadingDetail && (
            <div className="fixed inset-0 bg-black/20 flex items-center justify-center z-50">
              <Loader2 className="w-10 h-10 text-[#B8860B] animate-spin" />
            </div>
          )}
        </>
      )}

      {/* ── Add View ──────────────────────────────────── */}
      {view === 'add' && (
        <AddClientForm
          onSaved={handleClientSaved}
          onCancel={() => setView('list')}
        />
      )}

      {/* ── Detail View ───────────────────────────────── */}
      {view === 'detail' && selectedClient && (
        <ClientKundliView
          client={selectedClient}
          onBack={() => { setSelectedClient(null); setView('list'); fetchClients(); }}
          onNotesUpdate={(newNotes) => setSelectedClient((prev) => prev ? { ...prev, notes: newNotes } : prev)}
        />
      )}
    </section>
  );
}
