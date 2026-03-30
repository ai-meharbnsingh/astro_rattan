import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Sparkles, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import KundliForm, { type KundliFormData } from '@/components/kundli/KundliForm';
import KundliList from '@/components/kundli/KundliList';
import JHoraKundliView from '@/components/kundli/JHoraKundliView';

export default function KundliGenerator() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const prefill = (location.state as { birthDate?: string; birthTime?: string; birthPlace?: string }) || {};

  const [step, setStep] = useState<'loading' | 'list' | 'form' | 'generating' | 'result'>('loading');
  const [formData, setFormData] = useState<KundliFormData>({
    name: '',
    date: prefill.birthDate || '',
    time: prefill.birthTime || '',
    place: prefill.birthPlace || '',
    latitude: 28.6139,
    longitude: 77.2090,
    gender: 'male' as 'male' | 'female',
  });
  const [result, setResult] = useState<any>(null);
  const [savedKundlis, setSavedKundlis] = useState<any[]>([]);
  const [dashaData, setDashaData] = useState<any>(null);
  const [loadingDasha, setLoadingDasha] = useState(false);
  const [avakhadaData, setAvakhadaData] = useState<any>(null);
  const [loadingAvakhada, setLoadingAvakhada] = useState(false);
  const [extendedDashaData, setExtendedDashaData] = useState<any>(null);
  const [loadingExtendedDasha, setLoadingExtendedDasha] = useState(false);
  const [yogaDoshaData, setYogaDoshaData] = useState<any>(null);
  const [loadingYogaDosha, setLoadingYogaDosha] = useState(false);
  const [divisionalData, setDivisionalData] = useState<any>(null);
  const [loadingDivisional, setLoadingDivisional] = useState(false);
  const [ashtakvargaData, setAshtakvargaData] = useState<any>(null);
  const [loadingAshtakvarga, setLoadingAshtakvarga] = useState(false);
  const [shadbalaData, setShadbalaData] = useState<any>(null);
  const [loadingShadbala, setLoadingShadbala] = useState(false);
  const [transitData, setTransitData] = useState<any>(null);
  const [loadingTransit, setLoadingTransit] = useState(false);
  const [d10Data, setD10Data] = useState<any>(null);
  const [loadingD10, setLoadingD10] = useState(false);
  const [error, setError] = useState('');

  // Helper to reset all data when switching kundlis
  const resetTabData = () => {
    setDashaData(null);
    setAvakhadaData(null);
    setExtendedDashaData(null);
    setYogaDoshaData(null);
    setDivisionalData(null);
    setAshtakvargaData(null);
    setShadbalaData(null);
    setTransitData(null);
    setD10Data(null);
  };

  // On mount: load existing kundlis if logged in
  useEffect(() => {
    if (!isAuthenticated) {
      setStep('form');
      return;
    }
    api.get('/api/kundli/list')
      .then((data: any) => {
        const list = Array.isArray(data) ? data : [];
        setSavedKundlis(list);
        if (list.length > 0) {
          setStep('list');
        } else {
          setStep('form');
        }
      })
      .catch(() => setStep('form'));
  }, [isAuthenticated]);

  // Load a saved kundli into result view
  const loadKundli = async (kundli: any) => {
    try {
      const full = await api.get(`/api/kundli/${kundli.id}`);
      setResult(full);
      setFormData({
        name: full.person_name || kundli.person_name || '',
        date: full.birth_date || '',
        time: full.birth_time || '',
        place: full.birth_place || '',
        latitude: full.latitude || 28.6139,
        longitude: full.longitude || 77.2090,
        gender: 'male',
      });
      resetTabData();
      setStep('result');
    } catch {
      setError('Failed to load kundli');
    }
  };

  // Refresh saved kundlis list
  const fetchSavedKundlis = async () => {
    if (!isAuthenticated) return;
    try {
      const data = await api.get('/api/kundli');
      setSavedKundlis(data || []);
    } catch {
      setSavedKundlis([]);
    }
  };

  // Fetch dasha
  const fetchDasha = async () => {
    if (!result?.id || dashaData) return;
    setLoadingDasha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/dasha`, {});
      setDashaData(data);
    } catch { /* fallback */ }
    setLoadingDasha(false);
  };

  // Fetch Avakhada Chakra
  const fetchAvakhada = async () => {
    if (!result?.id || avakhadaData) return;
    setLoadingAvakhada(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/avakhada`);
      setAvakhadaData(data);
    } catch { /* fallback handled in UI */ }
    setLoadingAvakhada(false);
  };

  // Fetch Extended Dasha (Mahadasha -> Antardasha -> Pratyantar)
  const fetchExtendedDasha = async () => {
    if (!result?.id || extendedDashaData) return;
    setLoadingExtendedDasha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/extended-dasha`, {});
      setExtendedDashaData(data);
    } catch { /* fallback */ }
    setLoadingExtendedDasha(false);
  };

  // Fetch Yogas & Doshas
  const fetchYogaDosha = async () => {
    if (!result?.id || yogaDoshaData) return;
    setLoadingYogaDosha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/yogas-doshas`, {});
      setYogaDoshaData(data);
    } catch { /* fallback */ }
    setLoadingYogaDosha(false);
  };

  // Fetch divisional chart (D9 Navamsha by default)
  const fetchDivisional = async (chartType: string = 'D9') => {
    if (!result?.id) return;
    setLoadingDivisional(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: chartType });
      setDivisionalData(data);
    } catch { /* fallback */ }
    setLoadingDivisional(false);
  };

  // Fetch ashtakvarga
  const fetchAshtakvarga = async () => {
    if (!result?.id || ashtakvargaData) return;
    setLoadingAshtakvarga(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/ashtakvarga`, {});
      setAshtakvargaData(data);
    } catch { /* fallback */ }
    setLoadingAshtakvarga(false);
  };

  // Fetch shadbala
  const fetchShadbala = async () => {
    if (!result?.id || shadbalaData) return;
    setLoadingShadbala(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/shadbala`, {});
      setShadbalaData(data);
    } catch { /* fallback */ }
    setLoadingShadbala(false);
  };

  // Fetch transits (Gochara)
  const fetchTransit = async () => {
    if (!result?.id || transitData) return;
    setLoadingTransit(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/transits`, {});
      setTransitData(data);
    } catch { /* fallback */ }
    setLoadingTransit(false);
  };

  // Fetch D10 Dashamsha chart
  const fetchD10 = async () => {
    if (!result?.id || d10Data) return;
    setLoadingD10(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: 'D10' });
      setD10Data(data);
    } catch { /* fallback */ }
    setLoadingD10(false);
  };

  // Auto-fetch data for the Report tab when result is loaded
  useEffect(() => {
    if (step === 'result' && result?.id) {
      fetchDasha();
      fetchExtendedDasha();
      fetchAvakhada();
      fetchYogaDosha();
      fetchAshtakvarga();
      fetchShadbala();
      fetchDivisional('D9');
      fetchD10();
      fetchTransit();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [step, result?.id]);

  // Prashna Kundli — generate for current moment using browser geolocation
  const handlePrashnaKundli = async () => {
    if (!isAuthenticated) {
      setError('Sign in is required to generate and save a kundli.');
      return;
    }
    setStep('generating');
    setError('');

    // Try browser geolocation; fall back to Delhi if denied/unavailable
    let lat = 28.6139;
    let lon = 77.2090;
    let placeName = 'Delhi';
    try {
      const pos = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 });
      });
      lat = pos.coords.latitude;
      lon = pos.coords.longitude;
      placeName = `Current Location (${lat.toFixed(4)}, ${lon.toFixed(4)})`;
    } catch {
      // Geolocation denied or unavailable — use Delhi defaults
    }

    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:00`;
    setFormData({
      name: `Prashna ${dateStr}`,
      date: dateStr,
      time: `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`,
      place: placeName,
      latitude: lat,
      longitude: lon,
      gender: 'male',
    });
    try {
      const data = await api.post('/api/kundli/generate', {
        person_name: `Prashna ${dateStr}`,
        birth_date: dateStr,
        birth_time: timeStr,
        birth_place: placeName,
        latitude: lat,
        longitude: lon,
        timezone_offset: 5.5,
      });
      setResult(data);
      resetTabData();
      setStep('result');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate Prashna Kundli');
      setStep('form');
    }
  };

  const handleGenerate = async () => {
    if (!formData.name || !formData.date || !formData.time || !formData.place) return;
    if (!isAuthenticated) {
      setError('Sign in is required to generate and save a kundli.');
      return;
    }
    setStep('generating');
    setError('');
    try {
      const data = await api.post('/api/kundli/generate', {
        person_name: formData.name,
        birth_date: formData.date,
        birth_time: formData.time + ':00',
        birth_place: formData.place,
        latitude: formData.latitude,
        longitude: formData.longitude,
        timezone_offset: 5.5,
      });
      setResult(data);
      resetTabData();
      setStep('result');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate kundli');
      setStep('form');
    }
  };

  // --- LOADING ---
  if (step === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  // --- MY KUNDLIS LIST --- (delegated to KundliList)
  if (step === 'list') {
    return (
      <KundliList
        savedKundlis={savedKundlis}
        onLoadKundli={loadKundli}
        onNewKundli={() => setStep('form')}
        onPrashnaKundli={handlePrashnaKundli}
        onDeleteKundli={fetchSavedKundlis}
      />
    );
  }

  // --- GENERATING SPINNER ---
  if (step === 'generating') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] py-20">
        <div className="relative w-32 h-32 mb-8">
          <div className="absolute inset-0 rounded-full border-4 border-sacred-gold/20" />
          <div className="absolute inset-0 rounded-full border-4 border-sacred-gold border-t-transparent animate-spin" />
          <div className="absolute inset-4 rounded-full bg-sacred-gold/10 flex items-center justify-center">
            <Sparkles className="w-10 h-10 text-sacred-gold animate-pulse" />
          </div>
        </div>
        <h3 className="text-2xl font-sacred font-bold text-sacred-brown mb-2">Generating Your Kundli</h3>
        <p className="text-sacred-text-secondary">Analyzing planetary positions...</p>
      </div>
    );
  }

  // --- RESULT VIEW ---
  if (step === 'result' && result) {
    const planetsRaw = result.chart_data?.planets || {};
    const planets = Array.isArray(planetsRaw)
      ? planetsRaw
      : Object.entries(planetsRaw).map(([name, data]: [string, any]) => ({
          planet: name,
          sign: data?.sign || 'Unknown',
          house: data?.house || 0,
          nakshatra: data?.nakshatra || '',
          sign_degree: data?.sign_degree || 0,
          status: data?.sign_degree < 5 ? 'Entering' : data?.sign_degree > 25 ? 'Leaving' : 'Transiting',
        }));

    const handleDownloadPDF = async () => {
      try {
        const token = localStorage.getItem('astrovedic_token');
        const API_BASE = import.meta.env.VITE_API_URL || '';
        const resp = await fetch(`${API_BASE}/api/kundli/${result.id}/pdf`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({ detail: resp.statusText }));
          throw new Error(err.detail || 'PDF download failed');
        }
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kundli-${result.person_name || 'report'}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (e: any) {
        console.error('PDF download error:', e);
        alert(e.message || 'Failed to download PDF');
      }
    };

    return (
      <div className="pt-20 bg-transparent">
        <JHoraKundliView
          result={result}
          planets={planets}
          dashaData={dashaData}
          extendedDashaData={extendedDashaData}
          avakhadaData={avakhadaData}
          yogaDoshaData={yogaDoshaData}
          ashtakvargaData={ashtakvargaData}
          shadbalaData={shadbalaData}
          divisionalData={divisionalData}
          d10Data={d10Data}
          transitData={transitData}
          loadingDasha={loadingDasha}
          loadingAvakhada={loadingAvakhada}
          loadingYogaDosha={loadingYogaDosha}
          loadingAshtakvarga={loadingAshtakvarga}
          loadingShadbala={loadingShadbala}
          loadingDivisional={loadingDivisional}
          loadingD10={loadingD10}
          loadingTransit={loadingTransit}
          onBack={() => { setStep('list'); setResult(null); }}
          onDownloadPDF={handleDownloadPDF}
        />

      </div>
    );
  }

  // --- FORM VIEW --- (delegated to KundliForm)
  return (
    <KundliForm
      formData={formData}
      setFormData={setFormData}
      error={error}
      savedKundlisCount={savedKundlis.length}
      onGenerate={handleGenerate}
      onPrashnaKundli={handlePrashnaKundli}
      onBackToList={() => setStep('list')}
    />
  );
}
