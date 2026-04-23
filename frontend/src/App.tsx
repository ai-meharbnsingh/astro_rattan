import { useEffect, useRef, lazy, Suspense, Component } from 'react';
import type { ReactNode, ErrorInfo } from 'react';
import { Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';

function usePageTracking() {
  const location = useLocation();
  useEffect(() => {
    // `ScrollBehavior` supports only 'auto' | 'smooth' (mobile Safari can throw on unknown values).
    window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
    let sid = sessionStorage.getItem('_asid');
    if (!sid) { sid = Math.random().toString(36).slice(2) + Date.now().toString(36); sessionStorage.setItem('_asid', sid); }
    fetch('/api/analytics/hit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: location.pathname, session_id: sid, referrer: document.referrer || null }),
      keepalive: true,
    }).catch(() => {});
  }, [location.pathname]);
}
import { I18nProvider, useTranslation } from './lib/i18n';
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

// Lazy imports — code-split per route.
// The catch + reload handles stale SPA sessions: if a user had the old JS loaded
// before a deploy, dynamic imports for renamed chunks get 404s. Reloading fetches
// the fresh index.html which references the new chunk hashes.
function lazyWithReload<T extends React.ComponentType<any>>(
  importFn: () => Promise<{ default: T }>
) {
  return lazy(() =>
    importFn().catch(() => {
      // Avoid infinite reload loops: only reload once per session per key
      const key = `_chunk_reload_${importFn.toString().slice(0, 60)}`;
      if (!sessionStorage.getItem(key)) {
        sessionStorage.setItem(key, '1');
        window.location.reload();
      }
      return new Promise<{ default: T }>(() => {}); // suspend until reload
    })
  );
}

const Panchang        = lazyWithReload(() => import('./sections/Panchang'));
const KundliGenerator = lazyWithReload(() => import('./sections/KundliGenerator'));
const AuthPage        = lazyWithReload(() => import('./sections/AuthPage'));
const NumerologyTarot = lazyWithReload(() => import('./sections/NumerologyTarot'));
const LalKitabPage    = lazyWithReload(() => import('./sections/LalKitabPage'));
const AdminDashboard  = lazyWithReload(() => import('./sections/AdminDashboard'));
const FeedbackPage    = lazyWithReload(() => import('./sections/FeedbackPage'));
const Dashboard       = lazyWithReload(() => import('./sections/Dashboard'));
// P3.5 — Professional client management dashboard (astrologer role)
const AstrologerDashboard = lazyWithReload(() => import('./sections/AstrologerDashboard'));
const ClientProfile   = lazyWithReload(() => import('./sections/ClientProfile'));
const VastuShastraPage = lazyWithReload(() => import('./sections/VastuShastraPage'));
const HoroscopePage    = lazyWithReload(() => import('./sections/HoroscopePage'));
const BlogPage         = lazyWithReload(() => import('./sections/BlogPage'));

gsap.registerPlugin(ScrollTrigger);

// Respect prefers-reduced-motion: disable all GSAP animations globally
if (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  gsap.globalTimeline.timeScale(0);
  gsap.defaults({ duration: 0 });
}

class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean; error: Error | null }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error: Error): { hasError: boolean; error: Error } {
    return { hasError: true, error };
  }
  componentDidCatch(error: Error, info: ErrorInfo) {
    // Surface details in console (helps mobile remote debugging) and persist last crash for support.
    // eslint-disable-next-line no-console
    console.error('ErrorBoundary caught:', error, info);
    try {
      localStorage.setItem('ar_last_ui_error', JSON.stringify({
        message: error?.message || String(error),
        stack: error?.stack || null,
        componentStack: info?.componentStack || null,
        at: new Date().toISOString(),
      }));
    } catch { /* ignore */ }
  }
  render() {
    if (this.state.hasError) {
      const lang = (typeof window !== 'undefined' && localStorage.getItem('astrorattan-language') === 'hi') ? 'hi' : 'en';
      return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
          <div className="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mb-4">
            <span className="text-3xl">⚠️</span>
          </div>
          <h2 className="text-2xl font-sans text-gray-800 mb-2">{lang === 'hi' ? 'कुछ गलत हो गया' : 'Something went wrong'}</h2>
          <p className="text-gray-500 mb-2 max-w-md">{lang === 'hi' ? 'इस सेक्शन में त्रुटि आई है। आपका डेटा सुरक्षित है, कृपया रिफ्रेश करें।' : 'This section encountered an error. Your data is safe, try refreshing.'}</p>
          {this.state.error && (
            <p className="text-sm text-red-600 bg-red-50 px-3 py-1 rounded mb-4 max-w-md truncate">{this.state.error.message}</p>
          )}
          <div className="flex gap-3">
            <button onClick={() => this.setState({ hasError: false, error: null })}
              className="px-6 py-2.5 bg-sacred-gold-dark text-white rounded-lg hover:opacity-90 transition-all font-medium">
              {lang === 'hi' ? 'फिर से प्रयास करें' : 'Try Again'}
            </button>
            <button onClick={() => window.location.href = '/'}
              className="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all font-medium">
              {lang === 'hi' ? 'होम जाएं' : 'Go Home'}
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

function NotFound() {
  const { t } = useTranslation();
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <h2 className="text-6xl font-sans text-sacred-gold-dark mb-4">404</h2>
      <p className="text-xl text-gray-600 mb-6">{t('app.notFound')}</p>
      <Link to="/" className="px-6 py-2 border border-sacred-gold text-sacred-gold-dark hover:bg-gray-50 dark hover:text-background transition-all">
        {t('app.returnHome')}
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
  const { isAuthenticated, user } = useAuth();
  if (isAuthenticated) return <Navigate to={user?.role === 'admin' ? '/admin' : '/dashboard'} replace />;
  return <HomePage />;
}

function RequireAuth({ children }: { children: ReactNode }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-600" /></div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function AppInner() {
  usePageTracking();
  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      <div className="relative">
      <Navigation />

      <main>
        <ErrorBoundary>
        <Suspense fallback={<div className="flex items-center justify-center min-h-[60vh]"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-600"></div></div>}>
        <Routes>
          <Route path="/" element={<SmartHome />} />
          <Route path="/about" element={<HomePage />} />
          <Route path="/dashboard" element={<RequireAuth><ErrorBoundary><Dashboard /></ErrorBoundary></RequireAuth>} />
          {/* P3.5 — Professional client management dashboard for astrologers */}
          <Route path="/astrologer" element={<RequireAuth><ErrorBoundary><AstrologerDashboard /></ErrorBoundary></RequireAuth>} />
          <Route path="/astrologer/dashboard" element={<RequireAuth><ErrorBoundary><AstrologerDashboard /></ErrorBoundary></RequireAuth>} />
          <Route path="/client/:clientId" element={<RequireAuth><ClientProfile /></RequireAuth>} />
          <Route path="/kundli" element={<ErrorBoundary><KundliGenerator /></ErrorBoundary>} />
          <Route path="/panchang" element={<ErrorBoundary><Panchang /></ErrorBoundary>} />
          <Route path="/horoscope" element={<ErrorBoundary><HoroscopePage /></ErrorBoundary>} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/numerology" element={<RequireAuth><ErrorBoundary><NumerologyTarot /></ErrorBoundary></RequireAuth>} />
          <Route path="/lal-kitab" element={<RequireAuth><ErrorBoundary><LalKitabPage /></ErrorBoundary></RequireAuth>} />
          <Route path="/vastu" element={<RequireAuth><ErrorBoundary><VastuShastraPage /></ErrorBoundary></RequireAuth>} />
          <Route path="/admin" element={<RequireAuth><ErrorBoundary><AdminDashboard /></ErrorBoundary></RequireAuth>} />
          <Route path="/feedback" element={<RequireAuth><ErrorBoundary><FeedbackPage /></ErrorBoundary></RequireAuth>} />
          <Route path="/blog" element={<ErrorBoundary><BlogPage /></ErrorBoundary>} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        </Suspense>
        </ErrorBoundary>
      </main>

      <Footer />
      </div>
      <WhatsAppWidget />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
    <I18nProvider>
      <AppInner />
    </I18nProvider>
    </AuthProvider>
  );
}

export default App;
