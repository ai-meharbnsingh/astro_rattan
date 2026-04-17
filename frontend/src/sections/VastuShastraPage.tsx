import { useState, useCallback } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ArrowLeft, Loader2, Compass, Grid3X3, DoorOpen, Wrench, Home, LayoutGrid, Upload } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Heading } from '@/components/ui/heading';
import VastuForm from '@/components/vastu/VastuForm';
import type { VastuFormData } from '@/components/vastu/VastuForm';
import VastuMandalaTab from '@/components/vastu/VastuMandalaTab';
import VastuEntranceTab from '@/components/vastu/VastuEntranceTab';
import VastuRemediesTab from '@/components/vastu/VastuRemediesTab';
import VastuRoomPlacementTab from '@/components/vastu/VastuRoomPlacementTab';
import VastuHomeMapperTab from '@/components/vastu/VastuHomeMapperTab';

type MainMode = 'select' | 'analysis' | 'home-grid' | 'floorplan';
type AnalysisView = 'form' | 'generating' | 'result';

export default function VastuShastraPage() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [mainMode, setMainMode] = useState<MainMode>('select');
  const [analysisView, setAnalysisView] = useState<AnalysisView>('form');
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('home');

  const handleGenerate = useCallback(async (formData: VastuFormData) => {
    setAnalysisView('generating');
    setError('');
    try {
      const payload: any = {
        building_type: formData.buildingType,
        entrance_direction: formData.entranceDirection,
      };
      if (formData.entranceDegrees !== null) payload.entrance_degrees = formData.entranceDegrees;
      if (formData.problems.length > 0) payload.problems = formData.problems;
      const result = await api.post('/api/vastu/analyze', payload);
      setAnalysisData(result);
      setAnalysisView('result');
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to analyze';
      setError(msg);
      setAnalysisView('form');
    }
  }, []);

  const resetToSelect = () => {
    setMainMode('select');
    setAnalysisView('form');
    setAnalysisData(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-background bg-mandala py-24 px-4">
      <div className="max-w-5xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sacred-gold/10 border border-sacred-gold/20 mb-4">
            <Compass className="w-4 h-4 text-sacred-gold" />
            <span className="text-sm font-bold text-sacred-gold-dark tracking-wider uppercase">
              {t('auto.vastuShastra')}
            </span>
          </div>
          <Heading as={1} variant={1} className="mb-2">
            {t('auto.vastuShastraAnalysis')}
          </Heading>
          <p className="text-muted-foreground max-w-xl mx-auto">
            {t('auto.45DevtasVastuPurusha')}
          </p>
        </div>

        {/* ── Mode Selector ────────────────────────────────────────── */}
        {mainMode === 'select' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Mode 1 — Vastu Analysis */}
            <button
              onClick={() => setMainMode('analysis')}
              className="group text-left bg-white/5 hover:bg-white/10 border border-white/10 hover:border-sacred-gold/40 rounded-2xl p-6 transition-all"
            >
              <div className="w-12 h-12 rounded-xl bg-sacred-gold/10 border border-sacred-gold/20 flex items-center justify-center mb-4 group-hover:bg-sacred-gold/20 transition-colors">
                <Compass className="w-6 h-6 text-sacred-gold" />
              </div>
              <Heading as={3} variant={3} className="mb-1">
                {t('auto.vastuAnalysis')}
              </Heading>
              <p className="text-sm text-muted-foreground">
                {t('auto.enterBuildingTypeEnt')}
              </p>
              <div className="mt-4 flex flex-wrap gap-1.5">
                {(['auto.45Devtas', 'auto.32Padas', 'auto.remedies', 'auto.rooms'] as const).map(key => (
                  <span key={key} className="text-sm px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark border border-sacred-gold/20">{t(key)}</span>
                ))}
              </div>
            </button>

            {/* Mode 2 — My Home Grid */}
            <button
              onClick={() => setMainMode('home-grid')}
              className="group text-left bg-white/5 hover:bg-white/10 border border-white/10 hover:border-emerald-400/40 rounded-2xl p-6 transition-all"
            >
              <div className="w-12 h-12 rounded-xl bg-emerald-400/10 border border-emerald-400/20 flex items-center justify-center mb-4 group-hover:bg-emerald-400/20 transition-colors">
                <LayoutGrid className="w-6 h-6 text-emerald-400" />
              </div>
              <Heading as={3} variant={3} className="mb-1">
                {t('auto.myHomeGrid')}
              </Heading>
              <p className="text-sm text-muted-foreground">
                {t('auto.clickA33DirectionGri')}
              </p>
              <div className="mt-4 flex flex-wrap gap-1.5">
                {(['auto.noUploadNeeded', 'auto.instantReport', 'auto.devtaRemedies'] as const).map(key => (
                  <span key={key} className="text-sm px-2 py-0.5 rounded-full bg-emerald-400/10 text-emerald-600 border border-emerald-400/20">{t(key)}</span>
                ))}
              </div>
            </button>

            {/* Mode 3 — Floor Plan Upload */}
            <button
              onClick={() => setMainMode('floorplan')}
              className="group text-left bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-400/40 rounded-2xl p-6 transition-all"
            >
              <div className="w-12 h-12 rounded-xl bg-blue-400/10 border border-blue-400/20 flex items-center justify-center mb-4 group-hover:bg-blue-400/20 transition-colors">
                <Upload className="w-6 h-6 text-blue-400" />
              </div>
              <Heading as={3} variant={3} className="mb-1">
                {t('auto.floorPlanUpload')}
              </Heading>
              <p className="text-sm text-muted-foreground">
                {t('auto.uploadYourHomePhotoS')}
              </p>
              <div className="mt-4 flex flex-wrap gap-1.5">
                {(['auto.imageUpload', 'auto.northRotation', 'auto.clickToPlace', 'auto.zoomAndPan'] as const).map(key => (
                  <span key={key} className="text-sm px-2 py-0.5 rounded-full bg-blue-400/10 text-blue-600 border border-blue-400/20">{t(key)}</span>
                ))}
              </div>
            </button>
          </div>
        )}

        {/* ── Back button (all non-select modes) ───────────────────── */}
        {mainMode !== 'select' && (
          <button
            onClick={resetToSelect}
            className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-foreground mb-6 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            {t('auto.backToModes')}
          </button>
        )}

        {/* ── Home Grid mode ───────────────────────────────────────── */}
        {mainMode === 'home-grid' && (
          <VastuHomeMapperTab data={{}} initialMode="grid" />
        )}

        {/* ── Floor Plan mode ──────────────────────────────────────── */}
        {mainMode === 'floorplan' && (
          <VastuHomeMapperTab data={{}} initialMode="floorplan" />
        )}

        {/* ── Analysis mode ────────────────────────────────────────── */}
        {mainMode === 'analysis' && (
          <>
            {analysisView === 'form' && (
              <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-8">
                <VastuForm onGenerate={handleGenerate} loading={false} />
              </div>
            )}

            {analysisView === 'generating' && (
              <div className="text-center py-20">
                <Loader2 className="w-10 h-10 animate-spin text-sacred-gold mx-auto mb-4" />
                <p className="text-lg text-foreground font-semibold mb-1">
                  {t('auto.analyzingVastu')}
                </p>
                <p className="text-sm text-muted-foreground">
                  {t('auto.deepAnalysisOf45Devt')}
                </p>
              </div>
            )}

            {analysisView === 'result' && analysisData && (
              <>
                {/* Score Banner */}
                <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-6 flex items-center justify-between">
                  <div>
                    <Button
                      variant="ghost"
                      onClick={() => { setAnalysisView('form'); setAnalysisData(null); }}
                      className="text-foreground hover:text-white mb-2 -ml-2"
                    >
                      <ArrowLeft className="w-4 h-4 mr-1" />
                      {t('auto.newAnalysis')}
                    </Button>
                    <p className="text-sm text-gray-600">{t('auto.vastuScore')}</p>
                    <p className="text-sm text-gray-600 mt-1">
                      {isHi ? analysisData.score_label_hi : analysisData.score_label_en}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className={`text-5xl font-black ${
                      analysisData.score >= 80 ? 'text-emerald-400' :
                      analysisData.score >= 60 ? 'text-amber-400' : 'text-red-400'
                    }`}>
                      {analysisData.score}
                    </div>
                    <p className="text-sm text-gray-500">/100</p>
                  </div>
                </div>

                {/* Tabs */}
                <Tabs value={activeTab} onValueChange={setActiveTab}>
                  <TabsList className="grid grid-cols-3 sm:grid-cols-5 mb-6 bg-white/5 border border-white/10 rounded-xl p-1">
                    <TabsTrigger value="home" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-sm">
                      <LayoutGrid className="w-3.5 h-3.5 sm:mr-1" />
                      <span className="hidden sm:inline">{t('auto.myHome')}</span>
                    </TabsTrigger>
                    <TabsTrigger value="mandala" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-sm">
                      <Grid3X3 className="w-3.5 h-3.5 sm:mr-1" />
                      <span className="hidden sm:inline">{t('auto.45Devtas')}</span>
                    </TabsTrigger>
                    <TabsTrigger value="entrance" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-sm">
                      <DoorOpen className="w-3.5 h-3.5 sm:mr-1" />
                      <span className="hidden sm:inline">{t('auto.entrance')}</span>
                    </TabsTrigger>
                    <TabsTrigger value="remedies" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-sm">
                      <Wrench className="w-3.5 h-3.5 sm:mr-1" />
                      <span className="hidden sm:inline">{t('auto.remedies')}</span>
                    </TabsTrigger>
                    <TabsTrigger value="rooms" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-sm">
                      <Home className="w-3.5 h-3.5 sm:mr-1" />
                      <span className="hidden sm:inline">{t('auto.rooms')}</span>
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="home">
                    <VastuHomeMapperTab data={analysisData} />
                  </TabsContent>
                  <TabsContent value="mandala">
                    <VastuMandalaTab data={analysisData} />
                  </TabsContent>
                  <TabsContent value="entrance">
                    <VastuEntranceTab data={analysisData} />
                  </TabsContent>
                  <TabsContent value="remedies">
                    <VastuRemediesTab data={analysisData} />
                  </TabsContent>
                  <TabsContent value="rooms">
                    <VastuRoomPlacementTab data={analysisData} />
                  </TabsContent>
                </Tabs>
              </>
            )}
          </>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
