import { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, ChevronDown, Download, Share2, FileText, Heart, Briefcase, Activity, ArrowLeft, Loader2, X, CheckCircle, AlertTriangle, Shield, Printer, ScrollText } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import { isPuterAvailable, puterChatStream, VEDIC_SYSTEM_PROMPT } from '@/lib/puter-ai';
import InteractiveKundli, { ChartLegend, type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { PLANET_ASPECTS, getHouseSignificance, DIVISIONAL_CHART_OPTIONS } from '@/components/kundli/kundli-utils';
import { calculateJaiminiKarakas } from '@/components/kundli/jhora-utils';
import KundliForm, { type KundliFormData } from '@/components/kundli/KundliForm';
import KundliList from '@/components/kundli/KundliList';
import BirthDetailsTab from '@/components/kundli/BirthDetailsTab';
import LordshipsTab from '@/components/kundli/LordshipsTab';
import PredictionsTab from '@/components/kundli/PredictionsTab';
import ConsolidatedReport from '@/components/kundli/ConsolidatedReport';
import KundliSummaryModal from '@/components/KundliSummaryModal';
import JHoraKundliView from '@/components/kundli/JHoraKundliView';
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';

export default function KundliGenerator() {
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();
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
  const [doshaData, setDoshaData] = useState<any>(null);
  const [iogitaData, setIogitaData] = useState<any>(null);
  const [dashaData, setDashaData] = useState<any>(null);
  const [loadingDosha, setLoadingDosha] = useState(false);
  const [loadingIogita, setLoadingIogita] = useState(false);
  const [loadingDasha, setLoadingDasha] = useState(false);
  const [predictionsData, setPredictionsData] = useState<Record<string, any>>({});
  const [loadingPredictions, setLoadingPredictions] = useState(false);
  const [activePredictionPeriod, setActivePredictionPeriod] = useState<'general' | 'daily' | 'monthly' | 'yearly'>('general');
  const [avakhadaData, setAvakhadaData] = useState<any>(null);
  const [loadingAvakhada, setLoadingAvakhada] = useState(false);
  const [extendedDashaData, setExtendedDashaData] = useState<any>(null);
  const [loadingExtendedDasha, setLoadingExtendedDasha] = useState(false);
  const [expandedMahadasha, setExpandedMahadasha] = useState<string | null>(null);
  const [expandedAntardasha, setExpandedAntardasha] = useState<string | null>(null);
  const [yogaDoshaData, setYogaDoshaData] = useState<any>(null);
  const [loadingYogaDosha, setLoadingYogaDosha] = useState(false);
  const [divisionalData, setDivisionalData] = useState<any>(null);
  const [loadingDivisional, setLoadingDivisional] = useState(false);
  const [selectedDivision, setSelectedDivision] = useState('D9');
  const [ashtakvargaData, setAshtakvargaData] = useState<any>(null);
  const [loadingAshtakvarga, setLoadingAshtakvarga] = useState(false);
  const [shadbalaData, setShadbalaData] = useState<any>(null);
  const [loadingShadbala, setLoadingShadbala] = useState(false);
  const [transitData, setTransitData] = useState<any>(null);
  const [loadingTransit, setLoadingTransit] = useState(false);
  const [d10Data, setD10Data] = useState<any>(null);
  const [loadingD10, setLoadingD10] = useState(false);
  const [varshphalData, setVarshphalData] = useState<any>(null);
  const [loadingVarshphal, setLoadingVarshphal] = useState(false);
  const [varshphalYear, setVarshphalYear] = useState(new Date().getFullYear());
  const [error, setError] = useState('');
  const [reportOpen, setReportOpen] = useState(false);
  const [summaryOpen, setSummaryOpen] = useState(false);
  const [jhoraOpen, setJhoraOpen] = useState(false);
  const [sidePanel, setSidePanel] = useState<{
    type: 'planet' | 'house';
    planet?: PlanetData;
    house?: number;
    sign?: string;
    planets?: PlanetData[];
  } | null>(null);

  const HOUSE_SIGNIFICANCE = getHouseSignificance(t);

  const handlePlanetClick = useCallback((planet: PlanetData) => {
    setSidePanel({ type: 'planet', planet });
  }, []);

  const handleHouseClick = useCallback((house: number, sign: string, planets: PlanetData[]) => {
    setSidePanel({ type: 'house', house, sign, planets });
  }, []);

  // Helper to reset all tab data
  const resetTabData = () => {
    setDoshaData(null);
    setIogitaData(null);
    setDashaData(null);
    setPredictionsData({});
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

  // Fetch dosha for current kundli
  const fetchDosha = async () => {
    if (!result?.id || doshaData) return;
    setLoadingDosha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/dosha`, {});
      setDoshaData(data);
    } catch { /* fallback handled in UI */ }
    setLoadingDosha(false);
  };

  // Fetch io-gita analysis
  const fetchIogita = async () => {
    if (!result?.id || iogitaData) return;
    setLoadingIogita(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/iogita`, {});
      setIogitaData(data);
    } catch { /* fallback handled in UI */ }
    setLoadingIogita(false);
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

  // Fetch divisional chart
  const fetchDivisional = async (chartType?: string) => {
    if (!result?.id) return;
    const ct = chartType || selectedDivision;
    if (ct === 'Moon') {
      // Moon chart is computed client-side
      const moonPlanet = planets.find((p: any) => p.planet === 'Moon');
      const shift = (moonPlanet?.house || 1) - 1;
      const moonPositions = planets.map((p: any) => ({
        planet: p.planet,
        sign: p.sign,
        house: ((p.house - 1 - shift + 12) % 12) + 1,
        nakshatra: p.nakshatra || '',
        sign_degree: p.sign_degree || 0,
      }));
      const moonHouses = result.chart_data?.houses
        ? result.chart_data.houses.map((h: any) => ({
            number: ((h.number - 1 - shift + 12) % 12) + 1,
            sign: h.sign,
          }))
        : undefined;
      setDivisionalData({ planet_positions: moonPositions, houses: moonHouses });
      return;
    }
    setLoadingDivisional(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: ct });
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

  // Fetch D10 Dashamsha
  const fetchD10 = async () => {
    if (!result?.id || d10Data) return;
    setLoadingD10(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: 'D10' });
      setD10Data(data);
    } catch { /* fallback */ }
    setLoadingD10(false);
  };

  // Fetch Varshphal
  const fetchVarshphal = async (year?: number) => {
    if (!result?.id) return;
    setLoadingVarshphal(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/varshphal`, { year: year || varshphalYear });
      setVarshphalData(data);
    } catch { /* fallback */ }
    setLoadingVarshphal(false);
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
      fetchTransit();
      fetchDosha();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [step, result?.id]);

  // Build a textual summary of chart data for Puter AI prompt
  const buildChartPrompt = (): string => {
    const planetsRaw = result?.chart_data?.planets || {};
    const planetsList = Array.isArray(planetsRaw)
      ? planetsRaw.map((p: any) => `${p.planet} in ${p.sign} (House ${p.house}, ${p.sign_degree?.toFixed(1) || '?'}deg, Nakshatra: ${p.nakshatra || 'unknown'})`)
      : Object.entries(planetsRaw).map(([name, data]: [string, any]) =>
          `${name} in ${data?.sign || '?'} (House ${data?.house || '?'}, ${data?.sign_degree?.toFixed(1) || '?'}deg, Nakshatra: ${data?.nakshatra || 'unknown'})`);
    const personName = result?.person_name || formData.name || 'the native';
    const birthInfo = `Born: ${result?.birth_date || formData.date} at ${result?.birth_time || formData.time}, ${result?.birth_place || formData.place}`;
    return `Analyze this Vedic birth chart for ${personName} and provide detailed predictions.\n\n${birthInfo}\n\nPlanets:\n${planetsList.join('\n')}\n\nProvide predictions for: Career, Relationships, Health, Finance, Spiritual Growth.\nFormat each category with a heading and 2-3 paragraphs of insight.`;
  };

  // Fetch AI predictions — backend first, Puter.js fallback
  const fetchPredictions = async (period: 'general' | 'daily' | 'monthly' | 'yearly' = 'general') => {
    if (!result?.id) return;
    setActivePredictionPeriod(period);
    // If we already have data for this period, just switch to it
    if (predictionsData[period]) return;
    setLoadingPredictions(true);
    try {
      const data = await api.post('/api/ai/interpret', { kundli_id: result.id, prediction_type: period });
      setPredictionsData(prev => ({ ...prev, [period]: data }));
      setLoadingPredictions(false);
      return;
    } catch {
      // Backend failed (quota exhausted, network error, etc.) — try Puter.js
    }

    if (isPuterAvailable()) {
      try {
        const periodInstructions: Record<string, string> = {
          general: 'Provide predictions for: Career, Relationships, Health, Finance, Spiritual Growth.\nFormat each category with a heading and 2-3 paragraphs of insight.',
          daily: `Provide a DAILY horoscope prediction for today. Cover: general outlook, career, relationships, health, and a lucky tip. Keep it concise and actionable.`,
          monthly: `Provide a MONTHLY prediction for this month. Cover: career & finance, relationships, health, and key dates to watch.`,
          yearly: `Provide a YEARLY prediction for this year. Cover: overall theme, career, finance, relationships, health, and quarter-by-quarter highlights.`,
        };
        const prompt = buildChartPrompt().replace(
          'Provide predictions for: Career, Relationships, Health, Finance, Spiritual Growth.\nFormat each category with a heading and 2-3 paragraphs of insight.',
          periodInstructions[period] || periodInstructions.general
        );
        // Use streaming so the user sees text appear gradually
        setPredictionsData(prev => ({ ...prev, [period]: { interpretation: '', _streaming: true } }));
        setLoadingPredictions(false);
        const fullText = await puterChatStream(prompt, VEDIC_SYSTEM_PROMPT, (accumulated) => {
          setPredictionsData(prev => ({ ...prev, [period]: { interpretation: accumulated, _streaming: true } }));
        });
        setPredictionsData(prev => ({ ...prev, [period]: { interpretation: fullText, _puterFallback: true } }));
      } catch {
        // Don't clear other periods on failure
      }
    }
    setLoadingPredictions(false);
  };

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
    // Dignity map for calculating planet status
    const dignityMap: Record<string, { exalted: string[]; debilitated: string[]; own: string[] }> = {
      Sun: { exalted: ['Aries'], debilitated: ['Libra'], own: ['Leo'] },
      Moon: { exalted: ['Taurus'], debilitated: ['Scorpio'], own: ['Cancer'] },
      Mars: { exalted: ['Capricorn'], debilitated: ['Cancer'], own: ['Aries', 'Scorpio'] },
      Mercury: { exalted: ['Virgo'], debilitated: ['Pisces'], own: ['Gemini', 'Virgo'] },
      Jupiter: { exalted: ['Cancer'], debilitated: ['Capricorn'], own: ['Sagittarius', 'Pisces'] },
      Venus: { exalted: ['Pisces'], debilitated: ['Virgo'], own: ['Taurus', 'Libra'] },
      Saturn: { exalted: ['Libra'], debilitated: ['Aries'], own: ['Capricorn', 'Aquarius'] },
      Rahu: { exalted: ['Gemini', 'Taurus'], debilitated: ['Sagittarius', 'Scorpio'], own: [] },
      Ketu: { exalted: ['Sagittarius', 'Scorpio'], debilitated: ['Gemini', 'Taurus'], own: [] },
    };
    const calcDignity = (planet: string, sign: string): string => {
      const d = dignityMap[planet];
      if (!d) return 'Neutral';
      if (d.exalted.includes(sign)) return 'Exalted';
      if (d.debilitated.includes(sign)) return 'Debilitated';
      if (d.own.includes(sign)) return 'Own Sign';
      return 'Neutral';
    };

    const planetsRaw = result.chart_data?.planets || {};
    const planets = Array.isArray(planetsRaw)
      ? planetsRaw.map((p: any) => ({
          ...p,
          status: p.status && !['Transiting', 'Entering', 'Leaving'].includes(p.status) ? p.status : calcDignity(p.planet, p.sign),
          is_retrograde: p.is_retrograde || p.retrograde || (p.status?.toLowerCase()?.includes('retrograde')),
          is_combust: p.is_combust || p.combust || (p.status?.toLowerCase()?.includes('combust')),
          is_vargottama: p.is_vargottama || p.vargottama || (p.status?.toLowerCase()?.includes('vargottama')),
        }))
      : Object.entries(planetsRaw).map(([name, data]: [string, any]) => ({
          planet: name,
          sign: data?.sign || 'Unknown',
          house: data?.house || 0,
          nakshatra: data?.nakshatra || '',
          sign_degree: data?.sign_degree || 0,
          status: data?.status && !['Transiting', 'Entering', 'Leaving'].includes(data.status) ? data.status : calcDignity(name, data?.sign || ''),
          is_retrograde: data?.is_retrograde || data?.retrograde || false,
          is_combust: data?.is_combust || data?.combust || false,
          is_vargottama: data?.is_vargottama || data?.vargottama || false,
        }));

    // Inject Lagna as first entry in planets list
    const asc = result.chart_data?.ascendant;
    if (asc && !planets.some((p: any) => p.planet === 'Lagna')) {
      planets.unshift({
        planet: 'Lagna',
        sign: asc.sign || '',
        house: 1,
        nakshatra: '',
        sign_degree: asc.sign_degree ?? (asc.longitude % 30),
        status: '',
        is_retrograde: false,
        is_combust: false,
        is_vargottama: false,
      });
    }

    // Dosha display data
    const doshaDisplay = doshaData ? {
      mangal: doshaData.mangal_dosha || { has_dosha: false, severity: 'none', description: 'No data' },
      kaalsarp: doshaData.kaal_sarp_dosha || { has_dosha: false, severity: 'none', description: 'No data' },
      sadesati: doshaData.sade_sati || { has_sade_sati: false, phase: 'none', description: 'No data' },
    } : null;

    return (
      <div className="max-w-4xl mx-auto pt-24 pb-48 px-4 bg-transparent">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            {savedKundlis.length > 0 && (
              <Button variant="ghost" size="sm" onClick={() => { setStep('list'); setResult(null); }}>
                <ArrowLeft className="w-4 h-4" />
              </Button>
            )}
            <div>
              <h3 className="font-display font-bold text-2xl text-sacred-brown">{result.person_name || formData.name}&apos;s Kundli</h3>
              <p className="text-sm text-sacred-text-secondary">{result.birth_date || formData.date} | {result.birth_time || formData.time} | {result.birth_place || formData.place}</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="border-sacred-gold/50 text-sacred-brown">
              <Share2 className="w-4 h-4 mr-1" />Share
            </Button>
            <Button size="sm" className="btn-sacred" onClick={async () => {
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
            }}>
              <Download className="w-4 h-4 mr-1" />Download
            </Button>
          </div>
        </div>

        {/* Reports banner */}
        <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-2xl p-6 mb-8 border border-sacred-gold/20">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="font-display font-bold text-sacred-brown flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-sacred-gold" />Get Detailed PDF Reports
              </h4>
              <p className="text-sm text-sacred-text-secondary">Unlock 30+ page personalized reports with in-depth analysis</p>
            </div>
            <Button variant="outline" className="border-sacred-gold text-sacred-gold-dark">  View All Reports</Button>
          </div>
          <div className="grid grid-cols-4 gap-3">
            {[
              { icon: FileText, name: 'Complete Analysis', price: '\u20b9999' },
              { icon: Heart, name: 'Marriage', price: '\u20b9799' },
              { icon: Briefcase, name: 'Career', price: '\u20b9799' },
              { icon: Activity, name: 'Health', price: '\u20b9699' },
            ].map(({ icon: Icon, name, price }) => (
              <button key={name} className="bg-cosmic-card/60 rounded-xl p-3 border border-sacred-gold/20 hover:border-sacred-gold/50 transition-colors text-left">
                <Icon className="w-5 h-5 text-sacred-gold mb-2" />
                <p className="text-sm font-medium text-sacred-brown">{name}</p>
                <p className="text-xs text-sacred-gold-dark">{price}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="report" className="w-full">
          <TabsList className="mb-6 bg-sacred-cream flex-wrap">
            <TabsTrigger value="report" onClick={() => { fetchDasha(); fetchExtendedDasha(); fetchAvakhada(); fetchYogaDosha(); fetchAshtakvarga(); fetchShadbala(); fetchDivisional('D9'); }}><ScrollText className="w-3 h-3 mr-1" />Report</TabsTrigger>
            <TabsTrigger value="planets">Planets</TabsTrigger>
            <TabsTrigger value="details">Details</TabsTrigger>
            <TabsTrigger value="lordships">Lordships</TabsTrigger>
            <TabsTrigger value="dosha" onClick={fetchDosha}>Dosha</TabsTrigger>
            <TabsTrigger value="iogita" onClick={fetchIogita}>io-gita</TabsTrigger>
            <TabsTrigger value="dasha" onClick={() => { fetchDasha(); fetchExtendedDasha(); }}>Dasha</TabsTrigger>
            <TabsTrigger value="divisional" onClick={() => fetchDivisional()}>Divisional</TabsTrigger>
            <TabsTrigger value="ashtakvarga" onClick={fetchAshtakvarga}>Ashtakvarga</TabsTrigger>
            <TabsTrigger value="shadbala" onClick={fetchShadbala}>Shadbala</TabsTrigger>
            <TabsTrigger value="avakhada" onClick={fetchAvakhada}>Avakhada</TabsTrigger>
            <TabsTrigger value="yoga-dosha" onClick={fetchYogaDosha}>Yogas</TabsTrigger>
            <TabsTrigger value="predictions" onClick={() => fetchPredictions()}>Predictions</TabsTrigger>
            <TabsTrigger value="transits" onClick={fetchTransit}>Transits</TabsTrigger>
            <TabsTrigger value="varshphal" onClick={() => fetchVarshphal()}>Varshphal</TabsTrigger>
          </TabsList>

          {/* REPORT TAB — Consolidated single-page view */}
          <TabsContent value="report">
            <div className="space-y-6">
              {/* View Buttons */}
              <div className="flex justify-center gap-3">
                <Button
                  size="lg"
                  className="bg-[#d4af37] text-black hover:bg-[#ffd700] px-8"
                  onClick={() => {
                    fetchTransit();
                    fetchD10();
                    fetchDasha();
                    fetchExtendedDasha();
                    setJhoraOpen(true);
                  }}
                >
                  <ScrollText className="w-5 h-5 mr-2" />
                  JHora View
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-[#d4af37]/50 text-[#d4af37] hover:bg-[#d4af37]/10 px-8"
                  onClick={() => {
                    fetchTransit();
                    setReportOpen(true);
                  }}
                >
                  <ScrollText className="w-5 h-5 mr-2" />
                  Full Report
                </Button>
              </div>

              {/* JHora-style Fullscreen Overlay */}
              {jhoraOpen && (
                <div className="fixed inset-0 z-[9999] bg-[#FDF8F0]" style={{ width: '100vw', height: '100vh' }}>
                  <button onClick={() => setJhoraOpen(false)} className="absolute top-2 right-3 z-10 p-1.5 hover:bg-black/10 rounded text-[#D4A052] text-sm font-bold" title="Close">
                    <X className="w-5 h-5" />
                  </button>
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
                      loadingExtendedDasha={loadingExtendedDasha}
                      loadingAvakhada={loadingAvakhada}
                      loadingYogaDosha={loadingYogaDosha}
                      loadingAshtakvarga={loadingAshtakvarga}
                      loadingShadbala={loadingShadbala}
                      loadingDivisional={loadingDivisional}
                      loadingD10={loadingD10}
                      loadingTransit={loadingTransit}
                      onBack={() => setJhoraOpen(false)}
                      onDownloadPDF={async () => {}}
                    />
                </div>
              )}

              {/* Consolidated Report Popup */}
              <ConsolidatedReport
                open={reportOpen}
                onOpenChange={setReportOpen}
                result={result}
                planets={planets}
                dashaData={dashaData}
                avakhadaData={avakhadaData}
                yogaDoshaData={yogaDoshaData}
                ashtakvargaData={ashtakvargaData}
                shadbalaData={shadbalaData}
                divisionalData={divisionalData}
                loadingDasha={loadingDasha}
                loadingAvakhada={loadingAvakhada}
                loadingYogaDosha={loadingYogaDosha}
                loadingAshtakvarga={loadingAshtakvarga}
                loadingShadbala={loadingShadbala}
                loadingDivisional={loadingDivisional}
              />

              {/* Action bar */}
              <div className="flex flex-wrap gap-3 justify-end">
                <Button size="sm" className="btn-sacred" onClick={async () => {
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
                }}>
                  <Download className="w-4 h-4 mr-1" />Download PDF
                </Button>
                <Button size="sm" variant="outline" className="border-sacred-gold/50 text-sacred-brown" onClick={() => window.print()}>
                  <Printer className="w-4 h-4 mr-1" />Print
                </Button>
              </div>

              {/* Report title */}
              <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-2xl p-5 border border-sacred-gold/20 text-center">
                <h3 className="font-display font-bold text-xl text-sacred-brown">Consolidated Report</h3>
                <p className="text-sm text-sacred-text-secondary mt-1">{result.person_name} | {result.birth_date} | {result.birth_time} | {result.birth_place}</p>
              </div>

              {/* Charts row — Lagna, Moon, Gochar side by side */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 print:grid-cols-3">
                {/* 1. Lagna Chart (D1) */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">Lagna</h4>
                  <div className="flex justify-center">
                    <InteractiveKundli
                      chartData={{ planets, houses: result.chart_data?.houses, ascendant: result.chart_data?.ascendant } as ChartData}
                      onPlanetClick={handlePlanetClick}
                      onHouseClick={handleHouseClick}
                      compact
                    />
                  </div>
                </div>

                {/* 2. Moon Chart — houses shifted so Moon's house = 1 */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">Moon</h4>
                  <div className="flex justify-center">
                    {(() => {
                      const moonPlanet = planets.find((p: PlanetData) => p.planet === 'Moon');
                      const moonHouse = moonPlanet?.house || 1;
                      const shift = moonHouse - 1;
                      const moonPlanets = planets.map((p: PlanetData) => ({
                        ...p,
                        house: ((p.house - 1 - shift + 12) % 12) + 1,
                      }));
                      const moonHouses = result.chart_data?.houses
                        ? result.chart_data.houses.map((h: { number: number; sign: string }) => ({
                            number: ((h.number - 1 - shift + 12) % 12) + 1,
                            sign: h.sign,
                          }))
                        : undefined;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: moonPlanets, houses: moonHouses } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={handleHouseClick}
                          compact
                        />
                      );
                    })()}
                  </div>
                </div>

                {/* 3. Gochar (Transit) Chart */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">Gochar {transitData?.transit_date ? `(${transitData.transit_date})` : ''}</h4>
                  <div className="flex justify-center">
                    {loadingTransit ? (
                      <div className="flex items-center justify-center py-12"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                    ) : transitData?.transits ? (
                      <InteractiveKundli
                        chartData={{
                          planets: transitData.transits.map((tr: any) => ({
                            planet: tr.planet,
                            sign: tr.current_sign || tr.sign || '',
                            house: tr.house || 1,
                            nakshatra: tr.nakshatra || '',
                            sign_degree: tr.sign_degree || tr.degree || 0,
                            status: tr.is_retrograde ? 'Retrograde' : '',
                            is_retrograde: tr.is_retrograde,
                          })),
                          houses: transitData.chart_data?.houses || result.chart_data?.houses,
                        } as ChartData}
                        onPlanetClick={handlePlanetClick}
                        onHouseClick={handleHouseClick}
                        compact
                      />
                    ) : (
                      <p className="text-center text-sacred-text-secondary py-12 text-sm">Loading transit...</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Chart Legend */}
              <ChartLegend />

              {/* Grid layout — 2 columns on desktop, 1 on mobile */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 print:grid-cols-2">

                {/* 2. Planet Details Table */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Detailed Planet Positions</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead className="bg-sacred-gold/10">
                        <tr>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Planet</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Sign</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">House</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Nak.</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Degree</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {planets.map((planet: any, index: number) => (
                          <tr key={index} className="border-t border-sacred-gold/10 hover:bg-sacred-gold/5">
                            <td className="p-2 text-sacred-brown font-medium">{planet.planet}</td>
                            <td className="p-2 text-sacred-text-secondary">{planet.sign}</td>
                            <td className="p-2 text-center text-sacred-text-secondary">{planet.house}</td>
                            <td className="p-2 text-sacred-text-secondary">{planet.nakshatra || '\u2014'}</td>
                            <td className="p-2 text-center text-sacred-text-secondary">{planet.sign_degree?.toFixed(1)}&deg;</td>
                            <td className="p-2 text-center">
                              <span className={`text-xs px-1 py-0.5 rounded ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-500/20 text-green-400' : 'text-sacred-text-secondary'}`}>
                                {planet.status || '\u2014'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* 3. Divisional Chart (D9 default, dropdown for all) */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-display font-semibold text-sacred-brown">Divisional Chart</h4>
                    <select
                      value={selectedDivision}
                      onChange={(e) => {
                        setSelectedDivision(e.target.value);
                        setDivisionalData(null);
                        fetchDivisional(e.target.value);
                      }}
                      className="bg-[#22223a] border border-sacred-gold/30 rounded-lg px-3 py-1.5 text-sacred-brown text-sm focus:border-sacred-gold focus:outline-none"
                    >
                      {DIVISIONAL_CHART_OPTIONS.map((c) => (
                        <option key={c.code} value={c.code}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  {loadingDivisional ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : divisionalData?.planet_positions ? (
                    <div className="flex justify-center">
                      <InteractiveKundli
                        chartData={{
                          planets: divisionalData.planet_positions.map((p: any) => ({
                            planet: p.planet,
                            sign: p.sign,
                            house: p.house,
                            nakshatra: p.nakshatra || '',
                            sign_degree: p.sign_degree || 0,
                            status: '',
                          })),
                          houses: divisionalData.houses || Array.from({ length: 12 }, (_, i) => ({
                            number: i + 1,
                            sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
                          })),
                        } as ChartData}
                        onPlanetClick={handlePlanetClick}
                        onHouseClick={handleHouseClick}
                      />
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-8 text-sm">Select a chart...</p>
                  )}
                </div>

                {/* 4. Lordships */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">House Lordships</h4>
                  <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
                </div>

                {/* 5. Avakhada Chakra */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Avakhada Chakra</h4>
                  {loadingAvakhada ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : avakhadaData ? (
                    <div className="grid grid-cols-2 gap-2">
                      {[
                        { label: 'Ascendant (Lagna)', value: avakhadaData.ascendant },
                        { label: 'Lagna Lord', value: avakhadaData.ascendant_lord },
                        { label: 'Rashi (Moon Sign)', value: avakhadaData.rashi },
                        { label: 'Rashi Lord', value: avakhadaData.rashi_lord },
                        { label: 'Nakshatra', value: `${avakhadaData.nakshatra} (P${avakhadaData.nakshatra_pada})` },
                        { label: 'Yoga', value: avakhadaData.yoga },
                        { label: 'Karana', value: avakhadaData.karana },
                        { label: 'Yoni', value: avakhadaData.yoni },
                        { label: 'Gana', value: avakhadaData.gana },
                        { label: 'Nadi', value: avakhadaData.nadi },
                        { label: 'Varna', value: avakhadaData.varna },
                        { label: 'Naamakshar', value: avakhadaData.naamakshar },
                        { label: 'Sun Sign (Western)', value: avakhadaData.sun_sign },
                      ].map((item) => (
                        <div key={item.label} className="rounded-lg p-2 bg-cosmic-card/60">
                          <p className="text-[10px] text-sacred-text-secondary">{item.label}</p>
                          <p className="text-xs font-semibold text-sacred-brown">{item.value}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">Loading...</p>
                  )}
                </div>

                {/* 6. Vimshottari Dasha — with expandable AD/PD */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Vimshottari Dasha</h4>
                  {(loadingDasha || loadingExtendedDasha) ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : (extendedDashaData || dashaData) ? (
                    <div className="space-y-2">
                      {/* Current dasha info */}
                      <div className="rounded-lg p-3" style={{ background: 'rgba(184,134,11,0.1)' }}>
                        <p className="text-xs" style={{ color: '#b8b0a4' }}>Current Mahadasha</p>
                        <p className="text-sm font-display font-bold" style={{ color: '#D4A052' }}>
                          {(extendedDashaData || dashaData).current_dasha}
                        </p>
                        {(extendedDashaData || dashaData).current_antardasha && (extendedDashaData || dashaData).current_antardasha !== 'Unknown' && (
                          <p className="text-xs" style={{ color: '#D4A052' }}>
                            AD: {(extendedDashaData || dashaData).current_antardasha}
                            {extendedDashaData?.current_pratyantar && extendedDashaData.current_pratyantar !== 'Unknown' && ` / PD: ${extendedDashaData.current_pratyantar}`}
                          </p>
                        )}
                      </div>

                      {/* Expandable Mahadasha list */}
                      {extendedDashaData?.mahadasha ? (
                        <div className="space-y-1">
                          {extendedDashaData.mahadasha.map((md: any) => (
                            <div key={md.planet} className="border border-sacred-gold/10 rounded-lg overflow-hidden">
                              <button
                                onClick={() => setExpandedMahadasha(expandedMahadasha === md.planet ? null : md.planet)}
                                className="w-full flex items-center justify-between p-2 text-xs transition-colors"
                                style={{ background: md.is_current ? 'rgba(184,134,11,0.12)' : 'transparent' }}
                              >
                                <span className="flex items-center gap-1.5">
                                  <ChevronDown className={`w-3 h-3 transition-transform ${expandedMahadasha === md.planet ? 'rotate-180' : ''}`} style={{ color: '#D4A052' }} />
                                  <span className="font-semibold" style={{ color: md.is_current ? '#D4A052' : '#e8e0d4' }}>
                                    {md.planet} {md.is_current ? '←' : ''}
                                  </span>
                                </span>
                                <span style={{ color: '#b8b0a4' }}>{md.start?.slice(0,10)} — {md.end?.slice(0,10)} ({md.years}y)</span>
                              </button>

                              {expandedMahadasha === md.planet && (md.antardasha || []).length > 0 && (
                                <div className="border-t border-sacred-gold/10">
                                  {md.antardasha.map((ad: any) => (
                                    <div key={`${md.planet}-${ad.planet}`}>
                                      <button
                                        onClick={() => setExpandedAntardasha(expandedAntardasha === `${md.planet}-${ad.planet}` ? null : `${md.planet}-${ad.planet}`)}
                                        className="w-full flex items-center justify-between px-4 py-1.5 text-xs"
                                        style={{ background: ad.is_current ? 'rgba(184,134,11,0.06)' : 'transparent' }}
                                      >
                                        <span className="flex items-center gap-1">
                                          {ad.pratyantar?.length > 0 && <ChevronDown className={`w-2.5 h-2.5 transition-transform ${expandedAntardasha === `${md.planet}-${ad.planet}` ? 'rotate-180' : ''}`} style={{ color: '#b8b0a4' }} />}
                                          <span style={{ color: ad.is_current ? '#D4A052' : '#e8e0d4' }}>{ad.planet} AD {ad.is_current ? '*' : ''}</span>
                                        </span>
                                        <span style={{ color: '#b8b0a4', fontSize: '10px' }}>{ad.start?.slice(0,10)} — {ad.end?.slice(0,10)}</span>
                                      </button>

                                      {expandedAntardasha === `${md.planet}-${ad.planet}` && (ad.pratyantar || []).length > 0 && (
                                        <div className="border-t border-sacred-gold/5">
                                          {ad.pratyantar.map((pt: any, idx: number) => (
                                            <div key={idx} className="flex items-center justify-between px-8 py-1 text-xs"
                                              style={{ background: pt.is_current ? 'rgba(184,134,11,0.04)' : 'transparent' }}>
                                              <span style={{ color: pt.is_current ? '#D4A052' : '#b8b0a4' }}>
                                                {pt.planet} PD {pt.is_current ? '*' : ''}
                                              </span>
                                              <span style={{ color: '#b8b0a4', fontSize: '10px' }}>{pt.start?.slice(0,10)} — {pt.end?.slice(0,10)}</span>
                                            </div>
                                          ))}
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : (
                        /* Fallback: simple table when extendedDashaData unavailable */
                        <div className="overflow-x-auto">
                          <table className="w-full text-xs">
                            <thead><tr style={{ background: 'rgba(184,134,11,0.1)' }}>
                              <th className="text-left p-2 font-medium" style={{ color: '#D4A052' }}>Planet</th>
                              <th className="text-left p-2 font-medium" style={{ color: '#D4A052' }}>Start</th>
                              <th className="text-left p-2 font-medium" style={{ color: '#D4A052' }}>End</th>
                              <th className="text-center p-2 font-medium" style={{ color: '#D4A052' }}>Yrs</th>
                            </tr></thead>
                            <tbody>
                              {(dashaData.mahadasha_periods || []).map((p: any) => (
                                <tr key={p.planet} className="border-t border-sacred-gold/10" style={{ background: p.planet === dashaData.current_dasha ? 'rgba(184,134,11,0.1)' : 'transparent' }}>
                                  <td className="p-2" style={{ color: '#e8e0d4' }}>{p.planet}{p.planet === dashaData.current_dasha ? ' ←' : ''}</td>
                                  <td className="p-2" style={{ color: '#b8b0a4' }}>{p.start_date}</td>
                                  <td className="p-2" style={{ color: '#b8b0a4' }}>{p.end_date}</td>
                                  <td className="p-2 text-center" style={{ color: '#b8b0a4' }}>{p.years}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-center py-4 text-sm" style={{ color: '#b8b0a4' }}>Loading Dasha...</p>
                  )}
                </div>

                {/* 6b. Jaimini Karakas — separate card */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Jaimini Karakas</h4>
                  {(() => {
                    const karakas = calculateJaiminiKarakas(planets);
                    const karakaOrder = [
                      { key: 'AK', name: 'Atmakaraka' },
                      { key: 'AmK', name: 'Amatyakaraka' },
                      { key: 'BK', name: 'Bhratrikaraka' },
                      { key: 'MK', name: 'Matrikaraka' },
                      { key: 'PiK', name: 'Pitrikaraka' },
                      { key: 'GnK', name: 'Gnatikaraka' },
                      { key: 'DK', name: 'Darakaraka' },
                    ];
                    return (
                      <table className="w-full text-xs">
                        <thead><tr className="bg-sacred-gold/10">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Karaka</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Planet</th>
                        </tr></thead>
                        <tbody>
                          {karakaOrder.map(({ key, name }) => {
                            const planet = Object.entries(karakas).find(([, v]) => v === key)?.[0] || '-';
                            return (
                              <tr key={key} className="border-t border-sacred-gold/10">
                                <td className="p-2 text-sacred-brown"><span className="font-semibold">{key}</span> <span className="text-[10px] text-sacred-text-secondary">({name})</span></td>
                                <td className="p-2 font-semibold" style={{ color: '#B8860B' }}>{planet}</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    );
                  })()}
                </div>

                {/* 7. Yoga & Dosha */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4 lg:col-span-2">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Yogas & Doshas</h4>
                  {loadingYogaDosha ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : yogaDoshaData ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <CheckCircle className="w-4 h-4 text-green-500" />
                          <h5 className="text-sm font-semibold text-sacred-brown">Yogas (Positive Combinations)</h5>
                        </div>
                        <div className="space-y-1">
                          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).slice(0, 8).map((yoga: any, idx: number) => (
                            <div key={idx} className="rounded-lg p-2 text-xs border border-green-500/20 bg-green-500/5">
                              <div className="flex items-center justify-between">
                                <span className="font-medium text-sacred-brown">{yoga.name}</span>
                                <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-green-500/20 text-green-400">
                                  Present
                                </span>
                              </div>
                            </div>
                          ))}
                          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).length === 0 && (
                            <p className="text-sm text-sacred-text-secondary py-2">No yogas detected</p>
                          )}
                        </div>
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <Shield className="w-4 h-4 text-red-500" />
                          <h5 className="text-sm font-semibold text-sacred-brown">Doshas (Afflictions)</h5>
                        </div>
                        <div className="space-y-1">
                          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).slice(0, 8).map((dosha: any, idx: number) => (
                            <div key={idx} className="rounded-lg p-2 text-xs border border-red-500/20 bg-red-500/5">
                              <div className="flex items-center justify-between">
                                <span className="font-medium text-sacred-brown">{dosha.name}</span>
                                <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-red-500/20 text-red-400">
                                  Present
                                </span>
                              </div>
                            </div>
                          ))}
                          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).length === 0 && (
                            <p className="text-sm text-green-400 py-2">No doshas detected</p>
                          )}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">Loading Yoga & Dosha analysis...</p>
                  )}
                </div>

                {/* 7b. Mangal / Kaal Sarp / Sade Sati Dosha */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4 lg:col-span-2">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Dosha Analysis (Mangal, Kaal Sarp, Sade Sati)</h4>
                  {loadingDosha ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : doshaData ? (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {/* Mangal Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.mangal_dosha?.has_dosha ? 'border-red-500/30 bg-red-500/5' : 'border-green-500/20 bg-green-500/5'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">Mangal Dosha</h5>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${doshaData.mangal_dosha?.has_dosha ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                            {doshaData.mangal_dosha?.has_dosha ? doshaData.mangal_dosha.severity || 'Present' : 'Absent'}
                          </span>
                        </div>
                        <p className="text-xs text-sacred-text-secondary">{doshaData.mangal_dosha?.description || 'No Mangal Dosha'}</p>
                      </div>
                      {/* Kaal Sarp Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.kaal_sarp_dosha?.has_dosha ? 'border-red-500/30 bg-red-500/5' : 'border-green-500/20 bg-green-500/5'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">Kaal Sarp Dosha</h5>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${doshaData.kaal_sarp_dosha?.has_dosha ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                            {doshaData.kaal_sarp_dosha?.has_dosha ? doshaData.kaal_sarp_dosha.severity || 'Present' : 'Absent'}
                          </span>
                        </div>
                        <p className="text-xs text-sacred-text-secondary">{doshaData.kaal_sarp_dosha?.description || 'No Kaal Sarp Dosha'}</p>
                      </div>
                      {/* Sade Sati */}
                      <div className={`rounded-lg p-3 border ${doshaData.sade_sati?.has_sade_sati ? 'border-orange-500/30 bg-orange-500/5' : 'border-green-500/20 bg-green-500/5'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">Shani Sade Sati</h5>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${doshaData.sade_sati?.has_sade_sati ? 'bg-orange-500/20 text-orange-600' : 'bg-green-500/20 text-green-400'}`}>
                            {doshaData.sade_sati?.has_sade_sati ? `Active - ${doshaData.sade_sati.phase}` : 'Inactive'}
                          </span>
                        </div>
                        <p className="text-xs text-sacred-text-secondary">{doshaData.sade_sati?.description || 'Sade Sati not active'}</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">Loading Dosha analysis...</p>
                  )}
                </div>

                {/* 8. Ashtakvarga SAV bar chart */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Sarvashtakvarga</h4>
                  {loadingAshtakvarga ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : ashtakvargaData ? (
                    <div>
                      <div className="flex items-end gap-1 h-36">
                        {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map((sign) => {
                          const points = ashtakvargaData.sarvashtakvarga?.[sign] || 0;
                          const maxPoints = 56;
                          const heightPct = Math.round((points / maxPoints) * 100);
                          const isStrong = points >= 28;
                          return (
                            <div key={sign} className="flex-1 flex flex-col items-center gap-0.5">
                              <span className="text-[9px] font-medium text-sacred-brown">{points}</span>
                              <div className="w-full bg-sacred-gold/10 rounded-t-sm relative" style={{ height: '100px' }}>
                                <div
                                  className="absolute bottom-0 w-full rounded-t-sm"
                                  style={{ height: `${heightPct}%`, backgroundColor: isStrong ? '#B8860B' : '#b8b0a4' }}
                                />
                              </div>
                              <span className="text-[8px] text-sacred-text-secondary">{sign.slice(0, 3)}</span>
                            </div>
                          );
                        })}
                      </div>
                      <div className="flex items-center gap-3 mt-2 text-[10px] text-sacred-text-secondary">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#B8860B' }} />Strong</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#b8b0a4' }} />Weak</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">Loading Ashtakvarga...</p>
                  )}
                </div>

                {/* 9. Shadbala bar chart */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">Shadbala Strength</h4>
                  {loadingShadbala ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : shadbalaData?.planets ? (
                    <div className="space-y-2">
                      {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                        const data = shadbalaData.planets[planet];
                        if (!data) return null;
                        const pct = Math.min((data.total / data.required) * 100, 150);
                        const barColor = data.is_strong ? '#B8860B' : '#8B2332';
                        return (
                          <div key={planet} className="flex items-center gap-2">
                            <span className="w-12 text-xs font-medium text-sacred-brown">{planet}</span>
                            <div className="flex-1 bg-sacred-gold/10 rounded-full h-4 overflow-hidden">
                              <div className="h-full rounded-full" style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }} />
                            </div>
                            <span className={`text-xs w-16 text-right font-medium ${data.is_strong ? 'text-[#B8860B]' : 'text-[#8B2332]'}`}>
                              {data.total}/{data.required}
                            </span>
                          </div>
                        );
                      })}
                      <div className="flex items-center gap-3 mt-1 text-[10px] text-sacred-text-secondary">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#B8860B' }} />Strong</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#8B2332' }} />Weak</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">Loading Shadbala...</p>
                  )}
                </div>

              </div>
            </div>
          </TabsContent>

          {/* PLANETS TAB - Interactive Kundli Chart + Side Panel */}
          <TabsContent value="planets">
            <div className="flex flex-col xl:flex-row gap-8">
              {/* Interactive Chart */}
              <div className="w-full xl:w-[600px] xl:flex-shrink-0 flex justify-center">
                <InteractiveKundli
                  chartData={{ planets, houses: result.chart_data?.houses, ascendant: result.chart_data?.ascendant } as ChartData}
                  onPlanetClick={handlePlanetClick}
                  onHouseClick={handleHouseClick}
                />
              </div>

              {/* Side Panel - shown when planet or house is clicked */}
              <div className="flex-1 min-w-0">
                {sidePanel ? (
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-5 animate-in fade-in slide-in-from-right-4 duration-300">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="font-display font-bold text-sacred-brown text-lg">
                        {sidePanel.type === 'planet'
                          ? `${sidePanel.planet?.planet} Details`
                          : 'House Details'}
                      </h4>
                      <button
                        onClick={() => setSidePanel(null)}
                        className="text-sacred-text-secondary hover:text-sacred-brown transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>

                    {sidePanel.type === 'planet' && sidePanel.planet && (() => {
                      const p = sidePanel.planet;
                      const status = p.status?.toLowerCase() || '';
                      const strengthLabel = status.includes('exalted') ? 'Exalted' : status.includes('debilitated') ? 'Debilitated' : status.includes('own') ? 'Own Sign' : p.status || 'Transiting';
                      const strengthColor = status.includes('exalted') ? 'text-green-500' : status.includes('debilitated') ? 'text-red-500' : status.includes('own') ? 'text-blue-500' : 'text-sacred-text-secondary';
                      const aspects = (PLANET_ASPECTS[p.planet] || [7]).map((offset) => {
                        const targetHouse = ((p.house - 1 + offset) % 12) + 1;
                        return `House ${targetHouse}`;
                      });

                      return (
                        <div className="space-y-3">
                          <div className="grid grid-cols-2 gap-3">
                            <div className="bg-cosmic-card/60 rounded-lg p-3">
                              <p className="text-xs text-sacred-text-secondary">Sign</p>
                              <p className="font-semibold text-sacred-brown">{p.sign}</p>
                            </div>
                            <div className="bg-cosmic-card/60 rounded-lg p-3">
                              <p className="text-xs text-sacred-text-secondary">Degree</p>
                              <p className="font-semibold text-sacred-brown">{p.sign_degree?.toFixed(1)}&deg;</p>
                            </div>
                            <div className="bg-cosmic-card/60 rounded-lg p-3">
                              <p className="text-xs text-sacred-text-secondary">House</p>
                              <p className="font-semibold text-sacred-brown">{p.house}</p>
                            </div>
                            <div className="bg-cosmic-card/60 rounded-lg p-3">
                              <p className="text-xs text-sacred-text-secondary">Nakshatra</p>
                              <p className="font-semibold text-sacred-brown">{p.nakshatra || 'N/A'}</p>
                            </div>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">Strength</p>
                            <p className={`font-semibold ${strengthColor}`}>{strengthLabel}</p>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">Aspects</p>
                            <p className="font-semibold text-sacred-brown text-sm">{aspects.join(', ')}</p>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">House Placement</p>
                            <p className="text-sm text-sacred-brown">
                              {p.planet} in House {p.house} ({HOUSE_SIGNIFICANCE[p.house] || 'Unknown'})
                            </p>
                          </div>
                        </div>
                      );
                    })()}

                    {sidePanel.type === 'house' && (
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-3">
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">House Number</p>
                            <p className="font-semibold text-sacred-brown">{sidePanel.house}</p>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">Sign</p>
                            <p className="font-semibold text-sacred-brown">{sidePanel.sign}</p>
                          </div>
                        </div>
                        <div className="bg-cosmic-card/60 rounded-lg p-3">
                          <p className="text-xs text-sacred-text-secondary">Significance</p>
                          <p className="font-semibold text-sacred-brown">
                            {HOUSE_SIGNIFICANCE[sidePanel.house || 0] || 'Unknown'}
                          </p>
                        </div>
                        <div className="bg-cosmic-card/60 rounded-lg p-3">
                          <p className="text-xs text-sacred-text-secondary mb-2">Planets in this House</p>
                          {(sidePanel.planets || []).length > 0 ? (
                            <div className="space-y-1">
                              {(sidePanel.planets || []).map((p) => (
                                <button
                                  key={p.planet}
                                  className="w-full text-left text-sm text-sacred-brown hover:text-sacred-gold transition-colors flex items-center gap-2"
                                  onClick={() => setSidePanel({ type: 'planet', planet: p })}
                                >
                                  <span className="w-2 h-2 rounded-full bg-sacred-gold" />
                                  {p.planet} ({p.sign} {p.sign_degree?.toFixed(1)}&deg;)
                                </button>
                              ))}
                            </div>
                          ) : (
                            <p className="text-sm text-sacred-text-secondary">No planets in this house</p>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="bg-sacred-cream/50 rounded-xl border border-dashed border-sacred-gold/20 p-8 flex flex-col items-center justify-center h-full min-h-[200px]">
                    <Sparkles className="w-8 h-8 text-sacred-gold/40 mb-3" />
                    <p className="text-sacred-text-secondary text-sm text-center">
                      Click on any planet or house in the chart to see detailed information
                    </p>
                  </div>
                )}

                {/* Planet table below the side panel */}
                <div className="mt-6 overflow-x-auto rounded-xl border border-sacred-gold/20">
                  <table className="w-full">
                    <thead className="bg-sacred-cream">
                      <tr>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Planet</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Sign</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">House</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Nakshatra</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {planets.map((planet: any, index: number) => (
                        <tr
                          key={index}
                          className={`border-t border-sacred-gold/20 cursor-pointer transition-colors ${
                            sidePanel?.type === 'planet' && sidePanel.planet?.planet === planet.planet
                              ? 'bg-sacred-gold/10'
                              : 'hover:bg-sacred-gold/5'
                          }`}
                          onClick={() => handlePlanetClick(planet)}
                        >
                          <td className="p-3 text-sacred-brown font-medium text-sm">{planet.planet}</td>
                          <td className="p-3 text-sacred-text-secondary text-sm">{planet.sign}</td>
                          <td className="p-3 text-sacred-text-secondary text-sm">{planet.house}</td>
                          <td className="p-3 text-sacred-text-secondary text-sm">{planet.nakshatra || '\u2014'}</td>
                          <td className="p-3">
                            <span className={`text-xs px-2 py-1 rounded-full ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-500/20 text-green-400' : 'bg-cosmic-surface text-sacred-text-secondary'}`}>
                              {planet.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </TabsContent>

          {/* DETAILS TAB -- delegated to BirthDetailsTab */}
          <TabsContent value="details">
            <BirthDetailsTab planets={planets} />
          </TabsContent>

          {/* LORDSHIPS TAB -- delegated to LordshipsTab */}
          <TabsContent value="lordships">
            <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
          </TabsContent>

          {/* DOSHA TAB */}
          <TabsContent value="dosha">
            {loadingDosha ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Analyzing doshas...</span></div>
            ) : doshaDisplay ? (
              <div className="grid gap-4">
                {doshaDisplay.mangal.has_dosha && (
                <div className="bg-sacred-cream rounded-xl p-4 border border-red-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">Mangal Dosha</h4>
                    <span className="text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-400">
                      Present ({doshaDisplay.mangal.severity})
                    </span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.mangal.description}</p>
                </div>
                )}
                {doshaDisplay.kaalsarp.has_dosha && (
                <div className="bg-sacred-cream rounded-xl p-4 border border-red-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">Kaal Sarp Dosha</h4>
                    <span className="text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-400">Present</span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.kaalsarp.description}</p>
                </div>
                )}
                {doshaDisplay.sadesati.has_sade_sati && (
                <div className="bg-sacred-cream rounded-xl p-4 border border-orange-200">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">Shani Sade Sati</h4>
                    <span className="text-xs px-2 py-1 rounded-full bg-orange-100 text-orange-600">
                      Active - {doshaDisplay.sadesati.phase}
                    </span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.sadesati.description}</p>
                </div>
                )}
                {!doshaDisplay.mangal.has_dosha && !doshaDisplay.kaalsarp.has_dosha && !doshaDisplay.sadesati.has_sade_sati && (
                  <p className="text-sm py-4" style={{ color: '#22c55e' }}>No doshas detected - chart is free from Mangal Dosha, Kaal Sarp Dosha, and Sade Sati.</p>
                )}
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Dosha tab to load analysis</p>
            )}
          </TabsContent>

          {/* IO-GITA TAB */}
          <TabsContent value="iogita">
            {loadingIogita ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Analyzing your life path...</span></div>
            ) : iogitaData?.basin ? (
              <div className="space-y-6">
                {/* Overall Summary Card */}
                <div className="rounded-2xl p-6 border border-sacred-gold/30" style={{ background: 'linear-gradient(135deg, rgba(184,134,11,0.08) 0%, rgba(34,34,58,0.9) 100%)' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-full bg-sacred-gold/20 flex items-center justify-center">
                      <Sparkles className="w-6 h-6 text-sacred-gold" />
                    </div>
                    <div>
                      <h4 className="font-display font-bold text-xl" style={{ color: '#D4A052' }}>Your Life Pattern: {iogitaData.basin.name}</h4>
                      <p className="text-sm" style={{ color: '#b8b0a4' }}>Based on your planetary positions and current dasha</p>
                    </div>
                  </div>
                  <p className="text-sm leading-relaxed mb-4" style={{ color: '#e8e0d4' }}>{iogitaData.basin.description}</p>
                </div>

                {/* Strengths — Top Forces */}
                <div className="rounded-xl p-5 border border-sacred-gold/20" style={{ background: 'rgba(34,34,58,0.8)' }}>
                  <h4 className="font-display font-semibold mb-4" style={{ color: '#D4A052' }}>Your Strongest Qualities</h4>
                  <div className="space-y-3">
                    {(iogitaData.basin.top_3_atoms || []).map(([name, val]: [string, number], idx: number) => {
                      const labels: Record<string, string> = {
                        DHARMA: 'Righteousness & Duty', SATYA: 'Truth & Honesty', TYAGA: 'Selflessness',
                        AHANKAR: 'Self-Confidence', ATMA: 'Inner Awareness', MOKSHA: 'Spiritual Liberation',
                        KULA: 'Family & Tradition', RAJYA: 'Leadership & Authority', NYAYA: 'Justice & Fairness',
                        KRODHA: 'Drive & Determination', NITI: 'Strategy & Wisdom', SHAKTI: 'Power & Energy',
                        BHAKTI: 'Devotion & Faith', KAAM: 'Desire & Passion', LOBH: 'Ambition', MOH: 'Attachment & Love',
                      };
                      const colors = ['#D4A052', '#E8C078', '#B8860B'];
                      return (
                        <div key={name} className="flex items-center gap-3">
                          <span className="text-lg font-bold w-6" style={{ color: colors[idx] }}>{idx + 1}</span>
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-sm font-semibold" style={{ color: '#e8e0d4' }}>{labels[name] || name}</span>
                              <span className="text-xs" style={{ color: '#b8b0a4' }}>{Math.round(Math.abs(val) * 100)}%</span>
                            </div>
                            <div className="h-2 rounded-full overflow-hidden" style={{ background: 'rgba(184,134,11,0.15)' }}>
                              <div className="h-full rounded-full" style={{ width: `${Math.abs(val) * 100}%`, background: colors[idx] }} />
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Area to Improve */}
                {iogitaData.basin.top_negative && (
                  <div className="rounded-xl p-5 border border-red-500/20" style={{ background: 'rgba(196,62,78,0.08)' }}>
                    <h4 className="font-display font-semibold mb-2" style={{ color: '#f87171' }}>Area That Needs Attention</h4>
                    {(() => {
                      const negLabels: Record<string, string> = {
                        DHARMA: 'Following your duty', SATYA: 'Being truthful', TYAGA: 'Letting go of attachments',
                        KRODHA: 'Managing anger', LOBH: 'Controlling greed', MOH: 'Detaching from illusions',
                        KAAM: 'Moderating desires', AHANKAR: 'Ego management',
                        BHAKTI: 'Developing devotion', SHAKTI: 'Building inner strength',
                        MOKSHA: 'Spiritual growth', ATMA: 'Self-awareness',
                      };
                      const name = iogitaData.basin.top_negative[0];
                      return <p className="text-sm" style={{ color: '#fca5a5' }}>{negLabels[name] || name} — this area is suppressed in your chart. Focus on developing it for a more balanced life.</p>;
                    })()}
                  </div>
                )}

                {/* Guidance Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="rounded-xl p-5 border border-amber-500/20" style={{ background: 'rgba(245,158,11,0.08)' }}>
                    <h4 className="font-display font-semibold mb-2" style={{ color: '#fbbf24' }}>Be Mindful Of</h4>
                    <p className="text-sm leading-relaxed" style={{ color: '#fde68a' }}>{iogitaData.basin.warning}</p>
                  </div>
                  <div className="rounded-xl p-5 border border-emerald-500/20" style={{ background: 'rgba(16,185,129,0.08)' }}>
                    <h4 className="font-display font-semibold mb-2" style={{ color: '#34d399' }}>Path to Growth</h4>
                    <p className="text-sm leading-relaxed" style={{ color: '#6ee7b7' }}>{iogitaData.basin.escape_trigger}</p>
                  </div>
                </div>

                {/* Overall Insight */}
                {iogitaData.iogita_insight && (
                  <div className="rounded-xl p-5 border border-sacred-gold/20" style={{ background: 'rgba(34,34,58,0.8)' }}>
                    <h4 className="font-display font-semibold mb-3" style={{ color: '#D4A052' }}>Overall Life Reading</h4>
                    <p className="text-sm leading-relaxed" style={{ color: '#e8e0d4' }}>{iogitaData.iogita_insight}</p>
                  </div>
                )}

                {/* Normal Astrology Insights */}
                {iogitaData.normal_astrology && iogitaData.normal_astrology.length > 0 && (
                  <div className="rounded-xl p-5 border border-sacred-gold/20" style={{ background: 'rgba(34,34,58,0.8)' }}>
                    <h4 className="font-display font-semibold mb-3" style={{ color: '#D4A052' }}>Kundli Summary</h4>
                    <div className="space-y-2">
                      {iogitaData.normal_astrology.map((point: string, idx: number) => (
                        <div key={idx} className="flex gap-2 text-sm" style={{ color: '#e8e0d4' }}>
                          <span style={{ color: '#D4A052' }}>•</span>
                          <span className="leading-relaxed">{point}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : iogitaData ? (
              <p className="text-center py-8" style={{ color: '#b8b0a4' }}>Analysis returned partial data. Try again.</p>
            ) : (
              <p className="text-center py-8" style={{ color: '#b8b0a4' }}>Click the io-gita tab to run your life pattern analysis</p>
            )}
          </TabsContent>

          {/* DASHA TAB — Extended with Mahadasha -> Antardasha -> Pratyantar */}
          <TabsContent value="dasha">
            {(loadingDasha || loadingExtendedDasha) ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Calculating Vimshottari Dasha...</span></div>
            ) : extendedDashaData ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20">
                  <p className="text-sm text-sacred-text-secondary">Current Mahadasha</p>
                  <p className="text-xl font-display font-bold" style={{ color: '#B8860B' }}>{extendedDashaData.current_dasha} Mahadasha</p>
                  <div className="flex gap-4 mt-1">
                    {extendedDashaData.current_antardasha && extendedDashaData.current_antardasha !== 'Unknown' && (
                      <p className="text-sm text-sacred-gold-dark">Antardasha: {extendedDashaData.current_antardasha}</p>
                    )}
                    {extendedDashaData.current_pratyantar && extendedDashaData.current_pratyantar !== 'Unknown' && (
                      <p className="text-sm text-sacred-text-secondary">Pratyantar: {extendedDashaData.current_pratyantar}</p>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  {(extendedDashaData.mahadasha || []).map((md: any) => (
                    <div key={md.planet} className={`rounded-xl border overflow-hidden ${md.is_current ? 'border-[#B8860B]/50' : 'border-sacred-gold/20'}`}>
                      <button
                        onClick={() => setExpandedMahadasha(expandedMahadasha === md.planet ? null : md.planet)}
                        className={`w-full flex items-center justify-between p-4 transition-colors ${md.is_current ? 'bg-[#B8860B]/10' : 'bg-sacred-cream hover:bg-sacred-gold/5'}`}
                      >
                        <div className="flex items-center gap-3">
                          <ChevronDown className={`w-4 h-4 text-sacred-gold-dark transition-transform ${expandedMahadasha === md.planet ? 'rotate-180' : ''}`} />
                          <span className={`font-display font-semibold ${md.is_current ? 'text-[#B8860B]' : 'text-sacred-brown'}`}>
                            {md.planet} Mahadasha
                          </span>
                          {md.is_current && <span className="text-xs px-2 py-0.5 rounded-full bg-[#B8860B]/20 text-[#B8860B] font-medium">Current</span>}
                        </div>
                        <div className="text-right text-sm text-sacred-text-secondary">
                          <span>{md.start} \u2014 {md.end}</span>
                          <span className="ml-2 text-sacred-gold-dark">({md.years}y)</span>
                        </div>
                      </button>

                      {expandedMahadasha === md.planet && (
                        <div className="border-t border-sacred-gold/20">
                          {(md.antardasha || []).map((ad: any) => (
                            <div key={`${md.planet}-${ad.planet}`}>
                              <button
                                onClick={() => setExpandedAntardasha(expandedAntardasha === `${md.planet}-${ad.planet}` ? null : `${md.planet}-${ad.planet}`)}
                                className={`w-full flex items-center justify-between px-6 py-3 text-sm transition-colors ${ad.is_current ? 'bg-[#B8860B]/5' : 'hover:bg-sacred-gold/5'}`}
                              >
                                <div className="flex items-center gap-2">
                                  {ad.pratyantar && ad.pratyantar.length > 0 && (
                                    <ChevronDown className={`w-3 h-3 text-sacred-gold-dark transition-transform ${expandedAntardasha === `${md.planet}-${ad.planet}` ? 'rotate-180' : ''}`} />
                                  )}
                                  <span className={`font-medium ${ad.is_current ? 'text-[#B8860B]' : 'text-sacred-brown'}`}>
                                    {ad.planet} Antardasha
                                  </span>
                                  {ad.is_current && <span className="text-xs px-1.5 py-0.5 rounded-full bg-[#B8860B]/15 text-[#B8860B]">Current</span>}
                                </div>
                                <span className="text-sacred-text-secondary">{ad.start} \u2014 {ad.end}</span>
                              </button>

                              {expandedAntardasha === `${md.planet}-${ad.planet}` && ad.pratyantar && ad.pratyantar.length > 0 && (
                                <div className="bg-sacred-cream/50 border-t border-sacred-gold/10">
                                  {ad.pratyantar.map((pt: any, idx: number) => (
                                    <div
                                      key={idx}
                                      className={`flex items-center justify-between px-10 py-2 text-xs ${pt.is_current ? 'bg-[#B8860B]/5' : ''}`}
                                    >
                                      <span className={`${pt.is_current ? 'text-[#B8860B] font-semibold' : 'text-sacred-text-secondary'}`}>
                                        {pt.planet} Pratyantar
                                        {pt.is_current && <span className="ml-1 text-[#B8860B]">*</span>}
                                      </span>
                                      <span className="text-sacred-text-secondary">{pt.start} \u2014 {pt.end}</span>
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ) : dashaData ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20">
                  <p className="text-sm text-sacred-text-secondary">Current Mahadasha</p>
                  <p className="text-xl font-display font-bold text-sacred-brown">{dashaData.current_dasha} Mahadasha</p>
                  {dashaData.current_antardasha && <p className="text-sm text-sacred-gold-dark">Antardasha: {dashaData.current_antardasha}</p>}
                </div>
                <div className="rounded-xl border border-sacred-gold/20 overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-sacred-cream">
                      <tr>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Planet</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Start</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">End</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Years</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(dashaData.mahadasha_periods || []).map((p: any) => (
                        <tr key={p.planet} className={`border-t border-sacred-gold/20 ${p.planet === dashaData.current_dasha ? 'bg-sacred-gold/10 font-semibold' : ''}`}>
                          <td className="p-3 text-sacred-brown">{p.planet} {p.planet === dashaData.current_dasha ? '\u2190' : ''}</td>
                          <td className="p-3 text-sacred-text-secondary text-sm">{p.start_date}</td>
                          <td className="p-3 text-sacred-text-secondary text-sm">{p.end_date}</td>
                          <td className="p-3 text-sacred-text-secondary text-sm">{p.years}y</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Dasha tab to calculate periods</p>
            )}
          </TabsContent>

          {/* DIVISIONAL CHARTS TAB */}
          <TabsContent value="divisional">
            <div className="space-y-6">
              <div className="flex items-center gap-4 mb-4">
                <label className="text-sm font-medium text-sacred-brown">Select Chart Type:</label>
                <select
                  value={selectedDivision}
                  onChange={(e) => {
                    setSelectedDivision(e.target.value);
                    setDivisionalData(null);
                    fetchDivisional(e.target.value);
                  }}
                  className="bg-sacred-cream border border-sacred-gold/30 rounded-lg px-3 py-2 text-sacred-brown text-sm focus:border-sacred-gold focus:outline-none"
                >
                  {DIVISIONAL_CHART_OPTIONS.map((c) => (
                    <option key={c.code} value={c.code}>{c.name}</option>
                  ))}
                </select>
              </div>

              {loadingDivisional ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                  <span className="ml-2 text-sacred-text-secondary">Calculating divisional chart...</span>
                </div>
              ) : divisionalData ? (
                <div className="space-y-6">
                  <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20">
                    <h4 className="font-display font-bold text-sacred-brown text-lg">{divisionalData.chart_name || divisionalData.chart_type}</h4>
                    <p className="text-sm text-sacred-text-secondary">Division: {divisionalData.division}</p>
                  </div>

                  {divisionalData.planet_positions && (
                    <div className="flex justify-center">
                      <InteractiveKundli
                        chartData={{
                          planets: divisionalData.planet_positions.map((p: any) => ({
                            planet: p.planet,
                            sign: p.sign,
                            house: p.house,
                            nakshatra: p.nakshatra || '',
                            sign_degree: p.sign_degree || 0,
                            status: '',
                          })),
                          houses: Array.from({ length: 12 }, (_, i) => ({
                            number: i + 1,
                            sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
                          })),
                        } as ChartData}
                        onPlanetClick={handlePlanetClick}
                        onHouseClick={handleHouseClick}
                      />
                    </div>
                  )}

                  <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
                    <table className="w-full">
                      <thead className="bg-sacred-cream">
                        <tr>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Planet</th>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Sign</th>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Degree</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(divisionalData.planet_signs || {}).map(([planet, sign]: [string, any]) => {
                          const posData = (divisionalData.planet_positions || []).find((p: any) => p.planet === planet);
                          return (
                            <tr key={planet} className="border-t border-sacred-gold/20 hover:bg-sacred-gold/5">
                              <td className="p-3 text-sacred-brown font-medium text-sm">{planet}</td>
                              <td className="p-3 text-sacred-text-secondary text-sm">{sign as string}</td>
                              <td className="p-3 text-sacred-text-secondary text-sm">{posData?.sign_degree?.toFixed(1) || '--'}&deg;</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">Select a chart type and click the tab to load</p>
              )}
            </div>
          </TabsContent>

          {/* ASHTAKVARGA TAB */}
          <TabsContent value="ashtakvarga">
            {loadingAshtakvarga ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">Calculating Ashtakvarga...</span>
              </div>
            ) : ashtakvargaData ? (
              <div className="space-y-6">
                {/* SAV Chart — Visual Kundli with points in each house */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Sarvashtakvarga Chart</h4>
                  <div className="w-full max-w-[600px] mx-auto">
                    <InteractiveKundli
                      chartData={{
                        planets: (() => {
                          const signNames = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
                          return signNames.map((sign, i) => ({
                            planet: `${ashtakvargaData.sarvashtakvarga?.[sign] || 0}`,
                            sign,
                            house: i + 1,
                            nakshatra: 'SAV',
                            sign_degree: 15,
                            status: (ashtakvargaData.sarvashtakvarga?.[sign] || 0) >= 28 ? 'Strong' : 'Weak',
                          }));
                        })(),
                        houses: result?.chart_data?.houses,
                      }}
                      onPlanetClick={() => {}}
                      onHouseClick={() => {}}
                    />
                  </div>
                  <p className="text-xs text-center text-sacred-text-secondary mt-2">Numbers show SAV points per sign (28+ = strong)</p>
                </div>

                {/* SAV Bar Chart */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Sarvashtakvarga</h4>
                  <div className="flex items-end gap-2 h-48">
                    {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map((sign) => {
                      const points = ashtakvargaData.sarvashtakvarga?.[sign] || 0;
                      const maxPoints = 56;
                      const heightPct = Math.round((points / maxPoints) * 100);
                      const isStrong = points >= 28;
                      return (
                        <div key={sign} className="flex-1 flex flex-col items-center gap-1">
                          <span className="text-xs font-medium text-sacred-brown">{points}</span>
                          <div className="w-full bg-sacred-gold/10 rounded-t-md relative" style={{ height: '140px' }}>
                            <div
                              className="absolute bottom-0 w-full rounded-t-md transition-all"
                              style={{
                                height: `${heightPct}%`,
                                backgroundColor: isStrong ? '#B8860B' : '#b8b0a4',
                              }}
                            />
                          </div>
                          <span className="text-[10px] text-sacred-text-secondary truncate w-full text-center" title={sign}>
                            {sign.slice(0, 3)}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center gap-4 mt-3 text-xs text-sacred-text-secondary">
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#B8860B' }} />
                      <span>Strong (&ge;28)</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#b8b0a4' }} />
                      <span>Weak (&lt;28)</span>
                    </div>
                  </div>
                </div>

                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Bhinnashtakvarga</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-sacred-gold/20">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Planet</th>
                          {['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'].map((s) => (
                            <th key={s} className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{s}</th>
                          ))}
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Total</th>
                        </tr>
                      </thead>
                      <tbody>
                        {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                          const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                          const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
                          const total = signs.reduce((sum, s) => sum + (bindus[s] || 0), 0);
                          return (
                            <tr key={planet} className="border-t border-sacred-gold/10 hover:bg-sacred-gold/5">
                              <td className="p-2 text-sacred-brown font-medium">{planet}</td>
                              {signs.map((s) => {
                                const val = bindus[s] || 0;
                                return (
                                  <td key={s} className="text-center p-2">
                                    <span className={`inline-block w-6 h-6 rounded text-xs leading-6 ${val >= 5 ? 'bg-[#B8860B]/20 text-[#B8860B] font-bold' : val <= 2 ? 'bg-[#8B2332]/10 text-[#8B2332]' : 'text-sacred-text-secondary'}`}>
                                      {val}
                                    </span>
                                  </td>
                                );
                              })}
                              <td className="text-center p-2 font-semibold text-sacred-brown">{total}</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Ashtakvarga tab to calculate</p>
            )}
          </TabsContent>

          {/* SHADBALA TAB */}
          <TabsContent value="shadbala">
            {loadingShadbala ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">Calculating Shadbala...</span>
              </div>
            ) : shadbalaData?.planets ? (
              <div className="space-y-6">
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Shadbala Strength</h4>
                  <div className="space-y-3">
                    {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                      const data = shadbalaData.planets[planet];
                      if (!data) return null;
                      const pct = Math.min((data.total / data.required) * 100, 150);
                      const barColor = data.is_strong ? '#B8860B' : '#8B2332';
                      return (
                        <div key={planet} className="flex items-center gap-3">
                          <span className="w-16 text-sm font-medium text-sacred-brown">{planet}</span>
                          <div className="flex-1 relative">
                            <div className="bg-sacred-gold/10 rounded-full h-5 overflow-hidden">
                              <div
                                className="h-full rounded-full transition-all"
                                style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }}
                              />
                            </div>
                            <div
                              className="absolute top-0 h-5 border-r-2 border-dashed border-sacred-brown/40"
                              style={{ left: `${Math.min((data.required / (data.required * 1.5)) * 100, 100)}%` }}
                              title={`Required: ${data.required}`}
                            />
                          </div>
                          <span className={`text-sm w-20 text-right font-medium ${data.is_strong ? 'text-[#B8860B]' : 'text-[#8B2332]'}`}>
                            {data.total} / {data.required}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center gap-4 mt-3 text-xs text-sacred-text-secondary">
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#B8860B' }} />
                      <span>Strong</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#8B2332' }} />
                      <span>Weak</span>
                    </div>
                  </div>
                </div>

                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Detailed Breakdown</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-sacred-gold/20">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Planet</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Sthana</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Dig</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Kala</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Cheshta</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Naisargika</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Drik</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Total</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Ratio</th>
                        </tr>
                      </thead>
                      <tbody>
                        {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                          const d = shadbalaData.planets[planet];
                          if (!d) return null;
                          return (
                            <tr key={planet} className={`border-t border-sacred-gold/10 ${d.is_strong ? '' : 'bg-[#8B2332]/5'}`}>
                              <td className="p-2 text-sacred-brown font-medium">{planet}</td>
                              <td className="text-center p-2 text-sacred-text-secondary">{d.sthana}</td>
                              <td className="text-center p-2 text-sacred-text-secondary">{d.dig}</td>
                              <td className="text-center p-2 text-sacred-text-secondary">{d.kala}</td>
                              <td className="text-center p-2 text-sacred-text-secondary">{d.cheshta}</td>
                              <td className="text-center p-2 text-sacred-text-secondary">{d.naisargika}</td>
                              <td className="text-center p-2 text-sacred-text-secondary">{d.drik}</td>
                              <td className={`text-center p-2 font-semibold ${d.is_strong ? 'text-[#B8860B]' : 'text-[#8B2332]'}`}>{d.total}</td>
                              <td className={`text-center p-2 font-medium ${d.ratio >= 1 ? 'text-[#B8860B]' : 'text-[#8B2332]'}`}>{d.ratio}x</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Shadbala tab to calculate</p>
            )}
          </TabsContent>

          {/* AVAKHADA CHAKRA TAB */}
          <TabsContent value="avakhada">
            {loadingAvakhada ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">Calculating Avakhada Chakra...</span>
              </div>
            ) : avakhadaData ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20 mb-4">
                  <h4 className="font-display font-bold text-lg" style={{ color: '#e8e0d4' }}>Avakhada Chakra</h4>
                  <p className="text-sm text-sacred-text-secondary">Comprehensive Birth Summary</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[
                    { label: 'Ascendant (Lagna)', value: avakhadaData.ascendant },
                    { label: 'Lagna Lord', value: avakhadaData.ascendant_lord },
                    { label: 'Rashi (Moon Sign)', value: avakhadaData.rashi },
                    { label: 'Rashi Lord', value: avakhadaData.rashi_lord },
                    { label: 'Nakshatra', value: `${avakhadaData.nakshatra} (Pada ${avakhadaData.nakshatra_pada})` },
                    { label: 'Yoga', value: avakhadaData.yoga },
                    { label: 'Karana', value: avakhadaData.karana },
                    { label: 'Yoni', value: avakhadaData.yoni },
                    { label: 'Gana', value: avakhadaData.gana },
                    { label: 'Nadi', value: avakhadaData.nadi },
                    { label: 'Varna', value: avakhadaData.varna },
                    { label: 'Naamakshar', value: avakhadaData.naamakshar },
                    { label: 'Sun Sign (Western)', value: avakhadaData.sun_sign },
                  ].map((item) => (
                    <div
                      key={item.label}
                      className="rounded-xl p-4 border"
                      style={{ backgroundColor: '#1a1a2e', borderColor: 'rgba(184,134,11,0.2)' }}
                    >
                      <p className="text-xs font-medium mb-1" style={{ color: '#b8b0a4' }}>{item.label}</p>
                      <p className="font-display font-semibold text-base" style={{ color: '#e8e0d4' }}>{item.value}</p>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Avakhada tab to load birth summary</p>
            )}
          </TabsContent>

          {/* YOGA & DOSHA TAB */}
          <TabsContent value="yoga-dosha">
            {loadingYogaDosha ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">Analyzing Yogas and Doshas...</span>
              </div>
            ) : yogaDoshaData ? (
              <div className="space-y-8">
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <CheckCircle className="w-5 h-5" style={{ color: '#22c55e' }} />
                    <h4 className="font-display font-bold text-lg" style={{ color: '#e8e0d4' }}>Yogas (Positive Combinations)</h4>
                  </div>
                  <div className="grid gap-3">
                    {(yogaDoshaData.yogas || []).filter((y: any) => y.present).length === 0 && (
                      <p className="text-sm text-sacred-text-secondary py-4">No significant yogas detected in this chart.</p>
                    )}
                    {(yogaDoshaData.yogas || []).filter((y: any) => y.present).map((yoga: any, idx: number) => (
                      <div
                        key={idx}
                        className="rounded-xl p-4 border border-green-500/30"
                        style={{ backgroundColor: 'rgba(34,197,94,0.05)' }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-display font-semibold" style={{ color: '#e8e0d4' }}>{yoga.name}</h5>
                          <span className="text-xs px-2 py-1 rounded-full font-medium bg-green-500/20 text-green-400">
                            Present
                          </span>
                        </div>
                        <p className="text-sm" style={{ color: '#b8b0a4' }}>{yoga.description}</p>
                        {yoga.planets_involved && yoga.planets_involved.length > 0 && (
                          <div className="mt-2 flex gap-2">
                            {yoga.planets_involved.map((p: string) => (
                              <span key={p} className="text-xs px-2 py-0.5 rounded-full bg-green-500/10 text-green-400">{p}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <Shield className="w-5 h-5" style={{ color: '#8B2332' }} />
                    <h4 className="font-display font-bold text-lg" style={{ color: '#e8e0d4' }}>Doshas (Afflictions)</h4>
                  </div>
                  <div className="grid gap-3">
                    {(yogaDoshaData.doshas || []).filter((d: any) => d.present).length === 0 && (
                      <p className="text-sm py-4" style={{ color: '#22c55e' }}>No doshas detected — chart is free from major afflictions.</p>
                    )}
                    {(yogaDoshaData.doshas || []).filter((d: any) => d.present).map((dosha: any, idx: number) => (
                      <div
                        key={idx}
                        className={`rounded-xl p-4 border ${dosha.severity === 'high' ? 'border-red-500/40' : 'border-amber-400/40'}`}
                        style={{ backgroundColor: dosha.severity === 'high' ? 'rgba(139,35,50,0.05)' : 'rgba(245,158,11,0.05)' }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-display font-semibold" style={{ color: '#e8e0d4' }}>{dosha.name}</h5>
                          <div className="flex items-center gap-2">
                            {dosha.severity !== 'none' && (
                              <span className={`text-xs px-2 py-0.5 rounded-full ${dosha.severity === 'high' ? 'bg-red-500/20 text-red-400' : dosha.severity === 'medium' ? 'bg-amber-400/20 text-amber-600' : 'bg-yellow-200 text-yellow-700'}`}>
                                {dosha.severity}
                              </span>
                            )}
                            <span className="text-xs px-2 py-1 rounded-full font-medium bg-red-500/20 text-red-400">
                              Present
                            </span>
                          </div>
                        </div>
                        <p className="text-sm" style={{ color: '#b8b0a4' }}>{dosha.description}</p>
                        {dosha.remedies && dosha.remedies.length > 0 && (
                          <div className="mt-3 pt-3 border-t" style={{ borderColor: 'rgba(139,115,85,0.15)' }}>
                            <p className="text-xs font-semibold mb-2" style={{ color: '#B8860B' }}>
                              <AlertTriangle className="w-3 h-3 inline mr-1" />Remedies:
                            </p>
                            <ul className="space-y-1">
                              {dosha.remedies.map((r: string, ri: number) => (
                                <li key={ri} className="text-xs flex items-start gap-2" style={{ color: '#b8b0a4' }}>
                                  <span className="mt-1 w-1 h-1 rounded-full flex-shrink-0" style={{ backgroundColor: '#B8860B' }} />
                                  {r}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Yogas tab to analyze positive and negative combinations</p>
            )}
          </TabsContent>

          {/* PREDICTIONS TAB -- delegated to PredictionsTab */}
          <TabsContent value="predictions">
            <PredictionsTab
              predictionsData={predictionsData}
              loadingPredictions={loadingPredictions}
              activePeriod={activePredictionPeriod}
              onFetchPredictions={fetchPredictions}
            />
          </TabsContent>

          {/* TRANSITS (GOCHARA) TAB */}
          <TabsContent value="transits">
            {loadingTransit ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">Loading transits...</span>
              </div>
            ) : transitData ? (
              <div className="space-y-6">
                {/* Transit Chart — Current planet positions on Kundli */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Current Transit Chart ({transitData.transit_date})</h4>
                  <div className="w-full max-w-[600px] mx-auto">
                    <InteractiveKundli
                      chartData={{
                        planets: (transitData.transits || []).map((tr: any) => ({
                          planet: tr.planet,
                          sign: tr.current_sign,
                          house: tr.house || 1,
                          nakshatra: tr.nakshatra || '',
                          sign_degree: tr.sign_degree || 0,
                          status: tr.is_retrograde ? 'Retrograde' : (tr.effect === 'favorable' ? 'Benefic' : 'Malefic'),
                        })),
                        houses: transitData.chart_data?.houses || result?.chart_data?.houses,
                      }}
                      onPlanetClick={() => {}}
                      onHouseClick={() => {}}
                    />
                  </div>
                  <div className="flex items-center justify-center gap-4 mt-2 text-xs text-sacred-text-secondary">
                    <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: '#B8860B'}} /> Benefic Transit</span>
                    <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: '#8B2332'}} /> Malefic Transit</span>
                  </div>
                </div>

                {/* Header with date and Moon sign */}
                <div className="rounded-xl p-4 border" style={{ backgroundColor: 'rgba(184,134,11,0.04)', borderColor: 'rgba(184,134,11,0.25)' }}>
                  <h4 className="font-display font-bold text-lg mb-2" style={{ color: '#e8e0d4' }}>Gochara (Transits)</h4>
                  <p className="text-sm mb-3" style={{ color: '#b8b0a4' }}>Current planetary positions and their effects on your birth chart</p>
                  <div className="flex flex-wrap gap-4 text-sm">
                    <span style={{ color: '#e8e0d4' }}><strong>Transit Date:</strong> {transitData.transit_date}</span>
                    <span style={{ color: '#e8e0d4' }}><strong>Natal Moon:</strong> {transitData.natal_moon_sign}</span>
                  </div>
                </div>

                {/* Sade Sati Status */}
                <div
                  className={`rounded-xl p-4 border ${transitData.sade_sati?.active ? 'border-red-500/40' : 'border-green-500/30'}`}
                  style={{ backgroundColor: transitData.sade_sati?.active ? 'rgba(139,35,50,0.05)' : 'rgba(34,197,94,0.05)' }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h5 className="font-display font-semibold" style={{ color: '#e8e0d4' }}>
                      <Shield className="w-4 h-4 inline mr-2" />
                      Sade Sati
                    </h5>
                    <span className={`text-xs px-2 py-1 rounded-full font-medium ${transitData.sade_sati?.active ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                      {transitData.sade_sati?.active ? 'Active' : 'Not Active'}
                    </span>
                  </div>
                  {transitData.sade_sati?.active && (
                    <p className="text-xs mb-1" style={{ color: '#B8860B' }}>
                      <strong>Phase:</strong> {transitData.sade_sati.phase}
                    </p>
                  )}
                  <p className="text-sm" style={{ color: '#b8b0a4' }}>{transitData.sade_sati?.description}</p>
                </div>

                {/* Transit Table */}
                <div className="rounded-xl border overflow-hidden" style={{ borderColor: 'rgba(184,134,11,0.25)' }}>
                  <table className="w-full text-sm">
                    <thead>
                      <tr style={{ backgroundColor: 'rgba(184,134,11,0.08)' }}>
                        <th className="text-left p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>Planet</th>
                        <th className="text-left p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>Current Sign</th>
                        <th className="text-center p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>House from Moon</th>
                        <th className="text-center p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>Effect</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(transitData.transits || []).map((tr: any, idx: number) => (
                        <tr
                          key={idx}
                          className="border-t"
                          style={{ borderColor: 'rgba(184,134,11,0.15)', backgroundColor: idx % 2 === 0 ? 'transparent' : 'rgba(184,134,11,0.02)' }}
                        >
                          <td className="p-3 font-medium" style={{ color: '#e8e0d4' }}>{tr.planet}</td>
                          <td className="p-3" style={{ color: '#b8b0a4' }}>{tr.current_sign}</td>
                          <td className="p-3 text-center" style={{ color: '#b8b0a4' }}>{tr.natal_house_from_moon}</td>
                          <td className="p-3 text-center">
                            <span className={`inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full font-medium ${tr.effect === 'favorable' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                              {tr.effect === 'favorable' ? <CheckCircle className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
                              {tr.effect === 'favorable' ? 'Favorable' : 'Unfavorable'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Detailed descriptions */}
                <div className="grid gap-3">
                  {(transitData.transits || []).map((tr: any, idx: number) => (
                    <div
                      key={idx}
                      className={`rounded-xl p-4 border ${tr.effect === 'favorable' ? 'border-green-500/30' : 'border-red-500/30'}`}
                      style={{ backgroundColor: tr.effect === 'favorable' ? 'rgba(34,197,94,0.03)' : 'rgba(239,68,68,0.03)' }}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-display font-semibold" style={{ color: '#e8e0d4' }}>{tr.planet}</span>
                        <span className="text-xs" style={{ color: '#b8b0a4' }}>in {tr.current_sign}</span>
                        <span className={`text-xs px-1.5 py-0.5 rounded-full ${tr.effect === 'favorable' ? 'bg-green-500/15 text-green-400' : 'bg-red-500/15 text-red-400'}`}>
                          {tr.effect === 'favorable' ? 'Favorable' : 'Unfavorable'}
                        </span>
                      </div>
                      <p className="text-sm" style={{ color: '#b8b0a4' }}>{tr.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Transits tab to see current Gochara effects</p>
            )}
          </TabsContent>

          {/* VARSHPHAL TAB */}
          <TabsContent value="varshphal">
            <div className="space-y-6">
              {/* Year selector */}
              <div className="flex items-center gap-4 mb-4">
                <label className="text-sm font-medium text-sacred-brown">Select Year:</label>
                <select
                  value={varshphalYear}
                  onChange={(e) => {
                    const yr = Number(e.target.value);
                    setVarshphalYear(yr);
                    setVarshphalData(null);
                    fetchVarshphal(yr);
                  }}
                  className="bg-sacred-cream border border-sacred-gold/30 rounded-lg px-3 py-2 text-sacred-brown text-sm focus:border-sacred-gold focus:outline-none"
                >
                  {Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - 10 + i).map((yr) => (
                    <option key={yr} value={yr}>{yr}</option>
                  ))}
                </select>
              </div>

              {loadingVarshphal ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Calculating Varshphal...</span></div>
              ) : varshphalData ? (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Solar Return Info */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">Varsha Pravesh (Solar Return)</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Solar Return Date</p>
                        <p className="font-semibold text-sacred-brown">{varshphalData.solar_return?.date}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Solar Return Time</p>
                        <p className="font-semibold text-sacred-brown">{varshphalData.solar_return?.time}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Year Lord (Varsheshwar)</p>
                        <p className="font-semibold" style={{ color: '#B8860B' }}>{varshphalData.year_lord}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Completed Years</p>
                        <p className="font-semibold text-sacred-brown">{varshphalData.completed_years}</p>
                      </div>
                    </div>
                  </div>

                  {/* Muntha */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">Muntha</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Muntha Sign</p>
                        <p className="font-semibold text-sacred-brown">{varshphalData.muntha?.sign}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Muntha House</p>
                        <p className="font-semibold text-sacred-brown">House {varshphalData.muntha?.house}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Muntha Lord</p>
                        <p className="font-semibold" style={{ color: '#B8860B' }}>{varshphalData.muntha?.lord}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">Status</p>
                        <p className={`font-semibold ${varshphalData.muntha?.favorable ? 'text-green-400' : 'text-red-500'}`}>
                          {varshphalData.muntha?.favorable ? 'Favorable' : 'Challenging'}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Varshphal Chart */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">Varshphal Chart ({varshphalYear})</h4>
                    {varshphalData.chart_data?.planets ? (
                      <div className="flex justify-center">
                        <InteractiveKundli
                          chartData={{
                            planets: Object.entries(varshphalData.chart_data.planets).map(([name, data]: [string, any]) => ({
                              planet: name, sign: data?.sign || '', house: data?.house || 1,
                              nakshatra: data?.nakshatra || '', sign_degree: data?.sign_degree || 0,
                              status: data?.status || '', is_retrograde: data?.retrograde || false,
                            })),
                            houses: varshphalData.chart_data.houses,
                            ascendant: varshphalData.chart_data.ascendant,
                          } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={handleHouseClick}
                        />
                      </div>
                    ) : <p className="text-center text-sacred-text-secondary py-4 text-sm">No chart data</p>}
                  </div>

                  {/* Mudda Dasha */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">
                      Mudda Dasha
                      {varshphalData.current_mudda_dasha && (
                        <span className="ml-2 text-xs px-2 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold-dark">
                          Current: {varshphalData.current_mudda_dasha}
                        </span>
                      )}
                    </h4>
                    <table className="w-full text-xs">
                      <thead><tr className="bg-sacred-gold/10">
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">Planet</th>
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">Start</th>
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">End</th>
                        <th className="text-center p-2 text-sacred-gold-dark font-medium">Days</th>
                      </tr></thead>
                      <tbody>
                        {(varshphalData.mudda_dasha || []).map((md: any) => (
                          <tr key={md.planet} className={`border-t border-sacred-gold/10 ${md.planet === varshphalData.current_mudda_dasha ? 'bg-sacred-gold/10 font-semibold' : ''}`}>
                            <td className="p-2 text-sacred-brown">{md.planet}{md.planet === varshphalData.current_mudda_dasha ? ' \u2190' : ''}</td>
                            <td className="p-2 text-sacred-text-secondary">{md.start_date}</td>
                            <td className="p-2 text-sacred-text-secondary">{md.end_date}</td>
                            <td className="p-2 text-center text-sacred-text-secondary">{md.days}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">Select a year and click the Varshphal tab to calculate</p>
              )}
            </div>
          </TabsContent>
        </Tabs>

        <div className="mt-8 mb-16 text-center">
          <Button onClick={() => { setStep('form'); setResult(null); resetTabData(); }} variant="outline" className="border-cosmic-text-muted text-cosmic-text">
            Generate Another Kundli
          </Button>
        </div>

        {/* Summary Modal - Clean Landscape View */}
        <KundliSummaryModal
          isOpen={summaryOpen}
          onClose={() => setSummaryOpen(false)}
          data={{
            name: formData.name,
            date: formData.date,
            time: formData.time,
            place: formData.place,
            latitude: formData.latitude.toString(),
            longitude: formData.longitude.toString(),
            timezone: 'IST'
          }}
          onViewFullReport={() => {
            setSummaryOpen(false);
            // Scroll to top or show full report tabs
          }}
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
