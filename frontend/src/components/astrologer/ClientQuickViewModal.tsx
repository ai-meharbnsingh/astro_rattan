/**
 * ClientQuickViewModal — Sprint I.
 *
 * Triggered by clicking any client row / avatar on the Astrologer
 * Dashboard. Shows:
 *   - Profile photos (avatar + left hand + right hand if present)
 *   - JHora-style North Indian kundli (reuses InteractiveKundli)
 *   - Quick-action list (Schedule / Add Note / Full Profile)
 *   - Recent notes preview (top 5)
 *
 * The user can drill into the full /client/:id page via the
 * "View Full Profile" button.
 */
import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import InteractiveKundli, { type ChartData, type PlanetData } from '@/components/InteractiveKundli';
import {
  X, Loader2, Calendar, MapPin, Phone, NotebookPen, ChevronRight, User as UserIcon,
  Hand, BookOpen, Hash, Sparkles, Clock, StickyNote, ExternalLink,
} from 'lucide-react';

interface Props {
  clientId: string;
  isHi: boolean;
  onClose: () => void;
  onOpenFullProfile: (clientId: string) => void;
}

interface ClientDetail {
  id: string;
  name: string;
  phone: string | null;
  birth_date: string | null;
  birth_time: string | null;
  birth_place: string | null;
  latitude: number | null;
  longitude: number | null;
  timezone_offset: number | null;
  gender: string | null;
  notes: string | null;
  profile_photo_url: string | null;
  left_hand_photo_url: string | null;
  right_hand_photo_url: string | null;
}

interface KundliRef {
  id: string;
  person_name: string;
  chart_type: string;
  created_at: string;
}

interface NoteRow {
  id: string;
  content: string;
  chart_type: string;
  created_at: string;
}

const CHART_BADGE: Record<string, { labelEn: string; labelHi: string; icon: any }> = {
  vedic:      { labelEn: 'Vedic', labelHi: 'वैदिक', icon: Sparkles },
  lalkitab:   { labelEn: 'Lal Kitab', labelHi: 'लाल किताब', icon: BookOpen },
  numerology: { labelEn: 'Numerology', labelHi: 'अंक', icon: Hash },
};

export default function ClientQuickViewModal({ clientId, isHi, onClose, onOpenFullProfile }: Props) {
  const [client, setClient] = useState<ClientDetail | null>(null);
  const [kundlis, setKundlis] = useState<KundliRef[]>([]);
  const [notes, setNotes] = useState<NoteRow[]>([]);
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [chartLoading, setChartLoading] = useState(false);
  const [selectedChart, setSelectedChart] = useState<string>('vedic');
  const [loading, setLoading] = useState(true);

  // Escape to close + scroll lock
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prev;
    };
  }, [onClose]);

  // Load client + kundlis + notes
  useEffect(() => {
    if (!clientId) return;
    setLoading(true);
    (async () => {
      try {
        const data: any = await api.get(`/api/clients/${clientId}`);
        setClient(data.client);
        setKundlis(Array.isArray(data.kundlis) ? data.kundlis : []);
        // Default to the most-recent vedic chart, else the first kundli.
        const vedicKundli = (data.kundlis as KundliRef[] | undefined)?.find((k) => k.chart_type === 'vedic');
        const first = (data.kundlis as KundliRef[] | undefined)?.[0];
        if (vedicKundli) setSelectedChart(vedicKundli.chart_type);
        else if (first) setSelectedChart(first.chart_type);
      } catch { /* keep null */ }
      try {
        const n: any = await api.get(`/api/clients/${clientId}/notes`);
        setNotes(Array.isArray(n) ? n.slice(0, 5) : []);
      } catch { /* ignore */ }
      setLoading(false);
    })();
  }, [clientId]);

  // Load chart data for the currently-selected kundli type.
  useEffect(() => {
    if (!kundlis.length) { setChartData(null); return; }
    const k = kundlis.find((x) => x.chart_type === selectedChart) ?? kundlis[0];
    if (!k) { setChartData(null); return; }
    setChartLoading(true);
    api.get(`/api/kundli/${k.id}`)
      .then((res: any) => {
        if (!res?.chart_data) { setChartData(null); return; }
        // Adapt the payload to InteractiveKundli's expected ChartData shape.
        const planets: PlanetData[] = Object.entries(res.chart_data.planets || {}).map(([name, info]: [string, any]) => ({
          planet: name,
          sign: info.sign ?? '',
          house: info.house ?? 0,
          nakshatra: info.nakshatra ?? '',
          sign_degree: info.sign_degree ?? 0,
          longitude: info.longitude,
          status: info.status,
          is_retrograde: info.is_retrograde,
          is_combust: info.is_combust,
          is_vargottama: info.is_vargottama,
        } as PlanetData));
        const asc = res.chart_data.ascendant || {};
        const ZODIAC = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
        const ascIdx = ZODIAC.indexOf(asc.sign || 'Aries');
        setChartData({
          planets,
          houses: Array.from({ length: 12 }, (_, i) => ({ number: i + 1, sign: ZODIAC[(ascIdx + i) % 12] })),
          ascendant: asc?.longitude !== undefined ? {
            longitude: asc.longitude || 0,
            sign: asc.sign || 'Aries',
            sign_degree: asc.sign_degree,
          } : undefined,
        });
      })
      .catch(() => setChartData(null))
      .finally(() => setChartLoading(false));
  }, [kundlis, selectedChart]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-start justify-center p-4 bg-black/60 backdrop-blur-sm overflow-y-auto"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="relative w-full max-w-5xl my-8 rounded-2xl bg-white border border-sacred-gold/30 shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-sacred-gold/20 p-5 rounded-t-2xl flex items-start justify-between gap-3 z-10">
          <div className="flex items-center gap-3 min-w-0">
            {client?.profile_photo_url ? (
              <img
                src={client.profile_photo_url}
                alt=""
                className="w-12 h-12 rounded-full object-cover border-2 border-sacred-gold/40 shrink-0"
              />
            ) : (
              <div className="w-12 h-12 rounded-full bg-sacred-gold-dark text-white flex items-center justify-center text-lg font-bold shrink-0">
                {(client?.name ?? '?').slice(0, 1).toUpperCase()}
              </div>
            )}
            <div className="min-w-0">
              <h2 className="text-xl font-semibold text-foreground truncate">
                {client?.name ?? (isHi ? 'ग्राहक' : 'Client')}
              </h2>
              <p className="text-xs text-muted-foreground flex items-center gap-2 flex-wrap">
                {client?.birth_date && (
                  <span className="inline-flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {client.birth_date} {client.birth_time}
                  </span>
                )}
                {client?.birth_place && (
                  <span className="inline-flex items-center gap-1">
                    <MapPin className="w-3 h-3" />
                    {client.birth_place}
                  </span>
                )}
                {client?.phone && (
                  <span className="inline-flex items-center gap-1">
                    <Phone className="w-3 h-3" />
                    {client.phone}
                  </span>
                )}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-gray-100 shrink-0"
            aria-label={isHi ? 'बंद करें' : 'Close'}
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Body */}
        {loading ? (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
          </div>
        ) : !client ? (
          <div className="p-10 text-center text-muted-foreground">
            {isHi ? 'ग्राहक लोड नहीं हो सका' : 'Could not load client'}
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-0 divide-y lg:divide-y-0 lg:divide-x divide-sacred-gold/20">
            {/* LEFT — chart + chart-type tabs */}
            <div className="p-5">
              {kundlis.length > 0 ? (
                <>
                  <div className="flex items-center gap-2 mb-3 flex-wrap">
                    {kundlis.map((k) => {
                      const cfg = CHART_BADGE[k.chart_type] ?? { labelEn: k.chart_type, labelHi: k.chart_type, icon: BookOpen };
                      const Icon = cfg.icon;
                      const isActive = selectedChart === k.chart_type;
                      return (
                        <button
                          key={k.id}
                          onClick={() => setSelectedChart(k.chart_type)}
                          className={`inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border font-semibold transition-colors ${
                            isActive
                              ? 'bg-sacred-gold-dark text-white border-sacred-gold-dark'
                              : 'bg-white border-sacred-gold/30 text-sacred-gold-dark hover:bg-sacred-gold/10'
                          }`}
                        >
                          <Icon className="w-3.5 h-3.5" />
                          {isHi ? cfg.labelHi : cfg.labelEn}
                        </button>
                      );
                    })}
                  </div>
                  {chartLoading ? (
                    <div className="flex items-center justify-center h-80">
                      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
                    </div>
                  ) : chartData ? (
                    <div className="flex justify-center">
                      <div className="w-full max-w-md h-80">
                        <InteractiveKundli
                          chartData={chartData}
                          compact
                          hideCombust={selectedChart === 'lalkitab'}
                        />
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center h-80 text-muted-foreground text-sm">
                      {isHi ? 'कुंडली डेटा उपलब्ध नहीं' : 'Chart data not available'}
                    </div>
                  )}
                  <div className="text-center mt-3">
                    <button
                      onClick={() => onOpenFullProfile(client.id)}
                      className="inline-flex items-center gap-1 text-xs text-sacred-gold-dark hover:underline"
                    >
                      <ExternalLink className="w-3 h-3" />
                      {isHi ? 'पूर्ण विश्लेषण खोलें →' : 'Open full analysis →'}
                    </button>
                  </div>
                </>
              ) : (
                <div className="flex flex-col items-center justify-center h-80 text-muted-foreground text-sm">
                  <BookOpen className="w-12 h-12 mb-2 opacity-40" />
                  {isHi ? 'अभी तक कोई कुंडली नहीं' : 'No kundlis yet'}
                </div>
              )}

              {/* Palmistry photos */}
              {(client.profile_photo_url || client.left_hand_photo_url || client.right_hand_photo_url) && (
                <div className="mt-4 pt-4 border-t border-sacred-gold/10">
                  <p className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider mb-2">
                    {isHi ? 'चित्र' : 'Photos'}
                  </p>
                  <div className="flex gap-2 flex-wrap">
                    {client.profile_photo_url && (
                      <PhotoThumb src={client.profile_photo_url} label={isHi ? 'प्रोफ़ाइल' : 'Profile'} icon={UserIcon} />
                    )}
                    {client.left_hand_photo_url && (
                      <PhotoThumb src={client.left_hand_photo_url} label={isHi ? 'बायाँ हाथ' : 'Left Hand'} icon={Hand} />
                    )}
                    {client.right_hand_photo_url && (
                      <PhotoThumb src={client.right_hand_photo_url} label={isHi ? 'दायाँ हाथ' : 'Right Hand'} icon={Hand} />
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* RIGHT — actions + recent notes */}
            <div className="p-5 space-y-4">
              <div>
                <h3 className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider mb-2">
                  {isHi ? 'त्वरित क्रियाएँ' : 'Quick Actions'}
                </h3>
                <div className="space-y-1.5">
                  <ActionRow
                    icon={ExternalLink}
                    title={isHi ? 'पूर्ण प्रोफ़ाइल खोलें' : 'View Full Profile'}
                    subtitle={isHi ? 'सभी अनुभाग + टाइमलाइन' : 'All sections + timeline'}
                    onClick={() => onOpenFullProfile(client.id)}
                    primary
                  />
                  <ActionRow
                    icon={Clock}
                    title={isHi ? 'परामर्श निर्धारित करें' : 'Schedule Consultation'}
                    subtitle={isHi ? 'इस ग्राहक के लिए परामर्श बुक करें' : 'Book a session for this client'}
                    onClick={() => onOpenFullProfile(client.id)}
                  />
                  <ActionRow
                    icon={NotebookPen}
                    title={isHi ? 'नोट जोड़ें' : 'Add Note'}
                    subtitle={isHi ? 'इस ग्राहक के लिए नोट सहेजें' : 'Save a note for this client'}
                    onClick={() => onOpenFullProfile(client.id)}
                  />
                </div>
              </div>

              <div>
                <h3 className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <StickyNote className="w-3.5 h-3.5" />
                  {isHi ? 'हाल के नोट्स' : 'Recent Notes'}
                </h3>
                {notes.length === 0 ? (
                  <p className="text-xs text-muted-foreground italic">
                    {isHi ? 'अभी तक कोई नोट नहीं।' : 'No notes yet.'}
                  </p>
                ) : (
                  <div className="space-y-2">
                    {notes.map((n) => (
                      <div key={n.id} className="border-l-2 border-sacred-gold/40 pl-2 py-1">
                        <p className="text-xs text-foreground line-clamp-2">{n.content}</p>
                        <p className="text-[10px] text-muted-foreground mt-0.5">
                          {n.chart_type} · {n.created_at ? new Date(n.created_at).toLocaleDateString(isHi ? 'hi-IN' : 'en-IN') : ''}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="sticky bottom-0 bg-white border-t border-sacred-gold/20 p-4 rounded-b-2xl flex justify-between items-center">
          <div className="text-xs text-muted-foreground">
            {kundlis.length} {kundlis.length === 1 ? (isHi ? 'कुंडली' : 'chart') : (isHi ? 'कुंडलियाँ' : 'charts')} · {notes.length} {isHi ? 'नोट' : 'notes'}
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={onClose} className="border-sacred-gold/30">
              {isHi ? 'बंद करें' : 'Close'}
            </Button>
            <Button
              onClick={() => onOpenFullProfile(client?.id ?? '')}
              disabled={!client}
              className="bg-sacred-gold-dark text-white hover:bg-sacred-gold"
            >
              <ExternalLink className="w-4 h-4 mr-1.5" />
              {isHi ? 'पूर्ण प्रोफ़ाइल →' : 'Full Profile →'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

function PhotoThumb({ src, label, icon: Icon }: { src: string; label: string; icon: any }) {
  return (
    <div className="text-center">
      <img src={src} alt={label} className="w-16 h-16 object-cover rounded-lg border border-sacred-gold/40" />
      <p className="text-[10px] text-muted-foreground mt-1 flex items-center justify-center gap-1">
        <Icon className="w-2.5 h-2.5" /> {label}
      </p>
    </div>
  );
}

function ActionRow({ icon: Icon, title, subtitle, onClick, primary }: {
  icon: any; title: string; subtitle: string; onClick: () => void; primary?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 p-2.5 rounded-lg text-left transition-colors border ${
        primary
          ? 'border-sacred-gold/60 bg-sacred-gold/10 hover:bg-sacred-gold/20'
          : 'border-sacred-gold/20 hover:bg-sacred-gold/10'
      }`}
    >
      <Icon className={`w-4 h-4 shrink-0 ${primary ? 'text-sacred-gold-dark' : 'text-sacred-gold'}`} />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold text-foreground truncate">{title}</p>
        <p className="text-[11px] text-muted-foreground truncate">{subtitle}</p>
      </div>
      <ChevronRight className="w-4 h-4 text-muted-foreground shrink-0" />
    </button>
  );
}
