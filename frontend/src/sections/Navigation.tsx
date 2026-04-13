import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Sparkles, LogOut, Shield, MessageSquare } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import LanguageSwitcher from '@/components/LanguageSwitcher';

const serviceLinks = [
  { key: 'nav.kundli', href: '/kundli' },
  { key: 'nav.panchang', href: '/panchang' },
  { key: 'nav.lalKitab', href: '/lal-kitab' },
  { key: 'nav.numerology', href: '/numerology' },
  { key: 'nav.vastu', href: '/vastu' },
];

const authOnlyLinks = [
  { key: 'nav.home', href: '/dashboard' },
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
          ? 'bg-cosmic-bg backdrop-blur-lg border-b border-sacred-gold py-2'
          : 'bg-transparent py-4'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 shrink-0">
              <img src="/logo.png" alt="Astro Rattan" className="h-12 w-auto" />
            </Link>

            {/* Desktop Navigation - Service links always visible, Dashboard only when authenticated */}
            <div className="hidden lg:flex items-center gap-6">
              {isAuthenticated && authOnlyLinks.map((link) => (
                <Link
                  key={link.key}
                  to={link.href}
                  className="text-base text-cosmic-text hover:text-sacred-gold-dark transition-colors font-sans tracking-wide"
                >
                  {t(link.key)}
                </Link>
              ))}
              {serviceLinks.map((link) => (
                <Link
                  key={link.key}
                  to={link.href}
                  className="text-base text-cosmic-text hover:text-sacred-gold-dark transition-colors font-sans tracking-wide"
                >
                  {t(link.key)}
                </Link>
              ))}
              {isAuthenticated && (
                <Link
                  to="/feedback"
                  className="flex items-center gap-1.5 text-base text-cosmic-text hover:text-sacred-gold-dark transition-colors font-sans tracking-wide"
                >
                  <MessageSquare className="w-4 h-4" />
                  {t('nav.feedback')}
                </Link>
              )}
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-1">
              <div className="hidden sm:block">
                <LanguageSwitcher />
              </div>

              {isAuthenticated ? (
                <>
                  {user?.role === 'admin' && (
                    <Link to="/admin" className="p-2.5 text-cosmic-text hover:text-sacred-gold-dark transition-colors hidden sm:block" title={t('nav.admin')}>
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
                <Link to="/login" className="ml-2 px-4 py-2 bg-transparent border border-sacred-gold text-sacred-gold-dark text-base font-medium hover:bg-gray-50 hover:text-cosmic-bg transition-all hidden sm:flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4" />
                  {t('auth.signIn')}
                </Link>
              )}

              {/* Mobile toggle */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 text-cosmic-text ml-1"
                aria-expanded={isMobileMenuOpen}
                aria-controls="mobile-menu"
                aria-label={isMobileMenuOpen ? t('common.closeMenu') : t('common.openMenu')}
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div id="mobile-menu" className={`fixed inset-0 z-40 lg:hidden transition-all duration-500 ${isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible pointer-events-none'}`}>
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setIsMobileMenuOpen(false)} />
        <div className={`absolute top-20 left-4 right-4 bg-cosmic-bg backdrop-blur-lg border border-sacred-gold rounded-lg p-6 transition-all duration-500 ${isMobileMenuOpen ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
          <div className="space-y-1">
            {isAuthenticated && authOnlyLinks.map((link) => (
              <Link
                key={link.key}
                to={link.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className="block py-3 px-3 text-cosmic-text hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors font-sans"
              >
                {t(link.key)}
              </Link>
            ))}
            {serviceLinks.map((link) => (
              <Link
                key={link.key}
                to={link.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className="block py-3 px-3 text-cosmic-text hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors font-sans"
              >
                {t(link.key)}
              </Link>
            ))}
            {isAuthenticated && (
              <Link
                to="/feedback"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-2 py-3 px-3 text-cosmic-text hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors font-sans"
              >
                <MessageSquare className="w-4 h-4" />
                {t('nav.feedback')}
              </Link>
            )}
            <div className="pt-4 mt-4 border-t border-sacred-gold space-y-3">
              <LanguageSwitcher />
              {isAuthenticated ? (
                <button
                  onClick={() => { logout(); setIsMobileMenuOpen(false); }}
                  className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium text-center justify-center hover:bg-gray-50 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  {t('auth.signOut')}
                </button>
              ) : (
                <Link
                  to="/login"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium text-center justify-center hover:bg-gray-50 transition-colors"
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
