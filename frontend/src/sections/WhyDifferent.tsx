import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Check, X, Sparkles, Moon, Scroll, Users, BookOpen, Award } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

export default function WhyDifferent() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  const uniqueFeatures = [
    {
      icon: <Scroll className="w-6 h-6" />,
      title: l('22 Lal Kitab Specializations', '22 लाल किताब विशेषज्ञताएं'),
      desc: l('Nishaniyan Matcher, Chandra Chalana Protocol, Remedy Tracker with streaks, Teva classification — features you won\'t find in any other app.', 'निशानियां मैचर, चंद्र चालना प्रोटोकॉल, स्ट्रीक्स के साथ उपाय ट्रैकर, तेवा वर्गीकरण — ये सुविधाएं किसी अन्य ऐप में नहीं मिलेंगी।'),
      highlight: true,
    },
    {
      icon: <Moon className="w-6 h-6" />,
      title: l('43-Day Chandra Chalana Protocol', '43-दिवसीय चंद्र चालना प्रोटोकॉल'),
      desc: l('The only app with a complete Moon discipline tracker with daily tasks, journal entries, and progress persistence across devices.', 'इकलौता ऐप जिसमें दैनिक कार्यों, जर्नल एंट्रीज़ और क्रॉस-डिवाइस प्रगति के साथ पूर्ण चंद्र अनुशासन ट्रैकर है।'),
      highlight: true,
    },
    {
      icon: <Brain className="w-6 h-6" />,
      title: l('AI + Vedic Intelligence', 'AI + वैदिक बुद्धि'),
      desc: l('Gemini & OpenAI powered chart interpretation, Gita wisdom answers, and intelligent remedy suggestions — not just lookup tables.', 'जेमिनी और ओपनएआई से चार्ट व्याख्या, गीता ज्ञान उत्तर, और बुद्धिमान उपाय सुझाव — केवल लुकअप टेबल नहीं।'),
      highlight: false,
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: l('Astrologer Client Management', 'ज्योतिषी क्लाइंट प्रबंधन'),
      desc: l('Built-in tools for professional astrologers to manage multiple clients, add notes, and track consultation history.', 'पेशेवर ज्योतिषियों के लिए बहु-क्लाइंट प्रबंधन, नोट्स जोड़ने और परामर्श इतिहास ट्रैक करने के लिए अंतर्निहित टूल।'),
      highlight: false,
    },
    {
      icon: <Award className="w-6 h-6" />,
      title: l('Complete Bilingual Experience', 'पूर्ण द्विभाषी अनुभव'),
      desc: l('Not just translated UI — proper Hindi astrological terminology with authentic Sanskrit shlokas and regional accuracy.', 'केवल अनुवादित UI नहीं — प्रामाणिक संस्कृत श्लोकों और क्षेत्रीय सटीकता के साथ उचित हिंदी ज्योतिषीय शब्दावली।'),
      highlight: true,
    },
    {
      icon: <Sparkles className="w-6 h-6" />,
      title: l('Nishaniyan Matcher', 'निशानियां मैचर'),
      desc: l('Match real-life physical signs (moles, marks, lines) with your birth chart — a unique Lal Kitab diagnostic tool.', 'अपनी जन्म कुंडली के साथ वास्तविक जीवन भौतिक संकेतों (तिल, निशान, रेखाएं) का मिलान करें — एक अद्वितीय लाल किताब नैदानिक उपकरण।'),
      highlight: true,
    },
  ];

  const comparisonData = [
    { feature: l('Lal Kitab System', 'लाल किताब सिस्टम'), us: '22 Specialization Tabs', them: 'Basic Remedies Only' },
    { feature: l('Chandra Chalana Protocol', 'चंद्र चालना प्रोटोकॉल'), us: 'Full 43-Day Tracker', them: 'Not Available' },
    { feature: l('Nishaniyan Matcher', 'निशानियां मैचर'), us: 'Physical Sign Mapping', them: 'Not Available' },
    { feature: l('Remedy Tracker', 'उपाय ट्रैकर'), us: 'With Streaks & Journal', them: 'Static Lists Only' },
    { feature: l('Interpretation Depth', 'व्याख्या गहराई'), us: 'Classical Text-Based', them: 'Generic Templates' },
    { feature: l('Client Management', 'क्लाइंट प्रबंधन'), us: 'Built-in Dashboard', them: 'Not Available' },
    { feature: l('Divisional Charts', 'विभाजन चार्ट'), us: 'D1-D60 Complete', them: 'D9 Only' },
    { feature: l('Calculation Engine', 'गणना इंजन'), us: 'Swiss Ephemeris', them: 'Lookup Tables' },
  ];

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.why-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
      gsap.fromTo('.why-card', { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: '.why-grid', start: 'top 75%' } });
      gsap.fromTo('.compare-row', { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, stagger: 0.08, ease: 'power2.out', scrollTrigger: { trigger: '.compare-table', start: 'top 80%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative py-24 bg-gradient-to-b from-cosmic-bg via-cosmic-bg to-[#1a1510]">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-sacred-gold/5 rounded-full blur-3xl" />
        <div className="absolute bottom-40 right-10 w-96 h-96 bg-[#8B4513]/10 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="why-title text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 mb-6">
            <Sparkles className="w-4 h-4 text-sacred-gold-dark" />
            <span className="text-sm font-medium text-sacred-gold-dark uppercase tracking-wider">
              {l('What Makes Us Different', 'हमें क्या अलग बनाता है')}
            </span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans text-cosmic-text mb-6">
            {l('Features You Won\'t Find ', 'वे सुविधाएं जो आपको ')}<br />
            <span className="text-sacred-gold-dark">{l('Anywhere Else', 'कहीं और नहीं मिलेंगी')}</span>
          </h2>
          <p className="max-w-2xl mx-auto text-lg text-cosmic-text/80">
            {l('While others give you generic predictions from lookup tables, we built a complete astrological operating system.', 'जबकि अन्य लुकअप टेबल से सामान्य भविष्यवाणियां देते हैं, हमने एक पूर्ण ज्योतिषीय ऑपरेटिंग सिस्टम बनाया है।')}
          </p>
        </div>

        {/* Unique Features Grid */}
        <div className="why-grid grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
          {uniqueFeatures.map((item, index) => (
            <div
              key={index}
              className={`why-card group relative p-6 rounded-xl border transition-all duration-300 hover:scale-[1.02] ${
                item.highlight
                  ? 'bg-gradient-to-br from-sacred-gold/10 to-transparent border-sacred-gold/50 hover:border-sacred-gold'
                  : 'bg-cosmic-bg/50 border-sacred-gold/20 hover:border-sacred-gold/40'
              }`}
            >
              {item.highlight && (
                <div className="absolute -top-3 -right-3">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-sacred-gold text-white text-xs font-bold">
                    ★
                  </span>
                </div>
              )}
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-4 ${
                item.highlight ? 'bg-sacred-gold/20 text-sacred-gold-dark' : 'bg-sacred-gold/10 text-sacred-gold-dark'
              }`}>
                {item.icon}
              </div>
              <h3 className="text-lg font-sans font-semibold text-cosmic-text mb-2">
                {item.title}
              </h3>
              <p className="text-sm text-cosmic-text/70 leading-relaxed">
                {item.desc}
              </p>
            </div>
          ))}
        </div>

        {/* Comparison Table */}
        <div className="compare-table max-w-4xl mx-auto">
          <h3 className="text-2xl font-sans text-center text-cosmic-text mb-8">
            {l('Astro Rattan vs Others', 'एस्ट्रो रतन बनाम अन्य')}
          </h3>
          
          <div className="bg-cosmic-bg/80 rounded-2xl border border-sacred-gold/20 overflow-hidden">
            {/* Header */}
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
            
            {/* Rows */}
            {comparisonData.map((row, index) => (
              <div 
                key={index} 
                className={`compare-row grid grid-cols-3 gap-4 p-4 items-center ${
                  index !== comparisonData.length - 1 ? 'border-b border-sacred-gold/10' : ''
                }`}
              >
                <div className="text-sm text-cosmic-text font-medium">{row.feature}</div>
                <div className="flex items-center justify-center gap-2">
                  <Check className="w-4 h-4 text-green-500 flex-shrink-0" />
                  <span className="text-sm text-cosmic-text text-center">{l(row.us, row.us)}</span>
                </div>
                <div className="flex items-center justify-center gap-2">
                  <X className="w-4 h-4 text-red-400 flex-shrink-0" />
                  <span className="text-sm text-cosmic-text/50 text-center">{l(row.them, row.them)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom CTA */}
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
