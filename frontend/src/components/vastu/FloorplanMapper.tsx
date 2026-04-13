import { useState, useRef, useCallback, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { X, Grid3X3, Compass, ZoomIn, ZoomOut, Undo2, Sparkles, Loader2 } from 'lucide-react';

interface RoomMarker {
  id: string;
  room_type: string;
  x: number;  // pixel coords on original image
  y: number;
}

interface Props {
  imageUrl: string;
  imageWidth: number;
  imageHeight: number;
  markers: RoomMarker[];
  onAddMarker: (room_type: string, x: number, y: number) => void;
  onRemoveMarker: (id: string) => void;
  northRotation: number;
  onNorthRotationChange: (deg: number) => void;
}

const ROOM_OPTIONS: { key: string; en: string; hi: string; icon: string; special?: boolean }[] = [
  // ── Special marker ───────────────────────────────────────────────────
  { key: 'main_entrance',          en: 'Main Entrance',    hi: 'मुख्य द्वार',    icon: '🚪', special: true },
  // ── Common rooms ─────────────────────────────────────────────────────
  { key: 'pooja',                  en: 'Pooja Room',       hi: 'पूजा कक्ष',     icon: '🙏' },
  { key: 'kitchen',                en: 'Kitchen',          hi: 'रसोई',          icon: '🍳' },
  { key: 'dining_room',            en: 'Dining Room',      hi: 'भोजन कक्ष',     icon: '🍽️' },
  { key: 'living_room',            en: 'Living Room',      hi: 'बैठक',          icon: '🛋️' },
  { key: 'balcony',                en: 'Balcony',          hi: 'बालकनी',        icon: '🌿' },
  // ── Bedrooms (Bedroom 1 = Master; 2–6 = Children's zones) ───────────
  { key: 'bedroom_1',              en: 'Bedroom 1',        hi: 'शयनकक्ष 1',     icon: '🛏️' },
  { key: 'bedroom_2',              en: 'Bedroom 2',        hi: 'शयनकक्ष 2',     icon: '🛏️' },
  { key: 'bedroom_3',              en: 'Bedroom 3',        hi: 'शयनकक्ष 3',     icon: '🛏️' },
  { key: 'bedroom_4',              en: 'Bedroom 4',        hi: 'शयनकक्ष 4',     icon: '🛏️' },
  { key: 'bedroom_5',              en: 'Bedroom 5',        hi: 'शयनकक्ष 5',     icon: '🛏️' },
  { key: 'bedroom_6',              en: 'Bedroom 6',        hi: 'शयनकक्ष 6',     icon: '🛏️' },
  // ── Bathrooms / Toilets ──────────────────────────────────────────────
  { key: 'bathroom',               en: 'Bathroom 1',       hi: 'स्नानघर 1',     icon: '🚿' },
  { key: 'bathroom_2',             en: 'Bathroom 2',       hi: 'स्नानघर 2',     icon: '🚿' },
  { key: 'bathroom_3',             en: 'Bathroom 3',       hi: 'स्नानघर 3',     icon: '🚿' },
  { key: 'toilet',                 en: 'Toilet / WC',      hi: 'शौचालय',        icon: '🚽' },
  { key: 'toilet_2',               en: 'Toilet 2',         hi: 'शौचालय 2',      icon: '🚽' },
  // ── Other ────────────────────────────────────────────────────────────
  { key: 'staircase',              en: 'Staircase',        hi: 'सीढ़ी',         icon: '🪜' },
  { key: 'study_room',             en: 'Study Room',       hi: 'अध्ययन कक्ष',   icon: '📚' },
  { key: 'water_tank_underground', en: 'UG Water Tank',    hi: 'भूमिगत टंकी',   icon: '💧' },
  { key: 'water_tank_overhead',    en: 'OH Water Tank',    hi: 'ऊपरी टंकी',     icon: '🏗️' },
];

// Map display types → valid Vastu API types.
// bedroom_1 = master (SW ideal); bedroom_2+ = children's (NW/W ideal).
export const ROOM_TYPE_ALIAS: Record<string, string> = {
  bedroom_1:   'master_bedroom',
  bedroom_2:   'children_bedroom',
  bedroom_3:   'children_bedroom',
  bedroom_4:   'children_bedroom',
  bedroom_5:   'children_bedroom',
  bedroom_6:   'children_bedroom',
  dining_room: 'kitchen',
  toilet:      'bathroom',
  toilet_2:    'bathroom',
  bathroom_2:  'bathroom',
  bathroom_3:  'bathroom',
  balcony:     'living_room',
};

export default function FloorplanMapper({
  imageUrl, imageWidth, imageHeight,
  markers, onAddMarker, onRemoveMarker,
  northRotation, onNorthRotationChange,
}: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const containerRef = useRef<HTMLDivElement>(null);
  const [clickPos, setClickPos] = useState<{ x: number; y: number } | null>(null);
  const [showGrid, setShowGrid] = useState(true);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const panStart = useRef({ x: 0, y: 0, panX: 0, panY: 0 });
  const [autoDetecting, setAutoDetecting] = useState(false);
  const [editingMarkerId, setEditingMarkerId] = useState<string | null>(null);
  const [aiDone, setAiDone] = useState(false);

  // Attach wheel as non-passive so preventDefault() actually works (stops page scroll)
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      setZoom(prev => Math.min(3, Math.max(0.5, prev - e.deltaY * 0.001)));
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, []);

  const handlePanStart = useCallback((e: React.MouseEvent) => {
    if (e.button === 1 || e.altKey) {  // middle-click or Alt+click to pan
      e.preventDefault();
      setIsPanning(true);
      panStart.current = { x: e.clientX, y: e.clientY, panX: pan.x, panY: pan.y };
    }
  }, [pan]);

  const handlePanMove = useCallback((e: React.MouseEvent) => {
    if (!isPanning) return;
    setPan({
      x: panStart.current.panX + (e.clientX - panStart.current.x),
      y: panStart.current.panY + (e.clientY - panStart.current.y),
    });
  }, [isPanning]);

  const handlePanEnd = useCallback(() => setIsPanning(false), []);

  const handleUndo = useCallback(() => {
    if (markers.length > 0) {
      onRemoveMarker(markers[markers.length - 1].id);
    }
  }, [markers, onRemoveMarker]);

  const handleImageClick = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    // Close any open edit dropdown first
    setEditingMarkerId(null);
    const rect = e.currentTarget.getBoundingClientRect();
    const scaleX = imageWidth / rect.width;
    const scaleY = imageHeight / rect.height;
    const x = Math.round((e.clientX - rect.left) * scaleX);
    const y = Math.round((e.clientY - rect.top) * scaleY);
    setClickPos({ x, y });
  }, [imageWidth, imageHeight]);

  const selectRoom = useCallback((roomType: string) => {
    if (clickPos) {
      onAddMarker(roomType, clickPos.x, clickPos.y);
      setClickPos(null);
    }
  }, [clickPos, onAddMarker]);

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center gap-4 flex-wrap">
        {/* North rotation */}
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-sacred-gold" />
          <label className="text-sm text-cosmic-text/60">{isHi ? 'उत्तर दिशा' : 'North'}</label>
          <input
            type="range"
            min={0}
            max={359}
            value={northRotation}
            onChange={(e) => onNorthRotationChange(parseInt(e.target.value))}
            className="w-24 accent-amber-500"
          />
          <span className="text-sm text-sacred-gold font-mono w-8">{northRotation}°</span>
          <span className="text-sm text-cosmic-text/40">
            {northRotation === 0 ? '↑' : northRotation < 90 ? '↗' : northRotation === 90 ? '→' : northRotation < 180 ? '↘' : northRotation === 180 ? '↓' : northRotation < 270 ? '↙' : northRotation === 270 ? '←' : '↖'}
          </span>
        </div>

        {/* Grid toggle */}
        <button
          onClick={() => setShowGrid(!showGrid)}
          className={`flex items-center gap-1 px-2 py-1 rounded text-sm transition-colors ${
            showGrid ? 'bg-sacred-gold/20 text-sacred-gold' : 'bg-white/5 text-cosmic-text/40'
          }`}
        >
          <Grid3X3 className="w-3 h-3" />
          {isHi ? 'ग्रिड' : 'Grid'}
        </button>

        {/* Zoom controls */}
        <div className="flex items-center gap-1">
          <button onClick={() => setZoom(z => Math.max(0.5, z - 0.25))} className="p-1 rounded bg-white/5 text-cosmic-text/50 hover:text-white">
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <span className="text-sm text-cosmic-text/40 w-8 text-center">{Math.round(zoom * 100)}%</span>
          <button onClick={() => setZoom(z => Math.min(3, z + 0.25))} className="p-1 rounded bg-white/5 text-cosmic-text/50 hover:text-white">
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          {zoom !== 1 && (
            <button onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }); }} className="text-sm text-cosmic-text/40 hover:text-white ml-1">
              {isHi ? 'रीसेट' : 'Reset'}
            </button>
          )}
        </div>

        {/* Undo */}
        {markers.length > 0 && (
          <button onClick={handleUndo} className="flex items-center gap-1 px-2 py-1 rounded bg-white/5 text-cosmic-text/50 hover:text-white text-sm">
            <Undo2 className="w-3 h-3" />
            {isHi ? 'पूर्ववत' : 'Undo'}
          </button>
        )}

        {/* Auto-Detect Rooms */}
        <button
          disabled={autoDetecting}
          onClick={async () => {
            setAutoDetecting(true);
            try {
              const res = await api.post('/api/vastu/auto-detect', {
                image_url: imageUrl,
                image_width: imageWidth,
                image_height: imageHeight,
              });
              if (res.markers?.length > 0) {
                for (const m of res.markers) {
                  onAddMarker(m.room_type, m.x, m.y);
                }
              }
              setAiDone(true);
            } catch (e) {
              console.error('Auto-detect failed:', e);
              setAiDone(true); // still show manual hint on failure
            } finally {
              setAutoDetecting(false);
            }
          }}
          className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 text-sm font-medium hover:bg-amber-500/20 transition-colors disabled:opacity-40"
        >
          {autoDetecting ? <Loader2 className="w-3 h-3 animate-spin" /> : <Sparkles className="w-3 h-3" />}
          {isHi ? 'AI पहचान' : 'AI Detect'}
        </button>

        <span className="text-[10px] text-cosmic-text/40 ml-auto">
          {isHi ? 'क्लिक=कमरा जोड़ें, मार्कर क्लिक=बदलें' : 'Click=add room, Click marker=edit'}
        </span>
      </div>

      {/* AI Done — Manual Edit Hint */}
      {aiDone && markers.length > 0 && (
        <div className="flex items-center gap-2 px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg">
          <Sparkles className="w-4 h-4 text-amber-400 flex-shrink-0" />
          <p className="text-xs text-amber-300">
            {isHi
              ? `AI ने ${markers.length} कमरे पहचाने। गलत मार्कर पर क्लिक करके बदलें, X से हटाएँ, या खाली जगह क्लिक करके नया जोड़ें।`
              : `AI detected ${markers.length} rooms. Click any marker to change its type, X to remove, or click empty area to add more.`}
          </p>
        </div>
      )}
      {aiDone && markers.length === 0 && (
        <div className="flex items-center gap-2 px-3 py-2 bg-blue-500/10 border border-blue-500/20 rounded-lg">
          <Compass className="w-4 h-4 text-blue-400 flex-shrink-0" />
          <p className="text-xs text-blue-300">
            {isHi
              ? 'AI कोई कमरा नहीं पहचान पाया। चिंता न करें — इमेज पर क्लिक करके मैन्युअली कमरे रखें।'
              : 'AI could not detect rooms. No worries — click anywhere on the image to manually place rooms.'}
          </p>
        </div>
      )}

      {/* Image Canvas */}
      <div
        ref={containerRef}
        className="relative border border-white/10 rounded-xl overflow-hidden bg-black flex items-center justify-center"
        style={{ cursor: isPanning ? 'grabbing' : 'crosshair' }}
        onMouseDown={handlePanStart}
        onMouseMove={handlePanMove}
        onMouseUp={handlePanEnd}
        onMouseLeave={handlePanEnd}
      >
        {/* Inner wrapper sized exactly to the image aspect ratio — prevents grid/markers
            from bleeding into letterbox black areas that object-contain would create */}
        <div style={{
          transform: `scale(${zoom}) translate(${pan.x / zoom}px, ${pan.y / zoom}px)`,
          transformOrigin: 'center',
          transition: isPanning ? 'none' : 'transform 0.1s',
          position: 'relative',
          maxWidth: '100%',
          maxHeight: 500,
          aspectRatio: `${imageWidth} / ${imageHeight}`,
          flexShrink: 0,
        }}>
        <img
          src={imageUrl}
          alt="Floor plan"
          style={{ width: '100%', height: '100%', display: 'block' }}
          draggable={false}
        />

        {/* Translucent 3x3 Grid Overlay */}
        {showGrid && (
          <div className="absolute inset-0 pointer-events-none">
            {/* Grid lines — fixed pixel zone boundaries */}
            <div className="absolute top-0 bottom-0 left-1/3 w-px bg-sacred-gold/25" />
            <div className="absolute top-0 bottom-0 left-2/3 w-px bg-sacred-gold/25" />
            <div className="absolute left-0 right-0 top-1/3 h-px bg-sacred-gold/25" />
            <div className="absolute left-0 right-0 top-2/3 h-px bg-sacred-gold/25" />

            {/* Direction labels — rotate with northRotation so they always show
                the correct zone. Uses polar coordinates: r=44% from center. */}
            {([
              { d: 'N',  a: 0   },
              { d: 'NE', a: 45  },
              { d: 'E',  a: 90  },
              { d: 'SE', a: 135 },
              { d: 'S',  a: 180 },
              { d: 'SW', a: 225 },
              { d: 'W',  a: 270 },
              { d: 'NW', a: 315 },
            ] as { d: string; a: number }[]).map(({ d, a }) => {
              const rad = ((a + northRotation) * Math.PI) / 180;
              const r = 43;
              const x = 50 + r * Math.sin(rad);
              const y = 50 - r * Math.cos(rad);
              return (
                <span
                  key={d}
                  className="absolute text-sm font-bold text-sacred-gold/70"
                  style={{ left: `${x}%`, top: `${y}%`, transform: 'translate(-50%, -50%)' }}
                >
                  {d}
                </span>
              );
            })}
            {/* Brahmasthana — geometric center, source of all direction measurements */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center pointer-events-none">
              {/* Pulsing golden dot */}
              <div className="relative w-5 h-5 flex items-center justify-center">
                <div className="absolute w-5 h-5 rounded-full bg-sacred-gold/20 animate-ping" />
                <div className="w-3 h-3 rounded-full bg-sacred-gold border-2 border-sacred-gold/80 z-10" />
              </div>
              <span className="text-sm font-bold text-sacred-gold mt-0.5 whitespace-nowrap drop-shadow">✦ Brahmasthana</span>
            </div>

            {/* North arrow — confirms physical north direction */}
            <div
              className="absolute top-2 right-2 flex flex-col items-center"
              style={{ transform: `rotate(${northRotation}deg)`, transformOrigin: 'center' }}
            >
              <div className="w-0 h-0 border-l-[5px] border-l-transparent border-r-[5px] border-r-transparent border-b-[10px] border-b-red-500" />
              <span className="text-sm text-red-400 font-bold leading-none mt-0.5">N</span>
            </div>
          </div>
        )}

        {/* Click layer */}
        <div className="absolute inset-0" onClick={handleImageClick} />

        {/* Room Markers — click to edit room type, X to remove */}
        {markers.map((m) => {
          const px = (m.x / imageWidth) * 100;
          const py = (m.y / imageHeight) * 100;
          const opt = ROOM_OPTIONS.find(r => r.key === m.room_type);
          const isEditing = editingMarkerId === m.id;

          return (
            <div key={m.id} className="absolute -translate-x-1/2 -translate-y-1/2 pointer-events-auto z-10" style={{ left: `${px}%`, top: `${py}%` }}>
              {/* Marker chip — click to open edit dropdown */}
              <div
                onClick={(e) => { e.stopPropagation(); setEditingMarkerId(isEditing ? null : m.id); setClickPos(null); }}
                className={`flex items-center gap-1 rounded-lg px-2 py-1 cursor-pointer transition-all ${
                  isEditing
                    ? 'bg-sacred-gold/30 border-2 border-sacred-gold ring-2 ring-sacred-gold/20'
                    : 'bg-black/80 border border-sacred-gold/40 hover:border-sacred-gold'
                }`}
              >
                <span className="text-sm">{opt?.icon || '🏠'}</span>
                <span className="text-[10px] text-white font-medium whitespace-nowrap">
                  {isHi ? (opt?.hi || m.room_type) : (opt?.en || m.room_type)}
                </span>
                <button
                  onClick={(e) => { e.stopPropagation(); onRemoveMarker(m.id); setEditingMarkerId(null); }}
                  className="text-white/40 hover:text-red-400 ml-0.5"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>

              {/* Edit dropdown — change room type */}
              {isEditing && (
                <div className="absolute z-30 left-1/2 -translate-x-1/2 mt-1 bg-[#1a1a2e] border border-sacred-gold/30 rounded-xl shadow-2xl p-1 max-h-[200px] overflow-y-auto w-44">
                  <div className="px-2 py-1 border-b border-white/10 mb-1">
                    <span className="text-[9px] text-sacred-gold font-semibold">
                      {isHi ? 'कमरा बदलें' : 'Change Room Type'}
                    </span>
                  </div>
                  {ROOM_OPTIONS.map(ro => (
                    <button
                      key={ro.key}
                      onClick={(e) => {
                        e.stopPropagation();
                        // Remove old, add new at same position
                        onRemoveMarker(m.id);
                        onAddMarker(ro.key, m.x, m.y);
                        setEditingMarkerId(null);
                      }}
                      className={`w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-lg transition-colors ${
                        ro.key === m.room_type ? 'bg-sacred-gold/20 text-sacred-gold' : 'text-white hover:bg-white/10'
                      }`}
                    >
                      <span>{ro.icon}</span>
                      <span className="font-medium">{isHi ? ro.hi : ro.en}</span>
                      {ro.key === m.room_type && <span className="ml-auto text-[9px] text-sacred-gold">current</span>}
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {/* Click Position — Room Selector Popup */}
        {clickPos && (
          <div
            className="absolute z-20 bg-[#1a1a2e] border border-sacred-gold/30 rounded-xl shadow-2xl p-1 max-h-[200px] overflow-y-auto w-44"
            style={{
              left: `${(clickPos.x / imageWidth) * 100}%`,
              top: `${(clickPos.y / imageHeight) * 100}%`,
              transform: 'translate(-50%, 4px)',
            }}
          >
            <div className="px-2 py-1 flex items-center justify-between border-b border-white/10 mb-1">
              <span className="text-sm text-sacred-gold font-semibold">
                {isHi ? 'कमरा चुनें' : 'Select Room'}
              </span>
              <button onClick={() => setClickPos(null)} className="text-cosmic-text/40 hover:text-white">
                <X className="w-3 h-3" />
              </button>
            </div>
            {ROOM_OPTIONS.map(opt => (
              <button
                key={opt.key}
                onClick={() => selectRoom(opt.key)}
                className="w-full flex items-center gap-2 px-2 py-1.5 text-sm text-white hover:bg-white/10 rounded-lg transition-colors"
              >
                <span>{opt.icon}</span>
                <span className="font-medium">{isHi ? opt.hi : opt.en}</span>
              </button>
            ))}
          </div>
        )}
        </div>{/* close zoom transform div */}
      </div>

      {/* Markers Summary */}
      {markers.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {markers.map(m => {
            const opt = ROOM_OPTIONS.find(r => r.key === m.room_type);
            return (
              <span key={m.id} className="flex items-center gap-1 px-2 py-1 bg-white/5 border border-white/10 rounded-lg text-sm text-cosmic-text">
                {opt?.icon} {isHi ? opt?.hi : opt?.en}
                <button onClick={() => onRemoveMarker(m.id)} className="text-cosmic-text/30 hover:text-red-400 ml-1">
                  <X className="w-2.5 h-2.5" />
                </button>
              </span>
            );
          })}
        </div>
      )}
    </div>
  );
}
