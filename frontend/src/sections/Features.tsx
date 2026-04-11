import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { useTranslation } from '@/lib/i18n';

gsap.registerPlugin(ScrollTrigger);

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  const features = [
    {
      title: l('21 Kundli Engines', '21 कुंडली इंजन'),
      desc: l('Parashari + Jaimini + KP System. Divisional charts (D1-D60), Shadbala, Ashtakvarga, Yogini Dasha — depth no app matches.', 'पाराशरी + जैमिनी + केपी सिस्टम। विभाजन चार्ट (D1-D60), शडबल, अष्टकवर्ग, योगिनी दशा — ऐसी गहराई बहुत कम ऐप में मिलती है।'),
      img: 'https://images.unsplash.com/photo-1630694093867-4b947d812bf0?w=600&h=400&fit=crop&q=90',
    },
    {
      title: l('Live Panchang', 'लाइव पंचांग'),
      desc: l('Tithi, Nakshatra, Yoga, Karana with exact end times. Rahu Kaal, Choghadiya, Muhurat finder — location-aware.', 'तिथि, नक्षत्र, योग, करण के सटीक समाप्ति समय के साथ। राहु काल, चौघड़िया, मुहूर्त फाइंडर — लोकेशन आधारित।'),
      img: 'https://images.unsplash.com/photo-1545156521-77bd85671d30?w=600&h=400&fit=crop&q=90',
    },
    {
      title: l('Lal Kitab Remedies', 'लाल किताब उपाय'),
      desc: l('Full Lal Kitab system with personalized remedies, house analysis, and annual predictions — rarely found in apps.', 'व्यक्तिगत उपाय, भाव विश्लेषण और वार्षिक भविष्यवाणी के साथ पूर्ण लाल किताब सिस्टम — ऐप्स में दुर्लभ।'),
      img: 'https://images.unsplash.com/photo-1604881991720-f91add269bed?w=600&h=400&fit=crop&q=90',
    },
    {
      title: l('Dosha + Yoga Detection', 'दोष + योग पहचान'),
      desc: l('Mangal, Kaal Sarp, Sade Sati, Pitra, Kemdrum Dosha. Plus Gajakesari, Budhaditya, Panch Mahapurusha Yogas.', 'मंगल, कालसर्प, साढ़ेसाती, पितृ, केमद्रुम दोष। साथ में गजकेसरी, बुधादित्य, पंच महापुरुष योग।'),
      img: 'https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=600&h=400&fit=crop&q=90',
    },
    {
      title: l('Varshphal + Transits', 'वर्षफल + गोचर'),
      desc: l('Solar Return with Muntha & Mudda Dasha. Live Gochara transit tracking from your natal Moon.', 'मुन्था और मुद्दा दशा के साथ सोलर रिटर्न। जन्म चंद्र से लाइव गोचर ट्रैकिंग।'),
      img: 'https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=600&h=400&fit=crop&q=90',
    },
    {
      title: l('Numerology + Loshu Grid', 'अंकशास्त्र + लोशु ग्रिड'),
      desc: l('Life Path, Destiny, Soul Urge numbers. Mobile number analysis with Vedic Grid and compatibility.', 'लाइफ पाथ, डेस्टिनी, सोल अर्ज नंबर। वैदिक ग्रिड और संगतता के साथ मोबाइल नंबर विश्लेषण।'),
      img: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&h=400&fit=crop&q=90',
    },
  ];

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return; // reduced motion
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
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans text-cosmic-text mb-6">
            {l('Bridging Ancient Wisdom with Modern Technology', 'प्राचीन ज्ञान और आधुनिक तकनीक का संगम')}
          </h2>
          <div className="max-w-3xl mx-auto space-y-4 text-cosmic-text">
            <p>
              {l('Most astrology apps use lookup tables and generic predictions. Astro Rattan computes every position from Swiss Ephemeris — the same library used by research astronomers — accurate to arc-seconds.', 'अधिकांश ज्योतिष ऐप लुकअप टेबल और सामान्य भविष्यवाणी देते हैं। Astro Rattan Swiss Ephemeris से हर स्थिति की गणना करता है — यही लाइब्रेरी शोध खगोलविद भी उपयोग करते हैं — आर्क-सेकंड तक सटीक।')}
            </p>
            <p>
              {l('Three complete astrological systems in one app:', 'एक ही ऐप में तीन पूर्ण ज्योतिष प्रणालियां:')} <strong className="text-sacred-gold-dark">{l('Parashari', 'पाराशरी')}</strong> {l('(classical Vedic),', '(शास्त्रीय वैदिक),')} <strong className="text-sacred-gold-dark">{l('Jaimini', 'जैमिनी')}</strong> {l('(Chara Karakas, special lagnas), and', '(चर कारक, विशेष लग्न), और')} <strong className="text-sacred-gold-dark">{l('KP System', 'केपी सिस्टम')}</strong> {l('(Krishnamurti Paddhati with sub-lord analysis). Plus full', '(कृष्णमूर्ति पद्धति और सब-लॉर्ड विश्लेषण)। साथ में पूर्ण')} <strong className="text-sacred-gold-dark">{l('Lal Kitab', 'लाल किताब')}</strong> {l('remedies and', 'उपाय और')} <strong className="text-sacred-gold-dark">{l('Numerology', 'अंकशास्त्र')}</strong>.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="feature-card group relative bg-cosmic-bg border border-sacred-gold overflow-hidden"
            >
              <div className="h-40 overflow-hidden">
                <img
                  src={feature.img}
                  alt={feature.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  loading="lazy"
                />
                <div className="absolute inset-0 h-40 bg-gradient-to-t from-cosmic-bg via-cosmic-bg to-transparent" />
              </div>
              <CardContent className="relative p-6 pt-2">
                <h3 className="text-lg font-sans font-semibold text-cosmic-text mb-2 uppercase tracking-wide">
                  {feature.title}
                </h3>
                <p className="text-base text-cosmic-text leading-relaxed">{feature.desc}</p>
              </CardContent>
            </Card>
          ))}
        </div>

      </div>

    </section>
  );
}
