import { Loader2, Star, Crown, Eye, Clock, Wallet } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateBackend } from '@/lib/backend-translations';

interface JaiminiTabProps {
  data: any;
  loading: boolean;
}

export default function JaiminiTab({ data, loading }: JaiminiTabProps) {
  const { t, language } = useTranslation();

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-sacred-text-secondary">{t('common.loading')}</span>
      </div>
    );
  }

  if (!data) {
    return <p className="text-center text-sacred-text-secondary py-8">{t('common.noData')}</p>;
  }

  return (
    <div className="space-y-6">
      {/* Chara Karakas */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
          <Crown className="w-5 h-5 text-sacred-gold" />
          {language === 'hi' ? 'चर कारक (7 परिवर्तनशील कारक)' : 'Chara Karakas (7 Variable Significators)'}
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-slate-100">
                <th className="text-left p-2 font-medium text-slate-600">#</th>
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'कारक' : 'Karaka'}</th>
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'ग्रह' : 'Planet'}</th>
                <th className="text-center p-2 font-medium text-slate-600">{language === 'hi' ? 'अंश' : 'Degree'}</th>
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'अर्थ' : 'Significance'}</th>
              </tr>
            </thead>
            <tbody>
              {(data.chara_karakas || []).map((k: any, i: number) => (
                <tr key={k.karaka} className={`border-b border-slate-100 ${i === 0 ? 'bg-amber-50' : ''}`}>
                  <td className="p-2 text-slate-400">{i + 1}</td>
                  <td className="p-2 font-semibold" style={{ color: i === 0 ? '#92400e' : 'var(--ink)' }}>
                    {k.karaka} — {language === 'hi' ? k.name_hi : k.name_en}
                  </td>
                  <td className="p-2 font-semibold">{translatePlanet(k.planet, language)}</td>
                  <td className="p-2 text-center font-mono">{k.degree}°</td>
                  <td className="p-2 text-xs text-slate-500">{translateBackend(k.significance, language)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Special Lagnas */}
      {data.special_lagnas && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            {
              key: 'arudha_lagna',
              icon: <Star className="w-5 h-5 text-sacred-gold" />,
              title_en: 'Arudha Lagna (AL)',
              title_hi: 'आरूढ़ लग्न',
              desc_en: 'How the world perceives you',
              desc_hi: 'संसार आपको कैसे देखता है',
            },
            {
              key: 'upapada_lagna',
              icon: <Eye className="w-5 h-5 text-sacred-gold" />,
              title_en: 'Upapada Lagna (UL)',
              title_hi: 'उपपद लग्न',
              desc_en: 'Marriage & spouse indicator',
              desc_hi: 'विवाह और जीवनसाथी सूचक',
            },
            {
              key: 'karakamsha',
              icon: <Crown className="w-5 h-5 text-sacred-gold" />,
              title_en: 'Karakamsha',
              title_hi: 'कारकांश',
              desc_en: `Soul's journey (AK in D9)`,
              desc_hi: `आत्मा की यात्रा (AK नवांश में)`,
            },
            {
              key: 'hora_lagna',
              icon: <Wallet className="w-5 h-5 text-sacred-gold" />,
              title_en: 'Hora Lagna',
              title_hi: 'होरा लग्न',
              desc_en: 'Wealth & financial status',
              desc_hi: 'धन और आर्थिक स्थिति',
            },
            {
              key: 'ghatika_lagna',
              icon: <Clock className="w-5 h-5 text-sacred-gold" />,
              title_en: 'Ghatika Lagna',
              title_hi: 'घटिका लग्न',
              desc_en: 'Power, authority & social status',
              desc_hi: 'शक्ति, अधिकार और सामाजिक स्थिति',
            },
            {
              key: 'varnada_lagna',
              icon: <Star className="w-5 h-5 text-sacred-gold" />,
              title_en: 'Varnada Lagna',
              title_hi: 'वर्णद लग्न',
              desc_en: 'Purpose & dharmic calling',
              desc_hi: 'उद्देश्य और धार्मिक कर्तव्य',
            },
          ].map(({ key, icon, title_en, title_hi, desc_en, desc_hi }) => {
            const lagna = data.special_lagnas[key];
            if (!lagna) return null;
            return (
              <div key={key} className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
                <div className="flex items-center gap-2 mb-2">
                  {icon}
                  <h5 className="font-display font-semibold text-sacred-brown text-sm">
                    {language === 'hi' ? title_hi : title_en}
                  </h5>
                </div>
                <p className="text-2xl font-bold" style={{ color: 'var(--aged-gold-dim)' }}>
                  {translateSign(lagna.sign, language)}
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  {language === 'hi' ? `भाव ${lagna.house}` : `House ${lagna.house}`}
                  {lagna.atmakaraka && ` — AK: ${translatePlanet(lagna.atmakaraka, language)}`}
                </p>
                <p className="text-xs text-slate-400 mt-1">{language === 'hi' ? desc_hi : desc_en}</p>
              </div>
            );
          })}
        </div>
      )}

      {/* Indu Lagna */}
      {data.indu_lagna && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
            <Wallet className="w-5 h-5 text-sacred-gold" />
            {language === 'hi' ? 'इंदु लग्न (धन सूचक)' : 'Indu Lagna (Wealth Indicator)'}
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
              <p className="text-xs text-slate-400">{language === 'hi' ? 'इंदु लग्न राशि' : 'Indu Lagna Sign'}</p>
              <p className="text-lg font-bold" style={{ color: 'var(--aged-gold-dim)' }}>
                {translateSign(data.indu_lagna.indu_lagna_sign, language)}
              </p>
            </div>
            <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
              <p className="text-xs text-slate-400">{language === 'hi' ? 'भाव' : 'House'}</p>
              <p className="text-lg font-bold" style={{ color: 'var(--ink)' }}>{data.indu_lagna.indu_lagna_house}</p>
            </div>
            <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
              <p className="text-xs text-slate-400">{language === 'hi' ? '9वां स्वामी (लग्न)' : '9th Lord (Lagna)'}</p>
              <p className="text-lg font-bold" style={{ color: 'var(--ink)' }}>{translatePlanet(data.indu_lagna.ninth_lord_lagna, language)}</p>
            </div>
            <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
              <p className="text-xs text-slate-400">{language === 'hi' ? '9वां स्वामी (चंद्र)' : '9th Lord (Moon)'}</p>
              <p className="text-lg font-bold" style={{ color: 'var(--ink)' }}>{translatePlanet(data.indu_lagna.ninth_lord_moon, language)}</p>
            </div>
          </div>
        </div>
      )}

      {/* Chara Dasha */}
      {data.chara_dasha?.periods && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
            <Clock className="w-5 h-5 text-sacred-gold" />
            {language === 'hi' ? 'चर दशा (राशि आधारित समय)' : 'Chara Dasha (Sign-based Timing)'}
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-slate-100">
                  <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'राशि' : 'Sign'}</th>
                  <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'प्रकार' : 'Type'}</th>
                  <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'स्वामी' : 'Lord'}</th>
                  <th className="text-center p-2 font-medium text-slate-600">{language === 'hi' ? 'वर्ष' : 'Years'}</th>
                  <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'आरंभ' : 'Start'}</th>
                  <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'समाप्ति' : 'End'}</th>
                </tr>
              </thead>
              <tbody>
                {data.chara_dasha.periods.map((p: any, i: number) => {
                  const isCurrent = i === data.chara_dasha.current_period_index;
                  return (
                    <tr
                      key={i}
                      className={`border-b border-slate-100 ${isCurrent ? 'bg-amber-50 font-semibold' : ''}`}
                    >
                      <td className="p-2">
                        {translateSign(p.sign, language)}
                        {isCurrent && <span className="ml-1 text-xs text-amber-700">← {language === 'hi' ? 'वर्तमान' : 'Current'}</span>}
                      </td>
                      <td className="p-2">
                        {p.sign_type && (
                          <span
                            className="text-xs px-2 py-0.5 rounded-full font-medium"
                            style={{
                              backgroundColor: p.sign_type === 'Cardinal' ? '#dbeafe' : p.sign_type === 'Fixed' ? '#fef3c7' : '#d1fae5',
                              color: p.sign_type === 'Cardinal' ? '#1e40af' : p.sign_type === 'Fixed' ? '#92400e' : '#065f46',
                            }}
                          >
                            {language === 'hi' ? p.sign_type_hi : p.sign_type}
                          </span>
                        )}
                      </td>
                      <td className="p-2">{translatePlanet(p.lord, language)}</td>
                      <td className="p-2 text-center font-mono">{p.years}</td>
                      <td className="p-2 font-mono text-xs">{p.start_date}</td>
                      <td className="p-2 font-mono text-xs">{p.end_date}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Jaimini Drishti */}
      {data.jaimini_drishti?.sign_aspects && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
            <Eye className="w-5 h-5 text-sacred-gold" />
            {language === 'hi' ? 'जैमिनी दृष्टि (राशि दृष्टि)' : 'Jaimini Drishti (Sign-based Aspects)'}
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {Object.entries(data.jaimini_drishti.sign_aspects).map(([sign, targets]: [string, any]) => (
              <div key={sign} className="rounded-lg p-2 border border-slate-200 bg-white">
                <span className="font-semibold text-sm" style={{ color: 'var(--ink)' }}>
                  {translateSign(sign, language)}
                </span>
                <span className="text-xs text-slate-400 mx-1">→</span>
                <span className="text-xs text-slate-600">
                  {(targets as string[]).map((t: string) => translateSign(t, language)).join(', ')}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Jaimini Yogas */}
      {data.jaimini_yogas && data.jaimini_yogas.length > 0 && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
            <Star className="w-5 h-5 text-sacred-gold" />
            {language === 'hi' ? 'जैमिनी योग' : 'Jaimini Yogas'}
          </h4>
          <div className="space-y-2">
            {data.jaimini_yogas.map((yoga: any, i: number) => (
              <div key={i} className="rounded-lg p-3 border border-emerald-200 bg-emerald-50">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-sm text-emerald-800">
                    {language === 'hi' ? yoga.name_hi : yoga.name_en}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    yoga.strength === 'Strong' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                  }`}>
                    {yoga.strength === 'Strong' ? (language === 'hi' ? 'बलवान' : 'Strong') : (language === 'hi' ? 'दुर्बल' : 'Weak')}
                  </span>
                </div>
                <p className="text-xs text-slate-600">
                  {language === 'hi' ? yoga.description_hi : yoga.description_en}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Longevity */}
      {data.longevity && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
            <Clock className="w-5 h-5 text-sacred-gold" />
            {language === 'hi' ? 'आयु गणना' : 'Longevity Calculation'}
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3">
            <div className="rounded-lg p-3 border text-center" style={{
              backgroundColor: data.longevity.category === 'Purna' ? '#d1fae5' : data.longevity.category === 'Madhyama' ? '#fef3c7' : '#fee2e2',
              borderColor: data.longevity.category === 'Purna' ? '#059669' : data.longevity.category === 'Madhyama' ? '#d97706' : '#dc2626',
            }}>
              <p className="text-2xl font-bold" style={{
                color: data.longevity.category === 'Purna' ? '#065f46' : data.longevity.category === 'Madhyama' ? '#92400e' : '#991b1b',
              }}>
                {data.longevity.category}
              </p>
              <p className="text-sm" style={{ color: data.longevity.category === 'Purna' ? '#065f46' : data.longevity.category === 'Madhyama' ? '#92400e' : '#991b1b' }}>
                {language === 'hi' ? data.longevity.description_hi : data.longevity.description_en}
              </p>
            </div>
            <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
              <p className="text-xs text-slate-400">{language === 'hi' ? 'लग्न राशि' : 'Lagna Sign'}</p>
              <p className="font-semibold">{translateSign(data.longevity.lagna_sign, language)} ({data.longevity.lagna_modality})</p>
            </div>
            <div className="rounded-lg p-3 border" style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}>
              <p className="text-xs text-slate-400">{language === 'hi' ? '8वां स्वामी' : '8th Lord'}</p>
              <p className="font-semibold">{translatePlanet(data.longevity.eighth_lord, language)} {language === 'hi' ? 'में' : 'in'} {translateSign(data.longevity.eighth_lord_sign, language)} ({data.longevity.eighth_modality})</p>
            </div>
          </div>
          <p className="text-xs text-slate-400 italic">
            {language === 'hi' ? data.longevity.note_hi : data.longevity.note_en}
          </p>
        </div>
      )}

      {/* Argala */}
      {data.argala?.house_argalas && data.argala.house_argalas.length > 0 && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
            <Eye className="w-5 h-5 text-sacred-gold" />
            {language === 'hi' ? 'अर्गला (ग्रह हस्तक्षेप)' : 'Argala (Planetary Intervention)'}
          </h4>
          <div className="space-y-2">
            {data.argala.house_argalas.map((ha: any) => (
              <div key={ha.house} className="rounded-lg p-3 border border-slate-200 bg-white">
                <p className="font-semibold text-sm mb-1" style={{ color: 'var(--ink)' }}>
                  {language === 'hi' ? `भाव ${ha.house}` : `House ${ha.house}`}
                </p>
                <div className="space-y-2">
                  {ha.argalas.map((a: any, i: number) => (
                    <div key={i} className="rounded-md border border-slate-100 p-2 bg-slate-50/50">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-600">
                          {translateBackend(a.type, language)} — {a.planets.map((p: string) => translatePlanet(p, language)).join(', ')} (H{a.from_house})
                        </span>
                        <div className="flex items-center gap-1.5">
                          {a.nature && (
                            <span className={`px-2 py-0.5 rounded-full font-medium ${
                              a.nature === 'Shubha' ? 'bg-emerald-50 text-emerald-700' :
                              a.nature === 'Paapa' ? 'bg-red-50 text-red-700' :
                              'bg-amber-50 text-amber-700'
                            }`}>
                              {language === 'hi' ? a.nature_hi : a.nature_en}
                            </span>
                          )}
                          <span className={`px-2 py-0.5 rounded-full font-medium ${
                            a.blocked ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-600'
                          }`}>
                            {a.status === 'Blocked'
                              ? (language === 'hi' ? 'अवरुद्ध' : 'Blocked')
                              : (language === 'hi' ? 'सक्रिय' : 'Active')}
                          </span>
                        </div>
                      </div>
                      {(a.detail_en || a.detail_hi) && (
                        <p className="text-xs text-slate-500 mt-1">
                          {language === 'hi' ? a.detail_hi : a.detail_en}
                        </p>
                      )}
                      {(a.remedy_en || a.remedy_hi) && (
                        <p className="text-xs mt-1 italic" style={{ color: '#6b21a8' }}>
                          <span className="font-semibold">{language === 'hi' ? 'उपाय: ' : 'Remedy: '}</span>
                          {language === 'hi' ? a.remedy_hi : a.remedy_en}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
