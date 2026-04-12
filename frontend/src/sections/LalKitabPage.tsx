import { useState, useCallback, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BookOpen, ArrowLeft, Loader2 } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { autoRegisterClient } from '@/components/ClientSelector';
import NotesWidget from '@/components/NotesWidget';
import { Button } from '@/components/ui/button';
import type { LalKitabChartData } from '@/components/lalkitab/lalkitab-data';
import { generateLalKitabChart } from '@/components/lalkitab/lalkitab-data';
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
import LalKitabRelationsTab from '@/components/lalkitab/LalKitabRelationsTab';
import LalKitabRulesTab from '@/components/lalkitab/LalKitabRulesTab';
import LalKitabNishaniyaTab from '@/components/lalkitab/LalKitabNishaniyaTab';
import LalKitabGocharTab from '@/components/lalkitab/LalKitabGocharTab';
import LalKitabPredictionTab from '@/components/lalkitab/LalKitabPredictionTab';
import LalKitabRemediesTrackerTab from '@/components/lalkitab/LalKitabRemediesTrackerTab';
import LalKitabChandraChaalanaTab from '@/components/lalkitab/LalKitabChandraChaalanaTab';
import LalKitabRinTab from '@/components/lalkitab/LalKitabRinTab';
import LalKitabMarriageTab from '@/components/lalkitab/LalKitabMarriageTab';
import LalKitabCareerTab from '@/components/lalkitab/LalKitabCareerTab';
import LalKitabHealthTab from '@/components/lalkitab/LalKitabHealthTab';
import LalKitabWealthTab from '@/components/lalkitab/LalKitabWealthTab';
import LalKitabSavedPredictionsTab from '@/components/lalkitab/LalKitabSavedPredictionsTab';
import LalKitabTevaTab from '@/components/lalkitab/LalKitabTevaTab';
import LalKitabAdvancedTab from '@/components/lalkitab/LalKitabAdvancedTab';

type View = 'form' | 'generating' | 'result';

export default function LalKitabPage() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { user } = useAuth();
  const isAstrologer = user?.role === 'astrologer';
  const location = useLocation();
  const locState = (location.state as { loadKundliId?: string; clientId?: string }) || {};
  const [view, setView] = useState<View>(locState.loadKundliId ? 'generating' : 'form');
  const [chartData, setChartData] = useState<LalKitabChartData | null>(null);
  const [apiResult, setApiResult] = useState<any>(null);
  const [birthDate, setBirthDate] = useState('');
  const [error, setError] = useState('');
  const [clientId, setClientId] = useState(locState.clientId || '');
  const [kundliId, setKundliId] = useState(locState.loadKundliId || '');
  const [activeTopTab, setActiveTopTab] = useState('dashboard');

  // Auto-load existing kundli if navigated with loadKundliId
  useEffect(() => {
    if (!locState.loadKundliId) return;
    (async () => {
      try {
        const full = await api.get(`/api/kundli/${locState.loadKundliId}`);
        const lkChart = generateLalKitabChart(full);
        setChartData(lkChart);
        setApiResult(full);
        setClientId(full.client_id || '');
        setKundliId(full.id || '');
        setBirthDate(full.birth_date || '');
        setView('result');
      } catch (e) {
        console.error(e);
        setError('Failed to load chart');
        setView('form');
      }
    })();
  }, [locState.loadKundliId]);

  const handleGenerate = useCallback(async (formData: LalKitabFormData) => {
    setView('generating');
    setError('');
    setBirthDate(formData.date);
    try {
      const payload: any = {
        person_name: formData.name || 'Lal Kitab User',
        birth_date: formData.date,
        birth_time: formData.time,
        birth_place: formData.place,
        latitude: formData.latitude,
        longitude: formData.longitude,
        timezone_offset: -(new Date().getTimezoneOffset() / 60),
        gender: formData.gender,
        chart_type: 'lalkitab',
      };
      // Send phone for astrologers (required for new client auto-creation)
      if (formData.phone) payload.phone = formData.phone;
      // Send client_id if an existing client was selected
      if (formData.selectedClientId) payload.client_id = formData.selectedClientId;

      const result = await api.post('/api/kundli/generate', payload);
      const lkChart = generateLalKitabChart(result);
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
          timezone_offset: -(new Date().getTimezoneOffset() / 60),
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
    <div className="min-h-screen bg-cosmic-bg bg-mandala py-24 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-red-600 to-sacred-gold flex items-center justify-center mx-auto mb-4">
            <BookOpen className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-sans font-bold text-sacred-gold mb-2">
            {t('lk.title')}
          </h1>
          <p className="text-cosmic-text max-w-lg mx-auto">
            {t('lk.subtitle')}
          </p>
        </div>

        {/* Form View */}
        {view === 'form' && (
          <div className="max-w-xl mx-auto">
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
            <p className="text-lg font-sans text-sacred-gold">{t('lk.generating')}</p>
          </div>
        )}

        {/* Result View */}
        {view === 'result' && chartData && (
          <div>
            <Button
              variant="outline"
              onClick={() => { setView('form'); setChartData(null); }}
              className="mb-6 border-sacred-gold text-sacred-gold hover:bg-gray-50"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              {t('lk.backToForm')}
            </Button>

            <Tabs value={activeTopTab} onValueChange={setActiveTopTab} className="w-full">
              <div className="relative mb-6 md:mb-4 md:static">
                {/* Scroll hint arrows — mobile only */}
                <div className="absolute left-0 top-0 bottom-0 w-8 bg-gradient-to-r from-sacred-cream to-transparent z-10 pointer-events-none flex items-center justify-start pl-1 md:hidden">
                  <span className="text-sacred-gold-dark text-lg">‹</span>
                </div>
                <div className="absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-sacred-cream to-transparent z-10 pointer-events-none flex items-center justify-end pr-1 md:hidden">
                  <span className="text-sacred-gold-dark text-lg">›</span>
                </div>

                {/* Desktop: grouped tabs */}
                <div className="hidden md:flex md:flex-col md:gap-1">
                  <TabsList className="bg-sacred-cream w-full h-auto p-2 gap-1 grid grid-cols-4
                    [&>button]:whitespace-nowrap [&>button]:min-h-[36px] [&>button]:px-2 [&>button]:py-1.5 [&>button]:text-xs
                    [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md">
                    <TabsTrigger value="dashboard">{t('lk.tab.dashboard')}</TabsTrigger>
                    <TabsTrigger value="chart">{isHi ? 'चार्ट' : 'Chart'}</TabsTrigger>
                    <TabsTrigger value="analysis">{isHi ? 'विश्लेषण' : 'Analysis'}</TabsTrigger>
                    <TabsTrigger value="timing">{isHi ? 'समय व गोचर' : 'Timing & Gochar'}</TabsTrigger>
                  </TabsList>
                  <TabsList className="bg-sacred-cream w-full h-auto p-2 gap-1 grid grid-cols-4
                    [&>button]:whitespace-nowrap [&>button]:min-h-[36px] [&>button]:px-2 [&>button]:py-1.5 [&>button]:text-xs
                    [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md">
                    <TabsTrigger value="upay">{isHi ? 'उपाय' : 'Upay'}</TabsTrigger>
                    <TabsTrigger value="predictions">{isHi ? 'भविष्यवाणी' : 'Predictions'}</TabsTrigger>
                    <TabsTrigger value="nishaniyan">{t('lk.tab.nishaniyan')}</TabsTrigger>
                    <TabsTrigger value="advanced">{t('lk.tab.advanced')}</TabsTrigger>
                  </TabsList>
                </div>

                {/* Mobile: single horizontally scrollable row */}
                <TabsList className="md:hidden bg-sacred-cream w-full h-auto p-2 gap-1
                  flex flex-nowrap overflow-x-auto pb-3 scrollbar-hide
                  [&>button]:flex-shrink-0 [&>button]:flex-grow-0 [&>button]:basis-auto [&>button]:whitespace-nowrap [&>button]:min-h-[36px] [&>button]:px-3 [&>button]:py-1.5 [&>button]:text-xs
                  [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md">
                  <TabsTrigger value="dashboard">{t('lk.tab.dashboard')}</TabsTrigger>
                  <TabsTrigger value="chart">{isHi ? 'चार्ट' : 'Chart'}</TabsTrigger>
                  <TabsTrigger value="analysis">{isHi ? 'विश्लेषण' : 'Analysis'}</TabsTrigger>
                  <TabsTrigger value="timing">{isHi ? 'समय व गोचर' : 'Timing & Gochar'}</TabsTrigger>
                  <TabsTrigger value="upay">{isHi ? 'उपाय' : 'Upay'}</TabsTrigger>
                  <TabsTrigger value="predictions">{isHi ? 'भविष्यवाणी' : 'Predictions'}</TabsTrigger>
                  <TabsTrigger value="nishaniyan">{t('lk.tab.nishaniyan')}</TabsTrigger>
                  <TabsTrigger value="advanced">{t('lk.tab.advanced')}</TabsTrigger>
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
              </TabsContent>
              <TabsContent value="analysis" className="space-y-8">
                <LalKitabDoshaTab chartData={chartData} />
                <LalKitabRelationsTab chartData={chartData} />
                <LalKitabRulesTab chartData={chartData} />
              </TabsContent>
              <TabsContent value="timing" className="space-y-8">
                <LalKitabYearlyTab chartData={chartData} birthDate={birthDate} />
                <LalKitabVarshphalTab chartData={chartData} birthDate={birthDate} apiResult={apiResult} />
                <LalKitabGocharTab chartData={chartData} apiResult={apiResult} />
              </TabsContent>
              <TabsContent value="upay" className="space-y-8">
                <LalKitabRemediesTab chartData={chartData} kundliId={kundliId} />
                <LalKitabRemediesTrackerTab chartData={chartData} kundliId={kundliId} />
                <LalKitabChandraChaalanaTab />
              </TabsContent>
              <TabsContent value="predictions" className="space-y-8">
                <LalKitabPredictionTab chartData={chartData} />
                <LalKitabMarriageTab kundliId={kundliId} />
                <LalKitabCareerTab kundliId={kundliId} />
                <LalKitabHealthTab kundliId={kundliId} />
                <LalKitabWealthTab kundliId={kundliId} />
                <LalKitabSavedPredictionsTab kundliId={kundliId} />
              </TabsContent>
              <TabsContent value="nishaniyan">
                <LalKitabNishaniyaTab kundliId={kundliId} />
              </TabsContent>
              <TabsContent value="advanced" className="space-y-8">
                <LalKitabAdvancedTab kundliId={kundliId} chartData={chartData} />
                <LalKitabTevaTab chartData={chartData} apiResult={apiResult} />
                <LalKitabRinTab kundliId={kundliId} />
              </TabsContent>
            </Tabs>
            {clientId && <NotesWidget clientId={clientId} chartType="lalkitab" kundliId={kundliId} />}
          </div>
        )}
      </div>
    </div>
  );
}
