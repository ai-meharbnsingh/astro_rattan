import { useState, useCallback } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ArrowLeft, Loader2, Compass, Grid3X3, DoorOpen, Wrench, Home, LayoutGrid } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import VastuForm from '@/components/vastu/VastuForm';
import type { VastuFormData } from '@/components/vastu/VastuForm';
import VastuMandalaTab from '@/components/vastu/VastuMandalaTab';
import VastuEntranceTab from '@/components/vastu/VastuEntranceTab';
import VastuRemediesTab from '@/components/vastu/VastuRemediesTab';
import VastuRoomPlacementTab from '@/components/vastu/VastuRoomPlacementTab';
import VastuHomeMapperTab from '@/components/vastu/VastuHomeMapperTab';

type View = 'form' | 'generating' | 'result';

export default function VastuShastraPage() {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [view, setView] = useState<View>('form');
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('home');

  const handleGenerate = useCallback(async (formData: VastuFormData) => {
    setView('generating');
    setError('');
    try {
      const payload: any = {
        building_type: formData.buildingType,
        entrance_direction: formData.entranceDirection,
      };
      if (formData.entranceDegrees !== null) {
        payload.entrance_degrees = formData.entranceDegrees;
      }
      if (formData.problems.length > 0) {
        payload.problems = formData.problems;
      }

      const result = await api.post('/api/vastu/analyze', payload);
      setAnalysisData(result);
      setView('result');
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to analyze';
      setError(msg);
      setView('form');
    }
  }, []);

  return (
    <div className="min-h-screen bg-cosmic-bg bg-mandala py-24 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sacred-gold/10 border border-sacred-gold/20 mb-4">
            <Compass className="w-4 h-4 text-sacred-gold" />
            <span className="text-xs font-semibold text-sacred-gold tracking-wider uppercase">
              {isHi ? 'वास्तु शास्त्र' : 'Vastu Shastra'}
            </span>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">
            {isHi ? 'वास्तु शास्त्र विश्लेषण' : 'Vastu Shastra Analysis'}
          </h1>
          <p className="text-cosmic-text/70 max-w-xl mx-auto">
            {isHi
              ? '45 देवताओं का वास्तु पुरुष मंडल, 32 प्रवेश पद, और प्राचीन उपाय प्रणाली'
              : '45 Devtas Vastu Purusha Mandala, 32 Entrance Padas, and Ancient Remedial System'}
          </p>
        </div>

        {/* Form View */}
        {view === 'form' && (
          <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-8">
            <VastuForm onGenerate={handleGenerate} loading={false} />
          </div>
        )}

        {/* Loading View */}
        {view === 'generating' && (
          <div className="text-center py-20">
            <Loader2 className="w-10 h-10 animate-spin text-sacred-gold mx-auto mb-4" />
            <p className="text-lg text-white font-semibold mb-1">
              {isHi ? 'वास्तु विश्लेषण हो रहा है...' : 'Analyzing Vastu...'}
            </p>
            <p className="text-sm text-cosmic-text/60">
              {isHi ? '45 देवताओं और 32 पदों का गहन विश्लेषण' : 'Deep analysis of 45 Devtas and 32 Padas'}
            </p>
          </div>
        )}

        {/* Result View */}
        {view === 'result' && analysisData && (
          <>
            {/* Score Banner */}
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-6 flex items-center justify-between">
              <div>
                <Button
                  variant="ghost"
                  onClick={() => { setView('form'); setAnalysisData(null); }}
                  className="text-cosmic-text hover:text-white mb-2 -ml-2"
                >
                  <ArrowLeft className="w-4 h-4 mr-1" />
                  {isHi ? 'नया विश्लेषण' : 'New Analysis'}
                </Button>
                <p className="text-sm text-cosmic-text/60">{isHi ? 'वास्तु स्कोर' : 'Vastu Score'}</p>
                <p className="text-sm text-cosmic-text/70 mt-1">
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
                <p className="text-xs text-cosmic-text/40">/100</p>
              </div>
            </div>

            {/* Tabs */}
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid grid-cols-5 mb-6 bg-white/5 border border-white/10 rounded-xl p-1">
                <TabsTrigger value="home" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-xs">
                  <LayoutGrid className="w-3.5 h-3.5 mr-1" />
                  {isHi ? 'मेरा घर' : 'My Home'}
                </TabsTrigger>
                <TabsTrigger value="mandala" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-xs">
                  <Grid3X3 className="w-3.5 h-3.5 mr-1" />
                  {isHi ? '45 देवता' : '45 Devtas'}
                </TabsTrigger>
                <TabsTrigger value="entrance" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-xs">
                  <DoorOpen className="w-3.5 h-3.5 mr-1" />
                  {isHi ? 'प्रवेश पद' : 'Entrance'}
                </TabsTrigger>
                <TabsTrigger value="remedies" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-xs">
                  <Wrench className="w-3.5 h-3.5 mr-1" />
                  {isHi ? 'उपाय' : 'Remedies'}
                </TabsTrigger>
                <TabsTrigger value="rooms" className="data-[state=active]:bg-sacred-gold/20 data-[state=active]:text-sacred-gold rounded-lg text-xs">
                  <Home className="w-3.5 h-3.5 mr-1" />
                  {isHi ? 'कमरा' : 'Rooms'}
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
