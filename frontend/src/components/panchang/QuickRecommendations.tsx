import { Card, CardContent } from '@/components/ui/card';
import { Heading } from '@/components/ui/heading';
import { CheckCircle, AlertTriangle, Info } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function QuickRecommendations({ panchang, language, t }: Props) {
  const isHi = language === 'hi';
  const l = (en: string, hi: string) => isHi ? hi : en;

  // Generate recommendations based on panchang
  const dos: string[] = [];
  const donts: string[] = [];
  const notes: string[] = [];

  // Tithi-based recommendations
  const tithi = panchang.tithi?.name?.toLowerCase() || '';

  if (tithi.includes('ekadashi')) {
    dos.push(l('Good day for fasting (Vrat)', 'व्रत रखने का दिन'));
    dos.push(l('Worship Vishnu (विष्णु की पूजा)', 'विष्णु पूजा का समय'));
    donts.push(l('Avoid non-vegetarian food', 'मांसाहार से बचें'));
  }

  if (tithi.includes('amavasya') || tithi.includes('purnima')) {
    dos.push(l('Good for ancestors worship (तर्पण)', 'पितृ अर्चना का समय'));
    notes.push(l('Powerful day for meditation', 'ध्यान के लिए शक्तिशाली दिन'));
  }

  if (tithi.includes('pradosh')) {
    dos.push(l('Excellent for Shiva worship', 'शिव पूजा के लिए उत्तम'));
    dos.push(l('Perform evening rituals (संध्या)', 'संध्या कर्म का समय'));
  }

  if (tithi.includes('chaturthi')) {
    dos.push(l('Day of Ganesha worship', 'गणेश जी की पूजा का दिन'));
    dos.push(l('Good for starting new ventures', 'नए कार्य शुरू करने के लिए अच्छा'));
  }

  // Nakshatra-based recommendations
  const nakshatra = panchang.nakshatra?.name?.toLowerCase() || '';

  if (nakshatra.includes('ashwini') || nakshatra.includes('bharani') || nakshatra.includes('kritika')) {
    dos.push(l('Good for traveling', 'यात्रा के लिए शुभ'));
    dos.push(l('Favorable for starting education', 'शिक्षा शुरू करने के लिए अच्छा'));
  }

  if (nakshatra.includes('rohini') || nakshatra.includes('mrigashira')) {
    dos.push(l('Good for prosperity activities', 'धन संबंधी कार्यों के लिए'));
    dos.push(l('Favorable for planting/sowing', 'बीज बोने के लिए शुभ'));
  }

  if (nakshatra.includes('magha') || nakshatra.includes('purva')) {
    dos.push(l('Good for ceremonies & rituals', 'समारोह और पूजा के लिए'));
    dos.push(l('Favorable for construction start', 'निर्माण कार्य शुरू करने के लिए'));
  }

  // Yoga-based recommendations
  const yoga = panchang.yoga?.name?.toLowerCase() || '';

  if (yoga.includes('auspicious') || yoga.includes('siddhi') || yoga.includes('amrit')) {
    dos.push(l('Extra favorable for important events', 'महत्वपूर्ण कार्यों के लिए विशेष अनुकूल'));
    notes.push(l('Use this time wisely', 'इस समय का सर्वश्रेष्ठ उपयोग करें'));
  }

  if (yoga.includes('vaidhriti') || yoga.includes('vyatipata')) {
    donts.push(l('Avoid starting major projects', 'बड़े प्रोजेक्ट शुरू न करें'));
    notes.push(l('Better suited for completion of ongoing work', 'चल रहे काम पूरा करने के लिए अच्छा'));
  }

  // Special yogas
  if (panchang.special_yogas?.sarvartha_siddhi?.active) {
    dos.push(l('Perfect for ALL auspicious activities', 'सभी शुभ कार्यों के लिए उत्तम'));
    notes.push(l('Rare yoga - do not miss this opportunity!', 'दुर्लभ योग - मौका न छोड़ें'));
  }

  if (panchang.special_yogas?.ganda_moola?.active) {
    donts.push(l('AVOID major decisions today', 'आज महत्वपूर्ण निर्णय न लें'));
    donts.push(l('Not favorable for new beginning', 'नई शुरुआत के लिए प्रतिकूल'));
    notes.push(l('Choose another date if possible', 'संभव हो तो दूसरी तारीख चुनें'));
  }

  if (panchang.special_yogas?.dwipushkar?.active) {
    dos.push(l('Excellent for prosperity & wealth activities', 'धन और समृद्धि के कार्यों के लिए'));
  }

  // Paksha-based
  const paksha = panchang.tithi?.paksha?.toLowerCase() || '';
  if (paksha.includes('shukla')) {
    notes.push(l('Shukla Paksha - growth & positive phase', 'शुक्ल पक्ष - वृद्धि और सकारात्मक अवधि'));
  } else if (paksha.includes('krishna')) {
    notes.push(l('Krishna Paksha - introspection & completion phase', 'कृष्ण पक्ष - विचार और समापन की अवधि'));
  }

  return (
    <Card className="bg-gradient-to-br from-background to-background/50 border-border/50">
      <CardContent className="p-4">
        <div className="space-y-4">
          {/* Do's */}
          {dos.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <Heading as={5} variant={5} className="text-green-700">
                  {l('Good to Do Today', 'आज करने के लिए अच्छे काम')}
                </Heading>
              </div>
              <ul className="space-y-1">
                {dos.map((item, idx) => (
                  <li key={idx} className="text-sm text-foreground flex items-start gap-2">
                    <span className="text-green-600 mt-1">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Don'ts */}
          {donts.length > 0 && (
            <div className="pt-2 border-t border-border/30">
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangle className="w-4 h-4 text-orange-600" />
                <Heading as={5} variant={5} className="text-orange-700">
                  {l('Avoid Today', 'आज से बचें')}
                </Heading>
              </div>
              <ul className="space-y-1">
                {donts.map((item, idx) => (
                  <li key={idx} className="text-sm text-foreground flex items-start gap-2">
                    <span className="text-orange-600 mt-1">⚠</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Notes */}
          {notes.length > 0 && (
            <div className="pt-2 border-t border-border/30">
              <div className="flex items-center gap-2 mb-2">
                <Info className="w-4 h-4 text-blue-600" />
                <Heading as={5} variant={5} className="text-blue-700">
                  {l('Important Notes', 'महत्वपूर्ण नोट्स')}
                </Heading>
              </div>
              <ul className="space-y-1">
                {notes.map((item, idx) => (
                  <li key={idx} className="text-sm text-foreground flex items-start gap-2">
                    <span className="text-blue-600 mt-1">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {dos.length === 0 && donts.length === 0 && notes.length === 0 && (
            <p className="text-sm text-muted-foreground text-center py-4">
              {l('No specific recommendations - good day for regular activities', 'सामान्य कार्यों के लिए अच्छा दिन')}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
