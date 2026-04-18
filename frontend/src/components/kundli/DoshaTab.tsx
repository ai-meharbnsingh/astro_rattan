import { Loader2 } from 'lucide-react';
import { translateLabel, translateName, translateBackend } from '@/lib/backend-translations';
import { Heading } from '@/components/ui/heading';

interface DoshaTabProps {
  doshaData: any;
  doshaDisplay: { mangal: any; kaalsarp: any; sadesati: any } | null;
  loadingDosha: boolean;
  language: string;
  t: (key: string) => string;
}

export default function DoshaTab({ doshaData, doshaDisplay, loadingDosha, language, t }: DoshaTabProps) {
  void doshaData;
  if (loadingDosha) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-primary" /><span className="ml-2 text-foreground">{t('kundli.analyzingDoshas')}</span></div>
    );
  }

  if (!doshaDisplay) {
    return <p className="text-center text-foreground py-8">{t('kundli.clickDoshaTab')}</p>;
  }

  return (
    <div className="grid gap-4">
      {doshaDisplay.mangal.has_dosha && (
        <div className="bg-muted rounded-xl p-4 border border-red-300">
          <div className="flex items-center justify-between mb-2">
            <Heading as={4} variant={4}>{translateName('Mangal Dosha', language)}</Heading>
            <span className="text-sm px-2.5 py-0.5 rounded-full font-medium bg-red-100 text-red-800">
              {t('common.present')} ({translateLabel(doshaDisplay.mangal.severity, language)})
            </span>
          </div>
          <p className="text-sm text-muted-foreground">{translateBackend(doshaDisplay.mangal.description, language)}</p>
        </div>
      )}
      {doshaDisplay.kaalsarp.has_dosha && (
        <div className="bg-muted rounded-xl p-4 border border-red-300">
          <div className="flex items-center justify-between mb-2">
            <Heading as={4} variant={4}>{translateName('Kaal Sarp Dosha', language)}</Heading>
            <span className="text-sm px-2.5 py-0.5 rounded-full font-medium bg-red-100 text-red-800">{t('common.present')}</span>
          </div>
          <p className="text-sm text-muted-foreground">{translateBackend(doshaDisplay.kaalsarp.description, language)}</p>
        </div>
      )}
      {doshaDisplay.sadesati.has_sade_sati && (
        <div className={`rounded-xl p-4 border ${
          (doshaDisplay.sadesati as any)?.ashtam_shani
            ? 'border-red-400 bg-red-50'
            : 'border-orange-200 bg-muted'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <Heading as={4} variant={4}>{translateName('Sade Sati', language)}</Heading>
            <span className={`text-sm px-2.5 py-0.5 rounded-full font-medium ${
              (doshaDisplay.sadesati as any)?.ashtam_shani
                ? 'bg-red-100 text-red-700'
                : 'bg-orange-100 text-orange-600'
            }`}>
              {t('common.active')} - {translateLabel(doshaDisplay.sadesati.phase, language)}
            </span>
          </div>
          <p className="text-sm text-muted-foreground mb-3">{translateBackend(doshaDisplay.sadesati.description, language)}</p>

          {/* Ashtam Shani detailed effects */}
          {(doshaDisplay.sadesati as any)?.ashtam_shani && (doshaDisplay.sadesati as any)?.ashtam_effects && (
            <div className="mt-3 pt-3 border-t border-red-200 space-y-2">
              <p className="text-xs font-semibold text-red-700 uppercase tracking-wide">
                {language === 'hi' ? '⚠️ अष्टम शनि - विस्तृत प्रभाव' : '⚠️ Ashtam Shani — Detailed Effects'}
              </p>
              <ul className="text-xs text-red-700/90 space-y-1">
                {((doshaDisplay.sadesati as any).ashtam_effects as string[]).map((effect, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-red-500 font-bold mt-0.5">•</span>
                    <span>{effect}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Remedies */}
          {doshaDisplay.sadesati.remedies && doshaDisplay.sadesati.remedies.length > 0 && (
            <div className="mt-3 pt-3 border-t border-orange-200 space-y-2">
              <p className="text-xs font-semibold text-amber-700 uppercase tracking-wide">
                {language === 'hi' ? 'उपचार' : 'Remedies'}
              </p>
              <ul className="text-xs text-muted-foreground space-y-1">
                {(doshaDisplay.sadesati.remedies as string[]).slice(0, 4).map((remedy, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-amber-600 font-bold mt-0.5">•</span>
                    <span>{remedy}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      {!doshaDisplay.mangal.has_dosha && !doshaDisplay.kaalsarp.has_dosha && !doshaDisplay.sadesati.has_sade_sati && (
        <p className="text-sm py-4 text-success">{t('kundli.noDoshasInChart')}</p>
      )}

    </div>
  );
}
