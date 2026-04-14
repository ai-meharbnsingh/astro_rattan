import { Link } from 'react-router-dom';
import { Mail, Phone, Heart, ArrowRight, MessageSquare } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

// Vastu is WIP — only visible on staging
const isProduction = typeof window !== 'undefined' && window.location.hostname === 'astrorattan.com';

export default function Footer() {
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  return (
    <footer className="bg-cosmic-bg border-t border-sacred-gold/30 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Newsletter band */}
        <div className="rounded-2xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 sm:p-8 text-center mb-8">
          <h3 className="text-2xl sm:text-3xl font-sans text-cosmic-text mb-2">{l('Subscribe to Newsletter', 'न्यूज़लेटर सब्सक्राइब करें')}</h3>
          <p className="text-sm text-cosmic-text/70 mb-5">
            {l('Receive personalized astrology insights directly in your inbox.', 'व्यक्तिगत ज्योतिषीय इनसाइट्स सीधे अपने इनबॉक्स में प्राप्त करें।')}
          </p>
          <div className="max-w-xl mx-auto flex items-stretch">
            <input
              type="email"
              placeholder={l('Enter your email', 'अपना ईमेल दर्ज करें')}
              className="flex-1 bg-cosmic-bg border border-sacred-gold/40 rounded-l-full px-4 py-3 text-sm text-cosmic-text placeholder:text-cosmic-text/50 focus:outline-none"
            />
            <button className="px-5 py-3 rounded-r-full bg-sacred-gold-dark text-white hover:opacity-90 transition-opacity">
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Footer link blocks */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 border-t border-sacred-gold/20 pt-8">
          <div>
            <h4 className="text-lg font-sans text-sacred-gold-dark mb-3">{t('footer.services')}</h4>
            <div className="space-y-2 text-sm">
              <Link to="/kundli" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Kundli', 'कुंडली')}</Link>
              <Link to="/horoscope" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Horoscope', 'राशिफल')}</Link>
              <Link to="/panchang" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Panchang', 'पंचांग')}</Link>
              <Link to="/lal-kitab" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Lal Kitab', 'लाल किताब')}</Link>
              <Link to="/numerology" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Numerology', 'अंकशास्त्र')}</Link>
              {!isProduction && <Link to="/vastu" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Vastu', 'वास्तु')}</Link>}
            </div>
          </div>

          <div>
            <h4 className="text-lg font-sans text-sacred-gold-dark mb-3">{l('Important Links', 'महत्वपूर्ण लिंक')}</h4>
            <div className="space-y-2 text-sm">
              <Link to="/about" className="block text-cosmic-text hover:text-sacred-gold-dark">{t('footer.aboutUs')}</Link>
              <Link to="/feedback" className="block text-cosmic-text hover:text-sacred-gold-dark">{t('nav.feedback')}</Link>
              <Link to="/login" className="block text-cosmic-text hover:text-sacred-gold-dark">{t('auth.signIn')}</Link>
            </div>
          </div>

          <div>
            <h4 className="text-lg font-sans text-sacred-gold-dark mb-3">{l('More Links', 'अन्य लिंक')}</h4>
            <div className="space-y-2 text-sm">
              <Link to="/" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Home', 'होम')}</Link>
              <Link to="/dashboard" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Dashboard', 'डैशबोर्ड')}</Link>
              <Link to="/kundli" className="block text-cosmic-text hover:text-sacred-gold-dark">{l('Book Consultation', 'कंसल्टेशन बुक करें')}</Link>
            </div>
          </div>

          <div>
            <h4 className="text-lg font-sans text-sacred-gold-dark mb-3">{l('Contact Us', 'संपर्क करें')}</h4>
            <div className="space-y-3 text-sm">
              <a href="mailto:info@astrorattan.com" className="flex items-center gap-2 text-cosmic-text hover:text-sacred-gold-dark">
                <Mail className="w-4 h-4" />info@astrorattan.com
              </a>
              <a href="tel:+918076025521" className="flex items-center gap-2 text-cosmic-text hover:text-sacred-gold-dark">
                <Phone className="w-4 h-4" />+91 80760 25521
              </a>
              <Link to="/feedback" className="inline-flex items-center gap-2 text-cosmic-text hover:text-sacred-gold-dark">
                <MessageSquare className="w-4 h-4" />{l('Send Feedback', 'फीडबैक भेजें')}
              </Link>
            </div>
          </div>
        </div>

        {/* Bottom strip */}
        <div className="mt-8 border-t border-sacred-gold/20 pt-4 flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
          <span className="text-xs text-cosmic-text/70">&copy; {new Date().getFullYear()} Astro Rattan {t('footer.madeWith')} <Heart className="w-3 h-3 inline text-sacred-gold" /> {t('footer.inIndia')}</span>
          <div className="flex items-center gap-4">
            <span className="text-sm text-cosmic-text/80">{l("Get Consultancy from India's best Astrologer.", 'भारत के श्रेष्ठ ज्योतिषी से कंसल्टेंसी पाएं।')}</span>
            <Link to="/kundli" className="px-4 py-2 rounded-full bg-sacred-gold-dark text-white text-sm font-medium hover:opacity-90">
              {l('Consult Now', 'अभी परामर्श करें')}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
