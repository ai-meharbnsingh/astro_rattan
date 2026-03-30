import { useEffect, useRef, lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { I18nProvider } from './lib/i18n';
import { AuthProvider } from './hooks/useAuth';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

const CosmicBackground = lazy(() => import('./components/CosmicBackground'));
import Navigation from './sections/Navigation';
import ExactHero from './sections/ExactHero';
import ExactStats from './sections/ExactStats';
import ExactDaily from './sections/ExactDaily';
import ExactQuickLinks from './sections/ExactQuickLinks';
import ExactAIAssistant from './sections/ExactAIAssistant';
import ExactRecommended from './sections/ExactRecommended';
import Footer from './sections/Footer';
import DailyHoroscope from './sections/DailyHoroscope';
import Panchang from './sections/Panchang';
import SpiritualLibrary from './sections/SpiritualLibrary';
import Shop from './sections/Shop';
import AIChat from './sections/AIChat';
import KundliGenerator from './sections/KundliGenerator';
const Kundli3D = lazy(() => import('./sections/Kundli3D'));
import AuthPage from './sections/AuthPage';
import CartCheckout from './sections/CartCheckout';
import ConsultationPage from './sections/ConsultationPage';
import AdminDashboard from './sections/AdminDashboard';
import AstrologerDashboard from './sections/AstrologerDashboard';
import AstrologerPanel from './sections/AstrologerPanel';
import PrashnavaliPage from './sections/PrashnavaliPage';
import NumerologyTarot from './sections/NumerologyTarot';
import UserProfile from './sections/UserProfile';
import Dashboard from './sections/Dashboard';
import ReportMarketplace from './sections/ReportMarketplace';
import PalmistryPage from './sections/PalmistryPage';
import BlogPage from './sections/BlogPage';
import ReferralPage from './sections/ReferralPage';
import KPLalkitabPage from './sections/KPLalkitabPage';
import MessagesPage from './sections/MessagesPage';
import PlanetaryTransitsPage from './sections/PlanetaryTransitsPage';
import CommunityPage from './sections/CommunityPage';
import GamificationPage from './sections/GamificationPage';
import CosmicCalendarPage from './sections/CosmicCalendarPage';
import PreferencesPage from './sections/PreferencesPage';
import WhatsAppWidget from './components/WhatsAppWidget';

gsap.registerPlugin(ScrollTrigger);

function HomePage() {
  const mainRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>('.animate-section').forEach((section) => {
        gsap.fromTo(section,
          { opacity: 0, y: 50 },
          {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: section,
              start: 'top 80%',
              toggleActions: 'play none none reverse'
            }
          }
        );
      });
    }, mainRef);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={mainRef} className="space-y-0"
         style={{
           background: 'linear-gradient(135deg, #F5E6C8 0%, #EDE0C8 30%, #F0DFC0 60%, #E8D5B0 100%)',
           backgroundAttachment: 'fixed',
           position: 'relative',
         }}>
      {/* Subtle parchment noise overlay */}
      <div style={{
        position: 'fixed',
        inset: 0,
        pointerEvents: 'none',
        zIndex: 0,
        opacity: 0.04,
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        backgroundRepeat: 'repeat',
      }} />
      <div style={{ position: 'relative', zIndex: 1 }}>
        <ExactHero />
        <ExactStats />
        <ExactDaily />
        <ExactQuickLinks />
        <ExactAIAssistant />
        <ExactRecommended />
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
    <I18nProvider>
    <div className="min-h-screen bg-[#F5F0E8] text-[#1a1a2e] overflow-x-hidden">
      <Suspense fallback={null}>
          <CosmicBackground />
        </Suspense>
      <div className="relative">
      <Navigation />

      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/kundli" element={<KundliGenerator />} />
          <Route path="/kundli-3d" element={<Kundli3D />} />
          <Route path="/horoscope" element={<DailyHoroscope />} />
          <Route path="/panchang" element={<Panchang />} />
          <Route path="/ai-chat" element={<AIChat />} />
          <Route path="/library" element={<SpiritualLibrary />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/cart" element={<CartCheckout />} />
          <Route path="/consultation" element={<ConsultationPage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/astrologer-dashboard" element={<AstrologerDashboard />} />
          <Route path="/astrologer-panel" element={<AstrologerPanel />} />
          <Route path="/prashnavali" element={<PrashnavaliPage />} />
          <Route path="/numerology" element={<NumerologyTarot />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/reports" element={<ReportMarketplace />} />
          <Route path="/palmistry" element={<PalmistryPage />} />
          <Route path="/blog" element={<BlogPage />} />
          <Route path="/blog/:slug" element={<BlogPage />} />
          <Route path="/referral" element={<ReferralPage />} />
          <Route path="/kp-lalkitab" element={<KPLalkitabPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="/transits" element={<PlanetaryTransitsPage />} />
          <Route path="/community" element={<CommunityPage />} />
          <Route path="/journey" element={<GamificationPage />} />
          <Route path="/cosmic-calendar" element={<CosmicCalendarPage />} />
          <Route path="/preferences" element={<PreferencesPage />} />
        </Routes>
      </main>

      <Footer />
      </div>
      <WhatsAppWidget />
    </div>
    </I18nProvider>
    </AuthProvider>
  );
}

export default App;
