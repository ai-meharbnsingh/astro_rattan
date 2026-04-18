// NOTE: LalKitabContext is available for all child tabs via useLalKitab().
// New tabs should prefer context over props. Existing tabs will be migrated gradually.
import { useState, useCallback, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BookOpen, ArrowLeft, Loader2, ChevronDown, LayoutDashboard, ChartPie, Search, Clock3, Sparkles, ScrollText, Tags, Settings2, Home, CalendarCheck } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { autoRegisterClient } from '@/components/ClientSelector';
import NotesWidget from '@/components/NotesWidget';
import { Button } from '@/components/ui/button';
import type { LalKitabChartLite } from '@/components/lalkitab/lalkitab-core';
import { buildLalKitabChartLite } from '@/components/lalkitab/lalkitab-core';
import { LalKitabProvider, useLalKitab } from '@/components/lalkitab/LalKitabContext';
import LalKitabErrorBoundary from '@/components/lalkitab/LalKitabErrorBoundary';
import LalKitabForm from '@/components/lalkitab/LalKitabForm';
import type { LalKitabFormData } from '@/components/lalkitab/LalKitabForm';
import LalKitabDashboardTab from '@/components/lalkitab/LalKitabDashboardTab';
import LalKitabKundliTab from '@/components/lalkitab/LalKitabKundliTab';
import LalKitabPlanetsTab from '@/components/lalkitab/LalKitabPlanetsTab';
import LalKitabDoshaTab from '@/components/lalkitab/LalKitabDoshaTab';
import LalKitabRemediesTab from '@/components/lalkitab/LalKitabRemediesTab';
import LalKitabHousesTab from '@/components/lalkitab/LalKitabHousesTab';
import LalKitabYearlyTab from '@/components/lalkitab/LalKitabYearlyTab';
import LalKitabVarshphalTab from '@/components/lalkitab/LalKitabVarshphalTab';
import LalKitabDualViewTab from '@/components/lalkitab/LalKitabDualViewTab';
import LalKitabFullReport from '@/components/lalkitab/LalKitabFullReport';
import LalKitabRelationsTab from '@/components/lalkitab/LalKitabRelationsTab';
import LalKitabRulesTab from '@/components/lalkitab/LalKitabRulesTab';
import LalKitabNishaniyaTab from '@/components/lalkitab/LalKitabNishaniyaTab';
import LalKitabGocharTab from '@/components/lalkitab/LalKitabGocharTab';
import LalKitabPredictionTab from '@/components/lalkitab/LalKitabPredictionTab';
import LalKitabDashaTab from '@/components/lalkitab/LalKitabDashaTab';
import LalKitabChandraChaalanaTab from '@/components/lalkitab/LalKitabChandraChaalanaTab';
import LalKitabRinTab from '@/components/lalkitab/LalKitabRinTab';
import LalKitabMarriageTab from '@/components/lalkitab/LalKitabMarriageTab';
import LalKitabCareerTab from '@/components/lalkitab/LalKitabCareerTab';
import LalKitabHealthTab from '@/components/lalkitab/LalKitabHealthTab';
import LalKitabWealthTab from '@/components/lalkitab/LalKitabWealthTab';
import LalKitabSavedPredictionsTab from '@/components/lalkitab/LalKitabSavedPredictionsTab';
import LalKitabTevaTab from '@/components/lalkitab/LalKitabTevaTab';
import LalKitabAdvancedTab from '@/components/lalkitab/LalKitabAdvancedTab';
import LalKitabMilestonesTab from '@/components/lalkitab/LalKitabMilestonesTab';
import LalKitabTechnicalTab from '@/components/lalkitab/LalKitabTechnicalTab';
import LalKitabSacrificeTab from '@/components/lalkitab/LalKitabSacrificeTab';
import LalKitabForbiddenTab from '@/components/lalkitab/LalKitabForbiddenTab';
import LalKitabPalmistryTab from '@/components/lalkitab/LalKitabPalmistryTab';
import LalKitabFamilyTab from '@/components/lalkitab/LalKitabFamilyTab';
import LalKitabVastuTab from '@/components/lalkitab/LalKitabVastuTab';
import LalKitabRemedyTrackerTab from '@/components/lalkitab/LalKitabRemedyTrackerTab';
import LalKitabChandraKundaliTab from '@/components/lalkitab/LalKitabChandraKundaliTab';
// P2.1 / P2.7 / P2.8 — Farmaan corpus + rights provenance
import LalKitabFarmaanTab from '@/components/lalkitab/LalKitabFarmaanTab';

type View = 'form' | 'generating' | 'result';

export default function LalKitabPage() {
  return (
    <LalKitabErrorBoundary>
      <LalKitabProvider>
        <LalKitabPageInner />
      </LalKitabProvider>
    </LalKitabErrorBoundary>
  );
}

function LalKitabPageInner() {
  const { t, language } = useTranslation();
  const ctx = useLalKitab();
  const isHi = language === 'hi';
  const { user } = useAuth();
  const isAstrologer = user?.role === 'astrologer';
  const location = useLocation();
  const locState = (location.state as { loadKundliId?: string; clientId?: string }) || {};
  const [view, setView] = useState<View>(locState.loadKundliId ? 'generating' : 'form');
  const [chartData, setChartData] = useState<LalKitabChartLite | null>(null);
  const [apiResult, setApiResult] = useState<any>(null);
  const [birthDate, setBirthDate] = useState('');
  const [formName, setFormName] = useState('');
  const [formTime, setFormTime] = useState('');
  const [formPlace, setFormPlace] = useState('');
  const [error, setError] = useState('');
  const [clientId, setClientId] = useState(locState.clientId || '');
  const [kundliId, setKundliId] = useState(locState.loadKundliId || '');
  const [activeTopTab, setActiveTopTab] = useState('dashboard');
  const [timezoneAutoDetected, setTimezoneAutoDetected] = useState(false);
  const [edition, setEdition] = useState<'1939' | '1941' | '1942' | '1952'>('1952');
  const EDITIONS = ['1939', '1941', '1942', '1952'] as const;
  // P2.6 — Full Report modal state.
  const [showFullReport, setShowFullReport] = useState(false);

  // Sync local state to LalKitabContext so child tabs can access via useLalKitab()
  useEffect(() => { ctx.setChartData(chartData); }, [chartData]);
  useEffect(() => { ctx.setApiResult(apiResult); }, [apiResult]);
  useEffect(() => { ctx.setBirthDate(birthDate || null); }, [birthDate]);
  useEffect(() => { ctx.setKundliId(kundliId || null); }, [kundliId]);

  // Fetch consolidated Lal Kitab data when kundli is loaded.
  // Tabs can prefer ctx.fullData to avoid waterfall calls.
  useEffect(() => {
    if (!kundliId) { ctx.setFullData(null); return; }
    let cancelled = false;
    (async () => {
      try {
        const full = await api.get(`/api/lalkitab/full/${kundliId}`);
        if (!cancelled) ctx.setFullData(full);
      } catch {
        if (!cancelled) ctx.setFullData({ _errors: { full: 'Failed to load consolidated data' } });
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  const topTabs = [
    { value: 'dashboard', label: t('lk.tab.dashboard'), icon: LayoutDashboard },
    { value: 'chart', label: t('auto.chart'), icon: ChartPie },
    { value: 'analysis', label: t('auto.analysis'), icon: Search },
    { value: 'timing', label: t('auto.timingGochar'), icon: Clock3 },
    { value: 'upay', label: t('auto.upay'), icon: Sparkles },
    { value: 'predictions', label: t('auto.predictions'), icon: ScrollText },
    { value: 'nishaniyan', label: t('lk.tab.nishaniyan'), icon: Tags },
    { value: 'advanced', label: t('lk.tab.advanced'), icon: Settings2 },
    { value: 'vastu', label: isHi ? 'मकान' : 'Vastu', icon: Home },
    { value: 'tracker', label: isHi ? 'ट्रैकर' : 'Tracker', icon: CalendarCheck },
    { value: 'farmaan', label: isHi ? 'फ़रमान' : 'Farmaan', icon: BookOpen },
  ];

  // Auto-load existing kundli if navigated with loadKundliId
  useEffect(() => {
    if (!locState.loadKundliId) return;
    (async () => {
      try {
        const full = await api.get(`/api/kundli/${locState.loadKundliId}`);
        const lkChart = buildLalKitabChartLite(full);
        setChartData(lkChart);
        setApiResult(full);
        setClientId(full.client_id || '');
        setKundliId(full.id || '');
        setBirthDate(full.birth_date || '');
        setView('result');
      } catch (e) {
        setError('Failed to load chart');
        setView('form');
      }
    })();
  }, [locState.loadKundliId]);

  const handleGenerate = useCallback(async (formData: LalKitabFormData) => {
    setView('generating');
    setError('');
    setTimezoneAutoDetected(!formData.timezone_offset);
    setBirthDate(formData.date);
    setFormName(formData.name || 'Lal Kitab User');
    setFormTime(formData.time || '');
    setFormPlace(formData.place || '');
    try {
      const payload: any = {
        person_name: formData.name || 'Lal Kitab User',
        birth_date: formData.date,
        birth_time: formData.time,
        birth_place: formData.place,
        latitude: formData.latitude,
        longitude: formData.longitude,
        timezone_offset: formData.timezone_offset ?? (() => {
          const browserOffset = -(new Date().getTimezoneOffset() / 60);
          console.warn('Timezone offset not explicitly provided — using browser timezone:', browserOffset);
          setTimezoneAutoDetected(true);
          return browserOffset;
        })(),
        gender: formData.gender,
        chart_type: 'lalkitab',
      };
      // Send phone for astrologers (required for new client auto-creation)
      if (formData.phone) payload.phone = formData.phone;
      // Send client_id if an existing client was selected
      if (formData.selectedClientId) payload.client_id = formData.selectedClientId;

      const result = await api.post('/api/kundli/generate', payload);
      const lkChart = buildLalKitabChartLite(result);
      setChartData(lkChart);
      setApiResult(result);
      setClientId(result.client_id || '');
      setKundliId(result.id || '');
      setView('result');

      // Auto-register new client for astrologers (the kundli endpoint already does this,
      // but this is a safety net in case client_id wasn't returned)
      if (isAstrologer && formData.isNewClient && !formData.selectedClientId && !result.client_id) {
        autoRegisterClient({
          name: formData.name || 'Lal Kitab User',
          phone: formData.phone,
          birth_date: formData.date,
          birth_time: formData.time,
          birth_place: formData.place,
          latitude: formData.latitude,
          longitude: formData.longitude,
          timezone_offset: formData.timezone_offset ?? -(new Date().getTimezoneOffset() / 60),
          gender: formData.gender,
        });
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : typeof err === 'string' ? err : 'Failed to generate Lal Kitab kundli';
      setError(msg);
      setView('form');
    }
  }, [isAstrologer]);

  return (
    <div className="min-h-screen bg-background bg-mandala pt-32 pb-10 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Result View Header (only show when not in form) */}
        {view !== 'form' && (
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-10">
            {/* LEFT: Kundli-style user info */}
            <div className="flex items-center gap-3 min-w-0">
              <div className="min-w-0">
                {formName ? (
                  <>
                    <h3 className="font-bold text-xl sm:text-2xl text-sacred-brown truncate">{formName} — {t('lk.title')}</h3>
                    <p className="text-sm text-gray-500 truncate">
                      {birthDate}{formTime ? ` | ${formTime}` : ''}{formPlace ? ` | ${formPlace}` : ''}
                    </p>
                  </>
                ) : (
                  <h3 className="font-bold text-xl sm:text-2xl text-sacred-brown truncate">{t('lk.title')}</h3>
                )}
              </div>
            </div>
            {/* RIGHT: Full Report button + Edition Selector */}
            <div className="flex flex-col items-end gap-2 shrink-0">
              {kundliId && (
                <button
                  onClick={() => setShowFullReport(true)}
                  className="inline-flex items-center gap-2 px-5 py-2 rounded-xl bg-sacred-gold text-white font-semibold text-sm shadow-sm hover:bg-sacred-gold-dark transition-colors"
                >
                  <span aria-hidden="true">📄</span>
                  {isHi ? 'पूर्ण रिपोर्ट' : 'Full Report'}
                </button>
              )}
              <div className="flex items-center gap-1.5 flex-wrap justify-end">
                <span className="text-xs text-muted-foreground mr-1">{isHi ? 'संस्करण:' : 'Edition:'}</span>
                {EDITIONS.map((ed) => (
                  <button
                    key={ed}
                    onClick={() => setEdition(ed)}
                    className={`text-xs px-3 py-1 rounded-full border transition-all ${
                      edition === ed
                        ? 'bg-sacred-gold text-white border-sacred-gold font-semibold'
                        : 'border-sacred-gold/30 text-muted-foreground hover:border-sacred-gold/60'
                    }`}
                  >
                    {ed}
                  </button>
                ))}
                {edition !== '1952' && (
                  <span className="text-xs text-amber-600 ml-2">
                    {isHi ? `${edition} संस्करण: कुछ उपाय भिन्न हो सकते हैं` : `${edition} ed: some remedies may vary`}
                  </span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Form View */}
        {view === 'form' && (
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-6">
              <h1 className="text-3xl sm:text-4xl  font-bold text-sacred-gold mb-2">
                {t('lk.title')}
              </h1>
            </div>
            <LalKitabForm onGenerate={handleGenerate} loading={false} />
            {error && (
              <div className="mt-4 p-3 rounded-xl bg-red-50 border border-red-300 text-red-700 text-sm text-center">
                {error}
              </div>
            )}
          </div>
        )}

        {/* Generating View */}
        {view === 'generating' && (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="w-12 h-12 animate-spin text-sacred-gold mb-4" />
            <p className="text-lg  text-sacred-gold">{t('lk.generating')}</p>
          </div>
        )}

        {/* Result View */}
        {view === 'result' && chartData && (
          <div>
            <Button
              variant="outline"
              onClick={() => { setView('form'); setChartData(null); }}
              className="mb-6 border-sacred-gold text-sacred-gold hover:bg-white/10"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              {t('lk.backToForm')}
            </Button>

            {timezoneAutoDetected && (
              <div className="flex items-center gap-2 p-3 mb-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-800">
                <svg className="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>
                  {language === 'hi'
                    ? 'समय क्षेत्र स्वचालित रूप से ब्राउज़र से लिया गया है। सटीक कुंडली के लिए जन्म स्थान का समय क्षेत्र सत्यापित करें।'
                    : 'Timezone auto-detected from browser. Verify birth location timezone for accurate charts.'}
                </span>
              </div>
            )}

            {chartData?.isIncomplete && (
              <div className="p-4 mb-4 bg-amber-50 border-2 border-amber-300 rounded-xl">
                <h3 className="font-semibold text-amber-900 mb-1">
                  {language === 'hi' ? '⚠️ अधूरी कुंडली' : '⚠️ Incomplete Chart'}
                </h3>
                <p className="text-sm text-amber-800">
                  {language === 'hi'
                    ? 'कुछ ग्रहों की स्थिति उपलब्ध नहीं है। विश्लेषण की सटीकता प्रभावित हो सकती है।'
                    : 'Some planet positions are missing. Analysis accuracy may be affected.'}
                </p>
                {chartData.missingPlanets?.length > 0 && (
                  <p className="text-xs text-amber-700 mt-2">
                    {language === 'hi' ? 'अनुपस्थित ग्रह: ' : 'Missing planets: '}
                    <span className="font-mono">{chartData.missingPlanets.join(', ')}</span>
                  </p>
                )}
              </div>
            )}

            <Tabs value={activeTopTab} onValueChange={setActiveTopTab} className="w-full">
              <div className="mb-4">
                <TabsList className="bg-muted w-full h-auto p-2 gap-1 grid grid-cols-5 md:grid-cols-10
                  [&>button]:min-w-0 [&>button]:min-h-[50px] md:[&>button]:min-h-[58px] [&>button]:px-1 [&>button]:py-2 [&>button]:text-[10px] md:[&>button]:text-xs
                  [&>button]:flex [&>button]:flex-col [&>button]:items-center [&>button]:justify-center [&>button]:gap-0.5 md:[&>button]:gap-1 [&>button]:leading-tight
                  [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md">
                  {topTabs.map((tab) => (
                    <TabsTrigger key={tab.value} value={tab.value}>
                      <tab.icon className="w-3.5 h-3.5" />
                      <span className="truncate max-w-full">{tab.label}</span>
                    </TabsTrigger>
                  ))}
                </TabsList>
              </div>

              <TabsContent value="dashboard">
                <LalKitabDashboardTab
                  chartData={chartData}
                  birthDate={birthDate}
                  kundliId={kundliId}
                  onNavigateTab={setActiveTopTab}
                />
              </TabsContent>
              <TabsContent value="chart" className="space-y-8">
                <LalKitabKundliTab chartData={chartData} apiResult={apiResult} />
                <LalKitabPlanetsTab chartData={chartData} kundliId={kundliId} />
                <LalKitabHousesTab chartData={chartData} />
                <LalKitabChandraKundaliTab kundliId={kundliId} language={language} />
              </TabsContent>
              <TabsContent value="analysis" className="space-y-8">
                <LalKitabDoshaTab chartData={chartData} />
                <LalKitabRelationsTab chartData={chartData} />
                <LalKitabRulesTab chartData={chartData} />
                <LalKitabSacrificeTab kundliId={kundliId} language={language} />
                <LalKitabTechnicalTab kundliId={kundliId} language={language} />
              </TabsContent>
              <TabsContent value="timing" className="space-y-8">
                <LalKitabDashaTab kundliId={kundliId} language={language} />
                <LalKitabMilestonesTab kundliId={kundliId} language={language} />
                <LalKitabYearlyTab chartData={chartData} birthDate={birthDate} />
                {/* P2.5 — Comparative Dual-View (Tewa + Varshphal synchronised).
                    Placed between Tewa-driven Yearly and the Varshphal tab so
                    astrologers can compare natal vs current-year at a glance. */}
                <LalKitabDualViewTab apiResult={apiResult} />
                <LalKitabVarshphalTab />
                <LalKitabGocharTab chartData={chartData} apiResult={apiResult} />
              </TabsContent>
              <TabsContent value="upay" className="space-y-8">
                <LalKitabForbiddenTab kundliId={kundliId} language={language} />
                <LalKitabRemediesTab chartData={chartData} kundliId={kundliId} />
                <LalKitabChandraChaalanaTab />
              </TabsContent>
              <TabsContent value="predictions" className="space-y-4">
                <details open className="border border-sacred-gold/20 rounded-xl overflow-hidden">
                  <summary className="p-4 bg-card cursor-pointer font-semibold text-sacred-gold flex items-center justify-between">
                    {t('auto.generalPredictions')}
                    <ChevronDown className="w-4 h-4" />
                  </summary>
                  <div className="p-4">
                    <LalKitabPredictionTab chartData={chartData} kundliId={kundliId} />
                  </div>
                </details>
                <details className="border border-sacred-gold/20 rounded-xl overflow-hidden">
                  <summary className="p-4 bg-card cursor-pointer font-semibold text-sacred-gold flex items-center justify-between">
                    {t('auto.marriagePredictions')}
                    <ChevronDown className="w-4 h-4" />
                  </summary>
                  <div className="p-4">
                    <LalKitabMarriageTab kundliId={kundliId} />
                  </div>
                </details>
                <details className="border border-sacred-gold/20 rounded-xl overflow-hidden">
                  <summary className="p-4 bg-card cursor-pointer font-semibold text-sacred-gold flex items-center justify-between">
                    {t('auto.careerPredictions')}
                    <ChevronDown className="w-4 h-4" />
                  </summary>
                  <div className="p-4">
                    <LalKitabCareerTab kundliId={kundliId} />
                  </div>
                </details>
                <details className="border border-sacred-gold/20 rounded-xl overflow-hidden">
                  <summary className="p-4 bg-card cursor-pointer font-semibold text-sacred-gold flex items-center justify-between">
                    {t('auto.healthPredictions')}
                    <ChevronDown className="w-4 h-4" />
                  </summary>
                  <div className="p-4">
                    <LalKitabHealthTab kundliId={kundliId} />
                  </div>
                </details>
                <details className="border border-sacred-gold/20 rounded-xl overflow-hidden">
                  <summary className="p-4 bg-card cursor-pointer font-semibold text-sacred-gold flex items-center justify-between">
                    {t('auto.wealthPredictions')}
                    <ChevronDown className="w-4 h-4" />
                  </summary>
                  <div className="p-4">
                    <LalKitabWealthTab kundliId={kundliId} />
                  </div>
                </details>
                <details className="border border-sacred-gold/20 rounded-xl overflow-hidden">
                  <summary className="p-4 bg-card cursor-pointer font-semibold text-sacred-gold flex items-center justify-between">
                    {t('auto.savedPredictions')}
                    <ChevronDown className="w-4 h-4" />
                  </summary>
                  <div className="p-4">
                    <LalKitabSavedPredictionsTab kundliId={kundliId} />
                  </div>
                </details>
              </TabsContent>
              <TabsContent value="nishaniyan">
                <LalKitabNishaniyaTab kundliId={kundliId} />
              </TabsContent>
              <TabsContent value="advanced" className="space-y-8">
                <LalKitabPalmistryTab kundliId={kundliId} language={language} />
                <LalKitabFamilyTab kundliId={kundliId} language={language} />
                <LalKitabAdvancedTab kundliId={kundliId} chartData={chartData} />
                <LalKitabTevaTab apiResult={apiResult} />
                <LalKitabRinTab kundliId={kundliId} />
              </TabsContent>
              <TabsContent value="vastu" className="space-y-4">
                <LalKitabVastuTab kundliId={kundliId} language={language} />
              </TabsContent>
              <TabsContent value="tracker" className="space-y-4">
                <LalKitabRemedyTrackerTab kundliId={kundliId} language={language} />
              </TabsContent>
              <TabsContent value="farmaan" className="space-y-4">
                <LalKitabFarmaanTab />
              </TabsContent>
            </Tabs>
            {clientId && <NotesWidget clientId={clientId} chartType="lalkitab" kundliId={kundliId} />}
          </div>
        )}
      </div>

      {/* P2.6 — Full Report modal (portal-style overlay).
          Mounted at page root so it sits above tabs + navigation. */}
      {showFullReport && kundliId && (
        <LalKitabFullReport
          kundliId={kundliId}
          onClose={() => setShowFullReport(false)}
        />
      )}
    </div>
  );
}
