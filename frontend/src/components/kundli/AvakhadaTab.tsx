import { Loader2 } from 'lucide-react';
import { translatePlanet, translateSign, translateNakshatra } from '@/lib/backend-translations';

interface AvakhadaTabProps {
  avakhadaData: any;
  loadingAvakhada: boolean;
  language: string;
  t: (key: string) => string;
}

const AVAKHADA_TRANSLATIONS: Record<string, Record<string, string>> = {
  hi: {
    'Deva': 'देव', 'Manushya': 'मनुष्य', 'Rakshasa': 'राक्षस',
    'Aadi': 'आदि', 'Madhya': 'मध्य', 'Antya': 'अंत्य',
    'Brahmin': 'ब्राह्मण', 'Kshatriya': 'क्षत्रिय', 'Vaishya': 'वैश्य', 'Shudra': 'शूद्र',
    'Horse': 'अश्व', 'Elephant': 'हाथी', 'Goat': 'बकरी', 'Serpent': 'सर्प',
    'Dog': 'कुत्ता', 'Cat': 'बिल्ली', 'Rat': 'चूहा', 'Cow': 'गाय',
    'Buffalo': 'भैंस', 'Tiger': 'बाघ', 'Deer': 'हिरण', 'Monkey': 'बंदर',
    'Mongoose': 'नेवला', 'Lion': 'सिंह',
    'Gold': 'स्वर्ण', 'Silver': 'रजत', 'Copper': 'ताम्र', 'Iron': 'लोहा',
    'Shukla': 'शुक्ल', 'Krishna': 'कृष्ण',
  }
};

const NAKSHATRA_SYLLABLES: Record<string, string[]> = {
  'Ashwini': ['Chu', 'Che', 'Cho', 'La'], 'Bharani': ['Li', 'Lu', 'Le', 'Lo'],
  'Krittika': ['A', 'I', 'U', 'E'], 'Rohini': ['O', 'Va', 'Vi', 'Vu'],
  'Mrigashira': ['Ve', 'Vo', 'Ka', 'Ki'], 'Ardra': ['Ku', 'Gha', 'Ing', 'Jha'],
  'Punarvasu': ['Ke', 'Ko', 'Ha', 'Hi'], 'Pushya': ['Hu', 'He', 'Ho', 'Da'],
  'Ashlesha': ['Di', 'Du', 'De', 'Do'], 'Magha': ['Ma', 'Mi', 'Mu', 'Me'],
  'Purva Phalguni': ['Mo', 'Ta', 'Ti', 'Tu'], 'Uttara Phalguni': ['Te', 'To', 'Pa', 'Pi'],
  'Hasta': ['Pu', 'Sha', 'Na', 'Tha'], 'Chitra': ['Pe', 'Po', 'Ra', 'Ri'],
  'Swati': ['Ru', 'Re', 'Ro', 'Ta'], 'Vishakha': ['Ti', 'Tu', 'Te', 'To'],
  'Anuradha': ['Na', 'Ni', 'Nu', 'Ne'], 'Jyeshtha': ['No', 'Ya', 'Yi', 'Yu'],
  'Mula': ['Ye', 'Yo', 'Bha', 'Bhi'], 'Purva Ashadha': ['Bhu', 'Dha', 'Pha', 'Dha'],
  'Uttara Ashadha': ['Be', 'Bo', 'Ja', 'Ji'], 'Shravana': ['Ju', 'Je', 'Jo', 'Sha'],
  'Dhanishtha': ['Ga', 'Gi', 'Gu', 'Ge'], 'Shatabhisha': ['Go', 'Sa', 'Si', 'Su'],
  'Purva Bhadrapada': ['Se', 'So', 'Da', 'Di'], 'Uttara Bhadrapada': ['Du', 'Tha', 'Jha', 'Ana'],
  'Revati': ['De', 'Do', 'Cha', 'Chi'],
};

function translateAvakhadaValue(value: string | undefined, lang: string): string {
  if (!value || lang === 'en') return value || '';
  const translations = AVAKHADA_TRANSLATIONS[lang];
  if (!translations) return value;
  if (translations[value]) return translations[value];
  let result = value;
  for (const [en, hi] of Object.entries(translations)) {
    result = result.replace(new RegExp(`\\b${en}\\b`, 'g'), hi);
  }
  return result;
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';

export default function AvakhadaTab({ avakhadaData, loadingAvakhada, language, t }: AvakhadaTabProps) {
  const isHi = language === 'hi';

  if (loadingAvakhada) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.calculatingAvakhada')}</span>
      </div>
    );
  }

  if (!avakhadaData) {
    return <p className="text-center text-foreground py-8">{t('kundli.clickAvakhadaTab')}</p>;
  }

  const rows = [
    { label: t('avakhada.ascendant'), value: translateSign(avakhadaData.ascendant, language) },
    { label: t('avakhada.ascendantLord'), value: translatePlanet(avakhadaData.ascendant_lord, language) },
    { label: t('avakhada.rashi'), value: translateSign(avakhadaData.rashi, language) },
    { label: t('avakhada.rashiLord'), value: translatePlanet(avakhadaData.rashi_lord, language) },
    { label: t('avakhada.nakshatra'), value: `${translateNakshatra(avakhadaData.nakshatra, language)} (${t('kundli.pada')} ${avakhadaData.nakshatra_pada})` },
    { label: t('avakhada.yoga'), value: translateAvakhadaValue(avakhadaData.yoga, language) },
    { label: t('avakhada.karana'), value: translateAvakhadaValue(avakhadaData.karana, language) },
    { label: t('avakhada.yoni'), value: translateAvakhadaValue(avakhadaData.yoni, language) },
    { label: t('avakhada.gana'), value: translateAvakhadaValue(avakhadaData.gana, language) },
    { label: t('avakhada.nadi'), value: translateAvakhadaValue(avakhadaData.nadi, language) },
    { label: t('avakhada.varna'), value: translateAvakhadaValue(avakhadaData.varna, language) },
    { label: t('avakhada.sunSign'), value: translateSign(avakhadaData.sun_sign, language) },
    { label: t('avakhada.tithi'), value: avakhadaData.tithi ? `${translateAvakhadaValue(avakhadaData.tithi, language)} (${translateAvakhadaValue(avakhadaData.tithi_paksha, language)})` : undefined },
    { label: t('avakhada.tithiLord'), value: translatePlanet(avakhadaData.tithi_lord, language) },
    { label: t('avakhada.vaar'), value: avakhadaData.vaar ? `${translateAvakhadaValue(avakhadaData.vaar, language)} (${translatePlanet(avakhadaData.vaar_lord, language)})` : undefined },
    { label: t('avakhada.payaNakshatra'), value: translateAvakhadaValue(avakhadaData.paya_nakshatra, language) },
    { label: t('avakhada.payaChandra'), value: translateAvakhadaValue(avakhadaData.paya_chandra, language) },
  ].filter(item => item.value);

  const nakshatra = avakhadaData.nakshatra || '';
  const pada = avakhadaData.nakshatra_pada || 1;
  const syllables = NAKSHATRA_SYLLABLES[nakshatra] || (avakhadaData.naamakshar ? [avakhadaData.naamakshar] : []);

  return (
    <div className="space-y-4">
      {/* Avakhada Chakra main grid */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <span>{isHi ? 'अवखड़ा चक्र' : t('section.avakhadaChakra')}</span>
        </div>
        <div className="p-4">
          <p className="text-xs text-muted-foreground mb-4">{t('avakhada.birthSummary')}</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {rows.map((item) => (
              <div
                key={item.label}
                className="rounded-lg p-3 border"
                style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}
              >
                <p className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-1">{item.label}</p>
                <p className="font-semibold text-sm text-foreground">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Naamakshar syllable picker */}
      {syllables.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <span>{isHi ? 'नामाक्षर' : t('avakhada.naamakshar')}</span>
          </div>
          <div className="p-4">
            <div className="flex flex-wrap gap-2">
              {syllables.map((s, idx) => (
                <span
                  key={s}
                  className={`px-3 py-1 rounded-full text-sm font-semibold border transition-colors ${
                    idx + 1 === pada
                      ? 'bg-sacred-gold-dark text-white border-sacred-gold-dark shadow-sm'
                      : 'bg-muted/10 text-foreground border-border/30'
                  }`}
                  title={idx + 1 === pada ? t('auto.yourPada') : t('auto.padaIdx1')}
                >
                  {s}
                  {idx + 1 === pada && <span className="ml-1 text-xs opacity-80">★</span>}
                </span>
              ))}
            </div>
            {syllables.length > 1 && (
              <p className="text-xs text-muted-foreground mt-2">{t('auto.PadaPadaRecommendedF')}</p>
            )}
          </div>
        </div>
      )}

      {/* Lucky & Conflict Indicators */}
      {(avakhadaData.lucky_number || avakhadaData.good_planets?.length > 0 || avakhadaData.conflict_planets?.length > 0) && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <span>{isHi ? 'शुभ एवं अशुभ संकेतक' : 'Lucky & Conflict Indicators'}</span>
          </div>
          <div className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-3">
            {avakhadaData.lucky_number != null && (
              <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
                <p className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-1">{isHi ? 'शुभ अंक' : 'Lucky Number'}</p>
                <p className="font-semibold text-sm text-foreground">{avakhadaData.lucky_number}</p>
              </div>
            )}
            {avakhadaData.lucky_metal && (
              <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
                <p className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-1">{isHi ? 'शुभ धातु' : 'Lucky Metal'}</p>
                <p className="font-semibold text-sm text-foreground">{avakhadaData.lucky_metal}</p>
              </div>
            )}
            {avakhadaData.good_planets?.length > 0 && (
              <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
                <p className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">{isHi ? 'अनुकूल ग्रह' : 'Favourable Planets'}</p>
                <div className="flex flex-wrap gap-2">
                  {avakhadaData.good_planets.map((p: string) => (
                    <span key={p} className="px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">{translatePlanet(p, language)}</span>
                  ))}
                </div>
              </div>
            )}
            {avakhadaData.conflict_planets?.length > 0 && (
              <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
                <p className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">{isHi ? 'अशुभ ग्रह' : 'Conflict Planets'}</p>
                <div className="flex flex-wrap gap-2">
                  {avakhadaData.conflict_planets.map((p: string) => (
                    <span key={p} className="px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">{translatePlanet(p, language)}</span>
                  ))}
                </div>
              </div>
            )}
            {avakhadaData.lucky_days?.length > 0 && (
              <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
                <p className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">{isHi ? 'शुभ दिन' : 'Lucky Days'}</p>
                <div className="flex flex-wrap gap-2">
                  {avakhadaData.lucky_days.map((d: string) => (
                    <span key={d} className="px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{d}</span>
                  ))}
                </div>
              </div>
            )}
            {avakhadaData.good_numbers?.length > 0 && (
              <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
                <p className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">{isHi ? 'शुभ अंक' : 'Good Numbers'}</p>
                <div className="flex flex-wrap gap-2">
                  {avakhadaData.good_numbers.map((n: number) => (
                    <span key={n} className="px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">{n}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
