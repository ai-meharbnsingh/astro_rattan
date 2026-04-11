import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { useTranslation } from '@/lib/i18n';
import { Star, Clock, BookOpen, Shield, Calendar, Calculator, Zap, Globe, Users } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
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
      icon: <Zap className="w-6 h-6" />,
      title: l('AI-Powered Insights', 'AI-संचालित अंतर्दृष्टि'),
      subtitle: l('Gemini + OpenAI', 'जेमिनी + ओपनएआई'),
      desc: l('Not lookup tables — real AI interpretation of your chart. Ask questions, get Gita wisdom, receive personalized remedy suggestions based on your unique placements.', 'लुकअप टेबल नहीं — आपके चार्ट की वास्तविक AI व्याख्या। प्रश्न पूछें, गीता ज्ञान प्राप्त करें, अपनी अद्वितीय स्थितियों के आधार पर व्यक्तिगत उपाय सुझाव प्राप्त करें।'),
      badge: l('SMART', 'स्मार्ट'),
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

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.features-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
      gsap.fromTo('.feature-card', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} id="features" className="relative pt-4 pb-24 bg-cosmic-bg">

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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
          <div className="max-w-3xl mx-auto space-y-4 text-cosmic-text">
            <p className="text-lg">
              {l('Most astrology apps use lookup tables and generic predictions. ', 'अधिकांश ज्योतिष ऐप लुकअप टेबल और सामान्य भविष्यवाणी का उपयोग करते हैं। ')}
              <strong className="text-sacred-gold-dark">{l('Astro Rattan computes every position from Swiss Ephemeris', 'Astro Rattan Swiss Ephemeris से हर स्थिति की गणना करता है')}</strong>
              {l(' — the same library used by research astronomers — accurate to arc-seconds.', ' — यही लाइब्रेरी शोध खगोलविद भी उपयोग करते हैं — आर्क-सेकंड तक सटीक।')}
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card
              key={index}
              className={`feature-card group relative bg-cosmic-bg border border-sacred-gold/30 overflow-hidden hover:border-sacred-gold transition-all duration-300 hover:shadow-lg hover:shadow-sacred-gold/10`}
            >
              {/* Gradient background */}
              <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
              
              {/* Badge */}
              {feature.badge && (
                <div className="absolute top-4 right-4 z-10">
                  <span className="px-2 py-1 text-xs font-bold text-white bg-sacred-gold-dark rounded">
                    {feature.badge}
                  </span>
                </div>
              )}
              
              <CardContent className="relative p-6">
                {/* Icon */}
                <div className="w-12 h-12 rounded-lg bg-sacred-gold/10 flex items-center justify-center text-sacred-gold-dark mb-4 group-hover:bg-sacred-gold/20 transition-colors">
                  {feature.icon}
                </div>
                
                {/* Subtitle */}
                <p className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wider mb-1">
                  {feature.subtitle}
                </p>
                
                {/* Title */}
                <h3 className="text-lg font-sans font-semibold text-cosmic-text mb-3 uppercase tracking-wide">
                  {feature.title}
                </h3>
                
                {/* Description */}
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
            <div className="text-3xl font-bold text-sacred-gold-dark">2</div>
            <div className="text-sm text-cosmic-text/70">{l('AI Providers', 'AI प्रोवाइडर्स')}</div>
          </div>
        </div>
      </div>

    </section>
  );
}


