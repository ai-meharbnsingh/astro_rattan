import { Loader2 } from 'lucide-react';
import { translatePlanet, translateName } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';

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

  const currentName = yoginiData.current_dasha || yoginiData.current;

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-3">
          <span>{t('section.yoginiDasha')}</span>
          {currentName && (
            <span className="text-sm px-2 py-0.5 rounded-full bg-white/20 border border-white/30">
              {t('common.current')}: {translateName(currentName, language)}
            </span>
          )}
        </div>
        <Table className="w-full text-xs table-fixed">
          <TableHeader>
            <TableRow>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('table.yogini')}</TableHead>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[20%]">{t('table.planet')}</TableHead>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[20%]">{t('table.start')}</TableHead>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[20%]">{t('table.end')}</TableHead>
              <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[15%]">{t('table.years')}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {(yoginiData.periods || yoginiData.dashas || []).map((d: any, i: number) => {
              const isCurrent = d.yogini === currentName || d.is_current;
              return (
                <TableRow key={i} className={`border-t border-border ${isCurrent ? 'font-semibold' : ''}`}>
                  <TableCell className="p-2 text-foreground">{translateName(d.yogini, language)}{isCurrent ? ' ←' : ''}</TableCell>
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
