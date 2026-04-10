import { Loader2, Shield, Gem } from 'lucide-react';
import { translatePlanet, translateRemedy, translateSign, translateBackend } from '@/lib/backend-translations';

interface SadesatiTabProps {
  sadesatiData: any;
  loadingSadesati: boolean;
  doshaData: any;
  language: string;
  t: (key: string) => string;
}

export default function SadesatiTab(props: SadesatiTabProps) {
  const { sadesatiData, loadingSadesati, doshaData, language, t } = props;

  return (
            <div className="space-y-6">
              {loadingSadesati ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.loadingSadeSati')}</span></div>
              ) : sadesatiData ? (
                <div className="space-y-6">
                  {/* Introduction Card */}
                  <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/30">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-10 h-10 rounded-full bg-sacred-gold/20 flex items-center justify-center">
                        <span className="text-xl">♄</span>
                      </div>
                      <div>
                        <h3 className="font-display font-bold text-lg text-sacred-brown">{t('sadeSati.analysisTitle')}</h3>
                        <p className="text-sm text-gray-600">{t('sadeSati.birthMoonSign')}: <span className="text-sacred-gold-dark font-semibold">{translateSign(sadesatiData.moon_sign, language)}</span></p>
                      </div>
                    </div>
                    <p className="text-sm leading-relaxed text-gray-700">
                      {translateBackend(sadesatiData.explanation?.sadesati, language) || t('sadeSati.sadesatiExplanation')}
                    </p>
                    <p className="text-sm mt-2 leading-relaxed text-gray-700">
                      {translateBackend(sadesatiData.explanation?.dhayya, language) || t('sadeSati.dhayyaExplanation')}
                    </p>
                  </div>

                  {/* Sade Sati Cycles */}
                  {sadesatiData.cycles && sadesatiData.cycles.length > 0 && (
                    <div className="space-y-4">
                      <h4 className="font-display font-semibold text-sacred-brown flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-gold-hex"></span>
                        {t('sadeSati.cyclesTitle')}
                      </h4>

                      {sadesatiData.cycles.map((cycle: any, idx: number) => (
                        <div key={idx} className="bg-sacred-cream rounded-xl border border-sacred-gold overflow-hidden">
                          {/* Cycle Header */}
                          <div className={`p-4 ${cycle.severity === 'high' ? 'bg-red-50' : cycle.severity === 'extreme' ? 'bg-red-100' : 'bg-sacred-gold/10'}`}>
                            <div className="flex items-center justify-between">
                              <h5 className="font-display font-semibold text-sacred-brown">{translateBackend(cycle.title, language)}</h5>
                              <span className={`text-sm px-2 py-1 rounded-full font-medium ${
                                cycle.severity === 'extreme' ? 'bg-red-500/20 text-red-700' :
                                cycle.severity === 'high' ? 'bg-orange-500/20 text-orange-700' :
                                'bg-yellow-500/20 text-yellow-700'
                              }`}>
                                {cycle.severity === 'extreme' ? t('sadeSati.extremeImpact') : cycle.severity === 'high' ? t('sadeSati.intenseImpact') : t('sadeSati.moderateImpact')}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600 mt-1">
                              {cycle.start_date} to {cycle.end_date}
                            </p>
                            <p className="text-sm mt-2 text-gray-700">{translateBackend(cycle.description, language)}</p>
                          </div>

                          {/* Cycle Phases Table */}
                          {cycle.phases && cycle.phases.length > 0 && (
                            <div className="p-4 overflow-x-auto">
                              <table className="w-full text-sm">
                                <thead>
                                  <tr className="border-b border-sacred-gold">
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.dhayya')}</th>
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.transitSign')}</th>
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.startDate')}</th>
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.endDate')}</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {cycle.phases.map((phase: any, pidx: number) => {
                                    const phaseNames: Record<string, string> = {
                                      'first_dhayya': t('sadeSati.firstDhayya'),
                                      'second_dhayya': t('sadeSati.secondDhayya'),
                                      'third_dhayya': t('sadeSati.thirdDhayya')
                                    };
                                    return (
                                      <tr key={pidx} className="border-t border-sacred-gold hover:bg-sacred-gold/10">
                                        <td className="p-2">
                                          <span className="text-sacred-brown font-medium">{phaseNames[phase.phase_key] || phase.sub_phase}</span>
                                        </td>
                                        <td className="p-2 text-cosmic-text">{translateSign(phase.sign_name, language)}</td>
                                        <td className="p-2 text-cosmic-text">{phase.start_date}</td>
                                        <td className="p-2 text-cosmic-text">{phase.end_date}</td>
                                      </tr>
                                    );
                                  })}
                                </tbody>
                              </table>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Other Phases (Dhaiya, Panauti, Kantaka) */}
                  {sadesatiData.other_phases && sadesatiData.other_phases.length > 0 && (
                    <div className="space-y-4">
                      <h4 className="font-display font-semibold text-sacred-brown flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-[#8B2332]"></span>
                        {t('sadeSati.otherTransits')}
                      </h4>

                      <div className="bg-sacred-cream rounded-xl border border-sacred-gold overflow-hidden">
                        <div className="p-4 overflow-x-auto">
                          <table className="w-full text-sm">
                            <thead>
                              <tr className="border-b border-sacred-gold">
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.type')}</th>
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.details')}</th>
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.sign')}</th>
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.period')}</th>
                              </tr>
                            </thead>
                            <tbody>
                              {sadesatiData.other_phases.map((phase: any, idx: number) => (
                                <tr key={idx} className="border-t border-sacred-gold hover:bg-sacred-gold/10">
                                  <td className="p-2">
                                    <span className={`inline-block px-2 py-0.5 rounded text-sm font-medium ${
                                      phase.phase === 'Panauti' ? 'bg-red-500/20 text-red-700' :
                                      phase.phase === 'Dhaiya' ? 'bg-orange-500/20 text-orange-700' :
                                      'bg-blue-500/20 text-blue-700'
                                    }`}>
                                      {translateBackend(phase.phase, language)}
                                    </span>
                                  </td>
                                  <td className="p-2 text-sacred-brown">{translateBackend(phase.sub_phase, language)}</td>
                                  <td className="p-2 text-cosmic-text">{translateSign(phase.sign_name, language)}</td>
                                  <td className="p-2 text-cosmic-text text-sm">
                                    {phase.start_date} to {phase.end_date}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Phase Effects Details */}
                  <div className="space-y-4">
                    <h4 className="font-display font-semibold text-sacred-brown flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-gold-hex"></span>
                      {t('sadeSati.detailedEffects')}
                    </h4>

                    {[
                      { key: 'first_dhayya', title: t('sadeSati.firstDhayyaEffectsTitle'), effects: language === 'hi' ? 
                        ["मानसिक और शारीरिक सुख में गिरावट", "आंखों की बीमारी की संभावना", "वित्तीय हानि और अनावश्यक व्यय", "परिवार से अलगाव", "पिता को बीमारी हो सकती है", "आध्यात्मिकता में रुचि बढ़ती है", "दुर्घटना का भय; व्यर्थ घूमना"] :
                        ["Fall in mental and physical happiness", "Possibility of eye ailments", "Financial losses and unwanted expenditure", "Separation from family", "Father may suffer ailments", "Interest in spiritualism increases", "Fear of accidents; may wander uselessly"] },
                      { key: 'second_dhayya', title: t('sadeSati.secondDhayyaEffectsTitle'), effects: language === 'hi' ? 
                        ["शरीर के मध्य भाग में रोग", "शारीरिक ऊर्जा प्रभावित", "भाइयों और भागीदारों के साथ विवाद", "वित्तीय समस्याएं बनी रहती हैं", "गलत निर्णय लिए जा सकते हैं", "पारिवारिक और व्यावसायिक जीवन अस्थिर", "शत्रु नुकसान पहुंचा सकते हैं; प्रियजनों से अलगाव"] :
                        ["Ailments in middle part of body", "Physical energy affected", "Disputes with brothers and partners", "Financial problems persist", "Wrong decisions may be taken", "Family and business life unstable", "Enemies may inflict harm; separation from near ones"] },
                      { key: 'third_dhayya', title: t('sadeSati.thirdDhayyaEffectsTitle'), effects: language === 'hi' ? 
                        ["पैरों में रोग हो सकते हैं", "शारीरिक कमजोरी और आलस्य", "सुख में बाधाएं", "व्यय में वृद्धि", "रिश्तेदारों के साथ विवाद", "घरेलू सुख में बाधाएं", "नीच लोग परेशानी देते हैं"] :
                        ["Legs may suffer from ailments", "Physical weakness and laziness", "Happiness faces hurdles", "Expenses increase", "Conflicts with relatives", "Domestic happiness obstacles", "Lowly people give troubles"] },
                      { key: 'kantak_4th', title: t('sadeSati.kantaka4thEffectsTitle'), effects: language === 'hi' ? 
                        ["स्थान परिवर्तन या तबादला", "आवास समस्याएं", "हृदय रोग हो सकते हैं", "रक्तचाप अस्थिरता", "जनता/सरकार का विरोध", "कार्य क्षेत्र में बाधाएं", "शनि की दृष्टि से मानसिक भय"] :
                        ["Change of place or transfer", "Housing problems", "Heart problems may occur", "Blood pressure instability", "Opposition from public/government", "Obstacles in work sphere", "Mental fear due to Saturn's aspect"] },
                      { key: 'kantak_7th', title: t('sadeSati.kantaka7thEffectsTitle'), effects: language === 'hi' ? 
                        ["जीवन साथी को बीमारी हो सकती है", "मानसिक चिंता बढ़ती है", "भाग्य में बाधाएं", "पिता को कष्ट हो सकता है", "माता के स्वास्थ्य को कष्ट", "वाहन संबंधी समस्याएं", "यात्रा में कठिनाइयां"] :
                        ["Spouse may suffer ailments", "Mental anxiety increases", "Obstacles in fortune", "Father may suffer", "Mother's health may suffer", "Vehicle related problems", "Hardships in travelling"] },
                      { key: 'ashtam_8th', title: t('sadeSati.ashtam8thEffectsTitle'), effects: language === 'hi' ? 
                        ["दीर्घकालिक रोग और दुर्घटनाएं", "अपमानित होने का भय", "कार्य क्षेत्र में परिवर्तन", "धन में कमी आ सकती है", "बच्चों को कष्ट हो सकता है", "सबसे चुनौतीपूर्ण अवधि", "बच्चों से अलगाव की संभावना"] :
                        ["Long term ailments and accidents", "Fear of being insulted", "Change in work-sphere", "Wealth may diminish", "Children may suffer", "Most challenging period", "Possibilities of separation from children"] }
                    ].map((phase) => (
                      <div key={phase.key} className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                        <h5 className="font-display font-semibold text-sacred-brown mb-2">{phase.title}</h5>
                        <ul className="space-y-1">
                          {phase.effects.map((effect: string, idx: number) => (
                            <li key={idx} className="text-sm text-cosmic-text flex items-start gap-2">
                              <span className="mt-1.5 w-1 h-1 rounded-full bg-gold-hex flex-shrink-0"></span>
                              {effect}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>

                  {/* Detailed Remedies Section */}
                  {sadesatiData.detailed_remedies && (
                    <div className="space-y-4">
                      <h4 className="font-display font-semibold text-sacred-brown flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-green-500"></span>
                        {t('sadeSati.remediesTitle')}
                      </h4>

                      {/* Mantra Remedies */}
                      {sadesatiData.detailed_remedies.mantra && (
                        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                          <h5 className="font-display font-semibold text-sacred-brown mb-3">{translateBackend(sadesatiData.detailed_remedies.mantra.title, language)}</h5>
                          <div className="space-y-3">
                            {sadesatiData.detailed_remedies.mantra.items.map((item: any, idx: number) => (
                              <div key={idx} className="bg-white rounded-lg p-3">
                                <p className="font-medium text-sacred-brown text-sm">{item.name}</p>
                                {item.text && <p className="text-sm text-gold-hex font-serif my-1">{item.text}</p>}
                                <p className="text-sm text-cosmic-text">{item.instruction}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Other Remedies */}
                      {['stotra', 'vrat', 'donation', 'gemstones', 'other'].map((category) => {
                        const data = sadesatiData.detailed_remedies[category];
                        if (!data) return null;
                        return (
                          <div key={category} className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                            <h5 className="font-display font-semibold text-sacred-brown mb-3">{translateBackend(data.title, language)}</h5>
                            <ul className="space-y-1">
                              {(data.items || []).map((item: any, idx: number) => (
                                <li key={idx} className="text-sm text-cosmic-text flex items-start gap-2">
                                  <span className="mt-1.5 w-1 h-1 rounded-full bg-gold-hex flex-shrink-0"></span>
                                  {typeof item === 'string' ? translateBackend(item, language) : translateBackend(item.name, language) || translateBackend(item.instruction, language)}
                                </li>
                              ))}
                            </ul>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Fallback General Remedies */}
                  {(!sadesatiData.detailed_remedies) && sadesatiData.remedies && (
                    <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                      <h4 className="font-display font-semibold text-sacred-brown mb-3">Remedies</h4>
                      <ul className="space-y-2">
                        {sadesatiData.remedies.map((remedy: string, idx: number) => (
                          <li key={idx} className="text-sm text-cosmic-text flex items-start gap-2">
                            <Shield className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />
                            <span>{translateRemedy(remedy, language)}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                </div>
              ) : (
                <p className="text-center text-cosmic-text py-8">{t('kundli.clickSadeSatiTab')}</p>
              )}
            </div>
  );
}
