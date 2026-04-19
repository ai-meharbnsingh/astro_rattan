import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Star, BookOpen, Hash, User, Calendar, MapPin, Phone, Plus, StickyNote, Pencil, Save, Loader2, Check, X, Clock, Activity as ActivityIcon, CheckCircle2, XCircle, ChevronRight } from 'lucide-react';
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
                  className="input-sacred" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block"><Phone className="w-3 h-3 inline mr-1" />{t('auth.phoneNumberRequired')}</label>
                <input type="tel" value={editForm.phone} onChange={e => setEditForm(f => ({ ...f, phone: e.target.value }))}
                  className="input-sacred" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block"><Calendar className="w-3 h-3 inline mr-1" />{t('auto.birthDate')}</label>
                <input type="date" value={editForm.birth_date} onChange={e => setEditForm(f => ({ ...f, birth_date: e.target.value }))}
                  className="input-sacred" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">{t('auto.birthTime')}</label>
                <input type="time" step="1" value={editForm.birth_time} onChange={e => setEditForm(f => ({ ...f, birth_time: e.target.value }))}
                  className="input-sacred" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block"><MapPin className="w-3 h-3 inline mr-1" />Birth Place</label>
                <input type="text" value={editForm.birth_place} onChange={e => setEditForm(f => ({ ...f, birth_place: e.target.value }))}
                  className="input-sacred" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">{t('auto.gender')}</label>
                <select value={editForm.gender} onChange={e => setEditForm(f => ({ ...f, gender: e.target.value }))}
                  className="input-sacred">
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
                className="input-sacred resize-none" />
            </div>
            <div className="flex gap-2">
              <Button onClick={saveEdit} disabled={editSaving} className="flex items-center gap-2 px-4 py-2 text-sm">
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

      {/* 4-tab bar — Kundli / Lal Kitab / Numerology / Vastu.
          Tab shows green dot when client has data for that system. */}
      <ClientChartTabs
        client={client}
        kundlis={kundlis}
        birthState={birthState}
        navigate={navigate}
        onRefresh={async () => {
          try {
            const data: any = await api.get(`/api/clients/${clientId}`);
            setKundlis(data.kundlis ?? []);
          } catch { /* ignore */ }
        }}
      />

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

      {/* Notes — always visible on client profile, grouped by day so
          astrologers can scan every note they've ever added for this
          client regardless of chart context. */}
      <div className="mt-8">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <StickyNote className="w-4 h-4 text-sacred-gold-dark" />
            <Heading as={2} variant={6} className="uppercase tracking-wider">
              {t('notes.header')} ({notes.length})
            </Heading>
          </div>
          <p className="text-xs text-muted-foreground">
            {t('notes.subtitle') || 'All notes across every chart · date-wise'}
          </p>
        </div>

        {notes.length === 0 ? (
          <div className="text-center py-10 border border-dashed border-sacred-gold/30 rounded-lg">
            <StickyNote className="w-8 h-8 text-sacred-gold/40 mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">
              {t('notes.empty') || 'No notes yet. Notes added from Kundli / Lal Kitab / Numerology pages will appear here.'}
            </p>
          </div>
        ) : (() => {
          // Group by YYYY-MM-DD — most-recent day first.
          const groups: Record<string, typeof notes> = {};
          for (const n of notes) {
            const key = n.created_at ? n.created_at.slice(0, 10) : 'unknown';
            (groups[key] ??= []).push(n);
          }
          const dayKeys = Object.keys(groups).sort().reverse();
          const chartTypeChip: Record<string, { cls: string; labelKey: string }> = {
            vedic:      { cls: 'bg-amber-100 text-amber-800 border-amber-300', labelKey: 'notes.chartType.vedic' },
            lalkitab:   { cls: 'bg-orange-100 text-orange-800 border-orange-300', labelKey: 'notes.chartType.lalkitab' },
            numerology: { cls: 'bg-purple-100 text-purple-800 border-purple-300', labelKey: 'notes.chartType.numerology' },
            general:    { cls: 'bg-gray-100 text-gray-700 border-gray-300', labelKey: 'notes.chartType.general' },
          };
          return (
            <div className="space-y-4">
              {dayKeys.map((dayKey) => {
                const dayNotes = groups[dayKey];
                const headerLabel = dayKey === 'unknown'
                  ? (t('notes.unknownDate') || 'Undated')
                  : formatDate(dayKey);
                return (
                  <div key={dayKey}>
                    <div className="flex items-center gap-2 mb-2">
                      <Calendar className="w-3.5 h-3.5 text-sacred-gold-dark" />
                      <span className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider">
                        {headerLabel}
                      </span>
                      <span className="text-[11px] text-muted-foreground">
                        · {dayNotes.length} {dayNotes.length === 1 ? (t('notes.noteSingular') || 'note') : (t('notes.notePlural') || 'notes')}
                      </span>
                      <div className="flex-1 h-px bg-sacred-gold/15" />
                    </div>
                    <div className="space-y-2">
                      {dayNotes.map((note) => {
                        const chip = chartTypeChip[note.chart_type] ?? chartTypeChip.general;
                        return (
                          <div key={note.id} className="border-l-2 border-sacred-gold pl-4 py-2 bg-sacred-gold/5 rounded-r-lg">
                            <p className="text-sm text-foreground whitespace-pre-wrap">{note.content}</p>
                            <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                              <span className="text-[11px] text-muted-foreground">
                                {note.created_at ? formatDateTime(note.created_at) : ''}
                              </span>
                              <span className={`text-[10px] px-1.5 py-0.5 rounded-full border font-semibold uppercase ${chip.cls}`}>
                                {t(chip.labelKey) || note.chart_type}
                              </span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          );
        })()}
      </div>

      {/* Sprint I — Payments ledger (astrologer-only) */}
      {isAstrologer && <ClientPaymentsSection clientId={clientId!} />}
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
/**
 * ClientChartTabs — Sprint I profile redesign.
 *
 * Compact 4-tab bar (Kundli / Lal Kitab / Numerology / Vastu) with:
 *   - Green filled indicator when this client has data in that system
 *   - Selected-tab body with either:
 *       has data → 2–3 key facts preview + "Open Full Analysis →"
 *       no data  → "Generate" button
 *
 * Vastu does not currently persist per-client data, so the Vastu tab
 * deep-links to the standalone /vastu page with birth context.
 */
function ClientChartTabs({ client, kundlis, birthState, navigate, onRefresh }: {
  client: Client;
  kundlis: KundliSummary[];
  birthState: any;
  navigate: (to: string, opts?: any) => void;
  onRefresh: () => void | Promise<void>;
}) {
  const vedicK = kundlis.find((k) => !k.chart_type || k.chart_type === 'vedic');
  const lkK = kundlis.find((k) => k.chart_type === 'lalkitab');
  const numK = kundlis.find((k) => k.chart_type === 'numerology');

  type TabKey = 'kundli' | 'lalkitab' | 'numerology' | 'vastu';
  // Start on the first tab that has data (if any); else kundli.
  const initial: TabKey = vedicK ? 'kundli' : lkK ? 'lalkitab' : numK ? 'numerology' : 'kundli';
  const [tab, setTab] = useState<TabKey>(initial);
  const [generating, setGenerating] = useState<TabKey | null>(null);

  const tabs: { key: TabKey; label: string; icon: any; hasData: boolean }[] = [
    { key: 'kundli', label: 'Kundli', icon: Star, hasData: !!vedicK },
    { key: 'lalkitab', label: 'Lal Kitab', icon: BookOpen, hasData: !!lkK },
    { key: 'numerology', label: 'Numerology', icon: Hash, hasData: !!numK },
    { key: 'vastu', label: 'Vastu', icon: User, hasData: false }, // not client-scoped yet
  ];

  const generateChart = async (chart_type: string) => {
    if (!client.birth_date || !client.birth_time || client.latitude == null || client.longitude == null) {
      alert('Birth date, time, latitude and longitude required on client profile before generating.');
      return;
    }
    setGenerating(tab);
    try {
      await api.post('/api/clients/generate-all', {
        name: client.name,
        phone: client.phone || null,
        birth_date: client.birth_date,
        birth_time: client.birth_time,
        birth_place: client.birth_place || '',
        latitude: client.latitude,
        longitude: client.longitude,
        timezone_offset: client.timezone_offset ?? 5.5,
        gender: client.gender || 'male',
        generate_vedic: chart_type === 'vedic',
        generate_lalkitab: chart_type === 'lalkitab',
        generate_numerology: chart_type === 'numerology',
      });
      await onRefresh();
    } catch (e) {
      console.error('Generate failed', e);
    }
    setGenerating(null);
  };

  return (
    <div className="mb-8 rounded-xl border border-sacred-gold/30 bg-card overflow-hidden">
      {/* Tab bar */}
      <div className="flex border-b border-sacred-gold/20 bg-sacred-gold/5 overflow-x-auto">
        {tabs.map((tb) => {
          const Icon = tb.icon;
          const isActive = tab === tb.key;
          return (
            <button
              key={tb.key}
              onClick={() => setTab(tb.key)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-semibold transition-colors border-b-2 shrink-0 ${
                isActive
                  ? 'border-sacred-gold text-sacred-gold-dark bg-white'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tb.label}
              <span
                className={`w-2 h-2 rounded-full ${tb.hasData ? 'bg-emerald-500' : 'bg-gray-300'}`}
                aria-label={tb.hasData ? 'has data' : 'no data'}
              />
            </button>
          );
        })}
      </div>

      {/* Tab body */}
      <div className="p-5">
        {tab === 'kundli' && (
          <ChartTabBody
            icon={Star}
            title="Vedic Kundli"
            exists={!!vedicK}
            lastUpdated={vedicK?.created_at}
            onOpen={() => vedicK && navigate('/kundli', { state: { loadKundliId: vedicK.id } })}
            onGenerate={() => generateChart('vedic')}
            generating={generating === 'kundli'}
            emptyText="No Vedic kundli for this client yet. Generate one to get planet positions, dasha, yogas, and the full analysis suite."
          />
        )}
        {tab === 'lalkitab' && (
          <ChartTabBody
            icon={BookOpen}
            title="Lal Kitab"
            exists={!!lkK}
            lastUpdated={lkK?.created_at}
            onOpen={() => lkK && navigate('/lal-kitab', { state: { ...birthState, loadKundliId: lkK.id } })}
            onGenerate={() => generateChart('lalkitab')}
            generating={generating === 'lalkitab'}
            emptyText="No Lal Kitab chart yet. Generate to access Tewa, Doshas, Karmic Debts (Rin), safety layer and remedies."
          />
        )}
        {tab === 'numerology' && (
          <ChartTabBody
            icon={Hash}
            title="Numerology"
            exists={!!numK}
            lastUpdated={numK?.created_at}
            onOpen={() => numK && navigate('/numerology', { state: { clientName: client.name, birthDate: client.birth_date, loadKundliId: numK.id } })}
            onGenerate={() => generateChart('numerology')}
            generating={generating === 'numerology'}
            emptyText="No numerology profile yet. Generate to see life path, destiny, expression numbers and lucky-number guidance."
          />
        )}
        {tab === 'vastu' && (
          <ChartTabBody
            icon={User}
            title="Vastu"
            exists={false}
            lastUpdated={undefined}
            onOpen={() => navigate('/vastu', { state: birthState })}
            onGenerate={() => navigate('/vastu', { state: birthState })}
            generating={false}
            emptyText="Vastu consultations open in the standalone Vastu page (not persisted per-client yet). Opens with this client's birth context pre-filled."
            generateLabel="Open Vastu"
            openLabel="Open Vastu"
          />
        )}
      </div>
    </div>
  );
}

function ChartTabBody({ icon: Icon, title, exists, lastUpdated, onOpen, onGenerate, generating, emptyText, generateLabel, openLabel }: {
  icon: any; title: string; exists: boolean; lastUpdated?: string;
  onOpen: () => void; onGenerate: () => void; generating: boolean;
  emptyText: string; generateLabel?: string; openLabel?: string;
}) {
  return (
    <div className="flex items-center gap-5 flex-wrap">
      <div className={`w-16 h-16 rounded-full flex items-center justify-center shrink-0 ${
        exists ? 'bg-sacred-gold/15 text-sacred-gold-dark' : 'bg-gray-100 text-gray-400'
      }`}>
        <Icon className="w-8 h-8" />
      </div>
      <div className="flex-1 min-w-[200px]">
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
          {exists ? (
            <span className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> Generated
            </span>
          ) : (
            <span className="text-[11px] px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 font-semibold">
              Not yet
            </span>
          )}
        </div>
        {exists && lastUpdated && (
          <p className="text-xs text-muted-foreground mt-0.5">
            Last updated {formatDate(lastUpdated)}
          </p>
        )}
        {!exists && (
          <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
            {emptyText}
          </p>
        )}
      </div>
      <div className="flex gap-2 shrink-0">
        {exists ? (
          <Button
            onClick={onOpen}
            className="bg-sacred-gold-dark text-white hover:bg-sacred-gold"
          >
            <ChevronRight className="w-4 h-4 mr-1" />
            {openLabel || `Open ${title} →`}
          </Button>
        ) : (
          <Button
            onClick={onGenerate}
            disabled={generating}
            className="bg-sacred-gold-dark text-white hover:bg-sacred-gold disabled:opacity-50"
          >
            {generating ? <Loader2 className="w-4 h-4 animate-spin mr-1" /> : <Plus className="w-4 h-4 mr-1" />}
            {generating ? 'Generating…' : (generateLabel || `Generate ${title}`)}
          </Button>
        )}
      </div>
    </div>
  );
}

/**
 * ClientPaymentsSection — Sprint I.
 *
 * Simple ledger view for past payments received from this client.
 * Empty state when nothing recorded yet. Inline "+ Add payment" form.
 */
function ClientPaymentsSection({ clientId }: { clientId: string }) {
  const [payments, setPayments] = useState<any[]>([]);
  const [totalAmount, setTotalAmount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [formOpen, setFormOpen] = useState(false);
  const [form, setForm] = useState({ amount: '', currency: 'INR', method: '', purpose: '', paid_at: '', notes: '' });
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res: any = await api.get(`/api/clients/${clientId}/payments`);
      setPayments(Array.isArray(res?.payments) ? res.payments : []);
      setTotalAmount(res?.total_amount || 0);
    } catch { setPayments([]); }
    setLoading(false);
  };
  useEffect(() => { load(); }, [clientId]);

  const submit = async () => {
    if (!form.amount || parseFloat(form.amount) <= 0) return;
    setSaving(true);
    try {
      await api.post(`/api/clients/${clientId}/payments`, {
        amount: parseFloat(form.amount),
        currency: form.currency || 'INR',
        method: form.method || null,
        purpose: form.purpose || null,
        paid_at: form.paid_at || null,
        notes: form.notes || null,
        status: 'completed',
      });
      setForm({ amount: '', currency: 'INR', method: '', purpose: '', paid_at: '', notes: '' });
      setFormOpen(false);
      load();
    } catch (e) { console.error(e); }
    setSaving(false);
  };

  return (
    <div className="mt-8">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Hash className="w-4 h-4 text-sacred-gold-dark" />
          <Heading as={2} variant={6} className="uppercase tracking-wider">
            Payments ({payments.length})
          </Heading>
          {totalAmount > 0 && (
            <span className="text-sm font-bold text-sacred-gold-dark ml-2">
              Total: ₹{totalAmount.toLocaleString('en-IN')}
            </span>
          )}
        </div>
        <button
          onClick={() => setFormOpen((v) => !v)}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm bg-sacred-gold-dark text-white rounded-lg hover:bg-sacred-gold transition-colors"
        >
          <Plus className="w-3.5 h-3.5" />
          {formOpen ? 'Close' : 'Record Payment'}
        </button>
      </div>

      {formOpen && (
        <div className="mb-4 rounded-xl border border-sacred-gold/40 bg-sacred-gold/5 p-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
          <input
            type="number" step="0.01" min="0" placeholder="Amount *"
            value={form.amount}
            onChange={(e) => setForm((f) => ({ ...f, amount: e.target.value }))}
            className="px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
          />
          <input
            placeholder="Method (UPI / Cash / Card)"
            value={form.method}
            onChange={(e) => setForm((f) => ({ ...f, method: e.target.value }))}
            className="px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
          />
          <input
            placeholder="Purpose (Consultation / Report…)"
            value={form.purpose}
            onChange={(e) => setForm((f) => ({ ...f, purpose: e.target.value }))}
            className="px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
          />
          <input
            type="datetime-local"
            value={form.paid_at}
            onChange={(e) => setForm((f) => ({ ...f, paid_at: e.target.value }))}
            className="px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
          />
          <input
            placeholder="Notes (optional)"
            value={form.notes}
            onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
            className="px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm sm:col-span-2"
          />
          <div className="sm:col-span-3 flex justify-end gap-2">
            <button onClick={() => setFormOpen(false)} className="px-4 py-1.5 text-sm border border-sacred-gold/30 rounded-lg">Cancel</button>
            <button
              onClick={submit}
              disabled={saving || !form.amount}
              className="px-4 py-1.5 text-sm bg-sacred-gold-dark text-white rounded-lg hover:bg-sacred-gold disabled:opacity-50 inline-flex items-center gap-1.5"
            >
              {saving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
              Record
            </button>
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-sm text-muted-foreground">Loading…</div>
      ) : payments.length === 0 ? (
        <div className="text-center py-10 border border-dashed border-sacred-gold/30 rounded-lg">
          <p className="text-sm text-muted-foreground">No payments recorded yet.</p>
        </div>
      ) : (
        <div className="rounded-xl border border-sacred-gold/20 bg-card overflow-hidden">
          <table className="table-sacred w-full">
            <thead className="bg-sacred-gold/5 border-b border-sacred-gold/20">
              <tr className="text-left text-[10px] uppercase tracking-wider text-muted-foreground">
                <th className="px-4 py-2 font-semibold">Date</th>
                <th className="px-4 py-2 font-semibold">Amount</th>
                <th className="px-4 py-2 font-semibold">Method</th>
                <th className="px-4 py-2 font-semibold">Purpose</th>
                <th className="px-4 py-2 font-semibold">Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-sacred-gold/10">
              {payments.map((p: any) => (
                <tr key={p.id} className="hover:bg-sacred-gold/5">
                  <td className="px-4 py-2 text-sm text-foreground">
                    {p.paid_at ? formatDate(p.paid_at) : formatDate(p.created_at)}
                  </td>
                  <td className="px-4 py-2 text-sm font-semibold text-sacred-gold-dark">
                    {p.currency === 'INR' ? '₹' : p.currency + ' '}{Number(p.amount).toLocaleString('en-IN')}
                  </td>
                  <td className="px-4 py-2 text-xs text-muted-foreground">{p.method ?? '—'}</td>
                  <td className="px-4 py-2 text-xs text-muted-foreground">{p.purpose ?? '—'}</td>
                  <td className="px-4 py-2 text-xs text-muted-foreground truncate max-w-[200px]">{p.notes ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

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
