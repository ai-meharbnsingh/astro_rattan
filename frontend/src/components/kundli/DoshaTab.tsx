import { Loader2, Gem } from 'lucide-react';
import { translatePlanet, translateLabel, translateName } from '@/lib/backend-translations';

interface DoshaTabProps {
  doshaData: any;
  doshaDisplay: { mangal: any; kaalsarp: any; sadesati: any } | null;
  loadingDosha: boolean;
  language: string;
  t: (key: string) => string;
}

export default function DoshaTab({ doshaData, doshaDisplay, loadingDosha, language, t }: DoshaTabProps) {
  if (loadingDosha) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text/70">{t('kundli.analyzingDoshas')}</span></div>
    );
  }

  if (!doshaDisplay) {
    return <p className="text-center text-cosmic-text/70 py-8">{t('kundli.clickDoshaTab')}</p>;
  }

  return (
    <div className="grid gap-4">
      {doshaDisplay.mangal.has_dosha && (
        <div className="bg-sacred-cream rounded-xl p-4 border border-red-500/30">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-display font-semibold text-sacred-brown">{translateName('Mangal Dosha', language)}</h4>
            <span className="text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-400">
              {t('common.present')} ({translateLabel(doshaDisplay.mangal.severity, language)})
            </span>
          </div>
          <p className="text-sm text-cosmic-text/70">{doshaDisplay.mangal.description}</p>
        </div>
      )}
      {doshaDisplay.kaalsarp.has_dosha && (
        <div className="bg-sacred-cream rounded-xl p-4 border border-red-500/30">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-display font-semibold text-sacred-brown">{translateName('Kaal Sarp Dosha', language)}</h4>
            <span className="text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-400">{t('common.present')}</span>
          </div>
          <p className="text-sm text-cosmic-text/70">{doshaDisplay.kaalsarp.description}</p>
        </div>
      )}
      {doshaDisplay.sadesati.has_sade_sati && (
        <div className="bg-sacred-cream rounded-xl p-4 border border-orange-200">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-display font-semibold text-sacred-brown">{translateName('Sade Sati', language)}</h4>
            <span className="text-xs px-2 py-1 rounded-full bg-orange-100 text-orange-600">
              {t('common.active')} - {translateLabel(doshaDisplay.sadesati.phase, language)}
            </span>
          </div>
          <p className="text-sm text-cosmic-text/70">{doshaDisplay.sadesati.description}</p>
        </div>
      )}
      {!doshaDisplay.mangal.has_dosha && !doshaDisplay.kaalsarp.has_dosha && !doshaDisplay.sadesati.has_sade_sati && (
        <p className="text-sm py-4 text-success">{t('kundli.noDoshasInChart')}</p>
      )}

      {/* Gemstone Recommendations */}
      {doshaData?.gemstone_recommendations && doshaData.gemstone_recommendations.length > 0 && (
        <div className="bg-sacred-cream rounded-xl p-4 border border-sacred-gold/30 mt-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3 flex items-center gap-2">
            <Gem className="w-5 h-5 text-sacred-gold" />
            {language === 'hi' ? 'रत्न सिफारिशें' : 'Gemstone Recommendations'}
          </h4>
          <div className="grid gap-3">
            {doshaData.gemstone_recommendations.map((g: any, i: number) => (
              <div key={i} className={`rounded-lg p-3 border ${g.priority === 'primary' ? 'border-sacred-gold/50 bg-sacred-gold/5' : 'border-sacred-gold/20'}`}>
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-sm text-sacred-brown">
                    {language === 'hi' ? g.gemstone_hi : g.gemstone}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${g.priority === 'primary' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'}`}>
                    {g.priority === 'primary' ? (language === 'hi' ? 'प्राथमिक' : 'Primary') : (language === 'hi' ? 'सहायक' : 'Secondary')}
                  </span>
                </div>
                <p className="text-xs text-cosmic-text/70">
                  {language === 'hi' ? 'ग्रह' : 'Planet'}: <strong>{translatePlanet(g.planet, language)}</strong> ({g.reason})
                </p>
                <p className="text-xs text-cosmic-text/70 mt-1">
                  {language === 'hi' ? 'धातु' : 'Metal'}: {g.metal} &bull; {language === 'hi' ? 'अंगुली' : 'Finger'}: {g.finger} &bull; {language === 'hi' ? 'दिन' : 'Day'}: {g.day}
                </p>
              </div>
            ))}
          </div>
          <p className="text-xs text-cosmic-text/70 mt-2 italic">
            {language === 'hi' ? '* कृपया रत्न धारण करने से पहले किसी योग्य ज्योतिषी से परामर्श लें।' : '* Please consult a qualified astrologer before wearing any gemstone.'}
          </p>
        </div>
      )}
    </div>
  );
}
