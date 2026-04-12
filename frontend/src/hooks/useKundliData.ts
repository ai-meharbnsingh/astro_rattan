import { useState, useEffect, useCallback, useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import { isPuterAvailable, puterChatStream, VEDIC_SYSTEM_PROMPT } from '@/lib/puter-ai';
import { getHouseSignificance } from '@/components/kundli/kundli-utils';
import type { KundliFormData } from '@/components/kundli/KundliForm';
import type { PlanetData } from '@/components/InteractiveKundli';

export type SidePanelState = {
  type: 'planet' | 'house';
  planet?: PlanetData;
  house?: number;
  sign?: string;
  planets?: PlanetData[];
} | null;

export function useKundliData() {
  const { isAuthenticated } = useAuth();
  const { t, language } = useTranslation();
  const location = useLocation();
  const prefill = (location.state as { birthDate?: string; birthTime?: string; birthPlace?: string; loadKundliId?: string; clientId?: string; clientName?: string }) || {};

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
  const [varshphalYear, setVarshphalYear] = useState(() => new Date().getFullYear());
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
  const [westernAspectsData, setWesternAspectsData] = useState<any>(null);
  const [loadingWesternAspects, setLoadingWesternAspects] = useState(false);
  const [jaiminiData, setJaiminiData] = useState<any>(null);
  const [loadingJaimini, setLoadingJaimini] = useState(false);
  const [sadesatiData, setSadesatiData] = useState<any>(null);
  const [loadingSadesati, setLoadingSadesati] = useState(false);
  const [error, setError] = useState('');
  const [tabError, setTabError] = useState<string | null>(null);
  const [reportOpen, setReportOpen] = useState(false);
  const [summaryOpen, setSummaryOpen] = useState(false);
  const [jhoraOpen, setJhoraOpen] = useState(false);
  const [sidePanel, setSidePanel] = useState<SidePanelState>(null);

  const HOUSE_SIGNIFICANCE = getHouseSignificance(t);

  const handlePlanetClick = useCallback((planet: PlanetData) => {
    setSidePanel({ type: 'planet', planet });
  }, []);

  const handleHouseClick = useCallback((house: number, sign: string, planets: PlanetData[]) => {
    setSidePanel({ type: 'house', house, sign, planets });
  }, []);

  const resetTabData = useCallback(() => {
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
    setWesternAspectsData(null);
    setJaiminiData(null);
    setSadesatiData(null);
    setVarshphalData(null);
  }, []);

  // On mount: load existing kundlis if logged in, auto-open if loadKundliId passed
  const loadKundli = useCallback(async (kundli: any) => {
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
  }, [resetTabData]);

  useEffect(() => {
    if (!isAuthenticated) {
      setStep('form');
      return;
    }
    api.get('/api/kundli/list')
      .then((data: any) => {
        const list = Array.isArray(data) ? data : [];
        setSavedKundlis(list);
        // If navigated with a specific kundli to load, open it directly
        if (prefill.loadKundliId) {
          loadKundli({ id: prefill.loadKundliId });
        } else if (prefill.clientName) {
          // Pre-fill form with client data
          setFormData(prev => ({
            ...prev,
            name: prefill.clientName || prev.name,
            date: prefill.birthDate || prev.date,
            time: prefill.birthTime || prev.time,
            place: prefill.birthPlace || prev.place,
          }));
          setStep('form');
        } else {
          setStep('form');
        }
      })
      .catch(() => setStep('form'));
  }, [isAuthenticated, loadKundli, prefill.birthDate, prefill.birthPlace, prefill.birthTime, prefill.clientName, prefill.loadKundliId]);

  const fetchSavedKundlis = async () => {
    if (!isAuthenticated) return;
    try {
      const data = await api.get('/api/kundli');
      setSavedKundlis(data || []);
    } catch {
      setSavedKundlis([]);
    }
  };

  // --- Data fetching functions ---
  const fetchDosha = async () => {
    if (!result?.id || doshaData) return;
    setLoadingDosha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/dosha`, {});
      setDoshaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingDosha(false);
  };

  const fetchIogita = async () => {
    if (!result?.id || iogitaData) return;
    setLoadingIogita(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/iogita`, {});
      setIogitaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingIogita(false);
  };

  const fetchDasha = async () => {
    if (!result?.id || dashaData) return;
    setLoadingDasha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/dasha`, {});
      setDashaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingDasha(false);
  };

  const fetchAvakhada = async () => {
    if (!result?.id || avakhadaData) return;
    setLoadingAvakhada(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/avakhada`);
      setAvakhadaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingAvakhada(false);
  };

  const fetchExtendedDasha = async () => {
    if (!result?.id || extendedDashaData) return;
    setLoadingExtendedDasha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/extended-dasha`, {});
      if (data?.mahadasha) {
        setExtendedDashaData(data);
        // Auto-expand current mahadasha so user sees it immediately
        const currentMd = data.mahadasha.find((md: any) => md.is_current);
        if (currentMd) {
          setExpandedMahadasha(currentMd.planet);
        }
      } else {
        console.warn('Extended dasha response missing mahadasha:', data);
      }
    } catch (err) {
      console.error('Failed to fetch extended dasha:', err);
    }
    setLoadingExtendedDasha(false);
  };

  const fetchYogaDosha = async () => {
    if (!result?.id || yogaDoshaData) return;
    setLoadingYogaDosha(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/yogas-doshas`, {});
      setYogaDoshaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingYogaDosha(false);
  };

  const fetchDivisional = async (chartType?: string) => {
    if (!result?.id) return;
    const ct = chartType || selectedDivision;
    if (ct === 'Moon') {
      const planetsRaw = result.chart_data?.planets || {};
      const planetsArr = Array.isArray(planetsRaw) ? planetsRaw : Object.entries(planetsRaw).map(([name, data]: [string, any]) => ({ planet: name, ...data }));
      const moonPlanet = planetsArr.find((p: any) => p.planet === 'Moon');
      const shift = (moonPlanet?.house || 1) - 1;
      const moonPositions = planetsArr.map((p: any) => ({
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
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingDivisional(false);
  };

  const fetchAshtakvarga = async () => {
    if (!result?.id || ashtakvargaData) return;
    setLoadingAshtakvarga(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/ashtakvarga`, {});
      setAshtakvargaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingAshtakvarga(false);
  };

  const fetchShadbala = async () => {
    if (!result?.id || shadbalaData) return;
    setLoadingShadbala(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/shadbala`, {});
      setShadbalaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingShadbala(false);
  };

  const fetchTransit = async (customDate?: string, customTime?: string) => {
    if (!result?.id) return;
    if (!customDate && transitData) return;
    setLoadingTransit(true);
    setTransitHouseShift(0);
    try {
      const body: any = {};
      if (customDate) body.transit_date = customDate;
      if (customTime) body.transit_time = customTime;
      const data = await api.post(`/api/kundli/${result.id}/transits`, body);
      setTransitData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingTransit(false);
  };

  const fetchD10 = async () => {
    if (!result?.id || d10Data) return;
    setLoadingD10(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: 'D10' });
      setD10Data(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingD10(false);
  };

  const fetchVarshphal = async (year?: number) => {
    if (!result?.id || (!year && varshphalData)) return;
    let targetYear = year || varshphalYear;
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
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingVarshphal(false);
  };

  const fetchYogini = async () => {
    if (!result?.id || yoginiData) return;
    setLoadingYogini(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/yogini-dasha`);
      setYoginiData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingYogini(false);
  };

  const fetchKp = async () => {
    if (!result?.id || kpData) return;
    setLoadingKp(true);
    try {
      const data = await api.post(`/api/kundli/${result.id}/kp-analysis`, {});
      setKpData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingKp(false);
  };

  const fetchUpagrahas = async () => {
    if (!result?.id || upagrahasData) return;
    setLoadingUpagrahas(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/upagrahas`);
      setUpagrahasData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingUpagrahas(false);
  };

  const fetchSodashvarga = async () => {
    if (!result?.id || sodashvargaData) return;
    setLoadingSodashvarga(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/sodashvarga`);
      setSodashvargaData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingSodashvarga(false);
  };

  const fetchAspects = async () => {
    if (!result?.id || aspectsData) return;
    setLoadingAspects(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/aspects`);
      setAspectsData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingAspects(false);
  };

  const fetchWesternAspects = async () => {
    if (!result?.id || westernAspectsData) return;
    setLoadingWesternAspects(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/western-aspects`);
      setWesternAspectsData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingWesternAspects(false);
  };

  const fetchJaimini = async () => {
    if (!result?.id || jaiminiData) return;
    setLoadingJaimini(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/jaimini`);
      setJaiminiData(data);
    } catch (e: any) {
      console.error('Jaimini fetch error:', e);
    }
    setLoadingJaimini(false);
  };

  const fetchSadesati = async () => {
    if (!result?.id || sadesatiData) return;
    setLoadingSadesati(true);
    try {
      const data = await api.get(`/api/kundli/${result.id}/lifelong-sadesati`);
      setSadesatiData(data);
    } catch (e: any) { console.error(e); setTabError(e?.message || "Failed to load data"); }
    setLoadingSadesati(false);
  };

  // Auto-fetch core data when result loads (needed for Report tab)
  useEffect(() => {
    if (step === 'result' && result?.id) {
      fetchDasha();
      fetchDosha();
      fetchTransit();
      // Stagger the rest slightly
      setTimeout(() => { fetchExtendedDasha(); fetchAvakhada(); }, 500);
      setTimeout(() => { fetchYogaDosha(); fetchShadbala(); }, 1000);
      setTimeout(() => { fetchAshtakvarga(); fetchDivisional('D9'); }, 1500);
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

  const fetchPredictions = async (period: 'general' | 'daily' | 'monthly' | 'yearly' = 'general') => {
    if (!result?.id) return;
    setActivePredictionPeriod(period);
    if (predictionsData[period]) return;
    setLoadingPredictions(true);
    try {
      const data = await api.post('/api/ai/interpret', { kundli_id: result.id, prediction_type: period });
      setPredictionsData(prev => ({ ...prev, [period]: data }));
      setLoadingPredictions(false);
      return;
    } catch {
      // Backend failed — try Puter.js
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

  const handlePrashnaKundli = async () => {
    if (!isAuthenticated) {
      setError('Sign in is required to generate and save a kundli.');
      return;
    }
    setStep('generating');
    setError('');
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
        timezone_offset: -(new Date().getTimezoneOffset() / 60),
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
      const payload: any = {
        person_name: formData.name,
        birth_date: formData.date,
        birth_time: formData.time + ':00',
        birth_place: formData.place,
        latitude: formData.latitude,
        longitude: formData.longitude,
        timezone_offset: -(new Date().getTimezoneOffset() / 60),
      };
      if (formData.phone) payload.phone = formData.phone;
      if (formData.clientId) payload.client_id = formData.clientId;
      const data = await api.post('/api/kundli/generate', payload);
      setResult(data);
      resetTabData();
      setStep('result');
      // Refresh saved kundlis list (for Milan dropdown)
      try { const list = await api.get('/api/kundli/list'); setSavedKundlis(Array.isArray(list) ? list : []); } catch {}
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate kundli');
      setStep('form');
    }
  };

  // --- Computed values ---
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

  const planets = useMemo(() => {
    if (!result) return [];
    const planetsRaw = result.chart_data?.planets || {};
    const arr = Array.isArray(planetsRaw)
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
          nakshatra_pada: data?.nakshatra_pada || data?.pada || null,
          sign_degree: data?.sign_degree || 0,
          status: data?.status && !['Transiting', 'Entering', 'Leaving'].includes(data.status) ? data.status : calcDignity(name, data?.sign || ''),
          is_retrograde: data?.is_retrograde || data?.retrograde || false,
          is_combust: data?.is_combust || data?.combust || false,
          is_vargottama: data?.is_vargottama || data?.vargottama || false,
        }));

    // Inject Lagna
    const asc = result.chart_data?.ascendant;
    if (asc && !arr.some((p: any) => p.planet === 'Lagna')) {
      arr.unshift({
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
    return arr;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result]);

  const doshaDisplay = useMemo(() => {
    if (!doshaData) return null;
    return {
      mangal: doshaData.mangal_dosha || { has_dosha: false, severity: 'none', description: 'No data' },
      kaalsarp: doshaData.kaal_sarp_dosha || { has_dosha: false, severity: 'none', description: 'No data' },
      sadesati: doshaData.sade_sati || { has_sade_sati: false, phase: 'none', description: 'No data' },
    };
  }, [doshaData]);

  // Convenience helpers for tab components
  const changeDivision = (code: string) => {
    setSelectedDivision(code);
    setDivisionalData(null);
    fetchDivisional(code);
  };

  const refreshTransit = (date?: string, time?: string) => {
    setTransitData(null);
    fetchTransit(date, time);
  };

  const changeVarshphalYear = (yr: number) => {
    setVarshphalYear(yr);
    setVarshphalData(null);
    fetchVarshphal(yr);
  };

  const resetTransitFilters = () => {
    setTransitDate('');
    setTransitTime('');
    setTransitData(null);
    fetchTransit();
  };

  return {
    // Step
    step, setStep,
    // Form
    formData, setFormData,
    // Result
    result, setResult,
    // Saved
    savedKundlis,
    // Error
    error, tabError, setTabError,
    // Tab data & loading
    doshaData, loadingDosha,
    iogitaData, loadingIogita,
    dashaData, loadingDasha,
    extendedDashaData, loadingExtendedDasha,
    avakhadaData, loadingAvakhada,
    yogaDoshaData, loadingYogaDosha,
    divisionalData, loadingDivisional,
    ashtakvargaData, loadingAshtakvarga,
    shadbalaData, loadingShadbala,
    transitData, loadingTransit,
    d10Data, loadingD10,
    varshphalData, loadingVarshphal,
    yoginiData, loadingYogini,
    kpData, loadingKp,
    upagrahasData, loadingUpagrahas,
    sodashvargaData, loadingSodashvarga,
    aspectsData, loadingAspects,
    westernAspectsData, loadingWesternAspects,
    jaiminiData, loadingJaimini,
    sadesatiData, loadingSadesati,
    predictionsData, loadingPredictions,
    activePredictionPeriod,
    // UI state
    selectedDivision, setSelectedDivision,
    expandedMahadasha, setExpandedMahadasha,
    expandedAntardasha, setExpandedAntardasha,
    transitHouseShift, setTransitHouseShift,
    reportLagnaShift, setReportLagnaShift,
    reportMoonShift, setReportMoonShift,
    reportGocharShift, setReportGocharShift,
    transitDate, setTransitDate,
    transitTime, setTransitTime,
    varshphalYear,
    sidePanel, setSidePanel,
    reportOpen, setReportOpen,
    summaryOpen, setSummaryOpen,
    jhoraOpen, setJhoraOpen,
    // Fetch functions
    fetchDosha, fetchIogita, fetchDasha, fetchAvakhada,
    fetchExtendedDasha, fetchYogaDosha, fetchDivisional,
    fetchAshtakvarga, fetchShadbala, fetchTransit,
    fetchD10, fetchVarshphal, fetchYogini, fetchKp,
    fetchUpagrahas, fetchSodashvarga, fetchAspects,
    fetchWesternAspects, fetchJaimini, fetchSadesati,
    fetchPredictions, fetchSavedKundlis,
    // Convenience
    changeDivision, refreshTransit, changeVarshphalYear, resetTransitFilters,
    // Handlers
    handlePlanetClick, handleHouseClick,
    handleGenerate, handlePrashnaKundli,
    loadKundli, resetTabData,
    // Computed
    planets, doshaDisplay,
    HOUSE_SIGNIFICANCE,
    // i18n
    t, language,
  };
}
