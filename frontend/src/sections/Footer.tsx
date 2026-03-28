import { Link } from 'react-router-dom';
import { Stars, Mail, Phone, Facebook, Twitter, Instagram, Youtube, ChevronRight, Heart } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

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
  const { t } = useTranslation();

  const sectionTitleKeys: Record<string, string> = {
    services: 'footer.services',
    spiritual: 'footer.spiritual',
    shop: 'footer.shop',
    company: 'footer.company',
  };

  return (
    <footer className="relative bg-[#F5F0E8] overflow-hidden border-t border-[#9A7B0A]/20">
      {/* Top gold line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#9A7B0A]/50 to-transparent" />
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-16 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
          <div className="col-span-2 md:col-span-3 lg:col-span-2">
            <Link to="/" className="flex items-center gap-2 mb-6">
              <div className="w-12 h-12 bg-[#9A7B0A] flex items-center justify-center">
                <Stars className="w-7 h-7 text-[#1a1a2e]" />
              </div>
              <span className="font-['Cinzel'] font-bold text-2xl text-[#1a1a2e]">Astro Rattan</span>
            </Link>
            <p className="text-[#1a1a2e]/60 mb-6 max-w-sm">
              {t('footer.tagline')}
            </p>
            <div className="space-y-3 mb-6">
              <a href="mailto:support@astrovedic.com" className="flex items-center gap-3 text-[#1a1a2e]/60 hover:text-[#B8860B] transition-colors">
                <Mail className="w-5 h-5" />
                <span className="text-sm">support@astrovedic.com</span>
              </a>
              <a href="tel:+919911760060" className="flex items-center gap-3 text-[#1a1a2e]/60 hover:text-[#B8860B] transition-colors">
                <Phone className="w-5 h-5" />
                <span className="text-sm">+91 99117 60060</span>
              </a>
            </div>
            <div className="flex gap-3">
              {[Facebook, Twitter, Instagram, Youtube].map((Icon, i) => (
                <a 
                  key={i} 
                  href="#" 
                  className="w-10 h-10 bg-[#9A7B0A]/10 border border-[#9A7B0A]/20 flex items-center justify-center text-[#1a1a2e]/60 hover:text-[#B8860B] hover:border-[#9A7B0A]/40 transition-all"
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
          
          {Object.entries(footerLinks).map(([title, links]) => (
            <div key={title}>
              <h4 className="font-['Cinzel'] font-semibold text-[#9A7B0A] mb-4 capitalize">{t(sectionTitleKeys[title] || title)}</h4>
              <ul className="space-y-2">
                {links.map((link, i) => (
                  <li key={i}>
                    <Link 
                      to={link.href} 
                      className="text-sm text-[#1a1a2e]/60 hover:text-[#B8860B] transition-colors flex items-center gap-1"
                    >
                      <ChevronRight className="w-3 h-3" />
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        
        <div className="py-6 border-t border-[#9A7B0A]/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-[#1a1a2e]/40">
            &copy; {new Date().getFullYear()} Astro Rattan. {t('footer.madeWith')} <Heart className="w-4 h-4 inline text-[#ffaa33]" /> in India
          </p>
          <div className="flex gap-6">
            {['Privacy Policy', 'Terms of Service', 'Refund Policy'].map((item, i) => (
              <a
                key={i}
                href="#"
                className="text-sm text-[#1a1a2e]/40 hover:text-[#B8860B] transition-colors"
              >
                {item}
              </a>
            ))}
          </div>
        </div>
        <div className="pb-4 text-center">
          <p className="text-xs text-[#8B7355]/60" style={{ fontFamily: "'IM Fell English', serif" }}>
            {t('footer.poweredBy')}{' '}
            <a
              href="https://adaptive-mind.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#B8860B] hover:text-[#8B2332] transition-colors underline underline-offset-2"
            >
              Semantic Gravity
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
