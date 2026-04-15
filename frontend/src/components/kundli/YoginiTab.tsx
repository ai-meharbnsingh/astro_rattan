import { Loader2 } from 'lucide-react';
import { translatePlanet, translateName } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface YoginiTabProps {
  yoginiData: any;
  loadingYogini: boolean;
  language: string;
  t: (key: string) => string;
}

export default function YoginiTab({ yoginiData, loadingYogini, language, t }: YoginiTabProps) {
  if (loadingYogini) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-primary" /><span className="ml-2 text-foreground">{t('kundli.loadingYoginiDasha')}</span></div>
    );
  }

  if (!yoginiData) {
    return <p className="text-center text-foreground py-8">{t('common.noData')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-muted rounded-xl border border-border p-4">
        <Heading as={4} variant={4} className="mb-3">
          {t('section.yoginiDasha')}
          {(yoginiData.current_dasha || yoginiData.current) && <span className="ml-2 text-sm px-2 py-1 rounded-full bg-primary text-white-dark">{t('common.current')}: {translateName(yoginiData.current_dasha || yoginiData.current, language)}</span>}
        </Heading>
        <Table className="w-full text-sm">
          <TableHeader><TableRow className="bg-muted">
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.yogini')}</TableHead>
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.planet')}</TableHead>
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.start')}</TableHead>
            <TableHead className="text-left p-2 text-primary font-medium">{t('table.end')}</TableHead>
            <TableHead className="text-center p-2 text-primary font-medium">{t('table.years')}</TableHead>
          </TableRow></TableHeader>
          <TableBody>
            {(yoginiData.periods || yoginiData.dashas || []).map((d: any, i: number) => {
              const currentName = yoginiData.current_dasha || yoginiData.current;
              const isCurrent = d.yogini === currentName || d.is_current;
              return (
                <TableRow key={i} className={`border-t border-border ${isCurrent ? 'bg-muted font-semibold' : ''}`}>
                  <TableCell className="p-2 text-foreground">{translateName(d.yogini, language)}{isCurrent ? ' \u2190' : ''}</TableCell>
                  <TableCell className="p-2 text-foreground">{translatePlanet(d.planet, language)}</TableCell>
                  <TableCell className="p-2 text-foreground">{d.start_date || d.start}</TableCell>
                  <TableCell className="p-2 text-foreground">{d.end_date || d.end}</TableCell>
                  <TableCell className="p-2 text-center text-foreground">{d.span || d.years}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
