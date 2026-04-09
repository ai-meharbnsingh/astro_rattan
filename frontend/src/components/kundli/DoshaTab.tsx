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

    </div>
  );
}
