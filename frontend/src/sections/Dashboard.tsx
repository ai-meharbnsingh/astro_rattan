import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Loader2,
  Star,
  MessageSquare,
  Calendar,
  ShoppingBag,
  Sparkles,
  Clock,
  Moon,
  Sun,
  Eye,
  FileText,
  ArrowRight,
  User,
  Hash,
  Palette,
  Flame,
  Award,
  Zap,
  TrendingUp,
  TrendingDown,
  Minus,
  CheckCircle,
  Gift,
  Bell,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface PanchangSnapshot {
  tithi: string;
  nakshatra: string;
  yoga: string;
  karana: string;
  sunrise: string;
  sunset: string;
}

interface HoroscopeData {
  general: string;
  lucky_numbers?: number[];
  lucky_color?: string;
}

interface SavedKundli {
  id: number;
  name: string;
  date_of_birth?: string;
  created_at?: string;
}

interface Consultation {
  id: number;
  astrologer_name?: string;
  date?: string;
  time?: string;
  status: string;
  type?: string;
}

interface ActivitySummary {
  kundli_count: number;
  order_count: number;
  consultation_count: number;
  ai_chats: number;
}

interface DashaPeriod {
  planet: string;
  start_date: string;
  end_date: string;
  interpretation?: string;
}

interface DashaData {
  mahadasha?: DashaPeriod;
  antardasha?: DashaPeriod;
}

interface TransitData {
  planet: string;
  house: number;
  sign: string;
  impact: 'positive' | 'challenging' | 'neutral';
  interpretation: string;
}

interface KarmaProfile {
  streak: number;
  total_points: number;
  level: number;
  level_progress: number;
  next_level_points: number;
  badges: { name: string; icon: string; earned_at: string }[];
  checked_in_today: boolean;
}

interface CosmicCalendarEvent {
  name: string;
  date: string;
  type: string;
  description?: string;
}

interface Recommendation {
  text: string;
  icon: 'business' | 'caution' | 'spiritual' | 'remedy';
  color: string;
}

const zodiacSigns = [
  { name: 'Aries', symbol: '\u2648', start: [3, 21], end: [4, 19] },
  { name: 'Taurus', symbol: '\u2649', start: [4, 20], end: [5, 20] },
  { name: 'Gemini', symbol: '\u264A', start: [5, 21], end: [6, 20] },
  { name: 'Cancer', symbol: '\u264B', start: [6, 21], end: [7, 22] },
  { name: 'Leo', symbol: '\u264C', start: [7, 23], end: [8, 22] },
  { name: 'Virgo', symbol: '\u264D', start: [8, 23], end: [9, 22] },
  { name: 'Libra', symbol: '\u264E', start: [9, 23], end: [10, 22] },
  { name: 'Scorpio', symbol: '\u264F', start: [10, 23], end: [11, 21] },
  { name: 'Sagittarius', symbol: '\u2650', start: [11, 22], end: [12, 21] },
  { name: 'Capricorn', symbol: '\u2651', start: [12, 22], end: [1, 19] },
  { name: 'Aquarius', symbol: '\u2652', start: [1, 20], end: [2, 18] },
  { name: 'Pisces', symbol: '\u2653', start: [2, 19], end: [3, 20] },
];

function getZodiacSign(dateStr?: string) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  const month = d.getMonth() + 1;
  const day = d.getDate();
  for (const sign of zodiacSigns) {
    const [sm, sd] = sign.start;
    const [em, ed] = sign.end;
    if (sm <= em) {
      if ((month === sm && day >= sd) || (month === em && day <= ed) || (month > sm && month < em)) return sign;
    } else {
      if ((month === sm && day >= sd) || (month === em && day <= ed) || month > sm || month < em) return sign;
    }
  }
  return zodiacSigns[0];
}

const fallbackPanchang: PanchangSnapshot = {
  tithi: 'Shukla Paksha - Pratipada',
  nakshatra: 'Ashwini',
  yoga: 'Vriddhi',
  karana: 'Bava',
  sunrise: '06:45 AM',
  sunset: '05:52 PM',
};

const fallbackHoroscope: HoroscopeData = {
  general: 'Today brings positive energy. The planets align in your favor, creating opportunities for growth and self-discovery.',
  lucky_numbers: [3, 7, 11],
  lucky_color: 'Gold',
};

const quickActions = [
  { label: 'Generate Kundli', icon: Star, href: '/kundli', color: 'from-purple-500/20 to-purple-900/20 border-purple-500/30', iconColor: 'text-purple-400' },
  { label: 'Ask AI', icon: MessageSquare, href: '/ai-chat', color: 'from-blue-500/20 to-blue-900/20 border-blue-500/30', iconColor: 'text-blue-400' },
  { label: 'View Panchang', icon: Calendar, href: '/panchang', color: 'from-amber-500/20 to-amber-900/20 border-amber-500/30', iconColor: 'text-amber-400' },
  { label: 'Shop', icon: ShoppingBag, href: '/shop', color: 'from-green-500/20 to-green-900/20 border-green-500/30', iconColor: 'text-green-400' },
];

export default function Dashboard() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [panchang, setPanchang] = useState<PanchangSnapshot>(fallbackPanchang);
  const [horoscope, setHoroscope] = useState<HoroscopeData>(fallbackHoroscope);
  const [savedKundlis, setSavedKundlis] = useState<SavedKundli[]>([]);
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [activity, setActivity] = useState<ActivitySummary>({ kundli_count: 0, order_count: 0, consultation_count: 0, ai_chats: 0 });
  const [userProfile, setUserProfile] = useState<{ date_of_birth?: string }>({});
  const [loading, setLoading] = useState(true);
  const [dashaData, setDashaData] = useState<DashaData | null>(null);
  const [transits, setTransits] = useState<TransitData[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [karmaProfile, setKarmaProfile] = useState<KarmaProfile | null>(null);
  const [checkingIn, setCheckingIn] = useState(false);
  const [cosmicEvents, setCosmicEvents] = useState<CosmicCalendarEvent[]>([]);
  const [nextMuhurat, setNextMuhurat] = useState<{ event: string; date: string } | null>(null);

  const today = new Date();
  const todayStr = today.toISOString().split('T')[0];
  const dateDisplay = today.toLocaleDateString('en-IN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const userSign = getZodiacSign(userProfile.date_of_birth);
  const luckyNumbers = horoscope.lucky_numbers || [3, 7, 11];
  const luckyColor = horoscope.lucky_color || 'Gold';

  const generateRecommendations = useCallback((transitList: TransitData[], dasha: DashaData | null): Recommendation[] => {
    const recs: Recommendation[] = [];
    const hasPositiveJupiter = transitList.some(t => t.planet.toLowerCase().includes('jupiter') && t.impact === 'positive');
    const hasChallengingSaturn = transitList.some(t => t.planet.toLowerCase().includes('saturn') && t.impact === 'challenging');
    const hasPositiveVenus = transitList.some(t => t.planet.toLowerCase().includes('venus') && t.impact === 'positive');
    const hasChallengingMars = transitList.some(t => t.planet.toLowerCase().includes('mars') && t.impact === 'challenging');
    const hasRahu = transitList.some(t => t.planet.toLowerCase().includes('rahu'));

    if (hasPositiveJupiter) {
      recs.push({ text: 'Good day for business decisions and financial growth', icon: 'business', color: 'text-green-400' });
    }
    if (hasChallengingSaturn) {
      recs.push({ text: 'Avoid major purchases today — Saturn advises patience', icon: 'caution', color: 'text-amber-400' });
    }
    if (hasRahu) {
      recs.push({ text: 'Meditation recommended during Rahu Kaal for mental clarity', icon: 'spiritual', color: 'text-purple-400' });
    }
    if (hasPositiveVenus) {
      recs.push({ text: 'Favorable day for relationships and creative pursuits', icon: 'remedy', color: 'text-pink-400' });
    }
    if (hasChallengingMars) {
      recs.push({ text: 'Channel energy into exercise — avoid confrontations', icon: 'caution', color: 'text-red-400' });
    }
    if (dasha?.mahadasha?.planet?.toLowerCase().includes('jupiter')) {
      recs.push({ text: 'Wear yellow for Jupiter\'s blessing during your Mahadasha', icon: 'remedy', color: 'text-sacred-gold' });
    }

    // Ensure at least some recommendations
    if (recs.length === 0) {
      recs.push(
        { text: 'Stay mindful and observe planetary energies today', icon: 'spiritual', color: 'text-purple-400' },
        { text: 'A balanced day — focus on routine tasks', icon: 'business', color: 'text-green-400' },
        { text: 'Light a lamp during evening for positive vibrations', icon: 'remedy', color: 'text-sacred-gold' },
      );
    }

    return recs.slice(0, 4);
  }, []);

  const handleCheckIn = async () => {
    setCheckingIn(true);
    try {
      const res = await api.post('/api/karma/checkin', {});
      setKarmaProfile(prev => prev ? {
        ...prev,
        streak: res.streak ?? (prev.streak + 1),
        total_points: res.total_points ?? (prev.total_points + 10),
        checked_in_today: true,
      } : prev);
    } catch {
      // silently handle
    } finally {
      setCheckingIn(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    const loadDashboard = async () => {
      setLoading(true);

      // First fetch profile to get DOB for horoscope
      let dob: string | undefined;
      try {
        const me = await api.get('/api/auth/me');
        if (!cancelled) {
          setUserProfile({ date_of_birth: me.date_of_birth });
          dob = me.date_of_birth;
        }
      } catch {
        // profile fetch failed, continue without DOB
      }

      // Determine sign for horoscope
      const sign = getZodiacSign(dob);
      const signName = sign ? sign.name.toLowerCase() : 'aries';

      // Fetch remaining data in parallel
      const [panchangRes, horoscopeRes, kundliRes, consultRes, historyRes] = await Promise.allSettled([
        api.get(`/api/panchang?date=${todayStr}&latitude=28.6139&longitude=77.2090`),
        api.get(`/api/horoscope/${signName}?period=daily`),
        api.get('/api/kundli/list'),
        api.get('/api/consultations'),
        api.get('/api/auth/history'),
      ]);

      if (cancelled) return;

      if (panchangRes.status === 'fulfilled' && panchangRes.value) {
        const p = panchangRes.value;
        setPanchang({
          tithi: p.tithi?.name || p.tithi || fallbackPanchang.tithi,
          nakshatra: p.nakshatra?.name || p.nakshatra || fallbackPanchang.nakshatra,
          yoga: p.yoga?.name || p.yoga || fallbackPanchang.yoga,
          karana: p.karana?.name || p.karana || fallbackPanchang.karana,
          sunrise: p.sunrise || fallbackPanchang.sunrise,
          sunset: p.sunset || fallbackPanchang.sunset,
        });
      }

      if (horoscopeRes.status === 'fulfilled' && horoscopeRes.value) {
        const h = horoscopeRes.value;
        setHoroscope({
          general: h.content || h.general || fallbackHoroscope.general,
          lucky_numbers: h.lucky_numbers || fallbackHoroscope.lucky_numbers,
          lucky_color: h.lucky_color || fallbackHoroscope.lucky_color,
        });
      }

      if (kundliRes.status === 'fulfilled') {
        const list = Array.isArray(kundliRes.value) ? kundliRes.value : kundliRes.value?.kundlis || [];
        setSavedKundlis(list.slice(0, 5));
      }

      if (consultRes.status === 'fulfilled') {
        const list = Array.isArray(consultRes.value) ? consultRes.value : consultRes.value?.consultations || [];
        const upcoming = list.filter((c: Consultation) => c.status === 'booked' || c.status === 'confirmed' || c.status === 'scheduled');
        setConsultations(upcoming.slice(0, 5));
      }

      if (historyRes.status === 'fulfilled') {
        const h = historyRes.value;
        setActivity({
          kundli_count: h.kundlis?.count ?? 0,
          order_count: h.orders?.count ?? 0,
          consultation_count: h.consultations?.count ?? 0,
          ai_chats: h.ai_chats?.count ?? 0,
        });
      }

      // Fetch saved kundli list for dasha data
      const savedList = kundliRes.status === 'fulfilled'
        ? (Array.isArray(kundliRes.value) ? kundliRes.value : kundliRes.value?.kundlis || [])
        : [];

      // Second wave: dasha, transits, karma, cosmic calendar
      const firstKundliId = savedList.length > 0 ? savedList[0].id : null;

      const [dashaRes, transitRes, karmaRes, cosmicRes] = await Promise.allSettled([
        firstKundliId ? api.get(`/api/kundli/${firstKundliId}/dasha`) : Promise.reject('no kundli'),
        api.get('/api/cosmic-calendar/today'),
        api.get('/api/karma/profile'),
        api.get('/api/cosmic-calendar/upcoming'),
      ]);

      if (cancelled) return;

      let fetchedDasha: DashaData | null = null;
      if (dashaRes.status === 'fulfilled' && dashaRes.value) {
        const d = dashaRes.value;
        fetchedDasha = {
          mahadasha: d.mahadasha || d.current_mahadasha || null,
          antardasha: d.antardasha || d.current_antardasha || null,
        };
        setDashaData(fetchedDasha);
      }

      let fetchedTransits: TransitData[] = [];
      if (transitRes.status === 'fulfilled' && transitRes.value) {
        const t = transitRes.value;
        fetchedTransits = Array.isArray(t.transits) ? t.transits : Array.isArray(t) ? t : [];
        setTransits(fetchedTransits);
      }

      // Generate recommendations from transits and dasha
      setRecommendations(generateRecommendations(fetchedTransits, fetchedDasha));

      if (karmaRes.status === 'fulfilled' && karmaRes.value) {
        setKarmaProfile(karmaRes.value);
      }

      if (cosmicRes.status === 'fulfilled' && cosmicRes.value) {
        const events = Array.isArray(cosmicRes.value) ? cosmicRes.value : cosmicRes.value?.events || [];
        setCosmicEvents(events.slice(0, 3));
        // Check for upcoming muhurat
        const muhurat = events.find((e: CosmicCalendarEvent) => e.type === 'muhurat');
        if (muhurat) setNextMuhurat({ event: muhurat.name, date: muhurat.date });
      }

      setLoading(false);
    };

    loadDashboard();
    return () => { cancelled = true; };
  }, [isAuthenticated, todayStr]);

  if (authLoading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <User className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-sacred font-bold text-cosmic-text mb-2">Sign In Required</h2>
        <p className="text-cosmic-text-secondary mb-6">Please log in to view your personalized dashboard.</p>
        <Link to="/login">
          <Button className="btn-sacred">Sign In</Button>
        </Link>
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

  return (
    <section className="relative py-24 bg-transparent min-h-screen">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Welcome Banner */}
        <div className="bg-cosmic-card border border-sacred-gold/20 rounded-2xl p-6 sm:p-8 mb-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-sacred-gold/5 rounded-full -translate-y-1/2 translate-x-1/2 blur-3xl" />
          <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl sm:text-4xl font-sacred font-bold text-gradient-gold mb-2">
                Namaste, {user?.name || 'Seeker'}
              </h1>
              <p className="text-cosmic-text-secondary flex items-center gap-2">
                <Calendar className="w-4 h-4 text-sacred-gold" />
                {dateDisplay}
              </p>
              {userSign && (
                <p className="text-cosmic-text-secondary mt-1 flex items-center gap-2">
                  <span className="text-xl">{userSign.symbol}</span>
                  <span className="text-sacred-gold font-medium">{userSign.name}</span>
                </p>
              )}
            </div>
            <div className="flex items-center gap-3">
              <div className="text-center">
                <div className="flex items-center gap-1 text-sm text-cosmic-text-secondary">
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  <span>{panchang.sunrise}</span>
                </div>
              </div>
              <div className="w-px h-8 bg-sacred-gold/20" />
              <div className="text-center">
                <div className="flex items-center gap-1 text-sm text-cosmic-text-secondary">
                  <Moon className="w-3.5 h-3.5 text-blue-400" />
                  <span>{panchang.sunset}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

          {/* Today's Horoscope */}
          <div className="lg:col-span-2">
            <Card className="bg-cosmic-card border border-sacred-gold/20 h-full">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-sacred-gold" />
                    Today&apos;s Horoscope
                    {userSign && (
                      <Badge variant="outline" className="border-sacred-gold/30 text-sacred-gold ml-2">
                        {userSign.symbol} {userSign.name}
                      </Badge>
                    )}
                  </h2>
                  <Link to="/horoscope">
                    <Button variant="ghost" size="sm" className="text-sacred-gold hover:text-sacred-gold/80">
                      Full Reading <ArrowRight className="w-4 h-4 ml-1" />
                    </Button>
                  </Link>
                </div>
                <p className="text-cosmic-text leading-relaxed">{horoscope.general}</p>
              </CardContent>
            </Card>
          </div>

          {/* Panchang Snapshot */}
          <Card className="bg-cosmic-card border border-sacred-gold/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-sacred-gold" />
                  Panchang
                </h2>
                <Link to="/panchang">
                  <Button variant="ghost" size="sm" className="text-sacred-gold hover:text-sacred-gold/80">
                    <ArrowRight className="w-4 h-4" />
                  </Button>
                </Link>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center py-2 border-b border-sacred-gold/10">
                  <span className="text-cosmic-text-secondary text-sm">Tithi</span>
                  <span className="text-cosmic-text font-medium text-sm">{panchang.tithi}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-sacred-gold/10">
                  <span className="text-cosmic-text-secondary text-sm">Nakshatra</span>
                  <span className="text-cosmic-text font-medium text-sm">{panchang.nakshatra}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-sacred-gold/10">
                  <span className="text-cosmic-text-secondary text-sm">Yoga</span>
                  <span className="text-cosmic-text font-medium text-sm">{panchang.yoga}</span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-cosmic-text-secondary text-sm">Karana</span>
                  <span className="text-cosmic-text font-medium text-sm">{panchang.karana}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {quickActions.map((action) => (
            <Link key={action.label} to={action.href}>
              <Card className={`bg-gradient-to-br ${action.color} border hover:scale-[1.02] transition-transform cursor-pointer h-full`}>
                <CardContent className="p-5 text-center">
                  <div className="w-12 h-12 rounded-xl bg-cosmic-card/50 flex items-center justify-center mx-auto mb-3">
                    <action.icon className={`w-6 h-6 ${action.iconColor}`} />
                  </div>
                  <p className="text-cosmic-text font-medium text-sm">{action.label}</p>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>

        {/* Lucky Numbers & Colors + Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

          {/* Lucky Numbers & Color */}
          <Card className="bg-cosmic-card border border-sacred-gold/20">
            <CardContent className="p-6">
              <h2 className="font-sacred text-xl font-bold text-gradient-gold mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-sacred-gold" />
                Today&apos;s Lucky
              </h2>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Hash className="w-4 h-4 text-sacred-gold" />
                    <span className="text-cosmic-text-secondary text-sm">Lucky Numbers</span>
                  </div>
                  <div className="flex gap-2">
                    {luckyNumbers.map((n) => (
                      <span
                        key={n}
                        className="w-10 h-10 rounded-lg bg-sacred-gold/10 border border-sacred-gold/30 flex items-center justify-center text-sacred-gold font-bold"
                      >
                        {n}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Palette className="w-4 h-4 text-sacred-gold" />
                    <span className="text-cosmic-text-secondary text-sm">Lucky Color</span>
                  </div>
                  <Badge className="bg-sacred-gold/10 border border-sacred-gold/30 text-sacred-gold px-4 py-1.5">
                    {luckyColor}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <div className="lg:col-span-2">
            <Card className="bg-cosmic-card border border-sacred-gold/20 h-full">
              <CardContent className="p-6">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold mb-4 flex items-center gap-2">
                  <Clock className="w-5 h-5 text-sacred-gold" />
                  Recent Activity
                </h2>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="bg-cosmic-bg/50 rounded-xl p-4 text-center border border-sacred-gold/10">
                    <Star className="w-5 h-5 text-purple-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-cosmic-text">{activity.kundli_count}</p>
                    <p className="text-xs text-cosmic-text-secondary">Kundlis</p>
                  </div>
                  <div className="bg-cosmic-bg/50 rounded-xl p-4 text-center border border-sacred-gold/10">
                    <MessageSquare className="w-5 h-5 text-blue-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-cosmic-text">{activity.ai_chats}</p>
                    <p className="text-xs text-cosmic-text-secondary">AI Chats</p>
                  </div>
                  <div className="bg-cosmic-bg/50 rounded-xl p-4 text-center border border-sacred-gold/10">
                    <Eye className="w-5 h-5 text-green-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-cosmic-text">{activity.consultation_count}</p>
                    <p className="text-xs text-cosmic-text-secondary">Consultations</p>
                  </div>
                  <div className="bg-cosmic-bg/50 rounded-xl p-4 text-center border border-sacred-gold/10">
                    <ShoppingBag className="w-5 h-5 text-amber-400 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-cosmic-text">{activity.order_count}</p>
                    <p className="text-xs text-cosmic-text-secondary">Orders</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Current Dasha Period + Today's Transit Impact */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

          {/* Current Dasha Period Card */}
          <Card className="card-sacred border border-sacred-gold/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                  <Zap className="w-5 h-5 text-sacred-gold" />
                  Current Dasha Period
                </h2>
                {savedKundlis.length > 0 && (
                  <Link to="/kundli">
                    <Button variant="ghost" size="sm" className="text-sacred-gold hover:text-sacred-gold/80">
                      Full Chart <ArrowRight className="w-4 h-4 ml-1" />
                    </Button>
                  </Link>
                )}
              </div>
              {dashaData?.mahadasha ? (
                <div className="space-y-4">
                  {/* Mahadasha */}
                  <div className="p-3 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sacred-gold font-medium text-sm">Mahadasha</span>
                      <Badge variant="outline" className="border-sacred-gold/30 text-sacred-gold text-xs">
                        {dashaData.mahadasha.planet}
                      </Badge>
                    </div>
                    <p className="text-cosmic-text-secondary text-xs mb-2">
                      {dashaData.mahadasha.start_date && new Date(dashaData.mahadasha.start_date).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })}
                      {' - '}
                      {dashaData.mahadasha.end_date && new Date(dashaData.mahadasha.end_date).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })}
                    </p>
                    {/* Progress bar */}
                    {(() => {
                      const start = new Date(dashaData.mahadasha.start_date).getTime();
                      const end = new Date(dashaData.mahadasha.end_date).getTime();
                      const now = Date.now();
                      const progress = Math.min(100, Math.max(0, ((now - start) / (end - start)) * 100));
                      return (
                        <div className="w-full bg-cosmic-bg rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-sacred-gold to-sacred-saffron h-2 rounded-full transition-all"
                            style={{ width: `${progress}%` }}
                          />
                        </div>
                      );
                    })()}
                    {dashaData.mahadasha.interpretation && (
                      <p className="text-cosmic-text-secondary text-xs mt-2 leading-relaxed">{dashaData.mahadasha.interpretation}</p>
                    )}
                  </div>
                  {/* Antardasha */}
                  {dashaData.antardasha && (
                    <div className="p-3 bg-cosmic-bg/50 rounded-xl border border-purple-500/10">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-purple-400 font-medium text-sm">Antardasha</span>
                        <Badge variant="outline" className="border-purple-500/30 text-purple-400 text-xs">
                          {dashaData.antardasha.planet}
                        </Badge>
                      </div>
                      <p className="text-cosmic-text-secondary text-xs mb-2">
                        {dashaData.antardasha.start_date && new Date(dashaData.antardasha.start_date).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })}
                        {' - '}
                        {dashaData.antardasha.end_date && new Date(dashaData.antardasha.end_date).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })}
                      </p>
                      {(() => {
                        const start = new Date(dashaData.antardasha.start_date).getTime();
                        const end = new Date(dashaData.antardasha.end_date).getTime();
                        const now = Date.now();
                        const progress = Math.min(100, Math.max(0, ((now - start) / (end - start)) * 100));
                        return (
                          <div className="w-full bg-cosmic-bg rounded-full h-1.5">
                            <div
                              className="bg-gradient-to-r from-purple-500 to-purple-400 h-1.5 rounded-full transition-all"
                              style={{ width: `${progress}%` }}
                            />
                          </div>
                        );
                      })()}
                      {dashaData.antardasha.interpretation && (
                        <p className="text-cosmic-text-secondary text-xs mt-2 leading-relaxed">{dashaData.antardasha.interpretation}</p>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-6">
                  <Zap className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
                  <p className="text-cosmic-text-secondary text-sm mb-3">Generate a Kundli to see your Dasha periods</p>
                  <Link to="/kundli">
                    <Button size="sm" className="btn-sacred">Generate Kundli</Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Today's Transit Impact */}
          <Card className="card-sacred border border-sacred-gold/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-sacred-gold" />
                  Today&apos;s Transit Impact
                </h2>
              </div>
              {transits.length > 0 ? (
                <div className="space-y-2 max-h-[320px] overflow-y-auto pr-1">
                  {transits.map((transit, idx) => {
                    const impactIcon = transit.impact === 'positive'
                      ? <TrendingUp className="w-4 h-4 text-green-400" />
                      : transit.impact === 'challenging'
                        ? <TrendingDown className="w-4 h-4 text-red-400" />
                        : <Minus className="w-4 h-4 text-amber-400" />;
                    const impactBorder = transit.impact === 'positive'
                      ? 'border-green-500/20'
                      : transit.impact === 'challenging'
                        ? 'border-red-500/20'
                        : 'border-amber-500/20';
                    const impactBg = transit.impact === 'positive'
                      ? 'bg-green-500/5'
                      : transit.impact === 'challenging'
                        ? 'bg-red-500/5'
                        : 'bg-amber-500/5';
                    return (
                      <div key={idx} className={`flex items-start gap-3 p-3 rounded-xl border ${impactBorder} ${impactBg}`}>
                        <div className="mt-0.5 shrink-0">{impactIcon}</div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-0.5">
                            <span className="text-cosmic-text font-medium text-sm">{transit.planet}</span>
                            <span className="text-cosmic-text-secondary text-xs">in House {transit.house}</span>
                            {transit.sign && (
                              <Badge variant="outline" className="border-sacred-gold/20 text-cosmic-text-secondary text-xs px-1.5 py-0">
                                {transit.sign}
                              </Badge>
                            )}
                          </div>
                          <p className="text-cosmic-text-secondary text-xs leading-relaxed">{transit.interpretation}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-6">
                  <TrendingUp className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
                  <p className="text-cosmic-text-secondary text-sm">Transit data will appear when your chart is generated</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Personalized Recommendations */}
        {recommendations.length > 0 && (
          <div className="mb-8">
            <Card className="card-sacred border border-sacred-gold/20">
              <CardContent className="p-6">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold mb-4 flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-sacred-gold" />
                  Personalized Recommendations
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {recommendations.map((rec, idx) => {
                    const recIcon = rec.icon === 'business'
                      ? <TrendingUp className={`w-5 h-5 ${rec.color}`} />
                      : rec.icon === 'caution'
                        ? <Bell className={`w-5 h-5 ${rec.color}`} />
                        : rec.icon === 'spiritual'
                          ? <Eye className={`w-5 h-5 ${rec.color}`} />
                          : <Gift className={`w-5 h-5 ${rec.color}`} />;
                    return (
                      <div key={idx} className="flex items-start gap-3 p-4 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10">
                        <div className="w-10 h-10 rounded-lg bg-sacred-gold/5 flex items-center justify-center shrink-0">
                          {recIcon}
                        </div>
                        <p className="text-cosmic-text text-sm leading-relaxed pt-2">{rec.text}</p>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Karma & Streak Widget + Upcoming Events Widget */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

          {/* Karma & Streak Widget */}
          <Card className="card-sacred border border-sacred-gold/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                  <Flame className="w-5 h-5 text-orange-400" />
                  Karma &amp; Streak
                </h2>
              </div>
              {karmaProfile ? (
                <div className="space-y-4">
                  {/* Streak & Points row */}
                  <div className="grid grid-cols-3 gap-3">
                    <div className="bg-cosmic-bg/50 rounded-xl p-3 text-center border border-orange-500/10">
                      <Flame className="w-5 h-5 text-orange-400 mx-auto mb-1" />
                      <p className="text-2xl font-bold text-cosmic-text">{karmaProfile.streak}</p>
                      <p className="text-xs text-cosmic-text-secondary">Day Streak</p>
                    </div>
                    <div className="bg-cosmic-bg/50 rounded-xl p-3 text-center border border-sacred-gold/10">
                      <Award className="w-5 h-5 text-sacred-gold mx-auto mb-1" />
                      <p className="text-2xl font-bold text-cosmic-text">{karmaProfile.total_points}</p>
                      <p className="text-xs text-cosmic-text-secondary">Karma Points</p>
                    </div>
                    <div className="bg-cosmic-bg/50 rounded-xl p-3 text-center border border-purple-500/10">
                      <Star className="w-5 h-5 text-purple-400 mx-auto mb-1" />
                      <p className="text-2xl font-bold text-cosmic-text">Lv. {karmaProfile.level}</p>
                      <p className="text-xs text-cosmic-text-secondary">Level</p>
                    </div>
                  </div>
                  {/* Level progress bar */}
                  <div>
                    <div className="flex justify-between text-xs text-cosmic-text-secondary mb-1">
                      <span>Level {karmaProfile.level}</span>
                      <span>{karmaProfile.level_progress}%</span>
                    </div>
                    <div className="w-full bg-cosmic-bg rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-sacred-gold to-orange-400 h-2 rounded-full transition-all"
                        style={{ width: `${karmaProfile.level_progress}%` }}
                      />
                    </div>
                    {karmaProfile.next_level_points > 0 && (
                      <p className="text-xs text-cosmic-text-secondary mt-1">{karmaProfile.next_level_points - karmaProfile.total_points} points to next level</p>
                    )}
                  </div>
                  {/* Check In button */}
                  <Button
                    className={`w-full ${karmaProfile.checked_in_today ? 'bg-green-600/20 border border-green-500/30 text-green-400 cursor-default' : 'btn-sacred'}`}
                    onClick={karmaProfile.checked_in_today ? undefined : handleCheckIn}
                    disabled={karmaProfile.checked_in_today || checkingIn}
                  >
                    {checkingIn ? (
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    ) : karmaProfile.checked_in_today ? (
                      <CheckCircle className="w-4 h-4 mr-2" />
                    ) : (
                      <Flame className="w-4 h-4 mr-2" />
                    )}
                    {karmaProfile.checked_in_today ? 'Checked In Today' : 'Daily Check In'}
                  </Button>
                  {/* Badge gallery */}
                  {karmaProfile.badges && karmaProfile.badges.length > 0 && (
                    <div>
                      <p className="text-xs text-cosmic-text-secondary mb-2">Recent Badges</p>
                      <div className="flex gap-2">
                        {karmaProfile.badges.slice(-3).map((badge, idx) => (
                          <div key={idx} className="flex items-center gap-1.5 px-3 py-1.5 bg-sacred-gold/10 border border-sacred-gold/20 rounded-full">
                            <span className="text-sm">{badge.icon}</span>
                            <span className="text-xs text-sacred-gold font-medium">{badge.name}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-6">
                  <Flame className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
                  <p className="text-cosmic-text-secondary text-sm mb-3">Start your spiritual journey and earn karma</p>
                  <Button size="sm" className="btn-sacred" onClick={handleCheckIn} disabled={checkingIn}>
                    {checkingIn ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Flame className="w-4 h-4 mr-2" />}
                    First Check In
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Upcoming Events Widget */}
          <Card className="card-sacred border border-sacred-gold/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-sacred-gold" />
                  Upcoming Events
                </h2>
              </div>
              <div className="space-y-3">
                {/* Cosmic Calendar Events */}
                {cosmicEvents.length > 0 ? (
                  cosmicEvents.map((evt, idx) => (
                    <div key={idx} className="flex items-center gap-3 p-3 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10">
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                        evt.type === 'festival' ? 'bg-amber-500/10' : evt.type === 'muhurat' ? 'bg-green-500/10' : 'bg-purple-500/10'
                      }`}>
                        {evt.type === 'festival' ? (
                          <Gift className="w-5 h-5 text-amber-400" />
                        ) : evt.type === 'muhurat' ? (
                          <CheckCircle className="w-5 h-5 text-green-400" />
                        ) : (
                          <Calendar className="w-5 h-5 text-purple-400" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-cosmic-text font-medium text-sm truncate">{evt.name}</p>
                        <p className="text-cosmic-text-secondary text-xs">
                          {new Date(evt.date).toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' })}
                          {evt.description && ` - ${evt.description}`}
                        </p>
                      </div>
                      <Badge variant="outline" className="border-sacred-gold/20 text-cosmic-text-secondary text-xs capitalize shrink-0">
                        {evt.type}
                      </Badge>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-4">
                    <Calendar className="w-8 h-8 text-cosmic-text-muted mx-auto mb-2" />
                    <p className="text-cosmic-text-secondary text-sm">No upcoming events</p>
                  </div>
                )}

                {/* Next Consultation */}
                {consultations.length > 0 && (
                  <div className="flex items-center gap-3 p-3 bg-cosmic-bg/50 rounded-xl border border-blue-500/10">
                    <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center shrink-0">
                      <Clock className="w-5 h-5 text-blue-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-cosmic-text font-medium text-sm truncate">
                        Consultation with {consultations[0].astrologer_name || 'Astrologer'}
                      </p>
                      <p className="text-cosmic-text-secondary text-xs">
                        {consultations[0].date ? new Date(consultations[0].date).toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' }) : 'TBD'}
                        {consultations[0].time && ` at ${consultations[0].time}`}
                      </p>
                    </div>
                    <Badge variant="outline" className="border-blue-500/30 text-blue-400 text-xs shrink-0">
                      Consultation
                    </Badge>
                  </div>
                )}

                {/* Personalized Muhurat */}
                {nextMuhurat && (
                  <div className="flex items-center gap-3 p-3 bg-cosmic-bg/50 rounded-xl border border-green-500/10">
                    <div className="w-10 h-10 rounded-lg bg-green-500/10 flex items-center justify-center shrink-0">
                      <CheckCircle className="w-5 h-5 text-green-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-cosmic-text font-medium text-sm truncate">{nextMuhurat.event}</p>
                      <p className="text-cosmic-text-secondary text-xs">
                        {new Date(nextMuhurat.date).toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' })}
                      </p>
                    </div>
                    <Badge variant="outline" className="border-green-500/30 text-green-400 text-xs shrink-0">
                      Muhurat
                    </Badge>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Upcoming Consultations + Saved Kundlis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* Upcoming Consultations */}
          <Card className="bg-cosmic-card border border-sacred-gold/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                  <Clock className="w-5 h-5 text-sacred-gold" />
                  Upcoming Consultations
                </h2>
                <Link to="/consultation">
                  <Button variant="ghost" size="sm" className="text-sacred-gold hover:text-sacred-gold/80">
                    Book <ArrowRight className="w-4 h-4 ml-1" />
                  </Button>
                </Link>
              </div>
              {consultations.length === 0 ? (
                <div className="text-center py-8">
                  <Calendar className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
                  <p className="text-cosmic-text-secondary text-sm mb-3">No upcoming consultations</p>
                  <Link to="/consultation">
                    <Button size="sm" className="btn-sacred">Book a Session</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-3">
                  {consultations.map((c) => (
                    <div key={c.id} className="flex items-center gap-3 p-3 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10">
                      <div className="w-10 h-10 rounded-lg bg-sacred-gold/10 flex items-center justify-center shrink-0">
                        <Clock className="w-5 h-5 text-sacred-gold" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-cosmic-text font-medium text-sm truncate">
                          {c.astrologer_name || 'Astrologer'}
                        </p>
                        <p className="text-cosmic-text-secondary text-xs">
                          {c.date ? new Date(c.date).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' }) : 'TBD'}
                          {c.time && ` at ${c.time}`}
                        </p>
                      </div>
                      <Badge variant="outline" className="border-sacred-gold/30 text-sacred-gold text-xs shrink-0">
                        {c.status}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Saved Kundlis */}
          <Card className="bg-cosmic-card border border-sacred-gold/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-sacred text-xl font-bold text-gradient-gold flex items-center gap-2">
                  <FileText className="w-5 h-5 text-sacred-gold" />
                  Saved Kundlis
                </h2>
                <Link to="/kundli">
                  <Button variant="ghost" size="sm" className="text-sacred-gold hover:text-sacred-gold/80">
                    View All <ArrowRight className="w-4 h-4 ml-1" />
                  </Button>
                </Link>
              </div>
              {savedKundlis.length === 0 ? (
                <div className="text-center py-8">
                  <Star className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
                  <p className="text-cosmic-text-secondary text-sm mb-3">No saved kundlis yet</p>
                  <Link to="/kundli">
                    <Button size="sm" className="btn-sacred">Generate Kundli</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-3">
                  {savedKundlis.map((k) => (
                    <Link key={k.id} to="/kundli">
                      <div className="flex items-center gap-3 p-3 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10 hover:border-sacred-gold/30 transition-colors cursor-pointer">
                        <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center shrink-0">
                          <Star className="w-5 h-5 text-purple-400" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-cosmic-text font-medium text-sm truncate">{k.name}</p>
                          <p className="text-cosmic-text-secondary text-xs">
                            {k.date_of_birth
                              ? new Date(k.date_of_birth).toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' })
                              : k.created_at
                                ? `Created ${new Date(k.created_at).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}`
                                : 'Saved'}
                          </p>
                        </div>
                        <ArrowRight className="w-4 h-4 text-cosmic-text-secondary shrink-0" />
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
