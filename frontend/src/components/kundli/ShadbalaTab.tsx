import { Loader2 } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';

interface ShadbalaTabProps {
  shadbalaData: any;
  loadingShadbala: boolean;
  language: string;
  t: (key: string) => string;
}

export default function ShadbalaTab({ shadbalaData, loadingShadbala, language, t }: ShadbalaTabProps) {
  if (loadingShadbala) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-cosmic-text/70">{t('kundli.calculatingShadbala')}</span>
      </div>
    );
  }

  if (!shadbalaData?.planets) {
    return <p className="text-center text-cosmic-text/70 py-8">{t('kundli.clickShadbalaTab')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
        <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.shadbalaStrength')}</h4>
        <div className="space-y-3">
          {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
            const data = shadbalaData.planets[planet];
            if (!data) return null;
            const pct = Math.min((data.total / data.required) * 100, 150);
            const barColor = data.is_strong ? 'var(--aged-gold-dim)' : '#8B2332';
            return (
              <div key={planet} className="flex items-center gap-3">
                <span className="w-16 text-sm font-medium text-sacred-brown">{translatePlanet(planet, language)}</span>
                <div className="flex-1 relative">
                  <div className="bg-sacred-gold/10 rounded-full h-5 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{ width: `${Math.min(pct, 100)}%`, backgroundColor: barColor }}
                    />
                  </div>
                  <div
                    className="absolute top-0 h-5 border-r-2 border-dashed border-sacred-brown/40"
                    style={{ left: `${Math.min((data.required / (data.required * 1.5)) * 100, 100)}%` }}
                    title={`Required: ${data.required}`}
                  />
                </div>
                <span className={`text-sm w-20 text-right font-medium ${data.is_strong ? 'text-sacred-gold-dark' : 'text-wax-red-deep'}`}>
                  {data.total} / {data.required}
                </span>
              </div>
            );
          })}
        </div>
        <div className="flex items-center gap-4 mt-3 text-xs text-cosmic-text/70">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />
            <span>{t('kundli.strong')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#8B2332' }} />
            <span>{t('kundli.weak')}</span>
          </div>
        </div>
      </div>

      <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
        <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.detailedBreakdown')}</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-sacred-gold/20">
                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'स्थान' : 'Sthana'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'दिग्' : 'Dig'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'काल' : 'Kala'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'चेष्टा' : 'Cheshta'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'नैसर्गिक' : 'Naisargika'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'दृक्' : 'Drik'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.total')}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'अनुपात' : 'Ratio'}</th>
              </tr>
            </thead>
            <tbody>
              {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                const d = shadbalaData.planets[planet];
                if (!d) return null;
                return (
                  <tr key={planet} className={`border-t border-sacred-gold/10 ${d.is_strong ? '' : 'bg-red-5'}`}>
                    <td className="p-2 text-sacred-brown font-medium">{translatePlanet(planet, language)}</td>
                    <td className="text-center p-2 text-cosmic-text/70">{d.sthana}</td>
                    <td className="text-center p-2 text-cosmic-text/70">{d.dig}</td>
                    <td className="text-center p-2 text-cosmic-text/70">{d.kala}</td>
                    <td className="text-center p-2 text-cosmic-text/70">{d.cheshta}</td>
                    <td className="text-center p-2 text-cosmic-text/70">{d.naisargika}</td>
                    <td className="text-center p-2 text-cosmic-text/70">{d.drik}</td>
                    <td className={`text-center p-2 font-semibold ${d.is_strong ? 'text-sacred-gold-dark' : 'text-wax-red-deep'}`}>{d.total}</td>
                    <td className={`text-center p-2 font-medium ${d.ratio >= 1 ? 'text-sacred-gold-dark' : 'text-wax-red-deep'}`}>{d.ratio}x</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
