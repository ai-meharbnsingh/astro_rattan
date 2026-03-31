import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { I18nProvider } from './lib/i18n';
import { AuthProvider, useAuth } from './hooks/useAuth';

const CosmicBackground = lazy(() => import('./components/CosmicBackground'));
import Navigation from './sections/Navigation';
import Footer from './sections/Footer';

/* Kimi Exact Template Sections (landing page — before login) */
import ServiceCards from './sections/ServiceCards';
import StatsBar from './sections/StatsBar';
import DailyInsights from './sections/DailyInsights';
import CategoryTabs from './sections/CategoryTabs';
import AiAstrologyAssistant from './sections/AiAstrologyAssistant';
import RecommendedSection from './sections/RecommendedSection';
import ShopSection from './sections/ShopSection';

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

/* Landing page — Kimi template for visitors (not logged in) */
function LandingPage() {
  return (
    <div className="min-h-screen parchment-bg">
      {/* Decorative Background Pattern */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <svg
          className="absolute -right-40 -top-40 w-96 h-96 opacity-5"
          viewBox="0 0 200 200"
        >
          <circle cx="100" cy="100" r="90" fill="none" stroke="#8B4513" strokeWidth="1" />
          <circle cx="100" cy="100" r="70" fill="none" stroke="#8B4513" strokeWidth="1" />
          <circle cx="100" cy="100" r="50" fill="none" stroke="#8B4513" strokeWidth="1" />
          {[...Array(12)].map((_, i) => (
            <line
              key={i}
              x1="100"
              y1="10"
              x2="100"
              y2="30"
              stroke="#8B4513"
              strokeWidth="1"
              transform={`rotate(${i * 30} 100 100)`}
            />
          ))}
        </svg>
        <svg
          className="absolute -left-20 bottom-20 w-64 h-64 opacity-5"
          viewBox="0 0 200 200"
        >
          <circle cx="100" cy="100" r="90" fill="none" stroke="#8B4513" strokeWidth="1" />
          <circle cx="100" cy="100" r="70" fill="none" stroke="#8B4513" strokeWidth="1" />
        </svg>
      </div>

      {/* Main Content */}
      <main className="relative z-10">
        <ServiceCards />
        <StatsBar />
        <DailyInsights />
        <CategoryTabs />
        <AiAstrologyAssistant />
        <RecommendedSection />
        <ShopSection />
      </main>
    </div>
  );
}

/* Home route — Kimi template if visitor, Dashboard if logged in */
function HomePage() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return null;

  return isAuthenticated ? <Dashboard /> : <LandingPage />;
}

function App() {
  return (
    <AuthProvider>
    <I18nProvider>
    <div className="min-h-screen bg-[#F5E6D3] text-[#5D4037] overflow-x-hidden">
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
