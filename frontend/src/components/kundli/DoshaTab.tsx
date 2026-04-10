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
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.analyzingDoshas')}</span></div>
    );
  }

  if (!doshaDisplay) {
    return <p className="text-center text-cosmic-text py-8">{t('kundli.clickDoshaTab')}</p>;
  }

  return (
    <div className="grid gap-4">
      {doshaDisplay.mangal.has_dosha && (
        <div className="bg-sacred-cream rounded-xl p-4 border border-red-300">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-display font-semibold text-sacred-brown">{translateName('Mangal Dosha', language)}</h4>
            <span className="text-sm px-2.5 py-0.5 rounded-full font-medium bg-red-100 text-red-800">
              {t('common.present')} ({translateLabel(doshaDisplay.mangal.severity, language)})
            </span>
          </div>
          <p className="text-sm text-cosmic-text">{doshaDisplay.mangal.description}</p>
        </div>
      )}
      {doshaDisplay.kaalsarp.has_dosha && (
        <div className="bg-sacred-cream rounded-xl p-4 border border-red-300">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-display font-semibold text-sacred-brown">{translateName('Kaal Sarp Dosha', language)}</h4>
            <span className="text-sm px-2.5 py-0.5 rounded-full font-medium bg-red-100 text-red-800">{t('common.present')}</span>
          </div>
          <p className="text-sm text-cosmic-text">{doshaDisplay.kaalsarp.description}</p>
        </div>
      )}
      {doshaDisplay.sadesati.has_sade_sati && (
        <div className="bg-sacred-cream rounded-xl p-4 border border-orange-200">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-display font-semibold text-sacred-brown">{translateName('Sade Sati', language)}</h4>
            <span className="text-sm px-2.5 py-0.5 rounded-full font-medium bg-orange-100 text-orange-600">
              {t('common.active')} - {translateLabel(doshaDisplay.sadesati.phase, language)}
            </span>
          </div>
          <p className="text-sm text-cosmic-text">{doshaDisplay.sadesati.description}</p>
        </div>
      )}
      {!doshaDisplay.mangal.has_dosha && !doshaDisplay.kaalsarp.has_dosha && !doshaDisplay.sadesati.has_sade_sati && (
        <p className="text-sm py-4 text-success">{t('kundli.noDoshasInChart')}</p>
      )}

    </div>
  );
}
