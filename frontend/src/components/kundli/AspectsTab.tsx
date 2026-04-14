import { Loader2 } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';

interface AspectsTabProps {
  aspectsData: any;
  loadingAspects: boolean;
  language: string;
  t: (key: string) => string;
}

export default function AspectsTab({ aspectsData, loadingAspects, language, t }: AspectsTabProps) {
  const BENEFICS = ['Jupiter', 'Venus', 'Moon', 'Mercury'];
  const spl = language === 'hi' ? ' विशेष' : ' Spl';
  const housePrefix = language === 'hi' ? 'भा' : 'H';

  if (loadingAspects) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.loadingAspects')}</span></div>
    );
  }

  if (!aspectsData) {
    return <p className="text-center text-cosmic-text py-8">{t('common.noData')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Aspects on Planets */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.aspectsOnPlanets')}</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead><tr className="bg-sacred-gold">
                <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{t('table.house')}</th>
                <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'शुभ दृष्टि' : 'Aspected By (Benefic)'}</th>
                <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'अशुभ दृष्टि' : 'Aspected By (Malefic)'}</th>
                <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'दृष्टि करता है' : 'Aspects To'}</th>
              </tr></thead>
              <tbody>
                {(() => {
                  const summary = aspectsData.planet_aspects_summary;
                  if (summary && typeof summary === 'object' && !Array.isArray(summary)) {
                    return Object.entries(summary).map(([planet, data]: [string, any], i: number) => {
                      const aspBy = data.aspected_by || [];
                      const beneficList = aspBy.filter((a: any) => BENEFICS.includes(a.planet || a));
                      const maleficList = aspBy.filter((a: any) => !BENEFICS.includes(a.planet || a));
                      const aspectsTo = data.aspects_to || [];
                      return (
                        <tr key={planet} className="border-t border-sacred-gold hover:bg-sacred-gold/5">
                          <td className="p-1.5 font-semibold text-sacred-brown">{translatePlanet(planet, language)}</td>
                          <td className="p-1.5 text-center">{data.house}</td>
                          <td className="p-1.5">
                            {beneficList.length > 0 ? beneficList.map((a: any, j: number) => (
                              <span key={j} className="inline-flex items-center gap-1 mr-2">
                                <span className="text-green-600 font-medium">{translatePlanet(a.planet || a, language)}</span>
                                <span className="text-[10px] text-cosmic-text">({a.strength || '1.0'}x {a.offset ? `${a.offset}${housePrefix}` : ''}{a.type === 'special' ? spl : ''})</span>
                              </span>
                            )) : <span className="text-cosmic-text">-</span>}
                          </td>
                          <td className="p-1.5">
                            {maleficList.length > 0 ? maleficList.map((a: any, j: number) => (
                              <span key={j} className="inline-flex items-center gap-1 mr-2">
                                <span className="text-red-500 font-medium">{translatePlanet(a.planet || a, language)}</span>
                                <span className="text-[10px] text-cosmic-text">({a.strength || '1.0'}x {a.offset ? `${a.offset}${housePrefix}` : ''}{a.type === 'special' ? spl : ''})</span>
                              </span>
                            )) : <span className="text-cosmic-text">-</span>}
                          </td>
                          <td className="p-1.5">
                            {aspectsTo.length > 0 ? aspectsTo.map((a: any, j: number) => (
                              <span key={j} className="inline-flex items-center gap-1 mr-2">
                                <span className="font-medium">{housePrefix}{a.house}</span>
                                <span className="text-[10px] text-cosmic-text">({a.strength}x)</span>
                              </span>
                            )) : <span className="text-cosmic-text">-</span>}
                          </td>
                        </tr>
                      );
                    });
                  }
                  return <tr><td colSpan={5} className="text-center p-4 text-cosmic-text">{t('common.noData')}</td></tr>;
                })()}
              </tbody>
            </table>
          </div>
        </div>

        {/* Aspects on Bhavas */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.aspectsOnBhavas')}</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead><tr className="bg-sacred-gold">
                <th className="text-center p-1.5 text-sacred-gold-dark font-medium w-12">{t('table.house')}</th>
                <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'शुभ दृष्टि' : 'Benefic Aspects (Shubh)'}</th>
                <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'अशुभ दृष्टि' : 'Malefic Aspects (Ashubh)'}</th>
              </tr></thead>
              <tbody>
                {(() => {
                  const bhavas = aspectsData.bhava_summary || aspectsData.bhava_aspects;
                  const bhavaAspects = aspectsData.aspects_on_bhavas || {};
                  const renderHouse = (houseNum: number, ba: any) => {
                    const entries = bhavaAspects[String(houseNum)] || [];
                    const aspectedBy = Array.isArray(ba?.aspected_by) ? ba.aspected_by : [];
                    const beneficPlanets: string[] = [];
                    const maleficPlanets: string[] = [];
                    if (Array.isArray(entries) && entries.length > 0) {
                      entries.forEach((e: any) => {
                        const pName = e.planet || '';
                        const detail = `${translatePlanet(pName, language)} (${e.strength || 1}x${e.type === 'special' ? spl : ''})`;
                        if (BENEFICS.includes(pName)) beneficPlanets.push(detail);
                        else maleficPlanets.push(detail);
                      });
                    } else {
                      aspectedBy.forEach((p: any) => {
                        const pName = typeof p === 'string' ? p : p.planet || '';
                        if (BENEFICS.includes(pName)) beneficPlanets.push(translatePlanet(pName, language));
                        else maleficPlanets.push(translatePlanet(pName, language));
                      });
                    }
                    return (
                      <tr key={houseNum} className="border-t border-sacred-gold hover:bg-sacred-gold/5">
                        <td className="p-1.5 text-center font-semibold text-sacred-brown">{houseNum}</td>
                        <td className="p-1.5">{beneficPlanets.length > 0 ? <span className="text-green-600">{beneficPlanets.join(', ')}</span> : <span className="text-cosmic-text">-</span>}</td>
                        <td className="p-1.5">{maleficPlanets.length > 0 ? <span className="text-red-500">{maleficPlanets.join(', ')}</span> : <span className="text-cosmic-text">-</span>}</td>
                      </tr>
                    );
                  };
                  if (Array.isArray(bhavas)) {
                    return bhavas.map((ba: any, i: number) => renderHouse(ba.house || ba.bhava || i + 1, ba));
                  }
                  return [1,2,3,4,5,6,7,8,9,10,11,12].map(h => renderHouse(h, (bhavas || {})[h] || (bhavas || {})[String(h)]));
                })()}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
