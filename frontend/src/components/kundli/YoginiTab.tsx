import { Loader2 } from 'lucide-react';
import { translatePlanet, translateName } from '@/lib/backend-translations';

interface YoginiTabProps {
  yoginiData: any;
  loadingYogini: boolean;
  language: string;
  t: (key: string) => string;
}

export default function YoginiTab({ yoginiData, loadingYogini, language, t }: YoginiTabProps) {
  if (loadingYogini) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text/70">{t('kundli.loadingYoginiDasha')}</span></div>
    );
  }

  if (!yoginiData) {
    return <p className="text-center text-cosmic-text/70 py-8">{t('common.noData')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <h4 className="font-display font-semibold text-sacred-brown mb-3">
          {t('section.yoginiDasha')}
          {(yoginiData.current_dasha || yoginiData.current) && <span className="ml-2 text-xs px-2 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold-dark">{t('common.current')}: {translateName(yoginiData.current_dasha || yoginiData.current, language)}</span>}
        </h4>
        <table className="w-full text-xs">
          <thead><tr className="bg-sacred-gold/10">
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.yogini')}</th>
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.start')}</th>
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.end')}</th>
            <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.years')}</th>
          </tr></thead>
          <tbody>
            {(yoginiData.periods || yoginiData.dashas || []).map((d: any, i: number) => {
              const currentName = yoginiData.current_dasha || yoginiData.current;
              const isCurrent = d.yogini === currentName || d.is_current;
              return (
                <tr key={i} className={`border-t border-sacred-gold/10 ${isCurrent ? 'bg-sacred-gold/10 font-semibold' : ''}`}>
                  <td className="p-2 text-sacred-brown">{translateName(d.yogini, language)}{isCurrent ? ' \u2190' : ''}</td>
                  <td className="p-2 text-cosmic-text/70">{translatePlanet(d.planet, language)}</td>
                  <td className="p-2 text-cosmic-text/70">{d.start_date || d.start}</td>
                  <td className="p-2 text-cosmic-text/70">{d.end_date || d.end}</td>
                  <td className="p-2 text-center text-cosmic-text/70">{d.span || d.years}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
