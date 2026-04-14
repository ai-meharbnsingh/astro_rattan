import { useMemo } from 'react';
import { Sunrise, Info } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
}

// Lagna (Ascendant) descriptions
const LAGNA_INFO: Record<string, { en: string; hi: string }> = {
  'Aries': { en: 'Movable, Fire sign, ruled by Mars', hi: 'चर, अग्नि तत्व, मंगल द्वारा शासित' },
  'Taurus': { en: 'Fixed, Earth sign, ruled by Venus', hi: 'स्थिर, पृथ्वी तत्व, शुक्र द्वारा शासित' },
  'Gemini': { en: 'Dual, Air sign, ruled by Mercury', hi: 'द्विस्वभाव, वायु तत्व, बुध द्वारा शासित' },
  'Cancer': { en: 'Movable, Water sign, ruled by Moon', hi: 'चर, जल तत्व, चंद्र द्वारा शासित' },
  'Leo': { en: 'Fixed, Fire sign, ruled by Sun', hi: 'स्थिर, अग्नि तत्व, सूर्य द्वारा शासित' },
  'Virgo': { en: 'Dual, Earth sign, ruled by Mercury', hi: 'द्विस्वभाव, पृथ्वी तत्व, बुध द्वारा शासित' },
  'Libra': { en: 'Movable, Air sign, ruled by Venus', hi: 'चर, वायु तत्व, शुक्र द्वारा शासित' },
  'Scorpio': { en: 'Fixed, Water sign, ruled by Mars', hi: 'स्थिर, जल तत्व, मंगल द्वारा शासित' },
  'Sagittarius': { en: 'Dual, Fire sign, ruled by Jupiter', hi: 'द्विस्वभाव, अग्नि तत्व, गुरु द्वारा शासित' },
  'Capricorn': { en: 'Movable, Earth sign, ruled by Saturn', hi: 'चर, पृथ्वी तत्व, शनि द्वारा शासित' },
  'Aquarius': { en: 'Fixed, Air sign, ruled by Saturn', hi: 'स्थिर, वायु तत्व, शनि द्वारा शासित' },
  'Pisces': { en: 'Dual, Water sign, ruled by Jupiter', hi: 'द्विस्वभाव, जल तत्व, गुरु द्वारा शासित' },
};

const RASHI_HINDI: Record<string, string> = {
  'Aries': 'मेष', 'Taurus': 'वृषभ', 'Gemini': 'मिथुन', 'Cancer': 'कर्क',
  'Leo': 'सिंह', 'Virgo': 'कन्या', 'Libra': 'तुला', 'Scorpio': 'वृश्चिक',
  'Sagittarius': 'धनु', 'Capricorn': 'मकर', 'Aquarius': 'कुंभ', 'Pisces': 'मीन',
};

export default function LagnaTab({ panchang, language, t, timezoneOffset }: Props) {
  const lagnaTable = panchang.lagna_table || [];
  const toMinutes = (time: string) => {
    const [h, m] = String(time || '').split(':').map(Number);
    if (Number.isNaN(h) || Number.isNaN(m)) return -1;
    return h * 60 + m;
  };
  const isInTimeRange = (current: number, start: string, end: string) => {
    const startM = toMinutes(start);
    const endM = toMinutes(end);
    if (startM < 0 || endM < 0 || startM === endM) return false;
    if (startM < endM) return current >= startM && current < endM;
    return current >= startM || current < endM;
  };

  // Memoize current lagna calculation to avoid running on every render
  const currentLagna = useMemo(() => {
    // Find current lagna (based on panchang location time, not browser local time)
    const currentTimeAtLocation = new Date(Date.now() + ((timezoneOffset + new Date().getTimezoneOffset()) * 60 * 1000));
    const currentMinutes = currentTimeAtLocation.getHours() * 60 + currentTimeAtLocation.getMinutes();

    return lagnaTable.find((l) => isInTimeRange(currentMinutes, l.start, l.end));
  }, [lagnaTable, timezoneOffset]);

  return (
    <div className="space-y-3">
      {/* Current Lagna */}
      {currentLagna && (
        <div className="flex items-center gap-3 p-2 rounded-lg border border-sacred-gold/30 bg-sacred-gold/10">
          <Sunrise className="h-8 w-8 text-sacred-gold flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-cosmic-text-secondary">
              {language === 'hi' ? 'वर्तमान लग्न' : 'Current Lagna (Ascendant)'}
            </p>
            <span className="font-bold text-cosmic-text-primary">
              {language === 'hi'
                ? currentLagna.lagna_hindi || RASHI_HINDI[currentLagna.lagna] || currentLagna.lagna
                : currentLagna.lagna}
            </span>
            <span className="mx-2 text-sacred-gold">{currentLagna.start} - {currentLagna.end}</span>
            {LAGNA_INFO[currentLagna.lagna] && (
              <span className="text-xs text-cosmic-text-secondary">
                {language === 'hi'
                  ? LAGNA_INFO[currentLagna.lagna].hi
                  : LAGNA_INFO[currentLagna.lagna].en}
              </span>
            )}
          </div>
          <span className="px-2 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold font-semibold text-xs">
            {language === 'hi' ? 'अभी' : 'Now'}
          </span>
        </div>
      )}

      {/* Lagna Table */}
      <div className="rounded-lg border border-cosmic-border overflow-hidden">
        <h3 className="font-bold text-cosmic-text-primary p-2 flex items-center gap-1 bg-cosmic-card/30">
          <Sunrise className="h-4 w-4 text-sacred-gold" />
          {language === 'hi' ? 'दिन के लग्न' : "Today's Lagna Changes"}
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-sacred-gold/15">
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'लग्न' : 'Lagna'}
                </th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'प्रारंभ' : 'Start'}
                </th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'समाप्ति' : 'End'}
                </th>
              </tr>
            </thead>
            <tbody>
              {lagnaTable.map((lagna, index) => {
                const isCurrent = currentLagna?.start === lagna.start && currentLagna?.end === lagna.end;

                return (
                  <tr
                    key={index}
                    className={`
                      border-b border-cosmic-border/50 last:border-0
                      ${isCurrent ? 'bg-sacred-gold/10' : index % 2 === 0 ? 'bg-cosmic-card/30' : ''}
                    `}
                  >
                    <td className="px-2 py-1">
                      <div className="flex items-center gap-1">
                        <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                          {language === 'hi'
                            ? lagna.lagna_hindi || RASHI_HINDI[lagna.lagna] || lagna.lagna
                            : lagna.lagna}
                        </span>
                        {isCurrent && (
                          <span className="px-1.5 py-0.5 text-xs bg-sacred-gold text-cosmic-bg rounded-full">
                            {language === 'hi' ? 'अभी' : 'Now'}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-2 py-1 text-cosmic-text-secondary">
                      {lagna.start}
                    </td>
                    <td className="px-2 py-1 text-cosmic-text-secondary">
                      {lagna.end}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Lagna Info */}
      <div className="rounded-lg border border-cosmic-border p-2">
        <div className="flex items-start gap-2">
          <Info className="h-4 w-4 text-sacred-gold mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-semibold text-cosmic-text-primary mb-1">
              {language === 'hi' ? 'लग्न के बारे में' : 'About Lagna (Ascendant)'}
            </h4>
            <p className="text-sm text-cosmic-text-secondary leading-relaxed mb-2">
              {language === 'hi'
                ? 'लग्न (लग्न) वह राशि है जो पूर्व दिशा से उदित होती है। यह व्यक्ति के व्यक्तित्व, स्वास्थ्य और जीवन की दिशा का संकेत देता है। प्रत्येक लग्न लगभग 2 घंटे तक रहता है।'
                : 'Lagna (Ascendant) is the sign rising on the eastern horizon. It indicates personality, health, and life direction. Each lagna lasts approximately 2 hours.'}
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div className="p-2 rounded-lg bg-cosmic-card/50">
                <strong className="text-cosmic-text-primary">
                  {language === 'hi' ? 'चर राशि:' : 'Movable Signs:'}
                </strong>
                <p className="text-cosmic-text-secondary mt-0.5">
                  {language === 'hi'
                    ? 'मेष, कर्क, तुला, मकर - परिवर्तनशील'
                    : 'Aries, Cancer, Libra, Capricorn - Changeable'}
                </p>
              </div>
              <div className="p-2 rounded-lg bg-cosmic-card/50">
                <strong className="text-cosmic-text-primary">
                  {language === 'hi' ? 'स्थिर राशि:' : 'Fixed Signs:'}
                </strong>
                <p className="text-cosmic-text-secondary mt-0.5">
                  {language === 'hi'
                    ? 'वृषभ, सिंह, वृश्चिक, कुंभ - स्थिर'
                    : 'Taurus, Leo, Scorpio, Aquarius - Stable'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
