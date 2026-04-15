import { Loader2 } from 'lucide-react';
import { translateSign, translateNakshatra } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface UpagrahasTabProps {
  upagrahasData: any;
  loadingUpagrahas: boolean;
  language: string;
  t: (key: string) => string;
}

export default function UpagrahasTab({ upagrahasData, loadingUpagrahas, language, t }: UpagrahasTabProps) {
  const UPAGRAHA_HI: Record<string, string> = {
    Gulika: 'गुलिक',
    Mandi: 'मांडी',
    Yamakantaka: 'यमकंटक',
    Ardhaprahara: 'अर्धप्रहर',
    Kala: 'काल',
    Mrityu: 'मृत्यु',
    Dhuma: 'धूम',
    Vyatipata: 'व्यतीपात',
    Parivesha: 'परिवेष',
    IndraChapa: 'इन्द्रचाप',
    Upaketu: 'उपकेतु',
  };
  const upagrahaLabel = (name: string) => (language === 'hi' ? (UPAGRAHA_HI[name] || name) : name);

  if (loadingUpagrahas) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-primary" /><span className="ml-2 text-foreground">{t('kundli.loadingUpagrahas')}</span></div>
    );
  }

  if (!upagrahasData) {
    return <p className="text-center text-foreground py-8">{t('common.noData')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-muted rounded-xl border border-border p-4">
        <Heading as={4} variant={4} className="mb-3">{t('section.upagrahasTitle')}</Heading>
        <Table className="w-full text-sm">
          <TableHeader><TableRow className="bg-muted">
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.upagraha')}</TableHead>
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.longitude')}</TableHead>
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.sign')}</TableHead>
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.nakshatra')}</TableHead>
          </TableRow></TableHeader>
          <TableBody>
            {(() => {
              const raw = upagrahasData.upagrahas;
              const items = Array.isArray(raw) ? raw : Object.entries(raw || {}).map(([name, data]: [string, any]) => ({ name, ...data }));
              return items.map((u: any) => (
                <TableRow key={u.name} className="border-t border-border">
                  <TableCell className="p-2 font-semibold text-foreground">{upagrahaLabel(u.name)}</TableCell>
                  <TableCell className="p-2 text-foreground">{typeof u.longitude === 'number' ? u.longitude.toFixed(2) + '\u00b0' : u.longitude}</TableCell>
                  <TableCell className="p-2 text-foreground">{translateSign(u.sign, language)}</TableCell>
                  <TableCell className="p-2 text-foreground">{translateNakshatra(u.nakshatra, language) || u.nakshatra}{u.nakshatra_pada ? ` (${t('kundli.pada')} ${u.nakshatra_pada})` : u.pada ? ` (${t('kundli.pada')} ${u.pada})` : ''}</TableCell>
                </TableRow>
              ));
            })()}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
