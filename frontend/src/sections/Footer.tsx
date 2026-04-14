import { Link } from 'react-router-dom';
import { Mail, Phone, Heart } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

// Vastu is WIP — only visible on staging
const isProduction = typeof window !== 'undefined' && window.location.hostname === 'astrorattan.com';

export default function Footer() {
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  return (
    <footer className="bg-cosmic-bg border-t border-sacred-gold/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 text-sm">
        {/* Table layout — aligned columns */}
        <table className="w-full">
          <tbody>
            <tr className="">
              <td className="py-1.5 pr-4 font-semibold text-sacred-gold-dark whitespace-nowrap w-24">{t('footer.services')}:</td>
              <td className="py-1.5 w-1/5"><Link to="/kundli" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Kundli', 'कुंडली')}</Link></td>
              <td className="py-1.5 w-1/5"><Link to="/panchang" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Panchang', 'पंचांग')}</Link></td>
              <td className="py-1.5 w-1/5"><Link to="/lal-kitab" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Lal Kitab', 'लाल किताब')}</Link></td>
              <td className="py-1.5 w-1/5"><Link to="/numerology" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Numerology', 'अंकशास्त्र')}</Link></td>
              {!isProduction && <td className="py-1.5 w-1/5"><Link to="/vastu" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Vastu', 'वास्तु')}</Link></td>}
            </tr>
            <tr className="">
              <td className="py-1.5 pr-4 font-semibold text-sacred-gold-dark whitespace-nowrap">{t('footer.company')}:</td>
              <td className="py-1.5"><Link to="/about" className="text-cosmic-text hover:text-sacred-gold-dark">{t('footer.aboutUs')}</Link></td>
              <td className="py-1.5"><Link to="/" className="text-cosmic-text hover:text-sacred-gold-dark">{t('footer.contactShort')}</Link></td>
              <td className="py-1.5"><Link to="/privacy" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Privacy Policy', 'गोपनीयता नीति')}</Link></td>
              <td className="py-1.5"><Link to="/terms" className="text-cosmic-text hover:text-sacred-gold-dark">{l('Terms of Service', 'सेवा की शर्तें')}</Link></td>
              <td className="py-1.5"></td>
            </tr>
            <tr>
              <td className="py-1.5 pr-4 font-semibold text-sacred-gold-dark whitespace-nowrap">{l('Contact', 'संपर्क')}:</td>
              <td className="py-1.5" colSpan={2}>
                <a href="mailto:info@astrorattan.com" className="flex items-center gap-1 text-cosmic-text hover:text-sacred-gold-dark">
                  <Mail className="w-3.5 h-3.5" />info@astrorattan.com
                </a>
              </td>
              <td className="py-1.5" colSpan={2}>
                <a href="tel:+918076025521" className="flex items-center gap-1 text-cosmic-text hover:text-sacred-gold-dark">
                  <Phone className="w-3.5 h-3.5" />+91 80760 25521
                </a>
              </td>
              <td className="py-1.5"></td>
            </tr>
          </tbody>
        </table>

        {/* Copyright */}
        <div className="pt-2 mt-2 border-t border-sacred-gold/20 flex items-center justify-between text-xs text-cosmic-text/60">
          <span>&copy; {new Date().getFullYear()} Astro Rattan {t('footer.madeWith')} <Heart className="w-3 h-3 inline text-sacred-gold" /> {t('footer.inIndia')}</span>
          <span>{t('footer.poweredBy')} <a href="https://adaptive-mind.com" target="_blank" rel="noopener noreferrer" className="text-sacred-gold-dark hover:underline">Semantic Gravity</a></span>
        </div>
      </div>
    </footer>
  );
}
