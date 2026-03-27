import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Stars, Menu, X, MessageCircle, ShoppingCart, User, Search, ChevronDown, Shield, Star, Sparkles } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import LanguageSwitcher from '@/components/LanguageSwitcher';

const primaryLinks = [
  { key: 'nav.kundli', href: '/kundli' },
  { key: 'nav.horoscope', href: '/horoscope' },
  { key: 'nav.panchang', href: '/panchang' },
  { key: 'nav.shop', href: '/shop' },
  { key: 'nav.consultation', href: '/consultation' },
];

const moreLinks = [
  { key: 'nav.prashnavali', href: '/prashnavali' },
  { key: 'nav.numerology', href: '/numerology' },
  { key: 'nav.palmistry', href: '/palmistry' },
  { key: 'nav.library', href: '/library' },
  { key: 'nav.blog', href: '/blog' },
  { key: 'nav.community', href: '/community' },
];

const allLinks = [...primaryLinks, ...moreLinks];

export default function Navigation() {
  const { user, isAuthenticated } = useAuth();
  const { t } = useTranslation();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isMoreOpen, setIsMoreOpen] = useState(false);
  const moreRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (moreRef.current && !moreRef.current.contains(e.target as Node)) {
        setIsMoreOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        isScrolled
          ? 'bg-[#0a0a1a]/90 backdrop-blur-lg border-b border-[#d4af37]/20 py-2'
          : 'bg-transparent py-4'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 shrink-0">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#d4af37] to-[#b8860b] flex items-center justify-center">
                <Stars className="w-5 h-5 text-[#0a0a0a]" />
              </div>
              <span className="font-decorative font-bold text-xl text-[#d4af37] hidden sm:block">Astro Rattan</span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center gap-6">
              {primaryLinks.map((link) => (
                <Link
                  key={link.key}
                  to={link.href}
                  className="text-sm text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors font-cinzel tracking-wide uppercase text-[13px]"
                >
                  {t(link.key)}
                </Link>
              ))}

              {/* More dropdown */}
              <div ref={moreRef} className="relative">
                <button
                  onClick={() => setIsMoreOpen(!isMoreOpen)}
                  className="text-sm text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors font-cinzel tracking-wide uppercase text-[13px] flex items-center gap-1"
                >
                  More
                  <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isMoreOpen ? 'rotate-180' : ''}`} />
                </button>
                {isMoreOpen && (
                  <div className="absolute top-full mt-2 right-0 w-48 bg-[#0a0a1a]/95 backdrop-blur-lg border border-[#d4af37]/20 rounded-xl py-2 shadow-xl">
                    {moreLinks.map((link) => (
                      <Link
                        key={link.key}
                        to={link.href}
                        onClick={() => setIsMoreOpen(false)}
                        className="block px-4 py-2.5 text-sm text-[#f0f0f0]/80 hover:text-[#d4af37] hover:bg-[#d4af37]/10 transition-colors font-sacred"
                      >
                        {t(link.key)}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-1">
              <button className="p-2.5 text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors hidden sm:block">
                <Search className="w-5 h-5" />
              </button>

              <div className="hidden sm:block">
                <LanguageSwitcher />
              </div>

              <Link to="/ai-chat" className="p-2.5 text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors hidden sm:block">
                <MessageCircle className="w-5 h-5" />
              </Link>

              {isAuthenticated && (
                <Link to="/cart" className="p-2.5 text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors relative">
                  <ShoppingCart className="w-5 h-5" />
                  <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-[#d4af37] rounded-full text-[10px] text-[#0a0a0a] flex items-center justify-center font-bold">0</span>
                </Link>
              )}

              {isAuthenticated && user?.role === 'admin' && (
                <Link to="/admin" className="p-2.5 text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors hidden lg:block">
                  <Shield className="w-5 h-5" />
                </Link>
              )}

              {isAuthenticated && user?.role === 'astrologer' && (
                <Link to="/astrologer-dashboard" className="p-2.5 text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors hidden lg:block">
                  <Star className="w-5 h-5" />
                </Link>
              )}

              {isAuthenticated ? (
                <Link to="/profile" className="p-2.5 text-[#f0f0f0]/80 hover:text-[#d4af37] transition-colors">
                  <User className="w-5 h-5" />
                </Link>
              ) : (
                <Link to="/login" className="ml-2 px-4 py-2 bg-gradient-to-r from-[#d4af37] to-[#b8962e] text-[#0a0a0a] text-sm font-bold rounded-full hover:shadow-lg hover:shadow-[#d4af37]/25 transition-all hidden sm:flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4" />
                  Sign In
                </Link>
              )}

              {/* Mobile toggle */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 text-[#f0f0f0] ml-1"
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div className={`fixed inset-0 z-40 lg:hidden transition-all duration-500 ${isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible pointer-events-none'}`}>
        <div className="absolute inset-0 bg-[#0a0a1a]/95 backdrop-blur-xl" onClick={() => setIsMobileMenuOpen(false)} />
        <div className={`absolute top-20 left-4 right-4 bg-[#0a0a1a]/95 backdrop-blur-lg border border-[#d4af37]/20 rounded-2xl p-6 transition-all duration-500 ${isMobileMenuOpen ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
          <div className="space-y-1">
            {allLinks.map((link) => (
              <Link
                key={link.key}
                to={link.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className="block py-3 px-3 text-[#f0f0f0]/80 hover:text-[#d4af37] hover:bg-[#d4af37]/10 rounded-xl transition-colors font-sacred"
              >
                {t(link.key)}
              </Link>
            ))}
            <div className="pt-4 mt-4 border-t border-[#d4af37]/20 space-y-3">
              <LanguageSwitcher />
              <Link
                to="/ai-chat"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-2 w-full px-4 py-3 bg-gradient-to-r from-[#d4af37] to-[#b8962e] text-[#0a0a0a] font-bold rounded-xl text-center justify-center"
              >
                <MessageCircle className="w-4 h-4" />
                {t('nav.askAIAstrologer')}
              </Link>
              {!isAuthenticated && (
                <Link
                  to="/login"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="flex items-center gap-2 w-full px-4 py-3 border border-[#d4af37]/40 text-[#d4af37] font-bold rounded-xl text-center justify-center hover:bg-[#d4af37]/10 transition-colors"
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
