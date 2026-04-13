import { useTranslation } from '@/lib/i18n';
import { CheckCircle, XCircle, AlertCircle, AlertTriangle, ChevronRight, Sparkles } from 'lucide-react';

interface Props { result: any; }

const ROOM_ICONS: Record<string, string> = {
  pooja: '🙏', kitchen: '🍳', master_bedroom: '🛏️', living_room: '🛋️',
  bathroom: '🚿', staircase: '🪜', water_tank_underground: '💧',
  water_tank_overhead: '🏗️', study_room: '📚', children_bedroom: '🧒',
};

const COMPLIANCE_UI: Record<string, { icon: any; bg: string; text: string; border: string; en: string; hi: string }> = {
  ideal:      { icon: CheckCircle,   bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20', en: 'Ideal',      hi: 'आदर्श' },
  acceptable: { icon: CheckCircle,   bg: 'bg-blue-500/10',    text: 'text-blue-400',    border: 'border-blue-500/20',    en: 'Acceptable', hi: 'स्वीकार्य' },
  neutral:    { icon: AlertCircle,   bg: 'bg-slate-500/10',   text: 'text-slate-400',   border: 'border-slate-500/20',   en: 'Neutral',    hi: 'तटस्थ' },
  warning:    { icon: AlertTriangle, bg: 'bg-amber-500/10',   text: 'text-amber-400',   border: 'border-amber-500/20',   en: 'Warning',    hi: 'चेतावनी' },
  avoid:      { icon: XCircle,       bg: 'bg-red-500/10',     text: 'text-red-400',     border: 'border-red-500/20',     en: 'Misplaced',  hi: 'गलत स्थान' },
  blocked:    { icon: XCircle,       bg: 'bg-red-600/15',     text: 'text-red-500',     border: 'border-red-600/30',     en: 'Blocked',    hi: 'वर्जित' },
};

export default function HomeComplianceReport({ result }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  if (!result) return null;

  return (
    <div className="space-y-5 mt-6">
      {/* Overall Score */}
      <div className="bg-white/5 border border-white/10 rounded-xl p-5 flex items-center justify-between">
        <div>
          <p className="text-sm text-cosmic-text/60">{isHi ? 'गृह वास्तु स्कोर' : 'Home Vastu Score'}</p>
          <p className="text-sm text-cosmic-text/70 mt-1">
            {isHi ? result.overall_label_hi : result.overall_label_en}
          </p>
        </div>
        <div className={`text-5xl font-black ${
          result.overall_score >= 80 ? 'text-emerald-400' :
          result.overall_score >= 60 ? 'text-amber-400' : 'text-red-400'
        }`}>
          {result.overall_score}<span className="text-lg text-cosmic-text/30">/100</span>
        </div>
      </div>

      {/* Summary Badges */}
      <div className="flex gap-3 flex-wrap">
        {result.ideal_count > 0 && (
          <span className="px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 text-xs font-bold">
            {result.ideal_count} {isHi ? 'आदर्श' : 'Ideal'}
          </span>
        )}
        {result.acceptable_count > 0 && (
          <span className="px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-400 text-xs font-bold">
            {result.acceptable_count} {isHi ? 'ठीक' : 'OK'}
          </span>
        )}
        {result.neutral_count > 0 && (
          <span className="px-3 py-1.5 rounded-lg bg-slate-500/10 text-slate-400 text-xs font-bold">
            {result.neutral_count} {isHi ? 'तटस्थ' : 'Neutral'}
          </span>
        )}
        {result.avoid_count > 0 && (
          <span className="px-3 py-1.5 rounded-lg bg-red-500/10 text-red-400 text-xs font-bold">
            {result.avoid_count} {isHi ? 'गलत' : 'Misplaced'}
          </span>
        )}
      </div>

      {/* Brahma Sthana Status */}
      <div className={`rounded-xl p-4 border ${
        result.center_status.is_open
          ? 'bg-sacred-gold/5 border-sacred-gold/20'
          : 'bg-red-500/5 border-red-500/20'
      }`}>
        <div className="flex items-center gap-2">
          {result.center_status.is_open
            ? <Sparkles className="w-4 h-4 text-sacred-gold" />
            : <AlertTriangle className="w-4 h-4 text-red-400" />
          }
          <span className="text-sm font-semibold text-cosmic-text">
            {isHi ? 'ब्रह्म स्थान' : 'Brahma Sthana'}
          </span>
        </div>
        <p className="text-xs text-cosmic-text mt-1">
          {isHi ? result.center_status.assessment_hi : result.center_status.assessment_en}
        </p>
      </div>

      {/* Per-Room Cards */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-cosmic-text">{isHi ? 'कमरा-वार विश्लेषण' : 'Room-by-Room Analysis'}</h3>
        {result.room_results.map((r: any, i: number) => {
          const ui = COMPLIANCE_UI[r.compliance] || COMPLIANCE_UI.neutral;
          const Icon = ui.icon;
          return (
            <div key={i} className={`${ui.bg} border ${ui.border} rounded-xl p-4`}>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-lg">{ROOM_ICONS[r.room_type] || '🏠'}</span>
                <div className="flex-1">
                  <p className="text-sm font-bold text-cosmic-text">{isHi ? r.room_name_hi : r.room_name_en}</p>
                  <p className="text-[10px] text-cosmic-text/50">
                    {isHi ? r.assigned_direction_hi : r.assigned_direction_en} ({r.assigned_direction})
                  </p>
                </div>
                <div className={`flex items-center gap-1 px-2 py-0.5 rounded ${ui.bg}`}>
                  <Icon className={`w-3.5 h-3.5 ${ui.text}`} />
                  <span className={`text-[10px] font-bold ${ui.text} uppercase`}>
                    {isHi ? ui.hi : ui.en}
                  </span>
                </div>
              </div>

              {/* Reason */}
              <p className="text-xs text-cosmic-text/70 mb-2">{isHi ? r.reason_hi : r.reason_en}</p>

              {/* Ideal directions hint */}
              {r.compliance !== 'ideal' && (
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-[10px] text-cosmic-text/50">{isHi ? 'आदर्श:' : 'Ideal:'}</span>
                  {(isHi ? r.ideal_directions_hi : r.ideal_directions).map((d: string, di: number) => (
                    <span key={di} className="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[9px] font-bold">{d}</span>
                  ))}
                </div>
              )}

              {/* Tips */}
              <div className="space-y-1 mb-2">
                {(isHi ? r.tips_hi : r.tips_en).slice(0, 2).map((tip: string, ti: number) => (
                  <div key={ti} className="flex items-start gap-1">
                    <ChevronRight className="w-3 h-3 text-sacred-gold mt-0.5 flex-shrink-0" />
                    <p className="text-[10px] text-cosmic-text/60">{tip}</p>
                  </div>
                ))}
              </div>

              {/* Remedies for misplaced */}
              {r.remedies && r.compliance !== 'warning' && (
                <div className="bg-black/20 rounded-lg p-3 mt-2 space-y-2">
                  <p className="text-[10px] font-bold text-red-400 uppercase">
                    {isHi ? 'उपाय' : 'Remedies'}
                  </p>
                  <p className="text-xs text-cosmic-text">{isHi ? r.remedies.relocation_hi : r.remedies.relocation_en}</p>
                  {r.remedies.explanation_en && (
                    <p className="text-[10px] text-cosmic-text/60 italic">
                      {isHi ? r.remedies.explanation_hi : r.remedies.explanation_en}
                    </p>
                  )}
                  {r.remedies.metal_strip && (
                    <div className="flex items-center gap-2 text-[10px]">
                      <span className="text-sacred-gold font-semibold">{isHi ? 'धातु:' : 'Metal:'}</span>
                      <span className="text-cosmic-text">{isHi ? r.remedies.metal_strip.metal_hi : r.remedies.metal_strip.metal}</span>
                    </div>
                  )}
                  {r.remedies.color_therapy && (
                    <div className="flex items-center gap-2 text-[10px] flex-wrap">
                      <span className="text-sacred-gold font-semibold">{isHi ? 'रंग:' : 'Colors:'}</span>
                      {(isHi ? r.remedies.color_therapy.colors_hi : r.remedies.color_therapy.colors).map((c: string, ci: number) => (
                        <span key={ci} className="px-1.5 py-0.5 rounded bg-white/10 text-cosmic-text text-[9px]">{c}</span>
                      ))}
                    </div>
                  )}
                  {r.remedies.mantras?.map((m: any, mi: number) => (
                    <div key={mi} className="text-[10px]">
                      <span className="text-sacred-gold/60 italic">{m.mantra}</span>
                      <span className="text-cosmic-text/40 ml-1">— {isHi ? m.devta_hi : m.devta}</span>
                    </div>
                  ))}
                </div>
              )}

              {/* Brahma Sthana soft warning */}
              {r.remedies && r.compliance === 'warning' && (
                <div className="bg-amber-500/5 border border-amber-500/20 rounded-lg p-3 mt-2">
                  <p className="text-xs text-amber-400">{isHi ? r.remedies.relocation_hi : r.remedies.relocation_en}</p>
                </div>
              )}

              {/* Zone Devtas */}
              {r.zone_devtas?.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {r.zone_devtas.map((d: any, di: number) => (
                    <span key={di} className="text-[9px] px-1.5 py-0.5 rounded bg-white/5 text-cosmic-text/40">
                      {isHi ? d.name_hi : d.name}
                    </span>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Missing Critical Rooms */}
      {result.missing_critical_rooms?.length > 0 && (
        <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4">
          <h4 className="text-xs font-bold text-amber-400 mb-2">
            {isHi ? 'गायब महत्वपूर्ण कमरे' : 'Missing Critical Rooms'}
          </h4>
          {result.missing_critical_rooms.map((m: any, i: number) => (
            <div key={i} className="flex items-center gap-2 mb-1">
              <span className="text-sm">{ROOM_ICONS[m.room_type] || '🏠'}</span>
              <span className="text-xs text-cosmic-text">{isHi ? m.room_name_hi : m.room_name_en}</span>
              <span className="text-[9px] text-cosmic-text/40">→ {(isHi ? m.ideal_directions_hi : m.ideal_directions).join(', ')}</span>
            </div>
          ))}
        </div>
      )}

      {/* Duplicate Warnings */}
      {result.duplicate_warnings?.length > 0 && (
        <div className="bg-blue-500/5 border border-blue-500/20 rounded-xl p-4">
          {result.duplicate_warnings.map((d: any, i: number) => (
            <p key={i} className="text-xs text-blue-400">
              {isHi ? d.message_hi : d.message_en}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
