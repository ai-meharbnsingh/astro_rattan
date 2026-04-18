import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Star, BookOpen, Hash, User, Calendar, MapPin, Phone, Plus, StickyNote, Pencil, Save, Loader2, Check, X, Clock, Activity as ActivityIcon, CheckCircle2, XCircle } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/button';
import { api, formatDate, formatDateTime } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface Client {
  id: string; name: string; phone: string | null;
  birth_date: string | null; birth_time: string | null; birth_place: string | null;
  latitude: number | null; longitude: number | null; timezone_offset: number | null;
  gender: string | null; notes: string | null; created_at: string;
  // Sprint I — photo slots
  profile_photo_url?: string | null;
  left_hand_photo_url?: string | null;
  right_hand_photo_url?: string | null;
}

interface KundliSummary {
  id: string; person_name: string; birth_date: string; birth_time: string;
  birth_place: string; chart_type: string; created_at: string;
}

interface ConsultationLite {
  id: string;
  type: string;
  status: string;
  scheduled_at: string | null;
  duration_minutes: number | null;
  notes: string | null;
  created_at: string | null;
}

interface TimelineEvent {
  kind: 'note' | 'kundli' | 'consultation';
  timestamp: string | null;
  content?: string;
  chart_type?: string;
  person_name?: string;
  type?: string;
  status?: string;
  scheduled_at?: string | null;
  duration_minutes?: number | null;
  notes?: string | null;
  ref_id: string;
}

export default function ClientProfile() {
  const { clientId } = useParams<{ clientId: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { user } = useAuth();
  const isAstrologer = user?.role === 'astrologer' || user?.role === 'admin';
  const [client, setClient] = useState<Client | null>(null);
  const [kundlis, setKundlis] = useState<KundliSummary[]>([]);
  const [notes, setNotes] = useState<Array<{ id: string; content: string; chart_type: string; created_at: string }>>([]);
  // P3.5 — CRM enhancements (astrologer surfaces only)
  const [consultations, setConsultations] = useState<ConsultationLite[]>([]);
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(true);

  // Edit mode state
  const [editing, setEditing] = useState(false);
  const [editForm, setEditForm] = useState({ name: '', phone: '', birth_date: '', birth_time: '', birth_place: '', gender: '', notes: '' });
  const [editSaving, setEditSaving] = useState(false);
  const [editSaved, setEditSaved] = useState(false);

  useEffect(() => {
    if (!clientId) return;
    (async () => {
      try {
        const data = await api.get(`/api/clients/${clientId}`);
        setClient(data.client);
        setKundlis(data.kundlis);
        try {
          const n = await api.get(`/api/clients/${clientId}/notes`);
          setNotes(n);
        } catch { /* notes may not exist yet */ }
        // P3.5 — load consultations + unified timeline for astrologers.
        if (isAstrologer) {
          try {
            const c: any = await api.get(`/api/astrologer/consultations?client_id=${clientId}`);
            setConsultations(Array.isArray(c?.consultations) ? c.consultations : []);
          } catch { /* non-fatal */ }
          try {
            const tl: any = await api.get(`/api/astrologer/client-timeline/${clientId}`);
            setTimeline(Array.isArray(tl?.events) ? tl.events : []);
          } catch { /* non-fatal */ }
        }
      } catch { /* ignored */ }
      setLoading(false);
    })();
  }, [clientId, isAstrologer]);

  // P3.5 — quick-schedule a consultation from client profile.
  const [schedOpen, setSchedOpen] = useState(false);
  const [schedForm, setSchedForm] = useState<{ type: string; scheduled_at: string; duration_minutes: number; notes: string }>({
    type: 'chat', scheduled_at: '', duration_minutes: 30, notes: '',
  });
  const [schedSaving, setSchedSaving] = useState(false);
  const bookConsultation = async () => {
    if (!clientId) return;
    setSchedSaving(true);
    try {
      await api.post('/api/astrologer/consultations', {
        client_id: clientId,
        type: schedForm.type,
        scheduled_at: schedForm.scheduled_at || null,
        duration_minutes: schedForm.duration_minutes,
        notes: schedForm.notes || null,
        status: 'scheduled',
      });
      // refresh
      const c: any = await api.get(`/api/astrologer/consultations?client_id=${clientId}`);
      setConsultations(Array.isArray(c?.consultations) ? c.consultations : []);
      setSchedOpen(false);
      setSchedForm({ type: 'chat', scheduled_at: '', duration_minutes: 30, notes: '' });
    } catch { /* ignored */ }
    setSchedSaving(false);
  };
  const updateConsultationStatus = async (id: string, status: string) => {
    if (!clientId) return;
    try {
      await api.patch(`/api/astrologer/consultations/${id}`, { status });
      const c: any = await api.get(`/api/astrologer/consultations?client_id=${clientId}`);
      setConsultations(Array.isArray(c?.consultations) ? c.consultations : []);
    } catch { /* ignored */ }
  };

  const startEdit = () => {
    if (!client) return;
    setEditForm({
      name: client.name || '', phone: client.phone || '',
      birth_date: client.birth_date || '', birth_time: client.birth_time || '',
      birth_place: client.birth_place || '', gender: client.gender || '',
      notes: client.notes || '',
    });
    setEditing(true);
    setEditSaved(false);
  };

  const cancelEdit = () => { setEditing(false); setEditSaved(false); };

  const saveEdit = async () => {
    if (!clientId) return;
    setEditSaving(true);
    try {
      await api.patch(`/api/clients/${clientId}`, editForm);
      setClient(prev => prev ? { ...prev, ...editForm } : prev);
      setEditSaved(true);
      setTimeout(() => { setEditing(false); setEditSaved(false); }, 1500);
    } catch { /* ignored */ }
    setEditSaving(false);
  };

  if (loading) return <div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-600" /></div>;
  if (!client) return <div className="text-center py-20 text-foreground">{t('client.notFound')}</div>;

  const birthState = {
    clientId: client.id, clientName: client.name,
    birthDate: client.birth_date, birthTime: client.birth_time,
    birthPlace: client.birth_place, latitude: client.latitude, longitude: client.longitude,
  };

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-4xl mx-auto">
      {/* Back — astrologers land on /astrologer CRM; everyone else /dashboard */}
      <button onClick={() => navigate(isAstrologer ? '/astrologer' : '/dashboard')} className="flex items-center gap-1 text-sm text-foreground hover:text-sacred-gold-dark mb-6">
        <ArrowLeft className="w-4 h-4" /> {t('client.backToDashboard')}
      </button>

      {/* Client Info */}
      <div className="border border-sacred-gold p-6 mb-6">
        {!editing ? (
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-sacred-gold-dark border border-sacred-gold flex items-center justify-center">
                <User className="w-7 h-7 text-sacred-gold-dark" />
              </div>
              <div>
                <Heading as={1} variant={1}>{client.name}</Heading>
                <div className="flex flex-wrap gap-x-4 gap-y-1 mt-1 text-sm text-foreground">
                  {client.birth_date && <span className="flex items-center gap-1"><Calendar className="w-3 h-3" />{formatDate(client.birth_date)} {client.birth_time}</span>}
                  {client.birth_place && <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{client.birth_place}</span>}
                  {client.phone && <span className="flex items-center gap-1"><Phone className="w-3 h-3" />{client.phone}</span>}
                  {client.gender && <span className="capitalize">{client.gender}</span>}
                </div>
              </div>
            </div>
            <button onClick={startEdit} className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-sacred-gold-dark border border-sacred-gold rounded-lg hover:bg-sacred-gold/10 transition-colors">
              <Pencil className="w-3.5 h-3.5" /> {t('common.edit')}
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">{t('auth.fullName')}</label>
                <input type="text" value={editForm.name} onChange={e => setEditForm(f => ({ ...f, name: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block"><Phone className="w-3 h-3 inline mr-1" />{t('auth.phoneNumberRequired')}</label>
                <input type="tel" value={editForm.phone} onChange={e => setEditForm(f => ({ ...f, phone: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block"><Calendar className="w-3 h-3 inline mr-1" />{t('auto.birthDate')}</label>
                <input type="date" value={editForm.birth_date} onChange={e => setEditForm(f => ({ ...f, birth_date: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">{t('auto.birthTime')}</label>
                <input type="time" step="1" value={editForm.birth_time} onChange={e => setEditForm(f => ({ ...f, birth_time: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block"><MapPin className="w-3 h-3 inline mr-1" />Birth Place</label>
                <input type="text" value={editForm.birth_place} onChange={e => setEditForm(f => ({ ...f, birth_place: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">{t('auto.gender')}</label>
                <select value={editForm.gender} onChange={e => setEditForm(f => ({ ...f, gender: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none">
                  <option value="">{t('auto.select')}</option>
                  <option value="male">{t('auto.male')}</option>
                  <option value="female">{t('auto.female')}</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Notes</label>
              <textarea value={editForm.notes} onChange={e => setEditForm(f => ({ ...f, notes: e.target.value }))} rows={2}
                className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none resize-none" />
            </div>
            <div className="flex gap-2">
              <Button onClick={saveEdit} disabled={editSaving}
                className="flex items-center gap-2 px-4 py-2 bg-sacred-gold-dark text-white rounded-lg text-sm font-medium hover:bg-sacred-gold transition-all disabled:opacity-50">
                {editSaving ? <Loader2 className="w-4 h-4 animate-spin" /> : editSaved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
                {editSaving ? 'Saving...' : editSaved ? 'Saved!' : 'Save'}
              </Button>
              <Button variant="outline" onClick={cancelEdit}
                className="flex items-center gap-1.5 px-4 py-2 border-border text-foreground rounded-lg text-sm hover:bg-gray-50">
                <X className="w-3.5 h-3.5" /> {t('common.cancel')}
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Sprint I — Photo slots (profile + left hand + right hand) */}
      {isAstrologer && (
        <div className="border border-sacred-gold rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-sacred-gold-dark" />
              <Heading as={3} variant={6} className="uppercase tracking-wider">
                {t('client.photos') || 'Photos'}
              </Heading>
            </div>
            <span className="text-[11px] text-muted-foreground">
              Profile · Left Hand · Right Hand (palmistry)
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <ClientPhotoSlot
              clientId={client.id}
              field="profile_photo_url"
              label="Profile"
              value={client.profile_photo_url ?? null}
              onUpdate={(url) => setClient((prev) => prev ? { ...prev, profile_photo_url: url } : prev)}
            />
            <ClientPhotoSlot
              clientId={client.id}
              field="left_hand_photo_url"
              label="Left Hand"
              value={client.left_hand_photo_url ?? null}
              onUpdate={(url) => setClient((prev) => prev ? { ...prev, left_hand_photo_url: url } : prev)}
            />
            <ClientPhotoSlot
              clientId={client.id}
              field="right_hand_photo_url"
              label="Right Hand"
              value={client.right_hand_photo_url ?? null}
              onUpdate={(url) => setClient((prev) => prev ? { ...prev, right_hand_photo_url: url } : prev)}
            />
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-8">
        <Button onClick={() => navigate('/kundli', { state: { ...birthState, chartType: 'vedic' } })}
          className="bg-sacred-gold-dark text-background hover:bg-gray-50 h-14 rounded-lg uppercase tracking-wider text-sm">
          <Star className="w-4 h-4 mr-2" /> {t('client.newKundli')}
        </Button>
        <Button onClick={() => navigate('/lal-kitab', { state: birthState })}
          variant="outline" className="border-sacred-gold text-sacred-gold-dark h-14 rounded-lg uppercase tracking-wider text-sm">
          <BookOpen className="w-4 h-4 mr-2" /> {t('nav.lalKitab')}
        </Button>
        <Button onClick={() => navigate('/numerology', { state: { clientName: client.name, birthDate: client.birth_date } })}
          variant="outline" className="border-sacred-gold text-sacred-gold-dark h-14 rounded-lg uppercase tracking-wider text-sm">
          <Hash className="w-4 h-4 mr-2" /> {t('nav.numerology')}
        </Button>
      </div>

      {/* Charts */}
      <div className="mb-4 flex items-center justify-between">
        <Heading as={2} variant={6} className="uppercase tracking-wider">{t('client.charts')} ({kundlis.length})</Heading>
      </div>

      {kundlis.length === 0 ? (
        <div className="text-center py-12 border border-dashed border-sacred-gold">
          <p className="text-foreground mb-4">{t('client.noCharts')}</p>
          <Button onClick={() => navigate('/kundli', { state: { ...birthState, chartType: 'vedic' } })}
            className="bg-sacred-gold-dark text-background hover:bg-gray-50 text-sm uppercase rounded-lg">
            <Plus className="w-4 h-4 mr-1" /> {t('client.generateFirst')}
          </Button>
        </div>
      ) : (
        <div className="space-y-2">
          {kundlis.map(k => (
            <div key={k.id}
              onClick={() => {
                if (k.chart_type === 'lalkitab') {
                  navigate('/lal-kitab', { state: { ...birthState, loadKundliId: k.id } });
                } else {
                  navigate('/kundli', { state: { loadKundliId: k.id } });
                }
              }}
              className="flex items-center justify-between p-4 border border-sacred-gold hover:border-sacred-gold transition-colors cursor-pointer">
              <div className="flex items-center gap-3">
                {k.chart_type === 'lalkitab' ? (
                  <BookOpen className="w-4 h-4 text-orange-400" />
                ) : (
                  <Star className="w-4 h-4 text-amber-500" />
                )}
                <div>
                  <p className="text-sm text-foreground">{k.person_name}</p>
                  <p className="text-sm text-foreground">{formatDate(k.birth_date)} {k.birth_time} · {k.birth_place}</p>
                </div>
              </div>
              <div className="text-right">
                <span className="text-sm text-foreground uppercase">{k.chart_type || 'vedic'}</span>
                <p className="text-sm text-foreground">{formatDate(k.created_at)}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* P3.5 — Consultations (astrologer surface) */}
      {isAstrologer && (
        <>
          <div className="mb-4 mt-8 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-sacred-gold-dark" />
              <Heading as={2} variant={6} className="uppercase tracking-wider">
                {t('client.consultations') || 'Consultations'} ({consultations.length})
              </Heading>
            </div>
            <button
              onClick={() => setSchedOpen((v) => !v)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm bg-sacred-gold-dark text-white rounded-lg hover:bg-sacred-gold transition-colors"
            >
              <Plus className="w-3.5 h-3.5" />
              {schedOpen ? 'Close' : 'Schedule'}
            </button>
          </div>

          {schedOpen && (
            <div className="rounded-xl border border-sacred-gold/40 bg-sacred-gold/5 p-4 mb-4 space-y-3">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">Type</label>
                  <select
                    value={schedForm.type}
                    onChange={(e) => setSchedForm((f) => ({ ...f, type: e.target.value }))}
                    className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
                  >
                    <option value="chat">Chat</option>
                    <option value="audio">Audio</option>
                    <option value="video">Video</option>
                    <option value="in_person">In Person</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">When</label>
                  <input
                    type="datetime-local"
                    value={schedForm.scheduled_at}
                    onChange={(e) => setSchedForm((f) => ({ ...f, scheduled_at: e.target.value }))}
                    className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">Duration (min)</label>
                  <input
                    type="number" min={5} max={480} step={5}
                    value={schedForm.duration_minutes}
                    onChange={(e) => setSchedForm((f) => ({ ...f, duration_minutes: parseInt(e.target.value) || 30 }))}
                    className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
                  />
                </div>
              </div>
              <textarea
                value={schedForm.notes}
                onChange={(e) => setSchedForm((f) => ({ ...f, notes: e.target.value }))}
                rows={2}
                placeholder="Agenda, questions, topic…"
                className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm resize-none"
              />
              <div className="flex justify-end gap-2">
                <button onClick={() => setSchedOpen(false)} className="px-4 py-1.5 text-sm border border-sacred-gold/30 rounded-lg">Cancel</button>
                <button
                  onClick={bookConsultation}
                  disabled={schedSaving}
                  className="px-4 py-1.5 text-sm bg-sacred-gold-dark text-white rounded-lg hover:bg-sacred-gold disabled:opacity-50 flex items-center gap-1.5"
                >
                  {schedSaving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
                  Book
                </button>
              </div>
            </div>
          )}

          {consultations.length === 0 ? (
            <div className="text-sm text-muted-foreground border border-dashed border-sacred-gold/30 rounded-xl p-6 text-center mb-4">
              No consultations yet.
            </div>
          ) : (
            <div className="space-y-2 mb-4">
              {consultations.map((c) => {
                const when = c.scheduled_at ? new Date(c.scheduled_at) : null;
                const statusCls: Record<string, string> = {
                  scheduled: 'bg-sacred-gold/15 text-sacred-gold-dark border-sacred-gold/40',
                  confirmed: 'bg-blue-100 text-blue-800 border-blue-300',
                  active: 'bg-emerald-100 text-emerald-800 border-emerald-400 animate-pulse',
                  completed: 'bg-green-100 text-green-800 border-green-300',
                  cancelled: 'bg-gray-100 text-gray-600 border-gray-300',
                  no_show: 'bg-red-100 text-red-700 border-red-300',
                };
                return (
                  <div key={c.id} className="border border-sacred-gold/30 rounded-xl p-3 flex items-start justify-between gap-3 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full border font-semibold uppercase ${statusCls[c.status] ?? 'bg-gray-100 border-gray-300'}`}>
                          {c.status}
                        </span>
                        <span className="text-xs uppercase text-muted-foreground">{c.type}</span>
                        {when && (
                          <span className="text-xs text-foreground/75 inline-flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {when.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                          </span>
                        )}
                        {c.duration_minutes && <span className="text-xs text-muted-foreground">· {c.duration_minutes}min</span>}
                      </div>
                      {c.notes && <p className="text-sm text-foreground/80 mt-1">{c.notes}</p>}
                    </div>
                    <div className="flex items-center gap-1 shrink-0">
                      {c.status === 'scheduled' && (
                        <button onClick={() => updateConsultationStatus(c.id, 'confirmed')} className="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded-lg hover:bg-blue-200">Confirm</button>
                      )}
                      {(c.status === 'scheduled' || c.status === 'confirmed') && (
                        <button onClick={() => updateConsultationStatus(c.id, 'active')} className="text-xs px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-lg hover:bg-emerald-200">Start</button>
                      )}
                      {c.status === 'active' && (
                        <button onClick={() => updateConsultationStatus(c.id, 'completed')} className="text-xs px-2 py-0.5 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 inline-flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3" /> Complete
                        </button>
                      )}
                      {c.status !== 'completed' && c.status !== 'cancelled' && (
                        <button onClick={() => updateConsultationStatus(c.id, 'cancelled')} className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-100 hover:text-red-700 inline-flex items-center gap-1">
                          <XCircle className="w-3 h-3" /> Cancel
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Timeline — unified notes + kundlis + consultations */}
          {timeline.length > 0 && (
            <>
              <div className="mb-4 mt-8 flex items-center gap-2">
                <ActivityIcon className="w-4 h-4 text-sacred-gold-dark" />
                <Heading as={2} variant={6} className="uppercase tracking-wider">
                  {t('client.timeline') || 'Timeline'} ({timeline.length})
                </Heading>
              </div>
              <ol className="relative border-l-2 border-sacred-gold/20 space-y-3 ml-2 mb-6">
                {timeline.map((ev, i) => {
                  const ts = ev.timestamp ? new Date(ev.timestamp) : null;
                  const tint =
                    ev.kind === 'kundli' ? 'bg-sacred-gold/15 text-sacred-gold-dark' :
                    ev.kind === 'note' ? 'bg-violet-100 text-violet-700' :
                    'bg-blue-100 text-blue-700';
                  const Icon = ev.kind === 'kundli' ? BookOpen : ev.kind === 'note' ? StickyNote : Clock;
                  const title =
                    ev.kind === 'kundli' ? `Generated ${ev.chart_type ?? 'chart'} for ${ev.person_name ?? client.name}` :
                    ev.kind === 'note' ? `Note added${ev.chart_type ? ` (${ev.chart_type})` : ''}` :
                    `Consultation ${ev.status ?? ''} (${ev.type ?? ''})`;
                  const detail =
                    ev.kind === 'note' ? ev.content :
                    ev.kind === 'consultation' ? (ev.notes || ev.scheduled_at) :
                    null;
                  return (
                    <li key={`${ev.kind}-${ev.ref_id}-${i}`} className="ml-4">
                      <span className={`absolute -left-[13px] w-6 h-6 rounded-full flex items-center justify-center ${tint} border-2 border-background`}>
                        <Icon className="w-3 h-3" />
                      </span>
                      <div className="pb-2">
                        <div className="flex items-center justify-between gap-2 flex-wrap">
                          <p className="text-sm font-semibold text-foreground">{title}</p>
                          {ts && (
                            <span className="text-[11px] text-muted-foreground shrink-0">
                              {ts.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                            </span>
                          )}
                        </div>
                        {detail && <p className="text-xs text-foreground/70 mt-0.5 line-clamp-2">{detail}</p>}
                      </div>
                    </li>
                  );
                })}
              </ol>
            </>
          )}
        </>
      )}

      {/* Notes */}
      {notes.length > 0 && (
        <>
          <div className="mb-4 mt-8 flex items-center gap-2">
            <StickyNote className="w-4 h-4 text-sacred-gold-dark" />
            <Heading as={2} variant={6} className="uppercase tracking-wider">{t('notes.header')} ({notes.length})</Heading>
          </div>
          <div className="space-y-2">
            {notes.map(note => (
              <div key={note.id} className="border-l-2 border-sacred-gold pl-4 py-2">
                <p className="text-sm text-foreground whitespace-pre-wrap">{note.content}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-sm text-foreground">
                    {note.created_at ? formatDateTime(note.created_at) : ''}
                  </span>
                  <span className="text-sm px-1.5 py-0.5 bg-sacred-gold-dark text-white rounded">
                    {{
                      vedic: t('notes.chartType.vedic'),
                      lalkitab: t('notes.chartType.lalkitab'),
                      numerology: t('notes.chartType.numerology'),
                      general: t('notes.chartType.general')
                    }[note.chart_type] || note.chart_type}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

/**
 * Sprint I — Client photo slot (profile + left/right hand).
 *
 * Encodes the file as a data URL client-side and PATCHes the
 * /api/clients/{id} endpoint — no separate upload service needed.
 * 2MB limit per image enforced.
 */
function ClientPhotoSlot({ clientId, field, label, value, onUpdate }: {
  clientId: string;
  field: 'profile_photo_url' | 'left_hand_photo_url' | 'right_hand_photo_url';
  label: string;
  value: string | null;
  onUpdate: (url: string) => void;
}) {
  const ref = (window as any)._phSlotRefs ??= {};
  const slotKey = `${clientId}-${field}`;
  const [uploading, setUploading] = useState(false);

  const pick = async (file: File | null) => {
    if (!file) return;
    if (file.size > 2 * 1024 * 1024) {
      alert('File must be under 2MB');
      return;
    }
    setUploading(true);
    const reader = new FileReader();
    reader.onload = async () => {
      const dataUrl = String(reader.result ?? '');
      try {
        await api.patch(`/api/clients/${clientId}`, { [field]: dataUrl });
        onUpdate(dataUrl);
      } catch (e) {
        console.error('Upload failed', e);
      }
      setUploading(false);
    };
    reader.onerror = () => setUploading(false);
    reader.readAsDataURL(file);
  };

  const remove = async () => {
    try {
      await api.patch(`/api/clients/${clientId}`, { [field]: '' });
      onUpdate('');
    } catch (e) { console.error(e); }
  };

  return (
    <div className="border-2 border-dashed border-sacred-gold/30 rounded-lg p-3 flex flex-col items-center gap-2">
      <input
        id={slotKey}
        ref={(el) => { if (el) ref[slotKey] = el; }}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => pick(e.target.files?.[0] ?? null)}
      />
      {value ? (
        <div className="relative">
          <img src={value} alt={label} className="w-24 h-24 object-cover rounded-lg border border-sacred-gold/40" />
          {uploading && (
            <div className="absolute inset-0 rounded-lg bg-black/40 flex items-center justify-center">
              <Loader2 className="w-5 h-5 animate-spin text-white" />
            </div>
          )}
          <button
            onClick={remove}
            disabled={uploading}
            className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-red-500 text-white flex items-center justify-center text-xs disabled:opacity-50"
            aria-label="Remove"
          >
            ×
          </button>
        </div>
      ) : (
        <div className="w-24 h-24 rounded-lg bg-sacred-gold/10 flex items-center justify-center">
          {uploading ? <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /> : <User className="w-8 h-8 text-sacred-gold/50" />}
        </div>
      )}
      <div className="text-center">
        <p className="text-xs font-semibold text-foreground">{label}</p>
        <label htmlFor={slotKey} className="text-[11px] text-sacred-gold-dark hover:underline cursor-pointer">
          {value ? 'Change' : 'Upload'}
        </label>
      </div>
    </div>
  );
}
