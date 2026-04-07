import { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, ChevronDown, Download, Share2, FileText, Heart, Briefcase, Activity, ArrowLeft, Loader2, X, CheckCircle, AlertTriangle, Shield, Printer, ScrollText, Gem } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import { isPuterAvailable, puterChatStream, VEDIC_SYSTEM_PROMPT } from '@/lib/puter-ai';
import { translateBackend, translatePlanet, translateSign, translateName, translateRemedy, translateLabel } from '@/lib/backend-translations';
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
  const { t, language } = useTranslation();
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
  const [transitHouseShift, setTransitHouseShift] = useState(0);
  const [reportLagnaShift, setReportLagnaShift] = useState(0);
  const [reportMoonShift, setReportMoonShift] = useState(0);
  const [reportGocharShift, setReportGocharShift] = useState(0);
  const [transitDate, setTransitDate] = useState('');
  const [transitTime, setTransitTime] = useState('');
  const [d10Data, setD10Data] = useState<any>(null);
  const [loadingD10, setLoadingD10] = useState(false);
  const [varshphalData, setVarshphalData] = useState<any>(null);
  const [loadingVarshphal, setLoadingVarshphal] = useState(false);
  const [varshphalYear, setVarshphalYear] = useState(() => {
    // Default to current active Varshphal year: if birthday hasn't passed yet, use previous year
    const now = new Date();
    return now.getFullYear();
  });
  const [yoginiData, setYoginiData] = useState<any>(null);
  const [loadingYogini, setLoadingYogini] = useState(false);
  const [kpData, setKpData] = useState<any>(null);
  const [loadingKp, setLoadingKp] = useState(false);
  const [upagrahasData, setUpagrahasData] = useState<any>(null);
  const [loadingUpagrahas, setLoadingUpagrahas] = useState(false);
  const [sodashvargaData, setSodashvargaData] = useState<any>(null);
  const [loadingSodashvarga, setLoadingSodashvarga] = useState(false);
  const [aspectsData, setAspectsData] = useState<any>(null);
  const [loadingAspects, setLoadingAspects] = useState(false);
  const [sadesatiData, setSadesatiData] = useState<any>(null);
  const [loadingSadesati, setLoadingSadesati] = useState(false);
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
    setYoginiData(null);
    setKpData(null);
    setUpagrahasData(null);
    setSodashvargaData(null);
    setAspectsData(null);
    setSadesatiData(null);
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
      if (data?.mahadasha) {
        setExtendedDashaData(data);
      } else {
        console.warn('Extended dasha response missing mahadasha:', data);
      }
    } catch (err) {
      console.error('Failed to fetch extended dasha:', err);
    }
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

  // Fetch transits (Gochara) — supports custom date/time
  const fetchTransit = async (customDate?: string, customTime?: string) => {
    if (!result?.id) return;
    // Skip cache if custom date provided
    if (!customDate && transitData) return;
    setLoadingTransit(true);
    setTransitHouseShift(0); // reset house shift on new fetch
    try {
      const body: any = {};
      if (customDate) body.transit_date = customDate;
      if (customTime) body.transit_time = customTime;
      const data = await api.post(`/api/kundli/${result.id}/transits`, body);
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

  // Fetch Varshphal — default to the last solar return year (birthday-based)
  const fetchVarshphal = async (year?: number) => {
    if (!result?.id) return;
    let targetYear = year || varshphalYear;
    // Auto-detect: if birthday hasn't passed yet this year, use previous year
    if (!year && result?.birth_date) {
      const [, bm, bd] = result.birth_date.split('-').map(Number);
      const now = new Date();
      const thisYearBday = new Date(now.getFullYear(), bm - 1, bd);
      if (now < thisYearBday) {
        targetYear = now.getFullYear() - 1;
        setVarshphalYear(targetYear);
      }
    }
    setLoadingVarshphal(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/varshphal`, { year: targetYear });
      setVarshphalData(data);
    } catch { /* fallback */ }
    setLoadingVarshphal(false);
  };

  const fetchYogini = async () => {
    if (!result?.id) return;
    setLoadingYogini(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/yogini-dasha`);
      setYoginiData(data);
    } catch { /* */ }
    setLoadingYogini(false);
  };

  const fetchKp = async () => {
    if (!result?.id) return;
    setLoadingKp(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/kp-analysis`, {});
      setKpData(data);
    } catch { /* */ }
    setLoadingKp(false);
  };

  const fetchUpagrahas = async () => {
    if (!result?.id) return;
    setLoadingUpagrahas(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/upagrahas`);
      setUpagrahasData(data);
    } catch { /* */ }
    setLoadingUpagrahas(false);
  };

  const fetchSodashvarga = async () => {
    if (!result?.id) return;
    setLoadingSodashvarga(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/sodashvarga`);
      setSodashvargaData(data);
    } catch { /* */ }
    setLoadingSodashvarga(false);
  };

  const fetchAspects = async () => {
    if (!result?.id) return;
    setLoadingAspects(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/aspects`);
      setAspectsData(data);
    } catch { /* */ }
    setLoadingAspects(false);
  };

  const fetchSadesati = async () => {
    if (!result?.id) return;
    setLoadingSadesati(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/lifelong-sadesati`);
      setSadesatiData(data);
    } catch { /* */ }
    setLoadingSadesati(false);
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
      fetchYogini();
      fetchKp();
      fetchUpagrahas();
      fetchSodashvarga();
      fetchAspects();
      fetchSadesati();
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
        <h3 className="text-2xl font-sacred font-bold text-sacred-brown mb-2">{t('kundli.generatingYourKundli')}</h3>
        <p className="text-sacred-text-secondary">{t('kundli.analyzingPositions')}</p>
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
      gemstones: doshaData.gemstone_recommendations || [],
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
              <h3 className="font-display font-bold text-2xl text-sacred-brown">{result.person_name || formData.name} — {t('tab.kundli')}</h3>
              <p className="text-sm text-sacred-text-secondary">{result.birth_date || formData.date} | {result.birth_time || formData.time} | {result.birth_place || formData.place}</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="border-sacred-gold/50 text-sacred-brown">
              <Share2 className="w-4 h-4 mr-1" />{t('common.share')}
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
              <Download className="w-4 h-4 mr-1" />{t('common.download')}
            </Button>
          </div>
        </div>

        {/* Reports banner */}
        <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-2xl p-6 mb-8 border border-sacred-gold/20">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="font-display font-bold text-sacred-brown flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-sacred-gold" />{t('kundli.pdfReports')}
              </h4>
              <p className="text-sm text-sacred-text-secondary">{t('kundli.pdfSubtitle')}</p>
            </div>
            <Button variant="outline" className="border-sacred-gold text-sacred-gold-dark">{t('kundli.viewReports')}</Button>
          </div>
          <div className="grid grid-cols-4 gap-3">
            {[
              { icon: FileText, name: t('kundli.completeAnalysis'), price: '\u20b9999' },
              { icon: Heart, name: t('kundli.marriage'), price: '\u20b9799' },
              { icon: Briefcase, name: t('kundli.career'), price: '\u20b9799' },
              { icon: Activity, name: t('kundli.health'), price: '\u20b9699' },
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
            <TabsTrigger value="report" onClick={() => { fetchDasha(); fetchExtendedDasha(); fetchAvakhada(); fetchYogaDosha(); fetchAshtakvarga(); fetchShadbala(); fetchDivisional('D9'); }}><ScrollText className="w-3 h-3 mr-1" />{t('tab.report')}</TabsTrigger>
            <TabsTrigger value="planets">{t('tab.planets')}</TabsTrigger>
            <TabsTrigger value="details">{t('tab.details')}</TabsTrigger>
            <TabsTrigger value="lordships">{t('tab.lordships')}</TabsTrigger>
            <TabsTrigger value="dosha" onClick={fetchDosha}>{t('tab.dosha')}</TabsTrigger>
            <TabsTrigger value="iogita" onClick={fetchIogita}>{t('tab.iogita')}</TabsTrigger>
            <TabsTrigger value="dasha" onClick={() => { fetchDasha(); fetchExtendedDasha(); }}>{t('tab.dasha')}</TabsTrigger>
            <TabsTrigger value="divisional" onClick={() => fetchDivisional()}>{t('tab.divisional')}</TabsTrigger>
            <TabsTrigger value="ashtakvarga" onClick={fetchAshtakvarga}>{t('tab.ashtakvarga')}</TabsTrigger>
            <TabsTrigger value="shadbala" onClick={fetchShadbala}>{t('tab.shadbala')}</TabsTrigger>
            <TabsTrigger value="avakhada" onClick={fetchAvakhada}>{t('tab.avakhada')}</TabsTrigger>
            <TabsTrigger value="yoga-dosha" onClick={fetchYogaDosha}>{t('tab.yogas')}</TabsTrigger>
            <TabsTrigger value="predictions" onClick={() => fetchPredictions()}>{t('tab.predictions')}</TabsTrigger>
            <TabsTrigger value="transits" onClick={() => fetchTransit()}>{t('tab.transits')}</TabsTrigger>
            <TabsTrigger value="varshphal" onClick={() => fetchVarshphal()}>{t('tab.varshphal')}</TabsTrigger>
            <TabsTrigger value="kp" onClick={fetchKp}>{t('tab.kpSystem')}</TabsTrigger>
            <TabsTrigger value="yogini" onClick={fetchYogini}>{t('tab.yoginiDasha')}</TabsTrigger>
            <TabsTrigger value="upagrahas" onClick={fetchUpagrahas}>{t('tab.upagrahas')}</TabsTrigger>
            <TabsTrigger value="sodashvarga" onClick={fetchSodashvarga}>{t('tab.sodashvarga')}</TabsTrigger>
            <TabsTrigger value="aspects" onClick={fetchAspects}>{t('tab.aspects')}</TabsTrigger>
            <TabsTrigger value="sadesati" onClick={fetchSadesati}>{t('tab.sadeSati')}</TabsTrigger>
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
                  {t('kundli.jhoraView')}
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
                  {t('kundli.fullReport')}
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
                  <Download className="w-4 h-4 mr-1" />{t('common.downloadPDF')}
                </Button>
                <Button size="sm" variant="outline" className="border-sacred-gold/50 text-sacred-brown" onClick={() => window.print()}>
                  <Printer className="w-4 h-4 mr-1" />{t('common.printReport')}
                </Button>
              </div>

              {/* Report title */}
              <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-2xl p-5 border border-sacred-gold/20 text-center">
                <h3 className="font-display font-bold text-xl text-sacred-brown">{t('section.consolidatedReport')}</h3>
                <p className="text-sm text-sacred-text-secondary mt-1">{result.person_name} | {result.birth_date} | {result.birth_time} | {result.birth_place}</p>
              </div>

              {/* Charts row — Lagna, Moon, Gochar side by side */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 print:grid-cols-3">
                {/* 1. Lagna Chart (D1) — click house to rotate lagan */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">
                    {t('section.lagna')} <span className="text-xs font-normal opacity-50">({t('kundli.clickHouseToRotate')})</span>
                  </h4>
                  <div className="flex justify-center">
                    {(() => {
                      const shift = reportLagnaShift;
                      const basePlanets = planets;
                      const baseHouses = result.chart_data?.houses;
                      const shiftedPlanets = shift
                        ? basePlanets.map((p: PlanetData) => ({
                            ...p,
                            house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                          }))
                        : basePlanets;
                      const shiftedHouses = shift && baseHouses
                        ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                        : baseHouses;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: shiftedPlanets, houses: shiftedHouses, ascendant: result.chart_data?.ascendant } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            setReportLagnaShift(orig - 1 === 0 ? 0 : orig - 1);
                          }}
                          compact
                        />
                      );
                    })()}
                  </div>
                  {reportLagnaShift > 0 && (
                    <button onClick={() => setReportLagnaShift(0)} className="block mx-auto mt-1 text-xs text-sacred-gold underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 2. Moon Chart — click house to rotate lagan */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">
                    {t('section.moon')} <span className="text-xs font-normal opacity-50">({t('kundli.clickHouseToRotate')})</span>
                  </h4>
                  <div className="flex justify-center">
                    {(() => {
                      const moonPlanet = planets.find((p: PlanetData) => p.planet === 'Moon');
                      const moonHouse = moonPlanet?.house || 1;
                      const baseShift = moonHouse - 1;
                      const totalShift = baseShift + reportMoonShift;
                      const moonPlanets = planets.map((p: PlanetData) => ({
                        ...p,
                        house: ((((p.house || 1) - 1 - totalShift + 24) % 12) + 1),
                      }));
                      const moonHouses = result.chart_data?.houses
                        ? result.chart_data.houses.map((h: { number: number; sign: string }) => ({
                            number: ((h.number - 1 - totalShift + 24) % 12) + 1,
                            sign: h.sign,
                          }))
                        : undefined;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: moonPlanets, houses: moonHouses } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = totalShift ? ((house - 1 + totalShift) % 12) + 1 : house;
                            const newShift = ((orig - 1) - baseShift + 12) % 12;
                            setReportMoonShift(newShift);
                          }}
                          compact
                        />
                      );
                    })()}
                  </div>
                  {reportMoonShift > 0 && (
                    <button onClick={() => setReportMoonShift(0)} className="block mx-auto mt-1 text-xs text-sacred-gold underline">{t('common.resetView')}</button>
                  )}
                </div>

                {/* 3. Gochar (Transit) Chart — click house to rotate lagan */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-3">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center text-sm">
                    {t('section.gochar')} {transitData?.transit_date ? `(${transitData.transit_date})` : ''}
                    <span className="text-xs font-normal opacity-50"> ({t('kundli.clickHouseToRotate')})</span>
                  </h4>
                  <div className="flex justify-center">
                    {loadingTransit ? (
                      <div className="flex items-center justify-center py-12"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                    ) : transitData?.transits ? (() => {
                      const shift = reportGocharShift;
                      const transitPlanets = transitData.transits.map((tr: any) => ({
                        planet: tr.planet,
                        sign: tr.current_sign || tr.sign || '',
                        house: tr.house || 1,
                        nakshatra: tr.nakshatra || '',
                        sign_degree: tr.sign_degree || tr.degree || 0,
                        status: tr.is_retrograde ? 'Retrograde' : '',
                        is_retrograde: tr.is_retrograde,
                      }));
                      const baseHouses = transitData.chart_data?.houses || result.chart_data?.houses;
                      const shiftedPlanets = shift
                        ? transitPlanets.map((p: any) => ({
                            ...p,
                            house: ((((p.house || 1) - 1 - shift + 12) % 12) + 1),
                          }))
                        : transitPlanets;
                      const shiftedHouses = shift && baseHouses
                        ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                        : baseHouses;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: shiftedPlanets, houses: shiftedHouses } as ChartData}
                          onPlanetClick={handlePlanetClick}
                          onHouseClick={(house) => {
                            const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            setReportGocharShift(orig - 1 === 0 ? 0 : orig - 1);
                          }}
                          compact
                        />
                      );
                    })() : (
                      <p className="text-center text-sacred-text-secondary py-12 text-sm">{t('common.loading')}</p>
                    )}
                  </div>
                  {reportGocharShift > 0 && (
                    <button onClick={() => setReportGocharShift(0)} className="block mx-auto mt-1 text-xs text-sacred-gold underline">{t('common.resetView')}</button>
                  )}
                </div>
              </div>

              {/* Chart Legend */}
              <ChartLegend />

              {/* Grid layout — 2 columns on desktop, 1 on mobile */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 print:grid-cols-2">

                {/* 2. Planet Details Table */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.detailedPlanetPositions')}</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead className="bg-sacred-gold/10">
                        <tr>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.sign')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.house')}</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.nakshatra')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.degree')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.status')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {planets.map((planet: any, index: number) => (
                          <tr key={index} className="border-t border-sacred-gold/10 hover:bg-sacred-gold/5">
                            <td className="p-2 text-sacred-brown font-medium">{translatePlanet(planet.planet, language)}</td>
                            <td className="p-2 text-sacred-text-secondary">{translateSign(planet.sign, language)}</td>
                            <td className="p-2 text-center text-sacred-text-secondary">{planet.house}</td>
                            <td className="p-2 text-sacred-text-secondary">{planet.nakshatra || '\u2014'}</td>
                            <td className="p-2 text-center text-sacred-text-secondary">{planet.sign_degree?.toFixed(1)}&deg;</td>
                            <td className="p-2 text-center">
                              <span className={`text-xs px-1 py-0.5 rounded ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-500/20 text-green-400' : 'text-sacred-text-secondary'}`}>
                                {translateLabel(planet.status, language) || '\u2014'}
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
                    <h4 className="font-display font-semibold text-sacred-brown">{t('kundli.divisionalCharts')}</h4>
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
                    <p className="text-center text-sacred-text-secondary py-8 text-sm">{t('kundli.selectChart')}</p>
                  )}
                </div>

                {/* 4. Lordships */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.houseLordships')}</h4>
                  <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
                </div>

                {/* 5. Avakhada Chakra */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.avakhadaChakra')}</h4>
                  {loadingAvakhada ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : avakhadaData ? (
                    <div className="grid grid-cols-2 gap-2">
                      {[
                        { label: t('avakhada.ascendant'), value: avakhadaData.ascendant },
                        { label: t('avakhada.ascendantLord'), value: avakhadaData.ascendant_lord },
                        { label: t('avakhada.rashi'), value: avakhadaData.rashi },
                        { label: t('avakhada.rashiLord'), value: avakhadaData.rashi_lord },
                        { label: t('avakhada.nakshatra'), value: `${avakhadaData.nakshatra} (P${avakhadaData.nakshatra_pada})` },
                        { label: t('avakhada.yoga'), value: avakhadaData.yoga },
                        { label: t('avakhada.karana'), value: avakhadaData.karana },
                        { label: t('avakhada.yoni'), value: avakhadaData.yoni },
                        { label: t('avakhada.gana'), value: avakhadaData.gana },
                        { label: t('avakhada.nadi'), value: avakhadaData.nadi },
                        { label: t('avakhada.varna'), value: avakhadaData.varna },
                        { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
                        { label: t('avakhada.sunSign'), value: avakhadaData.sun_sign },
                      ].map((item) => (
                        <div key={item.label} className="rounded-lg p-2 bg-cosmic-card/60">
                          <p className="text-xs text-sacred-text-secondary">{item.label}</p>
                          <p className="text-xs font-semibold text-sacred-brown">{item.value}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 6. Vimshottari Dasha — with expandable AD/PD */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.vimshottariDasha')}</h4>
                  {(loadingDasha || loadingExtendedDasha) ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : (extendedDashaData || dashaData) ? (
                    <div className="space-y-2">
                      {/* Current dasha info */}
                      <div className="rounded-lg p-3" style={{ background: 'rgba(184,134,11,0.1)' }}>
                        <p className="text-xs" style={{ color: '#b8b0a4' }}>{t('section.currentMahadasha')}</p>
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
                                    {translatePlanet(md.planet, language)} {md.is_current ? '←' : ''}
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
                                          <span style={{ color: ad.is_current ? '#D4A052' : '#e8e0d4' }}>{translatePlanet(ad.planet, language)} AD {ad.is_current ? '*' : ''}</span>
                                        </span>
                                        <span style={{ color: '#b8b0a4', fontSize: '10px' }}>{ad.start?.slice(0,10)} — {ad.end?.slice(0,10)}</span>
                                      </button>

                                      {expandedAntardasha === `${md.planet}-${ad.planet}` && (ad.pratyantar || []).length > 0 && (
                                        <div className="border-t border-sacred-gold/5">
                                          {ad.pratyantar.map((pt: any, idx: number) => (
                                            <div key={idx} className="flex items-center justify-between px-8 py-1 text-xs"
                                              style={{ background: pt.is_current ? 'rgba(184,134,11,0.04)' : 'transparent' }}>
                                              <span style={{ color: pt.is_current ? '#D4A052' : '#b8b0a4' }}>
                                                {translatePlanet(pt.planet, language)} PD {pt.is_current ? '*' : ''}
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
                              <th className="text-left p-2 font-medium" style={{ color: '#D4A052' }}>{t('table.planet')}</th>
                              <th className="text-left p-2 font-medium" style={{ color: '#D4A052' }}>{t('table.start')}</th>
                              <th className="text-left p-2 font-medium" style={{ color: '#D4A052' }}>{t('table.end')}</th>
                              <th className="text-center p-2 font-medium" style={{ color: '#D4A052' }}>{t('table.years')}</th>
                            </tr></thead>
                            <tbody>
                              {(dashaData.mahadasha_periods || []).map((p: any) => (
                                <tr key={p.planet} className="border-t border-sacred-gold/10" style={{ background: p.planet === dashaData.current_dasha ? 'rgba(184,134,11,0.1)' : 'transparent' }}>
                                  <td className="p-2" style={{ color: '#e8e0d4' }}>{translatePlanet(p.planet, language)}{p.planet === dashaData.current_dasha ? ' ←' : ''}</td>
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
                    <p className="text-center py-4 text-sm" style={{ color: '#b8b0a4' }}>{t('common.loading')}</p>
                  )}
                </div>

                {/* 6b. Jaimini Karakas — separate card */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.jaiminiKarakas')}</h4>
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
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.karaka')}</th>
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                        </tr></thead>
                        <tbody>
                          {karakaOrder.map(({ key, name }) => {
                            const planet = Object.entries(karakas).find(([, v]) => v === key)?.[0] || '-';
                            return (
                              <tr key={key} className="border-t border-sacred-gold/10">
                                <td className="p-2 text-sacred-brown"><span className="font-semibold">{key}</span> <span className="text-xs text-sacred-text-secondary">({name})</span></td>
                                <td className="p-2 font-semibold" style={{ color: '#B8860B' }}>{translatePlanet(planet, language)}</td>
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
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.yogasAndDoshas')}</h4>
                  {loadingYogaDosha ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : yogaDoshaData ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <CheckCircle className="w-4 h-4 text-green-500" />
                          <h5 className="text-sm font-semibold text-sacred-brown">{t('section.yogas')}</h5>
                        </div>
                        <div className="space-y-1">
                          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).slice(0, 8).map((yoga: any, idx: number) => (
                            <div key={idx} className="rounded-lg p-2 text-xs border border-green-500/20 bg-green-500/5">
                              <div className="flex items-center justify-between">
                                <span className="font-medium text-sacred-brown">{translateName(yoga.name, language)}</span>
                                <span className="text-xs px-1.5 py-0.5 rounded-full bg-green-500/20 text-green-400">
                                  {t('common.present')}
                                </span>
                              </div>
                            </div>
                          ))}
                          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).length === 0 && (
                            <p className="text-sm text-sacred-text-secondary py-2">{t('kundli.noYogasDetected')}</p>
                          )}
                        </div>
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <Shield className="w-4 h-4 text-red-500" />
                          <h5 className="text-sm font-semibold text-sacred-brown">{t('section.doshas')}</h5>
                        </div>
                        <div className="space-y-1">
                          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).slice(0, 8).map((dosha: any, idx: number) => (
                            <div key={idx} className="rounded-lg p-2 text-xs border border-red-500/20 bg-red-500/5">
                              <div className="flex items-center justify-between">
                                <span className="font-medium text-sacred-brown">{translateName(dosha.name, language)}</span>
                                <span className="text-xs px-1.5 py-0.5 rounded-full bg-red-500/20 text-red-400">
                                  {t('common.present')}
                                </span>
                              </div>
                            </div>
                          ))}
                          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).length === 0 && (
                            <p className="text-sm text-green-400 py-2">{t('kundli.noDoshasDetected')}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 7b. Mangal / Kaal Sarp / Sade Sati Dosha */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4 lg:col-span-2">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.doshaAnalysis')}</h4>
                  {loadingDosha ? (
                    <div className="flex items-center justify-center py-8"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
                  ) : doshaData ? (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {/* Mangal Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.mangal_dosha?.has_dosha ? 'border-red-500/30 bg-red-500/5' : 'border-green-500/20 bg-green-500/5'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">{translateName('Mangal Dosha', language)}</h5>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${doshaData.mangal_dosha?.has_dosha ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                            {doshaData.mangal_dosha?.has_dosha ? translateLabel(doshaData.mangal_dosha.severity, language) || t('common.present') : t('common.absent')}
                          </span>
                        </div>
                        <p className="text-xs text-sacred-text-secondary">{doshaData.mangal_dosha?.description || t('kundli.noMangalDosha')}</p>
                      </div>
                      {/* Kaal Sarp Dosha */}
                      <div className={`rounded-lg p-3 border ${doshaData.kaal_sarp_dosha?.has_dosha ? 'border-red-500/30 bg-red-500/5' : 'border-green-500/20 bg-green-500/5'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">{translateName('Kaal Sarp Dosha', language)}</h5>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${doshaData.kaal_sarp_dosha?.has_dosha ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                            {doshaData.kaal_sarp_dosha?.has_dosha ? translateLabel(doshaData.kaal_sarp_dosha.severity, language) || t('common.present') : t('common.absent')}
                          </span>
                        </div>
                        <p className="text-xs text-sacred-text-secondary">{doshaData.kaal_sarp_dosha?.description || t('kundli.noKaalSarpDosha')}</p>
                      </div>
                      {/* Sade Sati */}
                      <div className={`rounded-lg p-3 border ${doshaData.sade_sati?.has_sade_sati ? 'border-orange-500/30 bg-orange-500/5' : 'border-green-500/20 bg-green-500/5'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-semibold text-sacred-brown">{translateName('Sade Sati', language)}</h5>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${doshaData.sade_sati?.has_sade_sati ? 'bg-orange-500/20 text-orange-600' : 'bg-green-500/20 text-green-400'}`}>
                            {doshaData.sade_sati?.has_sade_sati ? `${t('common.active')} - ${translateLabel(doshaData.sade_sati.phase, language)}` : t('common.inactive')}
                          </span>
                        </div>
                        <p className="text-xs text-sacred-text-secondary">{doshaData.sade_sati?.description || t('kundli.sadeSatiNotActive')}</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 8. Ashtakvarga SAV bar chart */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.sarvashtakvarga')}</h4>
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
                              <span className="text-xs font-medium text-sacred-brown">{points}</span>
                              <div className="w-full bg-sacred-gold/10 rounded-t-sm relative" style={{ height: '100px' }}>
                                <div
                                  className="absolute bottom-0 w-full rounded-t-sm"
                                  style={{ height: `${heightPct}%`, backgroundColor: isStrong ? '#B8860B' : '#b8b0a4' }}
                                />
                              </div>
                              <span className="text-xs text-sacred-text-secondary">{sign.slice(0, 3)}</span>
                            </div>
                          );
                        })}
                      </div>
                      <div className="flex items-center gap-3 mt-2 text-xs text-sacred-text-secondary">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#B8860B' }} />{t('kundli.strong')}</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#b8b0a4' }} />{t('kundli.weak')}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">{t('common.loading')}</p>
                  )}
                </div>

                {/* 9. Shadbala bar chart */}
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.shadbalaStrength')}</h4>
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
                            <span className="w-12 text-xs font-medium text-sacred-brown">{translatePlanet(planet, language)}</span>
                            <div className="flex-1 bg-sacred-gold/10 rounded-full h-4 overflow-hidden">
                              <div className="h-full rounded-full" style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }} />
                            </div>
                            <span className={`text-xs w-16 text-right font-medium ${data.is_strong ? 'text-[#B8860B]' : 'text-[#8B2332]'}`}>
                              {data.total}/{data.required}
                            </span>
                          </div>
                        );
                      })}
                      <div className="flex items-center gap-3 mt-1 text-xs text-sacred-text-secondary">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#B8860B' }} />{t('kundli.strong')}</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#8B2332' }} />{t('kundli.weak')}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center text-sacred-text-secondary py-4 text-sm">{t('common.loading')}</p>
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
                          ? `${translatePlanet(sidePanel.planet?.planet || '', language)} — ${t('kundli.details')}`
                          : t('kundli.houseDetails')}
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
                              <p className="text-xs text-sacred-text-secondary">{t('kundli.sign')}</p>
                              <p className="font-semibold text-sacred-brown">{translateSign(p.sign, language)}</p>
                            </div>
                            <div className="bg-cosmic-card/60 rounded-lg p-3">
                              <p className="text-xs text-sacred-text-secondary">{t('kundli.degree')}</p>
                              <p className="font-semibold text-sacred-brown">{p.sign_degree?.toFixed(1)}&deg;</p>
                            </div>
                            <div className="bg-cosmic-card/60 rounded-lg p-3">
                              <p className="text-xs text-sacred-text-secondary">{t('kundli.house')}</p>
                              <p className="font-semibold text-sacred-brown">{p.house}</p>
                            </div>
                            <div className="bg-cosmic-card/60 rounded-lg p-3">
                              <p className="text-xs text-sacred-text-secondary">{t('kundli.nakshatra')}</p>
                              <p className="font-semibold text-sacred-brown">{p.nakshatra || 'N/A'}</p>
                            </div>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">{t('kundli.strength')}</p>
                            <p className={`font-semibold ${strengthColor}`}>{translateLabel(strengthLabel, language)}</p>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">{t('kundli.aspects')}</p>
                            <p className="font-semibold text-sacred-brown text-sm">{aspects.join(', ')}</p>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">{t('kundli.housePlacement')}</p>
                            <p className="text-sm text-sacred-brown">
                              {translatePlanet(p.planet, language)} — {t('kundli.house')} {p.house} ({HOUSE_SIGNIFICANCE[p.house] || 'Unknown'})
                            </p>
                          </div>
                        </div>
                      );
                    })()}

                    {sidePanel.type === 'house' && (
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-3">
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">{t('kundli.houseNumber')}</p>
                            <p className="font-semibold text-sacred-brown">{sidePanel.house}</p>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">{t('kundli.sign')}</p>
                            <p className="font-semibold text-sacred-brown">{translateSign(sidePanel.sign || '', language)}</p>
                          </div>
                        </div>
                        <div className="bg-cosmic-card/60 rounded-lg p-3">
                          <p className="text-xs text-sacred-text-secondary">{t('kundli.significance')}</p>
                          <p className="font-semibold text-sacred-brown">
                            {HOUSE_SIGNIFICANCE[sidePanel.house || 0] || 'Unknown'}
                          </p>
                        </div>
                        <div className="bg-cosmic-card/60 rounded-lg p-3">
                          <p className="text-xs text-sacred-text-secondary mb-2">{t('kundli.planetsInHouse')}</p>
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
                            <p className="text-sm text-sacred-text-secondary">{t('kundli.noPlanets')}</p>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="bg-sacred-cream/50 rounded-xl border border-dashed border-sacred-gold/20 p-8 flex flex-col items-center justify-center h-full min-h-[200px]">
                    <Sparkles className="w-8 h-8 text-sacred-gold/40 mb-3" />
                    <p className="text-sacred-text-secondary text-sm text-center">
                      {t('kundli.clickInfo')}
                    </p>
                  </div>
                )}

                {/* Planet table below the side panel */}
                <div className="mt-6 overflow-x-auto rounded-xl border border-sacred-gold/20">
                  <table className="w-full">
                    <thead className="bg-sacred-cream">
                      <tr>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.planet')}</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.sign')}</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.house')}</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.nakshatra')}</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.status')}</th>
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
                          <td className="p-3 text-sacred-brown font-medium text-sm">{translatePlanet(planet.planet, language)}</td>
                          <td className="p-3 text-sacred-text-secondary text-sm">{translateSign(planet.sign, language)}</td>
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
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.analyzingDoshas')}</span></div>
            ) : doshaDisplay ? (
              <div className="grid gap-4">
                {doshaDisplay.mangal.has_dosha && (
                <div className="bg-sacred-cream rounded-xl p-4 border border-red-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">{translateName('Mangal Dosha', language)}</h4>
                    <span className="text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-400">
                      {t('common.present')} ({translateLabel(doshaDisplay.mangal.severity, language)})
                    </span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.mangal.description}</p>
                </div>
                )}
                {doshaDisplay.kaalsarp.has_dosha && (
                <div className="bg-sacred-cream rounded-xl p-4 border border-red-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">{translateName('Kaal Sarp Dosha', language)}</h4>
                    <span className="text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-400">{t('common.present')}</span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.kaalsarp.description}</p>
                </div>
                )}
                {doshaDisplay.sadesati.has_sade_sati && (
                <div className="bg-sacred-cream rounded-xl p-4 border border-orange-200">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">{translateName('Sade Sati', language)}</h4>
                    <span className="text-xs px-2 py-1 rounded-full bg-orange-100 text-orange-600">
                      {t('common.active')} - {translateLabel(doshaDisplay.sadesati.phase, language)}
                    </span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.sadesati.description}</p>
                </div>
                )}
                {!doshaDisplay.mangal.has_dosha && !doshaDisplay.kaalsarp.has_dosha && !doshaDisplay.sadesati.has_sade_sati && (
                  <p className="text-sm py-4" style={{ color: '#22c55e' }}>{t('kundli.noDoshasInChart')}</p>
                )}
                {/* Gemstone Recommendations */}
                {doshaDisplay.gemstones && doshaDisplay.gemstones.length > 0 && (
                  <div className="bg-sacred-cream rounded-xl p-4 border border-sacred-gold/30 mt-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
                      <Gem className="w-5 h-5 text-sacred-gold" />
                      {language === 'hi' ? 'रत्न सिफारिशें' : 'Gemstone Recommendations'}
                    </h4>
                    <div className="grid gap-3">
                      {doshaDisplay.gemstones.map((g: any, i: number) => (
                        <div key={i} className={`rounded-lg p-3 border ${g.priority === 'primary' ? 'border-sacred-gold/50 bg-sacred-gold/5' : 'border-sacred-gold/20'}`}>
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-semibold text-sm text-sacred-brown">
                              {language === 'hi' ? g.gemstone_hi : g.gemstone}
                            </span>
                            <span className={`text-xs px-2 py-0.5 rounded-full ${g.priority === 'primary' ? 'bg-sacred-gold/20 text-sacred-gold' : 'bg-blue-500/20 text-blue-400'}`}>
                              {g.priority === 'primary' ? (language === 'hi' ? 'प्राथमिक' : 'Primary') : (language === 'hi' ? 'सहायक' : 'Secondary')}
                            </span>
                          </div>
                          <p className="text-xs text-sacred-text-secondary">
                            {language === 'hi' ? 'ग्रह' : 'Planet'}: <strong>{translatePlanet(g.planet, language)}</strong> ({language === 'hi' ? g.reason : g.reason})
                          </p>
                          <p className="text-xs text-sacred-text-secondary mt-1">
                            {language === 'hi' ? 'धातु' : 'Metal'}: {g.metal} &bull; {language === 'hi' ? 'अंगुली' : 'Finger'}: {g.finger} &bull; {language === 'hi' ? 'दिन' : 'Day'}: {g.day}
                          </p>
                        </div>
                      ))}
                    </div>
                    <p className="text-xs text-sacred-text-muted mt-2 italic">
                      {language === 'hi' ? '* कृपया रत्न धारण करने से पहले किसी योग्य ज्योतिषी से परामर्श लें।' : '* Please consult a qualified astrologer before wearing any gemstone.'}
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickDoshaTab')}</p>
            )}
          </TabsContent>

          {/* IO-GITA TAB */}
          <TabsContent value="iogita">
            {loadingIogita ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.analyzingLifePath')}</span></div>
            ) : iogitaData?.basin ? (
              <div className="space-y-6">
                {/* Overall Summary Card */}
                <div className="rounded-2xl p-6 border border-sacred-gold/30" style={{ background: 'linear-gradient(135deg, rgba(184,134,11,0.08) 0%, rgba(34,34,58,0.9) 100%)' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-full bg-sacred-gold/20 flex items-center justify-center">
                      <Sparkles className="w-6 h-6 text-sacred-gold" />
                    </div>
                    <div>
                      <h4 className="font-display font-bold text-xl" style={{ color: '#D4A052' }}>{t('iogita.yourLifePattern')}: {iogitaData.basin.name}</h4>
                      <p className="text-sm" style={{ color: '#b8b0a4' }}>{t('iogita.basedOnPositions')}</p>
                    </div>
                  </div>
                  <p className="text-sm leading-relaxed mb-4" style={{ color: '#e8e0d4' }}>{iogitaData.basin.description}</p>
                </div>

                {/* Strengths — Top Forces */}
                <div className="rounded-xl p-5 border border-sacred-gold/20" style={{ background: 'rgba(34,34,58,0.8)' }}>
                  <h4 className="font-display font-semibold mb-4" style={{ color: '#D4A052' }}>{t('iogita.strongestQualities')}</h4>
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
                    <h4 className="font-display font-semibold mb-2" style={{ color: '#f87171' }}>{t('iogita.areaNeedsAttention')}</h4>
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
                    <h4 className="font-display font-semibold mb-2" style={{ color: '#fbbf24' }}>{t('iogita.beMindfulOf')}</h4>
                    <p className="text-sm leading-relaxed" style={{ color: '#fde68a' }}>{iogitaData.basin.warning}</p>
                  </div>
                  <div className="rounded-xl p-5 border border-emerald-500/20" style={{ background: 'rgba(16,185,129,0.08)' }}>
                    <h4 className="font-display font-semibold mb-2" style={{ color: '#34d399' }}>{t('iogita.pathToGrowth')}</h4>
                    <p className="text-sm leading-relaxed" style={{ color: '#6ee7b7' }}>{iogitaData.basin.escape_trigger}</p>
                  </div>
                </div>

                {/* Overall Insight */}
                {iogitaData.iogita_insight && (
                  <div className="rounded-xl p-5 border border-sacred-gold/20" style={{ background: 'rgba(34,34,58,0.8)' }}>
                    <h4 className="font-display font-semibold mb-3" style={{ color: '#D4A052' }}>{t('iogita.overallLifeReading')}</h4>
                    <p className="text-sm leading-relaxed" style={{ color: '#e8e0d4' }}>{iogitaData.iogita_insight}</p>
                  </div>
                )}

                {/* Normal Astrology Insights */}
                {iogitaData.normal_astrology && iogitaData.normal_astrology.length > 0 && (
                  <div className="rounded-xl p-5 border border-sacred-gold/20" style={{ background: 'rgba(34,34,58,0.8)' }}>
                    <h4 className="font-display font-semibold mb-3" style={{ color: '#D4A052' }}>{t('iogita.kundliSummary')}</h4>
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
              <p className="text-center py-8" style={{ color: '#b8b0a4' }}>{t('iogita.partialData')}</p>
            ) : (
              <p className="text-center py-8" style={{ color: '#b8b0a4' }}>{t('iogita.clickTab')}</p>
            )}
          </TabsContent>

          {/* DASHA TAB — Extended with Mahadasha -> Antardasha -> Pratyantar */}
          <TabsContent value="dasha">
            {(loadingDasha || loadingExtendedDasha) ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.calculatingDasha')}</span></div>
            ) : extendedDashaData ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20">
                  <p className="text-sm text-sacred-text-secondary">{t('section.currentMahadasha')}</p>
                  <p className="text-xl font-display font-bold" style={{ color: '#B8860B' }}>{translatePlanet(extendedDashaData.current_dasha, language)} {t('kundli.mahadasha')}</p>
                  <div className="flex gap-4 mt-1">
                    {extendedDashaData.current_antardasha && extendedDashaData.current_antardasha !== 'Unknown' && (
                      <p className="text-sm text-sacred-gold-dark">{t('kundli.antardasha')}: {translatePlanet(extendedDashaData.current_antardasha, language)}</p>
                    )}
                    {extendedDashaData.current_pratyantar && extendedDashaData.current_pratyantar !== 'Unknown' && (
                      <p className="text-sm text-sacred-text-secondary">{t('kundli.pratyantar')}: {translatePlanet(extendedDashaData.current_pratyantar, language)}</p>
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
                            {translatePlanet(md.planet, language)} {t('kundli.mahadasha')}
                          </span>
                          {md.is_current && <span className="text-xs px-2 py-0.5 rounded-full bg-[#B8860B]/20 text-[#B8860B] font-medium">{t('common.current')}</span>}
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
                                    {translatePlanet(ad.planet, language)} {t('kundli.antardasha')}
                                  </span>
                                  {ad.is_current && <span className="text-xs px-1.5 py-0.5 rounded-full bg-[#B8860B]/15 text-[#B8860B]">{t('common.current')}</span>}
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
                                        {translatePlanet(pt.planet, language)} {t('kundli.pratyantar')}
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
                  <p className="text-sm text-sacred-text-secondary">{t('section.currentMahadasha')}</p>
                  <p className="text-xl font-display font-bold text-sacred-brown">{translatePlanet(dashaData.current_dasha, language)} {t('kundli.mahadasha')}</p>
                  {dashaData.current_antardasha && <p className="text-sm text-sacred-gold-dark">{t('kundli.antardasha')}: {translatePlanet(dashaData.current_antardasha, language)}</p>}
                </div>
                <div className="rounded-xl border border-sacred-gold/20 overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-sacred-cream">
                      <tr>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.planet')}</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.start')}</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.end')}</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.years')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(dashaData.mahadasha_periods || []).map((p: any) => (
                        <tr key={p.planet} className={`border-t border-sacred-gold/20 ${p.planet === dashaData.current_dasha ? 'bg-sacred-gold/10 font-semibold' : ''}`}>
                          <td className="p-3 text-sacred-brown">{translatePlanet(p.planet, language)} {p.planet === dashaData.current_dasha ? '\u2190' : ''}</td>
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
              <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickDashaTab')}</p>
            )}
          </TabsContent>

          {/* DIVISIONAL CHARTS TAB */}
          <TabsContent value="divisional">
            <div className="space-y-6">
              <div className="flex items-center gap-4 mb-4">
                <label className="text-sm font-medium text-sacred-brown">{t('kundli.selectChart')}:</label>
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
                  <span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingDivisional')}</span>
                </div>
              ) : divisionalData ? (
                <div className="space-y-6">
                  <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20">
                    <h4 className="font-display font-bold text-sacred-brown text-lg">{divisionalData.chart_name || divisionalData.chart_type}</h4>
                    <p className="text-sm text-sacred-text-secondary">{t('kundli.division')}: {divisionalData.division}</p>
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
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.planet')}</th>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.sign')}</th>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.degree')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(divisionalData.planet_signs || {}).map(([planet, sign]: [string, any]) => {
                          const posData = (divisionalData.planet_positions || []).find((p: any) => p.planet === planet);
                          return (
                            <tr key={planet} className="border-t border-sacred-gold/20 hover:bg-sacred-gold/5">
                              <td className="p-3 text-sacred-brown font-medium text-sm">{translatePlanet(planet, language)}</td>
                              <td className="p-3 text-sacred-text-secondary text-sm">{translateSign(sign as string, language)}</td>
                              <td className="p-3 text-sacred-text-secondary text-sm">{posData?.sign_degree?.toFixed(1) || '--'}&deg;</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">{t('kundli.selectChartToLoad')}</p>
              )}
            </div>
          </TabsContent>

          {/* ASHTAKVARGA TAB */}
          <TabsContent value="ashtakvarga">
            {loadingAshtakvarga ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingAshtakvarga')}</span>
              </div>
            ) : ashtakvargaData ? (
              <div className="space-y-6">
                {/* SAV Chart — Visual Kundli with points in each house */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.sarvashtakvarga')} {t('kundli.chart')}</h4>
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
                  <p className="text-xs text-center text-sacred-text-secondary mt-2">{t('ashtakvarga.savDescription')}</p>
                </div>

                {/* SAV Bar Chart */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.sarvashtakvarga')}</h4>
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
                          <span className="text-xs text-sacred-text-secondary truncate w-full text-center" title={sign}>
                            {sign.slice(0, 3)}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center gap-4 mt-3 text-xs text-sacred-text-secondary">
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#B8860B' }} />
                      <span>{t('kundli.strong')} (&ge;28)</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#b8b0a4' }} />
                      <span>{t('kundli.weak')} (&lt;28)</span>
                    </div>
                  </div>
                </div>

                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.bhinnashtakvarga')}</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-sacred-gold/20">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                          {['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'].map((s) => (
                            <th key={s} className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{s}</th>
                          ))}
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.total')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                          const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                          const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
                          const total = signs.reduce((sum, s) => sum + (bindus[s] || 0), 0);
                          return (
                            <tr key={planet} className="border-t border-sacred-gold/10 hover:bg-sacred-gold/5">
                              <td className="p-2 text-sacred-brown font-medium">{translatePlanet(planet, language)}</td>
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
              <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickAshtakvargaTab')}</p>
            )}
          </TabsContent>

          {/* SHADBALA TAB */}
          <TabsContent value="shadbala">
            {loadingShadbala ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">{t('kundli.calculatingShadbala')}</span>
              </div>
            ) : shadbalaData?.planets ? (
              <div className="space-y-6">
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.shadbalaStrength')}</h4>
                  <div className="space-y-3">
                    {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                      const data = shadbalaData.planets[planet];
                      if (!data) return null;
                      const pct = Math.min((data.total / data.required) * 100, 150);
                      const barColor = data.is_strong ? '#B8860B' : '#8B2332';
                      return (
                        <div key={planet} className="flex items-center gap-3">
                          <span className="w-16 text-sm font-medium text-sacred-brown">{translatePlanet(planet, language)}</span>
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
                      <span>{t('kundli.strong')}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#8B2332' }} />
                      <span>{t('kundli.weak')}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.detailedBreakdown')}</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-sacred-gold/20">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Sthana</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Dig</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Kala</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Cheshta</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Naisargika</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Drik</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.total')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">Ratio</th>
                        </tr>
                      </thead>
                      <tbody>
                        {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                          const d = shadbalaData.planets[planet];
                          if (!d) return null;
                          return (
                            <tr key={planet} className={`border-t border-sacred-gold/10 ${d.is_strong ? '' : 'bg-[#8B2332]/5'}`}>
                              <td className="p-2 text-sacred-brown font-medium">{translatePlanet(planet, language)}</td>
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
              <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickShadbalaTab')}</p>
            )}
          </TabsContent>

          {/* AVAKHADA CHAKRA TAB */}
          <TabsContent value="avakhada">
            {loadingAvakhada ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">{t('kundli.calculatingAvakhada')}</span>
              </div>
            ) : avakhadaData ? (
              <div className="space-y-4">
                <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20 mb-4">
                  <h4 className="font-display font-bold text-lg" style={{ color: '#e8e0d4' }}>{t('section.avakhadaChakra')}</h4>
                  <p className="text-sm text-sacred-text-secondary">{t('avakhada.birthSummary')}</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[
                    { label: t('avakhada.ascendant'), value: avakhadaData.ascendant },
                    { label: t('avakhada.ascendantLord'), value: avakhadaData.ascendant_lord },
                    { label: t('avakhada.rashi'), value: avakhadaData.rashi },
                    { label: t('avakhada.rashiLord'), value: avakhadaData.rashi_lord },
                    { label: t('avakhada.nakshatra'), value: `${avakhadaData.nakshatra} (${t('kundli.pada')} ${avakhadaData.nakshatra_pada})` },
                    { label: t('avakhada.yoga'), value: avakhadaData.yoga },
                    { label: t('avakhada.karana'), value: avakhadaData.karana },
                    { label: t('avakhada.yoni'), value: avakhadaData.yoni },
                    { label: t('avakhada.gana'), value: avakhadaData.gana },
                    { label: t('avakhada.nadi'), value: avakhadaData.nadi },
                    { label: t('avakhada.varna'), value: avakhadaData.varna },
                    { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
                    { label: t('avakhada.sunSign'), value: avakhadaData.sun_sign },
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
              <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickAvakhadaTab')}</p>
            )}
          </TabsContent>

          {/* YOGA & DOSHA TAB */}
          <TabsContent value="yoga-dosha">
            {loadingYogaDosha ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">{t('kundli.analyzingYogasAndDoshas')}</span>
              </div>
            ) : yogaDoshaData ? (
              <div className="space-y-8">
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <CheckCircle className="w-5 h-5" style={{ color: '#22c55e' }} />
                    <h4 className="font-display font-bold text-lg" style={{ color: '#e8e0d4' }}>{t('section.yogas')}</h4>
                  </div>
                  <div className="grid gap-3">
                    {(yogaDoshaData.yogas || []).filter((y: any) => y.present).length === 0 && (
                      <p className="text-sm text-sacred-text-secondary py-4">{t('kundli.noYogasDetected')}</p>
                    )}
                    {(yogaDoshaData.yogas || []).filter((y: any) => y.present).map((yoga: any, idx: number) => (
                      <div
                        key={idx}
                        className="rounded-xl p-4 border border-green-500/30"
                        style={{ backgroundColor: 'rgba(34,197,94,0.05)' }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-display font-semibold" style={{ color: '#e8e0d4' }}>{translateName(yoga.name, language)}</h5>
                          <span className="text-xs px-2 py-1 rounded-full font-medium bg-green-500/20 text-green-400">
                            {t('common.present')}
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
                    <h4 className="font-display font-bold text-lg" style={{ color: '#e8e0d4' }}>{t('section.doshas')}</h4>
                  </div>
                  <div className="grid gap-3">
                    {(yogaDoshaData.doshas || []).filter((d: any) => d.present).length === 0 && (
                      <p className="text-sm py-4" style={{ color: '#22c55e' }}>{t('kundli.noDoshasInChart')}</p>
                    )}
                    {(yogaDoshaData.doshas || []).filter((d: any) => d.present).map((dosha: any, idx: number) => (
                      <div
                        key={idx}
                        className={`rounded-xl p-4 border ${dosha.severity === 'high' ? 'border-red-500/40' : 'border-amber-400/40'}`}
                        style={{ backgroundColor: dosha.severity === 'high' ? 'rgba(196,62,78,0.08)' : 'rgba(245,158,11,0.05)' }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-display font-semibold" style={{ color: '#e8e0d4' }}>{translateName(dosha.name, language)}</h5>
                          <div className="flex items-center gap-2">
                            {dosha.severity !== 'none' && (
                              <span className={`text-xs px-2 py-0.5 rounded-full ${dosha.severity === 'high' ? 'bg-red-500/20 text-red-400' : dosha.severity === 'medium' ? 'bg-amber-400/20 text-amber-600' : 'bg-yellow-500/20 text-yellow-400'}`}>
                                {translateLabel(dosha.severity, language)}
                              </span>
                            )}
                            <span className="text-xs px-2 py-1 rounded-full font-medium bg-red-500/20 text-red-400">
                              {t('common.present')}
                            </span>
                          </div>
                        </div>
                        <p className="text-sm" style={{ color: '#b8b0a4' }}>{dosha.description}</p>
                        {dosha.remedies && dosha.remedies.length > 0 && (
                          <div className="mt-3 pt-3 border-t" style={{ borderColor: 'rgba(184,134,11,0.2)' }}>
                            <p className="text-xs font-semibold mb-2" style={{ color: '#B8860B' }}>
                              <AlertTriangle className="w-3 h-3 inline mr-1" />{t('section.remedies')}:
                            </p>
                            <ul className="space-y-1">
                              {dosha.remedies.map((r: string, ri: number) => (
                                <li key={ri} className="text-xs flex items-start gap-2" style={{ color: '#b8b0a4' }}>
                                  <span className="mt-1 w-1 h-1 rounded-full flex-shrink-0" style={{ backgroundColor: '#B8860B' }} />
                                  {translateRemedy(r, language)}
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
              <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickYogasTab')}</p>
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
            {/* Date/Time Picker — always visible */}
            <div className="rounded-xl p-4 mb-4 border" style={{ backgroundColor: 'rgba(184,134,11,0.04)', borderColor: 'rgba(184,134,11,0.25)' }}>
              <h4 className="font-display font-bold text-lg mb-3" style={{ color: '#D4A052' }}>{t('section.gocharPredictions')}</h4>
              <div className="flex flex-wrap items-end gap-3">
                <div>
                  <label className="text-xs block mb-1" style={{ color: '#b8b0a4' }}>{t('common.date')}</label>
                  <input
                    type="date"
                    value={transitDate}
                    onChange={(e) => setTransitDate(e.target.value)}
                    className="px-3 py-1.5 rounded-lg text-sm border"
                    style={{ backgroundColor: '#22223a', borderColor: 'rgba(184,134,11,0.3)', color: '#e8e0d4' }}
                  />
                </div>
                <div>
                  <label className="text-xs block mb-1" style={{ color: '#b8b0a4' }}>{t('common.time')}</label>
                  <input
                    type="time"
                    value={transitTime}
                    onChange={(e) => setTransitTime(e.target.value)}
                    className="px-3 py-1.5 rounded-lg text-sm border"
                    style={{ backgroundColor: '#22223a', borderColor: 'rgba(184,134,11,0.3)', color: '#e8e0d4' }}
                  />
                </div>
                <Button
                  size="sm"
                  onClick={() => {
                    setTransitData(null);
                    fetchTransit(transitDate || undefined, transitTime ? `${transitTime}:00` : undefined);
                  }}
                  className="px-4"
                  style={{ backgroundColor: '#D4A052', color: '#1a1a2e' }}
                >
                  {transitDate ? t('transit.viewTransits') : t('transit.currentTransits')}
                </Button>
                {transitDate && (
                  <button
                    onClick={() => { setTransitDate(''); setTransitTime(''); setTransitData(null); fetchTransit(); }}
                    className="text-xs px-3 py-1.5 rounded-lg border"
                    style={{ borderColor: 'rgba(184,134,11,0.3)', color: '#b8b0a4' }}
                  >
                    {t('transit.resetToNow')}
                  </button>
                )}
              </div>
              {transitData && (
                <div className="flex flex-wrap gap-4 text-sm mt-3">
                  <span style={{ color: '#e8e0d4' }}><strong>{t('transit.transitDate')}:</strong> {transitData.transit_date}</span>
                  <span style={{ color: '#e8e0d4' }}><strong>{t('transit.natalMoon')}:</strong> {translateSign(transitData.natal_moon_sign, language)}</span>
                </div>
              )}
            </div>

            {loadingTransit ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">{t('transit.loading')}</span>
              </div>
            ) : transitData ? (
              <div className="space-y-6">
                {/* Transit Chart — clickable houses */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2">{t('transit.chart')} ({transitData.transit_date})</h4>
                  <p className="text-xs mb-3" style={{ color: '#b8b0a4' }}>{t('kundli.clickHouseToRotate')}</p>
                  <div className="w-full max-w-[600px] mx-auto">
                    {(() => {
                      const shift = transitHouseShift;
                      const transitPlanets = (transitData.transits || []).map((tr: any) => ({
                        planet: tr.planet,
                        sign: tr.current_sign,
                        house: shift ? ((((tr.house || 1) - 1 - shift + 12) % 12) + 1) : (tr.house || 1),
                        nakshatra: tr.nakshatra || '',
                        sign_degree: tr.sign_degree || 0,
                        status: tr.is_retrograde ? 'Retrograde' : (tr.effect === 'favorable' ? 'Benefic' : 'Malefic'),
                      }));
                      const baseHouses = transitData.chart_data?.houses || result?.chart_data?.houses;
                      const transitHouses = shift && baseHouses
                        ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                        : baseHouses;
                      return (
                        <InteractiveKundli
                          chartData={{ planets: transitPlanets, houses: transitHouses }}
                          onPlanetClick={() => {}}
                          onHouseClick={(house) => {
                            // Clicking house X: shift so that house becomes house 1
                            const originalHouse = shift ? ((house - 1 + shift) % 12) + 1 : house;
                            const newShift = originalHouse - 1;
                            setTransitHouseShift(newShift === 0 ? 0 : newShift);
                          }}
                        />
                      );
                    })()}
                  </div>
                  <div className="flex items-center justify-center gap-4 mt-2 text-xs text-sacred-text-secondary">
                    <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: '#D4A052'}} /> {t('transit.benefic')}</span>
                    <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full" style={{backgroundColor: '#C43E4E'}} /> {t('transit.malefic')}</span>
                    {transitHouseShift > 0 && (
                      <button onClick={() => setTransitHouseShift(0)} className="text-xs px-2 py-0.5 rounded border" style={{ borderColor: 'rgba(184,134,11,0.3)', color: '#D4A052' }}>
                        {t('common.resetView')}
                      </button>
                    )}
                  </div>
                </div>

                {/* Sade Sati Status */}
                <div
                  className={`rounded-xl p-4 border ${transitData.sade_sati?.active ? 'border-red-500/40' : 'border-green-500/30'}`}
                  style={{ backgroundColor: transitData.sade_sati?.active ? 'rgba(196,62,78,0.08)' : 'rgba(34,197,94,0.05)' }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h5 className="font-display font-semibold" style={{ color: '#e8e0d4' }}>
                      <Shield className="w-4 h-4 inline mr-2" />
                      {translateName('Sade Sati', language)}
                    </h5>
                    <span className={`text-xs px-2 py-1 rounded-full font-medium ${transitData.sade_sati?.active ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                      {transitData.sade_sati?.active ? t('common.active') : t('common.inactive')}
                    </span>
                  </div>
                  {transitData.sade_sati?.active && (
                    <p className="text-xs mb-1" style={{ color: '#B8860B' }}>
                      <strong>{t('table.phase')}:</strong> {translateLabel(transitData.sade_sati.phase, language)}
                    </p>
                  )}
                  <p className="text-sm" style={{ color: '#b8b0a4' }}>{transitData.sade_sati?.description}</p>
                </div>

                {/* Transit Table */}
                <div className="rounded-xl border overflow-hidden" style={{ borderColor: 'rgba(184,134,11,0.25)' }}>
                  <table className="w-full text-sm">
                    <thead>
                      <tr style={{ backgroundColor: 'rgba(184,134,11,0.08)' }}>
                        <th className="text-left p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>{t('table.planet')}</th>
                        <th className="text-left p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>{t('transit.currentSign')}</th>
                        <th className="text-center p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>{t('transit.houseFromMoon')}</th>
                        <th className="text-center p-3 font-display font-semibold" style={{ color: '#e8e0d4' }}>{t('transit.effect')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(transitData.transits || []).map((tr: any, idx: number) => (
                        <tr
                          key={idx}
                          className="border-t"
                          style={{ borderColor: 'rgba(184,134,11,0.15)', backgroundColor: idx % 2 === 0 ? 'transparent' : 'rgba(184,134,11,0.02)' }}
                        >
                          <td className="p-3 font-medium" style={{ color: '#e8e0d4' }}>{translatePlanet(tr.planet, language)}</td>
                          <td className="p-3" style={{ color: '#b8b0a4' }}>{translateSign(tr.current_sign, language)}</td>
                          <td className="p-3 text-center" style={{ color: '#b8b0a4' }}>{tr.natal_house_from_moon}</td>
                          <td className="p-3 text-center">
                            <span className={`inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full font-medium ${tr.effect === 'favorable' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                              {tr.effect === 'favorable' ? <CheckCircle className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
                              {tr.effect === 'favorable' ? t('common.favorable') : t('common.unfavorable')}
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
                        <span className="font-display font-semibold" style={{ color: '#e8e0d4' }}>{translatePlanet(tr.planet, language)}</span>
                        <span className="text-xs" style={{ color: '#b8b0a4' }}>{translateSign(tr.current_sign, language)}</span>
                        <span className={`text-xs px-1.5 py-0.5 rounded-full ${tr.effect === 'favorable' ? 'bg-green-500/15 text-green-400' : 'bg-red-500/15 text-red-400'}`}>
                          {tr.effect === 'favorable' ? t('common.favorable') : t('common.unfavorable')}
                        </span>
                      </div>
                      <p className="text-sm" style={{ color: '#b8b0a4' }}>{tr.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">{t('transit.clickTab')}</p>
            )}
          </TabsContent>

          {/* VARSHPHAL TAB */}
          <TabsContent value="varshphal">
            <div className="space-y-6">
              {/* Year selector */}
              <div className="flex items-center gap-4 mb-4">
                <label className="text-sm font-medium text-sacred-brown">{t('varshphal.selectYear')}:</label>
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
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('varshphal.calculating')}</span></div>
              ) : varshphalData ? (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Solar Return Info */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.solarReturn')}</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('varshphal.solarReturnDate')}</p>
                        <p className="font-semibold text-sacred-brown">{varshphalData.solar_return?.date}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('varshphal.solarReturnTime')}</p>
                        <p className="font-semibold text-sacred-brown">{varshphalData.solar_return?.time}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('section.yearLord')}</p>
                        <p className="font-semibold" style={{ color: '#B8860B' }}>{translatePlanet(varshphalData.year_lord, language)}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('varshphal.completedYears')}</p>
                        <p className="font-semibold text-sacred-brown">{varshphalData.completed_years}</p>
                      </div>
                    </div>
                  </div>

                  {/* Muntha */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.muntha')}</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('section.munthaSign')}</p>
                        <p className="font-semibold text-sacred-brown">{translateSign(varshphalData.muntha?.sign || '', language)}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('varshphal.munthaHouse')}</p>
                        <p className="font-semibold text-sacred-brown">House {varshphalData.muntha?.house}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('section.munthaLord')}</p>
                        <p className="font-semibold" style={{ color: '#B8860B' }}>{translatePlanet(varshphalData.muntha?.lord || '', language)}</p>
                      </div>
                      <div className="bg-white/5 rounded-lg p-3">
                        <p className="text-xs text-sacred-text-secondary">{t('table.status')}</p>
                        <p className={`font-semibold ${varshphalData.muntha?.favorable ? 'text-green-400' : 'text-red-500'}`}>
                          {varshphalData.muntha?.favorable ? t('common.favorable') : t('common.challenging')}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Varshphal Chart */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.varshphalChart')} ({varshphalYear})</h4>
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
                    ) : <p className="text-center text-sacred-text-secondary py-4 text-sm">{t('common.noData')}</p>}
                  </div>

                  {/* Mudda Dasha */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">
                      {t('section.muddaDasha')}
                      {varshphalData.current_mudda_dasha && (
                        <span className="ml-2 text-xs px-2 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold-dark">
                          {t('common.current')}: {translatePlanet(varshphalData.current_mudda_dasha, language)}
                        </span>
                      )}
                    </h4>
                    <table className="w-full text-xs">
                      <thead><tr className="bg-sacred-gold/10">
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.start')}</th>
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.end')}</th>
                        <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.days')}</th>
                      </tr></thead>
                      <tbody>
                        {(varshphalData.mudda_dasha || []).map((md: any) => (
                          <tr key={md.planet} className={`border-t border-sacred-gold/10 ${md.planet === varshphalData.current_mudda_dasha ? 'bg-sacred-gold/10 font-semibold' : ''}`}>
                            <td className="p-2 text-sacred-brown">{translatePlanet(md.planet, language)}{md.planet === varshphalData.current_mudda_dasha ? ' \u2190' : ''}</td>
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
                <p className="text-center text-sacred-text-secondary py-8">{t('varshphal.clickTab')}</p>
              )}
            </div>
          </TabsContent>

          {/* KP SYSTEM TAB */}
          <TabsContent value="kp">
            <div className="space-y-6">
              {loadingKp ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingKP')}</span></div>
              ) : kpData ? (
                <div className="space-y-6">
                  {/* 1. KP Planet Table — full reference chart style */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">Krishnamurti Paddhati — Planet Chart</h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-xs">
                        <thead><tr className="bg-sacred-gold/10">
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Planet</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">R/C</th>
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Sign</th>
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Degree</th>
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Nakshatra</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">Pada</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">RL</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">NL</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SL</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SS</th>
                        </tr></thead>
                        <tbody>
                          {(kpData.planets || []).map((p: any) => (
                            <tr key={p.planet} className="border-t border-sacred-gold/10">
                              <td className="p-1.5 font-semibold text-sacred-brown">{translatePlanet(p.planet, language)}</td>
                              <td className="p-1.5 text-center">{p.retrograde ? <span className="text-red-400 font-bold">R</span> : ''}</td>
                              <td className="p-1.5 text-sacred-text-secondary">{translateSign(p.sign, language)}</td>
                              <td className="p-1.5 text-sacred-text-secondary font-mono">{p.degree_dms || (typeof p.degree === 'number' ? p.degree.toFixed(2) : p.degree)}</td>
                              <td className="p-1.5 text-sacred-text-secondary">{p.nakshatra || '-'}</td>
                              <td className="p-1.5 text-center text-sacred-text-secondary">{p.pada || '-'}</td>
                              <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{p.sign_lord ? p.sign_lord.slice(0, 2) : '-'}</td>
                              <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(p.star_lord || p.nakshatra_lord || '-').slice(0, 2)}</td>
                              <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{p.sub_lord ? p.sub_lord.slice(0, 2) : '-'}</td>
                              <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{p.sub_sub_lord ? p.sub_sub_lord.slice(0, 2) : '-'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* Birth Chart + Cuspal Chart — North Indian Diamond */}
                  {(() => {
                    // Build chart data from KP planets for Birth Chart (Rashi-based houses)
                    const SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
                    const kpPlanets = kpData.planets || [];
                    // Birth chart: house derived from sign relative to ascendant sign
                    const ascSign = result?.chart_data?.ascendant?.sign || (kpData.cusps?.[0]?.sign) || 'Aries';
                    const ascIdx = SIGNS.indexOf(ascSign);
                    const birthPlanets: PlanetData[] = kpPlanets.map((p: any) => {
                      const signIdx = SIGNS.indexOf(p.sign);
                      const house = signIdx >= 0 && ascIdx >= 0 ? ((signIdx - ascIdx + 12) % 12) + 1 : 1;
                      return { planet: p.planet, sign: p.sign, house, nakshatra: p.nakshatra || '', sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, status: '', is_retrograde: p.retrograde };
                    });
                    const birthHouses = SIGNS.map((_, i) => ({ number: i + 1, sign: SIGNS[(ascIdx + i) % 12] }));

                    // Cuspal chart: house based on which cusp range the planet falls in
                    const cusps = kpData.cusps || [];
                    const cuspDegrees = cusps.map((c: any) => typeof c.degree === 'number' ? c.degree : 0);
                    const cuspalPlanets: PlanetData[] = kpPlanets.map((p: any) => {
                      const lon = typeof p.degree === 'number' ? p.degree : 0;
                      let house = 1;
                      for (let h = 0; h < 12; h++) {
                        const start = cuspDegrees[h] || 0;
                        const end = cuspDegrees[(h + 1) % 12] || 0;
                        if (end > start ? (lon >= start && lon < end) : (lon >= start || lon < end)) { house = h + 1; break; }
                      }
                      return { planet: p.planet, sign: p.sign, house, nakshatra: p.nakshatra || '', sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, status: '', is_retrograde: p.retrograde };
                    });
                    const cuspalHouses = cusps.map((c: any, i: number) => ({ number: i + 1, sign: c.sign || SIGNS[(ascIdx + i) % 12] }));

                    return (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                          <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center">Birth Chart</h4>
                          <InteractiveKundli chartData={{ planets: birthPlanets, houses: birthHouses, ascendant: result?.chart_data?.ascendant } as ChartData} compact />
                        </div>
                        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                          <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center">Cuspal Chart</h4>
                          <InteractiveKundli chartData={{ planets: cuspalPlanets, houses: cuspalHouses, ascendant: result?.chart_data?.ascendant } as ChartData} compact />
                        </div>
                      </div>
                    );
                  })()}

                  {/* 2. Bhava Details (Placidus) — House Cusps */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">Bhava Details (Placidus System)</h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-xs">
                        <thead><tr className="bg-sacred-gold/10">
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">House</th>
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Sign</th>
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Degree</th>
                          <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Nakshatra</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">Pada</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">RL</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">NL</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SL</th>
                          <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SS</th>
                        </tr></thead>
                        <tbody>
                          {(kpData.cusps || []).map((c: any, i: number) => {
                            const houseNames = ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth','Tenth','Eleventh','Twelfth'];
                            return (
                              <tr key={i} className="border-t border-sacred-gold/10">
                                <td className="p-1.5 font-semibold text-sacred-brown">{(c.house || i + 1)}.{houseNames[i] || ''}</td>
                                <td className="p-1.5 text-sacred-text-secondary">{translateSign(c.sign || '', language)}</td>
                                <td className="p-1.5 text-sacred-text-secondary font-mono">{c.degree_dms || (typeof c.degree === 'number' ? c.degree.toFixed(2) : c.degree || '-')}</td>
                                <td className="p-1.5 text-sacred-text-secondary">{c.nakshatra || '-'}</td>
                                <td className="p-1.5 text-center text-sacred-text-secondary">{c.pada || '-'}</td>
                                <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{c.sign_lord ? c.sign_lord.slice(0, 2) : '-'}</td>
                                <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(c.star_lord || '-').slice(0, 2)}</td>
                                <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(c.sub_lord || '-').slice(0, 2)}</td>
                                <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(c.sub_sub_lord || '-').slice(0, 2)}</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* 3. Significations of Houses */}
                  {kpData.house_significations && Object.keys(kpData.house_significations).length > 0 && (
                    <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                      <h4 className="font-display font-semibold text-sacred-brown mb-3">Significations of Houses</h4>
                      <div className="overflow-x-auto">
                        <table className="w-full text-xs">
                          <thead><tr className="bg-sacred-gold/10">
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">House</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Planets in Nak. of Occupants</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Occupants</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Planets in Nak. of Cusp Lord</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Cusp Sign Lord</th>
                          </tr></thead>
                          <tbody>
                            {[1,2,3,4,5,6,7,8,9,10,11,12].map(h => {
                              const sig = kpData.house_significations[h] || kpData.house_significations[String(h)] || {};
                              return (
                                <tr key={h} className="border-t border-sacred-gold/10">
                                  <td className="p-1.5 font-semibold text-sacred-brown">{h}</td>
                                  <td className="p-1.5 text-sacred-text-secondary">{(sig.planets_in_nak_of_occupants || []).join(', ') || '-'}</td>
                                  <td className="p-1.5 text-sacred-text-secondary font-medium">{(sig.occupants || []).join(', ') || '-'}</td>
                                  <td className="p-1.5 text-sacred-text-secondary">{(sig.planets_in_nak_of_cusp_sign_lord || []).join(', ') || '-'}</td>
                                  <td className="p-1.5 text-sacred-gold-dark font-medium">{sig.cusp_sign_lord || '-'}</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* 4. Houses Signified by Planets */}
                  {kpData.planet_significator_strengths && Object.keys(kpData.planet_significator_strengths).length > 0 && (
                    <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                      <h4 className="font-display font-semibold text-sacred-brown mb-3">Houses Signified by Planets</h4>
                      <div className="overflow-x-auto">
                        <table className="w-full text-xs">
                          <thead><tr className="bg-sacred-gold/10">
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Planet</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Very Strong</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Strong</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Normal</th>
                            <th className="text-left p-1.5 text-sacred-gold-dark font-medium">Weak</th>
                          </tr></thead>
                          <tbody>
                            {Object.entries(kpData.planet_significator_strengths).map(([planet, levels]: [string, any]) => (
                              <tr key={planet} className="border-t border-sacred-gold/10">
                                <td className="p-1.5 font-semibold text-sacred-brown">{translatePlanet(planet, language)}</td>
                                <td className="p-1.5 text-green-500 font-medium">{(levels.very_strong || []).join(' ')}</td>
                                <td className="p-1.5 text-blue-400 font-medium">{(levels.strong || []).join(' ')}</td>
                                <td className="p-1.5 text-sacred-text-secondary">{(levels.normal || []).join(' ')}</td>
                                <td className="p-1.5 text-orange-400">{(levels.weak || []).join(' ')}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* 5. Ruling Planets */}
                  {kpData.ruling_planets && Object.keys(kpData.ruling_planets).length > 0 && (
                    <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                      <h4 className="font-display font-semibold text-sacred-brown mb-3">Ruling Planets</h4>
                      <div className="grid grid-cols-2 gap-3 text-xs">
                        {[
                          ['day_lord', 'Day Lord'],
                          ['lagna_lord', 'Lagna Lord'],
                          ['lagna_nak_lord', 'Lagna Nak Lord'],
                          ['lagna_sub_lord', 'Lagna Sub Lord'],
                          ['moon_rashi_lord', 'Moon Rashi Lord'],
                          ['moon_nak_lord', 'Moon Nak Lord'],
                          ['moon_sub_lord', 'Moon Sub Lord'],
                        ].map(([key, label]) => (
                          <div key={key} className="flex items-center justify-between bg-white/5 rounded-lg p-2">
                            <span className="text-sacred-text-secondary">{label}</span>
                            <span className="font-semibold text-sacred-gold-dark">{translatePlanet(kpData.ruling_planets[key] || '-', language)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickKPTab')}</p>
              )}
            </div>
          </TabsContent>

          {/* YOGINI DASHA TAB */}
          <TabsContent value="yogini">
            <div className="space-y-6">
              {loadingYogini ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingYoginiDasha')}</span></div>
              ) : yoginiData ? (
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">
                    {t('section.yoginiDasha')}
                    {(yoginiData.current_dasha || yoginiData.current) && <span className="ml-2 text-xs px-2 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold-dark">{t('common.current')}: {translateName(yoginiData.current_dasha || yoginiData.current, language)}</span>}
                  </h4>
                  <table className="w-full text-xs">
                    <thead><tr className="bg-sacred-gold/10">
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.yogini')}</th>
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.start')}</th>
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.end')}</th>
                      <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.years')}</th>
                    </tr></thead>
                    <tbody>
                      {(yoginiData.periods || yoginiData.dashas || []).map((d: any, i: number) => {
                        const currentName = yoginiData.current_dasha || yoginiData.current;
                        const isCurrent = d.yogini === currentName || d.is_current;
                        return (
                          <tr key={i} className={`border-t border-sacred-gold/10 ${isCurrent ? 'bg-sacred-gold/10 font-semibold' : ''}`}>
                            <td className="p-2 text-sacred-brown">{translateName(d.yogini, language)}{isCurrent ? ' \u2190' : ''}</td>
                            <td className="p-2 text-sacred-text-secondary">{translatePlanet(d.planet, language)}</td>
                            <td className="p-2 text-sacred-text-secondary">{d.start_date || d.start}</td>
                            <td className="p-2 text-sacred-text-secondary">{d.end_date || d.end}</td>
                            <td className="p-2 text-center text-sacred-text-secondary">{d.span || d.years}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">{t('common.noData')}</p>
              )}
            </div>
          </TabsContent>

          {/* UPAGRAHAS TAB — API returns upagrahas as dict {name: {longitude, sign, ...}} */}
          <TabsContent value="upagrahas">
            <div className="space-y-6">
              {loadingUpagrahas ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingUpagrahas')}</span></div>
              ) : upagrahasData ? (
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.upagrahasTitle')}</h4>
                  <table className="w-full text-xs">
                    <thead><tr className="bg-sacred-gold/10">
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.upagraha')}</th>
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.longitude')}</th>
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.sign')}</th>
                      <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.nakshatra')}</th>
                    </tr></thead>
                    <tbody>
                      {(() => {
                        const raw = upagrahasData.upagrahas;
                        const items = Array.isArray(raw) ? raw : Object.entries(raw || {}).map(([name, data]: [string, any]) => ({ name, ...data }));
                        return items.map((u: any) => (
                          <tr key={u.name} className="border-t border-sacred-gold/10">
                            <td className="p-2 font-semibold text-sacred-brown">{u.name}</td>
                            <td className="p-2 text-sacred-text-secondary">{typeof u.longitude === 'number' ? u.longitude.toFixed(2) + '\u00b0' : u.longitude}</td>
                            <td className="p-2 text-sacred-text-secondary">{translateSign(u.sign, language)}</td>
                            <td className="p-2 text-sacred-text-secondary">{u.nakshatra}{u.nakshatra_pada ? ` (${t('kundli.pada')} ${u.nakshatra_pada})` : u.pada ? ` (${t('kundli.pada')} ${u.pada})` : ''}</td>
                          </tr>
                        ));
                      })()}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">{t('common.noData')}</p>
              )}
            </div>
          </TabsContent>

          {/* SODASHVARGA TAB — API returns by_sign as dict, varga_table as list, by_planet as dict */}
          <TabsContent value="sodashvarga">
            <div className="space-y-6">
              {loadingSodashvarga ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingSodashvarga')}</span></div>
              ) : sodashvargaData ? (
                <div className="space-y-6">
                  {/* Varga Table (list) or By Sign (dict) */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4 overflow-x-auto">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.sodashvargaTitle')}</h4>
                    {(() => {
                      const rows = sodashvargaData.varga_table || (Array.isArray(sodashvargaData.by_sign) ? sodashvargaData.by_sign : []);
                      if (rows.length > 0) {
                        return (
                          <table className="w-full text-xs min-w-[700px]">
                            <thead><tr className="bg-sacred-gold/10">
                              <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.varga')}</th>
                              {['Su', 'Mo', 'Ma', 'Me', 'Ju', 'Ve', 'Sa', 'Ra', 'Ke'].map(p => (
                                <th key={p} className="text-center p-1.5 text-sacred-gold-dark font-medium">{p}</th>
                              ))}
                            </tr></thead>
                            <tbody>
                              {rows.map((row: any) => {
                              const planets = row.placements || row.planets;
                              const planetEntries = Array.isArray(planets)
                                ? planets
                                : typeof planets === 'object'
                                  ? ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'].map(p => planets[p] || '')
                                  : [];
                              return (
                                <tr key={row.varga || row.division || row.name} className="border-t border-sacred-gold/10">
                                  <td className="p-2 font-semibold text-sacred-brown whitespace-nowrap">{row.varga || row.name || `D${row.division}`}</td>
                                  {planetEntries.map((pl: any, i: number) => {
                                    const sign = typeof pl === 'string' ? pl?.slice(0, 3) : (pl?.sign_abbr || pl?.sign?.slice(0, 3) || '');
                                    const dignity = typeof pl === 'object' ? pl?.dignity?.toLowerCase() : '';
                                    const dignityColors: Record<string, string> = {
                                      exalted: 'bg-green-500/30 text-green-700', own: 'bg-blue-500/20 text-blue-700',
                                      moolatrikona: 'bg-blue-500/20 text-blue-700', friend: 'bg-yellow-500/20 text-yellow-700',
                                      enemy: 'bg-orange-500/20 text-orange-700', debilitated: 'bg-red-500/20 text-red-700',
                                    };
                                    return <td key={i} className={`p-1.5 text-center text-xs rounded ${dignityColors[dignity] || ''}`}>{sign}</td>;
                                  })}
                                </tr>
                              );
                            })}
                            </tbody>
                          </table>
                        );
                      }
                      // Fallback: by_sign is a dict
                      if (sodashvargaData.by_sign && typeof sodashvargaData.by_sign === 'object') {
                        return (
                          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                            {Object.entries(sodashvargaData.by_sign).map(([planet, data]: [string, any]) => (
                              <div key={planet} className="bg-white/5 rounded-lg p-3">
                                <p className="font-semibold text-sacred-brown mb-1">{planet}</p>
                                {typeof data === 'object' && Object.entries(data as Record<string, any>).map(([varga, sign]) => (
                                  <p key={varga} className="text-sacred-text-secondary">{varga}: {String(sign)}</p>
                                ))}
                              </div>
                            ))}
                          </div>
                        );
                      }
                      return <p className="text-center text-sacred-text-secondary">{t('common.noData')}</p>;
                    })()}
                    <div className="flex flex-wrap gap-2 mt-3 text-xs">
                      <span className="px-2 py-1 rounded bg-green-500/30 text-green-700">{t('dignity.exalted')}</span>
                      <span className="px-2 py-1 rounded bg-blue-500/20 text-blue-700">{t('dignity.ownMoolatrikona')}</span>
                      <span className="px-2 py-1 rounded bg-yellow-500/20 text-yellow-700">{t('dignity.friend')}</span>
                      <span className="px-2 py-1 rounded bg-orange-500/20 text-orange-700">{t('dignity.enemy')}</span>
                      <span className="px-2 py-1 rounded bg-red-500/20 text-red-700">{t('dignity.debilitated')}</span>
                    </div>
                  </div>

                  {/* Vimshopak Bala — from by_planet dict or vimshopak list */}
                  {(sodashvargaData.by_planet || sodashvargaData.vimshopak) && (
                    <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                      <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.vimshopakBala')}</h4>
                      <div className="space-y-3">
                        {(() => {
                          const items = Array.isArray(sodashvargaData.vimshopak) ? sodashvargaData.vimshopak
                            : Object.entries(sodashvargaData.by_planet || {}).map(([planet, data]: [string, any]) => ({
                                planet,
                                score: typeof data === 'number' ? data : data?.vimshopak_bala ?? data?.vimshopak ?? data?.score ?? 0,
                                percentage: data?.percentage,
                                strength: data?.strength,
                                dignities: data?.dignities,
                              }));
                          const strengthColors: Record<string, string> = {
                            Strong: 'text-green-600 bg-green-500/15',
                            Medium: 'text-yellow-600 bg-yellow-500/15',
                            Weak: 'text-red-500 bg-red-500/15',
                          };
                          const dignityLabels: Record<string, { label: string; color: string }> = {
                            exalted: { label: 'Ex', color: 'text-green-700 bg-green-500/20' },
                            own: { label: 'Own', color: 'text-blue-700 bg-blue-500/15' },
                            moolatrikona: { label: 'Moo', color: 'text-blue-700 bg-blue-500/15' },
                            friend: { label: 'Fr', color: 'text-yellow-700 bg-yellow-500/15' },
                            neutral: { label: 'Neu', color: 'text-gray-600 bg-gray-500/10' },
                            enemy: { label: 'En', color: 'text-orange-700 bg-orange-500/15' },
                            debilitated: { label: 'Deb', color: 'text-red-700 bg-red-500/15' },
                          };
                          return items.map((v: any) => (
                            <div key={v.planet} className="space-y-1">
                              <div className="flex items-center gap-3 text-sm">
                                <span className="w-12 text-sacred-brown font-medium">{v.planet?.slice(0, 3)}</span>
                                <div className="flex-1 bg-sacred-gold/10 rounded-full h-4">
                                  <div className="bg-sacred-gold rounded-full h-4 transition-all" style={{ width: `${Math.min(100, ((typeof v.score === 'number' ? v.score : 0) / 20) * 100)}%` }} />
                                </div>
                                <span className="w-16 text-right text-sacred-text-secondary text-xs">{typeof v.score === 'number' ? v.score.toFixed(1) : '?'} / 20</span>
                                {v.percentage != null && (
                                  <span className="w-12 text-right text-sacred-brown font-semibold text-xs">{v.percentage}%</span>
                                )}
                                {v.strength && (
                                  <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${strengthColors[v.strength] || 'text-gray-500 bg-gray-500/10'}`}>{v.strength}</span>
                                )}
                              </div>
                              {v.dignities && typeof v.dignities === 'object' && (
                                <div className="flex items-center gap-1 ml-[60px] flex-wrap">
                                  {Object.entries(v.dignities as Record<string, number>)
                                    .filter(([, count]) => (count as number) > 0)
                                    .map(([dignity, count]) => {
                                      const info = dignityLabels[dignity] || { label: dignity.slice(0, 3), color: 'text-gray-500 bg-gray-500/10' };
                                      return (
                                        <span key={dignity} className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${info.color}`}>
                                          {info.label}:{count as number}
                                        </span>
                                      );
                                    })}
                                </div>
                              )}
                            </div>
                          ));
                        })()}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">{t('common.noData')}</p>
              )}
            </div>
          </TabsContent>

          {/* ASPECTS TAB — API: aspects_on_planets (list), aspects_on_bhavas (dict), bhava_summary (list) */}
          <TabsContent value="aspects">
            <div className="space-y-6">
              {loadingAspects ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingAspects')}</span></div>
              ) : aspectsData ? (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Aspects on Planets */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.aspectsOnPlanets')}</h4>
                    <div className="space-y-3">
                      {(() => {
                        // Prefer planet_aspects_summary (per-planet with full detail), fallback to flat list
                        const summary = aspectsData.planet_aspects_summary;
                        if (summary && typeof summary === 'object' && !Array.isArray(summary)) {
                          const strengthBadge = (s: number) => {
                            const color = s >= 1.0 ? 'bg-sacred-gold/30 text-sacred-gold-dark' : s >= 0.75 ? 'bg-blue-500/20 text-blue-700' : s >= 0.5 ? 'bg-yellow-500/20 text-yellow-700' : 'bg-gray-500/15 text-gray-600';
                            return <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${color}`}>{s}</span>;
                          };
                          const typeBadge = (t_val: string) => {
                            const color = t_val === 'full' ? 'bg-sacred-gold/20 text-sacred-gold-dark' : 'bg-purple-500/15 text-purple-700';
                            return <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${color}`}>{t_val}</span>;
                          };
                          return Object.entries(summary).map(([planet, data]: [string, any]) => (
                            <div key={planet} className="bg-white/5 rounded-lg p-3 text-xs">
                              <div className="flex items-center justify-between mb-1">
                                <span className="font-semibold text-sacred-brown">{translatePlanet(planet, language)} <span className="text-sacred-text-secondary font-normal">({t('table.house')} {data.house})</span></span>
                                <span className="text-xs">
                                  <span className="text-green-500">B:{data.benefic_aspects || 0}</span>{' '}
                                  <span className="text-red-400">M:{data.malefic_aspects || 0}</span>
                                </span>
                              </div>
                              {data.aspected_by && Array.isArray(data.aspected_by) && data.aspected_by.length > 0 && (
                                <div className="mt-1.5 space-y-1">
                                  <p className="text-sacred-text-secondary font-medium mb-0.5">{t('table.aspectedBy')}:</p>
                                  {data.aspected_by.map((a: any, i: number) => (
                                    <div key={i} className="flex items-center gap-1.5 ml-2">
                                      <span className="text-sacred-brown font-medium">{translatePlanet(a.planet, language)}</span>
                                      {strengthBadge(a.strength)}
                                      <span className="text-sacred-text-secondary">{a.offset}th house</span>
                                      {a.type && typeBadge(a.type)}
                                    </div>
                                  ))}
                                </div>
                              )}
                              {data.aspects_to && Array.isArray(data.aspects_to) && data.aspects_to.length > 0 && (
                                <div className="mt-1.5 space-y-1">
                                  <p className="text-sacred-text-secondary font-medium mb-0.5">{t('kundli.aspects')}:</p>
                                  {data.aspects_to.map((a: any, i: number) => (
                                    <div key={i} className="flex items-center gap-1.5 ml-2">
                                      <span className="text-sacred-brown">H{a.house}</span>
                                      {strengthBadge(a.strength)}
                                      <span className="text-sacred-text-secondary">{a.offset}th</span>
                                      {a.type && typeBadge(a.type)}
                                      {a.planets_in_house && a.planets_in_house.length > 0 && (
                                        <span className="text-sacred-text-secondary">({a.planets_in_house.join(', ')})</span>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          ));
                        }
                        // Fallback: flat list format (aspects_on_planets or planet_aspects)
                        const flatList = aspectsData.aspects_on_planets || aspectsData.planet_aspects || [];
                        if (Array.isArray(flatList) && flatList.length > 0) {
                          return flatList.map((pa: any, idx: number) => (
                            <div key={pa.planet || pa.aspecting || idx} className="bg-white/5 rounded-lg p-3 text-xs">
                              <div className="flex items-center justify-between mb-1">
                                <span className="font-semibold text-sacred-brown">
                                  {translatePlanet(pa.aspecting || pa.planet, language)}
                                  {' '}<span className="text-sacred-text-secondary font-normal">({t('table.house')} {pa.house_from || pa.house})</span>
                                  {' \u2192 '}
                                  {pa.aspected && <span className="font-semibold">{translatePlanet(pa.aspected, language)}</span>}
                                </span>
                                <span className="flex items-center gap-1.5">
                                  {pa.strength != null && (
                                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${pa.strength >= 1.0 ? 'bg-sacred-gold/30 text-sacred-gold-dark' : pa.strength >= 0.75 ? 'bg-blue-500/20 text-blue-700' : pa.strength >= 0.5 ? 'bg-yellow-500/20 text-yellow-700' : 'bg-gray-500/15 text-gray-600'}`}>{pa.strength}</span>
                                  )}
                                  {pa.type && (
                                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${pa.type === 'full' ? 'bg-sacred-gold/20 text-sacred-gold-dark' : 'bg-purple-500/15 text-purple-700'}`}>{pa.type}</span>
                                  )}
                                </span>
                              </div>
                              {pa.offset != null && (
                                <p className="text-sacred-text-secondary">{pa.offset}th house aspect</p>
                              )}
                              {pa.aspected_by && (Array.isArray(pa.aspected_by) ? pa.aspected_by.length > 0 : true) && (
                                <p className="text-sacred-text-secondary">{t('table.aspectedBy')}: {Array.isArray(pa.aspected_by) ? pa.aspected_by.map((a: any) => typeof a === 'string' ? a : a.planet).join(', ') : String(pa.aspected_by)}</p>
                              )}
                            </div>
                          ));
                        }
                        return <p className="text-center text-sacred-text-secondary">{t('common.noData')}</p>;
                      })()}
                    </div>
                  </div>

                  {/* Aspects on Bhavas */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.aspectsOnBhavas')}</h4>
                    <table className="w-full text-xs">
                      <thead><tr className="bg-sacred-gold/10">
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.bhava')}</th>
                        <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.aspectedBy')}</th>
                        <th className="text-center p-1 text-sacred-gold-dark font-medium">Str</th>
                        <th className="text-center p-1 text-sacred-gold-dark font-medium">B</th>
                        <th className="text-center p-1 text-sacred-gold-dark font-medium">M</th>
                      </tr></thead>
                      <tbody>
                        {(() => {
                          const bhavas = aspectsData.bhava_summary || aspectsData.bhava_aspects;
                          // aspects_on_bhavas has per-house strength data: {house_str: [{planet, strength, offset, type}]}
                          const bhavaAspects = aspectsData.aspects_on_bhavas || {};
                          const getStrengths = (houseKey: string | number) => {
                            const entries = bhavaAspects[String(houseKey)] || [];
                            if (!Array.isArray(entries) || entries.length === 0) return null;
                            return entries.map((e: any) => e.strength).filter((s: any) => s != null);
                          };
                          const renderStrength = (strengths: number[] | null) => {
                            if (!strengths || strengths.length === 0) return '-';
                            return strengths.map((s, i) => (
                              <span key={i} className={`inline-block px-1 py-0.5 rounded text-[10px] font-semibold mr-0.5 ${s >= 1.0 ? 'bg-sacred-gold/30 text-sacred-gold-dark' : s >= 0.75 ? 'bg-blue-500/20 text-blue-700' : s >= 0.5 ? 'bg-yellow-500/20 text-yellow-700' : 'bg-gray-500/15 text-gray-600'}`}>{s}</span>
                            ));
                          };
                          if (Array.isArray(bhavas)) {
                            return bhavas.map((ba: any, i: number) => {
                              const houseNum = ba.house || ba.bhava || i + 1;
                              const strengths = getStrengths(houseNum);
                              return (
                                <tr key={houseNum} className="border-t border-sacred-gold/10">
                                  <td className="p-2 font-semibold text-sacred-brown">{houseNum}</td>
                                  <td className="p-2 text-sacred-text-secondary">{Array.isArray(ba.aspected_by) ? ba.aspected_by.join(', ') : (ba.aspected_by || '-')}</td>
                                  <td className="p-1 text-center">{renderStrength(strengths)}</td>
                                  <td className="p-1 text-center text-green-500">{ba.benefic || ba.benefic_count || ba.benefic_aspects || 0}</td>
                                  <td className="p-1 text-center text-red-400">{ba.malefic || ba.malefic_count || ba.malefic_aspects || 0}</td>
                                </tr>
                              );
                            });
                          }
                          // Dict format: {1: {aspected_by: [...], ...}, 2: ...}
                          return Object.entries(bhavas || {}).map(([bhava, data]: [string, any]) => {
                            const strengths = getStrengths(bhava);
                            return (
                              <tr key={bhava} className="border-t border-sacred-gold/10">
                                <td className="p-2 font-semibold text-sacred-brown">{bhava}</td>
                                <td className="p-2 text-sacred-text-secondary">{Array.isArray(data?.aspected_by) ? data.aspected_by.join(', ') : String(data?.aspected_by || '-')}</td>
                                <td className="p-1 text-center">{renderStrength(strengths)}</td>
                                <td className="p-1 text-center text-green-500">{data?.benefic || 0}</td>
                                <td className="p-1 text-center text-red-400">{data?.malefic || 0}</td>
                              </tr>
                            );
                          });
                        })()}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">{t('common.noData')}</p>
              )}
            </div>
          </TabsContent>

          {/* SADE SATI TAB */}
          <TabsContent value="sadesati">
            <div className="space-y-6">
              {loadingSadesati ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingSadeSati')}</span></div>
              ) : sadesatiData ? (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Sade Sati Phases */}
                  <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                    <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.lifelongSadeSati')}</h4>
                    <div className="max-h-[400px] overflow-y-auto space-y-2">
                      {(sadesatiData.phases || sadesatiData.sade_sati_phases || []).map((phase: any, i: number) => (
                        <div key={i} className={`p-3 rounded-lg text-xs ${phase.is_current ? 'bg-sacred-gold/20 border border-sacred-gold/40' : 'bg-white/5'}`}>
                          <div className="flex justify-between items-center">
                            <span className="font-semibold text-sacred-brown">{translateLabel(phase.phase || phase.name, language)}{phase.is_current ? ` (${t('common.current')})` : ''}</span>
                            <span className="text-sacred-text-secondary">{translateLabel(phase.type || 'Sade Sati', language)}</span>
                          </div>
                          <p className="text-sacred-text-secondary mt-1">{phase.start_date || phase.start} \u2192 {phase.end_date || phase.end}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Dhaiya & Panauti Phases */}
                  {(sadesatiData.dhaiya_phases || sadesatiData.small_panoti_phases) && (
                    <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                      <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.dhaiyaPanauti')}</h4>
                      <div className="max-h-[400px] overflow-y-auto space-y-2">
                        {[...(sadesatiData.dhaiya_phases || []), ...(sadesatiData.small_panoti_phases || [])].map((phase: any, i: number) => (
                          <div key={i} className={`p-3 rounded-lg text-xs ${phase.is_current ? 'bg-orange-500/20 border border-orange-500/30' : 'bg-white/5'}`}>
                            <div className="flex justify-between items-center">
                              <span className="font-semibold text-sacred-brown">{translateLabel(phase.phase || phase.name, language)}{phase.is_current ? ` (${t('common.active')})` : ''}</span>
                              <span className="text-sacred-text-secondary">{translateLabel(phase.type || 'Dhaiya', language)}</span>
                            </div>
                            <p className="text-sacred-text-secondary mt-1">{phase.start_date || phase.start} \u2192 {phase.end_date || phase.end}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Remedies */}
                  {sadesatiData.remedies && sadesatiData.remedies.length > 0 && (
                    <div className="lg:col-span-2 bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                      <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.remediesGemstone')}</h4>
                      <ul className="space-y-2">
                        {sadesatiData.remedies.map((r: string, i: number) => (
                          <li key={i} className="flex gap-2 text-sm text-sacred-text-secondary">
                            <Shield className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />
                            <span>{translateRemedy(r, language)}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickSadeSatiTab')}</p>
              )}
            </div>
          </TabsContent>
        </Tabs>

        <div className="mt-8 mb-16 text-center">
          <Button onClick={() => { setStep('form'); setResult(null); resetTabData(); }} variant="outline" className="border-cosmic-text-muted text-cosmic-text">
            {t('common.generateAnother')}
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
