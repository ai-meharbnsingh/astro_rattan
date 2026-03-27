import { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Sparkles, ChevronRight, Loader2, Star, BookOpen, Gem, Hand } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

export default function KPLalkitabPage() {
  const { isAuthenticated } = useAuth();
  const [kundlis, setKundlis] = useState<any[]>([]);
  const [selectedKundli, setSelectedKundli] = useState('');
  const [loadingKundlis, setLoadingKundlis] = useState(true);

  // KP state
  const [kpResult, setKpResult] = useState<any>(null);
  const [kpLoading, setKpLoading] = useState(false);
  const [kpError, setKpError] = useState('');

  // Lal Kitab state
  const [lkResult, setLkResult] = useState<any>(null);
  const [lkLoading, setLkLoading] = useState(false);
  const [lkError, setLkError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      setLoadingKundlis(false);
      return;
    }
    api.get('/api/kundli/list')
      .then((data: any) => {
        const list = Array.isArray(data) ? data : [];
        setKundlis(list);
        if (list.length > 0) setSelectedKundli(list[0].id);
      })
      .catch(() => {})
      .finally(() => setLoadingKundlis(false));
  }, [isAuthenticated]);

  const analyzeKP = async () => {
    if (!selectedKundli) return;
    setKpLoading(true);
    setKpError('');
    setKpResult(null);
    try {
      const data = await api.post('/api/kp/cuspal', { kundli_id: selectedKundli });
      setKpResult(data);
    } catch (err) {
      setKpError(err instanceof Error ? err.message : 'Failed to analyze KP chart');
    }
    setKpLoading(false);
  };

  const fetchRemedies = async () => {
    if (!selectedKundli) return;
    setLkLoading(true);
    setLkError('');
    setLkResult(null);
    try {
      const data = await api.post('/api/lalkitab/remedies', { kundli_id: selectedKundli });
      setLkResult(data);
    } catch (err) {
      setLkError(err instanceof Error ? err.message : 'Failed to get remedies');
    }
    setLkLoading(false);
  };

  // Kundli selector shared between tabs
  const KundliSelector = () => (
    <div className="mb-6">
      <label className="block text-sm font-medium text-sacred-gold mb-2">Select Kundli</label>
      {loadingKundlis ? (
        <div className="flex items-center gap-2 text-cosmic-text">
          <Loader2 className="w-4 h-4 animate-spin text-sacred-gold" />
          <span className="text-sm">Loading kundlis...</span>
        </div>
      ) : !isAuthenticated ? (
        <p className="text-sm text-cosmic-text/70">Please sign in to access your saved kundlis.</p>
      ) : kundlis.length === 0 ? (
        <p className="text-sm text-cosmic-text/70">No kundlis found. Generate one first from the Kundli page.</p>
      ) : (
        <select
          value={selectedKundli}
          onChange={(e) => setSelectedKundli(e.target.value)}
          className="w-full rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text px-4 py-3 focus:outline-none focus:border-sacred-gold/50 transition-colors"
        >
          {kundlis.map((k: any) => (
            <option key={k.id} value={k.id}>
              {k.person_name} &mdash; {k.birth_date}
            </option>
          ))}
        </select>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-cosmic-bg bg-mandala py-24 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
            <Star className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-sacred font-bold text-sacred-gold mb-2">
            KP System & Lal Kitab
          </h1>
          <p className="text-cosmic-text/70 max-w-lg mx-auto">
            Explore Krishnamurti Paddhati analysis and traditional Lal Kitab remedies for your birth chart
          </p>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="kp" className="w-full">
          <TabsList className="mb-8 bg-cosmic-card border border-sacred-gold/20 w-full grid grid-cols-2">
            <TabsTrigger value="kp" className="font-sacred data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold">
              KP System
            </TabsTrigger>
            <TabsTrigger value="lalkitab" className="font-sacred data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold">
              Lal Kitab
            </TabsTrigger>
          </TabsList>

          {/* KP System Tab */}
          <TabsContent value="kp">
            <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
              <div className="flex items-center gap-3 mb-6">
                <Sparkles className="w-6 h-6 text-sacred-gold" />
                <h2 className="text-xl font-sacred font-bold text-sacred-gold">KP Cuspal Analysis</h2>
              </div>

              <KundliSelector />

              <Button
                onClick={analyzeKP}
                disabled={!selectedKundli || kpLoading}
                className="btn-sacred w-full sm:w-auto font-semibold disabled:opacity-50"
              >
                {kpLoading ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Analyzing...</>
                ) : (
                  <><Sparkles className="w-4 h-4 mr-2" />Analyze KP Chart<ChevronRight className="w-4 h-4 ml-2" /></>
                )}
              </Button>

              {kpError && (
                <div className="mt-4 p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{kpError}</div>
              )}

              {kpResult && (
                <div className="mt-8 space-y-6">
                  {/* Cuspal Chart - Cusps */}
                  {kpResult.cuspal_chart?.cusps && kpResult.cuspal_chart.cusps.length > 0 && (
                    <div>
                      <h3 className="text-lg font-sacred font-semibold text-sacred-gold mb-4">House Cusps &amp; Sub-Lords</h3>
                      <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
                        <table className="w-full">
                          <thead className="bg-cosmic-card">
                            <tr>
                              <th className="text-left p-4 text-sacred-gold font-medium text-sm">House</th>
                              <th className="text-left p-4 text-sacred-gold font-medium text-sm">Cusp Degree</th>
                              <th className="text-left p-4 text-sacred-gold font-medium text-sm">Sign</th>
                              <th className="text-left p-4 text-sacred-gold font-medium text-sm">Star Lord</th>
                              <th className="text-left p-4 text-sacred-gold font-medium text-sm">Sub Lord</th>
                            </tr>
                          </thead>
                          <tbody>
                            {kpResult.cuspal_chart.cusps.map((cusp: any, i: number) => (
                              <tr key={i} className="border-t border-sacred-gold/10">
                                <td className="p-4 text-cosmic-text font-medium">{cusp.house || i + 1}</td>
                                <td className="p-4 text-cosmic-text/80">{typeof cusp.degree === 'number' ? cusp.degree.toFixed(2) + '\u00B0' : cusp.degree || '--'}</td>
                                <td className="p-4 text-cosmic-text/80">{cusp.sign || '--'}</td>
                                <td className="p-4 text-sacred-gold">{cusp.star_lord || '--'}</td>
                                <td className="p-4 text-sacred-gold">{cusp.sub_lord || '--'}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* Planet Positions in KP */}
                  {kpResult.cuspal_chart?.planets && Object.keys(kpResult.cuspal_chart.planets).length > 0 && (
                    <div>
                      <h3 className="text-lg font-sacred font-semibold text-sacred-gold mb-4">Planet Star &amp; Sub Lords</h3>
                      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                        {Object.entries(kpResult.cuspal_chart.planets).map(([planet, info]: [string, any]) => (
                          <div key={planet} className="card-sacred rounded-xl p-4 border border-sacred-gold/20">
                            <h4 className="font-sacred font-semibold text-sacred-gold mb-2">{planet}</h4>
                            <div className="space-y-1 text-sm">
                              {info.degree !== undefined && (
                                <p className="text-cosmic-text/80">Degree: <span className="text-cosmic-text">{typeof info.degree === 'number' ? info.degree.toFixed(2) + '\u00B0' : info.degree}</span></p>
                              )}
                              {info.sign && <p className="text-cosmic-text/80">Sign: <span className="text-cosmic-text">{info.sign}</span></p>}
                              {info.star_lord && <p className="text-cosmic-text/80">Star Lord: <span className="text-sacred-gold">{info.star_lord}</span></p>}
                              {info.sub_lord && <p className="text-cosmic-text/80">Sub Lord: <span className="text-sacred-gold">{info.sub_lord}</span></p>}
                              {info.sub_sub_lord && <p className="text-cosmic-text/80">Sub-Sub Lord: <span className="text-sacred-gold">{info.sub_sub_lord}</span></p>}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Significators */}
                  {kpResult.significators && Object.keys(kpResult.significators).length > 0 && (
                    <div>
                      <h3 className="text-lg font-sacred font-semibold text-sacred-gold mb-4">House Significators</h3>
                      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                        {Object.entries(kpResult.significators).map(([house, planets]: [string, any]) => (
                          <div key={house} className="card-sacred rounded-xl p-4 border border-sacred-gold/20">
                            <h4 className="font-sacred font-semibold text-sacred-gold mb-2">House {house}</h4>
                            <div className="flex flex-wrap gap-2">
                              {(Array.isArray(planets) ? planets : [planets]).map((p: string, idx: number) => (
                                <span key={idx} className="text-xs px-2 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20">
                                  {p}
                                </span>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </TabsContent>

          {/* Lal Kitab Tab */}
          <TabsContent value="lalkitab">
            <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
              <div className="flex items-center gap-3 mb-6">
                <BookOpen className="w-6 h-6 text-sacred-gold" />
                <h2 className="text-xl font-sacred font-bold text-sacred-gold">Lal Kitab Remedies</h2>
              </div>

              <KundliSelector />

              <Button
                onClick={fetchRemedies}
                disabled={!selectedKundli || lkLoading}
                className="btn-sacred w-full sm:w-auto font-semibold disabled:opacity-50"
              >
                {lkLoading ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Fetching Remedies...</>
                ) : (
                  <><BookOpen className="w-4 h-4 mr-2" />Get Remedies<ChevronRight className="w-4 h-4 ml-2" /></>
                )}
              </Button>

              {lkError && (
                <div className="mt-4 p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{lkError}</div>
              )}

              {lkResult?.remedies_by_planet && (
                <div className="mt-8 space-y-4">
                  <h3 className="text-lg font-sacred font-semibold text-sacred-gold mb-4">Remedies by Planet</h3>
                  {Object.entries(lkResult.remedies_by_planet).map(([planet, remedy]: [string, any]) => (
                    <div key={planet} className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-full bg-sacred-gold/10 flex items-center justify-center">
                          <Star className="w-5 h-5 text-sacred-gold" />
                        </div>
                        <h4 className="text-lg font-sacred font-semibold text-sacred-gold">{planet}</h4>
                      </div>
                      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                        {remedy.gemstone && (
                          <div className="flex items-start gap-2">
                            <Gem className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                            <div>
                              <p className="text-xs text-cosmic-text/60 uppercase tracking-wide">Gemstone</p>
                              <p className="text-sm text-cosmic-text">{remedy.gemstone}</p>
                            </div>
                          </div>
                        )}
                        {remedy.metal && (
                          <div className="flex items-start gap-2">
                            <Sparkles className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                            <div>
                              <p className="text-xs text-cosmic-text/60 uppercase tracking-wide">Metal</p>
                              <p className="text-sm text-cosmic-text">{remedy.metal}</p>
                            </div>
                          </div>
                        )}
                        {remedy.finger && (
                          <div className="flex items-start gap-2">
                            <Hand className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                            <div>
                              <p className="text-xs text-cosmic-text/60 uppercase tracking-wide">Finger</p>
                              <p className="text-sm text-cosmic-text">{remedy.finger}</p>
                            </div>
                          </div>
                        )}
                        {remedy.fasting_day && (
                          <div className="flex items-start gap-2">
                            <BookOpen className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                            <div>
                              <p className="text-xs text-cosmic-text/60 uppercase tracking-wide">Fasting Day</p>
                              <p className="text-sm text-cosmic-text">{remedy.fasting_day}</p>
                            </div>
                          </div>
                        )}
                        {remedy.donation && (
                          <div className="flex items-start gap-2 sm:col-span-2">
                            <Star className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                            <div>
                              <p className="text-xs text-cosmic-text/60 uppercase tracking-wide">Donations</p>
                              <p className="text-sm text-cosmic-text">{Array.isArray(remedy.donation) ? remedy.donation.join(', ') : remedy.donation}</p>
                            </div>
                          </div>
                        )}
                      </div>
                      {remedy.remedy && (
                        <div className="mt-4 p-3 rounded-lg bg-sacred-gold/5 border border-sacred-gold/10">
                          <p className="text-xs text-cosmic-text/60 uppercase tracking-wide mb-1">Remedy</p>
                          <p className="text-sm text-cosmic-text leading-relaxed">
                            {Array.isArray(remedy.remedy) ? remedy.remedy.join('; ') : remedy.remedy}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
