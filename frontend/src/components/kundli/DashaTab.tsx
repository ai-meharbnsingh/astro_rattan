import React from 'react';
import { Loader2, ChevronDown } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';
import GeneralRemedies from './GeneralRemedies';

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
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const hi = language === 'hi';

  if (loadingDasha || loadingExtendedDasha) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-cosmic-text">{t('kundli.calculatingDasha')}</span>
      </div>
    );
  }

  if (extendedDashaData) {
    const currentMD = extendedDashaData.mahadasha?.find((md: any) => md.is_current);
    const currentAD = currentMD?.antardasha?.find((ad: any) => ad.is_current);
    const currentPT = currentAD?.pratyantar?.find((pt: any) => pt.is_current);
    
    return (
      <div className="space-y-6">
        {/* Current Dasha Summary Table */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-display font-semibold text-sacred-brown uppercase tracking-wide text-sm">{t('section.currentDashaStatus')}</h4>
            <span className="px-2 py-0.5 bg-sacred-brown text-white text-[10px] font-bold rounded animate-pulse">● {l('LIVE', 'लाइव')}</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead className="bg-sacred-gold">
                <tr>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium uppercase">{t('kundli.mahadasha')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium uppercase">{t('kundli.antardasha')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium uppercase">{t('kundli.pratyantar')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium uppercase">{hi ? 'अवधि' : 'Period'}</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-sacred-gold bg-sacred-gold/5 font-semibold">
                  <td className="p-2 text-sacred-brown text-sm">{translatePlanet(extendedDashaData.current_dasha, language)}</td>
                  <td className="p-2 text-sacred-brown text-sm">{translatePlanet(extendedDashaData.current_antardasha, language)}</td>
                  <td className="p-2 text-sacred-brown text-sm">{translatePlanet(extendedDashaData.current_pratyantar, language)}</td>
                  <td className="p-2 text-center text-cosmic-text whitespace-nowrap">
                    {currentPT ? `${currentPT.start} — ${currentPT.end}` : currentAD ? `${currentAD.start} — ${currentAD.end}` : ''}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Full Dasha Timeline Table */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3">{hi ? 'विस्तृत दशा तालिका' : 'Detailed Dasha Timeline'}</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead className="bg-sacred-gold">
                <tr>
                  <th className="w-8"></th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'दशा स्वामी' : 'Dasha Lord'}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.start')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.end')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{t('table.years')}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-sacred-gold/30">
                {(extendedDashaData.mahadasha || []).map((md: any) => {
                  const isMdExpanded = expandedMahadasha === md.planet;
                  return (
                    <React.Fragment key={md.planet}>
                      {/* Mahadasha Row */}
                      <tr 
                        className={`cursor-pointer transition-colors ${md.is_current ? 'bg-sacred-gold-dark/10' : 'hover:bg-sacred-gold/5'}`}
                        onClick={() => setExpandedMahadasha(isMdExpanded ? null : md.planet)}
                      >
                        <td className="p-1.5 text-center">
                          <ChevronDown className={`w-3.5 h-3.5 text-sacred-gold-dark transition-transform ${isMdExpanded ? 'rotate-180' : ''}`} />
                        </td>
                        <td className="p-1.5">
                          <span className={`font-bold ${md.is_current ? 'text-sacred-gold-dark' : 'text-sacred-brown'}`}>
                            {translatePlanet(md.planet, language)} {t('kundli.mahadasha')}
                          </span>
                          {md.is_current && <span className="ml-2 text-[9px] px-1 rounded bg-sacred-gold-dark text-white font-bold uppercase">{t('common.current')}</span>}
                        </td>
                        <td className="p-1.5 text-cosmic-text font-medium">{md.start}</td>
                        <td className="p-1.5 text-cosmic-text font-medium">{md.end}</td>
                        <td className="p-1.5 text-center text-sacred-gold-dark font-bold">{md.years}</td>
                      </tr>

                      {/* Antardasha Rows */}
                      {isMdExpanded && (md.antardasha || []).map((ad: any) => {
                        const adKey = `${md.planet}-${ad.planet}`;
                        const isAdExpanded = expandedAntardasha === adKey;
                        return (
                          <React.Fragment key={adKey}>
                            <tr 
                              className={`cursor-pointer transition-colors bg-white/30 ${ad.is_current ? 'bg-sacred-gold-dark/5 border-l-2 border-l-sacred-gold-dark' : 'hover:bg-sacred-gold/10'}`}
                              onClick={(e) => { e.stopPropagation(); setExpandedAntardasha(isAdExpanded ? null : adKey); }}
                            >
                              <td className="p-1.5 text-center pl-4">
                                <ChevronDown className={`w-3 h-3 text-sacred-gold-dark transition-transform ${isAdExpanded ? 'rotate-180' : ''}`} />
                              </td>
                              <td className="p-1.5 pl-4">
                                <span className={`font-semibold ${ad.is_current ? 'text-sacred-gold-dark' : 'text-sacred-brown/80'}`}>
                                  {translatePlanet(ad.planet, language)} {t('kundli.antardasha')}
                                </span>
                                {ad.is_current && <span className="ml-2 text-[8px] px-1 rounded border border-sacred-gold-dark text-sacred-gold-dark font-bold uppercase">{t('common.current')}</span>}
                              </td>
                              <td className="p-1.5 text-cosmic-text italic opacity-80">{ad.start}</td>
                              <td className="p-1.5 text-cosmic-text italic opacity-80">{ad.end}</td>
                              <td className="p-1.5 text-center text-cosmic-text opacity-60">{(ad.years || (parseFloat(ad.duration_years) || 0).toFixed(2))}</td>
                            </tr>

                            {/* Pratyantar Rows */}
                            {isAdExpanded && (ad.pratyantar || []).map((pt: any, idx: number) => (
                              <tr 
                                key={idx}
                                className={`bg-white/60 transition-colors ${pt.is_current ? 'bg-sacred-gold-dark/5' : 'hover:bg-sacred-gold/5'}`}
                              >
                                <td className="p-1"></td>
                                <td className="p-1.5 pl-12 text-[11px]">
                                  <span className={`${pt.is_current ? 'text-sacred-gold-dark font-bold' : 'text-cosmic-text opacity-70'}`}>
                                    {translatePlanet(pt.planet, language)} {t('kundli.pratyantar')}
                                  </span>
                                  {pt.is_current && <span className="ml-1 text-sacred-gold-dark font-bold">●</span>}
                                </td>
                                <td className="p-1.5 text-[11px] text-cosmic-text opacity-60">{pt.start}</td>
                                <td className="p-1.5 text-[11px] text-cosmic-text opacity-60">{pt.end}</td>
                                <td className="p-1"></td>
                              </tr>
                            ))}
                          </React.Fragment>
                        );
                      })}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
        
        {/* General Remedies */}
        <GeneralRemedies language={language} t={t} kundliId={extendedDashaData.kundli_id} />
      </div>
    );
  }

  if (dashaData) {
    return (
      <div className="space-y-4">
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs text-cosmic-text uppercase font-bold tracking-wider">{t('section.currentMahadasha')}</p>
          </div>
          <p className="text-lg font-display font-bold text-sacred-brown">
            {translatePlanet(dashaData.current_dasha, language)} {t('kundli.mahadasha')}
          </p>
          {dashaData.current_antardasha && (
            <p className="text-sm text-sacred-gold-dark font-medium mt-1">
              {t('kundli.antardasha')}: {translatePlanet(dashaData.current_antardasha, language)}
            </p>
          )}
        </div>

        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead className="bg-sacred-gold">
                <tr>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.start')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.end')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{t('table.years')}</th>
                </tr>
              </thead>
              <tbody>
                {(dashaData.mahadasha_periods || []).map((p: any) => (
                  <tr key={p.planet} className={`border-t border-sacred-gold transition-colors ${p.planet === dashaData.current_dasha ? 'bg-sacred-gold-dark/10 font-bold' : 'hover:bg-sacred-gold/5'}`}>
                    <td className="p-1.5 text-sacred-brown font-medium">
                      {translatePlanet(p.planet, language)}
                      {p.planet === dashaData.current_dasha && <span className="ml-2 text-[9px] px-1 rounded bg-sacred-gold-dark text-white uppercase">{t('common.current')}</span>}
                    </td>
                    <td className="p-1.5 text-cosmic-text">{p.start_date}</td>
                    <td className="p-1.5 text-cosmic-text">{p.end_date}</td>
                    <td className="p-1.5 text-center text-cosmic-text font-bold">{p.years}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        {/* General Remedies */}
        <GeneralRemedies language={language} t={t} kundliId={dashaData.kundli_id} />
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <p className="text-cosmic-text mb-3 text-sm">{t('kundli.clickDashaTab')}</p>
      <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-sacred-gold/10 border border-sacred-gold text-sacred-gold-dark text-sm font-medium cursor-default">
        <ChevronDown className="w-4 h-4" />
        {t('kundli.clickDashaTab')}
      </span>
    </div>
  );
}
