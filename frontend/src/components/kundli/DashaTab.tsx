import { Loader2, ChevronDown } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';

interface DashaTabProps {
  dashaData: any;
  extendedDashaData: any;
  loadingDasha: boolean;
  loadingExtendedDasha: boolean;
  expandedMahadasha: string | null;
  setExpandedMahadasha: (v: string | null) => void;
  expandedAntardasha: string | null;
  setExpandedAntardasha: (v: string | null) => void;
  language: string;
  t: (key: string) => string;
}

export default function DashaTab({
  dashaData, extendedDashaData, loadingDasha, loadingExtendedDasha,
  expandedMahadasha, setExpandedMahadasha, expandedAntardasha, setExpandedAntardasha,
  language, t,
}: DashaTabProps) {
  if (loadingDasha || loadingExtendedDasha) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.calculatingDasha')}</span></div>
    );
  }

  if (extendedDashaData) {
    return (
      <div className="space-y-4">
        <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold rounded-xl p-4 border border-sacred-gold">
          <p className="text-sm text-gray-600">{t('section.currentMahadasha')}</p>
          <p className="text-xl font-display font-bold text-gray-900">{translatePlanet(extendedDashaData.current_dasha, language)} {t('kundli.mahadasha')}</p>
          <div className="flex gap-4 mt-1">
            {extendedDashaData.current_antardasha && extendedDashaData.current_antardasha !== 'Unknown' && (
              <p className="text-sm text-sacred-gold-dark">{t('kundli.antardasha')}: {translatePlanet(extendedDashaData.current_antardasha, language)}</p>
            )}
            {extendedDashaData.current_pratyantar && extendedDashaData.current_pratyantar !== 'Unknown' && (
              <p className="text-sm text-cosmic-text">{t('kundli.pratyantar')}: {translatePlanet(extendedDashaData.current_pratyantar, language)}</p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          {(extendedDashaData.mahadasha || []).map((md: any) => (
            <div key={md.planet} className={`rounded-xl border overflow-hidden ${md.is_current ? 'border-sacred-gold-dark' : 'border-sacred-gold'}`}>
              <button
                onClick={() => setExpandedMahadasha(expandedMahadasha === md.planet ? null : md.planet)}
                className={`w-full flex items-center justify-between p-4 transition-colors ${md.is_current ? 'bg-sacred-gold-dark' : 'bg-sacred-cream hover:bg-sacred-gold/5'}`}
              >
                <div className="flex items-center gap-3">
                  <ChevronDown className={`w-4 h-4 text-sacred-gold-dark transition-transform ${expandedMahadasha === md.planet ? 'rotate-180' : ''}`} />
                  <span className={`font-display font-semibold ${md.is_current ? 'text-sacred-gold-dark' : 'text-sacred-brown'}`}>
                    {translatePlanet(md.planet, language)} {t('kundli.mahadasha')}
                  </span>
                  {md.is_current && <span className="text-sm px-2 py-0.5 rounded-full bg-sacred-cream text-sacred-brown font-medium">{t('common.current')}</span>}
                </div>
                <div className="text-right text-sm text-cosmic-text">
                  <span>{md.start} {'\u2014'} {md.end}</span>
                  <span className="ml-2 text-sacred-gold-dark">({md.years}y)</span>
                </div>
              </button>

              {expandedMahadasha === md.planet && (
                <div className="border-t border-sacred-gold">
                  {(md.antardasha || []).map((ad: any) => (
                    <div key={`${md.planet}-${ad.planet}`}>
                      <button
                        onClick={() => setExpandedAntardasha(expandedAntardasha === `${md.planet}-${ad.planet}` ? null : `${md.planet}-${ad.planet}`)}
                        className={`w-full flex items-center justify-between px-6 py-3 text-sm transition-colors ${ad.is_current ? 'bg-sacred-gold-dark' : 'hover:bg-sacred-gold/5'}`}
                      >
                        <div className="flex items-center gap-2">
                          {ad.pratyantar && ad.pratyantar.length > 0 && (
                            <ChevronDown className={`w-3 h-3 text-sacred-gold-dark transition-transform ${expandedAntardasha === `${md.planet}-${ad.planet}` ? 'rotate-180' : ''}`} />
                          )}
                          <span className={`font-medium ${ad.is_current ? 'text-sacred-gold-dark' : 'text-sacred-brown'}`}>
                            {translatePlanet(ad.planet, language)} {t('kundli.antardasha')}
                          </span>
                          {ad.is_current && <span className="text-sm px-1.5 py-0.5 rounded-full bg-sacred-cream text-sacred-brown">{t('common.current')}</span>}
                        </div>
                        <span className="text-cosmic-text">{ad.start} {'\u2014'} {ad.end}</span>
                      </button>

                      {expandedAntardasha === `${md.planet}-${ad.planet}` && ad.pratyantar && ad.pratyantar.length > 0 && (
                        <div className="bg-sacred-cream border-t border-sacred-gold">
                          {ad.pratyantar.map((pt: any, idx: number) => (
                            <div
                              key={idx}
                              className={`flex items-center justify-between px-10 py-2 text-sm ${pt.is_current ? 'bg-sacred-gold-dark' : ''}`}
                            >
                              <span className={`${pt.is_current ? 'text-sacred-gold-dark font-semibold' : 'text-cosmic-text'}`}>
                                {translatePlanet(pt.planet, language)} {t('kundli.pratyantar')}
                                {pt.is_current && <span className="ml-1 text-sacred-gold-dark">*</span>}
                              </span>
                              <span className="text-cosmic-text">{pt.start} {'\u2014'} {pt.end}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (dashaData) {
    return (
      <div className="space-y-4">
        <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold rounded-xl p-4 border border-sacred-gold">
          <p className="text-sm text-gray-600">{t('section.currentMahadasha')}</p>
          <p className="text-xl font-display font-bold text-gray-900">{translatePlanet(dashaData.current_dasha, language)} {t('kundli.mahadasha')}</p>
          {dashaData.current_antardasha && <p className="text-sm text-sacred-gold-dark">{t('kundli.antardasha')}: {translatePlanet(dashaData.current_antardasha, language)}</p>}
        </div>
        <div className="rounded-xl border border-sacred-gold overflow-x-auto">
          <table className="w-full">
            <thead className="bg-sacred-cream">
              <tr>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.planet')}</th>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.start')}</th>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.end')}</th>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.years')}</th>
              </tr>
            </thead>
            <tbody>
              {(dashaData.mahadasha_periods || []).map((p: any) => (
                <tr key={p.planet} className={`border-t border-sacred-gold ${p.planet === dashaData.current_dasha ? 'bg-sacred-gold font-semibold' : ''}`}>
                  <td className="p-3 text-sacred-brown">{translatePlanet(p.planet, language)} {p.planet === dashaData.current_dasha ? '\u2190' : ''}</td>
                  <td className="p-3 text-cosmic-text text-sm">{p.start_date}</td>
                  <td className="p-3 text-cosmic-text text-sm">{p.end_date}</td>
                  <td className="p-3 text-cosmic-text text-sm">{p.years}y</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <p className="text-cosmic-text mb-3 text-sm">Dasha periods have not been loaded yet.</p>
      <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-sacred-gold/10 border border-sacred-gold text-sacred-gold-dark text-sm font-medium cursor-default">
        <ChevronDown className="w-4 h-4" />
        Click the Dasha tab above to load analysis
      </span>
    </div>
  );
}
