import { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Plus, X, AlertTriangle } from 'lucide-react';

interface DirectionSummary {
  rooms: string[];
  element: string;
  element_hi: string;
  status: string;
}

interface GridLayoutResult {
  direction_summary?: Record<string, DirectionSummary>;
}

interface RoomPlacementInfo {
  ideal_directions?: string[];
  acceptable_directions?: string[];
  avoid_directions?: string[];
}

interface Props {
  assignments: Record<string, string[]>;
  onAssign: (direction: string, roomType: string) => void;
  onRemove: (direction: string, roomType: string) => void;
  layoutResult?: GridLayoutResult;
  roomPlacementData?: Record<string, RoomPlacementInfo>;
}

const ZONE_ORDER = ['NW', 'N', 'NE', 'W', 'Center', 'E', 'SW', 'S', 'SE'];

const ZONE_LABELS: Record<string, { en: string; hi: string }> = {
  NW: { en: 'Northwest', hi: 'वायव्य' },  N: { en: 'North', hi: 'उत्तर' },
  NE: { en: 'Northeast', hi: 'ईशान' },    W: { en: 'West', hi: 'पश्चिम' },
  Center: { en: 'Center', hi: 'केंद्र' },  E: { en: 'East', hi: 'पूर्व' },
  SW: { en: 'Southwest', hi: 'नैऋत्य' },  S: { en: 'South', hi: 'दक्षिण' },
  SE: { en: 'Southeast', hi: 'आग्नेय' },
};

const ROOM_OPTIONS: { key: string; en: string; hi: string; icon: string }[] = [
  { key: 'pooja',                  en: 'Pooja Room',       hi: 'पूजा कक्ष',           icon: '🙏' },
  { key: 'kitchen',                en: 'Kitchen',          hi: 'रसोई',                icon: '🍳' },
  { key: 'master_bedroom',        en: 'Master Bedroom',   hi: 'मुख्य शयनकक्ष',       icon: '🛏️' },
  { key: 'living_room',           en: 'Living Room',      hi: 'बैठक',                icon: '🛋️' },
  { key: 'bathroom',              en: 'Bathroom',         hi: 'स्नानघर',             icon: '🚿' },
  { key: 'staircase',             en: 'Staircase',        hi: 'सीढ़ी',               icon: '🪜' },
  { key: 'water_tank_underground', en: 'UG Water Tank',   hi: 'भूमिगत टंकी',         icon: '💧' },
  { key: 'water_tank_overhead',   en: 'OH Water Tank',    hi: 'ऊपरी टंकी',           icon: '🏗️' },
  { key: 'study_room',            en: 'Study Room',       hi: 'अध्ययन कक्ष',         icon: '📚' },
  { key: 'children_bedroom',      en: 'Children Room',    hi: 'बच्चों का कमरा',       icon: '🧒' },
];

const CENTER_HARD_BLOCK = new Set(['kitchen', 'bathroom', 'staircase']);

function getComplianceForRoomInZone(
  roomKey: string,
  direction: string,
  rpData?: Record<string, any>,
): 'ideal' | 'acceptable' | 'neutral' | 'avoid' | 'blocked' {
  if (!rpData || !rpData[roomKey]) return 'neutral';
  const room = rpData[roomKey];
  if (direction === 'Center') {
    if (CENTER_HARD_BLOCK.has(roomKey)) return 'blocked';
    if (room.avoid_directions?.includes('Center')) return 'avoid';
    return 'neutral';
  }
  if (room.ideal_directions?.includes(direction)) return 'ideal';
  if (room.acceptable_directions?.includes(direction)) return 'acceptable';
  if (room.avoid_directions?.includes(direction)) return 'avoid';
  return 'neutral';
}

const COMPLIANCE_STYLE: Record<string, { border: string; dot: string; label: string; labelHi: string }> = {
  ideal:      { border: 'border-emerald-500', dot: 'bg-emerald-400', label: 'Ideal', labelHi: 'आदर्श' },
  acceptable: { border: 'border-blue-500',    dot: 'bg-blue-400',    label: 'OK', labelHi: 'ठीक' },
  neutral:    { border: 'border-slate-500',   dot: 'bg-slate-400',   label: 'Neutral', labelHi: 'तटस्थ' },
  avoid:      { border: 'border-red-500',     dot: 'bg-red-400',     label: 'Avoid', labelHi: 'बचें' },
  blocked:    { border: 'border-red-600',     dot: 'bg-red-600',     label: 'Blocked', labelHi: 'वर्जित' },
};

export default function HomeGrid({ assignments, onAssign, onRemove, layoutResult, roomPlacementData }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  const getZoneStatus = (dir: string): string | null => {
    if (!layoutResult) return null;
    const ds = layoutResult.direction_summary?.[dir];
    return ds?.status || null;
  };

  return (
    <div className="grid grid-cols-3 gap-2 max-w-lg mx-auto">
      {ZONE_ORDER.map(dir => {
        const rooms = assignments[dir] || [];
        const isCenter = dir === 'Center';
        const zoneStatus = getZoneStatus(dir);
        const statusBorder = zoneStatus === 'misplaced' ? 'border-red-500/60' : zoneStatus === 'ideal' ? 'border-emerald-500/60' : '';

        return (
          <div
            key={dir}
            className={`relative min-h-[120px] rounded-xl border-2 p-3 transition-all ${
              isCenter
                ? 'border-dashed border-sacred-gold/40 bg-sacred-gold/5'
                : statusBorder || 'border-white/10 bg-white/5'
            }`}
          >
            {/* Direction Label */}
            <div className="text-center mb-2">
              <span className="text-sm font-bold text-sacred-gold">{dir}</span>
              <span className="text-sm text-cosmic-text/50 ml-1">
                {isHi ? ZONE_LABELS[dir].hi : ZONE_LABELS[dir].en}
              </span>
            </div>

            {/* Brahma Sthana label */}
            {isCenter && rooms.length === 0 && (
              <p className="text-sm text-sacred-gold/50 text-center italic">
                {t('auto.brahmaSthanaKeepOpen')}
              </p>
            )}

            {/* Assigned Rooms */}
            <div className="space-y-1.5">
              {rooms.map((roomKey, i) => {
                const opt = ROOM_OPTIONS.find(r => r.key === roomKey);
                const comp = getComplianceForRoomInZone(roomKey, dir, roomPlacementData);
                const style = COMPLIANCE_STYLE[comp];
                return (
                  <div key={`${roomKey}-${i}`} className={`flex items-center gap-1.5 bg-white/5 rounded-lg px-2 py-1.5 border ${style.border}/30`}>
                    <span className="text-sm">{opt?.icon || '🏠'}</span>
                    <span className="text-sm font-medium text-cosmic-text flex-1 truncate">
                      {isHi ? (opt?.hi || roomKey) : (opt?.en || roomKey)}
                    </span>
                    <div className={`w-2 h-2 rounded-full ${style.dot}`} title={isHi ? style.labelHi : style.label} />
                    <button
                      onClick={() => onRemove(dir, roomKey)}
                      className="text-cosmic-text/30 hover:text-red-400 transition-colors"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </div>
                );
              })}
            </div>

            {/* Add Room Button */}
            {rooms.length < 3 && (
              <div className="mt-2 relative">
                <button
                  onClick={() => setOpenDropdown(openDropdown === dir ? null : dir)}
                  className="w-full flex items-center justify-center gap-1 py-1.5 rounded-lg border border-dashed border-white/15 text-sm text-cosmic-text/50 hover:border-sacred-gold/40 hover:text-sacred-gold transition-all"
                >
                  <Plus className="w-3 h-3" />
                  {t('auto.addRoom')}
                </button>

                {/* Dropdown */}
                {openDropdown === dir && (
                  <div className="absolute z-20 left-0 right-0 mt-1 bg-[#1a1a2e] border border-white/15 rounded-xl shadow-xl max-h-[240px] overflow-y-auto">
                    {ROOM_OPTIONS.map(opt => {
                      const comp = getComplianceForRoomInZone(opt.key, dir, roomPlacementData);
                      const style = COMPLIANCE_STYLE[comp];
                      const isBlocked = comp === 'blocked';
                      return (
                        <button
                          key={opt.key}
                          disabled={isBlocked}
                          onClick={() => {
                            onAssign(dir, opt.key);
                            setOpenDropdown(null);
                          }}
                          className={`w-full flex items-center gap-2 px-3 py-2 text-left text-sm transition-colors ${
                            isBlocked
                              ? 'opacity-40 cursor-not-allowed'
                              : 'hover:bg-white/10'
                          }`}
                        >
                          <span>{opt.icon}</span>
                          <span className="flex-1 text-cosmic-text font-medium">
                            {isHi ? opt.hi : opt.en}
                          </span>
                          <div className={`w-2 h-2 rounded-full ${style.dot}`} />
                          <span className={`text-sm ${
                            comp === 'ideal' ? 'text-emerald-400' :
                            comp === 'acceptable' ? 'text-blue-400' :
                            comp === 'avoid' || comp === 'blocked' ? 'text-red-400' :
                            'text-cosmic-text/40'
                          }`}>
                            {isHi ? style.labelHi : style.label}
                          </span>
                        </button>
                      );
                    })}
                    {isCenter && (
                      <div className="px-3 py-2 flex items-center gap-1.5 border-t border-white/10">
                        <AlertTriangle className="w-3 h-3 text-amber-400" />
                        <span className="text-sm text-amber-400">
                          {t('auto.brahmaSthanaShouldRe')}
                        </span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
