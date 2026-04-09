import { useState, useCallback, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BookOpen, ArrowLeft, Loader2 } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
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

type View = 'form' | 'generating' | 'result';

export default function LalKitabPage() {
  const { t } = useTranslation();
  const location = useLocation();
  const locState = (location.state as { loadKundliId?: string; clientId?: string }) || {};
  const [view, setView] = useState<View>(locState.loadKundliId ? 'generating' : 'form');
  const [chartData, setChartData] = useState<LalKitabChartData | null>(null);
  const [birthDate, setBirthDate] = useState('');
  const [error, setError] = useState('');
  const [clientId, setClientId] = useState(locState.clientId || '');
  const [kundliId, setKundliId] = useState(locState.loadKundliId || '');

  // Auto-load existing kundli if navigated with loadKundliId
  useEffect(() => {
    if (!locState.loadKundliId) return;
    (async () => {
      try {
        const full = await api.get(`/api/kundli/${locState.loadKundliId}`);
        const lkChart = generateLalKitabChart(full);
        setChartData(lkChart);
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
  }, []);

  const handleGenerate = useCallback(async (formData: LalKitabFormData) => {
    setView('generating');
    setError('');
    setBirthDate(formData.date);
    try {
      const result = await api.post('/api/kundli/generate', {
        person_name: formData.name || 'Lal Kitab User',
        birth_date: formData.date,
        birth_time: formData.time,
        birth_place: formData.place,
        latitude: formData.latitude,
        longitude: formData.longitude,
        timezone_offset: -(new Date().getTimezoneOffset() / 60),
        gender: formData.gender,
        chart_type: 'lalkitab',
      });
      const lkChart = generateLalKitabChart(result);
      setChartData(lkChart);
      setClientId(result.client_id || '');
      setKundliId(result.id || '');
      setView('result');
    } catch (err) {
      const msg = err instanceof Error ? err.message : typeof err === 'string' ? err : 'Failed to generate Lal Kitab kundli';
      setError(msg);
      setView('form');
    }
  }, []);

  return (
    <div className="min-h-screen bg-cosmic-bg bg-mandala py-24 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-red-600 to-sacred-gold flex items-center justify-center mx-auto mb-4">
            <BookOpen className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-sacred font-bold text-sacred-gold mb-2">
            {t('lk.title')}
          </h1>
          <p className="text-cosmic-text/70 max-w-lg mx-auto">
            {t('lk.subtitle')}
          </p>
        </div>

        {/* Form View */}
        {view === 'form' && (
          <div className="max-w-xl mx-auto">
            <LalKitabForm onGenerate={handleGenerate} loading={false} />
            {error && (
              <div className="mt-4 p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-500 text-sm text-center">
                {error}
              </div>
            )}
          </div>
        )}

        {/* Generating View */}
        {view === 'generating' && (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="w-12 h-12 animate-spin text-sacred-gold mb-4" />
            <p className="text-lg font-sacred text-sacred-gold">{t('lk.generating')}</p>
          </div>
        )}

        {/* Result View */}
        {view === 'result' && chartData && (
          <div>
            <Button
              variant="outline"
              onClick={() => { setView('form'); setChartData(null); }}
              className="mb-6 border-sacred-gold/30 text-sacred-gold hover:bg-sacred-gold/10"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              {t('lk.backToForm')}
            </Button>

            <Tabs defaultValue="dashboard" className="w-full">
              <TabsList className="mb-6 bg-sacred-cream flex-wrap justify-start gap-1 h-auto p-2 [&>button]:py-2 [&>button]:text-sm [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md">
                <TabsTrigger value="dashboard">{t('lk.tab.dashboard')}</TabsTrigger>
                <TabsTrigger value="kundli">{t('lk.tab.kundli')}</TabsTrigger>
                <TabsTrigger value="planets">{t('lk.tab.planets')}</TabsTrigger>
                <TabsTrigger value="dosha">{t('lk.tab.dosha')}</TabsTrigger>
                <TabsTrigger value="remedies">{t('lk.tab.remedies')}</TabsTrigger>
                <TabsTrigger value="houses">{t('lk.tab.houses')}</TabsTrigger>
                <TabsTrigger value="yearly">{t('lk.tab.yearly')}</TabsTrigger>
                <TabsTrigger value="varshphal">{t('lk.tab.varshphal')}</TabsTrigger>
                <TabsTrigger value="relations">{t('lk.tab.relations')}</TabsTrigger>
                <TabsTrigger value="rules">{t('lk.tab.rules')}</TabsTrigger>
              </TabsList>

              <TabsContent value="dashboard">
                <LalKitabDashboardTab chartData={chartData} birthDate={birthDate} />
              </TabsContent>
              <TabsContent value="kundli">
                <LalKitabKundliTab chartData={chartData} />
              </TabsContent>
              <TabsContent value="planets">
                <LalKitabPlanetsTab chartData={chartData} />
              </TabsContent>
              <TabsContent value="dosha">
                <LalKitabDoshaTab chartData={chartData} />
              </TabsContent>
              <TabsContent value="remedies">
                <LalKitabRemediesTab chartData={chartData} />
              </TabsContent>
              <TabsContent value="houses">
                <LalKitabHousesTab chartData={chartData} />
              </TabsContent>
              <TabsContent value="yearly">
                <LalKitabYearlyTab chartData={chartData} birthDate={birthDate} />
              </TabsContent>
              <TabsContent value="varshphal">
                <LalKitabVarshphalTab chartData={chartData} birthDate={birthDate} />
              </TabsContent>
              <TabsContent value="relations">
                <LalKitabRelationsTab chartData={chartData} />
              </TabsContent>
              <TabsContent value="rules">
                <LalKitabRulesTab chartData={chartData} />
              </TabsContent>
            </Tabs>
            {clientId && <NotesWidget clientId={clientId} chartType="lalkitab" kundliId={kundliId} />}
          </div>
        )}
      </div>
    </div>
  );
}
