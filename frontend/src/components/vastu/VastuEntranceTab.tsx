import { useTranslation } from '@/lib/i18n';
import { DoorOpen, Star, AlertTriangle, ChevronRight } from 'lucide-react';
import VastuCompass from './VastuCompass';
import { Heading } from "@/components/ui/heading";

interface Props { data: any; }

const qualityColors: Record<string, string> = {
  SUPREME:   'bg-amber-500/20 text-amber-400 border-amber-500/30',
  EXCELLENT: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  GOOD:      'bg-green-500/20 text-green-400 border-green-500/30',
  NEUTRAL:   'bg-blue-500/20 text-blue-400 border-blue-500/30',
  CHALLENGE: 'bg-red-500/20 text-red-400 border-red-500/30',
};

function ScoreBar({ score, max = 5 }: { score: number; max?: number }) {
  return (
    <div className="flex gap-1">
      {Array.from({ length: max }, (_, i) => (
        <div
          key={i}
          className={`w-6 h-2 rounded-full ${
            i < score
              ? score >= 4 ? 'bg-emerald-400' : score >= 3 ? 'bg-blue-400' : 'bg-red-400'
              : 'bg-white/10'
          }`}
        />
      ))}
    </div>
  );
}

export default function VastuEntranceTab({ data }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const entrance = data?.entrance_analysis || data;

  if (!entrance || entrance.error) {
    return (
      <div className="text-center py-12 text-foreground/60">
        {t('auto.noEntranceAnalysisAv')}
      </div>
    );
  }

  const qStyle = qualityColors[entrance.quality] || qualityColors.NEUTRAL;

  return (
    <div className="space-y-6">
      {/* Main Pada Result */}
      <div className="bg-white/5 border border-white/10 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <DoorOpen className="w-6 h-6 text-sacred-gold" />
          <div>
            <Heading as={3} variant={3}>
              {t('auto.entrancePadaAnalysis')}
            </Heading>
            <p className="text-sm text-foreground/60">
              {t('auto.basedOnThe32PadaSyst')}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-sm text-foreground/60">{t('auto.padaCode')}</p>
            <p className="text-2xl font-bold text-sacred-gold">{entrance.pada}</p>
          </div>
          <div>
            <p className="text-sm text-foreground/60">{t('auto.padaName')}</p>
            <p className="text-xl font-bold text-foreground">{entrance.pada_name}</p>
            {isHi && <p className="text-sm text-foreground/70">{entrance.pada_name_hi}</p>}
          </div>
        </div>

        {/* Quality Badge */}
        <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg border ${qStyle} mb-4`}>
          {entrance.score >= 4 ? <Star className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
          <span className="font-bold text-sm">{isHi ? entrance.quality_hi : entrance.quality}</span>
        </div>

        {/* Score */}
        <div className="mb-4">
          <div className="flex items-center gap-3">
            <p className="text-sm text-foreground/60">{t('auto.qualityScore')}</p>
            <ScoreBar score={entrance.score} />
            <span className="text-sm font-bold text-foreground">{entrance.score}/{entrance.score_max}</span>
          </div>
        </div>

        {/* Effects */}
        <div className="bg-white/5 rounded-lg p-4">
          <p className="text-sm text-foreground/60 mb-1">{t('auto.effects')}</p>
          <p className="text-sm text-foreground leading-relaxed">{isHi ? entrance.effects_hi : entrance.effects_en}</p>
        </div>
      </div>

      {/* Compass Display — highlighted pada */}
      <div className="bg-white/5 border border-white/10 rounded-xl p-5">
        <Heading as={4} variant={4}>
          {t('auto.compassViewYourEntra')}
        </Heading>
        <VastuCompass
          value={entrance.direction}
          onChange={() => {}}
          mode="display"
          highlightedPada={entrance.pada}
        />
      </div>

      {/* Ruling Devta */}
      {entrance.ruling_devta && (
        <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-5">
          <Heading as={4} variant={4}>{t('auto.rulingDeity')}</Heading>
          <p className="text-lg font-bold text-foreground">
            {entrance.ruling_devta.name}
            {isHi && <span className="text-base text-foreground/70 ml-2">{entrance.ruling_devta.name_hi}</span>}
          </p>
          <p className="text-sm text-foreground/70 mt-1">
            {isHi ? entrance.ruling_devta.description_hi : entrance.ruling_devta.description_en}
          </p>
          <p className="text-sm text-sacred-gold/60 italic mt-2">{entrance.ruling_devta.mantra}</p>
        </div>
      )}

      {/* All Padas in this Direction */}
      {entrance.all_padas_in_direction && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <Heading as={4} variant={4}>
            {t('auto.all8PadasInEntranceD')}
          </Heading>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {entrance.all_padas_in_direction.map((p: any) => {
              const pStyle = qualityColors[p.quality] || qualityColors.NEUTRAL;
              const isCurrent = p.pada === entrance.pada;
              return (
                <div
                  key={p.pada}
                  className={`p-3 rounded-lg border text-center transition-all ${
                    isCurrent ? `${pStyle} border-2 ring-1 ring-white/20` : 'border-white/5 bg-white/5'
                  }`}
                >
                  <p className={`text-sm font-bold ${isCurrent ? '' : 'text-foreground/60'}`}>{p.pada}</p>
                  <p className={`text-sm font-semibold ${isCurrent ? '' : 'text-foreground/70'}`}>{p.name}</p>
                  {isHi && <p className="text-sm text-foreground/50">{p.name_hi}</p>}
                  <ScoreBar score={p.score} />
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Best & Worst in Direction */}
      <div className="grid grid-cols-2 gap-4">
        {entrance.best_pada_in_direction && (
          <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-4">
            <p className="text-sm text-emerald-400 font-semibold mb-1">{t('auto.bestPada')}</p>
            <p className="text-lg font-bold text-foreground">{entrance.best_pada_in_direction.pada}</p>
            <p className="text-sm text-foreground">{entrance.best_pada_in_direction.name}</p>
            {isHi && <p className="text-sm text-foreground/60">{entrance.best_pada_in_direction.name_hi}</p>}
          </div>
        )}
        {entrance.worst_pada_in_direction && (
          <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-4">
            <p className="text-sm text-red-400 font-semibold mb-1">{t('auto.worstPada')}</p>
            <p className="text-lg font-bold text-foreground">{entrance.worst_pada_in_direction.pada}</p>
            <p className="text-sm text-foreground">{entrance.worst_pada_in_direction.name}</p>
            {isHi && <p className="text-sm text-foreground/60">{entrance.worst_pada_in_direction.name_hi}</p>}
          </div>
        )}
      </div>

      {/* Entrance Remedies */}
      {entrance.remedies && entrance.remedies.length > 0 && (
        <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-5">
          <Heading as={4} variant={4}>
            {t('auto.entranceRemedies')}
          </Heading>
          <div className="space-y-3">
            {entrance.remedies.map((r: any, i: number) => (
              <div key={i} className="flex items-start gap-2">
                <ChevronRight className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-foreground/60 uppercase">{isHi ? r.type_hi : r.type}</p>
                  <p className="text-sm text-foreground">{isHi ? r.remedy_hi : r.remedy_en}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}