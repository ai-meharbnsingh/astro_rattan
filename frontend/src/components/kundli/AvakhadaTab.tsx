import { Loader2 } from 'lucide-react';
import { translatePlanet, translateSign, translateNakshatra } from '@/lib/backend-translations';

interface AvakhadaTabProps {
  avakhadaData: any;
  loadingAvakhada: boolean;
  language: string;
  t: (key: string) => string;
}

// Translation helpers for Avakhada values
const AVAKHADA_TRANSLATIONS: Record<string, Record<string, string>> = {
  hi: {
    // Gana
    'Deva': 'देव',
    'Manushya': 'मनुष्य',
    'Rakshasa': 'राक्षस',
    // Nadi
    'Aadi': 'आदि',
    'Madhya': 'मध्य',
    'Antya': 'अंत्य',
    // Varna
    'Brahmin': 'ब्राह्मण',
    'Kshatriya': 'क्षत्रिय',
    'Vaishya': 'वैश्य',
    'Shudra': 'शूद्र',
    // Yoni
    'Horse': 'अश्व',
    'Elephant': 'हाथी',
    'Goat': 'बकरी',
    'Serpent': 'सर्प',
    'Dog': 'कुत्ता',
    'Cat': 'बिल्ली',
    'Rat': 'चूहा',
    'Cow': 'गाय',
    'Buffalo': 'भैंस',
    'Tiger': 'बाघ',
    'Deer': 'हिरण',
    'Monkey': 'बंदर',
    'Mongoose': 'नेवला',
    'Lion': 'सिंह',
    // Paya
    'Gold': 'स्वर्ण',
    'Silver': 'रजत',
    'Copper': 'ताम्र',
    'Iron': 'लोहा',
    // Tithi Paksha
    'Shukla': 'शुक्ल',
    'Krishna': 'कृष्ण',
  }
};

function translateAvakhadaValue(value: string | undefined, lang: string): string {
  if (!value || lang === 'en') return value || '';
  const translations = AVAKHADA_TRANSLATIONS[lang];
  if (!translations) return value;
  
  // Check for exact match first
  if (translations[value]) return translations[value];
  
  // Try to translate parts (e.g., "Deer (Mrig)" -> "हिरण (मृग)")
  let result = value;
  for (const [en, hi] of Object.entries(translations)) {
    result = result.replace(new RegExp(`\\b${en}\\b`, 'g'), hi);
  }
  return result;
}

export default function AvakhadaTab({ avakhadaData, loadingAvakhada, language, t }: AvakhadaTabProps) {
  if (loadingAvakhada) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-cosmic-text">{t('kundli.calculatingAvakhada')}</span>
      </div>
    );
  }

  if (!avakhadaData) {
    return <p className="text-center text-cosmic-text py-8">{t('kundli.clickAvakhadaTab')}</p>;
  }

  return (
    <div className="space-y-4">
      <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold rounded-xl p-4 border border-sacred-gold mb-4">
        <h4 className="font-display font-bold text-lg" style={{ color: 'var(--ink)' }}>{t('section.avakhadaChakra')}</h4>
        <p className="text-sm text-cosmic-text">{t('avakhada.birthSummary')}</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {[
          { label: t('avakhada.ascendant'), value: translateSign(avakhadaData.ascendant, language) },
          { label: t('avakhada.ascendantLord'), value: translatePlanet(avakhadaData.ascendant_lord, language) },
          { label: t('avakhada.rashi'), value: translateSign(avakhadaData.rashi, language) },
          { label: t('avakhada.rashiLord'), value: translatePlanet(avakhadaData.rashi_lord, language) },
          { label: t('avakhada.nakshatra'), value: `${translateNakshatra(avakhadaData.nakshatra, language)} (${t('kundli.pada')} ${avakhadaData.nakshatra_pada})` },
          { label: t('avakhada.yoga'), value: avakhadaData.yoga },
          { label: t('avakhada.karana'), value: avakhadaData.karana },
          { label: t('avakhada.yoni'), value: translateAvakhadaValue(avakhadaData.yoni, language) },
          { label: t('avakhada.gana'), value: translateAvakhadaValue(avakhadaData.gana, language) },
          { label: t('avakhada.nadi'), value: translateAvakhadaValue(avakhadaData.nadi, language) },
          { label: t('avakhada.varna'), value: translateAvakhadaValue(avakhadaData.varna, language) },
          { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
          { label: t('avakhada.sunSign'), value: translateSign(avakhadaData.sun_sign, language) },
          { label: t('avakhada.tithi'), value: avakhadaData.tithi ? `${avakhadaData.tithi} (${translateAvakhadaValue(avakhadaData.tithi_paksha, language)})` : undefined },
          { label: t('avakhada.tithiLord'), value: translatePlanet(avakhadaData.tithi_lord, language) },
          { label: t('avakhada.vaar'), value: avakhadaData.vaar ? `${avakhadaData.vaar} (${translatePlanet(avakhadaData.vaar_lord, language)})` : undefined },
          { label: t('avakhada.payaNakshatra'), value: translateAvakhadaValue(avakhadaData.paya_nakshatra, language) },
          { label: t('avakhada.payaChandra'), value: translateAvakhadaValue(avakhadaData.paya_chandra, language) },
        ].filter(item => item.value).map((item) => (
          <div
            key={item.label}
            className="rounded-xl p-4 border"
            style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}
          >
            <p className="text-sm font-medium mb-1" style={{ color: 'var(--ink-light)' }}>{item.label}</p>
            <p className="font-display font-semibold text-base" style={{ color: 'var(--ink)' }}>{item.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
