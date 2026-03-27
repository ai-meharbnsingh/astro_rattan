import { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, Calendar, Clock, MapPin, User, ChevronRight, Download, Share2, FileText, Heart, Briefcase, Activity, ArrowLeft, Loader2, X } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';

export default function KundliGenerator() {
  const { isAuthenticated } = useAuth();
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
  const [error, setError] = useState('');
  const [sidePanel, setSidePanel] = useState<{
    type: 'planet' | 'house';
    planet?: PlanetData;
    house?: number;
    sign?: string;
    planets?: PlanetData[];
  } | null>(null);

  const HOUSE_SIGNIFICANCE: Record<number, string> = {
    1: 'Self, Personality, Appearance',
    2: 'Wealth, Family, Speech',
    3: 'Courage, Siblings, Communication',
    4: 'Home, Mother, Comfort',
    5: 'Children, Education, Creativity',
    6: 'Health, Enemies, Service',
    7: 'Marriage, Partnership, Business',
    8: 'Longevity, Transformation, Occult',
    9: 'Fortune, Dharma, Higher Learning',
    10: 'Career, Status, Authority',
    11: 'Gains, Aspirations, Friends',
    12: 'Losses, Moksha, Foreign Lands',
  };

  const PLANET_ASPECTS: Record<string, number[]> = {
    Sun: [7], Moon: [7], Mercury: [7], Venus: [7],
    Mars: [4, 7, 8], Jupiter: [5, 7, 9], Saturn: [3, 7, 10],
    Rahu: [5, 7, 9], Ketu: [5, 7, 9],
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
            <Sparkles className="w-8 h-8 text-white" />
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
                <Sparkles className="w-5 h-5 text-sacred-gold" />Get Detailed PDF Reports
              </h4>
              <p className="text-sm text-sacred-text-secondary">Unlock 30+ page personalized reports with in-depth analysis</p>
            </div>
            <Button variant="outline" className="border-sacred-gold text-sacred-gold-dark">View All Reports</Button>
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
          <TabsList className="mb-6 bg-sacred-cream">
            <TabsTrigger value="planets">Planets</TabsTrigger>
            <TabsTrigger value="dosha" onClick={fetchDosha}>Dosha</TabsTrigger>
            <TabsTrigger value="iogita" onClick={fetchIogita}>io-gita</TabsTrigger>
            <TabsTrigger value="dasha" onClick={fetchDasha}>Dasha</TabsTrigger>
          </TabsList>

          {/* PLANETS TAB - Interactive Kundli Chart + Side Panel */}
          <TabsContent value="planets">
            <div className="flex flex-col lg:flex-row gap-6">
              {/* Interactive Chart */}
              <div className="flex-shrink-0 flex justify-center">
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
                          : `House ${sidePanel.house} Details`}
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
          <TabsContent value="dasha">
            {loadingDasha ? (
              <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-sacred-text-secondary">Calculating Vimshottari Dasha...</span></div>
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
                          <td className="p-3 text-sacred-brown">{p.planet} {p.planet === dashaData.current_dasha ? '←' : ''}</td>
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
        </Tabs>

        <div className="mt-8 text-center">
          <Button onClick={() => { setStep('form'); setResult(null); setDoshaData(null); setIogitaData(null); setDashaData(null); }} variant="outline" className="border-cosmic-text-muted text-cosmic-text">
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
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <h3 className="text-2xl sm:text-3xl font-display font-bold text-sacred-brown mb-2">Generate Your Kundli</h3>
        <p className="text-sacred-text-secondary">Enter your birth details for a personalized Vedic birth chart</p>
      </div>
      {savedKundlis.length > 0 && (
        <Button variant="outline" onClick={() => setStep('list')} className="w-full mb-4 border-sacred-gold/50 text-sacred-brown">
          <ArrowLeft className="w-4 h-4 mr-2" />Back to My Kundlis ({savedKundlis.length})
        </Button>
      )}
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
