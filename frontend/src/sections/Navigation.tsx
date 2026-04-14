import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Sparkles, LogOut, Shield, User, ChevronDown } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import LanguageSwitcher from '@/components/LanguageSwitcher';

// Vastu is WIP — only visible on staging (non-production hosts)
const isProduction = typeof window !== 'undefined' && window.location.hostname === 'astrorattan.com';

const serviceLinks: { key: string; href: string; highlight?: boolean }[] = [
  { key: 'nav.kundli', href: '/kundli' },
  { key: 'nav.horoscope', href: '/horoscope' },
  { key: 'nav.panchang', href: '/panchang' },
  { key: 'nav.lalKitab', href: '/lal-kitab' },
  { key: 'nav.numerology', href: '/numerology' },
  ...(!isProduction ? [{ key: 'nav.vastu', href: '/vastu', highlight: true }] : []),
];

export default function Navigation() {
  const { user, isAuthenticated, logout } = useAuth();
  const { t } = useTranslation();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setIsProfileMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 border-b border-sacred-gold/45 shadow-[0_8px_18px_-14px_rgba(196,97,31,0.55)] transition-all duration-500 ${
        isScrolled
          ? 'bg-cosmic-bg/96 backdrop-blur-lg py-2'
          : 'bg-cosmic-bg/92 py-3'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/about" className="flex items-center gap-2 shrink-0">
              <img src="/logo.png" alt="Astro Rattan" className="h-14 sm:h-16 w-auto" />
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center gap-6">
              {serviceLinks.map((link) => (
                <Link
                  key={link.key}
                  to={link.href}
                  className={
                    link.highlight
                      ? 'text-base font-semibold text-sacred-gold-dark border border-sacred-gold px-3 py-1 rounded-lg hover:bg-sacred-gold hover:text-white transition-all font-sans tracking-wide'
                      : 'text-base text-cosmic-text hover:text-sacred-gold-dark transition-colors font-sans tracking-wide'
                  }
                >
                  {t(link.key)}
                </Link>
              ))}
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-1">
              <div className="hidden sm:block">
                <LanguageSwitcher />
              </div>

              {isAuthenticated ? (
                <div ref={profileMenuRef} className="relative hidden sm:block">
                  <button
                    onClick={() => setIsProfileMenuOpen((prev) => !prev)}
                    className="ml-2 inline-flex items-center gap-1.5 px-3 py-2 border border-sacred-gold rounded-lg text-cosmic-text hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors"
                    title={t('nav.profile')}
                  >
                    <User className="w-4 h-4" />
                    <span className="text-sm font-medium">{t('nav.profile')}</span>
                    <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isProfileMenuOpen ? 'rotate-180' : ''}`} />
                  </button>
                  {isProfileMenuOpen && (
                    <div className="absolute right-0 mt-2 w-44 bg-cosmic-bg border border-sacred-gold rounded-lg shadow-lg py-1 z-50">
                      <Link
                        to="/dashboard"
                        onClick={() => setIsProfileMenuOpen(false)}
                        className="flex items-center gap-2 px-3 py-2 text-sm text-cosmic-text hover:bg-gray-50 hover:text-sacred-gold-dark transition-colors"
                      >
                        <User className="w-4 h-4" />
                        {t('nav.profile')}
                      </Link>
                      {user?.role === 'admin' && (
                        <Link
                          to="/admin"
                          onClick={() => setIsProfileMenuOpen(false)}
                          className="flex items-center gap-2 px-3 py-2 text-sm text-cosmic-text hover:bg-gray-50 hover:text-sacred-gold-dark transition-colors"
                        >
                          <Shield className="w-4 h-4" />
                          {t('nav.admin')}
                        </Link>
                      )}
                      <button
                        onClick={() => {
                          logout();
                          setIsProfileMenuOpen(false);
                        }}
                        className="w-full flex items-center gap-2 px-3 py-2 text-sm text-cosmic-text hover:bg-gray-50 hover:text-sacred-gold-dark transition-colors"
                      >
                        <LogOut className="w-4 h-4" />
                        {t('auth.signOut')}
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <Link to="/login" className="ml-2 px-4 py-2 bg-transparent border border-sacred-gold text-sacred-gold-dark text-base font-medium hover:bg-gray-50 hover:text-cosmic-bg transition-all hidden sm:flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4" />
                  {t('auth.signIn')}
                </Link>
              )}

              {isAuthenticated && user?.role === 'admin' && (
                <Link to="/admin" className="p-2.5 text-cosmic-text hover:text-sacred-gold-dark transition-colors sm:hidden" title={t('nav.admin')}>
                  <Shield className="w-5 h-5" />
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
            {serviceLinks.map((link) => (
              <Link
                key={link.key}
                to={link.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={
                  link.highlight
                    ? 'block py-3 px-3 font-semibold text-sacred-gold-dark border border-sacred-gold rounded-lg hover:bg-sacred-gold hover:text-white transition-all font-sans'
                    : 'block py-3 px-3 text-cosmic-text hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors font-sans'
                }
              >
                {t(link.key)}
              </Link>
            ))}
            <div className="pt-4 mt-4 border-t border-sacred-gold space-y-3">
              <LanguageSwitcher />
              {isAuthenticated ? (
                <div className="space-y-2">
                  <Link
                    to="/dashboard"
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium justify-center hover:bg-gray-50 transition-colors"
                  >
                    <User className="w-4 h-4" />
                    {t('nav.profile')}
                  </Link>
                  <button
                    onClick={() => { logout(); setIsMobileMenuOpen(false); }}
                    className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium text-center justify-center hover:bg-gray-50 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    {t('auth.signOut')}
                  </button>
                </div>
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
