import { Link } from 'react-router-dom';
import { Stars, Mail, Phone, Facebook, Twitter, Instagram, Youtube, ChevronRight, Heart } from 'lucide-react';

const footerLinks = {
  services: [
    { label: 'Kundli Generation', href: '/kundli' },
    { label: 'Daily Horoscope', href: '/horoscope' },
    { label: 'Panchang', href: '/panchang' },
    { label: 'AI Astrologer', href: '/ai-chat' },
    { label: 'Spiritual Library', href: '/library' },
    { label: 'Dosha Analysis', href: '/kundli' },
  ],
  spiritual: [
    { label: 'Bhagavad Gita', href: '/library' },
    { label: 'Sacred Mantras', href: '/library' },
    { label: 'Aarti Collection', href: '/library' },
    { label: 'Pooja Vidhi', href: '/library' },
    { label: 'Vrat Katha', href: '/library' },
    { label: 'Chalisa', href: '/library' },
  ],
  shop: [
    { label: 'Gemstones', href: '/shop' },
    { label: 'Rudraksha', href: '/shop' },
    { label: 'Bracelets', href: '/shop' },
    { label: 'Yantras', href: '/shop' },
    { label: 'Vastu Products', href: '/shop' },
    { label: 'Idols', href: '/shop' },
  ],
  company: [
    { label: 'About Us', href: '/' },
    { label: 'Our Astrologers', href: '/' },
    { label: 'Careers', href: '/' },
    { label: 'Blog', href: '/blog' },
    { label: 'Contact', href: '/' },
    { label: 'FAQ', href: '/' },
  ],
};

export default function Footer() {
  return (
    <footer className="relative bg-cosmic-bg-light overflow-hidden border-t border-sacred-gold/10">
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-sacred-gold/50 to-transparent" />
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-16 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
          <div className="col-span-2 md:col-span-3 lg:col-span-2">
            <Link to="/" className="flex items-center gap-2 mb-6">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center shadow-glow-gold">
                <Stars className="w-7 h-7 text-cosmic-bg" />
              </div>
              <span className="font-sacred font-bold text-2xl text-cosmic-text">AstroVedic</span>
            </Link>
            <p className="text-cosmic-text-secondary mb-6 max-w-sm">Bridging ancient Vedic wisdom with modern AI technology to guide you through life&apos;s journey.</p>
            <div className="space-y-3 mb-6">
              <a href="mailto:support@astrovedic.com" className="flex items-center gap-3 text-cosmic-text-secondary hover:text-sacred-gold transition-colors">
                <Mail className="w-5 h-5" /><span className="text-sm">support@astrovedic.com</span>
              </a>
              <a href="tel:+919876543210" className="flex items-center gap-3 text-cosmic-text-secondary hover:text-sacred-gold transition-colors">
                <Phone className="w-5 h-5" /><span className="text-sm">+91 98765 43210</span>
              </a>
            </div>
            <div className="flex gap-3">
              {[Facebook, Twitter, Instagram, Youtube].map((Icon, i) => (
                <a key={i} href="#" className="w-10 h-10 rounded-full bg-sacred-gold/10 border border-sacred-gold/20 flex items-center justify-center text-cosmic-text-secondary hover:text-sacred-gold hover:border-sacred-gold/40 transition-all">
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
          {Object.entries(footerLinks).map(([title, links]) => (
            <div key={title}>
              <h4 className="font-sacred font-semibold text-sacred-gold mb-4 capitalize">{title}</h4>
              <ul className="space-y-2">
                {links.map((link, i) => (
                  <li key={i}>
                    <Link to={link.href} className="text-sm text-cosmic-text-secondary hover:text-sacred-gold transition-colors flex items-center gap-1">
                      <ChevronRight className="w-3 h-3" />{link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="py-6 border-t border-sacred-gold/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-cosmic-text-muted">&copy; {new Date().getFullYear()} AstroVedic. Made with <Heart className="w-4 h-4 inline text-sacred-saffron fill-sacred-saffron" /> in India</p>
          <div className="flex gap-6">
            {['Privacy Policy', 'Terms of Service', 'Refund Policy'].map((item, i) => (
              <a key={i} href="#" className="text-sm text-cosmic-text-muted hover:text-sacred-gold transition-colors">{item}</a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
