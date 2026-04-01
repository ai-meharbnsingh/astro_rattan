import { useEffect, useRef, lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { I18nProvider } from './lib/i18n';
import { AuthProvider } from './hooks/useAuth';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Eager imports — used on every page or the landing page
import Navigation from './sections/Navigation';
import Hero from './sections/Hero';
import Features from './sections/Features';
import About from './sections/About';
import Testimonials from './sections/Testimonials';
import CTA from './sections/CTA';
import Footer from './sections/Footer';
import WhatsAppWidget from './components/WhatsAppWidget';

// Lazy imports — code-split per route
const CosmicBackground = lazy(() => import('./components/CosmicBackground'));
const DailyHoroscope = lazy(() => import('./sections/DailyHoroscope'));
const Panchang = lazy(() => import('./sections/Panchang'));
const SpiritualLibrary = lazy(() => import('./sections/SpiritualLibrary'));
const Shop = lazy(() => import('./sections/Shop'));
const AIChat = lazy(() => import('./sections/AIChat'));
const KundliGenerator = lazy(() => import('./sections/KundliGenerator'));
const Kundli3D = lazy(() => import('./sections/Kundli3D'));
const AuthPage = lazy(() => import('./sections/AuthPage'));
const CartCheckout = lazy(() => import('./sections/CartCheckout'));
const ConsultationPage = lazy(() => import('./sections/ConsultationPage'));
const AdminDashboard = lazy(() => import('./sections/AdminDashboard'));
const AstrologerDashboard = lazy(() => import('./sections/AstrologerDashboard'));
const AstrologerPanel = lazy(() => import('./sections/AstrologerPanel'));
const PrashnavaliPage = lazy(() => import('./sections/PrashnavaliPage'));
const NumerologyTarot = lazy(() => import('./sections/NumerologyTarot'));
const UserProfile = lazy(() => import('./sections/UserProfile'));
const Dashboard = lazy(() => import('./sections/Dashboard'));
const ReportMarketplace = lazy(() => import('./sections/ReportMarketplace'));
const PalmistryPage = lazy(() => import('./sections/PalmistryPage'));
const BlogPage = lazy(() => import('./sections/BlogPage'));
const ReferralPage = lazy(() => import('./sections/ReferralPage'));
const KPLalkitabPage = lazy(() => import('./sections/KPLalkitabPage'));
const MessagesPage = lazy(() => import('./sections/MessagesPage'));
const PlanetaryTransitsPage = lazy(() => import('./sections/PlanetaryTransitsPage'));
const CommunityPage = lazy(() => import('./sections/CommunityPage'));
const GamificationPage = lazy(() => import('./sections/GamificationPage'));
const CosmicCalendarPage = lazy(() => import('./sections/CosmicCalendarPage'));
const PreferencesPage = lazy(() => import('./sections/PreferencesPage'));

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
    <div ref={mainRef}>
      <Hero />
      <Features />
      <About />
      <Testimonials />
      <CTA />
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
        <Suspense fallback={<div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-600"></div></div>}>
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
        </Suspense>
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
