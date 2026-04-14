import { Link } from 'react-router-dom';
import { Mail, Phone, Heart, ArrowRight, MessageSquare } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

// Vastu is WIP — only visible on staging
const isProduction = typeof window !== 'undefined' && window.location.hostname === 'astrorattan.com';

export default function Footer() {
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  return (
    <footer className="bg-sacred-gold-dark border-t border-white/20 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Newsletter band */}
        <div className="rounded-2xl border border-white/20 bg-white/5 p-6 sm:p-8 text-center mb-8">
          <h3 className="text-2xl sm:text-3xl font-sans text-white mb-2">{l('Subscribe to Newsletter', 'न्यूज़लेटर सब्सक्राइब करें')}</h3>
          <p className="text-sm text-amber-100/90 mb-5">
            {l('Receive personalized astrology insights directly in your inbox.', 'व्यक्तिगत ज्योतिषीय इनसाइट्स सीधे अपने इनबॉक्स में प्राप्त करें।')}
          </p>
          <div className="max-w-xl mx-auto flex items-stretch">
            <input
              type="email"
              placeholder={l('Enter your email', 'अपना ईमेल दर्ज करें')}
              className="flex-1 bg-white/10 border border-white/25 rounded-l-full px-4 py-3 text-sm text-white placeholder:text-amber-100/70 focus:outline-none"
            />
            <button className="px-5 py-3 rounded-r-full bg-[#f5d28a] text-[#5c2414] hover:bg-[#ffe2a8] transition-colors">
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Footer link blocks */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 border-t border-white/20 pt-8">
          <div>
            <h4 className="text-lg font-sans text-[#f5d28a] mb-3">{t('footer.services')}</h4>
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
            <h4 className="text-lg font-sans text-[#f5d28a] mb-3">{l('Important Links', 'महत्वपूर्ण लिंक')}</h4>
            <div className="space-y-2 text-sm">
              <Link to="/about" className="block text-amber-100 hover:text-white">{t('footer.aboutUs')}</Link>
              <Link to="/feedback" className="block text-amber-100 hover:text-white">{t('nav.feedback')}</Link>
              <Link to="/login" className="block text-amber-100 hover:text-white">{t('auth.signIn')}</Link>
            </div>
          </div>

          <div>
            <h4 className="text-lg font-sans text-[#f5d28a] mb-3">{l('More Links', 'अन्य लिंक')}</h4>
            <div className="space-y-2 text-sm">
              <Link to="/" className="block text-amber-100 hover:text-white">{l('Home', 'होम')}</Link>
              <Link to="/dashboard" className="block text-amber-100 hover:text-white">{l('Dashboard', 'डैशबोर्ड')}</Link>
              <Link to="/kundli" className="block text-amber-100 hover:text-white">{l('Book Consultation', 'कंसल्टेशन बुक करें')}</Link>
            </div>
          </div>

          <div>
            <h4 className="text-lg font-sans text-[#f5d28a] mb-3">{l('Contact Us', 'संपर्क करें')}</h4>
            <div className="space-y-3 text-sm">
              <a href="mailto:info@astrorattan.com" className="flex items-center gap-2 text-amber-100 hover:text-white">
                <Mail className="w-4 h-4" />info@astrorattan.com
              </a>
              <a href="tel:+918076025521" className="flex items-center gap-2 text-amber-100 hover:text-white">
                <Phone className="w-4 h-4" />+91 80760 25521
              </a>
              <Link to="/feedback" className="inline-flex items-center gap-2 text-amber-100 hover:text-white">
                <MessageSquare className="w-4 h-4" />{l('Send Feedback', 'फीडबैक भेजें')}
              </Link>
            </div>
          </div>
        </div>

        {/* Bottom strip */}
        <div className="mt-8 border-t border-white/20 pt-4 flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
          <span className="text-xs text-amber-100/85">&copy; {new Date().getFullYear()} Astro Rattan {t('footer.madeWith')} <Heart className="w-3 h-3 inline text-[#f5d28a]" /> {t('footer.inIndia')}</span>
          <div className="flex items-center gap-4">
            <span className="text-sm text-amber-100/90">{l("Get Consultancy from India's best Astrologer.", 'भारत के श्रेष्ठ ज्योतिषी से कंसल्टेंसी पाएं।')}</span>
            <Link to="/kundli" className="px-4 py-2 rounded-full bg-[#f5d28a] text-[#5c2414] text-sm font-medium hover:bg-[#ffe2a8] transition-colors">
              {l('Consult Now', 'अभी परामर्श करें')}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
