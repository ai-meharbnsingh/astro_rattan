import { useTranslation } from '@/lib/i18n';
import { Wrench, Palette, BookOpen, Sparkles, ChevronRight } from 'lucide-react';
import { Heading } from "@/components/ui/heading";

interface Props { data: any; }

export default function VastuRemediesTab({ data }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const remedies = data?.remedies || data;

  if (!remedies) {
    return (
      <div className="text-center py-12 text-foreground/60">
        {t('auto.selectProblemsToSeeR')}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Problems Analyzed */}
      {remedies.problems_analyzed?.length > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <Heading as={3} variant={3}>{t('auto.problemsAnalyzed')}</Heading>
          <div className="flex flex-wrap gap-2">
            {remedies.problems_analyzed.map((p: string) => (
              <span key={p} className="px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 text-sm font-medium capitalize">
                {p}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Metal Strip Remedies */}
      {remedies.metal_strip_remedies?.length > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-base font-bold text-sacred-gold flex items-center gap-2 mb-4">
            <Wrench className="w-5 h-5" />
            {t('auto.metalStripRemedies')}
          </h3>
          <div className="space-y-3">
            {remedies.metal_strip_remedies.map((m: any, i: number) => (
              <div key={i} className="bg-white/5 rounded-lg p-4 border border-white/5">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-foreground">{isHi ? m.direction_hi : m.direction_en}</span>
                  <span className="px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold text-sm font-bold">
                    {isHi ? m.metal_hi : m.metal}
                  </span>
                </div>
                <p className="text-sm text-foreground">{isHi ? m.purpose_hi : m.purpose_en}</p>
                <p className="text-sm text-foreground/60 mt-1 italic">{isHi ? m.placement_hi : m.placement_en}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Color Therapy */}
      {remedies.color_therapy?.length > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-base font-bold text-sacred-gold flex items-center gap-2 mb-4">
            <Palette className="w-5 h-5" />
            {t('auto.colorTherapy')}
          </h3>
          <div className="space-y-3">
            {remedies.color_therapy.map((c: any, i: number) => (
              <div key={i} className="bg-white/5 rounded-lg p-4 border border-white/5">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-foreground">{isHi ? c.direction_hi : c.direction_en}</span>
                  <span className="text-sm text-foreground/60">{c.element}</span>
                </div>
                <div className="flex flex-wrap gap-2 mb-2">
                  {(isHi ? c.colors_hi : c.colors).map((color: string, ci: number) => (
                    <span key={ci} className="px-2 py-0.5 rounded bg-white/10 text-foreground text-sm font-medium">
                      {color}
                    </span>
                  ))}
                </div>
                <p className="text-sm text-foreground/70">{isHi ? c.reasoning_hi : c.reasoning_en}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Mantras */}
      {remedies.mantras?.length > 0 && (
        <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-5">
          <h3 className="text-base font-bold text-sacred-gold flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5" />
            {t('auto.mantras')}
          </h3>
          <div className="space-y-3">
            {remedies.mantras.map((m: any, i: number) => (
              <div key={i} className="bg-white/5 rounded-lg p-4 border border-white/5">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-foreground">{m.devta}</span>
                  {isHi && <span className="text-sm text-foreground/60">({m.devta_hi})</span>}
                </div>
                <p className="text-sm text-sacred-gold font-mono italic mb-2">{m.mantra}</p>
                <p className="text-sm text-foreground">{isHi ? m.method_hi : m.method_en}</p>
                <p className="text-sm text-foreground/60 mt-1">{isHi ? m.purpose_hi : m.purpose_en}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Room Adjustments */}
      {remedies.room_adjustments?.length > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <Heading as={3} variant={3}>{t('auto.roomAdjustments')}</Heading>
          <div className="space-y-4">
            {remedies.room_adjustments.map((r: any, i: number) => (
              <div key={i} className="bg-white/5 rounded-lg p-4 border border-white/5">
                <p className="font-bold text-foreground mb-1">{isHi ? r.room_name_hi : r.room_name_en}</p>
                <p className="text-sm text-foreground mb-2">{isHi ? r.recommendation_hi : r.recommendation_en}</p>
                <p className="text-sm text-foreground/60">{isHi ? r.reason_hi : r.reason_en}</p>
                <div className="mt-2 space-y-1">
                  {(isHi ? r.tips_hi : r.tips_en).map((tip: string, ti: number) => (
                    <div key={ti} className="flex items-start gap-1.5">
                      <ChevronRight className="w-3 h-3 text-sacred-gold mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-foreground">{tip}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* General Remedies */}
      {remedies.general_remedies?.length > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-base font-bold text-sacred-gold flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5" />
            {t('auto.generalVastuRemedies')}
          </h3>
          <div className="space-y-2">
            {remedies.general_remedies.map((r: any, i: number) => (
              <div key={i} className="flex items-start gap-2">
                <ChevronRight className="w-4 h-4 text-sacred-gold mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-foreground">{isHi ? r.remedy_hi : r.remedy_en}</p>
                  <span className="text-sm text-foreground/50 uppercase">{r.category}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}