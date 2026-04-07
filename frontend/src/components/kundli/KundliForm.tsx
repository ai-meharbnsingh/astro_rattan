import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Calendar, Clock, MapPin, User, ChevronRight, ArrowLeft, Loader2 } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

// ── Geocode types & hook ────────────────────────────────────
interface GeocodeResult {
  name: string;
  lat: number;
  lon: number;
}

function useGeocodeAutocomplete() {
  const [suggestions, setSuggestions] = useState<GeocodeResult[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const search = (query: string) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (query.length < 3) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }
    timerRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const results = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(query)}`);
        setSuggestions(Array.isArray(results) ? results : []);
        setShowDropdown(true);
      } catch {
        setSuggestions([]);
      }
      setLoading(false);
    }, 300);
  };

  const close = () => {
    setShowDropdown(false);
  };

  return { suggestions, showDropdown, loading, search, close };
}

export interface KundliFormData {
  name: string;
  date: string;
  time: string;
  place: string;
  latitude: number;
  longitude: number;
  gender: 'male' | 'female';
}

interface KundliFormProps {
  formData: KundliFormData;
  setFormData: (data: KundliFormData) => void;
  error: string;
  savedKundlisCount: number;
  onGenerate: () => void;
  onPrashnaKundli: () => void;
  onBackToList: () => void;
}

export default function KundliForm({
  formData,
  setFormData,
  error,
  savedKundlisCount,
  onGenerate,
  onPrashnaKundli,
  onBackToList,
}: KundliFormProps) {
  const { t } = useTranslation();
  const geocode = useGeocodeAutocomplete();
  const placeWrapperRef = useRef<HTMLDivElement>(null);

  // Close geocode dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (placeWrapperRef.current && !placeWrapperRef.current.contains(e.target as Node)) {
        geocode.close();
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [geocode]);

  return (
    <div className="max-w-md mx-auto py-24 px-4 bg-transparent">
      <div className="text-center mb-8">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-8 h-8 text-cosmic-bg" />
        </div>
        <h3 className="text-2xl sm:text-3xl font-display font-bold text-sacred-brown mb-2">Generate Your Kundli</h3>
        <p className="text-sacred-text-secondary">Enter your birth details for a personalized Vedic birth chart</p>
      </div>
      {savedKundlisCount > 0 && (
        <Button variant="outline" onClick={onBackToList} className="w-full mb-4 border-sacred-gold/50 text-sacred-brown">
          <ArrowLeft className="w-4 h-4 mr-2" />Back to My Kundlis ({savedKundlisCount})
        </Button>
      )}
      <Button onClick={onPrashnaKundli} variant="outline" className="w-full mb-4 border-sacred-gold/50 text-sacred-brown hover:bg-sacred-gold/10">
        <Clock className="w-5 h-5 mr-2 text-sacred-gold" />{t('kundli.prashnaKundli')}
        <span className="ml-2 text-xs text-sacred-text-secondary">{t('kundli.prashnaSubtitle')}</span>
      </Button>
      {error && <div className="mb-4 p-3 rounded-xl bg-red-900/20 text-red-400 text-sm">{error}</div>}
      <div className="space-y-4">
        <div className="relative">
          <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
          <Input type="text" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="Full Name" className="pl-10 bg-sacred-cream border-sacred-gold/15 text-sacred-brown" />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <button onClick={() => setFormData({ ...formData, gender: 'male' })} className={`p-3 rounded-xl border transition-colors ${formData.gender === 'male' ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold-dark' : 'border-sacred-gold/15 text-sacred-text-secondary'}`}>Male</button>
          <button onClick={() => setFormData({ ...formData, gender: 'female' })} className={`p-3 rounded-xl border transition-colors ${formData.gender === 'female' ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold-dark' : 'border-sacred-gold/15 text-sacred-text-secondary'}`}>Female</button>
        </div>
        <div className="relative">
          <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-cosmic-text-muted" />
          <Input type="date" value={formData.date} onChange={(e) => setFormData({ ...formData, date: e.target.value })} className="pl-10 bg-sacred-cream border-sacred-gold/15 text-sacred-brown" />
        </div>
        <div className="relative">
          <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-cosmic-text-muted" />
          <Input type="time" value={formData.time} onChange={(e) => setFormData({ ...formData, time: e.target.value })} className="pl-10 bg-sacred-cream border-sacred-gold/15 text-sacred-brown" />
        </div>
        <div className="relative" ref={placeWrapperRef}>
          <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-cosmic-text-muted z-10" />
          <Input
            type="text"
            value={formData.place}
            onChange={(e) => {
              setFormData({ ...formData, place: e.target.value });
              geocode.search(e.target.value);
            }}
            placeholder="Birth Place (type to search)"
            className="pl-10 bg-sacred-cream border-sacred-gold/15 text-sacred-brown"
            autoComplete="off"
          />
          {geocode.loading && (
            <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 animate-spin text-sacred-gold" />
          )}
          {geocode.showDropdown && geocode.suggestions.length > 0 && (
            <div className="absolute z-50 left-0 right-0 top-full mt-1 bg-cosmic-bg border border-sacred-gold-dark/30 rounded-xl shadow-lg max-h-60 overflow-y-auto">
              {geocode.suggestions.map((s, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => {
                    setFormData({ ...formData, place: s.name.split(',')[0], latitude: s.lat, longitude: s.lon });
                    geocode.close();
                  }}
                  className="w-full text-left px-4 py-3 hover:bg-sacred-purple transition-colors border-b border-sacred-gold-dark/10 last:border-b-0"
                >
                  <p className="text-sm font-medium text-cosmic-text truncate">{s.name}</p>
                  <p className="text-xs text-cosmic-text/50">{s.lat.toFixed(4)}, {s.lon.toFixed(4)}</p>
                </button>
              ))}
            </div>
          )}
        </div>
        {/* Coordinates display */}
        <div className="flex items-center gap-2 text-xs text-sacred-text-secondary px-1">
          <MapPin className="w-3 h-3 text-sacred-gold" />
          <span>Lat: {formData.latitude.toFixed(4)}, Lon: {formData.longitude.toFixed(4)}</span>
        </div>
        <Button onClick={onGenerate} disabled={!formData.name || !formData.date || !formData.time || !formData.place} className="w-full btn-sacred font-semibold hover:bg-sacred-gold-dark disabled:opacity-50">
          <Sparkles className="w-5 h-5 mr-2" />Generate Kundli<ChevronRight className="w-5 h-5 ml-2" />
        </Button>
      </div>
    </div>
  );
}
