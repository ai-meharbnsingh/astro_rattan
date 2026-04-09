import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Sparkles, LogOut, Shield } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import LanguageSwitcher from '@/components/LanguageSwitcher';

const primaryLinks = [
  { key: 'HOME', href: '/dashboard' },
  { key: 'nav.kundli', href: '/kundli' },
  { key: 'nav.panchang', href: '/panchang' },
  { key: 'nav.lalKitab', href: '/lal-kitab' },
  { key: 'nav.numerology', href: '/numerology' },
];

export default function Navigation() {
  const { user, isAuthenticated, logout } = useAuth();
  const { t } = useTranslation();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        isScrolled
          ? 'bg-cosmic-bg/90 backdrop-blur-lg border-b border-sacred-gold/20 py-2'
          : 'bg-transparent py-4'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 shrink-0">
              <img src="/logo.png" alt="Astro Rattan" className="h-32 w-auto" />
            </Link>

            {/* Desktop Navigation - Only show when authenticated */}
            {isAuthenticated && (
              <div className="hidden lg:flex items-center gap-6">
                {primaryLinks.map((link) => (
                  <Link
                    key={link.key}
                    to={link.href}
                    className="text-base text-cosmic-text hover:text-sacred-gold-dark transition-colors font-cinzel tracking-wide uppercase"
                  >
                    {t(link.key)}
                  </Link>
                ))}
              </div>
            )}

            {/* Action buttons */}
            <div className="flex items-center gap-1">
              <div className="hidden sm:block -mt-8">
                <LanguageSwitcher />
              </div>

              {isAuthenticated ? (
                <>
                  {user?.role === 'admin' && (
                    <Link to="/admin" className="p-2.5 text-cosmic-text hover:text-sacred-gold-dark transition-colors hidden sm:block" title="Admin">
                      <Shield className="w-5 h-5" />
                    </Link>
                  )}
                  <button
                    onClick={logout}
                    className="p-2.5 text-cosmic-text hover:text-sacred-gold-dark transition-colors hidden sm:flex items-center gap-1"
                    title={t('auth.signOut')}
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </>
              ) : (
                <Link to="/login" className="ml-2 px-4 py-2 bg-transparent border border-sacred-gold text-sacred-gold-dark text-base font-medium hover:bg-sacred-gold-dark hover:text-cosmic-bg transition-all hidden sm:flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4" />
                  {t('auth.signIn')}
                </Link>
              )}

              {/* Mobile toggle */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 text-cosmic-text ml-1"
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div className={`fixed inset-0 z-40 lg:hidden transition-all duration-500 ${isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible pointer-events-none'}`}>
        <div className="absolute inset-0 bg-cosmic-bg/95 backdrop-blur-xl" onClick={() => setIsMobileMenuOpen(false)} />
        <div className={`absolute top-20 left-4 right-4 bg-cosmic-bg/95 backdrop-blur-lg border border-sacred-gold/20 rounded-none p-6 transition-all duration-500 ${isMobileMenuOpen ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
          <div className="space-y-1">
            {isAuthenticated && primaryLinks.map((link) => (
              <Link
                key={link.key}
                to={link.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className="block py-3 px-3 text-cosmic-text hover:text-sacred-gold-dark hover:bg-sacred-gold-dark/10 transition-colors font-sacred"
              >
                {t(link.key)}
              </Link>
            ))}
            <div className="pt-4 mt-4 border-t border-sacred-gold/20 space-y-3">
              <LanguageSwitcher />
              {isAuthenticated ? (
                <button
                  onClick={() => { logout(); setIsMobileMenuOpen(false); }}
                  className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium text-center justify-center hover:bg-sacred-gold-dark/10 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  {t('auth.signOut')}
                </button>
              ) : (
                <Link
                  to="/login"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium text-center justify-center hover:bg-sacred-gold-dark/10 transition-colors"
                >
                  <Sparkles className="w-4 h-4" />
                  {t('auth.signIn')}
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
