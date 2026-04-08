import { Link } from 'react-router-dom';
import { Stars, Mail, Phone, Instagram, Youtube, ChevronRight, Heart } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

const footerLinks = {
  services: [
    { label: 'Kundli Generation', href: '/kundli' },
    { label: 'Dosha Analysis', href: '/kundli' },
    { label: 'Panchang', href: '/panchang' },
    { label: 'Lal Kitab', href: '/lal-kitab' },
    { label: 'Numerology', href: '/numerology' },
  ],
  company: [
    { label: 'About Us', href: '/' },
    { label: 'Contact', href: '/' },
  ],
};

export default function Footer() {
  const { t } = useTranslation();

  const sectionTitleKeys: Record<string, string> = {
    services: 'footer.services',
    company: 'footer.company',
  };

  return (
    <footer className="relative bg-cosmic-bg overflow-hidden border-t border-sacred-gold/20">
      {/* Top gold line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-sacred-gold-dark/50 to-transparent" />
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-16 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
          <div className="col-span-2 md:col-span-3 lg:col-span-2">
            <Link to="/" className="flex items-center gap-2 mb-6">
              <div className="w-12 h-12 bg-sacred-gold-dark flex items-center justify-center">
                <Stars className="w-7 h-7 text-cosmic-bg" />
              </div>
              <span className="font-cinzel font-bold text-2xl text-cosmic-text">Astro Rattan</span>
            </Link>
            <p className="text-cosmic-text/60 mb-6 max-w-sm">
              {t('footer.tagline')}
            </p>
            <div className="space-y-3 mb-6">
              <a href="mailto:support@astrovedic.com" className="flex items-center gap-3 text-cosmic-text/60 hover:text-sacred-gold-dark transition-colors">
                <Mail className="w-5 h-5" />
                <span className="text-sm">support@astrovedic.com</span>
              </a>
              <a href="tel:+919911760060" className="flex items-center gap-3 text-cosmic-text/60 hover:text-sacred-gold-dark transition-colors">
                <Phone className="w-5 h-5" />
                <span className="text-sm">+91 99117 60060</span>
              </a>
            </div>
            <div className="flex gap-3">
              {[
                { Icon: Instagram, url: 'https://instagram.com/astrorattan' },
                { Icon: Youtube, url: 'https://youtube.com/@astrorattan' },
              ].map(({ Icon, url }) => (
                <a
                  key={url}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 bg-sacred-gold-dark/10 border border-sacred-gold/20 flex items-center justify-center text-cosmic-text/60 hover:text-sacred-gold-dark hover:border-sacred-gold/40 transition-all"
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
          
          {Object.entries(footerLinks).map(([title, links]) => (
            <div key={title}>
              <h4 className="font-cinzel font-semibold text-sacred-gold-dark mb-4 capitalize">{t(sectionTitleKeys[title] || title)}</h4>
              <ul className="space-y-2">
                {links.map((link, i) => (
                  <li key={i}>
                    <Link 
                      to={link.href} 
                      className="text-sm text-cosmic-text/60 hover:text-sacred-gold-dark transition-colors flex items-center gap-1"
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
        
        <div className="py-6 border-t border-sacred-gold/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-cosmic-text/40">
            &copy; {new Date().getFullYear()} Astro Rattan. {t('footer.madeWith')} <Heart className="w-4 h-4 inline text-sacred-gold" /> in India
          </p>
          <div className="flex gap-6">
            <span className="text-sm text-cosmic-text/40">All rights reserved</span>
          </div>
        </div>
        <div className="pb-4 text-center">
          <p className="text-xs text-cosmic-text-secondary/60" style={{ fontFamily: "'IM Fell English', serif" }}>
            {t('footer.poweredBy')}{' '}
            <a
              href="https://adaptive-mind.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sacred-gold-dark hover:text-sacred-maroon transition-colors underline underline-offset-2"
            >
              Semantic Gravity
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
