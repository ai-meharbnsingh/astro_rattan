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
const Panchang = lazy(() => import('./sections/Panchang'));
const KundliGenerator = lazy(() => import('./sections/KundliGenerator'));
const AuthPage = lazy(() => import('./sections/AuthPage'));
const NumerologyTarot = lazy(() => import('./sections/NumerologyTarot'));
const LalKitabPage = lazy(() => import('./sections/LalKitabPage'));

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
    <div className="min-h-screen bg-cosmic-bg text-cosmic-text overflow-x-hidden">
      <div className="relative">
      <Navigation />

      <main>
        <Suspense fallback={<div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-600"></div></div>}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/kundli" element={<KundliGenerator />} />
          <Route path="/panchang" element={<Panchang />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/numerology" element={<NumerologyTarot />} />
          <Route path="/lal-kitab" element={<LalKitabPage />} />
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
