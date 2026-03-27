import { useEffect, useRef } from 'react';
import { Routes, Route } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
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
import ReportMarketplace from './sections/ReportMarketplace';
import PalmistryPage from './sections/PalmistryPage';
import BlogPage from './sections/BlogPage';

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
    <div className="min-h-screen bg-cosmic-bg text-cosmic-text overflow-x-hidden">
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
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/reports" element={<ReportMarketplace />} />
          <Route path="/palmistry" element={<PalmistryPage />} />
          <Route path="/blog" element={<BlogPage />} />
          <Route path="/blog/:slug" element={<BlogPage />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default App;
