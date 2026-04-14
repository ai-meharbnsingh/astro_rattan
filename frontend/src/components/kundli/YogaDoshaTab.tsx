import { Loader2, CheckCircle, Shield, AlertTriangle, Gem } from 'lucide-react';
import { translateName, translateLabel, translateRemedy, translateBackend, translatePlanet } from '@/lib/backend-translations';

interface YogaDoshaTabProps {
  yogaDoshaData: any;
  loadingYogaDosha: boolean;
  doshaDisplay?: { mangal: any; kaalsarp: any; sadesati: any } | null;
  doshaData?: any;
  loadingDosha?: boolean;
  language: string;
  t: (key: string) => string;
}

export default function YogaDoshaTab({ yogaDoshaData, loadingYogaDosha, doshaDisplay, doshaData, loadingDosha, language, t }: YogaDoshaTabProps) {
  if (loadingYogaDosha) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-cosmic-text">{t('kundli.analyzingYogasAndDoshas')}</span>
      </div>
    );
  }

  if (!yogaDoshaData) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-cosmic-text mb-3 text-sm">{t('kundli.clickYogasTab')}</p>
        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-sacred-gold/10 border border-sacred-gold text-sacred-gold-dark text-sm font-medium cursor-default">
          <CheckCircle className="w-4 h-4" />
          {t('kundli.clickYogasTab')}
        </span>
      </div>
    );
  }

  const hi = language === 'hi';

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 1. Yogas Table */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <h4 className="font-display font-semibold text-sacred-brown">{t('section.yogas')}</h4>
          </div>
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-xs">
              <thead className="bg-sacred-gold">
                <tr>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'योग का नाम' : 'Yoga Name'}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'विवरण' : 'Description'}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{hi ? 'ग्रह' : 'Planets'}</th>
                </tr>
              </thead>
              <tbody>
                {(() => {
                  const presentYogas = (yogaDoshaData.yogas || []).filter((y: any) => y.present);
                  if (presentYogas.length === 0) {
                    return <tr><td colSpan={3} className="p-4 text-center text-cosmic-text">{t('yoga.noneDetected')}</td></tr>;
                  }
                  return presentYogas.map((yoga: any, idx: number) => (
                    <tr key={idx} className="border-t border-sacred-gold hover:bg-sacred-gold/5 transition-colors">
                      <td className="p-1.5 font-semibold text-sacred-brown whitespace-nowrap">{translateName(yoga.name, language)}</td>
                      <td className="p-1.5 text-cosmic-text leading-relaxed">{translateBackend(yoga.description, language)}</td>
                      <td className="p-1.5 text-center">
                        <div className="flex flex-wrap justify-center gap-1">
                          {(yoga.planets_involved || []).map((p: string) => (
                            <span key={p} className="px-1.5 py-0.5 rounded bg-green-100 text-green-800 font-medium">
                              {translatePlanet(p, language)}
                            </span>
                          ))}
                        </div>
                      </td>
                    </tr>
                  ));
                })()}
              </tbody>
            </table>
          </div>
        </div>

        {/* 2. Doshas Table */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <Shield className="w-4 h-4 text-red-700" />
            <h4 className="font-display font-semibold text-sacred-brown">{t('section.doshas')}</h4>
          </div>
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-xs">
              <thead className="bg-sacred-gold">
                <tr>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'दोष का नाम' : 'Dosha Name'}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{hi ? 'तीव्रता' : 'Severity'}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'विवरण और उपाय' : 'Description & Remedies'}</th>
                </tr>
              </thead>
              <tbody>
                {(() => {
                  const presentDoshas = (yogaDoshaData.doshas || []).filter((d: any) => d.present);
                  if (presentDoshas.length === 0) {
                    return <tr><td colSpan={3} className="p-4 text-center text-green-600 font-medium">{t('kundli.noDoshasInChart')}</td></tr>;
                  }
                  return presentDoshas.map((dosha: any, idx: number) => (
                    <tr key={idx} className="border-t border-sacred-gold hover:bg-sacred-gold/5 transition-colors">
                      <td className="p-1.5 font-semibold text-sacred-brown whitespace-nowrap">{translateName(dosha.name, language)}</td>
                      <td className="p-1.5 text-center">
                        <span className={`px-2 py-0.5 rounded-full font-medium ${
                          dosha.severity === 'high' ? 'bg-red-100 text-red-800' : 
                          dosha.severity === 'medium' ? 'bg-amber-100 text-amber-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {translateLabel(dosha.severity, language)}
                        </span>
                      </td>
                      <td className="p-1.5">
                        <p className="text-cosmic-text mb-1.5">{translateBackend(dosha.description, language)}</p>
                        {dosha.remedies && dosha.remedies.length > 0 && (
                          <div className="bg-white/40 p-1.5 rounded border border-sacred-gold/20">
                            <p className="text-[10px] font-bold text-sacred-gold-dark uppercase mb-1">{t('section.remedies')}:</p>
                            <ul className="space-y-0.5">
                              {dosha.remedies.map((r: string, ri: number) => (
                                <li key={ri} className="flex items-start gap-1 text-[11px] text-cosmic-text">
                                  <span className="mt-1 w-1 h-1 rounded-full bg-sacred-gold shrink-0" />
                                  {translateRemedy(r, language)}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </td>
                    </tr>
                  ));
                })()}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 3. Specific Dosha Analysis Table */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-4 h-4 text-orange-600" />
            <h4 className="font-display font-semibold text-sacred-brown">{t('section.doshaAnalysis')}</h4>
          </div>
          {loadingDosha ? (
            <div className="flex items-center justify-center py-8 flex-1"><Loader2 className="w-5 h-5 animate-spin text-sacred-gold" /></div>
          ) : (
            <div className="overflow-x-auto flex-1">
              <table className="w-full text-xs">
                <thead className="bg-sacred-gold">
                  <tr>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'दोष' : 'Analysis'}</th>
                    <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{hi ? 'स्थिति' : 'Status'}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'विवरण' : 'Details'}</th>
                  </tr>
                </thead>
                <tbody>
                  {doshaDisplay ? (
                    <>
                      {/* Mangal Dosha */}
                      <tr className="border-t border-sacred-gold hover:bg-sacred-gold/5 transition-colors">
                        <td className="p-1.5 font-semibold text-sacred-brown whitespace-nowrap">{translateName('Mangal Dosha', language)}</td>
                        <td className="p-1.5 text-center">
                          <span className={`px-2 py-0.5 rounded-full font-medium ${doshaDisplay.mangal.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaDisplay.mangal.has_dosha ? (hi ? 'उपस्थित' : 'Present') : (hi ? 'नहीं है' : 'Absent')}
                          </span>
                        </td>
                        <td className="p-1.5 text-cosmic-text">{translateBackend(doshaDisplay.mangal.description, language)}</td>
                      </tr>
                      {/* Kaal Sarp */}
                      <tr className="border-t border-sacred-gold hover:bg-sacred-gold/5 transition-colors">
                        <td className="p-1.5 font-semibold text-sacred-brown whitespace-nowrap">{translateName('Kaal Sarp Dosha', language)}</td>
                        <td className="p-1.5 text-center">
                          <span className={`px-2 py-0.5 rounded-full font-medium ${doshaDisplay.kaalsarp.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaDisplay.kaalsarp.has_dosha ? (hi ? 'उपस्थित' : 'Present') : (hi ? 'नहीं है' : 'Absent')}
                          </span>
                        </td>
                        <td className="p-1.5 text-cosmic-text">{translateBackend(doshaDisplay.kaalsarp.description, language)}</td>
                      </tr>
                      {/* Sade Sati */}
                      <tr className="border-t border-sacred-gold hover:bg-sacred-gold/5 transition-colors">
                        <td className="p-1.5 font-semibold text-sacred-brown whitespace-nowrap">{translateName('Sade Sati', language)}</td>
                        <td className="p-1.5 text-center">
                          <span className={`px-2 py-0.5 rounded-full font-medium ${doshaDisplay.sadesati.has_sade_sati ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-800'}`}>
                            {doshaDisplay.sadesati.has_sade_sati ? (hi ? 'सक्रिय' : 'Active') : (hi ? 'नहीं है' : 'Inactive')}
                          </span>
                        </td>
                        <td className="p-1.5 text-cosmic-text">
                          {doshaDisplay.sadesati.has_sade_sati && <span className="font-bold text-orange-700">[{translateLabel(doshaDisplay.sadesati.phase, language)}] </span>}
                          {translateBackend(doshaDisplay.sadesati.description, language)}
                        </td>
                      </tr>
                    </>
                  ) : (
                    <tr><td colSpan={3} className="p-4 text-center text-cosmic-text">{t('common.noData')}</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* 4. Gemstones Table */}
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <Gem className="w-4 h-4 text-sacred-gold-dark" />
            <h4 className="font-display font-semibold text-sacred-brown">{t('section.remediesGemstone')}</h4>
          </div>
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-xs">
              <thead className="bg-sacred-gold">
                <tr>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'रत्न' : 'Gemstone'}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{hi ? 'ग्रह' : 'Planet'}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{hi ? 'विवरण और धारण विधि' : 'Reason & wearing'}</th>
                </tr>
              </thead>
              <tbody>
                {(() => {
                  const gems = doshaData?.gemstone_recommendations || [];
                  if (gems.length === 0) {
                    return <tr><td colSpan={3} className="p-4 text-center text-cosmic-text">{t('common.noData')}</td></tr>;
                  }
                  return gems.map((gem: any, idx: number) => (
                    <tr key={idx} className="border-t border-sacred-gold hover:bg-sacred-gold/5 transition-colors">
                      <td className="p-1.5">
                        <p className="font-semibold text-sacred-brown whitespace-nowrap">{hi && gem.gemstone_hi ? gem.gemstone_hi : gem.gemstone}</p>
                        <span className={`text-[10px] px-1.5 py-0.5 rounded uppercase font-bold ${gem.priority === 'primary' ? 'bg-sacred-gold-dark text-white' : 'bg-sacred-gold/20 text-sacred-gold-dark'}`}>
                          {gem.priority === 'primary' ? (hi ? 'प्राथमिक' : 'Primary') : (hi ? 'द्वितीयक' : 'Secondary')}
                        </span>
                      </td>
                      <td className="p-1.5 text-center font-medium">{translatePlanet(gem.planet, language)}</td>
                      <td className="p-1.5">
                        <p className="text-cosmic-text mb-1.5 leading-relaxed">{translateBackend(gem.reason, language)}</p>
                        <div className="flex flex-wrap gap-2 text-[10px] text-sacred-gold-dark font-bold">
                          {gem.metal && <span className="bg-white/50 px-1.5 py-0.5 rounded border border-sacred-gold/10 whitespace-nowrap">{hi ? 'धातु' : 'Metal'}: {translateBackend(gem.metal, language)}</span>}
                          {gem.finger && <span className="bg-white/50 px-1.5 py-0.5 rounded border border-sacred-gold/10 whitespace-nowrap">{hi ? 'उंगली' : 'Finger'}: {translateBackend(gem.finger, language)}</span>}
                          {gem.day && <span className="bg-white/50 px-1.5 py-0.5 rounded border border-sacred-gold/10 whitespace-nowrap">{hi ? 'दिन' : 'Day'}: {translateBackend(gem.day, language)}</span>}
                        </div>
                      </td>
                    </tr>
                  ));
                })()}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
