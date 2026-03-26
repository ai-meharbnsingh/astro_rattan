import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Stars, Menu, X, Sparkles, MessageCircle, ShoppingCart, User, Shield, Star } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

const navLinks = [
  { name: 'Kundli', href: '/kundli' },
  { name: 'Horoscope', href: '/horoscope' },
  { name: 'Panchang', href: '/panchang' },
  { name: 'Prashnavali', href: '/prashnavali' },
  { name: 'Numerology', href: '/numerology' },
  { name: 'Palmistry', href: '/palmistry' },
  { name: 'Library', href: '/library' },
  { name: 'Blog', href: '/blog' },
  { name: 'Shop', href: '/shop' },
];

export default function Navigation() {
  const { user, isAuthenticated } = useAuth();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 100);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${isScrolled ? 'py-3' : 'py-6'}`}>
        <div className={`mx-auto transition-all duration-500 ${isScrolled ? 'max-w-4xl px-6' : 'max-w-7xl px-4 sm:px-6 lg:px-8'}`}>
          <div className={`flex items-center justify-between transition-all duration-500 ${isScrolled ? 'nav-sacred rounded-full px-6 py-3 shadow-lg' : ''}`}>
            <Link to="/" className="flex items-center gap-2 group">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shadow-md">
                <Stars className="w-6 h-6 text-white" />
              </div>
              <span className="font-sacred font-bold text-xl text-sacred-brown">AstroVedic</span>
            </Link>
            <div className="hidden lg:flex items-center gap-1">
              {navLinks.map((link) => (
                <Link key={link.name} to={link.href} className="px-4 py-2 text-sm nav-link-sacred font-medium">
                  {link.name}
                </Link>
              ))}
            </div>
            <div className="hidden lg:flex items-center gap-3">
              {isAuthenticated && user?.role === 'admin' && (
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/admin" className="text-sacred-brown hover:text-sacred-gold-dark">
                    <Shield className="w-4 h-4 mr-2" />Admin
                  </Link>
                </Button>
              )}
              {isAuthenticated && user?.role === 'astrologer' && (
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/astrologer-dashboard" className="text-sacred-brown hover:text-sacred-gold-dark">
                    <Star className="w-4 h-4 mr-2" />Dashboard
                  </Link>
                </Button>
              )}
              <Button variant="ghost" size="sm" asChild>
                <Link to="/ai-chat" className="text-sacred-brown hover:text-sacred-gold-dark">
                  <MessageCircle className="w-4 h-4 mr-2" />Ask AI
                </Link>
              </Button>
              {isAuthenticated && (
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/cart" className="text-sacred-brown hover:text-sacred-gold-dark">
                    <ShoppingCart className="w-4 h-4" />
                  </Link>
                </Button>
              )}
              {isAuthenticated ? (
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/profile" className="text-sacred-brown hover:text-sacred-gold-dark">
                    <User className="w-4 h-4 mr-2" />Profile
                  </Link>
                </Button>
              ) : (
                <Button size="sm" asChild className="btn-sacred">
                  <Link to="/login">
                    <Sparkles className="w-4 h-4 mr-2" />Sign In
                  </Link>
                </Button>
              )}
            </div>
            <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="lg:hidden p-2 text-sacred-brown">
              {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </nav>
      <div className={`fixed inset-0 z-40 lg:hidden transition-all duration-500 ${isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible'}`}>
        <div className="absolute inset-0 bg-sacred-cream/95 backdrop-blur-xl" onClick={() => setIsMobileMenuOpen(false)} />
        <div className={`absolute top-20 left-4 right-4 card-sacred rounded-2xl p-6 transition-all duration-500 ${isMobileMenuOpen ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
          <div className="space-y-4">
            {navLinks.map((link) => (
              <Link key={link.name} to={link.href} onClick={() => setIsMobileMenuOpen(false)} className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-sacred-gold/10 text-left transition-colors">
                <span className="text-sacred-brown font-medium">{link.name}</span>
              </Link>
            ))}
            <div className="pt-4 border-t border-sacred-gold/30 space-y-3">
              <Button className="w-full btn-sacred" asChild>
                <Link to="/ai-chat" onClick={() => setIsMobileMenuOpen(false)}>
                  <MessageCircle className="w-4 h-4 mr-2" />Ask AI Astrologer
                </Link>
              </Button>
              {isAuthenticated && (
                <>
                  <Button variant="outline" className="w-full border-sacred-gold text-sacred-brown hover:bg-sacred-gold/10" asChild>
                    <Link to="/cart" onClick={() => setIsMobileMenuOpen(false)}>
                      <ShoppingCart className="w-4 h-4 mr-2" />Cart
                    </Link>
                  </Button>
                  <Button variant="outline" className="w-full border-sacred-gold text-sacred-brown hover:bg-sacred-gold/10" asChild>
                    <Link to="/profile" onClick={() => setIsMobileMenuOpen(false)}>
                      <User className="w-4 h-4 mr-2" />Profile
                    </Link>
                  </Button>
                  {user?.role === 'admin' && (
                    <Button variant="outline" className="w-full border-sacred-gold text-sacred-brown hover:bg-sacred-gold/10" asChild>
                      <Link to="/admin" onClick={() => setIsMobileMenuOpen(false)}>
                        <Shield className="w-4 h-4 mr-2" />Admin
                      </Link>
                    </Button>
                  )}
                  {user?.role === 'astrologer' && (
                    <Button variant="outline" className="w-full border-sacred-gold text-sacred-brown hover:bg-sacred-gold/10" asChild>
                      <Link to="/astrologer-dashboard" onClick={() => setIsMobileMenuOpen(false)}>
                        <Star className="w-4 h-4 mr-2" />Astrologer Dashboard
                      </Link>
                    </Button>
                  )}
                </>
              )}
              {!isAuthenticated && (
                <Button variant="outline" className="w-full border-sacred-gold text-sacred-brown hover:bg-sacred-gold/10" asChild>
                  <Link to="/login" onClick={() => setIsMobileMenuOpen(false)}>
                    <Sparkles className="w-4 h-4 mr-2" />Sign In
                  </Link>
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
