import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Calendar, Clock, MapPin, User, ChevronRight, ArrowLeft, Loader2, Phone, ChevronDown } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import ClientSelector from '@/components/ClientSelector';
import type { ClientData } from '@/components/ClientSelector';

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
  phone?: string;
  clientId?: string | null;
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
  const { t, language } = useTranslation();
  const { user } = useAuth();
  const isAstrologer = user?.role === 'astrologer';
  const [isNewClient, setIsNewClient] = useState(true);
  const [_selectedClient, setSelectedClient] = useState<ClientData | null>(null);
  const [showCoordinates, setShowCoordinates] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});
  const geocode = useGeocodeAutocomplete();
  const placeWrapperRef = useRef<HTMLDivElement>(null);

  const handleClientSelect = (client: ClientData | null) => {
    setSelectedClient(client);
    if (client) {
      setFormData({
        ...formData,
        name: client.name || '',
        date: client.birth_date || '',
        time: client.birth_time || '',
        place: client.birth_place || '',
        latitude: client.latitude || 28.6139,
        longitude: client.longitude || 77.2090,
        gender: (client.gender === 'female' ? 'female' : 'male') as 'male' | 'female',
        phone: client.phone || '',
        clientId: client.id,
      });
      // Clear validation errors when a client is selected
      setValidationErrors({});
    }
  };

  const handleClientToggle = (isNew: boolean) => {
    setIsNewClient(isNew);
    if (isNew) {
      setSelectedClient(null);
      setFormData({
        name: '', date: '', time: '', place: '',
        latitude: 28.6139, longitude: 77.2090, gender: 'male',
        phone: '', clientId: null,
      });
      setValidationErrors({});
    }
  };

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

  // Inline validation on submit
  const handleSubmit = () => {
    const errors: Record<string, string> = {};
    if (!formData.name.trim()) {
      errors.name = language === 'hi' ? 'नाम आवश्यक है' : 'Name is required';
    }
    if (!formData.date) {
      errors.date = language === 'hi' ? 'जन्म तिथि आवश्यक है' : 'Birth date is required';
    }
    if (!formData.time) {
      errors.time = language === 'hi' ? 'जन्म समय आवश्यक है' : 'Birth time is required';
    }
    if (!formData.place.trim()) {
      errors.place = language === 'hi' ? 'जन्म स्थान आवश्यक है' : 'Birth place is required';
    }
    if (isAstrologer && isNewClient && !formData.phone?.trim()) {
      errors.phone = language === 'hi' ? 'फ़ोन नंबर आवश्यक है' : 'Phone number is required';
    }

    setValidationErrors(errors);
    if (Object.keys(errors).length > 0) return;
    onGenerate();
  };

  // Clear specific validation error when user types
  const clearError = (field: string) => {
    if (validationErrors[field]) {
      setValidationErrors(prev => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    }
  };

  const hi = language === 'hi';

  return (
    <div className="max-w-3xl mx-auto py-24 px-4 bg-transparent">
      <div className="text-center mb-10">
        <h3 className="text-3xl sm:text-4xl font-display font-bold text-sacred-brown">{hi ? 'अपनी कुंडली बनाएं' : 'Generate Your Kundli'}</h3>
      </div>
      
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        {savedKundlisCount > 0 && (
          <Button variant="outline" onClick={onBackToList} className="flex-1 border-sacred-gold text-sacred-brown">
            <ArrowLeft className="w-4 h-4 mr-2" />{hi ? `मेरी कुंडलियाँ (${savedKundlisCount})` : `My Kundlis (${savedKundlisCount})`}
          </Button>
        )}
        <Button onClick={onPrashnaKundli} variant="outline" className="flex-[2] border-sacred-gold text-sacred-brown hover:bg-sacred-gold/10">
          <Clock className="w-5 h-5 mr-2 text-sacred-gold" />{t('kundli.prashnaKundli')}
          <span className="ml-2 text-xs text-cosmic-text opacity-70 hidden sm:inline">{t('kundli.prashnaSubtitle')}</span>
        </Button>
      </div>

      {isAstrologer && (
        <div className="mb-6">
          <ClientSelector
            onSelectClient={handleClientSelect}
            isNewClient={isNewClient}
            onToggle={handleClientToggle}
          />
        </div>
      )}

      {error && <div className="mb-6 p-3 rounded-xl bg-red-50 border border-red-300 text-red-700 text-sm">{error}</div>}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
        {/* Name field */}
        <div className="md:col-span-2">
          <label htmlFor="kundli-name" className="block text-sm font-medium text-cosmic-text mb-1.5">
            {hi ? 'पूरा नाम' : 'Full Name'}
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
            <Input
              id="kundli-name"
              type="text"
              value={formData.name}
              onChange={(e) => { setFormData({ ...formData, name: e.target.value }); clearError('name'); }}
              placeholder={hi ? 'पूरा नाम दर्ज करें' : 'Enter full name'}
              className={`pl-10 h-12 bg-sacred-cream border-sacred-gold text-sacred-brown text-base ${validationErrors.name ? 'border-red-500 ring-1 ring-red-500' : ''}`}
            />
          </div>
          {validationErrors.name && <p className="text-red-600 text-xs mt-1">{validationErrors.name}</p>}
        </div>

        {/* Gender */}
        <div>
          <label className="block text-sm font-medium text-cosmic-text mb-1.5">{hi ? 'लिंग' : 'Gender'}</label>
          <div className="grid grid-cols-2 gap-3" role="radiogroup" aria-label={hi ? 'लिंग' : 'Gender'}>
            <button role="radio" aria-checked={formData.gender === 'male'} onClick={() => setFormData({ ...formData, gender: 'male' })} 
              className={`h-12 rounded-xl border transition-all font-medium ${formData.gender === 'male' ? 'border-sacred-gold bg-sacred-gold-dark text-white shadow-md' : 'border-sacred-gold/40 text-cosmic-text bg-white/50 hover:bg-sacred-gold/5'}`}>
              {hi ? 'पुरुष' : 'Male'}
            </button>
            <button role="radio" aria-checked={formData.gender === 'female'} onClick={() => setFormData({ ...formData, gender: 'female' })} 
              className={`h-12 rounded-xl border transition-all font-medium ${formData.gender === 'female' ? 'border-sacred-gold bg-sacred-gold-dark text-white shadow-md' : 'border-sacred-gold/40 text-cosmic-text bg-white/50 hover:bg-sacred-gold/5'}`}>
              {hi ? 'महिला' : 'Female'}
            </button>
          </div>
        </div>

        {/* Phone field (astrologer only) */}
        {isAstrologer ? (
          <div>
            {isNewClient && (
              <div>
                <label htmlFor="kundli-phone" className="block text-sm font-medium text-cosmic-text mb-1.5">
                  {hi ? 'क्लाइंट फ़ोन नंबर' : 'Client Phone Number'}
                </label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                  <Input
                    id="kundli-phone"
                    type="tel"
                    value={formData.phone || ''}
                    onChange={(e) => { setFormData({ ...formData, phone: e.target.value }); clearError('phone'); }}
                    placeholder={hi ? 'फ़ोन नंबर' : 'Phone number'}
                    className={`pl-10 h-12 bg-sacred-cream border-sacred-gold text-sacred-brown ${validationErrors.phone ? 'border-red-500 ring-1 ring-red-500' : ''}`}
                  />
                </div>
                {validationErrors.phone && <p className="text-red-600 text-xs mt-1">{validationErrors.phone}</p>}
              </div>
            )}
          </div>
        ) : (
          <div className="hidden md:block" /> // spacer
        )}

        {/* Date field */}
        <div>
          <label htmlFor="kundli-date" className="block text-sm font-medium text-cosmic-text mb-1.5">
            {hi ? 'जन्म तिथि' : 'Birth Date'}
          </label>
          <div className="relative">
            <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
            <Input
              id="kundli-date"
              type="date"
              value={formData.date}
              onChange={(e) => { setFormData({ ...formData, date: e.target.value }); clearError('date'); }}
              className={`pl-10 h-12 bg-sacred-cream border-sacred-gold text-sacred-brown ${validationErrors.date ? 'border-red-500 ring-1 ring-red-500' : ''}`}
            />
          </div>
          {validationErrors.date && <p className="text-red-600 text-xs mt-1">{validationErrors.date}</p>}
        </div>

        {/* Time field */}
        <div>
          <label htmlFor="kundli-time" className="block text-sm font-medium text-cosmic-text mb-1.5">
            {hi ? 'जन्म समय' : 'Birth Time'}
          </label>
          <div className="relative">
            <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
            <Input
              id="kundli-time"
              type="time"
              value={formData.time}
              onChange={(e) => { setFormData({ ...formData, time: e.target.value }); clearError('time'); }}
              className={`pl-10 h-12 bg-sacred-cream border-sacred-gold text-sacred-brown ${validationErrors.time ? 'border-red-500 ring-1 ring-red-500' : ''}`}
            />
          </div>
          {validationErrors.time && <p className="text-red-600 text-xs mt-1">{validationErrors.time}</p>}
        </div>

        {/* Place field */}
        <div className="md:col-span-2">
          <label htmlFor="kundli-place" className="block text-sm font-medium text-cosmic-text mb-1.5">
            {hi ? 'जन्म स्थान' : 'Birth Place'}
          </label>
          <div className="relative" ref={placeWrapperRef}>
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark z-10" />
            <Input
              id="kundli-place"
              type="text"
              value={formData.place}
              onChange={(e) => {
                setFormData({ ...formData, place: e.target.value });
                clearError('place');
                geocode.search(e.target.value);
              }}
              placeholder={hi ? 'जन्म स्थान (खोजने के लिए टाइप करें)' : 'Birth Place (type to search)'}
              className={`pl-10 h-12 bg-sacred-cream border-sacred-gold text-sacred-brown ${validationErrors.place ? 'border-red-500 ring-1 ring-red-500' : ''}`}
              autoComplete="off"
            />
            {geocode.loading && (
              <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 animate-spin text-sacred-gold" />
            )}
            {geocode.showDropdown && geocode.suggestions.length > 0 && (
              <div className="absolute z-50 left-0 right-0 bottom-full mb-1 sm:bottom-auto sm:top-full sm:mt-1 sm:mb-0 bg-white border border-gray-200 rounded-xl shadow-lg max-h-48 overflow-y-auto">
                {geocode.suggestions.map((s, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => {
                      setFormData({ ...formData, place: s.name.split(',')[0], latitude: s.lat, longitude: s.lon });
                      clearError('place');
                      geocode.close();
                    }}
                    className="w-full text-left px-4 py-3 hover:bg-sacred-purple transition-colors border-b border-sacred-gold-dark last:border-b-0"
                  >
                    <p className="text-sm font-medium text-cosmic-text truncate">{s.name}</p>
                    <p className="text-sm text-cosmic-text">{s.lat.toFixed(4)}, {s.lon.toFixed(4)}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
          {validationErrors.place && <p className="text-red-600 text-xs mt-1">{validationErrors.place}</p>}
          
          {/* Location confirmation + collapsible coordinates */}
          {formData.place && (
            <div className="mt-2 flex items-center gap-2 text-sm text-cosmic-text">
              <MapPin className="w-3.5 h-3.5 text-sacred-gold" />
              <span>{hi ? 'स्थान' : 'Location'}: {formData.place.split(',')[0]} &#10003;</span>
              <button
                type="button"
                onClick={() => setShowCoordinates(prev => !prev)}
                className="ml-auto text-xs text-sacred-gold-dark hover:underline flex items-center gap-0.5"
              >
                {hi ? 'निर्देशांक' : 'Coordinates'}
                <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showCoordinates ? 'rotate-180' : ''}`} />
              </button>
            </div>
          )}
          {showCoordinates && (
            <p className="text-xs text-cosmic-text mt-1 pl-5">
              Lat: {formData.latitude.toFixed(4)}, Lon: {formData.longitude.toFixed(4)}
            </p>
          )}
        </div>

        <div className="md:col-span-2 pt-4">
          <Button onClick={handleSubmit} disabled={false} className="w-full h-14 bg-sacred-gold text-white font-bold text-lg rounded-xl shadow-lg hover:bg-sacred-gold/90 transition-all hover:scale-[1.01] active:scale-[0.99]">
            <Sparkles className="w-6 h-6 mr-2" />{hi ? 'कुंडली बनाएं' : 'Generate Kundli'}<ChevronRight className="w-6 h-6 ml-2" />
          </Button>
        </div>
      </div>
    </div>
  );
}
