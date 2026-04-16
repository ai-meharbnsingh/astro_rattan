import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { useTranslation } from '@/lib/i18n';
import { Users, Grid3X3, Star, User, Phone, Calendar, Clock, MapPin, Sparkles, ChevronRight, Mail, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import LiveTransitWheel from '@/components/LiveTransitWheel';
import FreeKundliModal from '@/components/FreeKundliModal';
import { Heading } from '@/components/ui/heading';

const TAGLINE = { en: 'A complete astrology platform', hi: 'एक पूर्ण ज्योतिष प्लेटफ़ॉर्म' };

export default function Hero() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { t, language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.hero-shloka',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 1, delay: 0.3, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-title-main',
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 1.2, delay: 0.5, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-subtitle',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 1, delay: 0.7, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-cta',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8, delay: 0.9, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-wheel',
        { opacity: 0, scale: 0.85 },
        { opacity: 1, scale: 1, duration: 1.4, delay: 0.6, ease: 'power3.out' }
      );
      gsap.fromTo('.hero-stats',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8, delay: 1.1, ease: 'power3.out' }
      );
    }, heroRef);
    return () => ctx.revert();
  }, []);


  return (
    <section ref={heroRef} className="relative min-h-[60vh] flex items-center overflow-hidden pt-24 pb-6">
      {/* Background — noise texture */}
      <div className="absolute inset-0 z-[1] opacity-[0.03] pointer-events-none"
        style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")` }}
      />
      {/* Depth radial gradient behind text side */}
      <div className="absolute inset-0 z-[2] pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at 30% 50%, rgba(196,97,31,0.06) 0%, rgba(245,240,232,0) 60%)' }}
      />

      {/* Floating orbs */}
      <div className="absolute top-1/4 left-10 w-64 h-64 bg-sacred-gold/5 rounded-full blur-3xl opacity-20" />
      <div className="absolute bottom-1/4 right-10 w-80 h-80 bg-[#8B4513]/10 rounded-full blur-3xl opacity-20" />

      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-0">
        {/* Centered header above main section */}
        <div className="text-center">
          {/* Shloka */}
          <div className="hero-shloka opacity-0 mt-6">
            <p className="font-sans text-lg sm:text-2xl lg:text-[2.2rem] opacity-70 tracking-[3px] text-gray-600"
              style={{ textShadow: '0 0 15px rgba(255, 170, 51, 0.4)' }}>
              {'\u091C\u094D\u092F\u094B\u0924\u093F\u0937\u092E\u094D \u0905\u092F\u092E\u094D \u092C\u094D\u0930\u0939\u094D\u092E'} {t('hero.shlokaSupreme')}
            </p>
          </div>

          {/* Main Title */}
          <div className="hero-title-main opacity-0 mt-0 h-10 sm:h-12">
            <p className="text-sacred-gold-dark leading-[1.1] transition-opacity duration-500 font-normal text-2xl md:text-3xl">
              {language === 'hi' ? TAGLINE.hi : TAGLINE.en}
            </p>
          </div>

          {/* Quick nav links */}
          <div className="hero-shloka opacity-0 flex flex-wrap justify-center items-center gap-x-0 gap-y-0.5 mt-3 text-[11px] sm:text-[13px] text-sacred-gold-dark">
            {[
              { label: language === 'hi' ? 'राशिफल' : 'Horoscope', id: 'horoscope-section', href: '/horoscope' },
              { label: language === 'hi' ? 'पंचांग' : 'Panchang', id: 'panchang-section', href: '/panchang' },
              { label: language === 'hi' ? 'होरा' : 'Hora', id: 'hora-section', href: '/panchang' },
              { label: language === 'hi' ? 'चौघड़िया' : 'Choghadiya', id: 'hora-section', href: '/panchang' },
              { label: language === 'hi' ? 'सवाल-जवाब' : 'FAQ', id: 'faq-section', href: '' },
            ].map((item, i, arr) => (
              <span key={item.label} className="inline-flex items-center">
                <button
                  type="button"
                  onClick={() => {
                    const el = document.getElementById(item.id);
                    if (el) {
                      const y = el.getBoundingClientRect().top + window.scrollY - 80;
                      window.scrollTo({ top: y, behavior: 'smooth' });
                    } else if (item.href) {
                      window.location.href = item.href;
                    }
                  }}
                  className="hover:underline hover:text-sacred-gold cursor-pointer px-1.5 sm:px-2"
                >
                  {item.label}
                </button>
                {i < arr.length - 1 && <span className="text-sacred-gold/40">|</span>}
              </span>
            ))}
          </div>

        </div>

        {/* Two-column layout */}
        <div className="flex flex-col lg:flex-row items-stretch gap-6 lg:gap-10 mt-1">

          {/* LEFT — Kundli Form */}
          <div className="hero-cta opacity-0 w-full lg:w-[38%] shrink-0 lg:mt-[90px]">
            <div className="mb-5 text-center">
              <div className="inline-block rounded-xl px-5 py-2"
                style={{
                  background: 'linear-gradient(135deg, rgba(196,97,31,0.15) 0%, rgba(139,69,19,0.22) 100%)',
                  border: '1px solid rgba(196,97,31,0.35)',
                  boxShadow: '0 4px 20px rgba(196,97,31,0.15), inset 0 1px 0 rgba(255,255,255,0.4)',
                }}>
                <Heading as={2} variant={2} className="text-sacred-gold-dark tracking-tight"
                  style={{ textShadow: '0 2px 10px rgba(196,97,31,0.3)' }}>
                  {l('Get your free kundli', 'अपनी मुफ्त कुंडली पाएं')}
                </Heading>
              </div>
              <div className="h-1 w-24 rounded-full bg-gradient-to-r from-transparent via-sacred-gold-dark to-transparent mt-2 mx-auto" />
            </div>
            <HeroKundliForm language={language} l={l} />
          </div>

          {/* RIGHT — Zodiac Wheel */}
          <div className="hero-wheel opacity-0 w-full lg:w-[62%] -mt-14">
            <LiveTransitWheel />
          </div>

        </div>

        {/* Stats strip — separate section below hero */}
        <div className="hero-stats opacity-0 mt-16">
          <div className="rounded-2xl bg-sacred-gold/5 p-4 sm:p-5">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="rounded-xl border border-sacred-gold/25 bg-background/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Star className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-foreground">{l('10,000+ Kundlis Generated', '10,000+ कुंडलियां बनाई गईं')}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{l('Real usage data', 'वास्तविक उपयोग डेटा')}</p>
                </div>
              </div>
              <div className="rounded-xl border border-sacred-gold/25 bg-background/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Users className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-foreground">{l('Trusted by Astrologers', 'ज्योतिषियों द्वारा विश्वसनीय')}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{l('Professional daily workflows', 'पेशेवर दैनिक वर्कफ़्लो')}</p>
                </div>
              </div>
              <div className="rounded-xl border border-sacred-gold/25 bg-background/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Grid3X3 className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-foreground">{l('5 Modules in One', 'एक में 5 मॉड्यूल')}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{l('Single connected platform', 'एकीकृत सिंगल प्लेटफॉर्म')}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ── Inline Kundli Form for Hero ── */
function HeroKundliForm({ language, l }: { language: string; l: (en: string, hi: string) => string }) {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [gender, setGender] = useState('male');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [birthTime, setBirthTime] = useState('');
  const [birthPlace, setBirthPlace] = useState('');
  const [suggestions, setSuggestions] = useState<Array<{ name: string; lat: number; lon: number }>>([]);
  const [selectedPlace, setSelectedPlace] = useState<{ lat: number; lon: number } | null>(null);
  const [marketingConsent, setMarketingConsent] = useState(false);
  const [previewData, setPreviewData] = useState<any>(null);
  const [generating, setGenerating] = useState(false);
  const searchTimer = useRef<ReturnType<typeof setTimeout>>();

  const searchPlace = (q: string) => {
    setBirthPlace(q);
    setSelectedPlace(null);
    if (searchTimer.current) clearTimeout(searchTimer.current);
    if (q.length < 3) { setSuggestions([]); return; }
    searchTimer.current = setTimeout(async () => {
      try {
        const res = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(q)}`);
        setSuggestions(Array.isArray(res) ? res : []);
      } catch { setSuggestions([]); }
    }, 300);
  };

  const selectPlace = (p: { name: string; lat: number; lon: number }) => {
    setBirthPlace(p.name.split(',')[0]);
    setSelectedPlace({ lat: p.lat, lon: p.lon });
    setSuggestions([]);
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const data = await api.post('/api/kundli/free-preview', {
        name,
        birth_date: birthDate,
        birth_time: birthTime + ':00',
        birth_place: birthPlace,
        latitude: selectedPlace?.lat,
        longitude: selectedPlace?.lon,
        timezone_offset: 5.5,
        gender,
        phone,
        email,
        marketing_consent: marketingConsent,
      });
      setPreviewData(data);
    } catch {
      // fallback: navigate to /kundli as before
      navigate('/kundli', {
        state: {
          prefillName: name, prefillGender: gender, prefillPhone: phone, prefillEmail: email,
          prefillDate: birthDate, prefillTime: birthTime,
          prefillPlace: birthPlace,
          prefillLat: selectedPlace?.lat, prefillLon: selectedPlace?.lon,
        },
      });
    }
    setGenerating(false);
  };

  const inputClass = "w-full px-3 py-1.5 pl-9 rounded-lg bg-[#f0ecf8]/40 border border-sacred-gold/50 text-foreground text-sm focus:border-sacred-gold focus:outline-none placeholder:text-sacred-gold-dark/40";

  return (
    <div className="flex flex-col justify-start gap-3">
      {/* Fields — exact like screenshot: no heading */}
      <div className="flex flex-col gap-6">
        {/* Full Name */}
        <div>
          <label className="text-sm font-semibold text-foreground mb-0 block">{l('Full Name', 'पूरा नाम')}</label>
          <div className="relative mt-1">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
            <input type="text" value={name} onChange={e => setName(e.target.value)}
              placeholder={l('Enter full name', 'पूरा नाम दर्ज करें')} className={inputClass} />
          </div>
        </div>

        {/* Gender + Birth Place */}
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="text-sm font-semibold text-foreground mb-0 block">{l('Gender', 'लिंग')}</label>
            <div className="flex gap-4 mt-1">
              <button onClick={() => setGender('male')}
                className={`flex-1 py-1.5 rounded-lg text-sm font-semibold transition-all ${gender === 'male' ? 'bg-sacred-gold-dark text-white' : 'border border-sacred-gold/50 text-foreground'}`}>
                {l('Male', 'पुरुष')}
              </button>
              <button onClick={() => setGender('female')}
                className={`flex-1 py-1.5 rounded-lg text-sm font-semibold transition-all ${gender === 'female' ? 'bg-sacred-gold-dark text-white' : 'border border-sacred-gold/50 text-foreground'}`}>
                {l('Female', 'महिला')}
              </button>
            </div>
          </div>
          <div className="relative">
            <label className="text-sm font-semibold text-foreground mb-0 block">{l('Birth Place', 'जन्म स्थान')}</label>
            <div className="relative mt-1">
              <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="text" value={birthPlace} onChange={e => searchPlace(e.target.value)}
                placeholder={l('Search birth place', 'जन्म स्थान खोजें')} className={inputClass} />
            </div>
            {suggestions.length > 0 && (
              <div className="absolute left-0 right-0 top-full z-30 bg-white border border-sacred-gold/30 rounded-lg shadow-lg max-h-40 overflow-y-auto mt-1">
                {suggestions.map((s, idx) => (
                  <button key={idx} onClick={() => selectPlace(s)}
                    className="w-full text-left px-3 py-2 text-xs text-foreground hover:bg-sacred-gold/10 transition-colors">
                    {s.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Birth Date + Time */}
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="text-sm font-semibold text-foreground mb-0 block">{l('Birth Date', 'जन्म तिथि')}</label>
            <div className="relative mt-1">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="date" value={birthDate} onChange={e => setBirthDate(e.target.value)} className={inputClass} />
            </div>
          </div>
          <div>
            <label className="text-sm font-semibold text-foreground mb-0 block">{l('Birth Time', 'जन्म समय')}</label>
            <div className="relative mt-1">
              <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="time" step="1" value={birthTime} onChange={e => setBirthTime(e.target.value)} className={inputClass} />
            </div>
          </div>
        </div>

        {/* Phone + Email (Required) */}
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="text-sm font-semibold text-foreground mb-0 block">
              {l('Phone', '\u092B\u093C\u094B\u0928')} <span className="text-red-500">*</span>
            </label>
            <div className="relative mt-1">
              <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="tel" required value={phone} onChange={e => setPhone(e.target.value)}
                placeholder={l('Phone number', '\u092B\u093C\u094B\u0928 \u0928\u0902\u092C\u0930')} className={inputClass} />
            </div>
          </div>
          <div>
            <label className="text-sm font-semibold text-foreground mb-0 block">
              {l('Email', '\u0908\u092E\u0947\u0932')} <span className="text-red-500">*</span>
            </label>
            <div className="relative mt-1">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
                placeholder={l('Email address', '\u0908\u092E\u0947\u0932 \u092A\u0924\u093E')} className={inputClass} />
            </div>
          </div>
        </div>

        {/* Marketing consent */}
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={marketingConsent}
            onChange={(e) => setMarketingConsent(e.target.checked)}
            className="w-4 h-4 accent-sacred-gold"
          />
          <span className="text-xs text-gray-600">
            {l('Send me astrological updates & offers', '\u092E\u0941\u091D\u0947 \u091C\u094D\u092F\u094B\u0924\u093F\u0937\u0940\u092F \u0905\u092A\u0921\u0947\u091F \u0914\u0930 \u0911\u092B\u093C\u0930 \u092D\u0947\u091C\u0947\u0902')}
          </span>
        </label>
      </div>

      {/* Submit */}
      {(() => {
        const isFormValid = name && birthDate && birthTime && birthPlace && selectedPlace && phone && email;
        return (
          <button onClick={handleGenerate}
            disabled={!isFormValid || generating}
            className={`w-full py-2.5 rounded-lg font-semibold text-base transition-all flex items-center justify-center gap-2 shrink-0 ${
              isFormValid && !generating
                ? 'bg-sacred-gold hover:bg-sacred-gold-dark text-white cursor-pointer'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}>
            {generating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                {l('Generating...', '\u092C\u0928\u093E \u0930\u0939\u0947 \u0939\u0948\u0902...')}
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                {l('Submit', '\u091C\u092E\u093E \u0915\u0930\u0947\u0902')}
                <ChevronRight className="w-4 h-4" />
              </>
            )}
          </button>
        );
      })()}

      {/* Free Kundli Preview Modal */}
      {previewData && (
        <FreeKundliModal
          data={previewData}
          onClose={() => setPreviewData(null)}
          language={language}
        />
      )}
    </div>
  );
}
