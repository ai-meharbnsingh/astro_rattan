import { Loader2 } from 'lucide-react';

interface AvakhadaTabProps {
  avakhadaData: any;
  loadingAvakhada: boolean;
  t: (key: string) => string;
}

export default function AvakhadaTab({ avakhadaData, loadingAvakhada, t }: AvakhadaTabProps) {
  if (loadingAvakhada) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-cosmic-text">{t('kundli.calculatingAvakhada')}</span>
      </div>
    );
  }

  if (!avakhadaData) {
    return <p className="text-center text-cosmic-text py-8">{t('kundli.clickAvakhadaTab')}</p>;
  }

  return (
    <div className="space-y-4">
      <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold rounded-xl p-4 border border-sacred-gold mb-4">
        <h4 className="font-display font-bold text-lg" style={{ color: 'var(--ink)' }}>{t('section.avakhadaChakra')}</h4>
        <p className="text-sm text-cosmic-text">{t('avakhada.birthSummary')}</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {[
          { label: t('avakhada.ascendant'), value: avakhadaData.ascendant },
          { label: t('avakhada.ascendantLord'), value: avakhadaData.ascendant_lord },
          { label: t('avakhada.rashi'), value: avakhadaData.rashi },
          { label: t('avakhada.rashiLord'), value: avakhadaData.rashi_lord },
          { label: t('avakhada.nakshatra'), value: `${avakhadaData.nakshatra} (${t('kundli.pada')} ${avakhadaData.nakshatra_pada})` },
          { label: t('avakhada.yoga'), value: avakhadaData.yoga },
          { label: t('avakhada.karana'), value: avakhadaData.karana },
          { label: t('avakhada.yoni'), value: avakhadaData.yoni },
          { label: t('avakhada.gana'), value: avakhadaData.gana },
          { label: t('avakhada.nadi'), value: avakhadaData.nadi },
          { label: t('avakhada.varna'), value: avakhadaData.varna },
          { label: t('avakhada.naamakshar'), value: avakhadaData.naamakshar },
          { label: t('avakhada.sunSign'), value: avakhadaData.sun_sign },
          { label: t('avakhada.tithi'), value: avakhadaData.tithi ? `${avakhadaData.tithi} (${avakhadaData.tithi_paksha})` : undefined },
          { label: t('avakhada.tithiLord'), value: avakhadaData.tithi_lord },
          { label: t('avakhada.vaar'), value: avakhadaData.vaar ? `${avakhadaData.vaar} (${avakhadaData.vaar_lord})` : undefined },
          { label: t('avakhada.payaNakshatra'), value: avakhadaData.paya_nakshatra },
          { label: t('avakhada.payaChandra'), value: avakhadaData.paya_chandra },
        ].filter(item => item.value).map((item) => (
          <div
            key={item.label}
            className="rounded-xl p-4 border"
            style={{ backgroundColor: 'var(--parchment)', borderColor: 'rgba(184,134,11,0.2)' }}
          >
            <p className="text-sm font-medium mb-1" style={{ color: 'var(--ink-light)' }}>{item.label}</p>
            <p className="font-display font-semibold text-base" style={{ color: 'var(--ink)' }}>{item.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
