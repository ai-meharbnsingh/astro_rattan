import { useNavigate } from 'react-router-dom';
import { formatDate, api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, Download, Share2, FileText, Heart, Briefcase, Activity, ArrowLeft, Loader2, ScrollText, Home, RefreshCw } from 'lucide-react';
import { useKundliData } from '@/hooks/useKundliData';
import KundliForm from '@/components/kundli/KundliForm';
import KundliSummaryModal from '@/components/KundliSummaryModal';
import BirthDetailsTab from '@/components/kundli/BirthDetailsTab';
import LordshipsTab from '@/components/kundli/LordshipsTab';
import AspectsMatrixTab from '@/components/kundli/AspectsMatrixTab';
import KundliMilanTab from '@/components/kundli/KundliMilanTab';
import NotesWidget from '@/components/NotesWidget';
import JaiminiTab from '@/components/kundli/JaiminiTab';
import ReportTab from '@/components/kundli/ReportTab';
import PlanetsTab from '@/components/kundli/PlanetsTab';
import IogitaTab from '@/components/kundli/IogitaTab';
import DashaTab from '@/components/kundli/DashaTab';
import DivisionalTab from '@/components/kundli/DivisionalTab';
import AshtakvargaTab from '@/components/kundli/AshtakvargaTab';
import ShadbalaTab from '@/components/kundli/ShadbalaTab';
import AvakhadaTab from '@/components/kundli/AvakhadaTab';
import YogaDoshaTab from '@/components/kundli/YogaDoshaTab';
import TransitsTab from '@/components/kundli/TransitsTab';
import VarshphalTab from '@/components/kundli/VarshphalTab';
import KPTab from '@/components/kundli/KPTab';
import YoginiTab from '@/components/kundli/YoginiTab';
import UpagrahasTab from '@/components/kundli/UpagrahasTab';
import SodashvargaTab from '@/components/kundli/SodashvargaTab';
import AspectsTab from '@/components/kundli/AspectsTab';
import SadesatiTab from '@/components/kundli/SadesatiTab';
import MundaneTab from '@/components/kundli/MundaneTab';

export default function KundliGenerator() {
  const data = useKundliData();
  const {
    step, setStep, formData, setFormData, result, setResult,
    savedKundlis, error, tabError, setTabError, planets, doshaDisplay,
    // Tab data
    doshaData, loadingDosha, iogitaData, loadingIogita,
    dashaData, loadingDasha, extendedDashaData, loadingExtendedDasha,
    avakhadaData, loadingAvakhada, yogaDoshaData, loadingYogaDosha,
    divisionalData, loadingDivisional, ashtakvargaData, loadingAshtakvarga,
    shadbalaData, loadingShadbala, transitData, loadingTransit,
    d10Data, loadingD10, varshphalData, loadingVarshphal,
    yoginiData, loadingYogini, kpData, loadingKp,
    upagrahasData, loadingUpagrahas, sodashvargaData, loadingSodashvarga,
    aspectsData, loadingAspects, westernAspectsData, loadingWesternAspects,
    jaiminiData, loadingJaimini, sadesatiData, loadingSadesati,
    predictionsData, loadingPredictions, activePredictionPeriod,
    // UI state
    selectedDivision, expandedMahadasha, setExpandedMahadasha,
    expandedAntardasha, setExpandedAntardasha,
    transitHouseShift, setTransitHouseShift,
    reportLagnaShift, setReportLagnaShift,
    reportMoonShift, setReportMoonShift,
    reportGocharShift, setReportGocharShift,
    transitDate, setTransitDate, transitTime, setTransitTime,
    varshphalYear, sidePanel, setSidePanel,
    reportOpen, setReportOpen, summaryOpen, setSummaryOpen,
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
    HOUSE_SIGNIFICANCE,
    // i18n
    t, language,
  } = data;

  const navigate = useNavigate();

  // --- LOADING ---
  if (step === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  // --- LIST → go to dashboard ---
  if (step === 'list') {
    navigate('/dashboard');
    return null;
  }

  // --- GENERATING SKELETON ---
  if (step === 'generating') {
    return (
      <div className="max-w-7xl mx-auto pt-24 pb-48 px-4">
        {/* Header skeleton */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 animate-pulse bg-gray-200 rounded" />
          <div className="space-y-2 flex-1">
            <div className="h-6 w-48 animate-pulse bg-gray-200 rounded" />
            <div className="h-4 w-72 animate-pulse bg-gray-200 rounded" />
          </div>
        </div>
        {/* Tab bar skeleton */}
        <div className="flex gap-2 mb-6 overflow-hidden">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-10 w-24 animate-pulse bg-gray-200 rounded flex-shrink-0" />
          ))}
        </div>
        {/* Content skeleton cards */}
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="h-40 animate-pulse bg-gray-200 rounded-xl" />
            <div className="h-28 animate-pulse bg-gray-200 rounded-xl" />
          </div>
          <div className="space-y-4">
            <div className="h-52 animate-pulse bg-gray-200 rounded-xl" />
            <div className="h-16 animate-pulse bg-gray-200 rounded-xl" />
          </div>
        </div>
        <p className="text-center text-cosmic-text mt-8 animate-pulse">{t('kundli.analyzingPositions')}</p>
      </div>
    );
  }

  // --- RESULT VIEW ---
  if (step === 'result' && result) {
    return (
      <div className="max-w-7xl mx-auto pt-24 pb-48 px-4 bg-transparent">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-10">
          <div className="flex items-center gap-3 min-w-0">
            <Button variant="ghost" size="sm" onClick={() => navigate('/dashboard')} title="Dashboard" className="flex-shrink-0">
              <Home className="w-4 h-4" />
            </Button>
            <div className="min-w-0">
              <h3 className="font-display font-bold text-xl sm:text-2xl text-sacred-brown truncate">{result.person_name || formData.name} — {t('tab.kundli')}</h3>
              <p className="text-sm text-gray-500 truncate">{formatDate(result.birth_date) || formData.date} | {result.birth_time || formData.time} | {result.birth_place || formData.place}</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 flex-shrink-0">
            <Button variant="outline" size="sm" className="border-sacred-gold text-sacred-brown"
              onClick={async () => {
                try {
                  const fresh = await api.post(`/api/kundli/${result.id}/regenerate`, {});
                  setResult(fresh);
                  resetTabData();
                  alert('Chart regenerated with latest Swiss Ephemeris data');
                } catch (e) { console.error(e); alert('Regeneration failed'); }
              }}>
              <RefreshCw className="w-4 h-4 mr-1" />{language === 'hi' ? 'पुनः गणना' : 'Regenerate'}
            </Button>
            <Button variant="outline" size="sm" className="border-sacred-gold text-sacred-brown" onClick={async () => {
              const shareData = {
                title: `Kundli - ${result.person_name}`,
                text: `Vedic Kundli for ${result.person_name}, generated on Astro Rattan`,
                url: window.location.href,
              };
              try {
                if (navigator.share) {
                  await navigator.share(shareData);
                } else {
                  await navigator.clipboard.writeText(`${shareData.title}\n${shareData.text}\n${shareData.url}`);
                  alert(language === 'hi' ? 'लिंक कॉपी हो गया!' : 'Link copied to clipboard!');
                }
              } catch (e) {
                if ((e as Error).name !== 'AbortError') console.error(e);
              }
            }}>
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

        {/* Tabs */}
        <Tabs defaultValue="report" className="w-full">
          <div className="relative mb-8">
            {/* Left arrow hint */}
            <div className="absolute left-0 top-0 bottom-0 w-8 bg-gradient-to-r from-sacred-cream to-transparent z-10 pointer-events-none flex items-center justify-start pl-1">
              <span className="text-sacred-gold-dark text-lg">‹</span>
            </div>
            {/* Right arrow hint */}
            <div className="absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-sacred-cream to-transparent z-10 pointer-events-none flex items-center justify-end pr-1">
              <span className="text-sacred-gold-dark text-lg">›</span>
            </div>
          <TabsList className="bg-sacred-cream flex flex-nowrap overflow-x-auto w-full h-auto p-2 gap-1 pb-3 scrollbar-hide [&>button]:flex-shrink-0 [&>button]:flex-grow-0 [&>button]:basis-auto [&>button]:whitespace-nowrap [&>button]:min-h-[40px] [&>button]:px-3 [&>button]:py-2 [&>button]:text-sm [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md">
            <TabsTrigger value="report" onClick={async () => { await fetchDasha(); fetchExtendedDasha(); fetchAvakhada(); fetchYogaDosha(); fetchShadbala(); }}><ScrollText className="w-3 h-3 mr-1" />{t('tab.report')}</TabsTrigger>
            <TabsTrigger value="planets">{t('tab.planets')}</TabsTrigger>
            <TabsTrigger value="details">{t('tab.details')}</TabsTrigger>
            <TabsTrigger value="lordships">{t('tab.lordships')}</TabsTrigger>
            <TabsTrigger value="iogita" onClick={fetchIogita}>{t('tab.iogita')}</TabsTrigger>
            <TabsTrigger value="dasha" onClick={() => { fetchDasha(); fetchExtendedDasha(); }}>{t('tab.dasha')}</TabsTrigger>
            <TabsTrigger value="divisional" onClick={() => fetchDivisional()}>{t('tab.divisional')}</TabsTrigger>
            <TabsTrigger value="ashtakvarga" onClick={fetchAshtakvarga}>{t('tab.ashtakvarga')}</TabsTrigger>
            <TabsTrigger value="shadbala" onClick={fetchShadbala}>{t('tab.shadbala')}</TabsTrigger>
            <TabsTrigger value="avakhada" onClick={fetchAvakhada}>{t('tab.avakhada')}</TabsTrigger>
            <TabsTrigger value="yoga-dosha" onClick={() => { fetchYogaDosha(); fetchDosha(); }}>{language === 'hi' ? 'योग/दोष' : 'Yogas/Dosha'}</TabsTrigger>
            <TabsTrigger value="transits" onClick={() => fetchTransit()}>{t('tab.transits')}</TabsTrigger>
            <TabsTrigger value="varshphal" onClick={() => fetchVarshphal()}>{t('tab.varshphal')}</TabsTrigger>
            <TabsTrigger value="kp" onClick={fetchKp}>{t('tab.kpSystem')}</TabsTrigger>
            <TabsTrigger value="yogini" onClick={fetchYogini}>{t('tab.yoginiDasha')}</TabsTrigger>
            <TabsTrigger value="upagrahas" onClick={fetchUpagrahas}>{t('tab.upagrahas')}</TabsTrigger>
            <TabsTrigger value="sodashvarga" onClick={fetchSodashvarga}>{t('tab.sodashvarga')}</TabsTrigger>
            <TabsTrigger value="aspects" onClick={fetchAspects}>{t('tab.aspects')}</TabsTrigger>
            <TabsTrigger value="aspects-matrix" onClick={fetchWesternAspects}>{language === 'hi' ? 'दृष्टि मैट्रिक्स' : 'Aspects Matrix'}</TabsTrigger>
            <TabsTrigger value="jaimini" onClick={fetchJaimini}>{language === 'hi' ? 'जैमिनी' : 'Jaimini'}</TabsTrigger>
            <TabsTrigger value="sadesati" onClick={fetchSadesati}>{t('tab.sadeSati')}</TabsTrigger>
            <TabsTrigger value="mundane">{language === 'hi' ? 'मुंडन ज्योतिष' : 'Mundane'}</TabsTrigger>
            <TabsTrigger value="milan">{language === 'hi' ? 'कुंडली मिलान' : 'Kundli Milan'}</TabsTrigger>
          </TabsList>
          </div>

          {tabError && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 flex items-center justify-between">
              <p className="text-sm text-red-700">{tabError}</p>
              <button onClick={() => setTabError(null)} className="text-red-500 hover:text-red-700 text-sm font-medium ml-3">Dismiss</button>
            </div>
          )}

          <TabsContent value="report" className="min-h-[300px]">
            <ReportTab
              result={result} planets={planets} formData={formData} language={language} t={t}
              doshaData={doshaData} loadingDosha={loadingDosha}
              dashaData={dashaData} loadingDasha={loadingDasha}
              extendedDashaData={extendedDashaData} loadingExtendedDasha={loadingExtendedDasha}
              avakhadaData={avakhadaData} loadingAvakhada={loadingAvakhada}
              yogaDoshaData={yogaDoshaData} loadingYogaDosha={loadingYogaDosha}
              ashtakvargaData={ashtakvargaData} loadingAshtakvarga={loadingAshtakvarga}
              shadbalaData={shadbalaData} loadingShadbala={loadingShadbala}
              divisionalData={divisionalData} loadingDivisional={loadingDivisional}
              transitData={transitData} loadingTransit={loadingTransit}
              d10Data={d10Data} loadingD10={loadingD10}
              selectedDivision={selectedDivision}
              reportLagnaShift={reportLagnaShift} setReportLagnaShift={setReportLagnaShift}
              reportMoonShift={reportMoonShift} setReportMoonShift={setReportMoonShift}
              reportGocharShift={reportGocharShift} setReportGocharShift={setReportGocharShift}
              expandedMahadasha={expandedMahadasha} setExpandedMahadasha={setExpandedMahadasha}
              expandedAntardasha={expandedAntardasha} setExpandedAntardasha={setExpandedAntardasha}
              jhoraOpen={jhoraOpen} setJhoraOpen={setJhoraOpen}
              reportOpen={reportOpen} setReportOpen={setReportOpen}
              fetchTransit={fetchTransit} fetchD10={fetchD10}
              fetchDasha={fetchDasha} fetchExtendedDasha={fetchExtendedDasha}
              changeDivision={changeDivision}
              handlePlanetClick={handlePlanetClick} handleHouseClick={handleHouseClick}
            />
          </TabsContent>

          <TabsContent value="planets" className="min-h-[300px]">
            <PlanetsTab
              planets={planets} result={result}
              sidePanel={sidePanel} setSidePanel={setSidePanel}
              handlePlanetClick={handlePlanetClick} handleHouseClick={handleHouseClick}
              language={language} t={t} HOUSE_SIGNIFICANCE={HOUSE_SIGNIFICANCE}
            />
          </TabsContent>

          <TabsContent value="details" className="min-h-[300px]">
            <BirthDetailsTab planets={planets} />
          </TabsContent>

          <TabsContent value="lordships" className="min-h-[300px]">
            <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
          </TabsContent>

          <TabsContent value="iogita" className="min-h-[300px]">
            <IogitaTab iogitaData={iogitaData} loadingIogita={loadingIogita} language={language} t={t} />
          </TabsContent>

          <TabsContent value="dasha" className="min-h-[300px]">
            <DashaTab
              dashaData={dashaData} extendedDashaData={extendedDashaData}
              loadingDasha={loadingDasha} loadingExtendedDasha={loadingExtendedDasha}
              expandedMahadasha={expandedMahadasha} setExpandedMahadasha={setExpandedMahadasha}
              expandedAntardasha={expandedAntardasha} setExpandedAntardasha={setExpandedAntardasha}
              language={language} t={t}
            />
          </TabsContent>

          <TabsContent value="divisional" className="min-h-[300px]">
            <DivisionalTab
              divisionalData={divisionalData} loadingDivisional={loadingDivisional}
              selectedDivision={selectedDivision} changeDivision={changeDivision}
              handlePlanetClick={handlePlanetClick} handleHouseClick={handleHouseClick}
              language={language} t={t}
            />
          </TabsContent>

          <TabsContent value="ashtakvarga" className="min-h-[300px]">
            <AshtakvargaTab
              ashtakvargaData={ashtakvargaData} loadingAshtakvarga={loadingAshtakvarga}
              result={result} language={language} t={t}
            />
          </TabsContent>

          <TabsContent value="shadbala" className="min-h-[300px]">
            <ShadbalaTab shadbalaData={shadbalaData} loadingShadbala={loadingShadbala} language={language} t={t} />
          </TabsContent>

          <TabsContent value="avakhada" className="min-h-[300px]">
            <AvakhadaTab avakhadaData={avakhadaData} loadingAvakhada={loadingAvakhada} t={t} />
          </TabsContent>

          <TabsContent value="yoga-dosha" className="min-h-[300px]">
            <YogaDoshaTab yogaDoshaData={yogaDoshaData} loadingYogaDosha={loadingYogaDosha} doshaDisplay={doshaDisplay} doshaData={doshaData} loadingDosha={loadingDosha} language={language} t={t} />
          </TabsContent>


          <TabsContent value="transits" className="min-h-[300px]">
            <TransitsTab
              transitData={transitData} loadingTransit={loadingTransit}
              transitHouseShift={transitHouseShift} setTransitHouseShift={setTransitHouseShift}
              transitDate={transitDate} setTransitDate={setTransitDate}
              transitTime={transitTime} setTransitTime={setTransitTime}
              result={result} language={language} t={t}
              refreshTransit={refreshTransit} resetTransitFilters={resetTransitFilters}
            />
          </TabsContent>

          <TabsContent value="varshphal" className="min-h-[300px]">
            <VarshphalTab
              varshphalData={varshphalData} loadingVarshphal={loadingVarshphal}
              varshphalYear={varshphalYear} changeVarshphalYear={changeVarshphalYear}
              handlePlanetClick={handlePlanetClick} handleHouseClick={handleHouseClick}
              language={language} t={t}
            />
          </TabsContent>

          <TabsContent value="kp" className="min-h-[300px]">
            <KPTab kpData={kpData} loadingKp={loadingKp} result={result} language={language} t={t} />
          </TabsContent>

          <TabsContent value="yogini" className="min-h-[300px]">
            <YoginiTab yoginiData={yoginiData} loadingYogini={loadingYogini} language={language} t={t} />
          </TabsContent>

          <TabsContent value="upagrahas" className="min-h-[300px]">
            <UpagrahasTab upagrahasData={upagrahasData} loadingUpagrahas={loadingUpagrahas} language={language} t={t} />
          </TabsContent>

          <TabsContent value="sodashvarga" className="min-h-[300px]">
            <SodashvargaTab sodashvargaData={sodashvargaData} loadingSodashvarga={loadingSodashvarga} language={language} t={t} />
          </TabsContent>

          <TabsContent value="aspects" className="min-h-[300px]">
            <AspectsTab aspectsData={aspectsData} loadingAspects={loadingAspects} language={language} t={t} />
          </TabsContent>

          <TabsContent value="aspects-matrix" className="min-h-[300px]">
            <AspectsMatrixTab data={westernAspectsData} loading={loadingWesternAspects} />
          </TabsContent>


          <TabsContent value="jaimini" className="min-h-[300px]">
            <JaiminiTab data={jaiminiData} loading={loadingJaimini} />
          </TabsContent>

          <TabsContent value="sadesati" className="min-h-[300px]">
            <SadesatiTab sadesatiData={sadesatiData} loadingSadesati={loadingSadesati} doshaData={doshaData} language={language} t={t} />
          </TabsContent>

          <TabsContent value="mundane" className="min-h-[300px]">
            <MundaneTab language={language} />
          </TabsContent>

          <TabsContent value="milan" className="min-h-[300px]">
            <KundliMilanTab savedKundlis={savedKundlis} currentKundliId={result?.id} />
          </TabsContent>
        </Tabs>

        <div className="mt-8 mb-16 text-center">
          <Button onClick={() => { setStep('form'); setResult(null); resetTabData(); }} variant="outline" className="border-cosmic-text-muted text-cosmic-text">
            {t('common.generateAnother')}
          </Button>
        </div>

        {/* Summary Modal */}
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
          }}
        />
        {result?.client_id && <NotesWidget clientId={result.client_id} chartType="vedic" kundliId={result.id} />}
      </div>
    );
  }

  // --- FORM VIEW ---
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
