import { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, Calendar, Clock, MapPin, User, ChevronRight, ChevronDown, Download, Share2, FileText, Heart, Briefcase, Activity, ArrowLeft, Loader2, X, CheckCircle, AlertTriangle, Shield } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';

export default function KundliGenerator() {
  const { isAuthenticated } = useAuth();
  const { t } = useTranslation();
  const location = useLocation();
  const prefill = (location.state as { birthDate?: string; birthTime?: string; birthPlace?: string }) || {};

  const [step, setStep] = useState<'loading' | 'list' | 'form' | 'generating' | 'result'>('loading');
  const [formData, setFormData] = useState({
    name: '',
    date: prefill.birthDate || '',
    time: prefill.birthTime || '',
    place: prefill.birthPlace || '',
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
  const [predictionsData, setPredictionsData] = useState<any>(null);
  const [loadingPredictions, setLoadingPredictions] = useState(false);
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
  const [error, setError] = useState('');
  const [sidePanel, setSidePanel] = useState<{
    type: 'planet' | 'house';
    planet?: PlanetData;
    house?: number;
    sign?: string;
    planets?: PlanetData[];
  } | null>(null);

  const HOUSE_SIGNIFICANCE: Record<number, string> = {
    1: t('kundli.house1'),
    2: t('kundli.house2'),
    3: t('kundli.house3'),
    4: t('kundli.house4'),
    5: t('kundli.house5'),
    6: t('kundli.house6'),
    7: t('kundli.house7'),
    8: t('kundli.house8'),
    9: t('kundli.house9'),
    10: t('kundli.house10'),
    11: t('kundli.house11'),
    12: t('kundli.house12'),
  };

  const PLANET_ASPECTS: Record<string, number[]> = {
    Sun: [7], Moon: [7], Mercury: [7], Venus: [7],
    Mars: [4, 7, 8], Jupiter: [5, 7, 9], Saturn: [3, 7, 10],
    Rahu: [5, 7, 9], Ketu: [5, 7, 9],
  };

  // Sign → Lord mapping
  const SIGN_LORD: Record<string, string> = {
    Aries: 'Mars', Taurus: 'Venus', Gemini: 'Mercury', Cancer: 'Moon',
    Leo: 'Sun', Virgo: 'Mercury', Libra: 'Venus', Scorpio: 'Mars',
    Sagittarius: 'Jupiter', Capricorn: 'Saturn', Aquarius: 'Saturn', Pisces: 'Jupiter',
  };

  // Sign → Element
  const SIGN_ELEMENT: Record<string, string> = {
    Aries: 'Fire', Leo: 'Fire', Sagittarius: 'Fire',
    Taurus: 'Earth', Virgo: 'Earth', Capricorn: 'Earth',
    Gemini: 'Air', Libra: 'Air', Aquarius: 'Air',
    Cancer: 'Water', Scorpio: 'Water', Pisces: 'Water',
  };

  // Sign → Sign Type
  const SIGN_TYPE: Record<string, string> = {
    Aries: 'Moveable', Cancer: 'Moveable', Libra: 'Moveable', Capricorn: 'Moveable',
    Taurus: 'Fixed', Leo: 'Fixed', Scorpio: 'Fixed', Aquarius: 'Fixed',
    Gemini: 'Dual', Virgo: 'Dual', Sagittarius: 'Dual', Pisces: 'Dual',
  };

  // Planet nature
  const PLANET_NATURE: Record<string, string> = {
    Sun: 'Malefic', Moon: 'Benefic', Mars: 'Malefic', Mercury: 'Benefic',
    Jupiter: 'Benefic', Venus: 'Benefic', Saturn: 'Malefic', Rahu: 'Malefic', Ketu: 'Malefic',
  };

  // Dignity calculation
  const getDignity = (planet: string, sign: string): string => {
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
    const d = dignityMap[planet];
    if (!d) return t('kundli.neutral');
    if (d.exalted.includes(sign)) return t('kundli.exalted');
    if (d.debilitated.includes(sign)) return t('kundli.debilitated');
    if (d.own.includes(sign)) return t('kundli.ownSign');
    return t('kundli.neutral');
  };

  const handlePlanetClick = useCallback((planet: PlanetData) => {
    setSidePanel({ type: 'planet', planet });
  }, []);

  const handleHouseClick = useCallback((house: number, sign: string, planets: PlanetData[]) => {
    setSidePanel({ type: 'house', house, sign, planets });
  }, []);

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
        gender: 'male',
      });
      setDoshaData(null);
      setIogitaData(null);
      setDashaData(null);
      setPredictionsData(null);
      setAvakhadaData(null);
      setExtendedDashaData(null);
      setYogaDoshaData(null);
      setDivisionalData(null);
      setAshtakvargaData(null);
      setShadbalaData(null);
      setStep('result');
    } catch {
      setError('Failed to load kundli');
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

  // Fetch AI predictions
  const fetchPredictions = async () => {
    if (!result?.id || predictionsData) return;
    setLoadingPredictions(true);
    try {
      const data = await api.post('/api/ai/interpret', { kundli_id: result.id });
      setPredictionsData(data);
    } catch { /* fallback handled in UI */ }
    setLoadingPredictions(false);
  };

  // Prashna Kundli — generate for current moment
  const handlePrashnaKundli = async () => {
    if (!isAuthenticated) {
      setError('Sign in is required to generate and save a kundli.');
      return;
    }
    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:00`;
    setFormData({
      name: `Prashna ${dateStr}`,
      date: dateStr,
      time: `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`,
      place: 'Delhi',
      gender: 'male',
    });
    setStep('generating');
    setError('');
    try {
      const data = await api.post('/api/kundli/generate', {
        person_name: `Prashna ${dateStr}`,
        birth_date: dateStr,
        birth_time: timeStr,
        birth_place: 'Delhi',
        latitude: 28.6139,
        longitude: 77.2090,
        timezone_offset: 5.5,
      });
      setResult(data);
      setDoshaData(null);
      setIogitaData(null);
      setDashaData(null);
      setPredictionsData(null);
      setAvakhadaData(null);
      setExtendedDashaData(null);
      setYogaDoshaData(null);
      setDivisionalData(null);
      setAshtakvargaData(null);
      setShadbalaData(null);
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
        latitude: 28.6139,
        longitude: 77.2090,
        timezone_offset: 5.5,
      });
      setResult(data);
      setDoshaData(null);
      setIogitaData(null);
      setDashaData(null);
      setPredictionsData(null);
      setAvakhadaData(null);
      setExtendedDashaData(null);
      setYogaDoshaData(null);
      setDivisionalData(null);
      setAshtakvargaData(null);
      setShadbalaData(null);
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

  // --- MY KUNDLIS LIST ---
  if (step === 'list') {
    return (
      <div className="max-w-2xl mx-auto py-24 px-4 bg-transparent">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
            <Sparkles className="w-8 h-8 text-[#1a1a2e]" />
          </div>
          <h3 className="text-2xl font-display font-bold text-sacred-brown mb-2">My Kundlis</h3>
          <p className="text-sacred-text-secondary">Your saved birth charts</p>
        </div>
        <div className="space-y-3 mb-6">
          {savedKundlis.map((k: any) => (
            <button key={k.id} onClick={() => loadKundli(k)}
              className="w-full text-left p-4 bg-sacred-cream rounded-xl border border-sacred-gold/20 hover:border-sacred-gold/50 transition-colors">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-display font-semibold text-sacred-brown">{k.person_name}</h4>
                  <p className="text-sm text-sacred-text-secondary">{k.birth_date} | {k.birth_time} | {k.birth_place}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-sacred-gold" />
              </div>
            </button>
          ))}
        </div>
        <Button onClick={() => setStep('form')} className="w-full btn-sacred">
          <Sparkles className="w-5 h-5 mr-2" />Generate New Kundli
        </Button>
        <Button onClick={handlePrashnaKundli} variant="outline" className="w-full mt-3 border-sacred-gold/50 text-sacred-brown hover:bg-sacred-gold/10">
          <Clock className="w-5 h-5 mr-2 text-sacred-gold" />{t('kundli.prashnaKundli')}
          <span className="ml-2 text-xs text-sacred-text-secondary">{t('kundli.prashnaSubtitle')}</span>
        </Button>
      </div>
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

    // Dosha display data
    const doshaDisplay = doshaData ? {
      mangal: doshaData.mangal_dosha || { has_dosha: false, severity: 'none', description: 'No data' },
      kaalsarp: doshaData.kaal_sarp_dosha || { has_dosha: false, severity: 'none', description: 'No data' },
      sadesati: doshaData.sade_sati || { has_sade_sati: false, phase: 'none', description: 'No data' },
    } : null;

    return (
      <div className="max-w-4xl mx-auto py-24 px-4 bg-transparent">
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
            <Button size="sm" className="btn-sacred">
              <Download className="w-4 h-4 mr-1" />Download
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
            <Button variant="outline" className="border-sacred-gold text-sacred-gold-dark">  {t('kundli.viewReports')}</Button>
          </div>
          <div className="grid grid-cols-4 gap-3">
            {[
              { icon: FileText, name: 'Complete Analysis', price: '₹999' },
              { icon: Heart, name: 'Marriage', price: '₹799' },
              { icon: Briefcase, name: 'Career', price: '₹799' },
              { icon: Activity, name: 'Health', price: '₹699' },
            ].map(({ icon: Icon, name, price }) => (
              <button key={name} className="bg-cosmic-card/60 rounded-xl p-3 border border-sacred-gold/20 hover:border-sacred-gold/50 transition-colors text-left">
                <Icon className="w-5 h-5 text-sacred-gold mb-2" />
                <p className="text-sm font-medium text-sacred-brown">{name}</p>
                <p className="text-xs text-sacred-gold-dark">{price}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Tabs: Planets | Dosha | io-gita | Dasha */}
        <Tabs defaultValue="planets" className="w-full">
          <TabsList className="mb-6 bg-sacred-cream flex-wrap">
            <TabsTrigger value="planets">  {t('kundli.planets')}</TabsTrigger>
            <TabsTrigger value="details">{t('kundli.details')}</TabsTrigger>
            <TabsTrigger value="lordships">{t('kundli.lordships')}</TabsTrigger>
            <TabsTrigger value="dosha" onClick={fetchDosha}>  {t('kundli.dosha')}</TabsTrigger>
            <TabsTrigger value="iogita" onClick={fetchIogita}>io-gita</TabsTrigger>
            <TabsTrigger value="dasha" onClick={() => { fetchDasha(); fetchExtendedDasha(); }}>  {t('kundli.dasha')}</TabsTrigger>
            <TabsTrigger value="divisional" onClick={() => fetchDivisional()}>{t('kundli.divisional')}</TabsTrigger>
            <TabsTrigger value="ashtakvarga" onClick={fetchAshtakvarga}>{t('kundli.ashtakvarga')}</TabsTrigger>
            <TabsTrigger value="shadbala" onClick={fetchShadbala}>{t('kundli.shadbala')}</TabsTrigger>
            <TabsTrigger value="avakhada" onClick={fetchAvakhada}>{t('avakhada.title')}</TabsTrigger>
            <TabsTrigger value="yoga-dosha" onClick={fetchYogaDosha}>{t('yoga.title').split(' ')[0]}</TabsTrigger>
            <TabsTrigger value="predictions" onClick={fetchPredictions}>{t('kundli.predictions')}</TabsTrigger>
          </TabsList>

          {/* PLANETS TAB - Interactive Kundli Chart + Side Panel */}
          <TabsContent value="planets">
            <div className="flex flex-col xl:flex-row gap-8">
              {/* Interactive Chart — full width on mobile, large on desktop */}
              <div className="w-full xl:w-[600px] xl:flex-shrink-0 flex justify-center">
                <InteractiveKundli
                  chartData={{ planets, houses: result.chart_data?.houses } as ChartData}
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
                          : `{t('kundli.houseDetails')}`}
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
                              <p className="text-xs text-sacred-text-secondary">  {t('kundli.sign')}</p>
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
                            <p className="text-xs text-sacred-text-secondary">  {t('kundli.houseNumber')}</p>
                            <p className="font-semibold text-sacred-brown">{sidePanel.house}</p>
                          </div>
                          <div className="bg-cosmic-card/60 rounded-lg p-3">
                            <p className="text-xs text-sacred-text-secondary">  {t('kundli.sign')}</p>
                            <p className="font-semibold text-sacred-brown">{sidePanel.sign}</p>
                          </div>
                        </div>
                        <div className="bg-cosmic-card/60 rounded-lg p-3">
                          <p className="text-xs text-sacred-text-secondary">  {t('kundli.significance')}</p>
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
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Planet</th>
                        <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">  {t('kundli.sign')}</th>
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

          {/* DETAILS TAB — Birth Details Table */}
          <TabsContent value="details">
            <div className="space-y-4">
              <h4 className="font-sacred text-lg font-bold text-[#1a1a2e]">{t('kundli.birthDetailsTable')}</h4>
              <div className="overflow-x-auto rounded-xl border" style={{ borderColor: 'rgba(139,115,85,0.2)' }}>
                <table className="w-full text-sm">
                  <thead style={{ backgroundColor: '#E8E0D4' }}>
                    <tr>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>Planet</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.sign')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.degree')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.nakshatra')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.house')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.dignity')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.signType')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.element')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.nature')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.retrograde')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {planets.map((p: any, idx: number) => {
                      const dignity = getDignity(p.planet, p.sign);
                      const signType = SIGN_TYPE[p.sign] || '—';
                      const element = SIGN_ELEMENT[p.sign] || '—';
                      const nature = PLANET_NATURE[p.planet] || '—';
                      const isRetro = (p.status || '').toLowerCase().includes('retrograde') || (p.status || '').toLowerCase().includes(' r');
                      const dignityColor = dignity === t('kundli.exalted') ? '#16a34a' : dignity === t('kundli.debilitated') ? '#dc2626' : dignity === t('kundli.ownSign') ? '#2563eb' : '#8B7355';
                      const nakshatraParts = (p.nakshatra || '').split(' Pada ');
                      const nakshatraName = nakshatraParts[0] || p.nakshatra || '—';
                      const pada = nakshatraParts[1] || '—';

                      return (
                        <tr key={idx} className="border-t" style={{ borderColor: 'rgba(139,115,85,0.2)', backgroundColor: idx % 2 === 0 ? '#F5F0E8' : '#FDFBF7' }}>
                          <td className="p-3 font-medium" style={{ color: '#1a1a2e', fontFamily: 'serif' }}>{p.planet}</td>
                          <td className="p-3" style={{ color: '#1a1a2e' }}>{p.sign}</td>
                          <td className="p-3" style={{ color: '#1a1a2e' }}>{p.sign_degree != null ? `${Number(p.sign_degree).toFixed(2)}°` : '—'}</td>
                          <td className="p-3" style={{ color: '#1a1a2e' }}>{nakshatraName}{pada !== '—' ? ` (${t('kundli.pada')} ${pada})` : ''}</td>
                          <td className="p-3" style={{ color: '#1a1a2e' }}>{p.house}</td>
                          <td className="p-3 font-medium" style={{ color: dignityColor }}>{dignity}</td>
                          <td className="p-3" style={{ color: '#8B7355' }}>{signType}</td>
                          <td className="p-3" style={{ color: '#8B7355' }}>{element}</td>
                          <td className="p-3">
                            <span className={`text-xs px-2 py-0.5 rounded-full ${nature === 'Benefic' || nature === t('kundli.benefic') ? 'bg-green-500/15 text-green-600' : 'bg-red-500/15 text-red-600'}`}>
                              {nature}
                            </span>
                          </td>
                          <td className="p-3" style={{ color: isRetro ? '#dc2626' : '#8B7355' }}>
                            {isRetro ? `${t('common.yes')} ℞` : t('common.no')}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </TabsContent>

          {/* LORDSHIPS TAB — House Lordships */}
          <TabsContent value="lordships">
            <div className="space-y-4">
              <h4 className="font-sacred text-lg font-bold text-[#1a1a2e]">{t('kundli.houseLordships')}</h4>
              <div className="overflow-x-auto rounded-xl border" style={{ borderColor: 'rgba(139,115,85,0.2)' }}>
                <table className="w-full text-sm">
                  <thead style={{ backgroundColor: '#E8E0D4' }}>
                    <tr>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.house')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.sign')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.lord')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.placedIn')}</th>
                      <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.significance')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Array.from({ length: 12 }, (_, i) => {
                      const houseNum = i + 1;
                      const houses = result.chart_data?.houses || {};
                      // Houses can be an array or object
                      const houseData = Array.isArray(houses) ? houses[i] : houses[houseNum] || houses[String(houseNum)];
                      const houseSign = houseData?.sign || (Array.isArray(houses) ? houseData : '—');
                      const signName = typeof houseSign === 'string' ? houseSign : '—';
                      const lord = SIGN_LORD[signName] || '—';

                      // Find which house the lord sits in
                      const lordPlanet = planets.find((p: any) => p.planet === lord);
                      const lordPlacedIn = lordPlanet ? `House ${lordPlanet.house}` : '—';

                      return (
                        <tr key={houseNum} className="border-t" style={{ borderColor: 'rgba(139,115,85,0.2)', backgroundColor: houseNum % 2 === 1 ? '#F5F0E8' : '#FDFBF7' }}>
                          <td className="p-3 font-medium" style={{ color: '#1a1a2e', fontFamily: 'serif' }}>{houseNum}</td>
                          <td className="p-3" style={{ color: '#1a1a2e' }}>{signName}</td>
                          <td className="p-3 font-medium" style={{ color: '#B8860B' }}>{lord}</td>
                          <td className="p-3" style={{ color: '#1a1a2e' }}>{lordPlacedIn}</td>
                          <td className="p-3" style={{ color: '#8B7355' }}>{HOUSE_SIGNIFICANCE[houseNum] || '—'}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </TabsContent>

          {/* DOSHA TAB — wired to real API */}
          <TabsContent value="dosha">
            {loadingDosha ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Analyzing doshas...</span></div>
            ) : doshaDisplay ? (
              <div className="grid gap-4">
                <div className={`bg-sacred-cream rounded-xl p-4 border ${doshaDisplay.mangal.has_dosha ? 'border-red-500/30' : 'border-green-500/30'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">Mangal Dosha</h4>
                    <span className={`text-xs px-2 py-1 rounded-full ${doshaDisplay.mangal.has_dosha ? 'bg-red-900/200/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                      {doshaDisplay.mangal.has_dosha ? `Present (${doshaDisplay.mangal.severity})` : 'Not Present'}
                    </span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.mangal.description}</p>
                </div>
                <div className={`bg-sacred-cream rounded-xl p-4 border ${doshaDisplay.kaalsarp.has_dosha ? 'border-red-500/30' : 'border-green-500/30'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">Kaal Sarp Dosha</h4>
                    <span className={`text-xs px-2 py-1 rounded-full ${doshaDisplay.kaalsarp.has_dosha ? 'bg-red-900/200/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                      {doshaDisplay.kaalsarp.has_dosha ? 'Present' : 'Not Present'}
                    </span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.kaalsarp.description}</p>
                </div>
                <div className={`bg-sacred-cream rounded-xl p-4 border ${doshaDisplay.sadesati.has_sade_sati ? 'border-orange-200' : 'border-green-500/30'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-semibold text-sacred-brown">Shani Sade Sati</h4>
                    <span className={`text-xs px-2 py-1 rounded-full ${doshaDisplay.sadesati.has_sade_sati ? 'bg-orange-100 text-orange-600' : 'bg-green-500/20 text-green-400'}`}>
                      {doshaDisplay.sadesati.has_sade_sati ? `Active — ${doshaDisplay.sadesati.phase}` : 'Not Active'}
                    </span>
                  </div>
                  <p className="text-sm text-sacred-text-secondary">{doshaDisplay.sadesati.description}</p>
                </div>
              </div>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the Dosha tab to load analysis</p>
            )}
          </TabsContent>

          {/* IO-GITA TAB — wired to real API */}
          <TabsContent value="iogita">
            {loadingIogita ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Running io-gita attractor analysis...</span></div>
            ) : iogitaData?.basin ? (
              <div className="space-y-6">
                {/* Basin card */}
                <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-2xl p-6 border border-sacred-gold/30">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-12 h-12 rounded-full bg-sacred-gold/20 flex items-center justify-center">
                      <Sparkles className="w-6 h-6 text-sacred-gold" />
                    </div>
                    <div>
                      <h4 className="font-display font-bold text-xl text-sacred-brown">{iogitaData.basin.name}</h4>
                      <p className="text-sacred-gold-dark text-lg">{iogitaData.basin.hindi}</p>
                    </div>
                  </div>
                  <p className="text-sacred-text-secondary mb-4">{iogitaData.basin.description}</p>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="bg-cosmic-card/60 rounded-lg p-3">
                      <p className="text-sacred-text-secondary">Escape Possible</p>
                      <p className="font-semibold text-sacred-brown">{iogitaData.basin.escape_possible ? 'Yes — phase transition likely' : 'No — basin is stable'}</p>
                    </div>
                    <div className="bg-cosmic-card/60 rounded-lg p-3">
                      <p className="text-sacred-text-secondary">Trajectory Steps</p>
                      <p className="font-semibold text-sacred-brown">{iogitaData.basin.trajectory_steps} steps</p>
                    </div>
                  </div>
                </div>

                {/* Top atoms */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Dominant Atoms (Top 3)</h4>
                  <div className="space-y-3">
                    {(iogitaData.basin.top_3_atoms || []).map(([name, val]: [string, number]) => (
                      <div key={name} className="flex items-center gap-3">
                        <span className="w-20 text-sm font-medium text-sacred-brown">{name}</span>
                        <div className="flex-1 bg-sacred-gold/10 rounded-full h-4 overflow-hidden">
                          <div className="bg-gradient-to-r from-sacred-gold to-sacred-saffron h-full rounded-full transition-all" style={{ width: `${Math.abs(val) * 100}%` }} />
                        </div>
                        <span className="text-sm text-sacred-gold-dark w-14 text-right">{val.toFixed(3)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Suppressed atom */}
                {iogitaData.basin.top_negative && (
                  <div className="bg-red-900/20 rounded-xl p-5 border border-red-500/30">
                    <h4 className="font-display font-semibold text-red-700 mb-2">Most Suppressed Force</h4>
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-medium text-red-400">{iogitaData.basin.top_negative[0]}</span>
                      <div className="flex-1 bg-red-900/200/20 rounded-full h-3 overflow-hidden">
                        <div className="bg-red-400 h-full rounded-full" style={{ width: `${Math.abs(iogitaData.basin.top_negative[1]) * 100}%` }} />
                      </div>
                      <span className="text-sm text-red-400">{iogitaData.basin.top_negative[1].toFixed(3)}</span>
                    </div>
                  </div>
                )}

                {/* Warning + escape */}
                <div className="bg-amber-50 rounded-xl p-5 border border-amber-200">
                  <h4 className="font-display font-semibold text-amber-700 mb-2">Warning</h4>
                  <p className="text-sm text-amber-600">{iogitaData.basin.warning}</p>
                </div>
                <div className="bg-blue-50 rounded-xl p-5 border border-blue-200">
                  <h4 className="font-display font-semibold text-blue-700 mb-2">Escape Trigger</h4>
                  <p className="text-sm text-blue-600">{iogitaData.basin.escape_trigger}</p>
                </div>

                {/* io-gita insight */}
                {iogitaData.iogita_insight && (
                  <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                    <h4 className="font-display font-semibold text-sacred-brown mb-2">io-gita Combined Insight</h4>
                    <p className="text-sm text-sacred-text-secondary leading-relaxed">{iogitaData.iogita_insight}</p>
                  </div>
                )}
              </div>
            ) : iogitaData ? (
              <p className="text-center text-sacred-text-secondary py-8">io-gita analysis returned partial data. Try again.</p>
            ) : (
              <p className="text-center text-sacred-text-secondary py-8">Click the io-gita tab to run attractor analysis</p>
            )}
          </TabsContent>

          {/* DASHA TAB */}
          {/* DASHA TAB — Extended with Mahadasha -> Antardasha -> Pratyantar */}
          <TabsContent value="dasha">
            {(loadingDasha || loadingExtendedDasha) ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Calculating Vimshottari Dasha...</span></div>
            ) : extendedDashaData ? (
              <div className="space-y-4">
                {/* Current period summary */}
                <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold/10 rounded-xl p-4 border border-sacred-gold/20">
                  <p className="text-sm text-sacred-text-secondary">{t('dasha.current')} {t('dasha.mahadasha')}</p>
                  <p className="text-xl font-display font-bold" style={{ color: '#B8860B' }}>{extendedDashaData.current_dasha} {t('dasha.mahadasha')}</p>
                  <div className="flex gap-4 mt-1">
                    {extendedDashaData.current_antardasha && extendedDashaData.current_antardasha !== 'Unknown' && (
                      <p className="text-sm text-sacred-gold-dark">{t('dasha.antardasha')}: {extendedDashaData.current_antardasha}</p>
                    )}
                    {extendedDashaData.current_pratyantar && extendedDashaData.current_pratyantar !== 'Unknown' && (
                      <p className="text-sm text-sacred-text-secondary">{t('dasha.pratyantar')}: {extendedDashaData.current_pratyantar}</p>
                    )}
                  </div>
                </div>

                {/* Expandable Mahadasha list */}
                <div className="space-y-2">
                  {(extendedDashaData.mahadasha || []).map((md: any) => (
                    <div key={md.planet} className={`rounded-xl border overflow-hidden ${md.is_current ? 'border-[#B8860B]/50' : 'border-sacred-gold/20'}`}>
                      {/* Mahadasha header */}
                      <button
                        onClick={() => setExpandedMahadasha(expandedMahadasha === md.planet ? null : md.planet)}
                        className={`w-full flex items-center justify-between p-4 transition-colors ${md.is_current ? 'bg-[#B8860B]/10' : 'bg-sacred-cream hover:bg-sacred-gold/5'}`}
                      >
                        <div className="flex items-center gap-3">
                          <ChevronDown className={`w-4 h-4 text-sacred-gold-dark transition-transform ${expandedMahadasha === md.planet ? 'rotate-180' : ''}`} />
                          <span className={`font-display font-semibold ${md.is_current ? 'text-[#B8860B]' : 'text-sacred-brown'}`}>
                            {md.planet} {t('dasha.mahadasha')}
                          </span>
                          {md.is_current && <span className="text-xs px-2 py-0.5 rounded-full bg-[#B8860B]/20 text-[#B8860B] font-medium">{t('dasha.current')}</span>}
                        </div>
                        <div className="text-right text-sm text-sacred-text-secondary">
                          <span>{md.start} — {md.end}</span>
                          <span className="ml-2 text-sacred-gold-dark">({md.years}y)</span>
                        </div>
                      </button>

                      {/* Antardasha list (expanded) */}
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
                                    {ad.planet} {t('dasha.antardasha')}
                                  </span>
                                  {ad.is_current && <span className="text-xs px-1.5 py-0.5 rounded-full bg-[#B8860B]/15 text-[#B8860B]">{t('dasha.current')}</span>}
                                </div>
                                <span className="text-sacred-text-secondary">{ad.start} — {ad.end}</span>
                              </button>

                              {/* Pratyantar list (expanded) */}
                              {expandedAntardasha === `${md.planet}-${ad.planet}` && ad.pratyantar && ad.pratyantar.length > 0 && (
                                <div className="bg-sacred-cream/50 border-t border-sacred-gold/10">
                                  {ad.pratyantar.map((pt: any, idx: number) => (
                                    <div
                                      key={idx}
                                      className={`flex items-center justify-between px-10 py-2 text-xs ${pt.is_current ? 'bg-[#B8860B]/5' : ''}`}
                                    >
                                      <span className={`${pt.is_current ? 'text-[#B8860B] font-semibold' : 'text-sacred-text-secondary'}`}>
                                        {pt.planet} {t('dasha.pratyantar')}
                                        {pt.is_current && <span className="ml-1 text-[#B8860B]">*</span>}
                                      </span>
                                      <span className="text-sacred-text-secondary">{pt.start} — {pt.end}</span>
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
              /* Fallback to simple table if extended data failed */
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
                  {[
                    { code: 'D1', name: 'Rashi (D1)' },
                    { code: 'D2', name: 'Hora (D2)' },
                    { code: 'D3', name: 'Drekkana (D3)' },
                    { code: 'D4', name: 'Chaturthamsha (D4)' },
                    { code: 'D7', name: 'Saptamsha (D7)' },
                    { code: 'D9', name: 'Navamsha (D9)' },
                    { code: 'D10', name: 'Dashamsha (D10)' },
                    { code: 'D12', name: 'Dwadashamsha (D12)' },
                    { code: 'D16', name: 'Shodashamsha (D16)' },
                    { code: 'D20', name: 'Vimshamsha (D20)' },
                    { code: 'D24', name: 'Chaturvimshamsha (D24)' },
                    { code: 'D27', name: 'Bhamsha (D27)' },
                    { code: 'D30', name: 'Trimshamsha (D30)' },
                    { code: 'D40', name: 'Khavedamsha (D40)' },
                    { code: 'D45', name: 'Akshavedamsha (D45)' },
                    { code: 'D60', name: 'Shashtiamsha (D60)' },
                  ].map((c) => (
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
                    <p className="text-sm text-sacred-text-secondary">Division: {divisionalData.division}</p>
                  </div>

                  {/* Divisional chart using InteractiveKundli */}
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

                  {/* Planet positions table */}
                  <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
                    <table className="w-full">
                      <thead className="bg-sacred-cream">
                        <tr>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">Planet</th>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('kundli.sign')}</th>
                          <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('kundli.degree')}</th>
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
                <span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingAshtakvarga')}</span>
              </div>
            ) : ashtakvargaData ? (
              <div className="space-y-6">
                {/* SAV Bar Chart */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('kundli.sarvashtakvarga')}</h4>
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
                                backgroundColor: isStrong ? '#B8860B' : '#8B7355',
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
                      <span>{t('kundli.strong')} (&ge;28)</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: '#8B7355' }} />
                      <span>{t('kundli.weak')} (&lt;28)</span>
                    </div>
                  </div>
                </div>

                {/* BAV Table */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('kundli.bhinnashtakvarga')}</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-sacred-gold/20">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Planet</th>
                          {['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'].map((s) => (
                            <th key={s} className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{s}</th>
                          ))}
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.total')}</th>
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
                <span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingShadbala')}</span>
              </div>
            ) : shadbalaData?.planets ? (
              <div className="space-y-6">
                {/* Summary bar chart: Total vs Required */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('kundli.shadbalaTitle')}</h4>
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
                            {/* Required marker */}
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

                {/* Detailed breakdown table */}
                <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
                  <h4 className="font-display font-semibold text-sacred-brown mb-4">Detailed Breakdown</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-sacred-gold/20">
                          <th className="text-left p-2 text-sacred-gold-dark font-medium">Planet</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.sthana')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.dig')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.kala')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.cheshta')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.naisargika')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.drik')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.total')}</th>
                          <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('kundli.ratio')}</th>
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
                  <h4 className="font-display font-bold text-lg" style={{ color: '#1a1a2e' }}>{t('avakhada.title')}</h4>
                  <p className="text-sm text-sacred-text-secondary">{t('avakhada.subtitle')}</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[
                    { label: t('avakhada.ascendant'), value: avakhadaData.ascendant },
                    { label: t('avakhada.ascendantLord'), value: avakhadaData.ascendant_lord },
                    { label: t('avakhada.rashi'), value: avakhadaData.rashi },
                    { label: t('avakhada.rashiLord'), value: avakhadaData.rashi_lord },
                    { label: t('avakhada.nakshatra'), value: `${avakhadaData.nakshatra} (${t('avakhada.pada')} ${avakhadaData.nakshatra_pada})` },
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
                      style={{ backgroundColor: '#F5F0E8', borderColor: 'rgba(184,134,11,0.2)' }}
                    >
                      <p className="text-xs font-medium mb-1" style={{ color: '#8B7355' }}>{item.label}</p>
                      <p className="font-display font-semibold text-base" style={{ color: '#1a1a2e' }}>{item.value}</p>
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
                {/* Yogas Section */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <CheckCircle className="w-5 h-5" style={{ color: '#22c55e' }} />
                    <h4 className="font-display font-bold text-lg" style={{ color: '#1a1a2e' }}>{t('yoga.title')}</h4>
                  </div>
                  <div className="grid gap-3">
                    {(yogaDoshaData.yogas || []).map((yoga: any, idx: number) => (
                      <div
                        key={idx}
                        className={`rounded-xl p-4 border ${yoga.present ? 'border-green-500/30' : 'border-sacred-gold/15'}`}
                        style={{ backgroundColor: yoga.present ? 'rgba(34,197,94,0.05)' : '#F5F0E8' }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-display font-semibold" style={{ color: '#1a1a2e' }}>{yoga.name}</h5>
                          <span className={`text-xs px-2 py-1 rounded-full font-medium ${yoga.present ? 'bg-green-500/20 text-green-600' : 'bg-gray-200 text-gray-500'}`}>
                            {yoga.present ? t('yoga.present') : t('yoga.absent')}
                          </span>
                        </div>
                        <p className="text-sm" style={{ color: '#8B7355' }}>{yoga.description}</p>
                        {yoga.present && yoga.planets_involved && yoga.planets_involved.length > 0 && (
                          <div className="mt-2 flex gap-2">
                            {yoga.planets_involved.map((p: string) => (
                              <span key={p} className="text-xs px-2 py-0.5 rounded-full bg-green-500/10 text-green-600">{p}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Doshas Section */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <Shield className="w-5 h-5" style={{ color: '#8B2332' }} />
                    <h4 className="font-display font-bold text-lg" style={{ color: '#1a1a2e' }}>{t('dosha.extended.title')}</h4>
                  </div>
                  <div className="grid gap-3">
                    {(yogaDoshaData.doshas || []).map((dosha: any, idx: number) => (
                      <div
                        key={idx}
                        className={`rounded-xl p-4 border ${dosha.present ? (dosha.severity === 'high' ? 'border-red-500/40' : 'border-amber-400/40') : 'border-green-500/30'}`}
                        style={{ backgroundColor: dosha.present ? (dosha.severity === 'high' ? 'rgba(139,35,50,0.05)' : 'rgba(245,158,11,0.05)') : 'rgba(34,197,94,0.05)' }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-display font-semibold" style={{ color: '#1a1a2e' }}>{dosha.name}</h5>
                          <div className="flex items-center gap-2">
                            {dosha.present && dosha.severity !== 'none' && (
                              <span className={`text-xs px-2 py-0.5 rounded-full ${dosha.severity === 'high' ? 'bg-red-500/20 text-red-600' : dosha.severity === 'medium' ? 'bg-amber-400/20 text-amber-600' : 'bg-yellow-200 text-yellow-700'}`}>
                                {dosha.severity}
                              </span>
                            )}
                            <span className={`text-xs px-2 py-1 rounded-full font-medium ${dosha.present ? 'bg-red-500/20 text-red-600' : 'bg-green-500/20 text-green-600'}`}>
                              {dosha.present ? t('dosha.present') : t('dosha.absent')}
                            </span>
                          </div>
                        </div>
                        <p className="text-sm" style={{ color: '#8B7355' }}>{dosha.description}</p>
                        {dosha.present && dosha.remedies && dosha.remedies.length > 0 && (
                          <div className="mt-3 pt-3 border-t" style={{ borderColor: 'rgba(139,115,85,0.15)' }}>
                            <p className="text-xs font-semibold mb-2" style={{ color: '#B8860B' }}>
                              <AlertTriangle className="w-3 h-3 inline mr-1" />{t('dosha.remedies')}:
                            </p>
                            <ul className="space-y-1">
                              {dosha.remedies.map((r: string, ri: number) => (
                                <li key={ri} className="text-xs flex items-start gap-2" style={{ color: '#8B7355' }}>
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

          {/* PREDICTIONS TAB — AI-powered */}
          <TabsContent value="predictions">
            {loadingPredictions ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
                <span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingPredictions')}</span>
              </div>
            ) : predictionsData ? (
              <div className="space-y-4">
                <div className="rounded-2xl p-6 border" style={{ backgroundColor: '#F5F0E8', borderColor: 'rgba(139,115,85,0.2)' }}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: 'rgba(184,134,11,0.15)' }}>
                      <Sparkles className="w-5 h-5" style={{ color: '#B8860B' }} />
                    </div>
                    <h4 className="font-sacred font-bold text-xl" style={{ color: '#1a1a2e' }}>{t('kundli.aiPredictions')}</h4>
                  </div>
                  <div className="prose prose-sm max-w-none" style={{ color: '#1a1a2e' }}>
                    {(predictionsData.interpretation || predictionsData.response || predictionsData.text || JSON.stringify(predictionsData))
                      .split('\n')
                      .filter((line: string) => line.trim())
                      .map((paragraph: string, idx: number) => (
                        <p key={idx} className="mb-3 leading-relaxed" style={{ fontFamily: 'serif', color: '#1a1a2e' }}>
                          {paragraph}
                        </p>
                      ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <Sparkles className="w-10 h-10 mx-auto mb-3" style={{ color: 'rgba(184,134,11,0.4)' }} />
                <p className="text-sacred-text-secondary mb-4">{t('kundli.getPredictions')}</p>
                <Button onClick={fetchPredictions} className="btn-sacred">
                  <Sparkles className="w-4 h-4 mr-2" />{t('kundli.predictions')}
                </Button>
              </div>
            )}
          </TabsContent>
        </Tabs>

        <div className="mt-8 text-center">
          <Button onClick={() => { setStep('form'); setResult(null); setDoshaData(null); setIogitaData(null); setDashaData(null); setPredictionsData(null); setAvakhadaData(null); setExtendedDashaData(null); setYogaDoshaData(null); setDivisionalData(null); setAshtakvargaData(null); setShadbalaData(null); }} variant="outline" className="border-cosmic-text-muted text-cosmic-text">
            Generate Another Kundli
          </Button>
        </div>
      </div>
    );
  }

  // --- FORM VIEW ---
  return (
    <div className="max-w-md mx-auto py-24 px-4 bg-transparent">
      <div className="text-center mb-8">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-8 h-8 text-[#1a1a2e]" />
        </div>
        <h3 className="text-2xl sm:text-3xl font-display font-bold text-sacred-brown mb-2">Generate Your Kundli</h3>
        <p className="text-sacred-text-secondary">Enter your birth details for a personalized Vedic birth chart</p>
      </div>
      {savedKundlis.length > 0 && (
        <Button variant="outline" onClick={() => setStep('list')} className="w-full mb-4 border-sacred-gold/50 text-sacred-brown">
          <ArrowLeft className="w-4 h-4 mr-2" />Back to My Kundlis ({savedKundlis.length})
        </Button>
      )}
      <Button onClick={handlePrashnaKundli} variant="outline" className="w-full mb-4 border-sacred-gold/50 text-sacred-brown hover:bg-sacred-gold/10">
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
        <div className="relative">
          <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-cosmic-text-muted" />
          <Input type="text" value={formData.place} onChange={(e) => setFormData({ ...formData, place: e.target.value })} placeholder="Birth Place" className="pl-10 bg-sacred-cream border-sacred-gold/15 text-sacred-brown" />
        </div>
        <Button onClick={handleGenerate} disabled={!formData.name || !formData.date || !formData.time || !formData.place} className="w-full btn-sacred font-semibold hover:bg-sacred-gold-dark disabled:opacity-50">
          <Sparkles className="w-5 h-5 mr-2" />Generate Kundli<ChevronRight className="w-5 h-5 ml-2" />
        </Button>
      </div>
    </div>
  );
}
