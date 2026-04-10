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
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.loadingYoginiDasha')}</span></div>
    );
  }

  if (!yoginiData) {
    return <p className="text-center text-cosmic-text py-8">{t('common.noData')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
        <h4 className="font-display font-semibold text-sacred-brown mb-3">
          {t('section.yoginiDasha')}
          {(yoginiData.current_dasha || yoginiData.current) && <span className="ml-2 text-sm px-2 py-1 rounded-full bg-sacred-gold-dark text-white-dark">{t('common.current')}: {translateName(yoginiData.current_dasha || yoginiData.current, language)}</span>}
        </h4>
        <table className="w-full text-sm">
          <thead><tr className="bg-sacred-gold">
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
                <tr key={i} className={`border-t border-sacred-gold ${isCurrent ? 'bg-sacred-gold font-semibold' : ''}`}>
                  <td className="p-2 text-sacred-brown">{translateName(d.yogini, language)}{isCurrent ? ' \u2190' : ''}</td>
                  <td className="p-2 text-cosmic-text">{translatePlanet(d.planet, language)}</td>
                  <td className="p-2 text-cosmic-text">{d.start_date || d.start}</td>
                  <td className="p-2 text-cosmic-text">{d.end_date || d.end}</td>
                  <td className="p-2 text-center text-cosmic-text">{d.span || d.years}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
