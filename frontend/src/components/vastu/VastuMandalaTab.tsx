import { useTranslation } from '@/lib/i18n';
import { Grid3X3, Sparkles, Shield, AlertTriangle, Star } from 'lucide-react';
import VastuMandalaGrid from './VastuMandalaGrid';

interface Props { data: any; }

const natureStyles: Record<string, { bg: string; text: string; icon: any }> = {
  supreme:  { bg: 'bg-amber-500/20', text: 'text-amber-400', icon: Star },
  positive: { bg: 'bg-emerald-500/20', text: 'text-emerald-400', icon: Sparkles },
  neutral:  { bg: 'bg-blue-500/20', text: 'text-blue-400', icon: Shield },
  negative: { bg: 'bg-red-500/20', text: 'text-red-400', icon: AlertTriangle },
  fierce:   { bg: 'bg-orange-500/20', text: 'text-orange-400', icon: AlertTriangle },
};

export default function VastuMandalaTab({ data }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const mandala = data?.mandala || data;
  const zones = mandala?.zones || {};
  const energy = mandala?.energy_balance;
  const body = mandala?.body_mapping;

  return (
    <div className="space-y-6">
      {/* Grid Info */}
      <div className="bg-white/5 border border-white/10 rounded-xl p-5">
        <h3 className="text-lg font-bold text-sacred-gold flex items-center gap-2 mb-3">
          <Grid3X3 className="w-5 h-5" />
          {t('auto.vastuPurushaMandala')}
        </h3>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <p className="text-cosmic-text/60">{t('auto.gridType')}</p>
            <p className="font-semibold text-cosmic-text">{isHi ? mandala?.grid_type_hi : mandala?.grid_type}</p>
          </div>
          <div>
            <p className="text-cosmic-text/60">{t('auto.totalSquares')}</p>
            <p className="font-semibold text-cosmic-text">{mandala?.total_squares}</p>
          </div>
          <div>
            <p className="text-cosmic-text/60">{t('auto.totalDevtas')}</p>
            <p className="font-semibold text-cosmic-text">45</p>
          </div>
        </div>
      </div>

      {/* Interactive Mandala Grid */}
      {zones && Object.keys(zones).length > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-base font-bold text-sacred-gold mb-3">
            {t('auto.mandalaGridClickToEx')}
          </h3>
          <VastuMandalaGrid zones={zones} />
        </div>
      )}

      {/* Energy Balance */}
      {energy && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-base font-bold text-cosmic-text mb-3">{t('auto.energyBalance')}</h3>
          <div className="flex gap-4 mb-3">
            <div className="flex-1 bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold text-emerald-400">{energy.positive}</p>
              <p className="text-sm text-emerald-300">{t('auto.positive')}</p>
            </div>
            <div className="flex-1 bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold text-red-400">{energy.negative}</p>
              <p className="text-sm text-red-300">{t('auto.negative')}</p>
            </div>
            <div className="flex-1 bg-blue-500/10 border border-blue-500/20 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold text-blue-400">{energy.neutral}</p>
              <p className="text-sm text-blue-300">{t('auto.neutral')}</p>
            </div>
          </div>
          <p className="text-sm text-cosmic-text">{isHi ? energy.assessment_hi : energy.assessment_en}</p>
        </div>
      )}

      {/* Body Mapping */}
      {body && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-base font-bold text-sacred-gold mb-3">{t('auto.vastuPurushaBodyMap')}</h3>
          <div className="grid grid-cols-3 gap-3">
            {Object.entries(body).map(([part, info]: [string, any]) => (
              <div key={part} className="bg-white/5 rounded-lg p-3">
                <p className="text-sm text-sacred-gold font-semibold capitalize">{part.replace('_', ' ')}</p>
                <p className="text-sm font-bold text-cosmic-text">{isHi ? info.direction_hi : info.direction}</p>
                <p className="text-sm text-cosmic-text/70 mt-1">{isHi ? info.significance_hi : info.significance_en}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Zones with Devtas */}
      {Object.entries(zones).map(([zoneName, zone]: [string, any]) => (
        <div key={zoneName} className="bg-white/5 border border-white/10 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-cosmic-text">
              {isHi ? zone.zone_hi : zone.zone_en}
            </h3>
            <div className="flex gap-2 text-sm">
              {zone.positive_count > 0 && <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">+{zone.positive_count}</span>}
              {zone.negative_count > 0 && <span className="px-2 py-0.5 rounded bg-red-500/20 text-red-400">-{zone.negative_count}</span>}
              {zone.neutral_count > 0 && <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400">~{zone.neutral_count}</span>}
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {zone.devtas.map((d: any) => {
              const style = natureStyles[d.nature] || natureStyles.neutral;
              const Icon = style.icon;
              return (
                <div key={d.id} className={`${style.bg} border border-white/5 rounded-lg p-3`}>
                  <div className="flex items-center gap-2 mb-1">
                    <Icon className={`w-4 h-4 ${style.text}`} />
                    <span className="font-bold text-sm text-cosmic-text">{d.name}</span>
                    <span className="text-sm text-cosmic-text/60">({isHi ? d.name_hi : d.name})</span>
                  </div>
                  {isHi && <p className="text-sm font-semibold text-cosmic-text/80 mb-1">{d.name_hi}</p>}
                  <p className="text-sm text-cosmic-text/70 mb-2">{isHi ? d.description_hi : d.description_en}</p>
                  <div className="flex flex-wrap gap-2 text-sm">
                    <span className="px-1.5 py-0.5 rounded bg-white/5 text-cosmic-text">{isHi ? d.element_hi : d.element}</span>
                    <span className="px-1.5 py-0.5 rounded bg-white/5 text-cosmic-text">{isHi ? d.direction_hi : d.direction}</span>
                    <span className="px-1.5 py-0.5 rounded bg-white/5 text-cosmic-text">{isHi ? d.body_part_hi : d.body_part}</span>
                  </div>
                  <p className="text-sm text-sacred-gold/60 mt-1.5 italic">{d.mantra}</p>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
