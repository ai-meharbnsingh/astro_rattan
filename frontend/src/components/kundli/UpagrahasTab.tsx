import { useState } from 'react';
import { Loader2, AlertTriangle, ChevronDown, ChevronRight, Layers } from 'lucide-react';
import { translateSign, translateNakshatra } from '@/lib/backend-translations';
import { Heading } from '@/components/ui/heading';
import SlokaHover from './SlokaHover';

interface UpagrahasTabProps {
  upagrahasData: any;
  loadingUpagrahas: boolean;
  language: string;
  t: (key: string) => string;
}

const UPAGRAHA_HI: Record<string, string> = {
  Gulika: 'गुलिक', Mandi: 'मांडी', Yamakantaka: 'यमकंटक',
  Ardhaprahara: 'अर्धप्रहर', Kala: 'काल', Mrityu: 'मृत्यु',
  Dhuma: 'धूम', Vyatipata: 'व्यतीपात', Parivesha: 'परिवेष',
  IndraChapa: 'इन्द्रचाप', Upaketu: 'उपकेतु',
};

const NATURE_STYLE: Record<string, string> = {
  severe_malefic: 'bg-red-100 text-red-800',
  malefic:        'bg-orange-100 text-orange-800',
  neutral:        'bg-slate-100 text-slate-700',
  benefic:        'bg-emerald-100 text-emerald-800',
};
const NATURE_LABEL: Record<string, { en: string; hi: string }> = {
  severe_malefic: { en: 'Severe Malefic', hi: 'घोर पापी' },
  malefic:        { en: 'Malefic',        hi: 'पापी' },
  neutral:        { en: 'Neutral',        hi: 'सम' },
  benefic:        { en: 'Benefic',        hi: 'शुभ' },
};

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';

export default function UpagrahasTab({ upagrahasData, loadingUpagrahas, language, t }: UpagrahasTabProps) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const isHi = language === 'hi';

  const toggle = (name: string) => setExpanded(prev => {
    const next = new Set(prev);
    if (next.has(name)) next.delete(name);
    else next.add(name);
    return next;
  });

  const uLabel = (name: string) => isHi ? (UPAGRAHA_HI[name] || name) : name;

  if (loadingUpagrahas) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.loadingUpagrahas')}</span>
      </div>
    );
  }

  if (!upagrahasData) {
    return <p className="text-center text-foreground py-8">{t('common.noData')}</p>;
  }

  const raw = upagrahasData.upagrahas;
  const items: any[] = Array.isArray(raw)
    ? raw
    : Object.entries(raw || {}).map(([name, data]: [string, any]) => ({ name, ...data }));

  const lagnaAlerts = items.filter(
    u => (u.name === 'Gulika' || u.name === 'Mandi') && u.house === 1
  );

  return (
    <div className="space-y-4">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Layers className="w-6 h-6" />
          {isHi ? 'उपग्रह' : 'Upagrahas'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi ? 'गुलिक, मांडी एवं अन्य सूक्ष्म ग्रहों की स्थिति' : 'Positions of Gulika, Mandi and other sub-planets'}
        </p>
      </div>

      {/* Critical Gulika/Mandi in Lagna alert */}
      {lagnaAlerts.map(u => (
        <div key={u.name} className="rounded-xl border-2 border-red-400 bg-red-50 p-4 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
          <div>
            <p className="font-bold text-red-800 text-sm">
              {isHi
                ? <>{UPAGRAHA_HI[u.name] || u.name}{' लग्न में — अत्यंत अशुभ ('}<SlokaHover slokaRef="Phaladeepika Adh. 25" language={language}>{'फलदीपिका अध्याय 25'}</SlokaHover>{')'}</>
                : <>{u.name}{' in Lagna — Highly Inauspicious ('}<SlokaHover slokaRef="Phaladeepika Adh. 25" language={language}>{'Phaladeepika Adh. 25'}</SlokaHover>{')'}</>}
            </p>
            <p className="text-xs text-red-700 mt-1 leading-relaxed">
              {isHi
                ? <>{UPAGRAHA_HI[u.name] || u.name}{' लग्न में होने से जातक की जीवन-शक्ति, स्वास्थ्य एवं समग्र भाग्य पर गहरा पाप-प्रभाव पड़ता है। '}<SlokaHover slokaRef="Phaladeepika Adh. 25" language={language}>{'फलदीपिका'}</SlokaHover>{' के अनुसार यह सर्वाधिक क्रूर संयोगों में से एक है।'}</>
                : <>{u.name}{" occupying the Lagna casts a severe malefic shadow over the native's vitality, health, and overall fortune. "}<SlokaHover slokaRef="Phaladeepika Adh. 25" language={language}>{'Phaladeepika Adh. 25'}</SlokaHover>{' classifies this as one of the most inauspicious placements.'}</>}
            </p>
          </div>
        </div>
      ))}

      {/* Main table */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <span>{isHi ? 'उपग्रह' : t('section.upagrahasTitle')}</span>
        </div>
        <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '4%' }} />
            <col style={{ width: '16%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '14%' }} />
            <col style={{ width: '26%' }} />
            <col style={{ width: '16%' }} />
            <col style={{ width: '16%' }} />
          </colgroup>
          <thead>
            <tr>
              <th className={thCls}></th>
              <th className={thCls}>{t('table.upagraha')}</th>
              <th className={`${thCls} text-center`}>{t('table.house')}</th>
              <th className={thCls}>{t('table.sign')}</th>
              <th className={thCls}>{t('table.nakshatra')}</th>
              <th className={thCls}>{t('table.longitude')}</th>
              <th className={thCls}>{isHi ? 'स्वभाव' : 'Nature'}</th>
            </tr>
          </thead>
          <tbody>
            {items.map((u: any) => {
              const hasInterp = u.interpretation_en || u.classical_meaning_en;
              const isOpen = expanded.has(u.name);
              const natStyle = NATURE_STYLE[u.nature] || NATURE_STYLE.neutral;
              const natLabel = isHi
                ? (NATURE_LABEL[u.nature]?.hi || u.nature)
                : (NATURE_LABEL[u.nature]?.en || u.nature);
              const isLagna = u.house === 1 && (u.name === 'Gulika' || u.name === 'Mandi');

              return (
                <>
                  <tr
                    key={u.name}
                    className={`${hasInterp ? 'cursor-pointer hover:bg-muted/20' : ''} ${isLagna ? 'bg-red-50' : ''}`}
                    onClick={hasInterp ? () => toggle(u.name) : undefined}
                  >
                    <td className={`${tdCls} text-center`}>
                      {hasInterp && (
                        isOpen
                          ? <ChevronDown className="w-3 h-3 text-primary inline" />
                          : <ChevronRight className="w-3 h-3 text-primary inline" />
                      )}
                    </td>
                    <td className={`${tdCls} font-semibold`}>
                      {uLabel(u.name)}
                      {isLagna && <span className="ml-1.5 text-[10px] font-bold text-red-600">⚠</span>}
                    </td>
                    <td className={`${tdCls} text-center`}>
                      {u.house > 0 ? u.house : '—'}
                    </td>
                    <td className={tdCls}>{translateSign(u.sign, language)}</td>
                    <td className={`${tdCls} break-words overflow-hidden`}>
                      {translateNakshatra(u.nakshatra, language) || u.nakshatra}
                      {(u.nakshatra_pada || u.pada) && ` (${t('kundli.pada')} ${u.nakshatra_pada || u.pada})`}
                    </td>
                    <td className={tdCls}>
                      {typeof u.longitude === 'number' ? u.longitude.toFixed(2) + '°' : u.longitude}
                    </td>
                    <td className={tdCls}>
                      {u.nature && (
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${natStyle}`}>
                          {natLabel}
                        </span>
                      )}
                    </td>
                  </tr>
                  {isOpen && hasInterp && (
                    <tr key={`${u.name}-interp`} className="bg-muted/30">
                      <td colSpan={7} className="p-3 border-t border-border">
                        {(u.classical_meaning_en || u.classical_meaning_hi) && (
                          <p className="text-xs text-foreground/70 italic mb-1">
                            {isHi ? (u.classical_meaning_hi || u.classical_meaning_en) : (u.classical_meaning_en || u.classical_meaning_hi)}
                          </p>
                        )}
                        <p className="text-xs text-foreground/80 leading-relaxed">
                          {isHi ? (u.interpretation_hi || u.interpretation_en) : (u.interpretation_en || u.interpretation_hi)}
                        </p>
                      </td>
                    </tr>
                  )}
                </>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
