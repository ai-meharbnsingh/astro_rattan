import { useTranslation } from '@/lib/i18n';
import { HomeIcon, CheckCircle, XCircle, AlertCircle, ChevronRight } from 'lucide-react';

interface Props { data: any; }

const ROOM_ICONS: Record<string, string> = {
  pooja: '🙏', kitchen: '🍳', master_bedroom: '🛏️', living_room: '🛋️',
  bathroom: '🚿', staircase: '🪜', water_tank_underground: '💧',
  water_tank_overhead: '🏗️', study_room: '📚', children_bedroom: '🧒',
};

export default function VastuRoomPlacementTab({ data }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const placement = data?.room_placement || data;
  const rooms = placement?.rooms || {};

  return (
    <div className="space-y-6">
      <div className="bg-white/5 border border-white/10 rounded-xl p-5">
        <h3 className="text-lg font-bold text-sacred-gold flex items-center gap-2 mb-2">
          <HomeIcon className="w-5 h-5" />
          {isHi ? 'वास्तु अनुसार कमरा व्यवस्था' : 'Vastu Room Placement Guide'}
        </h3>
        <p className="text-sm text-cosmic-text/60">
          {isHi
            ? 'प्राचीन वास्तु शास्त्र के अनुसार प्रत्येक कमरे की आदर्श दिशा'
            : 'Ideal direction for each room according to ancient Vastu Shastra principles'}
        </p>
      </div>

      {Object.entries(rooms).map(([key, room]: [string, any]) => (
        <div key={key} className="bg-white/5 border border-white/10 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">{ROOM_ICONS[key] || '🏠'}</span>
            <div>
              <h4 className="text-base font-bold text-cosmic-text">{isHi ? room.room_name_hi : room.room_name_en}</h4>
            </div>
          </div>

          {/* Direction Grid */}
          <div className="grid grid-cols-3 gap-3 mb-4">
            {/* Ideal */}
            <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-lg p-3">
              <div className="flex items-center gap-1 mb-2">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                <p className="text-xs font-semibold text-emerald-400">{isHi ? 'आदर्श' : 'Ideal'}</p>
              </div>
              <div className="flex flex-wrap gap-1">
                {(isHi ? room.ideal_directions_hi : room.ideal_directions).map((d: string, i: number) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 text-xs font-bold">
                    {d}
                  </span>
                ))}
              </div>
            </div>

            {/* Acceptable */}
            <div className="bg-blue-500/5 border border-blue-500/20 rounded-lg p-3">
              <div className="flex items-center gap-1 mb-2">
                <AlertCircle className="w-3.5 h-3.5 text-blue-400" />
                <p className="text-xs font-semibold text-blue-400">{isHi ? 'स्वीकार्य' : 'OK'}</p>
              </div>
              <div className="flex flex-wrap gap-1">
                {(isHi ? room.acceptable_directions_hi : room.acceptable_directions).length > 0 ? (
                  (isHi ? room.acceptable_directions_hi : room.acceptable_directions).map((d: string, i: number) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 text-xs font-bold">
                      {d}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-cosmic-text/40">—</span>
                )}
              </div>
            </div>

            {/* Avoid */}
            <div className="bg-red-500/5 border border-red-500/20 rounded-lg p-3">
              <div className="flex items-center gap-1 mb-2">
                <XCircle className="w-3.5 h-3.5 text-red-400" />
                <p className="text-xs font-semibold text-red-400">{isHi ? 'बचें' : 'Avoid'}</p>
              </div>
              <div className="flex flex-wrap gap-1">
                {(isHi ? room.avoid_directions_hi : room.avoid_directions).map((d: string, i: number) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-red-500/10 text-red-300 text-xs font-bold">
                    {d}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Reason */}
          <div className="bg-white/5 rounded-lg p-3 mb-3">
            <p className="text-xs text-cosmic-text/60 mb-1">{isHi ? 'कारण' : 'Reason'}</p>
            <p className="text-sm text-cosmic-text">{isHi ? room.reason_hi : room.reason_en}</p>
          </div>

          {/* Tips */}
          <div className="space-y-1.5">
            <p className="text-xs font-semibold text-sacred-gold">{isHi ? 'सुझाव' : 'Tips'}</p>
            {(isHi ? room.tips_hi : room.tips_en).map((tip: string, ti: number) => (
              <div key={ti} className="flex items-start gap-1.5">
                <ChevronRight className="w-3 h-3 text-sacred-gold mt-0.5 flex-shrink-0" />
                <p className="text-xs text-cosmic-text">{tip}</p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
