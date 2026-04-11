import { Loader2 } from 'lucide-react';
import { translateSign, translateNakshatra } from '@/lib/backend-translations';

interface UpagrahasTabProps {
  upagrahasData: any;
  loadingUpagrahas: boolean;
  language: string;
  t: (key: string) => string;
}

export default function UpagrahasTab({ upagrahasData, loadingUpagrahas, language, t }: UpagrahasTabProps) {
  const UPAGRAHA_HI: Record<string, string> = {
    Gulika: 'गुलिक',
    Mandi: 'मांडी',
    Yamakantaka: 'यमकंटक',
    Ardhaprahara: 'अर्धप्रहर',
    Kala: 'काल',
    Mrityu: 'मृत्यु',
    Dhuma: 'धूम',
    Vyatipata: 'व्यतीपात',
    Parivesha: 'परिवेष',
    IndraChapa: 'इन्द्रचाप',
    Upaketu: 'उपकेतु',
  };
  const upagrahaLabel = (name: string) => (language === 'hi' ? (UPAGRAHA_HI[name] || name) : name);

  if (loadingUpagrahas) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.loadingUpagrahas')}</span></div>
    );
  }

  if (!upagrahasData) {
    return <p className="text-center text-cosmic-text py-8">{t('common.noData')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
        <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.upagrahasTitle')}</h4>
        <table className="w-full text-sm">
          <thead><tr className="bg-sacred-gold">
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.upagraha')}</th>
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.longitude')}</th>
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.sign')}</th>
            <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.nakshatra')}</th>
          </tr></thead>
          <tbody>
            {(() => {
              const raw = upagrahasData.upagrahas;
              const items = Array.isArray(raw) ? raw : Object.entries(raw || {}).map(([name, data]: [string, any]) => ({ name, ...data }));
              return items.map((u: any) => (
                <tr key={u.name} className="border-t border-sacred-gold">
                  <td className="p-2 font-semibold text-sacred-brown">{upagrahaLabel(u.name)}</td>
                  <td className="p-2 text-cosmic-text">{typeof u.longitude === 'number' ? u.longitude.toFixed(2) + '\u00b0' : u.longitude}</td>
                  <td className="p-2 text-cosmic-text">{translateSign(u.sign, language)}</td>
                  <td className="p-2 text-cosmic-text">{translateNakshatra(u.nakshatra, language) || u.nakshatra}{u.nakshatra_pada ? ` (${t('kundli.pada')} ${u.nakshatra_pada})` : u.pada ? ` (${t('kundli.pada')} ${u.pada})` : ''}</td>
                </tr>
              ));
            })()}
          </tbody>
        </table>
      </div>
    </div>
  );
}
