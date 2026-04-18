import { useState } from 'react';
import { Loader2, AlertTriangle, ChevronDown, ChevronRight, BookOpen } from 'lucide-react';
import { translateSign, translateNakshatra } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

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

export default function UpagrahasTab({ upagrahasData, loadingUpagrahas, language, t }: UpagrahasTabProps) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const isHi = language === 'hi';

  const toggle = (name: string) => setExpanded(prev => {
    const next = new Set(prev);
    next.has(name) ? next.delete(name) : next.add(name);
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

  // Gulika or Mandi in Lagna (house 1) — critical alert
  const lagnaAlerts = items.filter(
    u => (u.name === 'Gulika' || u.name === 'Mandi') && u.house === 1
  );

  return (
    <div className="space-y-6">
      {/* Critical Gulika/Mandi in Lagna alert */}
      {lagnaAlerts.map(u => (
        <div key={u.name} className="rounded-xl border-2 border-red-400 bg-red-50 p-4 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
          <div>
            <p className="font-bold text-red-800 text-sm">
              {isHi
                ? `${UPAGRAHA_HI[u.name] || u.name} लग्न में — अत्यंत अशुभ (फलदीपिका अध्याय 25)`
                : `${u.name} in Lagna — Highly Inauspicious (Phaladeepika Adh. 25)`}
            </p>
            <p className="text-xs text-red-700 mt-1 leading-relaxed">
              {isHi
                ? `${UPAGRAHA_HI[u.name] || u.name} लग्न में होने से जातक की जीवन-शक्ति, स्वास्थ्य एवं समग्र भाग्य पर गहरा पाप-प्रभाव पड़ता है। फलदीपिका के अनुसार यह सर्वाधिक क्रूर संयोगों में से एक है।`
                : `${u.name} occupying the Lagna casts a severe malefic shadow over the native's vitality, health, and overall fortune. Phaladeepika Adh. 25 classifies this as one of the most inauspicious placements.`}
            </p>
          </div>
        </div>
      ))}

      {/* Main table */}
      <div className="bg-muted rounded-xl border border-border p-4">
        <Heading as={4} variant={4} className="mb-3">{t('section.upagrahasTitle')}</Heading>
        <div className="overflow-x-auto">
          <Table className="w-full text-sm min-w-[600px]">
            <TableHeader>
              <TableRow className="bg-muted">
                <TableHead className="text-left p-2 text-primary font-medium w-6"></TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.upagraha')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium">{t('table.house')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.sign')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.longitude')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">{isHi ? 'स्वभाव' : 'Nature'}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
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
                    <TableRow
                      key={u.name}
                      className={`border-t border-border ${hasInterp ? 'cursor-pointer hover:bg-muted/20' : ''} ${isLagna ? 'bg-red-50' : ''}`}
                      onClick={hasInterp ? () => toggle(u.name) : undefined}
                    >
                      <TableCell className="p-2 text-center w-6">
                        {hasInterp && (
                          isOpen
                            ? <ChevronDown className="w-3 h-3 text-primary" />
                            : <ChevronRight className="w-3 h-3 text-primary" />
                        )}
                      </TableCell>
                      <TableCell className="p-2 font-semibold text-foreground">
                        {uLabel(u.name)}
                        {isLagna && <span className="ml-1.5 text-[10px] font-bold text-red-600">⚠</span>}
                      </TableCell>
                      <TableCell className="p-2 text-center text-foreground">
                        {u.house > 0 ? u.house : '—'}
                      </TableCell>
                      <TableCell className="p-2 text-foreground">{translateSign(u.sign, language)}</TableCell>
                      <TableCell className="p-2 text-foreground">
                        {translateNakshatra(u.nakshatra, language) || u.nakshatra}
                        {(u.nakshatra_pada || u.pada) && ` (${t('kundli.pada')} ${u.nakshatra_pada || u.pada})`}
                      </TableCell>
                      <TableCell className="p-2 text-foreground">
                        {typeof u.longitude === 'number' ? u.longitude.toFixed(2) + '°' : u.longitude}
                      </TableCell>
                      <TableCell className="p-2">
                        {u.nature && (
                          <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${natStyle}`}>
                            {natLabel}
                          </span>
                        )}
                      </TableCell>
                    </TableRow>
                    {isOpen && hasInterp && (
                      <TableRow key={`${u.name}-interp`} className="bg-muted/30">
                        <TableCell colSpan={7} className="p-3">
                          {(u.classical_meaning_en || u.classical_meaning_hi) && (
                            <p className="text-xs text-foreground/70 italic mb-1">
                              {isHi ? (u.classical_meaning_hi || u.classical_meaning_en) : (u.classical_meaning_en || u.classical_meaning_hi)}
                            </p>
                          )}
                          <p className="text-xs text-foreground/80 leading-relaxed">
                            {isHi ? (u.interpretation_hi || u.interpretation_en) : (u.interpretation_en || u.interpretation_hi)}
                          </p>
                        </TableCell>
                      </TableRow>
                    )}
                  </>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
