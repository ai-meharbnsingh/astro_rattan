import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Star, IndianRupee, Users, Calendar, Loader2, CheckCircle, Clock, Edit, Save, ToggleLeft, ToggleRight, Video } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import VideoSessionPanel from '@/components/consultations/VideoSessionPanel';

interface AstrologerStats {
  earnings: number;
  consultations: number;
  rating: number;
  upcoming: number;
}

interface AstrologerConsultation {
  id: string;
  client_name: string;
  client_email?: string;
  type: string;
  status: string;
  scheduled_at?: string;
  created_at: string;
  video_link?: string;
}

interface ActiveVideoSession {
  consultationId: string;
  roomName: string;
  videoLink: string;
  title: string;
  subtitle: string;
}

interface AstrologerProfile {
  bio: string;
  per_minute_rate: number;
  specializations: string;
  languages: string;
  is_available: boolean;
}

const statusColors: Record<string, string> = {
  requested: 'bg-yellow-100 text-yellow-700',
  accepted: 'bg-blue-500/20 text-blue-400',
  active: 'bg-green-500/20 text-green-400',
  completed: 'bg-cosmic-surface text-cosmic-text-secondary',
};

const formatPrice = (price: number) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

export default function AstrologerDashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState<AstrologerStats | null>(null);
  const [consultations, setConsultations] = useState<AstrologerConsultation[]>([]);
  const [profile, setProfile] = useState<AstrologerProfile>({ bio: '', per_minute_rate: 0, specializations: '', languages: '', is_available: true });
  const [loading, setLoading] = useState(true);
  const [editingProfile, setEditingProfile] = useState(false);
  const [saving, setSaving] = useState(false);
  const [specsInput, setSpecsInput] = useState('');
  const [langsInput, setLangsInput] = useState('');
  const [joiningVideoId, setJoiningVideoId] = useState<string | null>(null);
  const [activeVideoSession, setActiveVideoSession] = useState<ActiveVideoSession | null>(null);

  useEffect(() => {
    if (user?.role !== 'astrologer') { setLoading(false); return; }
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      const [statsRes, consRes, profileRes] = await Promise.allSettled([
        api.get('/api/astrologer/dashboard'),
        api.get('/api/astrologer/consultations'),
        api.get('/api/astrologer/profile'),
      ]);
      if (!cancelled) {
        if (statsRes.status === 'fulfilled') setStats(statsRes.value);
        if (consRes.status === 'fulfilled') {
          const list = Array.isArray(consRes.value) ? consRes.value : consRes.value.consultations || [];
          setConsultations(list.map((item: any) => ({
            id: item.id,
            client_name: item.client_name || item.user_name || 'Client',
            client_email: item.client_email,
            type: item.type,
            status: item.status,
            scheduled_at: item.scheduled_at,
            created_at: item.created_at,
            video_link: typeof item.video_link === 'string' ? item.video_link : undefined,
          })));
        }
        if (profileRes.status === 'fulfilled') {
          const p = profileRes.value as Partial<AstrologerProfile> & { rate?: number; specializations?: string | string[]; languages?: string | string[] };
          const specializations = Array.isArray(p.specializations) ? p.specializations.join(', ') : (p.specializations || '');
          const languages = Array.isArray(p.languages) ? p.languages.join(', ') : (p.languages || '');
          const normalizedProfile = {
            bio: p.bio || '',
            per_minute_rate: p.per_minute_rate ?? p.rate ?? 0,
            specializations,
            languages,
            is_available: p.is_available ?? true,
          };
          setProfile(normalizedProfile);
          setSpecsInput(normalizedProfile.specializations);
          setLangsInput(normalizedProfile.languages);
        }
        setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, [user?.role]);

  const acceptConsultation = async (id: string) => {
    try {
      await api.patch(`/api/consultations/${id}/accept`, {});
      setConsultations((prev) => prev.map((c) => (c.id === id ? { ...c, status: 'accepted' } : c)));
    } catch { /* empty */ }
  };

  const completeConsultation = async (id: string) => {
    try {
      await api.patch(`/api/consultations/${id}/complete`, {});
      setConsultations((prev) => prev.map((c) => (c.id === id ? { ...c, status: 'completed' } : c)));
    } catch { /* empty */ }
  };

  const joinVideoSession = async (consultation: AstrologerConsultation) => {
    setJoiningVideoId(consultation.id);
    try {
      const response = await api.post(`/api/consultation/${consultation.id}/video-link`, {});
      const videoLink = String(response.video_link ?? consultation.video_link ?? '');
      const roomName = String(response.room_name ?? videoLink.split('/').pop() ?? `AstroRattan-${consultation.id}`);
      const status = typeof response.status === 'string' ? response.status : consultation.status;

      setConsultations((prev) => prev.map((item) => (
        item.id === consultation.id
          ? { ...item, status, video_link: videoLink }
          : item
      )));
      setActiveVideoSession({
        consultationId: consultation.id,
        roomName,
        videoLink,
        title: `${consultation.client_name} — Video Consultation`,
        subtitle: 'Allow camera and microphone access in your browser to join the live session.',
      });
    } catch { /* empty */ }
    setJoiningVideoId(null);
  };

  const saveProfile = async () => {
    setSaving(true);
    try {
      const updated = {
        bio: profile.bio,
        per_minute_rate: profile.per_minute_rate,
        specializations: specsInput.trim(),
        languages: langsInput.trim(),
      };
      await api.patch('/api/astrologer/profile', updated);
      setProfile((prev) => ({ ...prev, ...updated }));
      setEditingProfile(false);
    } catch { /* empty */ }
    setSaving(false);
  };

  const toggleAvailability = async () => {
    try {
      const newVal = !profile.is_available;
      await api.patch('/api/astrologer/availability', { is_available: newVal });
      setProfile((prev) => ({ ...prev, is_available: newVal }));
    } catch { /* empty */ }
  };

  if (user?.role !== 'astrologer') {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <Star className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-cosmic-text mb-2">Astrologer Access Required</h2>
        <p className="text-cosmic-text-secondary">This dashboard is only accessible to verified astrologers.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
      </div>
    );
  }

  const statCards = [
    { label: 'Earnings', value: formatPrice(stats?.earnings ?? 0), icon: IndianRupee, color: 'bg-green-500/20 text-green-400' },
    { label: 'Consultations', value: stats?.consultations ?? 0, icon: Users, color: 'bg-blue-500/20 text-blue-400' },
    { label: 'Rating', value: (stats?.rating ?? 0).toFixed(1), icon: Star, color: 'bg-yellow-100 text-yellow-600' },
    { label: 'Pending', value: stats?.upcoming ?? 0, icon: Clock, color: 'bg-purple-100 text-purple-600' },
  ];

  return (
    <section className="max-w-6xl mx-auto py-24 px-4">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-sacred-gold flex items-center justify-center">
            <Star className="w-5 h-5 text-[#1a1a2e]" />
          </div>
          <div>
            <h2 className="text-2xl font-display font-bold text-cosmic-text">Astrologer Dashboard</h2>
            <p className="text-sm text-cosmic-text-secondary">Manage your consultations and profile</p>
          </div>
        </div>
        <Button onClick={toggleAvailability} variant="outline" className={profile.is_available ? 'border-green-300 text-green-400' : 'border-cosmic-text-muted text-cosmic-text-secondary'}>
          {profile.is_available ? <ToggleRight className="w-5 h-5 mr-2" /> : <ToggleLeft className="w-5 h-5 mr-2" />}
          {profile.is_available ? 'Available' : 'Unavailable'}
        </Button>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((s) => (
          <Card key={s.label} className="bg-cosmic-card border-0 shadow-soft">
            <CardContent className="p-5 flex items-center gap-4">
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${s.color}`}>
                <s.icon className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">{s.label}</p>
                <p className="text-2xl font-bold text-cosmic-text">{s.value}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="consultations" className="w-full">
        <TabsList className="bg-cosmic-surface mb-6">
          <TabsTrigger value="consultations" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Consultations</TabsTrigger>
          <TabsTrigger value="profile" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">Profile</TabsTrigger>
        </TabsList>

        <TabsContent value="consultations">
          {consultations.length === 0 ? (
            <div className="text-center py-12">
              <Calendar className="w-12 h-12 text-cosmic-text-muted mx-auto mb-3" />
              <p className="text-cosmic-text-secondary">No consultations yet.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {consultations.map((c) => (
                <Card key={c.id} className="bg-cosmic-card border-0 shadow-soft">
                  <CardContent className="p-4">
                    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                      <div>
                        <p className="font-medium text-cosmic-text">{c.client_name}</p>
                        <p className="text-sm text-cosmic-text-secondary capitalize">{c.type} consultation</p>
                        {c.scheduled_at && <p className="text-xs text-cosmic-text-muted">{new Date(c.scheduled_at).toLocaleString()}</p>}
                      </div>
                      <div className="flex flex-wrap items-center gap-3">
                        <Badge className={statusColors[c.status] || 'bg-cosmic-surface text-cosmic-text-secondary'}>{c.status}</Badge>
                        {c.status === 'requested' && (
                          <Button size="sm" onClick={() => acceptConsultation(c.id)} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">Accept</Button>
                        )}
                        {c.type === 'video' && (c.status === 'accepted' || c.status === 'active') && (
                          <Button
                            size="sm"
                            onClick={() => joinVideoSession(c)}
                            disabled={joiningVideoId === c.id}
                            className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark"
                          >
                            {joiningVideoId === c.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Video className="mr-1 h-4 w-4" />}
                            {c.video_link ? 'Rejoin' : 'Join'}
                          </Button>
                        )}
                        {(c.status === 'accepted' || c.status === 'active') && (
                          <Button size="sm" onClick={() => completeConsultation(c.id)} variant="outline" className="border-green-300 text-green-400">
                            <CheckCircle className="w-4 h-4 mr-1" />Complete
                          </Button>
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

        <TabsContent value="profile">
          <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-semibold text-cosmic-text">My Profile</h3>
                {!editingProfile ? (
                  <Button variant="outline" size="sm" onClick={() => setEditingProfile(true)}>
                    <Edit className="w-4 h-4 mr-1" />Edit
                  </Button>
                ) : (
                  <Button size="sm" onClick={saveProfile} disabled={saving} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
                    <Save className="w-4 h-4 mr-1" />{saving ? 'Saving...' : 'Save'}
                  </Button>
                )}
              </div>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Bio</label>
                  {editingProfile ? (
                    <Textarea value={profile.bio} onChange={(e) => setProfile({ ...profile, bio: e.target.value })} className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary text-sm">{profile.bio || 'No bio set'}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Rate per minute (INR)</label>
                  {editingProfile ? (
                    <Input type="number" value={profile.per_minute_rate} onChange={(e) => setProfile({ ...profile, per_minute_rate: Number(e.target.value) })} className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary text-sm">{formatPrice(profile.per_minute_rate)}</p>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Specializations (comma-separated)</label>
                  {editingProfile ? (
                    <Input value={specsInput} onChange={(e) => setSpecsInput(e.target.value)} placeholder="Vedic, Nadi, KP" className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <div className="flex flex-wrap gap-1">
                      {profile.specializations.split(',').map((s) => s.trim()).filter(Boolean).map((s) => <Badge key={s} variant="outline">{s}</Badge>)}
                      {!profile.specializations.trim() && <p className="text-sm text-cosmic-text-muted">None set</p>}
                    </div>
                  )}
                </div>
                <div>
                  <label className="text-sm font-medium text-cosmic-text mb-1 block">Languages (comma-separated)</label>
                  {editingProfile ? (
                    <Input value={langsInput} onChange={(e) => setLangsInput(e.target.value)} placeholder="Hindi, English, Sanskrit" className="bg-cosmic-card border-sacred-gold/15" />
                  ) : (
                    <p className="text-cosmic-text-secondary text-sm">{profile.languages.trim() || 'None set'}</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </section>
  );
}
