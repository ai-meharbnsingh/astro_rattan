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
    return <p className="text-center text-cosmic-text py-8">{t('kundli.clickYogasTab')}</p>;
  }

  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-2 mb-4">
          <CheckCircle className="w-5 h-5" style={{ color: '#22c55e' }} />
          <h4 className="font-display font-bold text-lg" style={{ color: 'var(--ink)' }}>{t('section.yogas')}</h4>
        </div>
        <div className="grid gap-3">
          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).length === 0 && (
            <p className="text-sm text-cosmic-text py-4">{t('kundli.noYogasDetected')}</p>
          )}
          {(yogaDoshaData.yogas || []).filter((y: any) => y.present).map((yoga: any, idx: number) => (
            <div
              key={idx}
              className="rounded-xl p-4 border border-green-300"
              style={{ backgroundColor: 'rgba(34,197,94,0.05)' }}
            >
              <div className="flex items-center justify-between mb-2">
                <h5 className="font-display font-semibold" style={{ color: 'var(--ink)' }}>{translateName(yoga.name, language)}</h5>
                <span className="text-sm px-2 py-1 rounded-full font-medium bg-green-100 text-green-800">
                  {t('common.present')}
                </span>
              </div>
              <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{translateBackend(yoga.description, language)}</p>
              {yoga.planets_involved && yoga.planets_involved.length > 0 && (
                <div className="mt-2 flex gap-2">
                  {yoga.planets_involved.map((p: string) => (
                    <span key={p} className="text-sm px-2 py-0.5 rounded-full bg-green-100 text-green-800">{p}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="flex items-center gap-2 mb-4">
          <Shield className="w-5 h-5" style={{ color: '#8B2332' }} />
          <h4 className="font-display font-bold text-lg" style={{ color: 'var(--ink)' }}>{t('section.doshas')}</h4>
        </div>
        <div className="grid gap-3">
          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).length === 0 && (
            <p className="text-sm py-4" style={{ color: '#22c55e' }}>{t('kundli.noDoshasInChart')}</p>
          )}
          {(yogaDoshaData.doshas || []).filter((d: any) => d.present).map((dosha: any, idx: number) => (
            <div
              key={idx}
              className={`rounded-xl p-4 border ${dosha.severity === 'high' ? 'border-red-300' : 'border-amber-400'}`}
              style={{ backgroundColor: dosha.severity === 'high' ? 'rgba(196,62,78,0.08)' : 'rgba(245,158,11,0.05)' }}
            >
              <div className="flex items-center justify-between mb-2">
                <h5 className="font-display font-semibold" style={{ color: 'var(--ink)' }}>{translateName(dosha.name, language)}</h5>
                <div className="flex items-center gap-2">
                  {dosha.severity !== 'none' && (
                    <span className={`text-sm px-2 py-0.5 rounded-full ${dosha.severity === 'high' ? 'bg-red-100 text-red-800' : dosha.severity === 'medium' ? 'bg-amber-100 text-amber-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {translateLabel(dosha.severity, language)}
                    </span>
                  )}
                  <span className="text-sm px-2 py-1 rounded-full font-medium bg-red-100 text-red-800">
                    {t('common.present')}
                  </span>
                </div>
              </div>
              <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{translateBackend(dosha.description, language)}</p>
              {dosha.remedies && dosha.remedies.length > 0 && (
                <div className="mt-3 pt-3 border-t" style={{ borderColor: 'rgba(184,134,11,0.2)' }}>
                  <p className="text-sm font-semibold mb-2" style={{ color: 'var(--aged-gold-dim)' }}>
                    <AlertTriangle className="w-3 h-3 inline mr-1" />{t('section.remedies')}:
                  </p>
                  <ul className="space-y-1">
                    {dosha.remedies.map((r: string, ri: number) => (
                      <li key={ri} className="text-sm flex items-start gap-2" style={{ color: 'var(--ink-light)' }}>
                        <span className="mt-1 w-1 h-1 rounded-full flex-shrink-0" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />
                        {translateRemedy(r, language)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Specific Doshas: Mangal, Kaal Sarp, Sade Sati */}
      {loadingDosha && (
        <div className="flex items-center justify-center py-6">
          <Loader2 className="w-5 h-5 animate-spin text-sacred-gold" />
          <span className="ml-2 text-sm text-cosmic-text">{t('kundli.analyzingDoshas')}</span>
        </div>
      )}
      {doshaDisplay && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="w-5 h-5" style={{ color: '#DC2626' }} />
            <h4 className="font-display font-bold text-lg" style={{ color: 'var(--ink)' }}>{language === 'hi' ? 'विशेष दोष' : 'Specific Doshas'}</h4>
          </div>
          <div className="grid gap-3">
            {doshaDisplay.mangal.has_dosha && (
              <div className="rounded-xl p-4 border border-red-300" style={{ backgroundColor: 'rgba(196,62,78,0.08)' }}>
                <div className="flex items-center justify-between mb-2">
                  <h5 className="font-display font-semibold" style={{ color: 'var(--ink)' }}>{translateName('Mangal Dosha', language)}</h5>
                  <span className="text-sm px-2 py-1 rounded-full bg-red-100 text-red-800">
                    {t('common.present')} ({translateLabel(doshaDisplay.mangal.severity, language)})
                  </span>
                </div>
                <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{doshaDisplay.mangal.description}</p>
              </div>
            )}
            {doshaDisplay.kaalsarp.has_dosha && (
              <div className="rounded-xl p-4 border border-red-300" style={{ backgroundColor: 'rgba(196,62,78,0.08)' }}>
                <div className="flex items-center justify-between mb-2">
                  <h5 className="font-display font-semibold" style={{ color: 'var(--ink)' }}>{translateName('Kaal Sarp Dosha', language)}</h5>
                  <span className="text-sm px-2 py-1 rounded-full bg-red-100 text-red-800">{t('common.present')}</span>
                </div>
                <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{doshaDisplay.kaalsarp.description}</p>
              </div>
            )}
            {doshaDisplay.sadesati.has_sade_sati && (
              <div className="rounded-xl p-4 border border-orange-200" style={{ backgroundColor: 'rgba(245,158,11,0.05)' }}>
                <div className="flex items-center justify-between mb-2">
                  <h5 className="font-display font-semibold" style={{ color: 'var(--ink)' }}>{translateName('Sade Sati', language)}</h5>
                  <span className="text-sm px-2 py-1 rounded-full bg-orange-100 text-orange-600">
                    {t('common.active')} - {translateLabel(doshaDisplay.sadesati.phase, language)}
                  </span>
                </div>
                <p className="text-sm" style={{ color: 'var(--ink-light)' }}>{doshaDisplay.sadesati.description}</p>
              </div>
            )}
            {!doshaDisplay.mangal.has_dosha && !doshaDisplay.kaalsarp.has_dosha && !doshaDisplay.sadesati.has_sade_sati && (
              <p className="text-sm py-4" style={{ color: '#22c55e' }}>{t('kundli.noDoshasInChart')}</p>
            )}
          </div>
        </div>
      )}

      {/* Gemstone Recommendations */}
      {doshaData?.gemstone_recommendations && doshaData.gemstone_recommendations.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Gem className="w-5 h-5" style={{ color: 'var(--aged-gold-dim)' }} />
            <h4 className="font-display font-bold text-lg" style={{ color: 'var(--ink)' }}>{language === 'hi' ? 'रत्न सिफारिशें' : 'Gemstone Recommendations'}</h4>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {doshaData.gemstone_recommendations.map((gem: any, idx: number) => (
              <div key={idx} className="rounded-xl p-4 border border-sacred-gold" style={{ backgroundColor: 'rgba(184,134,11,0.05)' }}>
                <div className="flex items-center justify-between mb-2">
                  <h5 className="font-display font-semibold" style={{ color: 'var(--ink)' }}>
                    {language === 'hi' && gem.gemstone_hi ? gem.gemstone_hi : gem.gemstone}
                  </h5>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${gem.priority === 'primary' ? 'bg-sacred-gold text-sacred-gold-dark font-semibold' : 'bg-sacred-cream text-cosmic-text'}`}>
                    {gem.priority === 'primary' ? (language === 'hi' ? 'प्राथमिक' : 'Primary') : (language === 'hi' ? 'द्वितीयक' : 'Secondary')}
                  </span>
                </div>
                <p className="text-sm mb-2" style={{ color: 'var(--ink-light)' }}>
                  {language === 'hi' ? 'ग्रह' : 'Planet'}: {translatePlanet(gem.planet, language)} — {gem.reason}
                </p>
                <div className="flex flex-wrap gap-3 text-xs" style={{ color: 'var(--ink-light)' }}>
                  {gem.metal && <span>{language === 'hi' ? 'धातु' : 'Metal'}: {gem.metal}</span>}
                  {gem.finger && <span>{language === 'hi' ? 'उंगली' : 'Finger'}: {gem.finger}</span>}
                  {gem.day && <span>{language === 'hi' ? 'दिन' : 'Day'}: {gem.day}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
