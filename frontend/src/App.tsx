import { useEffect, useRef, lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { I18nProvider } from './lib/i18n';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

const CosmicBackground = lazy(() => import('./components/three/CosmicBackground'));
import WhatsAppWidget from './components/WhatsAppWidget';
import Navigation from './sections/Navigation';
import Hero from './sections/Hero';
import Features from './sections/Features';
import About from './sections/About';
import Testimonials from './sections/Testimonials';
import CTA from './sections/CTA';
import Footer from './sections/Footer';
import DailyHoroscope from './sections/DailyHoroscope';
import Panchang from './sections/Panchang';
import SpiritualLibrary from './sections/SpiritualLibrary';
import Shop from './sections/Shop';
import AIChat from './sections/AIChat';
import KundliGenerator from './sections/KundliGenerator';
import AuthPage from './sections/AuthPage';
import CartCheckout from './sections/CartCheckout';
import ConsultationPage from './sections/ConsultationPage';
import AdminDashboard from './sections/AdminDashboard';
import AstrologerDashboard from './sections/AstrologerDashboard';
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
    <I18nProvider>
    <div className="min-h-screen bg-cosmic-bg text-cosmic-text overflow-x-hidden">
      <Suspense fallback={null}>
        <CosmicBackground />
      </Suspense>

      <div className="relative z-10">
      <Navigation />

      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/kundli" element={<KundliGenerator />} />
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
  );
}

export default App;
