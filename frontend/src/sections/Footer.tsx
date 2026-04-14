import { Link } from 'react-router-dom';
import { Mail, Phone, Instagram, Youtube, Heart } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export default function Footer() {
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  return (
    <footer className="bg-cosmic-bg border-t border-sacred-gold/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 space-y-1.5 text-sm">
        {/* Row 1: Services spread across full width */}
        <div className="flex items-center justify-between">
          <span className="font-semibold text-sacred-gold-dark">{t('footer.services')}:</span>
          <div className="flex-1 flex items-center justify-evenly">
            <Link to="/kundli" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Kundli', 'कुंडली')}</Link>
            <Link to="/panchang" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Panchang', 'पंचांग')}</Link>
            <Link to="/lal-kitab" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Lal Kitab', 'लाल किताब')}</Link>
            <Link to="/numerology" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Numerology', 'अंकशास्त्र')}</Link>
            <Link to="/vastu" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Vastu', 'वास्तु')}</Link>
          </div>
        </div>

        {/* Row 2: Company spread across full width */}
        <div className="flex items-center justify-between">
          <span className="font-semibold text-sacred-gold-dark">{t('footer.company')}:</span>
          <div className="flex-1 flex items-center justify-evenly">
            <Link to="/about" className="text-cosmic-text hover:text-sacred-gold-dark">{t('footer.aboutUs')}</Link>
            <Link to="/" className="text-cosmic-text hover:text-sacred-gold-dark">{t('footer.contactShort')}</Link>
            <Link to="/privacy" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Privacy', 'गोपनीयता')}</Link>
            <Link to="/terms" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Terms', 'शर्तें')}</Link>
          </div>
        </div>

        {/* Row 3: Contact spread across full width */}
        <div className="flex items-center justify-between">
          <span className="font-semibold text-sacred-gold-dark">{l('Contact', 'संपर्क')}:</span>
          <div className="flex-1 flex items-center justify-evenly">
            <a href="mailto:info@astrorattan.com" className="flex items-center gap-1 text-cosmic-text hover:text-sacred-gold-dark"><Mail className="w-3.5 h-3.5" />info@astrorattan.com</a>
            <a href="tel:+918076025521" className="flex items-center gap-1 text-cosmic-text hover:text-sacred-gold-dark"><Phone className="w-3.5 h-3.5" />+91 80760 25521</a>
            <a href="https://instagram.com/astrorattan" target="_blank" rel="noopener noreferrer" className="text-cosmic-text hover:text-sacred-gold-dark"><Instagram className="w-4 h-4" /></a>
            <a href="https://youtube.com/@astrorattan" target="_blank" rel="noopener noreferrer" className="text-cosmic-text hover:text-sacred-gold-dark"><Youtube className="w-4 h-4" /></a>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-1.5 border-t border-sacred-gold/20 flex items-center justify-between text-xs text-cosmic-text/60">
          <span>&copy; {new Date().getFullYear()} Astro Rattan {t('footer.madeWith')} <Heart className="w-3 h-3 inline text-sacred-gold" /> {t('footer.inIndia')}</span>
          <span>{t('footer.poweredBy')} <a href="https://adaptive-mind.com" target="_blank" rel="noopener noreferrer" className="text-sacred-gold-dark hover:underline">Semantic Gravity</a></span>
        </div>
      </div>
    </footer>
  );
}
