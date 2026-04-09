import { useState, useEffect, useRef } from 'react';
import { StickyNote, X, Send, Loader2 } from 'lucide-react';
import { api, formatDateTime } from '@/lib/api';

interface Note {
  id: string;
  content: string;
  chart_type: string;
  created_at: string;
}

interface NotesWidgetProps {
  clientId: string;
  chartType: string;
  kundliId?: string;
}

export default function NotesWidget({ clientId, chartType, kundliId }: NotesWidgetProps) {
  const [open, setOpen] = useState(false);
  const [notes, setNotes] = useState<Note[]>([]);
  const [newNote, setNewNote] = useState('');
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const dragging = useRef(false);
  const dragOffset = useRef({ x: 0, y: 0 });
  const btnRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    // Position bottom-right by default
    setPosition({ x: window.innerWidth - 70, y: window.innerHeight - 160 });
  }, []);

  const fetchNotes = async () => {
    if (!clientId) return;
    setLoading(true);
    try {
      const data = await api.get(`/api/clients/${clientId}/notes`);
      setNotes(data);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleOpen = () => {
    setOpen(true);
    fetchNotes();
  };

  const handleSave = async () => {
    if (!newNote.trim() || !clientId) return;
    setSaving(true);
    try {
      await api.post(`/api/clients/${clientId}/notes`, {
        content: newNote.trim(),
        chart_type: chartType,
        kundli_id: kundliId || null,
      });
      setNewNote('');
      fetchNotes();
    } catch (e) { console.error(e); }
    setSaving(false);
  };

  // Dragging
  const onMouseDown = (e: React.MouseEvent) => {
    dragging.current = true;
    dragOffset.current = { x: e.clientX - position.x, y: e.clientY - position.y };
    e.preventDefault();
  };
  useEffect(() => {
    const onMouseMove = (e: MouseEvent) => {
      if (!dragging.current) return;
      setPosition({ x: e.clientX - dragOffset.current.x, y: e.clientY - dragOffset.current.y });
    };
    const onMouseUp = () => { dragging.current = false; };
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    return () => { window.removeEventListener('mousemove', onMouseMove); window.removeEventListener('mouseup', onMouseUp); };
  }, []);

  if (!clientId) return null;

  const formatNoteDate = (d: string) => formatDateTime(d) || d;

  const chartLabel: Record<string, string> = {
    vedic: 'Kundli', lalkitab: 'Lal Kitab', numerology: 'Numerology', general: 'General',
  };

  return (
    <>
      {/* Floating draggable button */}
      <button
        ref={btnRef}
        onMouseDown={onMouseDown}
        onClick={() => !dragging.current && (open ? setOpen(false) : handleOpen())}
        className="fixed z-50 w-12 h-12 bg-sacred-gold-dark text-cosmic-bg rounded-full shadow-lg flex items-center justify-center hover:bg-sacred-gold transition-colors cursor-grab active:cursor-grabbing"
        style={{ left: position.x, top: position.y }}
        title="Astrologer Notes"
      >
        <StickyNote className="w-5 h-5" />
        {notes.length > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-bold">
            {notes.length}
          </span>
        )}
      </button>

      {/* Notes Panel */}
      {open && (
        <div className="fixed z-50 bg-cosmic-bg border border-sacred-gold/30 shadow-2xl flex flex-col"
          style={{ width: '360px', maxHeight: '500px', right: '20px', bottom: '80px' }}>
          {/* Header */}
          <div className="flex items-center justify-between p-3 border-b border-sacred-gold/20 bg-sacred-gold-dark/5">
            <h3 className="text-sm font-cinzel text-sacred-gold-dark uppercase tracking-wider">Notes</h3>
            <button onClick={() => setOpen(false)} className="text-cosmic-text/60 hover:text-cosmic-text">
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Add note */}
          <div className="p-3 border-b border-sacred-gold/10">
            <textarea
              value={newNote}
              onChange={e => setNewNote(e.target.value)}
              placeholder="Add a note..."
              rows={3}
              className="w-full bg-transparent border border-sacred-gold/20 text-cosmic-text text-sm p-2 resize-none focus:border-sacred-gold outline-none"
            />
            <button
              onClick={handleSave}
              disabled={saving || !newNote.trim()}
              className="mt-2 w-full flex items-center justify-center gap-2 bg-sacred-gold-dark text-cosmic-bg text-xs py-2 font-cinzel uppercase tracking-wider disabled:opacity-50 hover:bg-sacred-gold transition-colors"
            >
              {saving ? <Loader2 className="w-3 h-3 animate-spin" /> : <Send className="w-3 h-3" />}
              Save Note
            </button>
          </div>

          {/* Notes list */}
          <div className="flex-1 overflow-y-auto p-3 space-y-3" style={{ maxHeight: '300px' }}>
            {loading ? (
              <div className="text-center py-4"><Loader2 className="w-4 h-4 animate-spin text-sacred-gold mx-auto" /></div>
            ) : notes.length === 0 ? (
              <p className="text-center text-cosmic-text/60 text-xs py-4">No notes yet</p>
            ) : (
              notes.map(note => (
                <div key={note.id} className="border-l-2 border-sacred-gold/30 pl-3 py-1">
                  <p className="text-sm text-cosmic-text whitespace-pre-wrap">{note.content}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs text-cosmic-text/60">{formatNoteDate(note.created_at)}</span>
                    <span className="text-xs px-1.5 py-0.5 bg-sacred-gold-dark/10 text-sacred-gold-dark rounded">
                      {chartLabel[note.chart_type] || note.chart_type}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </>
  );
}
