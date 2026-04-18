import { useState, useRef, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useTranslation } from '@/lib/i18n';
import { formatDate, api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Heading } from '@/components/ui/heading';
import { Download, Share2, Loader2, ScrollText, Home, RefreshCw, ChevronDown, X, BookOpen, Star, Clock3, Sparkles, Grid3X3, Eye } from 'lucide-react';
import { useKundliData } from '@/hooks/useKundliData';
import KundliForm from '@/components/kundli/KundliForm';
import KundliSummaryModal from '@/components/KundliSummaryModal';
import ConsolidatedReport from '@/components/kundli/ConsolidatedReport';
import JHoraKundliView from '@/components/kundli/JHoraKundliView';
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
import AshtakvargaPhalaTab from '@/components/kundli/AshtakvargaPhalaTab';
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
import DashaSelector from '@/components/kundli/DashaSelector';
import DashaPhalaTab from '@/components/kundli/DashaPhalaTab';
import D108Analysis from '@/components/kundli/D108Analysis';
import ChartAnimation from '@/components/kundli/ChartAnimation';
import BirthRectification from '@/components/kundli/BirthRectification';
import KPHorary from '@/components/kp/KPHorary';
import SarvatobhadraChakra from '@/components/sarvatobhadra/SarvatobhadraChakra';
import PravrajyaTab from '@/components/kundli/PravrajyaTab';
import ApatyaTab from '@/components/kundli/ApatyaTab';
import StriJatakaTab from '@/components/kundli/StriJatakaTab';
import LifespanTab from '@/components/kundli/LifespanTab';
import ConjunctionsTab from '@/components/kundli/ConjunctionsTab';
import RogaTab from '@/components/kundli/RogaTab';
import BhavaPhalaTab from '@/components/kundli/BhavaPhalaTab';
import VrittiTab from '@/components/kundli/VrittiTab';
import BhavaVicharaTab from '@/components/kundli/BhavaVicharaTab';
import LongevityTab from '@/components/kundli/LongevityTab';
import JanmaPredictionsTab from '@/components/kundli/JanmaPredictionsTab';

// ── Single source of truth for ALL tab definitions ──────────
interface TabDef {
  value: string;
  labelEn: string;
  labelHi: string;
  i18nKey?: string; // if we use t() for label
  primary: boolean;
  category?: 'charts' | 'timing' | 'analysis' | 'advanced';
  icon?: React.ComponentType<{ className?: string }>;
  onActivate?: () => void; // set dynamically below
}

const TAB_DEFS: Omit<TabDef, 'onActivate'>[] = [
  // Primary tabs
  { value: 'report',        labelEn: 'Report',         labelHi: 'रिपोर्ट',          primary: true, icon: ScrollText },
  { value: 'planets',       labelEn: 'Planets',        labelHi: 'ग्रह',             primary: true, icon: Star },
  { value: 'dasha',         labelEn: 'Dasha',          labelHi: 'दशा',             primary: true, icon: Clock3 },
  { value: 'yoga-dosha',    labelEn: 'Yogas/Dosha',    labelHi: 'योग/दोष',          primary: true, icon: Sparkles },
  { value: 'divisional',    labelEn: 'Divisional',     labelHi: 'विभाजन चार्ट',     primary: true, icon: Grid3X3 },
  { value: 'aspects',       labelEn: 'Aspects',        labelHi: 'दृष्टि',           primary: true, icon: Eye },
  // Charts
  { value: 'ashtakvarga',   labelEn: 'Ashtakvarga',    labelHi: 'अष्टकवर्ग',        primary: false, category: 'charts' },
  { value: 'ashtakvarga-phala', labelEn: 'Ashtakvarga Effects', labelHi: 'अष्टकवर्ग फल', primary: false, category: 'analysis' },
  { value: 'sodashvarga',   labelEn: 'Sodashvarga',    labelHi: 'षोडशवर्ग',         primary: false, category: 'charts' },
  { value: 'd108',          labelEn: 'D108 Chart',     labelHi: 'D108 अष्टोत्तरांश',  primary: false, category: 'charts' },
  { value: 'animation',     labelEn: 'Chart Animation', labelHi: 'चार्ट एनिमेशन',    primary: false, category: 'charts' },
  { value: 'sarvatobhadra', labelEn: 'Sarvatobhadra',   labelHi: 'सर्वतोभद्र चक्र',   primary: false, category: 'charts' },
  // Timing
  { value: 'yogini',        labelEn: 'Yogini Dasha',   labelHi: 'योगिनी दशा',       primary: false, category: 'timing' },
  { value: 'dasha-phala',   labelEn: 'Dasha Effects',  labelHi: 'दशा फल',           primary: false, category: 'timing' },
  // dasha-systems merged into "dasha" tab via DashaSelector (5 systems in one)
  { value: 'varshphal',     labelEn: 'Varshphal',      labelHi: 'वर्षफल',           primary: false, category: 'timing' },
  { value: 'transits',      labelEn: 'Transits',       labelHi: 'गोचर',            primary: false, category: 'timing' },
  { value: 'sadesati',      labelEn: 'Sade Sati',      labelHi: 'साढ़े साती',        primary: false, category: 'timing' },
  // Analysis
  { value: 'shadbala',      labelEn: 'Shadbala',       labelHi: 'षड्बल',            primary: false, category: 'analysis' },
  { value: 'kp',            labelEn: 'KP System',      labelHi: 'केपी सिस्टम',      primary: false, category: 'analysis' },
  { value: 'kp-horary',     labelEn: 'KP Horary',     labelHi: 'केपी प्रश्न',       primary: false, category: 'analysis' },
  { value: 'jaimini',       labelEn: 'Jaimini',        labelHi: 'जैमिनी',           primary: false, category: 'analysis' },
  { value: 'pravrajya',     labelEn: 'Pravrajya Yogas', labelHi: 'प्रव्रज्या योग',   primary: false, category: 'analysis' },
  { value: 'apatya',        labelEn: 'Progeny (Apatya)',labelHi: 'संतान',             primary: false, category: 'analysis' },
  { value: 'stri-jataka',   labelEn: 'Stri Jataka',     labelHi: 'स्त्री जातक',       primary: false, category: 'analysis' },
  { value: 'lifespan',      labelEn: 'Lifespan',        labelHi: 'आयुर्दाय',         primary: false, category: 'analysis' },
  { value: 'conjunctions',  labelEn: 'Conjunctions',    labelHi: 'ग्रह युतियाँ',      primary: false, category: 'analysis' },
  { value: 'roga',          labelEn: 'Disease Analysis', labelHi: 'रोग विश्लेषण',     primary: false, category: 'analysis' },
  { value: 'bhava-phala',   labelEn: 'Bhava Phala',    labelHi: 'भाव फल',           primary: false, category: 'analysis' },
  { value: 'vritti',        labelEn: 'Career (Vritti)', labelHi: 'आजीविका',          primary: false, category: 'analysis' },
  { value: 'janma-predictions', labelEn: 'Janma Predictions', labelHi: 'जन्म फल',       primary: false, category: 'analysis' },
  { value: 'iogita',        labelEn: 'Iogita',         labelHi: 'आयोगिता',          primary: false, category: 'analysis' },
  { value: 'aspects-matrix',labelEn: 'Aspects Matrix',  labelHi: 'दृष्टि मैट्रिक्स', primary: false, category: 'analysis' },
  // Advanced
  { value: 'bhava-vichara', labelEn: 'Bhava Analysis', labelHi: 'भाव विचार',        primary: false, category: 'advanced' },
  { value: 'longevity',     labelEn: 'Longevity Indicators', labelHi: 'आयु संकेतक',  primary: false, category: 'advanced' },
  { value: 'mundane',       labelEn: 'Mundane',        labelHi: 'मुंडन ज्योतिष',    primary: false, category: 'advanced' },
  { value: 'rectification', labelEn: 'Birth Rectification', labelHi: 'जन्म समय शोधन', primary: false, category: 'advanced' },
  { value: 'upagrahas',     labelEn: 'Upagrahas',      labelHi: 'उपग्रह',           primary: false, category: 'advanced' },
  { value: 'lordships',     labelEn: 'Lordships',      labelHi: 'लॉर्डशिप',         primary: false, category: 'advanced' },
  { value: 'details',       labelEn: 'Birth Details',   labelHi: 'विवरण',            primary: false, category: 'advanced' },
  { value: 'avakhada',      labelEn: 'Avakhada',       labelHi: 'अवखड़ा',           primary: false, category: 'advanced' },
  { value: 'milan',         labelEn: 'Kundli Milan',   labelHi: 'कुंडली मिलान',     primary: false, category: 'advanced' },
];

const CATEGORY_LABELS: Record<string, { en: string; hi: string }> = {
  charts:   { en: 'Charts',   hi: 'चार्ट' },
  timing:   { en: 'Timing',   hi: 'समय' },
  analysis: { en: 'Analysis', hi: 'विश्लेषण' },
  advanced: { en: 'Advanced', hi: 'उन्नत' },
};

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
    predictionsData: _predictionsData, loadingPredictions: _loadingPredictions, activePredictionPeriod: _activePredictionPeriod,
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
    fetchPredictions: _fetchPredictions, fetchSavedKundlis: _fetchSavedKundlis,
    // Convenience
    changeDivision, refreshTransit, changeVarshphalYear, resetTransitFilters,
    // Handlers
    handlePlanetClick, handleHouseClick,
    handleGenerate, handlePrashnaKundli,
    loadKundli: _loadKundli, resetTabData,
    // Computed
    HOUSE_SIGNIFICANCE,
    // i18n
    t: tFromHook, language: langFromHook,
  } = data;

  const { t: tDirect, language: langDirect } = useTranslation();
  const t = tFromHook || tDirect;
  const language = langFromHook || langDirect;

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const urlMode = searchParams.get('mode') ?? '';
  const [activeTab, setActiveTab] = useState('report');
  const [showMoreTabs, setShowMoreTabs] = useState(false);
  const [showMobileMoreSheet, setShowMobileMoreSheet] = useState(false);
  const moreDropdownRef = useRef<HTMLDivElement>(null);

  // Sarvatobhadra Chakra state
  const [sbcGrid, setSbcGrid] = useState<any[][] | null>(null);
  const [sbcVedhas, setSbcVedhas] = useState<any[]>([]);
  const [loadingSbc, setLoadingSbc] = useState(false);

  // Close desktop dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (moreDropdownRef.current && !moreDropdownRef.current.contains(e.target as Node)) {
        setShowMoreTabs(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // Auto-activate rectification tab when result arrives in rectification mode
  useEffect(() => {
    if (urlMode === 'rectification' && step === 'result') {
      setActiveTab('rectification');
    }
  }, [step, urlMode]);

  // Fetch Sarvatobhadra Chakra data
  const fetchSarvatobhadra = async () => {
    if (sbcGrid || !result?.id) return;
    setLoadingSbc(true);
    try {
      const res = await api.get(`/api/kundli/${result.id}/sarvatobhadra`);
      setSbcGrid(res.grid || null);
      setSbcVedhas(res.vedhas || []);
    } catch (err) {
      console.error('Failed to load Sarvatobhadra data', err);
    } finally {
      setLoadingSbc(false);
    }
  };

  // Map of tab value -> onActivate fetch function
  const tabActivateMap: Record<string, () => void> = {
    'report': async () => { await fetchDasha(); fetchExtendedDasha(); fetchAvakhada(); fetchYogaDosha(); fetchShadbala(); },
    'iogita': fetchIogita,
    'dasha': () => { fetchDasha(); fetchExtendedDasha(); },
    'divisional': () => fetchDivisional(),
    'ashtakvarga': fetchAshtakvarga,
    'shadbala': fetchShadbala,
    'avakhada': fetchAvakhada,
    'yoga-dosha': () => { fetchYogaDosha(); fetchDosha(); },
    'transits': () => fetchTransit(),
    'varshphal': () => fetchVarshphal(),
    'kp': fetchKp,
    'yogini': fetchYogini,
    'upagrahas': fetchUpagrahas,
    'sodashvarga': fetchSodashvarga,
    'aspects': fetchAspects,
    'aspects-matrix': fetchWesternAspects,
    'jaimini': fetchJaimini,
    'sadesati': fetchSadesati,
    'sarvatobhadra': fetchSarvatobhadra,
  };

  const handleTabChange = (tabValue: string) => {
    setActiveTab(tabValue);
    setShowMoreTabs(false);
    setShowMobileMoreSheet(false);
    const activator = tabActivateMap[tabValue];
    if (activator) activator();
  };

  const hi = language === 'hi';
  const primaryTabs = TAB_DEFS.filter(t => t.primary);
  const moreTabs = TAB_DEFS.filter(t => !t.primary);

  // Group secondary tabs by category
  const groupedMoreTabs = (['charts', 'timing', 'analysis', 'advanced'] as const).map(cat => ({
    category: cat,
    label: CATEGORY_LABELS[cat],
    tabs: moreTabs.filter(t => t.category === cat),
  })).filter(g => g.tabs.length > 0);

  // Check if current active tab is a "more" tab
  const isMoreTabActive = moreTabs.some(t => t.value === activeTab);

  // --- LOADING ---
  if (step === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  // --- LIST -> go to dashboard ---
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
          <div className="w-10 h-10 animate-pulse bg-sacred-gold/15 rounded" />
          <div className="space-y-2 flex-1">
            <div className="h-6 w-48 animate-pulse bg-sacred-gold/15 rounded" />
            <div className="h-4 w-72 animate-pulse bg-sacred-gold/15 rounded" />
          </div>
        </div>
        {/* Tab bar skeleton */}
        <div className="flex gap-2 mb-6 overflow-hidden">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-10 w-24 animate-pulse bg-sacred-gold/15 rounded flex-shrink-0" />
          ))}
        </div>
        {/* Content skeleton cards */}
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="h-40 animate-pulse bg-sacred-gold/15 rounded-xl" />
            <div className="h-28 animate-pulse bg-sacred-gold/15 rounded-xl" />
          </div>
          <div className="space-y-4">
            <div className="h-52 animate-pulse bg-sacred-gold/15 rounded-xl" />
            <div className="h-16 animate-pulse bg-sacred-gold/15 rounded-xl" />
          </div>
        </div>
        <p className="text-center text-foreground mt-8 animate-pulse">{t('kundli.analyzingPositions')}</p>
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
            <Button variant="ghost" size="sm" onClick={() => navigate('/dashboard')} title={t('nav.dashboard')} className="flex-shrink-0">
              <Home className="w-4 h-4" />
            </Button>
            <div className="min-w-0">
              <h3 className=" font-bold text-xl sm:text-2xl text-sacred-brown truncate">{result.person_name || formData.name} — {t('tab.kundli')}</h3>
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
                  alert(t('auto.chartRegeneratedWith'));
                } catch { alert(t('auto.regenerationFailed')); }
              }}>
              <RefreshCw className="w-4 h-4 mr-1" />{t('auto.regenerate')}
            </Button>
            <Button variant="outline" size="sm" className="border-sacred-gold text-sacred-brown"
              onClick={() => {
                fetchTransit();
                fetchD10();
                fetchDasha();
                fetchExtendedDasha();
                setJhoraOpen(true);
              }}>
              <ScrollText className="w-4 h-4 mr-1" />{t('kundli.jhoraView')}
            </Button>
            <Button variant="outline" size="sm" className="border-sacred-gold text-sacred-brown"
              onClick={() => {
                fetchTransit();
                setReportOpen(true);
              }}>
              <ScrollText className="w-4 h-4 mr-1" />{t('kundli.fullReport')}
            </Button>
            <Button size="sm"
              className="bg-gradient-to-r from-sacred-gold to-sacred-gold-dark text-white hover:from-sacred-gold/90 hover:to-sacred-gold-dark/90 font-semibold border border-sacred-gold-dark/30 shadow-md"
              onClick={() => {
                if (!result?.id) return;
                const token = localStorage.getItem('astrorattan_token') || '';
                const a = document.createElement('a');
                a.href = `/api/kundli/${result.id}/full-report?token=${encodeURIComponent(token)}&lang=${language}`;
                a.download = `Kundli_Report_${result.person_name || 'chart'}.pdf`;
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
                setTimeout(() => document.body.removeChild(a), 1000);
              }}>
              <BookOpen className="w-4 h-4 mr-1" />{t('auto.downloadFullReportPD')}
            </Button>
          </div>
        </div>

        {/* Tabs — controlled mode */}
        <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full kundli-tabs">
          <div className="mb-4">
            <TabsList className="bg-sacred-gold/5 border border-sacred-gold/20 w-full h-auto p-2 gap-1 grid grid-cols-6
              [&>button]:min-w-0 [&>button]:min-h-[58px] [&>button]:px-1 [&>button]:py-2 [&>button]:text-[11px] md:[&>button]:text-xs
              [&>button]:flex [&>button]:flex-col [&>button]:items-center [&>button]:justify-center [&>button]:gap-1 [&>button]:leading-tight
              [&>button]:text-sacred-gold-dark/70 [&>button:hover]:bg-sacred-gold/10 [&>button:hover]:text-sacred-gold-dark
              [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md">
              {primaryTabs.map(tab => (
                <TabsTrigger key={tab.value} value={tab.value}>
                  {tab.icon && <tab.icon className="w-3.5 h-3.5" />}
                  <span className="truncate max-w-full">{hi ? tab.labelHi : tab.labelEn}</span>
                </TabsTrigger>
              ))}
            </TabsList>
            {/* "More Analysis" dropdown button */}
            <div className="relative mt-1" ref={moreDropdownRef}>
              <button
                onClick={() => setShowMoreTabs(prev => !prev)}
                className={`inline-flex items-center gap-1.5 px-4 py-2 text-xs font-medium rounded-md border transition-colors ${
                  isMoreTabActive
                    ? 'bg-sacred-gold/20 border-sacred-gold text-sacred-gold-dark'
                    : 'bg-muted border-sacred-gold/40 text-foreground hover:bg-sacred-gold/10'
                }`}
              >
                {t('auto.moreAnalysis')}
                <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showMoreTabs ? 'rotate-180' : ''}`} />
              </button>
              {showMoreTabs && (
                <div className="absolute top-full left-0 mt-1 z-50 bg-white border border-sacred-gold/30 rounded-xl shadow-xl p-4 min-w-[420px] grid grid-cols-2 gap-4">
                  {groupedMoreTabs.map(group => (
                    <div key={group.category}>
                      <p className="text-[10px] font-semibold uppercase tracking-wider text-sacred-gold-dark mb-2">
                        {hi ? group.label.hi : group.label.en}
                      </p>
                      <div className="space-y-0.5">
                        {group.tabs.map(tab => (
                          <button
                            key={tab.value}
                            onClick={() => handleTabChange(tab.value)}
                            className={`w-full text-left px-3 py-1.5 rounded-md text-xs transition-colors ${
                              activeTab === tab.value
                                ? 'bg-sacred-gold-dark text-white font-medium'
                                : 'text-foreground hover:bg-sacred-gold/10'
                            }`}
                          >
                            {hi ? tab.labelHi : tab.labelEn}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* "More" button for mobile */}
          <div className="mb-8 md:hidden">
            <button
              onClick={() => setShowMobileMoreSheet(true)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${
                isMoreTabActive
                  ? 'bg-sacred-gold/20 border-sacred-gold text-sacred-gold-dark'
                  : 'bg-muted border-sacred-gold/40 text-foreground'
              }`}
            >
              {t('auto.moreAnalysis')}
              <ChevronDown className="w-3 h-3" />
            </button>
          </div>

          {/* Mobile "More" bottom sheet overlay */}
          {showMobileMoreSheet && (
            <div className="fixed inset-0 z-50 md:hidden">
              <div className="absolute inset-0 bg-black/50" onClick={() => setShowMobileMoreSheet(false)} />
              <div className="absolute bottom-0 left-0 right-0 bg-white rounded-t-2xl max-h-[70vh] overflow-y-auto p-5 pb-8 animate-in slide-in-from-bottom">
                <div className="flex items-center justify-between mb-4">
                  <Heading as={3} variant={5} className="text-sacred-brown">
                    {t('auto.moreAnalysis')}
                  </Heading>
                  <button onClick={() => setShowMobileMoreSheet(false)} className="p-1 rounded-full hover:bg-sacred-gold/10">
                    <X className="w-5 h-5 text-foreground" />
                  </button>
                </div>
                {groupedMoreTabs.map(group => (
                  <div key={group.category} className="mb-4">
                    <p className="text-[10px] font-semibold uppercase tracking-wider text-sacred-gold-dark mb-2">
                      {hi ? group.label.hi : group.label.en}
                    </p>
                    <div className="grid grid-cols-2 gap-1.5">
                      {group.tabs.map(tab => (
                        <button
                          key={tab.value}
                          onClick={() => handleTabChange(tab.value)}
                          className={`text-left px-3 py-2.5 rounded-lg text-sm transition-colors ${
                            activeTab === tab.value
                              ? 'bg-sacred-gold-dark text-white font-medium'
                              : 'text-foreground bg-muted hover:bg-sacred-gold/10'
                          }`}
                        >
                          {hi ? tab.labelHi : tab.labelEn}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {tabError && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 flex items-center justify-between">
              <p className="text-sm text-red-700">{tabError}</p>
              <button onClick={() => setTabError(null)} className="text-red-500 hover:text-red-700 text-sm font-medium ml-3">{t('auto.dismiss')}</button>
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
            <DashaSelector
              kundliId={result?.id || ''}
              vimshottariData={dashaData}
              yoginiData={yoginiData}
              language={language}
              t={t}
            />
          </TabsContent>

          <TabsContent value="dasha-phala" className="min-h-[300px]">
            <DashaPhalaTab
              kundliId={result?.id || ''}
              language={language}
              t={t}
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

          <TabsContent value="ashtakvarga-phala" className="min-h-[300px]">
            <AshtakvargaPhalaTab
              kundliId={result?.id || ''}
              language={language}
              t={t}
            />
          </TabsContent>

          <TabsContent value="shadbala" className="min-h-[300px]">
            <ShadbalaTab shadbalaData={shadbalaData} loadingShadbala={loadingShadbala} language={language} t={t} />
          </TabsContent>

          <TabsContent value="avakhada" className="min-h-[300px]">
            <AvakhadaTab avakhadaData={avakhadaData} loadingAvakhada={loadingAvakhada} language={language} t={t} />
          </TabsContent>

          <TabsContent value="yoga-dosha" className="min-h-[300px]">
            <YogaDoshaTab yogaDoshaData={yogaDoshaData} loadingYogaDosha={loadingYogaDosha} doshaDisplay={doshaDisplay} doshaData={doshaData} loadingDosha={loadingDosha} language={language} t={t} kundliId={result?.id || ''} />
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

          <TabsContent value="pravrajya" className="min-h-[300px]">
            <PravrajyaTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="apatya" className="min-h-[300px]">
            <ApatyaTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="stri-jataka" className="min-h-[300px]">
            <StriJatakaTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="lifespan" className="min-h-[300px]">
            <LifespanTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="conjunctions" className="min-h-[300px]">
            <ConjunctionsTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="roga" className="min-h-[300px]">
            <RogaTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="bhava-phala" className="min-h-[300px]">
            <BhavaPhalaTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="vritti" className="min-h-[300px]">
            <VrittiTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="bhava-vichara" className="min-h-[300px]">
            <BhavaVicharaTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="longevity" className="min-h-[300px]">
            <LongevityTab kundliId={result?.id || ''} language={language} t={t} />
          </TabsContent>

          <TabsContent value="janma-predictions" className="min-h-[300px]">
            <JanmaPredictionsTab kundliId={result?.id || ''} language={language} t={t} />
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

          {/* DashaSelector is now inside the "dasha" tab above — removed duplicate */}

          <TabsContent value="d108" className="min-h-[300px]">
            <D108Analysis
              kundliId={result?.id || ''}
              language={language}
              t={t}
            />
          </TabsContent>

          <TabsContent value="animation" className="min-h-[300px]">
            <ChartAnimation
              kundliId={result?.id || ''}
              natalPlanets={(planets || []).map((p: any) => ({
                planet: p.planet,
                sign: p.sign,
                longitude: typeof p.longitude === 'number' ? p.longitude : (p.sign_degree || 0),
              }))}
              lagnaLongitude={result?.chart_data?.lagna_degree || 0}
              language={language}
              t={t}
            />
          </TabsContent>

          <TabsContent value="rectification" className="min-h-[300px]">
            <BirthRectification
              birthDate={result?.birth_date || formData.date}
              birthPlace={{
                lat: formData.latitude,
                lon: formData.longitude,
                name: result?.birth_place || formData.place,
              }}
              language={language}
              t={t}
            />
          </TabsContent>

          <TabsContent value="kp-horary" className="min-h-[300px]">
            <KPHorary language={language} t={t} />
          </TabsContent>

          <TabsContent value="sarvatobhadra" className="min-h-[300px]">
            {loadingSbc ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-6 h-6 animate-spin text-primary" />
                <span className="ml-2 text-foreground">{language === 'hi' ? 'सर्वतोभद्र चक्र लोड हो रहा है...' : 'Loading Sarvatobhadra Chakra...'}</span>
              </div>
            ) : sbcGrid ? (
              <div className="max-w-2xl mx-auto">
                <SarvatobhadraChakra
                  grid={sbcGrid}
                  vedhas={sbcVedhas}
                  showVedhaLines={true}
                  className="w-full"
                />
              </div>
            ) : (
              <p className="text-center text-foreground py-8">
                {language === 'hi' ? 'सर्वतोभद्र चक्र डेटा उपलब्ध नहीं है' : 'No Sarvatobhadra Chakra data available'}
              </p>
            )}
          </TabsContent>
        </Tabs>

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
          result={result}
          dashaData={dashaData}
          yogaDoshaData={yogaDoshaData}
          doshaData={doshaData}
          avakhadaData={avakhadaData}
          onViewFullReport={() => {
            setSummaryOpen(false);
          }}
        />

        {/* JHora-style Fullscreen Overlay */}
        {jhoraOpen && (
          <div className="fixed inset-0 z-[9999] bg-parchment w-screen h-screen">
            <button onClick={() => setJhoraOpen(false)} className="absolute top-2 right-3 z-10 p-1.5 hover:bg-black rounded text-sacred-gold text-sm font-bold" title={t('common.close')}>
              <X className="w-5 h-5" />
            </button>
            <JHoraKundliView
              result={result}
              planets={planets}
              dashaData={dashaData}
              extendedDashaData={extendedDashaData}
              avakhadaData={avakhadaData}
              yogaDoshaData={yogaDoshaData}
              ashtakvargaData={ashtakvargaData}
              shadbalaData={shadbalaData}
              divisionalData={divisionalData}
              d10Data={d10Data}
              transitData={transitData}
              loadingDasha={loadingDasha}
              loadingExtendedDasha={loadingExtendedDasha}
              loadingAvakhada={loadingAvakhada}
              loadingYogaDosha={loadingYogaDosha}
              loadingAshtakvarga={loadingAshtakvarga}
              loadingShadbala={loadingShadbala}
              loadingDivisional={loadingDivisional}
              loadingD10={loadingD10}
              loadingTransit={loadingTransit}
              onBack={() => setJhoraOpen(false)}
              onDownloadPDF={async () => {}}
            />
          </div>
        )}

        {/* Consolidated Report Popup */}
        <ConsolidatedReport
          open={reportOpen}
          onOpenChange={setReportOpen}
          result={result}
          planets={planets}
          dashaData={dashaData}
          avakhadaData={avakhadaData}
          yogaDoshaData={yogaDoshaData}
          ashtakvargaData={ashtakvargaData}
          shadbalaData={shadbalaData}
          divisionalData={divisionalData}
          loadingDasha={loadingDasha}
          loadingAvakhada={loadingAvakhada}
          loadingYogaDosha={loadingYogaDosha}
          loadingAshtakvarga={loadingAshtakvarga}
          loadingShadbala={loadingShadbala}
          loadingDivisional={loadingDivisional}
        />

        {result?.client_id && <NotesWidget clientId={result.client_id} chartType="vedic" kundliId={result.id} />}
      </div>
    );
  }

  // --- FORM VIEW ---
  // mode=horary: show KP Horary standalone (no birth data needed)
  if (urlMode === 'horary') {
    return (
      <div className="max-w-3xl mx-auto pt-32 pb-10 px-4">
        <div className="mb-6 flex items-center gap-3">
          <button onClick={() => navigate('/kundli')} className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1">
            ← {language === 'hi' ? 'कुंडली पर वापस जाएं' : 'Back to Kundli'}
          </button>
        </div>
        <KPHorary language={language} t={t} />
      </div>
    );
  }

  return (
    <>
      <KundliForm
        formData={formData}
        setFormData={setFormData}
        error={error}
        savedKundlisCount={savedKundlis.length}
        onGenerate={handleGenerate}
        onPrashnaKundli={handlePrashnaKundli}
        onBackToList={() => setStep('list')}
        timeOptional={urlMode === 'moon'}
      />

      {/* -- What's inside: tab preview --------------------------------- */}
      <section className="max-w-3xl mx-auto px-4 pb-20 pt-2">
        <div className="text-center mb-6">
          <h2 className="text-xl sm:text-2xl  text-foreground">
            {t('auto.analysisModulesHeading')}
          </h2>
        </div>

        <div className="flex flex-wrap gap-2 justify-center">
          {TAB_DEFS.map(tab => (
            <span
              key={tab.value}
              className="px-3 py-1.5 rounded-full text-xs font-medium border border-sacred-gold/40 text-sacred-gold-dark bg-sacred-gold/5 hover:bg-sacred-gold/15 transition-colors"
            >
              {hi ? tab.labelHi : tab.labelEn}
            </span>
          ))}
        </div>
      </section>
    </>
  );
}
