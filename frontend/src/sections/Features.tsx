import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { useTranslation } from '@/lib/i18n';
import { Star, Clock, BookOpen, Calculator, Globe, Users, Check, X, Sparkles } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  const features = [
    {
      icon: <Star className="w-6 h-6" />,
      title: l('22 Lal Kitab Specializations', '22 लाल किताब विशेषताएं'),
      subtitle: l('ONLY here', 'केवल यहाँ'),
      desc: l('Nishaniyan Matcher, Chandra Chalana 43-day protocol, Remedy Tracker with streaks, Teva classification, Dosha analysis — the most complete Lal Kitab system available.', 'निशानियां मैचर, चंद्र चालना 43-दिवसीय प्रोटोकॉल, स्ट्रीक्स के साथ उपाय ट्रैकर, तेवा वर्गीकरण, दोष विश्लेषण — उपलब्ध सबसे पूर्ण लाल किताब सिस्टम।'),
      badge: l('EXCLUSIVE', 'विशेष'),
      color: 'from-amber-500/20 to-orange-500/10',
    },
    {
      icon: <Calculator className="w-6 h-6" />,
      title: l('21 Kundli Engines', '21 कुंडली इंजन'),
      subtitle: l('Unmatched Depth', 'बेजोड़ गहराई'),
      desc: l('Parashari + Jaimini + KP System. Divisional charts D1-D60, Shadbala strength analysis, Ashtakvarga bindu calculations — depth no other app matches.', 'पाराशरी + जैमिनी + केपी सिस्टम। विभाजन चार्ट D1-D60, शडबल शक्ति विश्लेषण, अष्टकवर्ग बिंदु गणना — ऐसी गहराई कोई अन्य ऐप नहीं मिलती।'),
      badge: null,
      color: 'from-blue-500/20 to-cyan-500/10',
    },
    {
      icon: <BookOpen className="w-6 h-6" />,
      title: l('Classical Interpretations', 'शास्त्रीय व्याख्याएं'),
      subtitle: l('Authentic Wisdom', 'प्रामाणिक ज्ञान'),
      desc: l('Expert-crafted predictions based on Brihat Parashara Hora Shastra and Lal Kitab. Detailed analysis of planetary yogas, doshas, and remedial measures.', 'बृहत् पराशर होरा शास्त्र और लाल किताब पर आधारित विशेषज्ञ-निर्मित भविष्यवाणियां। ग्रह योगों, दोषों और उपायों का विस्तृत विश्लेषण।'),
      badge: l('SCRIPTURAL', 'शास्त्रीय'),
      color: 'from-purple-500/20 to-pink-500/10',
    },
    {
      icon: <Clock className="w-6 h-6" />,
      title: l('Live Panchang', 'लाइव पंचांग'),
      subtitle: l('Location-Aware', 'लोकेशन-आधारित'),
      desc: l('Real-time Tithi, Nakshatra, Yoga, Karana with exact end times. Rahu Kaal, Choghadiya, Muhurat finder — all calculated for YOUR location, not generic tables.', 'वास्तविक समय तिथि, नक्षत्र, योग, करण सटीक समाप्ति समय के साथ। राहु काल, चौघड़िया, मुहूर्त फाइंडर — सब आपके स्थान के लिए गणना की गई, सामान्य टेबल नहीं।'),
      badge: null,
      color: 'from-green-500/20 to-emerald-500/10',
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: l('Astrologer Tools', 'ज्योतिषी टूल्स'),
      subtitle: l('Professional Grade', 'पेशेवर ग्रेड'),
      desc: l('Client management dashboard, per-client notes widget, consultation history tracking — built for professionals who manage multiple birth charts daily.', 'क्लाइंट प्रबंधन डैशबोर्ड, प्रति-क्लाइंट नोट्स विजेट, परामर्श इतिहास ट्रैकिंग — पेशेवरों के लिए बनाया गया जो रोजाना कई जन्म कुंडलियां प्रबंधित करते हैं।'),
      badge: l('PRO', 'प्रो'),
      color: 'from-rose-500/20 to-red-500/10',
    },
    {
      icon: <Globe className="w-6 h-6" />,
      title: l('True Bilingual', 'सच्चा द्विभाषी'),
      subtitle: l('Hindi + English', 'हिंदी + अंग्रेजी'),
      desc: l('Not machine-translated. Authentic Hindi astrological terminology with proper Sanskrit shlokas. Switch languages seamlessly without losing context.', 'मशीन-अनुवादित नहीं। उचित संस्कृत श्लोकों के साथ प्रामाणिक हिंदी ज्योतिषीय शब्दावली। संदर्भ खोए बिना सहजता से भाषाएं बदलें।'),
      badge: null,
      color: 'from-indigo-500/20 to-blue-500/10',
    },
  ];

  const comparisonData = [
    {
      feature: l('Chandra Chalana Protocol', 'चंद्र चालना प्रोटोकॉल'),
      us: l('Full 43-Day Moon Tracker', 'पूर्ण 43-दिवसीय चंद्र ट्रैकर'),
      them: l('Not available anywhere', 'कहीं उपलब्ध नहीं'),
      exclusive: true,
    },
    {
      feature: l('Nishaniyan Matcher', 'निशानियां मैचर'),
      us: l('Physical sign ↔ chart mapping', 'भौतिक संकेत ↔ चार्ट मैपिंग'),
      them: l('Not available anywhere', 'कहीं उपलब्ध नहीं'),
      exclusive: true,
    },
    {
      feature: l('Remedy Tracker', 'उपाय ट्रैकर'),
      us: l('Streaks + daily journal', 'स्ट्रीक्स + दैनिक जर्नल'),
      them: l('Static remedy lists only', 'केवल स्थिर सूचियां'),
      exclusive: true,
    },
    {
      feature: l('Lal Kitab Depth', 'लाल किताब गहराई'),
      us: l('22 specialized tabs', '22 विशेषज्ञता टैब'),
      them: l('Teva + basic remedies only', 'केवल तेवा + बुनियादी उपाय'),
      exclusive: false,
    },
    {
      feature: l('Astrologer Dashboard', 'ज्योतिषी डैशबोर्ड'),
      us: l('Client notes, history, per-chart tools', 'क्लाइंट नोट्स, इतिहास, प्रति-चार्ट टूल'),
      them: l('Marketplace portals only', 'केवल मार्केटप्लेस पोर्टल'),
      exclusive: false,
    },
    {
      feature: l('AI Interpretation', 'AI व्याख्या'),
      us: l('Inline Gemini + GPT for self-use', 'स्व-उपयोग के लिए इनलाइन AI'),
      them: l('Paid consultation or basic chatbot', 'भुगतान परामर्श या बुनियादी चैटबॉट'),
      exclusive: false,
    },
  ];

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.features-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
      gsap.fromTo('.feature-card', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
      gsap.fromTo('.compare-row', { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, stagger: 0.08, ease: 'power2.out', scrollTrigger: { trigger: '.compare-table', start: 'top 80%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} id="features" className="relative py-24 bg-cosmic-bg">

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Section Header */}
        <div className="features-title text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 mb-6">
            <span className="text-sm font-medium text-sacred-gold-dark uppercase tracking-wider">
              {l('Complete Astrological Operating System', 'पूर्ण ज्योतिषीय ऑपरेटिंग सिस्टम')}
            </span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans text-cosmic-text mb-6">
            {l('Everything You Need', 'आपको जो कुछ भी चाहिए')}<br />
            <span className="text-sacred-gold-dark">{l('In One Platform', 'एक ही प्लेटफॉर्म में')}</span>
          </h2>
          <p className="max-w-3xl mx-auto text-lg text-cosmic-text/80">
            {l('Most astrology apps use lookup tables and generic predictions. ', 'अधिकांश ज्योतिष ऐप लुकअप टेबल और सामान्य भविष्यवाणी का उपयोग करते हैं। ')}
            <strong className="text-sacred-gold-dark">{l('Astro Rattan computes every position from Swiss Ephemeris', 'Astro Rattan Swiss Ephemeris से हर स्थिति की गणना करता है')}</strong>
            {l(' — the same library used by research astronomers — accurate to arc-seconds.', ' — यही लाइब्रेरी शोध खगोलविद भी उपयोग करते हैं — आर्क-सेकंड तक सटीक।')}
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="feature-card group relative bg-cosmic-bg border border-sacred-gold/30 overflow-hidden hover:border-sacred-gold transition-all duration-300 hover:shadow-lg hover:shadow-sacred-gold/10"
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
              {feature.badge && (
                <div className="absolute top-4 right-4 z-10">
                  <span className="px-2 py-1 text-xs font-bold text-white bg-sacred-gold-dark rounded">
                    {feature.badge}
                  </span>
                </div>
              )}
              <CardContent className="relative p-6">
                <div className="w-12 h-12 rounded-lg bg-sacred-gold/10 flex items-center justify-center text-sacred-gold-dark mb-4 group-hover:bg-sacred-gold/20 transition-colors">
                  {feature.icon}
                </div>
                <p className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wider mb-1">
                  {feature.subtitle}
                </p>
                <h3 className="text-lg font-sans font-semibold text-cosmic-text mb-3 uppercase tracking-wide">
                  {feature.title}
                </h3>
                <p className="text-sm text-cosmic-text/70 leading-relaxed">
                  {feature.desc}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Stats Bar */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 p-6 rounded-2xl bg-sacred-gold/5 border border-sacred-gold/20">
          <div className="text-center">
            <div className="text-3xl font-bold text-sacred-gold-dark">22</div>
            <div className="text-sm text-cosmic-text/70">{l('Lal Kitab Tabs', 'लाल किताब टैब्स')}</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-sacred-gold-dark">21</div>
            <div className="text-sm text-cosmic-text/70">{l('Kundli Engines', 'कुंडली इंजन')}</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-sacred-gold-dark">43</div>
            <div className="text-sm text-cosmic-text/70">{l('Day Protocol', 'दिवसीय प्रोटोकॉल')}</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-sacred-gold-dark">3</div>
            <div className="text-sm text-cosmic-text/70">{l('Scriptural Systems', 'शास्त्रीय प्रणालियां')}</div>
          </div>
        </div>

        {/* Comparison Table */}
        <div className="compare-table max-w-4xl mx-auto mt-24">
          <h3 className="text-2xl sm:text-3xl font-sans text-center text-cosmic-text mb-4">
            {l('Astro Rattan vs Others', 'एस्ट्रो रतन बनाम अन्य')}
          </h3>
          <p className="text-center text-cosmic-text/60 mb-10">
            {l('See exactly what sets us apart', 'देखें हम क्या अलग देते हैं')}
          </p>

          <div className="bg-cosmic-bg/80 rounded-2xl border border-sacred-gold/20 overflow-hidden">
            {/* Table Header */}
            <div className="grid grid-cols-3 gap-4 p-4 bg-sacred-gold/10 border-b border-sacred-gold/20">
              <div className="text-sm font-semibold text-cosmic-text/70 uppercase tracking-wider">
                {l('Feature', 'सुविधा')}
              </div>
              <div className="text-center">
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold-dark text-sm font-semibold">
                  <Sparkles className="w-3 h-3" /> Astro Rattan
                </span>
              </div>
              <div className="text-center text-sm font-semibold text-cosmic-text/50">
                {l('Other Apps', 'अन्य ऐप्स')}
              </div>
            </div>

            {/* Table Rows */}
            {comparisonData.map((row, index) => (
              <div
                key={index}
                className={`compare-row grid grid-cols-3 gap-4 p-4 items-center ${
                  index !== comparisonData.length - 1 ? 'border-b border-sacred-gold/10' : ''
                } ${row.exclusive ? 'bg-sacred-gold/5' : ''}`}
              >
                <div className="text-sm text-cosmic-text font-medium flex items-center gap-2">
                  {row.feature}
                  {row.exclusive && (
                    <span className="hidden sm:inline px-1.5 py-0.5 text-[10px] font-bold text-sacred-gold-dark border border-sacred-gold/40 rounded uppercase tracking-wide">
                      {l('Only us', 'सिर्फ हम')}
                    </span>
                  )}
                </div>
                <div className="flex items-center justify-center gap-2">
                  <Check className="w-4 h-4 text-green-500 flex-shrink-0" />
                  <span className="text-sm text-cosmic-text text-center">{row.us}</span>
                </div>
                <div className="flex items-center justify-center gap-2">
                  <X className="w-4 h-4 text-red-400 flex-shrink-0" />
                  <span className="text-sm text-cosmic-text/50 text-center">{row.them}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── See What's Inside — Screenshot Showcase ─────────────── */}
        <div className="mt-24">
          <h3 className="text-2xl sm:text-3xl font-sans text-center text-cosmic-text mb-3">
            {l("See What's Inside", 'अंदर क्या है देखें')}
          </h3>
          <p className="text-center text-cosmic-text/60 mb-10 text-sm">
            {l('Real screens from the platform', 'प्लेटफॉर्म की वास्तविक स्क्रीन')}
          </p>

          <div className="rounded-2xl p-6 sm:p-8" style={{ background: '#FAF7F2' }}>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {[
                { label: l('Kundli Engine', 'कुंडली इंजन'),           file: 'showcase-kundli.png'     },
                { label: l('Lal Kitab Workspace', 'लाल किताब वर्कस्पेस'), file: 'showcase-lalkitab.png'  },
                { label: l('Live Panchang', 'लाइव पंचांग'),            file: 'showcase-panchang.png'   },
                { label: l('Numerology Grid', 'न्यूमेरोलॉजी ग्रिड'),   file: 'showcase-numerology.png' },
                { label: l('Client Manager', 'क्लाइंट मैनेजर'),        file: 'showcase-clients.png'    },
                { label: l('Chandra Chalana', 'चंद्र चालना'),          file: 'showcase-chandra.png'    },
              ].map(({ label, file }) => (
                <div
                  key={file}
                  className="group overflow-hidden rounded-xl"
                  style={{ border: '1px solid #e0d5c5' }}
                >
                  <div className="overflow-hidden" style={{ height: '220px' }}>
                    <img
                      src={`/images/showcase/${file}`}
                      alt={label}
                      className="w-full h-full object-cover object-top group-hover:scale-[1.02] transition-transform duration-300"
                      loading="lazy"
                    />
                  </div>
                  <div className="px-4 py-3" style={{ background: '#FAF7F2', borderTop: '1px solid #e0d5c5' }}>
                    <p className="text-sm font-semibold text-center uppercase tracking-wider" style={{ color: '#C4611F' }}>
                      {label}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
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
              {l('Get Started Free', 'मुफ्त शुरू करें')}
              <Sparkles className="w-4 h-4" />
            </a>
            <a
              href="/kundli"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border-2 border-sacred-gold/50 text-sacred-gold-dark rounded-lg font-semibold hover:bg-sacred-gold/10 transition-all"
            >
              {l('Try Demo Chart', 'डेमो चार्ट देखें')}
            </a>
          </div>
        </div>

      </div>
    </section>
  );
}
