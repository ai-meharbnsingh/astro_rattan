import { Link } from 'react-router-dom';
import { Mail, Phone, Instagram, Youtube, Heart } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export default function Footer() {
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  return (
    <footer className="bg-cosmic-bg border-t border-sacred-gold">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Main row: Logo+contact | Services | Company — all compact */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {/* Brand */}
          <div className="col-span-2 sm:col-span-2 flex items-start gap-3">
            <Link to="/">
              <img src="/logo.png" alt="Astro Rattan" className="h-12 w-auto" />
            </Link>
            <div className="text-sm text-cosmic-text">
              <p className="mb-1">{t('footer.tagline')}</p>
              <a href="mailto:info@astrorattan.com" className="flex items-center gap-1 hover:text-sacred-gold-dark">
                <Mail className="w-3.5 h-3.5" />info@astrorattan.com
              </a>
              <a href="tel:+918076025521" className="flex items-center gap-1 hover:text-sacred-gold-dark">
                <Phone className="w-3.5 h-3.5" />+91 80760 25521
              </a>
              <div className="flex gap-2 mt-1">
                <a href="https://instagram.com/astrorattan" target="_blank" rel="noopener noreferrer" className="text-cosmic-text hover:text-sacred-gold-dark"><Instagram className="w-4 h-4" /></a>
                <a href="https://youtube.com/@astrorattan" target="_blank" rel="noopener noreferrer" className="text-cosmic-text hover:text-sacred-gold-dark"><Youtube className="w-4 h-4" /></a>
              </div>
            </div>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-semibold text-sacred-gold-dark text-sm mb-2">{t('footer.services')}</h4>
            <ul className="space-y-1 text-sm">
              <li><Link to="/kundli" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Kundli', 'कुंडली')}</Link></li>
              <li><Link to="/panchang" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Panchang', 'पंचांग')}</Link></li>
              <li><Link to="/lal-kitab" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Lal Kitab', 'लाल किताब')}</Link></li>
              <li><Link to="/numerology" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Numerology', 'अंकशास्त्र')}</Link></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-semibold text-sacred-gold-dark text-sm mb-2">{t('footer.company')}</h4>
            <ul className="space-y-1 text-sm">
              <li><Link to="/about" className="text-cosmic-text hover:text-sacred-gold-dark">{t('footer.aboutUs')}</Link></li>
              <li><Link to="/" className="text-cosmic-text hover:text-sacred-gold-dark">{t('footer.contactShort')}</Link></li>
              <li><Link to="/privacy" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Privacy Policy', 'गोपनीयता नीति')}</Link></li>
              <li><Link to="/terms" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Terms of Service', 'सेवा की शर्तें')}</Link></li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-4 pt-3 border-t border-sacred-gold/30 flex flex-wrap items-center justify-between gap-2 text-xs text-cosmic-text">
          <span>&copy; {new Date().getFullYear()} Astro Rattan. {t('footer.madeWith')} <Heart className="w-3 h-3 inline text-sacred-gold" /> {t('footer.inIndia')}</span>
          <span>{l('Your data is encrypted and never shared.', 'आपका डेटा एन्क्रिप्टेड है।')}</span>
          <span>{t('footer.poweredBy')} <a href="https://adaptive-mind.com" target="_blank" rel="noopener noreferrer" className="text-sacred-gold-dark hover:underline">Semantic Gravity</a></span>
        </div>
      </div>
    </footer>
  );
}
