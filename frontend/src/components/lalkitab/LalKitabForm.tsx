import { useState, useRef, useEffect } from 'react';
import { Calendar, Clock, MapPin, User, Loader2, Phone } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import ClientSelector from '@/components/ClientSelector';
import type { ClientData } from '@/components/ClientSelector';

export interface LalKitabFormData {
  name: string;
  date: string;
  time: string;
  place: string;
  latitude: number;
  longitude: number;
  gender: 'male' | 'female';
  phone?: string;
  isNewClient?: boolean;
  selectedClientId?: string | null;
}

interface LalKitabFormProps {
  onGenerate: (formData: LalKitabFormData) => void;
  loading: boolean;
}

interface GeocodeResult {
  name: string;
  lat: number;
  lon: number;
}

export default function LalKitabForm({ onGenerate, loading }: LalKitabFormProps) {
  const { t, language } = useTranslation();
  const { user } = useAuth();
  const isAstrologer = user?.role === 'astrologer';

  const [isNewClient, setIsNewClient] = useState(true);
  const [selectedClient, setSelectedClient] = useState<ClientData | null>(null);

  const [formData, setFormData] = useState<LalKitabFormData>({
    name: '',
    date: '',
    time: '',
    place: '',
    latitude: 0,
    longitude: 0,
    gender: 'male',
    phone: '',
  });

  const handleClientSelect = (client: ClientData | null) => {
    setSelectedClient(client);
    if (client) {
      setFormData((prev) => ({
        ...prev,
        name: client.name || '',
        date: client.birth_date || '',
        time: client.birth_time || '',
        place: client.birth_place || '',
        latitude: client.latitude || 0,
        longitude: client.longitude || 0,
        gender: (client.gender === 'female' ? 'female' : 'male') as 'male' | 'female',
        phone: client.phone || '',
        selectedClientId: client.id,
        isNewClient: false,
      }));
    }
  };

  const handleClientToggle = (isNew: boolean) => {
    setIsNewClient(isNew);
    if (isNew) {
      setSelectedClient(null);
      setFormData({
        name: '',
        date: '',
        time: '',
        place: '',
        latitude: 0,
        longitude: 0,
        gender: 'male',
        phone: '',
        isNewClient: true,
        selectedClientId: null,
      });
    }
  };

  const [suggestions, setSuggestions] = useState<GeocodeResult[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [geocodeLoading, setGeocodeLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const placeWrapperRef = useRef<HTMLDivElement>(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (placeWrapperRef.current && !placeWrapperRef.current.contains(e.target as Node)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handlePlaceChange = (query: string) => {
    setFormData((prev) => ({ ...prev, place: query, latitude: 0, longitude: 0 }));

    if (timerRef.current) clearTimeout(timerRef.current);

    if (query.length < 3) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }

    timerRef.current = setTimeout(async () => {
      setGeocodeLoading(true);
      try {
        const results = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(query)}`);
        setSuggestions(Array.isArray(results) ? results : []);
        setShowDropdown(true);
      } catch {
        setSuggestions([]);
      }
      setGeocodeLoading(false);
    }, 300);
  };

  const handleSelectPlace = (result: GeocodeResult) => {
    setFormData((prev) => ({
      ...prev,
      place: result.name.split(',')[0],
      latitude: result.lat,
      longitude: result.lon,
    }));
    setShowDropdown(false);
  };

  const isValid = formData.date && formData.time && formData.place && (formData.latitude !== 0 || formData.longitude !== 0)
    && (!isAstrologer || !isNewClient || !!formData.phone?.trim() || !!selectedClient);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isValid && !loading) {
      onGenerate({
        ...formData,
        isNewClient,
        selectedClientId: selectedClient?.id || null,
      });
    }
  };

  const inputClass =
    'w-full rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text px-4 py-3 focus:outline-none focus:border-sacred-gold/50 transition-colors';

  return (
    <form onSubmit={handleSubmit} className="card-sacred rounded-xl p-6 border border-sacred-gold/20">
      <h2 className="text-xl font-sans font-semibold text-sacred-gold mb-1">
        {t('lk.enterDetails')}
      </h2>
      <p className="text-sm text-gray-500 mb-6">
        {t('lk.subtitle')}
      </p>

      {isAstrologer && (
        <ClientSelector
          onSelectClient={handleClientSelect}
          isNewClient={isNewClient}
          onToggle={handleClientToggle}
        />
      )}

      <div className="space-y-4">
        {/* Name */}
        <div>
          <label className="block text-sm font-medium text-sacred-gold mb-2">
            {t('lk.name')}
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold/60" />
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData((prev) => ({ ...prev, name: e.target.value }))}
              placeholder={language === 'hi' ? 'अपना नाम दर्ज करें' : 'Enter your name'}
              className={`${inputClass} pl-10`}
            />
          </div>
        </div>

        {/* Date of Birth */}
        <div>
          <label className="block text-sm font-medium text-sacred-gold mb-2">
            {t('lk.dob')}
          </label>
          <div className="relative">
            <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold/60" />
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData((prev) => ({ ...prev, date: e.target.value }))}
              className={`${inputClass} pl-10`}
              required
            />
          </div>
        </div>

        {/* Time of Birth */}
        <div>
          <label className="block text-sm font-medium text-sacred-gold mb-2">
            {t('lk.tob')}
          </label>
          <div className="relative">
            <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold/60" />
            <input
              type="time"
              value={formData.time}
              onChange={(e) => setFormData((prev) => ({ ...prev, time: e.target.value }))}
              className={`${inputClass} pl-10`}
              required
            />
          </div>
        </div>

        {/* Place of Birth */}
        <div ref={placeWrapperRef}>
          <label className="block text-sm font-medium text-sacred-gold mb-2">
            {t('lk.pob')}
          </label>
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold/60 z-10" />
            <input
              type="text"
              value={formData.place}
              onChange={(e) => handlePlaceChange(e.target.value)}
              placeholder={language === 'hi' ? 'जन्म स्थान खोजें' : 'Search birth place'}
              className={`${inputClass} pl-10`}
              autoComplete="off"
              required
            />
            {geocodeLoading && (
              <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 animate-spin text-sacred-gold" />
            )}
          </div>

          {showDropdown && suggestions.length > 0 && (
            <div className="relative">
              <div className="absolute z-50 left-0 right-0 mt-1 bg-cosmic-bg border border-sacred-gold/30 rounded-xl shadow-lg max-h-60 overflow-y-auto">
                {suggestions.map((s, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => handleSelectPlace(s)}
                    className="w-full text-left px-4 py-3 hover:bg-sacred-gold/10 transition-colors border-b border-sacred-gold/10 last:border-b-0"
                  >
                    <p className="text-sm font-medium text-cosmic-text truncate">{s.name}</p>
                    <p className="text-sm text-gray-600">
                      {s.lat.toFixed(4)}, {s.lon.toFixed(4)}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          )}

          {formData.latitude !== 0 && formData.longitude !== 0 && (
            <div className="flex items-center gap-2 text-sm text-gray-600 mt-1 px-1">
              <MapPin className="w-3 h-3 text-sacred-gold" />
              <span>
                {formData.latitude.toFixed(4)}, {formData.longitude.toFixed(4)}
              </span>
            </div>
          )}
        </div>

        {/* Gender */}
        <div>
          <label className="block text-sm font-medium text-sacred-gold mb-2">
            {t('lk.gender')}
          </label>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setFormData((prev) => ({ ...prev, gender: 'male' }))}
              className={`p-3 rounded-xl border text-sm font-medium transition-colors ${
                formData.gender === 'male'
                  ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold'
                  : 'border-sacred-gold/20 text-gray-500 hover:border-sacred-gold/40'
              }`}
            >
              {t('lk.male')}
            </button>
            <button
              type="button"
              onClick={() => setFormData((prev) => ({ ...prev, gender: 'female' }))}
              className={`p-3 rounded-xl border text-sm font-medium transition-colors ${
                formData.gender === 'female'
                  ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold'
                  : 'border-sacred-gold/20 text-gray-500 hover:border-sacred-gold/40'
              }`}
            >
              {t('lk.female')}
            </button>
          </div>
        </div>

        {/* Phone (required for astrologers creating new client kundli) */}
        {isAstrologer && isNewClient && (
          <div>
            <label className="block text-sm font-medium text-sacred-gold mb-2">
              Client Phone <span className="text-red-400">*</span>
            </label>
            <div className="relative">
              <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold/60" />
              <input
                type="tel"
                value={formData.phone || ''}
                onChange={(e) => setFormData((prev) => ({ ...prev, phone: e.target.value }))}
                placeholder="Client phone number"
                className={`${inputClass} pl-10`}
              />
            </div>
          </div>
        )}

        {/* Submit */}
        <Button
          type="submit"
          disabled={!isValid || loading}
          className="btn-sacred w-full font-semibold disabled:opacity-50"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              {t('lk.generating')}
            </>
          ) : (
            t('lk.generate')
          )}
        </Button>
      </div>
    </form>
  );
}
