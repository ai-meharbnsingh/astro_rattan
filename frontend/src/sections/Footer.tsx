import { Link } from 'react-router-dom';
import { Mail, Phone, Instagram, Youtube, ChevronRight, Heart } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { useAuth } from '@/hooks/useAuth';

const serviceLinks = [
  { label: 'Kundli Generation', href: '/kundli' },
  { label: 'Dosha Analysis', href: '/kundli' },
  { label: 'Panchang', href: '/panchang' },
  { label: 'Lal Kitab', href: '/lal-kitab' },
  { label: 'Numerology', href: '/numerology' },
];

const footerLinks = {
  company: [
    { label: 'About Us', href: '/' },
    { label: 'Contact', href: '/' },
  ],
};

export default function Footer() {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();

  const sectionTitleKeys: Record<string, string> = {
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
              <img src="/logo.png" alt="Astro Rattan" className="h-28 w-auto" />
            </Link>
            <p className="text-cosmic-text mb-6 max-w-sm">
              {t('footer.tagline')}
            </p>
            <div className="space-y-3 mb-6">
              <a href="mailto:support@astrovedic.com" className="flex items-center gap-3 text-cosmic-text hover:text-sacred-gold-dark transition-colors">
                <Mail className="w-5 h-5" />
                <span className="text-base">support@astrovedic.com</span>
              </a>
              <a href="tel:+919911760060" className="flex items-center gap-3 text-cosmic-text hover:text-sacred-gold-dark transition-colors">
                <Phone className="w-5 h-5" />
                <span className="text-base">+91 99117 60060</span>
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
                  className="w-10 h-10 bg-sacred-gold-dark/10 border border-sacred-gold/20 flex items-center justify-center text-cosmic-text hover:text-sacred-gold-dark hover:border-sacred-gold/40 transition-all"
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
          
          {isAuthenticated && (
            <div>
              <h4 className="font-cinzel font-semibold text-sacred-gold-dark mb-4">{t('footer.services')}</h4>
              <ul className="space-y-2">
                {serviceLinks.map((link, i) => (
                  <li key={i}>
                    <Link to={link.href} className="text-base text-cosmic-text hover:text-sacred-gold-dark transition-colors flex items-center gap-1">
                      <ChevronRight className="w-4 h-4" />{link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {Object.entries(footerLinks).map(([title, links]) => (
            <div key={title}>
              <h4 className="font-cinzel font-semibold text-sacred-gold-dark mb-4 capitalize">{t(sectionTitleKeys[title] || title)}</h4>
              <ul className="space-y-2">
                {links.map((link, i) => (
                  <li key={i}>
                    <Link 
                      to={link.href} 
                      className="text-base text-cosmic-text hover:text-sacred-gold-dark transition-colors flex items-center gap-1"
                    >
                      <ChevronRight className="w-4 h-4" />
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        
        <div className="py-6 border-t border-sacred-gold/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-base text-cosmic-text">
            &copy; {new Date().getFullYear()} Astro Rattan. {t('footer.madeWith')} <Heart className="w-4 h-4 inline text-sacred-gold" /> in India
          </p>
          <div className="flex gap-6">
            <span className="text-base text-cosmic-text">All rights reserved</span>
          </div>
        </div>
        <div className="pb-4 text-center">
          <p className="text-base text-cosmic-text-secondary" style={{ fontFamily: "'IM Fell English', serif" }}>
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
