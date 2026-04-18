import { useMemo } from 'react';
import { Sunrise, Info } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
  minuteTick: number;
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

export default function LagnaTab({ panchang, language, t, timezoneOffset, minuteTick }: Props) {
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
  }, [lagnaTable, timezoneOffset, minuteTick]);

  // Check if any lagna has ganda/sandhi warning
  const hasGandaSandhi = lagnaTable.some((l: any) => l.ganda_sandhi);

  return (
    <div className="space-y-3">
      {/* Ganda/Sandhi Warning Banner */}
      {hasGandaSandhi && (
        <div className="rounded-lg border border-purple-200 bg-purple-50/60 p-3">
          <div className="flex items-start gap-2">
            <Info className="h-5 w-5 text-purple-600 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm font-semibold text-purple-900 mb-1">
                {language === 'hi' ? 'गंडा और संधि लग्न सतर्कता' : 'Ganda & Sandhi Lagna Alert'}
              </p>
              <p className="text-xs text-purple-700 leading-relaxed">
                {language === 'hi'
                  ? 'आज के दिन गंडा लग्न (किसी भी राशि के प्रथम 3°20′) और संधि लग्न (अंतिम 3°20′) अशुभ हैं। महत्वपूर्ण कार्यों के लिए इन समयों से बचें।'
                  : 'Today\'s Ganda Lagna (first 3°20′ of any sign) and Sandhi Lagna (last 3°20′) are inauspicious. Avoid important ceremonies during these periods.'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Current Lagna */}
      {currentLagna && (
        <div className="flex items-center gap-3 p-2 rounded-lg border border-sacred-gold/30 bg-sacred-gold/10">
          <Sunrise className="h-8 w-8 text-sacred-gold flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-muted-foreground">
              {t('auto.currentLagnaAscendan')}
            </p>
            <span className="font-bold text-foreground">
              {language === 'hi'
                ? currentLagna.lagna_hindi || RASHI_HINDI[currentLagna.lagna] || currentLagna.lagna
                : currentLagna.lagna}
            </span>
            {(panchang as any).samvat?.pushkara?.active && (
              <span className="inline-flex items-center gap-0.5 ml-1 px-1.5 py-0.5 rounded-full bg-amber-100 border border-amber-400/50 text-amber-700 text-[10px] font-semibold" title={language === 'hi' ? 'वर्तमान लग्न पुष्कर नवांश में है — अत्यन्त शुभ' : 'Current lagna is in Pushkara Navamsha — highly auspicious'}>
                ✦ {language === 'hi' ? 'पुष्कर नवांश' : 'Pushkara Navamsha'}
              </span>
            )}
            <span className="mx-2 text-sacred-gold">{currentLagna.start} - {currentLagna.end}</span>
            {LAGNA_INFO[currentLagna.lagna] && (
              <Text variant="small" as="span">
                {language === 'hi'
                  ? LAGNA_INFO[currentLagna.lagna].hi
                  : LAGNA_INFO[currentLagna.lagna].en}
              </Text>
            )}
          </div>
          <span className="px-2 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold font-semibold text-xs">
            {t('auto.now')}
          </span>
        </div>
      )}

      {/* Lagna Table */}
      <div className="rounded-lg border overflow-hidden">
        <h3 className="font-bold text-foreground p-2 flex items-center gap-1 bg-card/30">
          <Sunrise className="h-4 w-4 text-sacred-gold" />
          {language === 'hi' ? 'दिन के लग्न' : "Today's Lagna Changes"}
        </h3>

        <div className="overflow-x-auto">
          <Table className="w-full text-sm">
            <TableHeader>
              <TableRow className="bg-sacred-gold/15">
                <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {t('auto.lagna')}
                </TableHead>
                <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {t('auto.start')}
                </TableHead>
                <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {t('auto.end')}
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {lagnaTable.map((lagna, index) => {
                const isCurrent = currentLagna?.start === lagna.start && currentLagna?.end === lagna.end;

                return (
                  <TableRow
                    key={index}
                    className={`
                      border-b border/50 last:border-0
                      ${isCurrent ? 'bg-sacred-gold/10' : index % 2 === 0 ? 'bg-card/30' : ''}
                      ${(lagna as any).ganda_sandhi ? 'opacity-75' : ''}
                    `}
                  >
                    <TableCell className="px-2 py-1">
                      <div className="flex items-center gap-1.5">
                        <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-foreground'}`}>
                          {language === 'hi'
                            ? lagna.lagna_hindi || RASHI_HINDI[lagna.lagna] || lagna.lagna
                            : lagna.lagna}
                        </span>
                        {(lagna as any).ganda_sandhi && (
                          <span
                            className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[11px] font-semibold"
                            style={{
                              backgroundColor: (lagna as any).ganda_sandhi === 'ganda' ? 'rgba(239,68,68,0.15)' : 'rgba(168,85,247,0.15)',
                              color: (lagna as any).ganda_sandhi === 'ganda' ? '#dc2626' : '#a855f7',
                              border: `1px solid ${(lagna as any).ganda_sandhi === 'ganda' ? 'rgba(239,68,68,0.4)' : 'rgba(168,85,247,0.4)'}`
                            }}
                            title={
                              (lagna as any).ganda_sandhi === 'ganda'
                                ? (language === 'hi' ? 'गंडा लग्न — पहले 3°20′ (अशुभ)' : 'Ganda Lagna — first 3°20′ (inauspicious)')
                                : (language === 'hi' ? 'संधि लग्न — अंतिम 3°20′ (अशुभ)' : 'Sandhi Lagna — last 3°20′ (inauspicious)')
                            }
                          >
                            ⚠ {language === 'hi'
                              ? ((lagna as any).ganda_sandhi === 'ganda' ? 'गंडा' : 'संधि')
                              : ((lagna as any).ganda_sandhi === 'ganda' ? 'Ganda' : 'Sandhi')}
                          </span>
                        )}
                        {isCurrent && (
                          <span className="px-1.5 py-0.5 text-xs bg-sacred-gold text-background rounded-full">
                            {t('auto.now')}
                          </span>
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="px-2 py-1 text-muted-foreground">
                      {lagna.start}
                    </TableCell>
                    <TableCell className="px-2 py-1 text-muted-foreground">
                      {lagna.end}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Lagna Info */}
      <div className="rounded-lg border p-2">
        <div className="flex items-start gap-2">
          <Info className="h-4 w-4 text-sacred-gold mt-0.5 flex-shrink-0" />
          <div>
            <Heading as={4} variant={4}>
              {t('auto.aboutLagnaAscendant')}
            </Heading>
            <p className="text-sm text-muted-foreground leading-relaxed mb-2">
              {t('auto.lagnaAscendantIsTheS')}
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div className="p-2 rounded-lg bg-card/50">
                <strong className="text-foreground">
                  {t('auto.movableSigns')}
                </strong>
                <p className="text-muted-foreground mt-0.5">
                  {t('auto.ariesCancerLibraCapr')}
                </p>
              </div>
              <div className="p-2 rounded-lg bg-card/50">
                <strong className="text-foreground">
                  {t('auto.fixedSigns')}
                </strong>
                <p className="text-muted-foreground mt-0.5">
                  {t('auto.taurusLeoScorpioAqua')}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}