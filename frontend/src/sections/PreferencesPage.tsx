import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Loader2,
  Settings,
  Bell,
  Globe,
  Star,
  Save,
  CheckCircle,
  User,
  Sparkles,
  BookOpen,
  Calendar,
  Eye,
  Hash,
  Palette,
  Sun,
  Moon,
  Heart,
  ArrowLeft,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface ContentPreferences {
  kundli: boolean;
  horoscope: boolean;
  panchang: boolean;
  tarot: boolean;
  numerology: boolean;
  remedies: boolean;
  spiritual_content: boolean;
}

interface NotificationPreferences {
  transit_alerts: boolean;
  muhurat_alerts: boolean;
  festival_alerts: boolean;
  daily_digest: boolean;
  email_notifications: boolean;
}

interface DisplayPreferences {
  language: string;
  preferred_zodiac_sign: string;
}

interface FavoriteAstrologer {
  id: number;
  name: string;
  specialty?: string;
  avatar?: string;
}

const zodiacSigns = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

const languages = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'Hindi' },
  { code: 'sa', label: 'Sanskrit' },
  { code: 'ta', label: 'Tamil' },
  { code: 'te', label: 'Telugu' },
  { code: 'bn', label: 'Bengali' },
  { code: 'mr', label: 'Marathi' },
  { code: 'gu', label: 'Gujarati' },
  { code: 'kn', label: 'Kannada' },
];

const contentItems: { key: keyof ContentPreferences; label: string; icon: React.ReactNode }[] = [
  { key: 'kundli', label: 'Kundli & Birth Charts', icon: <Star className="w-4 h-4 text-purple-400" /> },
  { key: 'horoscope', label: 'Daily Horoscope', icon: <Sun className="w-4 h-4 text-amber-400" /> },
  { key: 'panchang', label: 'Panchang & Calendar', icon: <Calendar className="w-4 h-4 text-blue-400" /> },
  { key: 'tarot', label: 'Tarot Readings', icon: <Eye className="w-4 h-4 text-pink-400" /> },
  { key: 'numerology', label: 'Numerology', icon: <Hash className="w-4 h-4 text-green-400" /> },
  { key: 'remedies', label: 'Remedies & Rituals', icon: <Sparkles className="w-4 h-4 text-sacred-gold" /> },
  { key: 'spiritual_content', label: 'Spiritual Content', icon: <BookOpen className="w-4 h-4 text-indigo-400" /> },
];

const notificationItems: { key: keyof NotificationPreferences; label: string; description: string }[] = [
  { key: 'transit_alerts', label: 'Transit Alerts', description: 'Get notified when planets change signs or houses' },
  { key: 'muhurat_alerts', label: 'Muhurat Alerts', description: 'Auspicious timing notifications for important events' },
  { key: 'festival_alerts', label: 'Festival Alerts', description: 'Reminders for upcoming festivals and observances' },
  { key: 'daily_digest', label: 'Daily Digest', description: 'A summary of your daily horoscope and cosmic events' },
  { key: 'email_notifications', label: 'Email Notifications', description: 'Receive alerts and digest via email' },
];

function ToggleSwitch({ checked, onChange }: { checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-sacred-gold/50 ${
        checked ? 'bg-sacred-gold' : 'bg-cosmic-bg border border-sacred-gold/20'
      }`}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full transition-transform duration-200 ${
          checked ? 'translate-x-6 bg-cosmic-bg' : 'translate-x-1 bg-cosmic-text-secondary'
        }`}
      />
    </button>
  );
}

export default function PreferencesPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const [contentPrefs, setContentPrefs] = useState<ContentPreferences>({
    kundli: true,
    horoscope: true,
    panchang: true,
    tarot: false,
    numerology: false,
    remedies: true,
    spiritual_content: false,
  });

  const [notifPrefs, setNotifPrefs] = useState<NotificationPreferences>({
    transit_alerts: true,
    muhurat_alerts: true,
    festival_alerts: true,
    daily_digest: false,
    email_notifications: false,
  });

  const [displayPrefs, setDisplayPrefs] = useState<DisplayPreferences>({
    language: 'en',
    preferred_zodiac_sign: 'Aries',
  });

  const [favoriteAstrologers, setFavoriteAstrologers] = useState<FavoriteAstrologer[]>([]);

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    const loadPreferences = async () => {
      setLoading(true);
      try {
        const [prefsRes, notifRes, astrologersRes] = await Promise.allSettled([
          api.get('/api/preferences'),
          api.get('/api/notifications/preferences'),
          api.get('/api/astrologers/favorites'),
        ]);

        if (cancelled) return;

        if (prefsRes.status === 'fulfilled' && prefsRes.value) {
          const p = prefsRes.value;
          if (p.content) {
            setContentPrefs(prev => ({ ...prev, ...p.content }));
          }
          if (p.display) {
            setDisplayPrefs(prev => ({ ...prev, ...p.display }));
          }
        }

        if (notifRes.status === 'fulfilled' && notifRes.value) {
          setNotifPrefs(prev => ({ ...prev, ...notifRes.value }));
        }

        if (astrologersRes.status === 'fulfilled') {
          const list = Array.isArray(astrologersRes.value)
            ? astrologersRes.value
            : astrologersRes.value?.astrologers || [];
          setFavoriteAstrologers(list);
        }
      } catch {
        // Defaults remain
      }
      setLoading(false);
    };

    loadPreferences();
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    try {
      await Promise.allSettled([
        api.put('/api/preferences', {
          content: contentPrefs,
          display: displayPrefs,
        }),
        api.put('/api/notifications/preferences', notifPrefs),
      ]);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch {
      // Handle silently
    } finally {
      setSaving(false);
    }
  };

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
        <p className="text-cosmic-text-secondary mb-6">Please log in to manage your preferences.</p>
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
    <section className="relative py-24 bg-cosmic-bg min-h-screen">
      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link to="/dashboard">
            <Button variant="ghost" size="sm" className="text-cosmic-text-secondary hover:text-sacred-gold">
              <ArrowLeft className="w-4 h-4 mr-1" /> Back
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl sm:text-4xl font-sacred font-bold text-gradient-gold flex items-center gap-3">
              <Settings className="w-8 h-8 text-sacred-gold" />
              Preferences
            </h1>
            <p className="text-cosmic-text-secondary mt-1">Customize your AstroVedic experience</p>
          </div>
        </div>

        {/* Content Preferences */}
        <Card className="card-sacred border border-sacred-gold/20 mb-6">
          <CardContent className="p-6">
            <h2 className="font-sacred text-xl font-bold text-gradient-gold mb-1 flex items-center gap-2">
              <Palette className="w-5 h-5 text-sacred-gold" />
              Content Preferences
            </h2>
            <p className="text-cosmic-text-secondary text-sm mb-5">Choose which types of content interest you most</p>
            <div className="space-y-3">
              {contentItems.map((item) => (
                <div key={item.key} className="flex items-center justify-between p-3 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-sacred-gold/5 flex items-center justify-center shrink-0">
                      {item.icon}
                    </div>
                    <span className="text-cosmic-text font-medium text-sm">{item.label}</span>
                  </div>
                  <ToggleSwitch
                    checked={contentPrefs[item.key]}
                    onChange={(v) => setContentPrefs(prev => ({ ...prev, [item.key]: v }))}
                  />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Notification Settings */}
        <Card className="card-sacred border border-sacred-gold/20 mb-6">
          <CardContent className="p-6">
            <h2 className="font-sacred text-xl font-bold text-gradient-gold mb-1 flex items-center gap-2">
              <Bell className="w-5 h-5 text-sacred-gold" />
              Notification Settings
            </h2>
            <p className="text-cosmic-text-secondary text-sm mb-5">Control when and how you receive alerts</p>
            <div className="space-y-3">
              {notificationItems.map((item) => (
                <div key={item.key} className="flex items-center justify-between p-3 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10">
                  <div className="flex-1 min-w-0 mr-4">
                    <span className="text-cosmic-text font-medium text-sm block">{item.label}</span>
                    <span className="text-cosmic-text-secondary text-xs">{item.description}</span>
                  </div>
                  <ToggleSwitch
                    checked={notifPrefs[item.key]}
                    onChange={(v) => setNotifPrefs(prev => ({ ...prev, [item.key]: v }))}
                  />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Display Preferences */}
        <Card className="card-sacred border border-sacred-gold/20 mb-6">
          <CardContent className="p-6">
            <h2 className="font-sacred text-xl font-bold text-gradient-gold mb-1 flex items-center gap-2">
              <Globe className="w-5 h-5 text-sacred-gold" />
              Display Preferences
            </h2>
            <p className="text-cosmic-text-secondary text-sm mb-5">Personalize how content is displayed</p>
            <div className="space-y-5">
              {/* Language Selector */}
              <div>
                <label className="text-cosmic-text font-medium text-sm block mb-2">Language</label>
                <select
                  value={displayPrefs.language}
                  onChange={(e) => setDisplayPrefs(prev => ({ ...prev, language: e.target.value }))}
                  className="w-full bg-cosmic-bg border border-sacred-gold/20 rounded-xl px-4 py-2.5 text-cosmic-text text-sm focus:outline-none focus:ring-2 focus:ring-sacred-gold/50 focus:border-sacred-gold/40"
                >
                  {languages.map((lang) => (
                    <option key={lang.code} value={lang.code} className="bg-cosmic-bg text-cosmic-text">
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>
              {/* Preferred Zodiac Sign */}
              <div>
                <label className="text-cosmic-text font-medium text-sm block mb-2">Preferred Zodiac Sign for Horoscope</label>
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                  {zodiacSigns.map((sign) => (
                    <button
                      key={sign}
                      type="button"
                      onClick={() => setDisplayPrefs(prev => ({ ...prev, preferred_zodiac_sign: sign }))}
                      className={`px-3 py-2 rounded-xl text-sm font-medium transition-all ${
                        displayPrefs.preferred_zodiac_sign === sign
                          ? 'bg-sacred-gold/20 border border-sacred-gold/40 text-sacred-gold'
                          : 'bg-cosmic-bg/50 border border-sacred-gold/10 text-cosmic-text-secondary hover:border-sacred-gold/20 hover:text-cosmic-text'
                      }`}
                    >
                      {sign}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Preferred Astrologers */}
        <Card className="card-sacred border border-sacred-gold/20 mb-8">
          <CardContent className="p-6">
            <h2 className="font-sacred text-xl font-bold text-gradient-gold mb-1 flex items-center gap-2">
              <Heart className="w-5 h-5 text-pink-400" />
              Preferred Astrologers
            </h2>
            <p className="text-cosmic-text-secondary text-sm mb-5">Your favorited astrologers for quick access</p>
            {favoriteAstrologers.length > 0 ? (
              <div className="space-y-3">
                {favoriteAstrologers.map((astrologer) => (
                  <div key={astrologer.id} className="flex items-center gap-3 p-3 bg-cosmic-bg/50 rounded-xl border border-sacred-gold/10">
                    <div className="w-10 h-10 rounded-full bg-sacred-gold/10 flex items-center justify-center shrink-0">
                      {astrologer.avatar ? (
                        <img src={astrologer.avatar} alt={astrologer.name} className="w-10 h-10 rounded-full object-cover" />
                      ) : (
                        <Star className="w-5 h-5 text-sacred-gold" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-cosmic-text font-medium text-sm truncate">{astrologer.name}</p>
                      {astrologer.specialty && (
                        <p className="text-cosmic-text-secondary text-xs">{astrologer.specialty}</p>
                      )}
                    </div>
                    <Badge variant="outline" className="border-pink-500/30 text-pink-400 text-xs shrink-0">
                      <Heart className="w-3 h-3 mr-1 fill-current" /> Favorite
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6">
                <Heart className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
                <p className="text-cosmic-text-secondary text-sm mb-3">No favorite astrologers yet</p>
                <Link to="/consultation">
                  <Button size="sm" className="btn-sacred">Browse Astrologers</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="flex items-center justify-end gap-3">
          {saved && (
            <span className="text-green-400 text-sm flex items-center gap-1">
              <CheckCircle className="w-4 h-4" /> Preferences saved
            </span>
          )}
          <Button
            className="btn-sacred px-8"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? (
              <Loader2 className="w-4 h-4 animate-spin mr-2" />
            ) : (
              <Save className="w-4 h-4 mr-2" />
            )}
            {saving ? 'Saving...' : 'Save Preferences'}
          </Button>
        </div>
      </div>
    </section>
  );
}
