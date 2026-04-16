import { Check, X } from 'lucide-react';

interface DosAndDontsProps {
  dos: Array<{ en: string; hi: string }>;
  donts: Array<{ en: string; hi: string }>;
  language: string;
  t: (key: string) => string;
}

export default function DosAndDonts({ dos, donts, language, t }: DosAndDontsProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {/* Do's */}
      <div className="rounded-xl bg-green-50 border border-green-200 p-4">
        <h4 className="text-sm font-semibold text-green-700 mb-2">{t('auto.dos')}</h4>
        <div className="space-y-2">
          {dos.map((item, i) => (
            <div key={i} className="flex items-start gap-2">
              <Check className="w-4 h-4 text-green-600 mt-0.5 shrink-0" />
              <p className="text-sm text-foreground">{language === 'hi' ? item.hi : item.en}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Don'ts */}
      <div className="rounded-xl bg-red-50 border border-red-200 p-4">
        <h4 className="text-sm font-semibold text-red-700 mb-2">{t('auto.donts')}</h4>
        <div className="space-y-2">
          {donts.map((item, i) => (
            <div key={i} className="flex items-start gap-2">
              <X className="w-4 h-4 text-red-600 mt-0.5 shrink-0" />
              <p className="text-sm text-foreground">{language === 'hi' ? item.hi : item.en}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
