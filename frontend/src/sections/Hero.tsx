import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { useTranslation } from '@/lib/i18n';
import { Users, Grid3X3, Star, User, Phone, Calendar, Clock, MapPin, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import LiveTransitWheel from '@/components/LiveTransitWheel';

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
          <div className="hero-shloka opacity-0">
            <p className="font-sans text-lg sm:text-2xl lg:text-[2.2rem] opacity-70 tracking-[3px] text-gray-600"
              style={{ textShadow: '0 0 15px rgba(255, 170, 51, 0.4)' }}>
              {'\u091C\u094D\u092F\u094B\u0924\u093F\u0937\u092E\u094D \u0905\u092F\u092E\u094D \u092C\u094D\u0930\u0939\u094D\u092E'} {t('hero.shlokaSupreme')}
            </p>
          </div>

          {/* Main Title */}
          <div className="hero-title-main opacity-0 mt-0">
            <h1
              className="text-xl sm:text-2xl lg:text-3xl text-cosmic-text leading-[1.1] font-sans"
              style={{
                fontWeight: 700,
                letterSpacing: '0',
              }}
            >
              {l('A Complete Astrology Platform', 'एक पूर्ण ज्योतिष प्लेटफॉर्म')}
            </h1>
          </div>

        </div>

        {/* Two-column layout */}
        <div className="flex flex-col lg:flex-row items-stretch gap-4 lg:gap-6 mt-1">

          {/* LEFT — Kundli Form */}
          <div className="hero-cta opacity-0 w-full lg:w-[38%] shrink-0">
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
              <div className="rounded-xl border border-sacred-gold/25 bg-cosmic-bg/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Star className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-cosmic-text">{l('10,000+ Kundlis Generated', '10,000+ कुंडलियां बनाई गईं')}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{l('Real usage data', 'वास्तविक उपयोग डेटा')}</p>
                </div>
              </div>
              <div className="rounded-xl border border-sacred-gold/25 bg-cosmic-bg/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Users className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-cosmic-text">{l('Trusted by Astrologers', 'ज्योतिषियों द्वारा विश्वसनीय')}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{l('Professional daily workflows', 'पेशेवर दैनिक वर्कफ़्लो')}</p>
                </div>
              </div>
              <div className="rounded-xl border border-sacred-gold/25 bg-cosmic-bg/70 p-3 sm:p-4 flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark flex items-center justify-center shrink-0">
                  <Grid3X3 className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-base font-semibold text-cosmic-text">{l('5 Modules in One', 'एक में 5 मॉड्यूल')}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{l('Single connected platform', 'एकीकृत सिंगल प्लेटफॉर्म')}</p>
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
  const [birthDate, setBirthDate] = useState('');
  const [birthTime, setBirthTime] = useState('');
  const [birthPlace, setBirthPlace] = useState('');
  const [suggestions, setSuggestions] = useState<Array<{ name: string; lat: number; lon: number }>>([]);
  const [selectedPlace, setSelectedPlace] = useState<{ lat: number; lon: number } | null>(null);
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

  const handleGenerate = () => {
    navigate('/kundli', {
      state: {
        prefillName: name, prefillGender: gender, prefillPhone: phone,
        prefillDate: birthDate, prefillTime: birthTime,
        prefillPlace: birthPlace,
        prefillLat: selectedPlace?.lat, prefillLon: selectedPlace?.lon,
      },
    });
  };

  const inputClass = "w-full px-3 py-2.5 pl-9 rounded-lg bg-[#f0ecf8]/40 border border-sacred-gold/50 text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none placeholder:text-sacred-gold-dark/40";

  return (
    <div className="flex flex-col h-full justify-between">
      {/* Heading */}
      <h3 className="text-base text-cosmic-text font-medium pb-1 border-b border-cosmic-border shrink-0">
        {l('Generate Your Kundli', 'अपनी कुंडली बनाएं')}
      </h3>

      {/* Fields — stretch to fill height */}
      <div className="flex-1 flex flex-col justify-between py-2 gap-1">
        {/* Full Name */}
        <div>
          <label className="text-sm font-semibold text-cosmic-text mb-0.5 block">{l('Full Name', 'पूरा नाम')}</label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
            <input type="text" value={name} onChange={e => setName(e.target.value)}
              placeholder={l('Enter full name', 'पूरा नाम दर्ज करें')} className={inputClass} />
          </div>
        </div>

        {/* Gender + Phone */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-sm font-semibold text-cosmic-text mb-0.5 block">{l('Gender', 'लिंग')}</label>
            <div className="flex gap-2">
              <button onClick={() => setGender('male')}
                className={`flex-1 py-2 rounded-lg text-sm font-semibold transition-all ${gender === 'male' ? 'bg-sacred-gold-dark text-white' : 'border border-sacred-gold/50 text-cosmic-text'}`}>
                {l('Male', 'पुरुष')}
              </button>
              <button onClick={() => setGender('female')}
                className={`flex-1 py-2 rounded-lg text-sm font-semibold transition-all ${gender === 'female' ? 'bg-sacred-gold-dark text-white' : 'border border-sacred-gold/50 text-cosmic-text'}`}>
                {l('Female', 'महिला')}
              </button>
            </div>
          </div>
          <div>
            <label className="text-sm font-semibold text-cosmic-text mb-0.5 block">{l('Phone', 'फ़ोन')}</label>
            <div className="relative">
              <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="tel" value={phone} onChange={e => setPhone(e.target.value)}
                placeholder={l('Number', 'नंबर')} className={inputClass} />
            </div>
          </div>
        </div>

        {/* Birth Date + Time */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-sm font-semibold text-cosmic-text mb-0.5 block">{l('Birth Date', 'जन्म तिथि')}</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="date" value={birthDate} onChange={e => setBirthDate(e.target.value)} className={inputClass} />
            </div>
          </div>
          <div>
            <label className="text-sm font-semibold text-cosmic-text mb-0.5 block">{l('Birth Time', 'जन्म समय')}</label>
            <div className="relative">
              <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
              <input type="time" step="1" value={birthTime} onChange={e => setBirthTime(e.target.value)} className={inputClass} />
            </div>
          </div>
        </div>

        {/* Birth Place */}
        <div className="relative">
          <label className="text-sm font-semibold text-cosmic-text mb-0.5 block">{l('Birth Place', 'जन्म स्थान')}</label>
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50" />
            <input type="text" value={birthPlace} onChange={e => searchPlace(e.target.value)}
              placeholder={l('Search birth place', 'जन्म स्थान खोजें')} className={inputClass} />
          </div>
          {suggestions.length > 0 && (
            <div className="absolute left-0 right-0 top-full z-30 bg-white border border-sacred-gold/30 rounded-lg shadow-lg max-h-40 overflow-y-auto mt-1">
              {suggestions.map((s, idx) => (
                <button key={idx} onClick={() => selectPlace(s)}
                  className="w-full text-left px-3 py-2 text-xs text-cosmic-text hover:bg-sacred-gold/10 transition-colors">
                  {s.name}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Submit */}
      <button onClick={handleGenerate}
        disabled={!name || !birthDate || !birthTime || !birthPlace}
        className="w-full py-3 bg-sacred-gold/70 text-sacred-gold-dark rounded-lg font-semibold text-base hover:bg-sacred-gold hover:text-white transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 shrink-0">
        <Sparkles className="w-4 h-4" />
        {l('Generate Kundli', 'कुंडली बनाएं')}
      </button>
    </div>
  );
}
