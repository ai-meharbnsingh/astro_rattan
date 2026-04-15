import { Link } from 'react-router-dom';
import { Mail, Phone, Heart, MessageSquare } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';

// Vastu is WIP — only visible on staging
const isProduction = typeof window !== 'undefined' && window.location.hostname === 'astrorattan.com';

export default function Footer() {
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  return (
    <footer className="bg-sacred-gold-dark border-t border-white/20 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Footer link blocks */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <Heading as={4} variant={4} className="text-[#f5d28a] mb-3">{t('footer.services')}</Heading>
            <div className="space-y-2 text-sm">
              <Link to="/kundli" className="block text-amber-100 hover:text-white">{l('Kundli', 'कुंडली')}</Link>
              <Link to="/horoscope" className="block text-amber-100 hover:text-white">{l('Horoscope', 'राशिफल')}</Link>
              <Link to="/panchang" className="block text-amber-100 hover:text-white">{l('Panchang', 'पंचांग')}</Link>
              <Link to="/lal-kitab" className="block text-amber-100 hover:text-white">{l('Lal Kitab', 'लाल किताब')}</Link>
              <Link to="/numerology" className="block text-amber-100 hover:text-white">{l('Numerology', 'अंकशास्त्र')}</Link>
              {!isProduction && <Link to="/vastu" className="block text-amber-100 hover:text-white">{l('Vastu', 'वास्तु')}</Link>}
            </div>
          </div>

          <div>
            <Heading as={4} variant={4} className="text-[#f5d28a] mb-3">{l('Important Links', 'महत्वपूर्ण लिंक')}</Heading>
            <div className="space-y-2 text-sm">
              <Link to="/about" className="block text-amber-100 hover:text-white">{t('footer.aboutUs')}</Link>
              <Link to="/feedback" className="block text-amber-100 hover:text-white">{t('nav.feedback')}</Link>
              <Link to="/login" className="block text-amber-100 hover:text-white">{t('auth.signIn')}</Link>
            </div>
          </div>

          <div>
            <Heading as={4} variant={4} className="text-[#f5d28a] mb-3">{l('More Links', 'अन्य लिंक')}</Heading>
            <div className="space-y-2 text-sm">
              <Link to="/" className="block text-amber-100 hover:text-white">{l('Home', 'होम')}</Link>
              <Link to="/dashboard" className="block text-amber-100 hover:text-white">{l('Dashboard', 'डैशबोर्ड')}</Link>
              <Link to="/kundli" className="block text-amber-100 hover:text-white">{l('Book Consultation', 'कंसल्टेशन बुक करें')}</Link>
            </div>
          </div>

          <div>
            <Heading as={4} variant={4} className="text-[#f5d28a] mb-3">{l('Contact Us', 'संपर्क करें')}</Heading>
            <div className="space-y-3 text-sm">
              <a href="mailto:info@astrorattan.com" className="flex items-center gap-2 text-amber-100 hover:text-white">
                <Mail className="w-4 h-4" />info@astrorattan.com
              </a>
              <a href="tel:+918076025521" className="flex items-center gap-2 text-amber-100 hover:text-white">
                <Phone className="w-4 h-4" />+91 80760 25521
              </a>
              <div className="flex items-center gap-3">
                <a href="https://instagram.com/astrorattan" target="_blank" rel="noopener noreferrer" className="text-amber-100 hover:text-white transition-colors" title="Instagram">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                </a>
                <a href="https://twitter.com/astrorattan" target="_blank" rel="noopener noreferrer" className="text-amber-100 hover:text-white transition-colors" title="Twitter / X">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                </a>
                <a href="https://facebook.com/astrorattan" target="_blank" rel="noopener noreferrer" className="text-amber-100 hover:text-white transition-colors" title="Facebook">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="https://linkedin.com/company/astrorattan" target="_blank" rel="noopener noreferrer" className="text-amber-100 hover:text-white transition-colors" title="LinkedIn">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                </a>
              </div>
              <Link to="/feedback" className="inline-flex items-center gap-2 text-amber-100 hover:text-white">
                <MessageSquare className="w-4 h-4" />{l('Send Feedback', 'फीडबैक भेजें')}
              </Link>
            </div>
          </div>
        </div>

        {/* Bottom strip */}
        <div className="mt-8 border-t border-white/20 pt-4 flex flex-col gap-3 items-center text-center">
          <span className="text-sm text-amber-100/85">&copy; {new Date().getFullYear()} Astro Rattan (Powered by: <a href="https://www.adaptive-mind.com" target="_blank" rel="noopener noreferrer" className="text-[#f5d28a] hover:text-white underline">Semantic Gravity</a>). All Rights Reserved</span>
        </div>
      </div>
    </footer>
  );
}
