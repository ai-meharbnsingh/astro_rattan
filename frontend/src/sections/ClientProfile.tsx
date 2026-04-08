import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Star, BookOpen, Hash, User, Calendar, MapPin, Phone, Plus, StickyNote } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';

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
      } catch (e) { console.error(e); }
      setLoading(false);
    })();
  }, [clientId]);

  if (loading) return <div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-600" /></div>;
  if (!client) return <div className="text-center py-20 text-cosmic-text/70">Client not found</div>;

  const birthState = {
    clientId: client.id, clientName: client.name,
    birthDate: client.birth_date, birthTime: client.birth_time,
    birthPlace: client.birth_place, latitude: client.latitude, longitude: client.longitude,
  };

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-4xl mx-auto">
      {/* Back */}
      <button onClick={() => navigate('/dashboard')} className="flex items-center gap-1 text-sm text-cosmic-text/70 hover:text-sacred-gold-dark mb-6">
        <ArrowLeft className="w-4 h-4" /> Back to Dashboard
      </button>

      {/* Client Info */}
      <div className="border border-sacred-gold/20 p-6 mb-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 bg-sacred-gold-dark/10 border border-sacred-gold/20 flex items-center justify-center">
              <User className="w-7 h-7 text-sacred-gold-dark" />
            </div>
            <div>
              <h1 className="text-2xl font-cinzel text-cosmic-text">{client.name}</h1>
              <div className="flex flex-wrap gap-x-4 gap-y-1 mt-1 text-xs text-cosmic-text/70">
                {client.birth_date && <span className="flex items-center gap-1"><Calendar className="w-3 h-3" />{client.birth_date} {client.birth_time}</span>}
                {client.birth_place && <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{client.birth_place}</span>}
                {client.phone && <span className="flex items-center gap-1"><Phone className="w-3 h-3" />{client.phone}</span>}
                {client.gender && <span className="capitalize">{client.gender}</span>}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-8">
        <Button onClick={() => navigate('/kundli', { state: { ...birthState, chartType: 'vedic' } })}
          className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold h-14 rounded-none font-cinzel uppercase tracking-wider text-xs">
          <Star className="w-4 h-4 mr-2" /> New Kundli
        </Button>
        <Button onClick={() => navigate('/lal-kitab', { state: birthState })}
          variant="outline" className="border-sacred-gold/30 text-sacred-gold-dark h-14 rounded-none font-cinzel uppercase tracking-wider text-xs">
          <BookOpen className="w-4 h-4 mr-2" /> Lal Kitab
        </Button>
        <Button onClick={() => navigate('/numerology', { state: { clientName: client.name, birthDate: client.birth_date } })}
          variant="outline" className="border-sacred-gold/30 text-sacred-gold-dark h-14 rounded-none font-cinzel uppercase tracking-wider text-xs">
          <Hash className="w-4 h-4 mr-2" /> Numerology
        </Button>
      </div>

      {/* Charts */}
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-sm font-cinzel text-cosmic-text/70 uppercase tracking-wider">Charts ({kundlis.length})</h2>
      </div>

      {kundlis.length === 0 ? (
        <div className="text-center py-12 border border-dashed border-sacred-gold/20">
          <p className="text-cosmic-text/60 mb-4">No charts generated yet</p>
          <Button onClick={() => navigate('/kundli', { state: { ...birthState, chartType: 'vedic' } })}
            className="bg-sacred-gold-dark text-cosmic-bg hover:bg-sacred-gold text-xs font-cinzel uppercase rounded-none">
            <Plus className="w-4 h-4 mr-1" /> Generate First Chart
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
              className="flex items-center justify-between p-4 border border-sacred-gold/15 hover:border-sacred-gold/40 transition-colors cursor-pointer">
              <div className="flex items-center gap-3">
                {k.chart_type === 'lalkitab' ? (
                  <BookOpen className="w-4 h-4 text-orange-400" />
                ) : (
                  <Star className="w-4 h-4 text-amber-500" />
                )}
                <div>
                  <p className="text-sm text-cosmic-text">{k.person_name}</p>
                  <p className="text-xs text-cosmic-text/60">{k.birth_date} {k.birth_time} · {k.birth_place}</p>
                </div>
              </div>
              <div className="text-right">
                <span className="text-xs text-cosmic-text/60 uppercase">{k.chart_type || 'vedic'}</span>
                <p className="text-xs text-cosmic-text/60">{k.created_at ? k.created_at.toString().slice(0, 10) : ''}</p>
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
            <h2 className="text-sm font-cinzel text-cosmic-text/70 uppercase tracking-wider">Notes ({notes.length})</h2>
          </div>
          <div className="space-y-2">
            {notes.map(note => (
              <div key={note.id} className="border-l-2 border-sacred-gold/30 pl-4 py-2">
                <p className="text-sm text-cosmic-text whitespace-pre-wrap">{note.content}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs text-cosmic-text/60">
                    {note.created_at ? new Date(note.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) + ' ' + new Date(note.created_at).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : ''}
                  </span>
                  <span className="text-xs px-1.5 py-0.5 bg-sacred-gold-dark/10 text-sacred-gold-dark rounded">
                    {{ vedic: 'Kundli', lalkitab: 'Lal Kitab', numerology: 'Numerology', general: 'General' }[note.chart_type] || note.chart_type}
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
