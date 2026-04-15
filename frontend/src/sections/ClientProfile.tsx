import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Star, BookOpen, Hash, User, Calendar, MapPin, Phone, Plus, StickyNote, Pencil, Save, Loader2, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api, formatDate, formatDateTime } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface Client {
  id: string; name: string; phone: string | null;
  birth_date: string | null; birth_time: string | null; birth_place: string | null;
  latitude: number | null; longitude: number | null; timezone_offset: number | null;
  gender: string | null; notes: string | null; created_at: string;
}

interface KundliSummary {
  id: string; person_name: string; birth_date: string; birth_time: string;
  birth_place: string; chart_type: string; created_at: string;
}

export default function ClientProfile() {
  const { clientId } = useParams<{ clientId: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [client, setClient] = useState<Client | null>(null);
  const [kundlis, setKundlis] = useState<KundliSummary[]>([]);
  const [notes, setNotes] = useState<Array<{ id: string; content: string; chart_type: string; created_at: string }>>([]);
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
      } catch { /* ignored */ }
      setLoading(false);
    })();
  }, [clientId]);

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
      {/* Back */}
      <button onClick={() => navigate('/dashboard')} className="flex items-center gap-1 text-sm text-foreground hover:text-sacred-gold-dark mb-6">
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
                <label className="text-xs text-muted-foreground mb-1 block"><Calendar className="w-3 h-3 inline mr-1" />Birth Date</label>
                <input type="date" value={editForm.birth_date} onChange={e => setEditForm(f => ({ ...f, birth_date: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">Birth Time</label>
                <input type="time" step="1" value={editForm.birth_time} onChange={e => setEditForm(f => ({ ...f, birth_time: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block"><MapPin className="w-3 h-3 inline mr-1" />Birth Place</label>
                <input type="text" value={editForm.birth_place} onChange={e => setEditForm(f => ({ ...f, birth_place: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none" />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">Gender</label>
                <select value={editForm.gender} onChange={e => setEditForm(f => ({ ...f, gender: e.target.value }))}
                  className="w-full px-3 py-2 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none">
                  <option value="">Select</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
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
