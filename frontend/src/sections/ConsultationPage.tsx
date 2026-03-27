import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Users, Star, Clock, Phone, Video, MessageSquare, Loader2, Calendar, Globe, VideoIcon, CircleDot } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import VideoSessionPanel from '@/components/consultations/VideoSessionPanel';

interface Astrologer {
  id: string;
  name: string;
  bio: string;
  rate: number;
  rating: number;
  specializations: string[];
  languages: string[];
  is_available: boolean;
  image_url?: string;
  total_consultations?: number;
}

interface Consultation {
  id: string;
  astrologer_name: string;
  type: string;
  status: string;
  scheduled_at?: string;
  created_at: string;
  duration_minutes?: number;
  notes?: string;
  video_link?: string;
}

interface VideoSessionState {
  consultationId: string;
  title: string;
  subtitle: string;
  roomName: string;
  videoLink: string;
}

type VideoCallStatus = 'waiting' | 'active' | 'ended' | null;

const statusColors: Record<string, string> = {
  requested: 'bg-yellow-100 text-yellow-700',
  accepted: 'bg-blue-100 text-blue-700',
  active: 'bg-green-500/20 text-green-700',
  completed: 'bg-cosmic-surface text-cosmic-text-secondary',
  cancelled: 'bg-red-500/20 text-red-400',
};

const typeIcons: Record<string, React.ReactNode> = {
  chat: <MessageSquare className="w-4 h-4" />,
  call: <Phone className="w-4 h-4" />,
  video: <Video className="w-4 h-4" />,
};

const formatPrice = (price: number) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

const toList = (value: unknown): string[] => {
  if (Array.isArray(value)) return value.map((item) => String(item).trim()).filter(Boolean);
  if (typeof value === 'string') return value.split(',').map((item) => item.trim()).filter(Boolean);
  return [];
};

const extractVideoLink = (item: Record<string, unknown>) => {
  if (typeof item.video_link === 'string' && item.video_link.startsWith('https://meet.jit.si/')) return item.video_link;
  if (typeof item.notes === 'string' && item.notes.startsWith('https://meet.jit.si/')) return item.notes;
  return undefined;
};

const normalizeAstrologer = (item: Record<string, unknown>): Astrologer => ({
  id: String(item.id ?? ''),
  name: String(item.display_name ?? item.name ?? 'Astrologer'),
  bio: String(item.bio ?? ''),
  rate: Number(item.per_minute_rate ?? item.rate ?? 0),
  rating: Number(item.rating ?? 0),
  specializations: toList(item.specializations),
  languages: toList(item.languages),
  is_available: Boolean(item.is_available),
  image_url: typeof item.image_url === 'string' ? item.image_url : undefined,
  total_consultations: typeof item.total_consultations === 'number' ? item.total_consultations : undefined,
});

const normalizeConsultation = (item: Record<string, unknown>): Consultation => ({
  id: String(item.id ?? ''),
  astrologer_name: String(item.astrologer_name ?? 'Astrologer'),
  type: String(item.type ?? 'chat'),
  status: String(item.status ?? 'requested'),
  scheduled_at: typeof item.scheduled_at === 'string' ? item.scheduled_at : undefined,
  created_at: String(item.created_at ?? ''),
  duration_minutes: typeof item.duration_minutes === 'number' ? item.duration_minutes : undefined,
  notes: typeof item.notes === 'string' ? item.notes : undefined,
  video_link: extractVideoLink(item),
});

export default function ConsultationPage() {
  const { isAuthenticated } = useAuth();
  const [astrologers, setAstrologers] = useState<Astrologer[]>([]);
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [loading, setLoading] = useState(true);
  const [booking, setBooking] = useState<string | null>(null);
  const [bookingType, setBookingType] = useState('chat');
  const [specFilter, setSpecFilter] = useState('all');
  const [availFilter, setAvailFilter] = useState('all');
  const [joiningVideoId, setJoiningVideoId] = useState<string | null>(null);
  const [activeVideoSession, setActiveVideoSession] = useState<VideoSessionState | null>(null);
  const [videoStatuses, setVideoStatuses] = useState<Record<string, VideoCallStatus>>({});
  const [startingVideoId, setStartingVideoId] = useState<string | null>(null);

  /** Poll video-status for all accepted/active video consultations */
  const fetchVideoStatuses = useCallback(async (items: Consultation[]) => {
    const videoItems = items.filter(
      (c) => c.type === 'video' && ['accepted', 'active', 'requested'].includes(c.status),
    );
    const statuses: Record<string, VideoCallStatus> = {};
    await Promise.allSettled(
      videoItems.map(async (c) => {
        try {
          const res = await api.get(`/api/consultation/${c.id}/video-status`);
          statuses[c.id] = (res.status as VideoCallStatus) ?? null;
        } catch {
          statuses[c.id] = null;
        }
      }),
    );
    setVideoStatuses((prev) => ({ ...prev, ...statuses }));
  }, []);

  /** Start a video call via the new start-video endpoint */
  const handleStartVideo = useCallback(async (consultation: Consultation) => {
    setStartingVideoId(consultation.id);
    try {
      const res = await api.post(`/api/consultation/${consultation.id}/start-video`, {});
      const roomUrl = String(res.room_url ?? '');
      const updatedStatus = String(res.status ?? 'active');

      // Update consultation in local state
      setConsultations((prev) =>
        prev.map((item) =>
          item.id === consultation.id
            ? { ...item, status: updatedStatus, video_link: roomUrl }
            : item,
        ),
      );
      setVideoStatuses((prev) => ({ ...prev, [consultation.id]: 'active' }));

      // Open the video room URL in a new tab
      if (roomUrl) {
        window.open(roomUrl, '_blank', 'noopener,noreferrer');
      }
    } catch {
      /* empty */
    }
    setStartingVideoId(null);
  }, []);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      try {
        const data = await api.get('/api/astrologers');
        if (!cancelled) {
          const list = Array.isArray(data) ? data : data.astrologers || [];
          setAstrologers(list.map((item: Record<string, unknown>) => normalizeAstrologer(item)));
        }
      } catch { /* empty */ }
      if (isAuthenticated) {
        try {
          const data = await api.get('/api/consultations');
          if (!cancelled) {
            const list = Array.isArray(data) ? data : data.consultations || [];
            const normalized = list.map((item: Record<string, unknown>) => normalizeConsultation(item));
            setConsultations(normalized);
            fetchVideoStatuses(normalized);
          }
        } catch { /* empty */ }
      }
      if (!cancelled) setLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  const allSpecs = Array.from(new Set(astrologers.flatMap((a) => a.specializations || [])));

  const filtered = astrologers.filter((a) => {
    if (specFilter !== 'all' && !(a.specializations || []).includes(specFilter)) return false;
    if (availFilter === 'available' && !a.is_available) return false;
    return true;
  });

  const handleBook = async (astrologerId: string) => {
    setBooking(astrologerId);
    try {
      const data = await api.post('/api/consultations/book', {
        astrologer_id: astrologerId,
        type: bookingType,
      });
      const newConsultation = normalizeConsultation(data.consultation || data);
      setConsultations((prev) => [newConsultation, ...prev]);
    } catch { /* empty */ }
    setBooking(null);
  };

  const openVideoSession = async (consultation: Consultation) => {
    setJoiningVideoId(consultation.id);
    try {
      const response = await api.post(`/api/consultation/${consultation.id}/video-link`, {});
      const videoLink = String(response.video_link ?? consultation.video_link ?? '');
      const roomName = String(response.room_name ?? videoLink.split('/').pop() ?? `AstroRattan-${consultation.id}`);
      const status = typeof response.status === 'string' ? response.status : consultation.status;

      setConsultations((prev) => prev.map((item) => (
        item.id === consultation.id
          ? { ...item, status, video_link: videoLink, notes: videoLink }
          : item
      )));
      setActiveVideoSession({
        consultationId: consultation.id,
        title: `${consultation.astrologer_name} — Video Consultation`,
        subtitle: 'Allow camera and microphone access in your browser to join the live session.',
        roomName,
        videoLink,
      });
    } catch { /* empty */ }
    setJoiningVideoId(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
      </div>
    );
  }

  return (
    <section className="max-w-6xl mx-auto py-24 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-4">
          <Users className="w-4 h-4" />Consultations
        </div>
        <h2 className="text-3xl sm:text-4xl font-display font-bold text-cosmic-text mb-2">
          Consult with <span className="text-gradient-indigo">Expert Astrologers</span>
        </h2>
        <p className="text-cosmic-text-secondary">Book a personalized session via chat, call, or video</p>
      </div>

      <Tabs defaultValue="astrologers" className="w-full">
        <TabsList className="grid grid-cols-2 bg-cosmic-surface mb-8 max-w-xs mx-auto">
          <TabsTrigger value="astrologers" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-white">Astrologers</TabsTrigger>
          <TabsTrigger value="my" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-white">My Bookings</TabsTrigger>
        </TabsList>

        <TabsContent value="astrologers">
          {/* Filters */}
          <div className="flex flex-wrap gap-3 mb-6">
            <Select value={specFilter} onValueChange={setSpecFilter}>
              <SelectTrigger className="w-48 bg-cosmic-card border-sacred-gold/15">
                <SelectValue placeholder="Specialization" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Specializations</SelectItem>
                {allSpecs.map((s) => (
                  <SelectItem key={s} value={s}>{s}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={availFilter} onValueChange={setAvailFilter}>
              <SelectTrigger className="w-40 bg-cosmic-card border-sacred-gold/15">
                <SelectValue placeholder="Availability" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="available">Available Now</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {filtered.length === 0 ? (
            <div className="text-center py-12 text-cosmic-text-secondary">No astrologers found matching your filters.</div>
          ) : (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {filtered.map((astrologer) => (
                <Card key={astrologer.id} className="bg-cosmic-card border-0 shadow-soft hover:shadow-soft-lg transition-all">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-3">
                      <div className="w-12 h-12 rounded-full bg-sacred-gold/10 flex items-center justify-center text-sacred-gold font-bold text-lg">
                        {astrologer.name.charAt(0)}
                      </div>
                      <Badge className={astrologer.is_available ? 'bg-green-500/20 text-green-700' : 'bg-cosmic-surface text-cosmic-text-secondary'}>
                        {astrologer.is_available ? 'Available' : 'Busy'}
                      </Badge>
                    </div>
                    <h3 className="font-display font-semibold text-cosmic-text text-lg">{astrologer.name}</h3>
                    <p className="text-sm text-cosmic-text-secondary mt-1 line-clamp-2">{astrologer.bio}</p>
                    <div className="flex items-center gap-3 mt-3 text-sm text-cosmic-text-secondary">
                      <span className="flex items-center gap-1"><Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />{astrologer.rating.toFixed(1)}</span>
                      <span className="flex items-center gap-1"><Clock className="w-4 h-4" />{formatPrice(astrologer.rate)}/min</span>
                    </div>
                    {astrologer.languages && astrologer.languages.length > 0 && (
                      <div className="flex items-center gap-1 mt-2 text-xs text-cosmic-text-muted">
                        <Globe className="w-3 h-3" />{astrologer.languages.join(', ')}
                      </div>
                    )}
                    <div className="flex flex-wrap gap-1 mt-3">
                      {(astrologer.specializations || []).slice(0, 3).map((s) => (
                        <Badge key={s} variant="outline" className="text-xs">{s}</Badge>
                      ))}
                    </div>
                    {isAuthenticated && astrologer.is_available && (
                      <div className="mt-4 flex gap-2">
                        <Select value={bookingType} onValueChange={setBookingType}>
                          <SelectTrigger className="flex-1 bg-cosmic-card border-sacred-gold/15" size="sm">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="chat"><span className="flex items-center gap-1"><MessageSquare className="w-3 h-3" />Chat</span></SelectItem>
                            <SelectItem value="call"><span className="flex items-center gap-1"><Phone className="w-3 h-3" />Call</span></SelectItem>
                            <SelectItem value="video"><span className="flex items-center gap-1"><Video className="w-3 h-3" />Video</span></SelectItem>
                          </SelectContent>
                        </Select>
                        <Button size="sm" onClick={() => handleBook(astrologer.id)} disabled={booking === astrologer.id} className="bg-sacred-gold text-white hover:bg-sacred-gold-dark">
                          {booking === astrologer.id ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Book'}
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="my">
          {!isAuthenticated ? (
            <div className="text-center py-12 text-cosmic-text-secondary">Please sign in to view your consultations.</div>
          ) : consultations.length === 0 ? (
            <div className="text-center py-12">
              <Calendar className="w-12 h-12 text-cosmic-text-muted mx-auto mb-3" />
              <p className="text-cosmic-text-secondary">No consultations yet. Book one above!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {consultations.map((c) => (
                <Card key={c.id} className="bg-cosmic-card border-0 shadow-soft">
                  <CardContent className="p-4">
                    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 rounded-full bg-sacred-gold/10 flex items-center justify-center text-sacred-gold">
                          {typeIcons[c.type] || <MessageSquare className="w-4 h-4" />}
                        </div>
                        <div>
                          <p className="font-medium text-cosmic-text">{c.astrologer_name}</p>
                          <p className="text-sm text-cosmic-text-secondary capitalize">{c.type} consultation</p>
                          {c.scheduled_at && <p className="text-xs text-cosmic-text-muted">{new Date(c.scheduled_at).toLocaleString()}</p>}
                        </div>
                      </div>
                      <div>
                        <div className="flex flex-wrap items-center justify-end gap-3">
                          <Badge className={statusColors[c.status] || 'bg-cosmic-surface text-cosmic-text-secondary'}>
                            {c.status}
                          </Badge>
                          {/* Video call status indicator */}
                          {c.type === 'video' && videoStatuses[c.id] && (
                            <Badge className={
                              videoStatuses[c.id] === 'active'
                                ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                                : videoStatuses[c.id] === 'waiting'
                                ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                                : 'bg-cosmic-surface text-cosmic-text-secondary'
                            }>
                              <CircleDot className="w-3 h-3 mr-1" />
                              {videoStatuses[c.id] === 'active' ? 'In Progress' : videoStatuses[c.id] === 'waiting' ? 'Waiting' : 'Ended'}
                            </Badge>
                          )}
                          {/* Join Video Call button — uses start-video endpoint */}
                          {c.type === 'video' && (c.status === 'accepted' || c.status === 'active') && (
                            <Button
                              size="sm"
                              onClick={() => handleStartVideo(c)}
                              disabled={startingVideoId === c.id}
                              className="bg-sacred-gold text-white hover:bg-sacred-gold-dark border border-sacred-gold/20"
                            >
                              {startingVideoId === c.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <VideoIcon className="mr-2 h-4 w-4" />}
                              Join Video Call
                            </Button>
                          )}
                          {/* Existing embedded session button */}
                          {c.type === 'video' && (c.status === 'accepted' || c.status === 'active') && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => openVideoSession(c)}
                              disabled={joiningVideoId === c.id}
                              className="border-sacred-gold/20 text-cosmic-text hover:bg-sacred-gold/10"
                            >
                              {joiningVideoId === c.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Video className="mr-2 h-4 w-4" />}
                              {c.video_link ? 'Rejoin Embedded' : 'Embed Session'}
                            </Button>
                          )}
                        </div>
                        {c.type === 'video' && c.status === 'requested' && (
                          <p className="mt-2 text-xs text-cosmic-text-muted">Video room unlocks after the astrologer accepts the booking.</p>
                        )}
                      </div>
                    </div>
                    {activeVideoSession?.consultationId === c.id && (
                      <div className="mt-4">
                        <VideoSessionPanel
                          title={activeVideoSession.title}
                          subtitle={activeVideoSession.subtitle}
                          roomName={activeVideoSession.roomName}
                          videoLink={activeVideoSession.videoLink}
                          onClose={() => setActiveVideoSession(null)}
                        />
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </section>
  );
}
