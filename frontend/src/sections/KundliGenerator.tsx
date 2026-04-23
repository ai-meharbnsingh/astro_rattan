import { useState, useRef, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useTranslation } from '@/lib/i18n';
import { formatDate, api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Heading } from '@/components/ui/heading';
import { Download, Share2, Loader2, ScrollText, Home, RefreshCw, ChevronDown, X, BookOpen, Star, Clock3, Sparkles, Grid3X3, Eye } from 'lucide-react';
import { useKundliData } from '@/hooks/useKundliData';
import SEOHead from '@/components/SEOHead';
import { generateBreadcrumbSchema } from '@/lib/seoConfig';
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
import RemediesTab from '@/components/kundli/RemediesTab';
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
import SarvatobhadraChakra, { SarvatobhadraTheorySection } from '@/components/sarvatobhadra/SarvatobhadraChakra';
import PravrajyaTab from '@/components/kundli/PravrajyaTab';
import ApatyaTab from '@/components/kundli/ApatyaTab';
import StriJatakaTab from '@/components/kundli/StriJatakaTab';
import ConjunctionsTab from '@/components/kundli/ConjunctionsTab';
import RogaTab from '@/components/kundli/RogaTab';
import BhavaPhalaTab from '@/components/kundli/BhavaPhalaTab';
import VrittiTab from '@/components/kundli/VrittiTab';
import BhavaVicharaTab from '@/components/kundli/BhavaVicharaTab';
import LongevityTab from '@/components/kundli/LongevityTab';
import JanmaPredictionsTab from '@/components/kundli/JanmaPredictionsTab';
import KalachakraTab from '@/components/kundli/KalachakraTab';
import NavamshaCareerTab from '@/components/kundli/NavamshaCareerTab';
import GrahaSambandhaTab from '@/components/kundli/GrahaSambandhaTab';
import PanchadhaMaitriTab from '@/components/kundli/PanchadhaMaitriTab';
import FamilyDemiseTab from '@/components/kundli/FamilyDemiseTab';
import GochaVedhaTab from '@/components/kundli/GochaVedhaTab';
import NadiAnalysisTab from '@/components/kundli/NadiAnalysisTab';
import TransitLuckyTab from '@/components/kundli/TransitLuckyTab';
import TransitInterpretationsTab from '@/components/kundli/TransitInterpretationsTab';
import AstroMapTab from '@/components/kundli/AstroMapTab';
import KundliInterpretationsTab from '@/components/kundli/KundliInterpretationsTab';
import AdvancedTheorySection from '@/components/kundli/AdvancedTheorySection';

import AnalysisTheorySection from '@/components/kundli/AnalysisTheorySection';
import ChartsTheorySection from '@/components/kundli/ChartsTheorySection';

// ── Single source of truth for ALL tab definitions ──────────
interface TabDef {
  value: string;
  labelEn: string;
  labelHi: string;
  descriptionEn?: string;
  descriptionHi?: string;
  i18nKey?: string; // if we use t() for label
  primary: boolean;
  category?: 'charts' | 'timing' | 'analysis' | 'advanced';
  icon?: React.ComponentType<{ className?: string }>;
  onActivate?: () => void; // set dynamically below
}

const TAB_DEFS: Omit<TabDef, 'onActivate'>[] = [
  // Primary tabs
  { value: 'report',        labelEn: 'Report',         labelHi: 'रिपोर्ट',          primary: true, icon: ScrollText },
  { value: 'remedies',      labelEn: 'Remedies',       labelHi: 'उपाय',             primary: true, icon: BookOpen },
  { value: 'planets',       labelEn: 'Planets',        labelHi: 'ग्रह',             primary: true, icon: Star },
  { value: 'dasha',         labelEn: 'Dasha',          labelHi: 'दशा',             primary: true, icon: Clock3 },
  { value: 'yoga-dosha',    labelEn: 'Yogas/Dosha',    labelHi: 'योग/दोष',          primary: true, icon: Sparkles },
  { value: 'divisional',    labelEn: 'Divisional',     labelHi: 'विभाजन चार्ट',     primary: true, icon: Grid3X3 },
  { value: 'aspects',       labelEn: 'Aspects',        labelHi: 'दृष्टि',           primary: true, icon: Eye },
  // Charts
  { value: 'ashtakvarga',   labelEn: 'Ashtakvarga',    labelHi: 'अष्टकवर्ग',        primary: false, category: 'charts',   descriptionEn: 'Planetary strength scores across 8 sensitive points per sign', descriptionHi: 'प्रत्येक राशि में 8 संवेदनशील बिंदुओं पर ग्रह बल स्कोर' },
  { value: 'ashtakvarga-phala', labelEn: 'Ashtakvarga Effects', labelHi: 'अष्टकवर्ग फल', primary: false, category: 'analysis', descriptionEn: 'Interpretive results derived from Ashtakvarga scores', descriptionHi: 'अष्टकवर्ग स्कोर से निकाले गए व्याख्यात्मक परिणाम' },
  { value: 'sodashvarga',   labelEn: 'Sodashvarga',    labelHi: 'षोडशवर्ग',         primary: false, category: 'charts',   descriptionEn: '16 divisional charts for life-area specific analysis', descriptionHi: 'जीवन-क्षेत्र विशिष्ट विश्लेषण के लिए 16 विभाजन चार्ट' },
  { value: 'd108',          labelEn: 'D108 Chart',     labelHi: 'D108 अष्टोत्तरांश',  primary: false, category: 'charts',  descriptionEn: 'Rare D108 chart for deep spiritual & karmic insights', descriptionHi: 'गहन आध्यात्मिक और कर्मिक अंतर्दृष्टि के लिए दुर्लभ D108 चार्ट' },
  { value: 'animation',     labelEn: 'Chart Animation', labelHi: 'चार्ट एनिमेशन',   primary: false, category: 'charts',   descriptionEn: 'Animated planetary motion showing transit movement over time', descriptionHi: 'समय के साथ गोचर गति दिखाने वाली एनिमेटेड ग्रहीय गति' },
  { value: 'sarvatobhadra', labelEn: 'Sarvatobhadra',   labelHi: 'सर्वतोभद्र चक्र',  primary: false, category: 'charts',   descriptionEn: 'Auspicious chakra grid used for muhurta and transit analysis', descriptionHi: 'मुहूर्त और गोचर विश्लेषण के लिए उपयोग किया जाने वाला शुभ चक्र ग्रिड' },
  // Timing
  { value: 'yogini',        labelEn: 'Yogini Dasha',   labelHi: 'योगिनी दशा',       primary: false, category: 'timing',   descriptionEn: '8-goddess 36-year Yogini dasha timing cycle', descriptionHi: '8 देवियों वाली 36 वर्षीय योगिनी दशा समय चक्र' },
  { value: 'dasha-phala',   labelEn: 'Dasha Effects',  labelHi: 'दशा फल',           primary: false, category: 'timing',   descriptionEn: 'Interpretive predictions for currently active dasha periods', descriptionHi: 'वर्तमान में सक्रिय दशा अवधियों के लिए व्याख्यात्मक भविष्यवाणियाँ' },
  // dasha-systems merged into "dasha" tab via DashaSelector (5 systems in one)
  { value: 'varshphal',     labelEn: 'Varshphal',      labelHi: 'वर्षफल',           primary: false, category: 'timing',   descriptionEn: 'Annual solar return chart analysis for the current year', descriptionHi: 'वर्तमान वर्ष के लिए वार्षिक सौर वापसी चार्ट विश्लेषण' },
  { value: 'transits',      labelEn: 'Transits',       labelHi: 'गोचर',             primary: false, category: 'timing',   descriptionEn: 'Current planetary positions overlaid on natal chart', descriptionHi: 'जन्म कुंडली पर चिह्नित वर्तमान ग्रहीय स्थितियाँ' },
  { value: 'sadesati',      labelEn: 'Sade Sati',      labelHi: 'साढ़े साती',        primary: false, category: 'timing',   descriptionEn: 'Saturn\'s 7.5-year cycle over natal Moon — phase & intensity', descriptionHi: 'जन्म चंद्रमा पर शनि का 7.5 वर्षीय चक्र — चरण और तीव्रता' },
  { value: 'kalachakra',    labelEn: 'Kalachakra Dasha', labelHi: 'कालचक्र दशा',    primary: false, category: 'timing',   descriptionEn: 'Kalachakra dasha timing system based on nakshatra groups', descriptionHi: 'नक्षत्र समूहों पर आधारित कालचक्र दशा समय प्रणाली' },
  { value: 'gochara-vedha', labelEn: 'Gochara Vedha',  labelHi: 'गोचर वेध',         primary: false, category: 'timing',   descriptionEn: 'Obstruction points that neutralise a beneficial transit', descriptionHi: 'बिंदु जो शुभ गोचर को निष्प्रभावी कर देते हैं' },
  { value: 'transit-interp', labelEn: 'Transit Interpretations', labelHi: 'गोचर व्याख्या', primary: false, category: 'timing', descriptionEn: 'Written interpretations for each active transit planet', descriptionHi: 'प्रत्येक सक्रिय गोचर ग्रह के लिए लिखित व्याख्याएँ' },
  { value: 'transit-lucky', labelEn: 'Lucky Indicators', labelHi: 'शुभ संकेतक',      primary: false, category: 'timing',   descriptionEn: 'Auspicious timing windows derived from transit patterns', descriptionHi: 'गोचर पैटर्न से प्राप्त शुभ समय खिड़कियाँ' },
  // Analysis
  { value: 'shadbala',      labelEn: 'Shadbala',       labelHi: 'षड्बल',            primary: false, category: 'analysis', descriptionEn: 'Six-fold strength measurement — numerical power of each planet', descriptionHi: 'षड्बल — प्रत्येक ग्रह की छह-गुणी शक्ति मापन' },
  { value: 'kp',            labelEn: 'KP System',      labelHi: 'केपी सिस्टम',      primary: false, category: 'analysis', descriptionEn: 'Krishnamurti Paddhati — sub-lord & stellar system analysis', descriptionHi: 'कृष्णमूर्ति पद्धति — उप-स्वामी और तारकीय प्रणाली विश्लेषण' },
  { value: 'kp-horary',     labelEn: 'KP Horary',      labelHi: 'केपी प्रश्न',       primary: false, category: 'analysis', descriptionEn: 'Answer specific questions using KP horary method', descriptionHi: 'केपी प्रश्न कुंडली विधि द्वारा विशिष्ट प्रश्नों के उत्तर' },
  { value: 'jaimini',       labelEn: 'Jaimini',        labelHi: 'जैमिनी',           primary: false, category: 'analysis', descriptionEn: 'Jaimini astrology — chara karaka, special dashas & rajayogas', descriptionHi: 'जैमिनी ज्योतिष — चर कारक, विशेष दशाएँ और राजयोग' },
  { value: 'pravrajya',     labelEn: 'Pravrajya Yogas', labelHi: 'प्रव्रज्या योग',   primary: false, category: 'analysis', descriptionEn: 'Yogas for renunciation, spirituality & monastic life', descriptionHi: 'वैराग्य, आध्यात्मिकता और सन्यासी जीवन के लिए योग' },
  { value: 'apatya',        labelEn: 'Progeny (Apatya)',labelHi: 'संतान',            primary: false, category: 'analysis', descriptionEn: 'Children — potential, timing & indicators from 5th house', descriptionHi: 'संतान — 5वें भाव से संभावना, समय और संकेतक' },
  { value: 'stri-jataka',   labelEn: 'Stri Jataka',    labelHi: 'स्त्री जातक',       primary: false, category: 'analysis', descriptionEn: 'Traditional female horoscopy — marriage & feminine signifiers', descriptionHi: 'पारंपरिक स्त्री जातक — विवाह और स्त्री संकेतक' },
  { value: 'conjunctions',  labelEn: 'Conjunctions',   labelHi: 'ग्रह युतियाँ',      primary: false, category: 'analysis', descriptionEn: 'Planetary conjunctions and their combined effects in chart', descriptionHi: 'ग्रह युतियाँ और चार्ट में उनके संयुक्त प्रभाव' },
  { value: 'roga',          labelEn: 'Disease Analysis', labelHi: 'रोग विश्लेषण',    primary: false, category: 'analysis', descriptionEn: 'Health vulnerabilities and disease tendencies from chart', descriptionHi: 'स्वास्थ्य कमजोरियाँ और चार्ट से रोग प्रवृत्तियाँ' },
  { value: 'bhava-phala',   labelEn: 'Bhava Phala',    labelHi: 'भाव फल',           primary: false, category: 'analysis', descriptionEn: 'Predicted results for each of the 12 houses', descriptionHi: '12 भावों में से प्रत्येक के लिए अनुमानित परिणाम' },
  { value: 'vritti',        labelEn: 'Career (Vritti)', labelHi: 'आजीविका',          primary: false, category: 'analysis', descriptionEn: 'Career & livelihood — profession indicators and timing', descriptionHi: 'आजीविका और करियर — पेशा संकेतक और समय' },
  { value: 'janma-predictions', labelEn: 'Janma Predictions', labelHi: 'जन्म फल',    primary: false, category: 'analysis', descriptionEn: 'Birth chart predictions based on lagna, moon & planetary positions', descriptionHi: 'लग्न, चंद्रमा और ग्रह स्थितियों पर आधारित जन्म कुंडली भविष्यवाणियाँ' },
  { value: 'kundli-interpretations', labelEn: 'Interpretations', labelHi: 'कुंडली व्याख्या', primary: false, category: 'analysis', descriptionEn: 'Comprehensive AI-assisted chart interpretations for all areas', descriptionHi: 'सभी क्षेत्रों के लिए व्यापक AI-सहायक चार्ट व्याख्या' },
  { value: 'iogita',        labelEn: 'Iogita',         labelHi: 'आयोगिता',          primary: false, category: 'analysis', descriptionEn: 'Yoga strength & aptitude analysis — skills and talents', descriptionHi: 'योग बल और योग्यता विश्लेषण — कौशल और प्रतिभा' },
  { value: 'aspects-matrix',labelEn: 'Aspects Matrix',  labelHi: 'दृष्टि मैट्रिक्स', primary: false, category: 'analysis', descriptionEn: 'Full grid of all planetary aspects — both Vedic & Western', descriptionHi: 'सभी ग्रहीय दृष्टियों का पूर्ण ग्रिड — वैदिक और पाश्चात्य दोनों' },
  { value: 'navamsha-career', labelEn: 'Navamsha Career', labelHi: 'नवांश करियर',    primary: false, category: 'analysis', descriptionEn: 'Career insights derived specifically from the D9 Navamsha chart', descriptionHi: 'D9 नवांश चार्ट से प्राप्त विशिष्ट करियर अंतर्दृष्टि' },
  { value: 'graha-sambandha', labelEn: 'Graha Sambandha', labelHi: 'ग्रह सम्बन्ध',  primary: false, category: 'analysis', descriptionEn: 'Planetary relationships — mutual aspects, exchange & conjunction', descriptionHi: 'ग्रह संबंध — पारस्परिक दृष्टि, परिवर्तन और युति' },
  { value: 'panchadha-maitri', labelEn: 'Panchadha Maitri', labelHi: 'पंचधा मैत्री', primary: false, category: 'analysis', descriptionEn: 'Five-fold friendship table between planet pairs', descriptionHi: 'ग्रह युग्मों के बीच पंचधा मैत्री सारणी' },
  { value: 'nadi-analysis', labelEn: 'Nadi Analysis',  labelHi: 'नाड़ी विश्लेषण',    primary: false, category: 'analysis', descriptionEn: 'Nadi nakshatra-based predictive techniques and readings', descriptionHi: 'नाड़ी नक्षत्र-आधारित भविष्यवाणी तकनीक और पठन' },
  // Advanced
  { value: 'bhava-vichara', labelEn: 'Bhava Analysis', labelHi: 'भाव विचार',        primary: false, category: 'advanced', descriptionEn: 'Deep house-by-house analysis with lord strength & occupants', descriptionHi: 'स्वामी बल और अधिवासियों के साथ गहन भाव-दर-भाव विश्लेषण' },
  { value: 'longevity',     labelEn: 'Longevity Indicators', labelHi: 'आयु संकेतक', primary: false, category: 'advanced', descriptionEn: 'Ayurdaya lifespan calculation using multiple classical methods', descriptionHi: 'कई शास्त्रीय विधियों का उपयोग करके आयुर्दाय आयु गणना' },
  { value: 'mundane',       labelEn: 'Mundane',        labelHi: 'मुंडन ज्योतिष',    primary: false, category: 'advanced', descriptionEn: 'World events & mundane astrology predictions', descriptionHi: 'विश्व घटनाएँ और मुंडन ज्योतिष भविष्यवाणियाँ' },
  { value: 'rectification', labelEn: 'Birth Rectification', labelHi: 'जन्म समय शोधन', primary: false, category: 'advanced', descriptionEn: 'Correct uncertain birth time using life events & techniques', descriptionHi: 'जीवन घटनाओं और तकनीकों का उपयोग करके अनिश्चित जन्म समय को सही करें' },
  { value: 'upagrahas',     labelEn: 'Upagrahas',      labelHi: 'उपग्रह',           primary: false, category: 'advanced', descriptionEn: 'Sub-planets like Gulika, Mandi & Dhuma and their influences', descriptionHi: 'उपग्रह जैसे गुलिका, मंडी और धूमा और उनके प्रभाव' },
  { value: 'lordships',     labelEn: 'Lordships',      labelHi: 'लॉर्डशिप',         primary: false, category: 'advanced', descriptionEn: 'House lordship table — which planet rules which house', descriptionHi: 'भाव स्वामित्व सारणी — कौन सा ग्रह किस भाव का स्वामी है' },
  { value: 'details',       labelEn: 'Birth Details',  labelHi: 'विवरण',             primary: false, category: 'advanced', descriptionEn: 'Full birth chart data including panchanga and basic details', descriptionHi: 'पंचांग और बुनियादी विवरण सहित पूर्ण जन्म कुंडली डेटा' },
  { value: 'avakhada',      labelEn: 'Avakhada',       labelHi: 'अवखड़ा',           primary: false, category: 'advanced', descriptionEn: 'Avakhada chakra — nakshatra, tithi, karana & panchanga data', descriptionHi: 'अवखड़ा चक्र — नक्षत्र, तिथि, करण और पंचांग डेटा' },
  { value: 'milan',         labelEn: 'Kundli Milan',   labelHi: 'कुंडली मिलान',     primary: false, category: 'advanced', descriptionEn: 'Kundli compatibility matching — 36 gun milan & doshas', descriptionHi: 'कुंडली अनुकूलता मिलान — 36 गुण मिलान और दोष' },
  { value: 'family-demise', labelEn: 'Family Longevity', labelHi: 'परिवार आयु विचार', primary: false, category: 'advanced', descriptionEn: 'Family longevity — parental & sibling longevity indicators', descriptionHi: 'पारिवारिक आयु — माता-पिता और भाई-बहन आयु संकेतक' },
  { value: 'astro-map',    labelEn: 'Astro Map',       labelHi: 'ज्योतिष मानचित्र', primary: false, category: 'advanced', descriptionEn: 'Astrocartography map — best locations for living and travel', descriptionHi: 'ज्योतिष मानचित्र — रहने और यात्रा के लिए सर्वोत्तम स्थान' },
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
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const [hoveredTabValue, setHoveredTabValue] = useState<string | null>(null);

  // Sarvatobhadra Chakra state
  const [sbcGrid, setSbcGrid] = useState<any[][] | null>(null);
  const [sbcVedhas, setSbcVedhas] = useState<any[]>([]);
  const [loadingSbc, setLoadingSbc] = useState(false);

  // Auto-activate rectification tab when result arrives in rectification mode
  useEffect(() => {
    if (urlMode === 'rectification' && step === 'result') {
      setActiveTab('rectification');
    }
  }, [step, urlMode]);

  // Auto-activate tab from ?tab= query param when on result step
  useEffect(() => {
    const tabFromUrl = searchParams.get('tab');
    if (tabFromUrl && step === 'result' && TAB_DEFS.some(t => t.value === tabFromUrl)) {
      handleTabChange(tabFromUrl);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [step, searchParams]);

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
    setExpandedCategory(null);
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

  const breadcrumbs = generateBreadcrumbSchema([
    { name: 'Home', item: '/' },
    { name: 'Kundli', item: '/kundli' }
  ]);

  // --- LOADING ---
  if (step === 'loading') {
    return (
      <>
        <SEOHead pageKey="kundli" jsonLd={[breadcrumbs]} />
        <div className="flex items-center justify-center min-h-[60vh]">
          <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
        </div>
      </>
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
      <div className="max-w-screen-2xl mx-auto pt-24 pb-48 px-4">
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
      <div className="max-w-screen-2xl mx-auto pt-24 pb-48 px-4 bg-transparent">
        <SEOHead pageKey="kundli" jsonLd={[breadcrumbs]} />
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
                setReportOpen(true);
              }}>
              <ScrollText className="w-4 h-4 mr-1" />{t('kundli.fullReport')}
            </Button>
            <Button size="sm"
              className="bg-gradient-to-r from-sacred-gold to-sacred-gold-dark text-white hover:from-sacred-gold/90 hover:to-sacred-gold-dark/90 font-semibold border border-sacred-gold-dark/30 shadow-md"
              onClick={async () => {
                if (!result?.id) return;
                const token = localStorage.getItem('astrorattan_token');
                const API_BASE = import.meta.env.VITE_API_URL || '';
                try {
                  const resp = await fetch(`${API_BASE}/api/kundli/${result.id}/full-report?lang=${language}`, {
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
                  a.download = `Kundli_Report_${result.person_name || 'chart'}.pdf`;
                  document.body.appendChild(a);
                  a.click();
                  document.body.removeChild(a);
                  URL.revokeObjectURL(url);
                } catch (e: any) {
                  alert(e.message || t('report.failedToDownloadPDF'));
                }
              }}>
              <BookOpen className="w-4 h-4 mr-1" />{t('auto.downloadFullReportPD')}
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
          </div>
        </div>

        {/* Tabs — controlled mode */}
        <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full kundli-tabs">
          <div className="mb-4">
            <TabsList
              className="bg-sacred-gold/5 border border-sacred-gold/20 w-full h-auto p-2 gap-1 grid grid-flow-col auto-cols-[minmax(92px,1fr)] overflow-x-auto
              [&>button]:w-full [&>button]:min-h-[58px] [&>button]:px-1 [&>button]:py-2 [&>button]:text-[11px] md:[&>button]:text-xs
              [&>button]:flex [&>button]:flex-col [&>button]:items-center [&>button]:justify-center [&>button]:gap-1 [&>button]:leading-tight
              [&>button]:text-sacred-gold-dark/70 [&>button:hover]:bg-sacred-gold/10 [&>button:hover]:text-sacred-gold-dark
              [&>button[data-state=active]]:bg-sacred-gold-dark [&>button[data-state=active]]:text-white [&>button[data-state=active]]:shadow-md"
            >
              {primaryTabs.map(tab => (
                <TabsTrigger key={tab.value} value={tab.value}>
                  {tab.icon && <tab.icon className="w-3.5 h-3.5" />}
                  <span className="truncate max-w-full">{hi ? tab.labelHi : tab.labelEn}</span>
                </TabsTrigger>
              ))}
            </TabsList>
            {/* 4 category tabs + hover-reveal item strip — single hover zone */}
            <div className="mt-1" onMouseLeave={() => { setExpandedCategory(null); setHoveredTabValue(null); }}>
              {/* Category header row */}
              <div className="grid grid-cols-4 bg-sacred-gold/5 border border-sacred-gold/20 rounded-lg p-1.5 gap-1">
                {groupedMoreTabs.map(group => {
                  const isCatActive = group.tabs.some(t => t.value === activeTab);
                  const isExpanded = expandedCategory === group.category;
                  return (
                    <button
                      key={group.category}
                      onMouseEnter={() => setExpandedCategory(group.category)}
                      onClick={() => setExpandedCategory(isExpanded ? null : group.category)}
                      className={`min-h-[42px] px-1 py-2 rounded-md text-[11px] md:text-xs font-semibold flex items-center justify-center gap-1 transition-all ${
                        isCatActive
                          ? 'bg-sacred-gold-dark text-white shadow-md'
                          : isExpanded
                          ? 'bg-sacred-gold/15 text-sacred-gold-dark border border-sacred-gold/40'
                          : 'text-sacred-gold-dark/70 hover:bg-sacred-gold/10 hover:text-sacred-gold-dark'
                      }`}
                    >
                      {hi ? group.label.hi : group.label.en}
                    </button>
                  );
                })}
              </div>

              {/* Item strip — shown on hover, hidden on mouse-leave of whole zone */}
              {expandedCategory && (
                <div className="mt-0.5 p-2 bg-white border border-sacred-gold/20 rounded-lg flex flex-wrap gap-1.5 shadow-sm">
                  {groupedMoreTabs.find(g => g.category === expandedCategory)?.tabs.map(tab => (
                    <div key={tab.value} className="relative">
                      <button
                        onClick={() => handleTabChange(tab.value)}
                        onMouseEnter={() => setHoveredTabValue(tab.value)}
                        onMouseLeave={() => setHoveredTabValue(null)}
                        className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                          activeTab === tab.value
                            ? 'bg-sacred-gold-dark text-white shadow-sm'
                            : 'bg-sacred-gold/5 border border-sacred-gold/25 text-foreground hover:bg-sacred-gold/15 hover:border-sacred-gold/50'
                        }`}
                      >
                        {hi ? tab.labelHi : tab.labelEn}
                      </button>
                      {hoveredTabValue === tab.value && tab.descriptionEn && (
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50 bg-sacred-brown text-white rounded-lg shadow-xl px-3 py-2 w-48 pointer-events-none text-center">
                          <p className="text-[10px] leading-relaxed opacity-90">{hi ? tab.descriptionHi : tab.descriptionEn}</p>
                          <div className="absolute top-full left-1/2 -translate-x-1/2 border-[5px] border-transparent border-t-sacred-brown" />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

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

          <TabsContent value="remedies" className="min-h-[300px]">
            <RemediesTab kundliId={result?.id || ''} language={language} t={t} />
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
            <AdvancedTheorySection language={language} tab="details" />
          </TabsContent>

          <TabsContent value="lordships" className="min-h-[300px]">
            <LordshipsTab planets={planets} houses={result.chart_data?.houses || {}} />
            <AdvancedTheorySection language={language} tab="lordships" />
          </TabsContent>

          <TabsContent value="iogita" className="min-h-[300px]">
            <IogitaTab iogitaData={iogitaData} loadingIogita={loadingIogita} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="iogita" />
          </TabsContent>

          <TabsContent value="dasha" className="min-h-[300px]">
            <DashaSelector
              key={result?.id || ''}
              kundliId={result?.id || ''}
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
            <AnalysisTheorySection language={language} tab="ashtakvarga-phala" />
          </TabsContent>

          <TabsContent value="shadbala" className="min-h-[300px]">
            <ShadbalaTab shadbalaData={shadbalaData} loadingShadbala={loadingShadbala} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="shadbala" />
          </TabsContent>

          <TabsContent value="avakhada" className="min-h-[300px]">
            <AvakhadaTab avakhadaData={avakhadaData} loadingAvakhada={loadingAvakhada} language={language} t={t} />
            <AdvancedTheorySection language={language} tab="avakhada" />
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
            <AnalysisTheorySection language={language} tab="kp" />
          </TabsContent>

          <TabsContent value="yogini" className="min-h-[300px]">
            <YoginiTab yoginiData={yoginiData} loadingYogini={loadingYogini} language={language} t={t} />
          </TabsContent>

          <TabsContent value="upagrahas" className="min-h-[300px]">
            <UpagrahasTab upagrahasData={upagrahasData} loadingUpagrahas={loadingUpagrahas} language={language} t={t} />
            <AdvancedTheorySection language={language} tab="upagrahas" />
          </TabsContent>

          <TabsContent value="sodashvarga" className="min-h-[300px]">
            <SodashvargaTab sodashvargaData={sodashvargaData} loadingSodashvarga={loadingSodashvarga} language={language} t={t} />
          </TabsContent>

          <TabsContent value="aspects" className="min-h-[300px]">
            <AspectsTab aspectsData={aspectsData} loadingAspects={loadingAspects} language={language} t={t} />
          </TabsContent>

          <TabsContent value="aspects-matrix" className="min-h-[300px]">
            <AspectsMatrixTab data={westernAspectsData} loading={loadingWesternAspects} />
            <AnalysisTheorySection language={language} tab="aspects-matrix" />
          </TabsContent>

          <TabsContent value="jaimini" className="min-h-[300px]">
            <JaiminiTab data={jaiminiData} loading={loadingJaimini} />
            <AnalysisTheorySection language={language} tab="jaimini" />
          </TabsContent>

          <TabsContent value="pravrajya" className="min-h-[300px]">
            <PravrajyaTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="pravrajya" />
          </TabsContent>

          <TabsContent value="apatya" className="min-h-[300px]">
            <ApatyaTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="apatya" />
          </TabsContent>

          <TabsContent value="stri-jataka" className="min-h-[300px]">
            <StriJatakaTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="stri-jataka" />
          </TabsContent>


          <TabsContent value="conjunctions" className="min-h-[300px]">
            <ConjunctionsTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="conjunctions" />
          </TabsContent>

          <TabsContent value="roga" className="min-h-[300px]">
            <RogaTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="roga" />
          </TabsContent>

          <TabsContent value="bhava-phala" className="min-h-[300px]">
            <BhavaPhalaTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="bhava-phala" />
          </TabsContent>

          <TabsContent value="vritti" className="min-h-[300px]">
            <VrittiTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="vritti" />
          </TabsContent>

          <TabsContent value="bhava-vichara" className="min-h-[300px]">
            <BhavaVicharaTab kundliId={result?.id || ''} language={language} t={t} />
            <AdvancedTheorySection language={language} tab="bhava-vichara" />
          </TabsContent>

          <TabsContent value="longevity" className="min-h-[300px]">
            <LongevityTab kundliId={result?.id || ''} language={language} t={t} />
            <AdvancedTheorySection language={language} tab="longevity" />
          </TabsContent>

          <TabsContent value="janma-predictions" className="min-h-[300px]">
            <JanmaPredictionsTab kundliId={result?.id || ''} language={language} t={t} />
            <AnalysisTheorySection language={language} tab="janma-predictions" />
          </TabsContent>

          <TabsContent value="kundli-interpretations" className="min-h-[300px]">
            <KundliInterpretationsTab kundliId={result?.id || ''} language={language} />
            <AnalysisTheorySection language={language} tab="kundli-interpretations" />
          </TabsContent>

          <TabsContent value="sadesati" className="min-h-[300px]">
            <SadesatiTab sadesatiData={sadesatiData} loadingSadesati={loadingSadesati} doshaData={doshaData} language={language} t={t} />
          </TabsContent>

          <TabsContent value="mundane" className="min-h-[300px]">
            <MundaneTab language={language} />
            <AdvancedTheorySection language={language} tab="mundane" />
          </TabsContent>

          <TabsContent value="milan" className="min-h-[300px]">
            <KundliMilanTab savedKundlis={savedKundlis} currentKundliId={result?.id} />
            <AdvancedTheorySection language={language} tab="milan" />
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
            <ChartsTheorySection language={language} tab="animation" />
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
            <AdvancedTheorySection language={language} tab="rectification" />
          </TabsContent>

          <TabsContent value="kp-horary" className="min-h-[300px]">
            <KPHorary language={language} t={t} />
            <AnalysisTheorySection language={language} tab="kp-horary" />
          </TabsContent>

          <TabsContent value="kalachakra" className="min-h-[300px]">
            <KalachakraTab kundliId={result?.id || ''} language={language} />
          </TabsContent>

          <TabsContent value="gochara-vedha" className="min-h-[300px]">
            <GochaVedhaTab kundliId={result?.id || ''} language={language} />
          </TabsContent>

          <TabsContent value="transit-interp" className="min-h-[300px]">
            <TransitInterpretationsTab kundliId={result?.id || ''} language={language} />
          </TabsContent>

          <TabsContent value="transit-lucky" className="min-h-[300px]">
            <TransitLuckyTab kundliId={result?.id || ''} language={language} />
          </TabsContent>

          <TabsContent value="navamsha-career" className="min-h-[300px]">
            <NavamshaCareerTab kundliId={result?.id || ''} language={language} />
            <AnalysisTheorySection language={language} tab="navamsha-career" />
          </TabsContent>

          <TabsContent value="graha-sambandha" className="min-h-[300px]">
            <GrahaSambandhaTab kundliId={result?.id || ''} language={language} />
            <AnalysisTheorySection language={language} tab="graha-sambandha" />
          </TabsContent>

          <TabsContent value="panchadha-maitri" className="min-h-[300px]">
            <PanchadhaMaitriTab kundliId={result?.id || ''} language={language} />
            <AnalysisTheorySection language={language} tab="panchadha-maitri" />
          </TabsContent>

          <TabsContent value="nadi-analysis" className="min-h-[300px]">
            <NadiAnalysisTab kundliId={result?.id || ''} language={language} />
            <AnalysisTheorySection language={language} tab="nadi-analysis" />
          </TabsContent>

          <TabsContent value="family-demise" className="min-h-[300px]">
            <FamilyDemiseTab kundliId={result?.id || ''} language={language} />
            <AdvancedTheorySection language={language} tab="family-demise" />
          </TabsContent>

          <TabsContent value="astro-map" className="min-h-[300px]">
            <AstroMapTab kundliId={result?.id || ''} kundliData={result} language={language} />
            <AdvancedTheorySection language={language} tab="astro-map" />
          </TabsContent>

          <TabsContent value="sarvatobhadra" className="min-h-[300px]">
            <div className="space-y-4">
              <div>
                <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
                  <Grid3X3 className="w-6 h-6" />
                  {language === 'hi' ? 'सर्वतोभद्र चक्र' : 'Sarvatobhadra Chakra'}
                </Heading>
                <p className="text-sm text-muted-foreground">
                  {language === 'hi'
                    ? 'मूहूर्त, गोचर और शुभ-अशुभ संकेतों के लिए उपयोग होने वाला पारंपरिक चक्र-ग्रिड।'
                    : 'An auspicious chakra grid used for muhurta, transits, and timing indicators.'}
                </p>
              </div>

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
              <ChartsTheorySection language={language} tab="sarvatobhadra" />
            </div>
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
      <div className="max-w-5xl mx-auto pt-32 pb-10 px-4">
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
      <SEOHead pageKey="kundli" jsonLd={[breadcrumbs]} />
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
      <section className="max-w-5xl mx-auto px-4 pb-20 pt-2">
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
