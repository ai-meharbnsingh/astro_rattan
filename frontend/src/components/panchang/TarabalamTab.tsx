import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";
import { Star } from 'lucide-react';
import PanchangTabHeader from './PanchangTabHeader';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

const RASHI_HI: Record<string, string> = {
  Mesha: 'मेष', Aries: 'मेष',
  Vrishabha: 'वृषभ', Taurus: 'वृषभ',
  Mithuna: 'मिथुन', Gemini: 'मिथुन',
  Karka: 'कर्क', Cancer: 'कर्क',
  Simha: 'सिंह', Leo: 'सिंह',
  Kanya: 'कन्या', Virgo: 'कन्या',
  Tula: 'तुला', Libra: 'तुला',
  Vrishchika: 'वृश्चिक', Scorpio: 'वृश्चिक',
  Dhanu: 'धनु', Sagittarius: 'धनु',
  Makara: 'मकर', Capricorn: 'मकर',
  Kumbha: 'कुम्भ', Aquarius: 'कुम्भ',
  Meena: 'मीन', Pisces: 'मीन',
};

const hiRashi = (name: string): string => RASHI_HI[name] || name;

export default function TarabalamTab({ panchang, language, t }: Props) {
  const hi = language === 'hi';
  const tarabalam = panchang.tarabalam || [];
  const chandrabalam = panchang.chandrabalam || [];

  const emptyMessage = (
    <div className="text-center py-6 text-muted-foreground text-sm">
      {t('auto.noDataAvailable')}
    </div>
  );

  return (
    <div className="space-y-4">
      <PanchangTabHeader
        icon={Star}
        title={language === 'hi' ? 'तारा बल / चन्द्र बल' : 'Tara Balam / Chandra Balam'}
        description={language === 'hi'
          ? 'आज के नक्षत्र-संगति (तारा बल) और चन्द्र राशि के अनुसार बल (चन्द्र बल) का सार।'
          : 'A quick view of Tarabalam (nakshatra compatibility) and Chandrabalam (moon strength by rashi) for today.'}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-2">
        {/* Tarabalam Section */}
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Star className="w-4 h-4" />
            <span>{t('panchang.tarabalam')}</span>
          </div>
          <div className="px-4 py-2 text-xs text-muted-foreground border-b border-border">
            {t('panchang.nakshatraCompatToday')}
          </div>

          {tarabalam.length === 0 ? emptyMessage : (
            <div className="overflow-x-auto">
              <Table className="table-fixed text-xs sm:text-sm w-full">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[40%]">
                      {t('auto.nakshatra')}
                    </TableHead>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[35%]">
                      {t('panchang.tara')}
                    </TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[25%]">
                      {t('auto.status')}
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {tarabalam.map((row, idx) => (
                    <TableRow
                      key={`tara-${idx}`}
                      className={`border-t border-border hover:bg-muted/5 ${!row.good ? 'bg-red-50/50' : ''}`}
                    >
                      <TableCell className="p-2 font-medium text-foreground">
                        {row.nakshatra}
                      </TableCell>
                      <TableCell className="p-2 text-muted-foreground">
                        {row.tara}
                        {row.interpretation && (
                          <p className="text-[11px] text-muted-foreground mt-0.5 italic">
                            {typeof row.interpretation === 'object'
                              ? (hi ? row.interpretation.hi : row.interpretation.en)
                              : (hi ? row.interpretation_hi || row.interpretation : row.interpretation)}
                          </p>
                        )}
                      </TableCell>
                      <TableCell className="p-2 text-center">
                        {row.good ? (
                          <span className="inline-block px-1.5 py-0.5 rounded text-xs font-medium bg-green-500/15 text-green-600">
                            {t('auto.good')} ✓
                          </span>
                        ) : (
                          <span className="inline-block px-1.5 py-0.5 rounded text-xs font-medium bg-red-500/10 text-red-600">
                            {t('panchang.bad')} ✗
                          </span>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </div>

        {/* Chandrabalam Section */}
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Star className="w-4 h-4" />
            <span>{t('panchang.chandrabalam')}</span>
          </div>
          <div className="px-4 py-2 text-xs text-muted-foreground border-b border-border">
            {t('panchang.moonStrengthByRashi')}
          </div>

          {chandrabalam.length === 0 ? emptyMessage : (
            <div className="overflow-x-auto">
              <Table className="table-fixed text-xs sm:text-sm w-full">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[35%]">
                      {t('auto.rashi')}
                    </TableHead>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[30%]">
                      {t('panchang.balam')}
                    </TableHead>
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[35%]">
                      {t('auto.status')}
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {chandrabalam.map((row, idx) => {
                    const isAshtama = row.house_from_moon === 8;
                    return (
                      <TableRow
                        key={`chandra-${idx}`}
                        className={`border-t border-border hover:bg-muted/5 ${!row.good ? 'bg-red-50/50' : ''} ${isAshtama ? 'bg-red-100/60' : ''}`}
                      >
                        <TableCell className="p-2 font-medium text-foreground">
                          {hi ? hiRashi(row.rashi) : row.rashi}
                          {isAshtama && (
                            <span className="ml-1 inline-block px-1 py-0.5 rounded text-[10px] font-bold bg-red-600 text-white leading-none">
                              {t('panchang.ashtama')}
                            </span>
                          )}
                        </TableCell>
                        <TableCell className="p-2 text-muted-foreground">
                          {row.balam}
                          {row.interpretation && (
                            <p className="text-[11px] text-muted-foreground mt-0.5 italic">
                              {typeof row.interpretation === 'object'
                                ? (hi ? row.interpretation.hi : row.interpretation.en)
                                : (hi ? row.interpretation_hi || row.interpretation : row.interpretation)}
                            </p>
                          )}
                        </TableCell>
                        <TableCell className="p-2 text-center">
                          {row.good ? (
                            <span className="inline-block px-1.5 py-0.5 rounded text-xs font-medium bg-green-500/15 text-green-600">
                              {t('auto.good')} ✓
                            </span>
                          ) : (
                            <span className="inline-block px-1.5 py-0.5 rounded text-xs font-medium bg-red-500/10 text-red-600">
                              {t('panchang.bad')} ✗
                            </span>
                          )}
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
