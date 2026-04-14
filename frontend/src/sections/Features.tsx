import { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { useTranslation } from '@/lib/i18n';
import { X, Sparkles } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  const [lightbox, setLightbox] = useState<{ file: string; label: string } | null>(null);

  useEffect(() => {
    if (!lightbox) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setLightbox(null); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [lightbox]);

  const features = [
    {
      image: '/images/features/feature-lalkitab.png',
      title: l('Lal Kitab — Complete System', 'लाल किताब — पूर्ण सिस्टम'),
      subtitle: l('ONLY HERE', 'केवल यहाँ'),
      desc: l('Nishaniyan Matcher, Chandra Chalana 43-day protocol, Remedy Tracker with streaks, Teva classification, Dosha analysis, Annual Gochar, Planet analysis — the most complete Lal Kitab toolkit available.', 'निशानियां मैचर, चंद्र चालना 43-दिवसीय प्रोटोकॉल, स्ट्रीक्स के साथ उपाय ट्रैकर, तेवा वर्गीकरण, दोष विश्लेषण, वार्षिक गोचर — उपलब्ध सबसे पूर्ण लाल किताब टूलकिट।'),
      badge: l('EXCLUSIVE', 'विशेष'),
    },
    {
      image: '/images/features/feature-kundli.jpg',
      imagePosition: 'center top',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Kundli — 3 Vedic Systems', 'कुंडली — 3 वैदिक सिस्टम'),
      subtitle: l('Unmatched Depth', 'बेजोड़ गहराई'),
      desc: l('Parashari, Jaimini & KP System in one place. Ashtakvarga, Dasha timeline, Varshphal annual chart, Kundli Milan compatibility, General Remedies — 8 deep-analysis tools, not just a birth chart.', 'पाराशरी, जैमिनी और केपी सिस्टम एक जगह। अष्टकवर्ग, दशा टाइमलाइन, वर्षफल, कुंडली मिलान, सामान्य उपाय — केवल जन्म कुंडली नहीं, 8 गहन विश्लेषण टूल।'),
      badge: l('UNMATCHED DEPTH', 'बेजोड़ गहराई'),
    },
    {
      image: '/images/features/feature-horoscope.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Horoscope — Daily + Predictive', 'राशिफल — दैनिक + प्रेडिक्टिव'),
      subtitle: l('AI Powered', 'एआई समर्थित'),
      desc: l(
        'Personalized daily horoscope based on your exact birth chart. Not generic sun-sign predictions — real Dasha-based forecasts with transit overlays for accurate life event timing.',
        'आपकी सटीक जन्म कुंडली पर आधारित व्यक्तिगत दैनिक राशिफल। सामान्य सन-साइन भविष्यवाणी नहीं — दशा आधारित पूर्वानुमान और गोचर ओवरले के साथ अधिक सटीक समय निर्धारण।'
      ),
      badge: l('AI POWERED', 'एआई समर्थित'),
    },
    {
      image: '/images/features/feature-panchang.jpg',
      title: l('Live Panchang', 'लाइव पंचांग'),
      subtitle: l('Location-Aware', 'लोकेशन-आधारित'),
      desc: l('Real-time Tithi, Nakshatra, Yoga, Karana with exact end times. Rahu Kaal, Choghadiya, Muhurat finder — all calculated for YOUR location, not generic tables.', 'वास्तविक समय तिथि, नक्षत्र, योग, करण सटीक समाप्ति समय के साथ। राहु काल, चौघड़िया, मुहूर्त फाइंडर — सब आपके स्थान के लिए गणना की गई, सामान्य टेबल नहीं।'),
      badge: l('LOCATION-AWARE', 'लोकेशन-आधारित'),
    },
    {
      image: '/images/features/feature-numerology.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Numerology — Name + Mobile', 'अंकशास्त्र — नाम + मोबाइल'),
      subtitle: l('Dual Engine', 'डुअल इंजन'),
      desc: l(
        'Name numerology + mobile number numerology with Lo Shu grid logic, lucky numbers, compatibility signals, and practical correction suggestions.',
        'लो शु ग्रिड लॉजिक के साथ नाम अंकशास्त्र और मोबाइल नंबर अंकशास्त्र, भाग्यशाली अंक, अनुकूलता संकेत और व्यवहारिक सुधार सुझाव।'
      ),
      badge: l('DUAL ENGINE', 'डुअल इंजन'),
    },
    {
      image: '/images/features/feature-vastu.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Vastu Shastra Analyzer', 'वास्तु शास्त्र विश्लेषक'),
      subtitle: l('Pro', 'प्रो'),
      desc: l(
        'Floor plan scoring based on Vastu Purusha Mandala. Direction analysis for each room, remedies for doshas, and zone-wise energy mapping for home and office.',
        'वास्तु पुरुष मंडल के आधार पर फ्लोर प्लान स्कोरिंग। प्रत्येक कमरे की दिशा विश्लेषण, दोषों के उपाय और घर व कार्यालय के लिए ज़ोन-वाइज ऊर्जा मैपिंग।'
      ),
      badge: l('PRO', 'प्रो'),
    },
  ];


  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.features-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
      gsap.fromTo('.feature-card', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <>
    <section ref={sectionRef} id="features" className="relative pt-4 pb-24 bg-cosmic-bg">

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Section Header */}
        <div className="features-title text-center mb-16">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl text-sacred-gold-dark mb-6 leading-[1.1]" style={{ fontWeight: 800, letterSpacing: '-0.02em' }}>
            {l('Complete astrological operating system', 'पूर्ण ज्योतिषीय ऑपरेटिंग सिस्टम')}
          </h2>
          <div className="max-w-full mx-auto text-lg text-gray-600 leading-relaxed">
            <p>{l('Most astrology apps use lookup tables and generic predictions.', 'अधिकांश ज्योतिष ऐप लुकअप टेबल और सामान्य भविष्यवाणी का उपयोग करते हैं।')}</p>
            <p><strong className="text-sacred-gold-dark">{l('Astro Rattan computes every position from Swiss Ephemeris', 'Astro Rattan Swiss Ephemeris से हर स्थिति की गणना करता है')}</strong>{l(' — the same library used by research astronomers — accurate to arc-seconds.', ' — यही लाइब्रेरी शोध खगोलविद भी उपयोग करते हैं — आर्क-सेकंड तक सटीक।')}</p>
          </div>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="feature-card group relative bg-white border border-[#e0d5c5] overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-sacred-gold/10"
            >
              <div className="relative px-3 pt-3">
                <img
                  src={feature.image}
                  alt={feature.title}
                  className="w-full h-[180px] object-cover object-center"
                  style={{
                    objectPosition: feature.imagePosition || 'center center',
                    filter: feature.imageFilter || 'sepia(0.2) brightness(0.95) contrast(1.05)',
                  }}
                  loading="lazy"
                />
                {feature.badge && (
                  <span className="absolute top-3 right-3 z-10 bg-[#8B4513] text-white text-[10px] font-semibold px-[10px] py-1 rounded">
                    {feature.badge}
                  </span>
                )}
              </div>
              <CardContent className="p-5">
                <h3 className="text-lg font-sans font-semibold text-cosmic-text mb-1 uppercase tracking-wide">
                  {feature.title}
                </h3>
                <p className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wider mb-3">
                  {feature.subtitle}
                </p>
                <p className="text-sm text-gray-600 leading-relaxed">
                  {feature.desc}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>


        {/* CTA */}
        <div className="text-center mt-16">
          <p className="text-xl text-cosmic-text mb-6">
            {l('Ready to experience the difference?', 'अंतर अनुभव करने के लिए तैयार हैं?')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/login"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-sacred-gold-dark text-white rounded-lg font-semibold hover:bg-sacred-gold transition-all shadow-lg shadow-sacred-gold/20"
            >
              {l('Create Your Account', 'अपना अकाउंट बनाएं')}
              <Sparkles className="w-4 h-4" />
            </a>
            <a
              href="/kundli"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border-2 border-sacred-gold/50 text-sacred-gold-dark rounded-lg font-semibold hover:bg-sacred-gold/10 transition-all"
            >
              {l('Try Free Kundli', 'मुफ्त कुंडली देखें')}
            </a>
          </div>
        </div>

      </div>
    </section>

    {/* ── Lightbox ─────────────────────────────────────────────── */}
    {lightbox && (
      <div
        className="fixed inset-0 z-[9999] flex items-center justify-center p-4 sm:p-8"
        style={{ background: 'rgba(0,0,0,0.85)' }}
        onClick={() => setLightbox(null)}
      >
        {/* Card — stops propagation so clicking the image doesn't close */}
        <div
          className="relative max-w-5xl w-full rounded-2xl overflow-hidden shadow-2xl"
          onClick={e => e.stopPropagation()}
        >
          <img
            src={`/images/showcase/${lightbox.file}`}
            alt={lightbox.label}
            className="w-full h-auto block"
          />
          {/* Label bar */}
          <div className="px-6 py-4 flex items-center justify-between" style={{ background: '#1a1625' }}>
            <p className="text-sm font-bold uppercase tracking-widest" style={{ color: '#C4611F' }}>
              {lightbox.label}
            </p>
            <button
              type="button"
              onClick={() => setLightbox(null)}
              className="text-gray-500 hover:text-gray-800 transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* ESC hint */}
        <p className="absolute bottom-4 left-0 right-0 text-center text-white/50 text-xs pointer-events-none">
          {l('Press ESC or click outside to close', 'बंद करने के लिए ESC दबाएं या बाहर क्लिक करें')}
        </p>
      </div>
    )}
  </>
  );
}
