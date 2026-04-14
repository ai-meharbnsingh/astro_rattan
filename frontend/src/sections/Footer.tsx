import { Link } from 'react-router-dom';
import { Mail, Phone, Instagram, Youtube, Heart } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export default function Footer() {
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  return (
    <footer className="bg-cosmic-bg border-t border-sacred-gold/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 space-y-2 text-sm">
        {/* Row 1: Services horizontal */}
        <div className="flex flex-wrap items-center gap-1">
          <span className="font-semibold text-sacred-gold-dark mr-2">{t('footer.services')}:</span>
          <Link to="/kundli" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Kundli', 'कुंडली')}</Link>
          <span className="text-cosmic-text/30">|</span>
          <Link to="/panchang" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Panchang', 'पंचांग')}</Link>
          <span className="text-cosmic-text/30">|</span>
          <Link to="/lal-kitab" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Lal Kitab', 'लाल किताब')}</Link>
          <span className="text-cosmic-text/30">|</span>
          <Link to="/numerology" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Numerology', 'अंकशास्त्र')}</Link>
          <span className="text-cosmic-text/30">|</span>
          <Link to="/vastu" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Vastu', 'वास्तु')}</Link>
        </div>

        {/* Row 2: Company horizontal */}
        <div className="flex flex-wrap items-center gap-1">
          <span className="font-semibold text-sacred-gold-dark mr-2">{t('footer.company')}:</span>
          <Link to="/about" className="text-cosmic-text hover:text-sacred-gold-dark">{t('footer.aboutUs')}</Link>
          <span className="text-cosmic-text/30">|</span>
          <Link to="/privacy" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Privacy Policy', 'गोपनीयता नीति')}</Link>
          <span className="text-cosmic-text/30">|</span>
          <Link to="/terms" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Terms of Service', 'सेवा की शर्तें')}</Link>
        </div>

        {/* Row 3: Contact horizontal */}
        <div className="flex flex-wrap items-center gap-3">
          <a href="mailto:info@astrorattan.com" className="flex items-center gap-1 text-cosmic-text hover:text-sacred-gold-dark">
            <Mail className="w-3.5 h-3.5" />info@astrorattan.com
          </a>
          <a href="tel:+918076025521" className="flex items-center gap-1 text-cosmic-text hover:text-sacred-gold-dark">
            <Phone className="w-3.5 h-3.5" />+91 80760 25521
          </a>
          <a href="https://instagram.com/astrorattan" target="_blank" rel="noopener noreferrer" className="text-cosmic-text hover:text-sacred-gold-dark"><Instagram className="w-4 h-4" /></a>
          <a href="https://youtube.com/@astrorattan" target="_blank" rel="noopener noreferrer" className="text-cosmic-text hover:text-sacred-gold-dark"><Youtube className="w-4 h-4" /></a>
        </div>

        {/* Row 4: Copyright */}
        <div className="pt-2 border-t border-sacred-gold/20 flex flex-wrap items-center justify-between gap-2 text-xs text-cosmic-text/70">
          <span>&copy; {new Date().getFullYear()} Astro Rattan {t('footer.madeWith')} <Heart className="w-3 h-3 inline text-sacred-gold" /> {t('footer.inIndia')}</span>
          <span>{t('footer.poweredBy')} <a href="https://adaptive-mind.com" target="_blank" rel="noopener noreferrer" className="text-sacred-gold-dark hover:underline">Semantic Gravity</a></span>
        </div>
      </div>
    </footer>
  );
}
