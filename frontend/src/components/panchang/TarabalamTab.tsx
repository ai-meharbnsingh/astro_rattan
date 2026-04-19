import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

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
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-2">
      {/* Tarabalam Section */}
      <div className="rounded-lg border overflow-hidden">
        <div className="px-3 py-2 bg-sacred-gold/10 border-b border-sacred-gold/20">
          <h3 className="font-bold text-foreground text-sm">
            {t('panchang.tarabalam')}
          </h3>
          <p className="text-xs text-muted-foreground">
            {t('panchang.nakshatraCompatToday')}
          </p>
        </div>

        {tarabalam.length === 0 ? emptyMessage : (
          <div className="overflow-x-auto">
            <Table className="table-fixed text-xs sm:text-sm w-full">
              <TableHeader>
                <TableRow className="bg-sacred-gold/15">
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[40%]">
                    {t('auto.nakshatra')}
                  </TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[35%]">
                    {t('panchang.tara')}
                  </TableHead>
                  <TableHead className="text-center px-2 py-1 text-sacred-gold-dark font-semibold w-[25%]">
                    {t('auto.status')}
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {tarabalam.map((row, idx) => (
                  <TableRow
                    key={`tara-${idx}`}
                    className={`border-b border/50 last:border-0 ${!row.good ? 'bg-red-50/50' : ''}`}
                  >
                    <TableCell className="px-2 py-1 font-medium text-foreground">
                      {row.nakshatra}
                    </TableCell>
                    <TableCell className="px-2 py-1 text-muted-foreground">
                      {row.tara}
                      {row.interpretation && (
                        <p className="text-[11px] text-muted-foreground mt-0.5 italic">
                          {typeof row.interpretation === 'object'
                            ? (hi ? row.interpretation.hi : row.interpretation.en)
                            : (hi ? row.interpretation_hi || row.interpretation : row.interpretation)}
                        </p>
                      )}
                    </TableCell>
                    <TableCell className="px-2 py-1 text-center">
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
      <div className="rounded-lg border overflow-hidden">
        <div className="px-3 py-2 bg-sacred-gold/10 border-b border-sacred-gold/20">
          <h3 className="font-bold text-foreground text-sm">
            {t('panchang.chandrabalam')}
          </h3>
          <p className="text-xs text-muted-foreground">
            {t('panchang.moonStrengthByRashi')}
          </p>
        </div>

        {chandrabalam.length === 0 ? emptyMessage : (
          <div className="overflow-x-auto">
            <Table className="table-fixed text-xs sm:text-sm w-full">
              <TableHeader>
                <TableRow className="bg-sacred-gold/15">
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[35%]">
                    {t('auto.rashi')}
                  </TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">
                    {t('panchang.balam')}
                  </TableHead>
                  <TableHead className="text-center px-2 py-1 text-sacred-gold-dark font-semibold w-[35%]">
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
                      className={`border-b border/50 last:border-0 ${!row.good ? 'bg-red-50/50' : ''} ${isAshtama ? 'bg-red-100/60' : ''}`}
                    >
                      <TableCell className="px-2 py-1 font-medium text-foreground">
                        {hi ? hiRashi(row.rashi) : row.rashi}
                        {isAshtama && (
                          <span className="ml-1 inline-block px-1 py-0.5 rounded text-[10px] font-bold bg-red-600 text-white leading-none">
                            {t('panchang.ashtama')}
                          </span>
                        )}
                      </TableCell>
                      <TableCell className="px-2 py-1 text-muted-foreground">
                        {row.balam}
                        {row.interpretation && (
                          <p className="text-[11px] text-muted-foreground mt-0.5 italic">
                            {typeof row.interpretation === 'object'
                              ? (hi ? row.interpretation.hi : row.interpretation.en)
                              : (hi ? row.interpretation_hi || row.interpretation : row.interpretation)}
                          </p>
                        )}
                      </TableCell>
                      <TableCell className="px-2 py-1 text-center">
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
  );
}
