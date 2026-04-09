import { Loader2, Shield, Gem } from 'lucide-react';
import { translatePlanet, translateRemedy } from '@/lib/backend-translations';

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
                  <div className="bg-gradient-to-r from-dark to-dark-secondary rounded-xl p-5 border border-gold-30">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-10 h-10 rounded-full bg-gold-20 flex items-center justify-center">
                        <span className="text-xl">♄</span>
                      </div>
                      <div>
                        <h3 className="font-display font-bold text-lg text-cream">{language === 'hi' ? 'शनि साढ़े साती विश्लेषण' : 'Shani Sade Sati Analysis'}</h3>
                        <p className="text-sm text-warm">{language === 'hi' ? 'जन्म चंद्र राशि' : 'Birth Moon Sign'}: <span className="text-gold-hex font-semibold">{sadesatiData.moon_sign}</span></p>
                      </div>
                    </div>
                    <p className="text-sm leading-relaxed text-warm">
                      {sadesatiData.explanation?.sadesati || (language === 'hi' ? "साढ़े सात वर्ष की अवधि जिसमें शनि जन्म राशि (चंद्र राशि) से बारहवें, प्रथम और द्वितीय भाव में गोचर करता है, शनि की साढ़ेसाती कहलाती है।" : "The seven and a half year period during which Saturn transits in the twelfth, first and second houses from the birth rashi (Moon sign) is called the Sadhesati of Saturn.")}
                    </p>
                    <p className="text-sm mt-2 leading-relaxed text-warm">
                      {sadesatiData.explanation?.dhayya || (language === 'hi' ? "एक साढ़ेसाती लगभग ढाई वर्ष की तीन अवधियों से बनी होती है, क्योंकि शनि एक राशि में ढाई वर्ष गोचर करता है।" : "One Sadhesati is made up of three periods of approximately two and a half years each, because Saturn travels in one rashi for two and a half years.")}
                    </p>
                  </div>

                  {/* Sade Sati Cycles */}
                  {sadesatiData.cycles && sadesatiData.cycles.length > 0 && (
                    <div className="space-y-4">
                      <h4 className="font-display font-semibold text-sacred-brown flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-gold-hex"></span>
                        {language === 'hi' ? 'साढ़ेसाती चक्र (सामान्यतः जीवन में 3)' : 'Sade Sati Cycles (Normally 3 in a lifetime)'}
                      </h4>

                      {sadesatiData.cycles.map((cycle: any, idx: number) => (
                        <div key={idx} className="bg-sacred-cream rounded-xl border border-sacred-gold overflow-hidden">
                          {/* Cycle Header */}
                          <div className={`p-4 ${cycle.severity === 'high' ? 'bg-red-10' : cycle.severity === 'extreme' ? 'bg-red-20' : 'bg-sacred-gold'}`}>
                            <div className="flex items-center justify-between">
                              <h5 className="font-display font-semibold text-sacred-brown">{cycle.title}</h5>
                              <span className={`text-sm px-2 py-1 rounded-full font-medium ${
                                cycle.severity === 'extreme' ? 'bg-red-30 text-wax-red-light' :
                                cycle.severity === 'high' ? 'bg-orange-500 text-orange-400' :
                                'bg-yellow-500 text-yellow-600'
                              }`}>
                                {cycle.severity === 'extreme' ? (language === 'hi' ? 'अत्यधिक' : 'Extreme') : cycle.severity === 'high' ? (language === 'hi' ? 'तीव्र' : 'Intense') : (language === 'hi' ? 'मध्यम' : 'Moderate')} {language === 'hi' ? 'प्रभाव' : 'Impact'}
                              </span>
                            </div>
                            <p className="text-sm text-cosmic-text mt-1">
                              {cycle.start_date} to {cycle.end_date}
                            </p>
                            <p className="text-sm mt-2 text-warm">{cycle.description}</p>
                          </div>

                          {/* Cycle Phases Table */}
                          {cycle.phases && cycle.phases.length > 0 && (
                            <div className="p-4">
                              <table className="w-full text-sm">
                                <thead>
                                  <tr className="border-b border-sacred-gold">
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">Dhayya</th>
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">Transit Sign</th>
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">Start Date</th>
                                    <th className="text-left p-2 text-sacred-gold-dark font-medium">End Date</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {cycle.phases.map((phase: any, pidx: number) => {
                                    const phaseNames: Record<string, string> = {
                                      'first_dhayya': 'First Dhayya (Rising)',
                                      'second_dhayya': 'Second Dhayya (Peak)',
                                      'third_dhayya': 'Third Dhayya (Setting)'
                                    };
                                    return (
                                      <tr key={pidx} className="border-t border-sacred-gold hover:bg-sacred-gold">
                                        <td className="p-2">
                                          <span className="text-sacred-brown font-medium">{phaseNames[phase.phase_key] || phase.sub_phase}</span>
                                        </td>
                                        <td className="p-2 text-cosmic-text">{phase.sign_name}</td>
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
                        Other Saturn Transits (Dhaiya, Panauti, Kantaka)
                      </h4>

                      <div className="bg-sacred-cream rounded-xl border border-sacred-gold overflow-hidden">
                        <div className="p-4">
                          <table className="w-full text-sm">
                            <thead>
                              <tr className="border-b border-sacred-gold">
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">Type</th>
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">Details</th>
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">Sign</th>
                                <th className="text-left p-2 text-sacred-gold-dark font-medium">Period</th>
                              </tr>
                            </thead>
                            <tbody>
                              {sadesatiData.other_phases.map((phase: any, idx: number) => (
                                <tr key={idx} className="border-t border-sacred-gold hover:bg-sacred-gold">
                                  <td className="p-2">
                                    <span className={`inline-block px-2 py-0.5 rounded text-sm font-medium ${
                                      phase.phase === 'Panauti' ? 'bg-[#8B2332] text-wax-red-light' :
                                      phase.phase === 'Dhaiya' ? 'bg-orange-500 text-orange-400' :
                                      'bg-blue-500 text-blue-400'
                                    }`}>
                                      {phase.phase}
                                    </span>
                                  </td>
                                  <td className="p-2 text-sacred-brown">{phase.sub_phase}</td>
                                  <td className="p-2 text-cosmic-text">{phase.sign_name}</td>
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
                      Detailed Effects of Each Phase
                    </h4>

                    {[
                      { key: 'first_dhayya', title: "First Dhayya (Rising) - 12th from Moon", effects: ["Fall in mental and physical happiness", "Possibility of eye ailments", "Financial losses and unwanted expenditure", "Separation from family", "Father may suffer ailments", "Interest in spiritualism increases", "Fear of accidents; may wander uselessly"] },
                      { key: 'second_dhayya', title: "Second Dhayya (Peak) - Over Moon Sign", effects: ["Ailments in middle part of body", "Physical energy affected", "Disputes with brothers and partners", "Financial problems persist", "Wrong decisions may be taken", "Family and business life unstable", "Enemies may inflict harm; separation from near ones"] },
                      { key: 'third_dhayya', title: "Third Dhayya (Setting) - 2nd from Moon", effects: ["Legs may suffer from ailments", "Physical weakness and laziness", "Happiness faces hurdles", "Expenses increase", "Conflicts with relatives", "Domestic happiness obstacles", "Lowly people give troubles"] },
                      { key: 'kantak_4th', title: "Kantaka Saturn - 4th House", effects: ["Change of place or transfer", "Housing problems", "Heart problems may occur", "Blood pressure instability", "Opposition from public/government", "Obstacles in work sphere", "Mental fear due to Saturn's aspect"] },
                      { key: 'kantak_7th', title: "Kantaka Saturn - 7th House", effects: ["Spouse may suffer ailments", "Mental anxiety increases", "Obstacles in fortune", "Father may suffer", "Mother's health may suffer", "Vehicle related problems", "Hardships in travelling"] },
                      { key: 'ashtam_8th', title: "Ashtam Shani (Panauti) - 8th House", effects: ["Long term ailments and accidents", "Fear of being insulted", "Change in work-sphere", "Wealth may diminish", "Children may suffer", "Most challenging period", "Possibilities of separation from children"] }
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
                        Remedies for Sade Sati
                      </h4>

                      {/* Mantra Remedies */}
                      {sadesatiData.detailed_remedies.mantra && (
                        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                          <h5 className="font-display font-semibold text-sacred-brown mb-3">{sadesatiData.detailed_remedies.mantra.title}</h5>
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
                            <h5 className="font-display font-semibold text-sacred-brown mb-3">{data.title}</h5>
                            <ul className="space-y-1">
                              {(data.items || []).map((item: any, idx: number) => (
                                <li key={idx} className="text-sm text-cosmic-text flex items-start gap-2">
                                  <span className="mt-1.5 w-1 h-1 rounded-full bg-gold-hex flex-shrink-0"></span>
                                  {typeof item === 'string' ? item : item.name || item.instruction}
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
