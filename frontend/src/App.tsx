import { useEffect, useRef, lazy, Suspense, Component } from 'react';
import type { ReactNode, ErrorInfo } from 'react';
import { Routes, Route, Link, Navigate } from 'react-router-dom';
import { I18nProvider } from './lib/i18n';
import { AuthProvider } from './hooks/useAuth';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Eager imports — used on every page or the landing page
import Navigation from './sections/Navigation';
import Hero from './sections/Hero';
import Features from './sections/Features';
import Footer from './sections/Footer';
import WhatsAppWidget from './components/WhatsAppWidget';
import { useAuth } from './hooks/useAuth';

// Lazy imports — code-split per route
const Panchang = lazy(() => import('./sections/Panchang'));
const KundliGenerator = lazy(() => import('./sections/KundliGenerator'));
const AuthPage = lazy(() => import('./sections/AuthPage'));
const NumerologyTarot = lazy(() => import('./sections/NumerologyTarot'));
const LalKitabPage = lazy(() => import('./sections/LalKitabPage'));
const AdminDashboard = lazy(() => import('./sections/AdminDashboard'));
const Dashboard = lazy(() => import('./sections/Dashboard'));
const ClientProfile = lazy(() => import('./sections/ClientProfile'));

gsap.registerPlugin(ScrollTrigger);

class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(): { hasError: boolean } {
    return { hasError: true };
  }
  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, info);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
          <h2 className="text-2xl font-cinzel text-sacred-gold-dark mb-4">Something went wrong</h2>
          <p className="text-cosmic-text/60 mb-6">An unexpected error occurred.</p>
          <button onClick={() => { this.setState({ hasError: false }); window.location.href = '/'; }}
            className="px-6 py-2 border border-sacred-gold text-sacred-gold-dark hover:bg-sacred-gold-dark hover:text-cosmic-bg transition-all">
            Return Home
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <h2 className="text-6xl font-cinzel text-sacred-gold-dark mb-4">404</h2>
      <p className="text-xl text-cosmic-text/70 mb-6">Page not found</p>
      <Link to="/" className="px-6 py-2 border border-sacred-gold text-sacred-gold-dark hover:bg-sacred-gold-dark hover:text-cosmic-bg transition-all">
        Return Home
      </Link>
    </div>
  );
}

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
    </div>
  );
}

function SmartHome() {
  const { isAuthenticated } = useAuth();
  if (isAuthenticated) return <Navigate to="/dashboard" replace />;
  return <HomePage />;
}

function RequireAuth({ children }: { children: ReactNode }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-600" /></div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function App() {
  return (
    <AuthProvider>
    <I18nProvider>
    <div className="min-h-screen bg-cosmic-bg text-cosmic-text overflow-x-hidden">
      <div className="relative">
      <Navigation />

      <main>
        <ErrorBoundary>
        <Suspense fallback={<div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-600"></div></div>}>
        <Routes>
          <Route path="/" element={<SmartHome />} />
          <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
          <Route path="/client/:clientId" element={<RequireAuth><ClientProfile /></RequireAuth>} />
          <Route path="/kundli" element={<RequireAuth><KundliGenerator /></RequireAuth>} />
          <Route path="/panchang" element={<RequireAuth><Panchang /></RequireAuth>} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/numerology" element={<RequireAuth><NumerologyTarot /></RequireAuth>} />
          <Route path="/lal-kitab" element={<RequireAuth><LalKitabPage /></RequireAuth>} />
          <Route path="/admin" element={<RequireAuth><AdminDashboard /></RequireAuth>} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        </Suspense>
        </ErrorBoundary>
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
