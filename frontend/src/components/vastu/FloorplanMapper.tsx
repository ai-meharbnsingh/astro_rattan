import { useState, useRef, useCallback } from 'react';
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

const ROOM_OPTIONS: { key: string; en: string; hi: string; icon: string }[] = [
  { key: 'pooja',                  en: 'Pooja Room',       hi: 'पूजा कक्ष',     icon: '🙏' },
  { key: 'kitchen',                en: 'Kitchen',          hi: 'रसोई',          icon: '🍳' },
  { key: 'master_bedroom',        en: 'Master Bedroom',   hi: 'मुख्य शयनकक्ष', icon: '🛏️' },
  { key: 'living_room',           en: 'Living Room',      hi: 'बैठक',          icon: '🛋️' },
  { key: 'bathroom',              en: 'Bathroom',         hi: 'स्नानघर',       icon: '🚿' },
  { key: 'staircase',             en: 'Staircase',        hi: 'सीढ़ी',         icon: '🪜' },
  { key: 'water_tank_underground', en: 'UG Water Tank',   hi: 'भूमिगत टंकी',   icon: '💧' },
  { key: 'water_tank_overhead',   en: 'OH Water Tank',    hi: 'ऊपरी टंकी',     icon: '🏗️' },
  { key: 'study_room',            en: 'Study Room',       hi: 'अध्ययन कक्ष',   icon: '📚' },
  { key: 'children_bedroom',      en: 'Children Room',    hi: 'बच्चों का कमरा', icon: '🧒' },
];

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

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    setZoom(prev => Math.min(3, Math.max(0.5, prev - e.deltaY * 0.001)));
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
          <label className="text-xs text-cosmic-text/60">{isHi ? 'उत्तर दिशा' : 'North'}</label>
          <input
            type="range"
            min={0}
            max={359}
            value={northRotation}
            onChange={(e) => onNorthRotationChange(parseInt(e.target.value))}
            className="w-24 accent-amber-500"
          />
          <span className="text-xs text-sacred-gold font-mono w-8">{northRotation}°</span>
        </div>

        {/* Grid toggle */}
        <button
          onClick={() => setShowGrid(!showGrid)}
          className={`flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors ${
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
          <span className="text-[10px] text-cosmic-text/40 w-8 text-center">{Math.round(zoom * 100)}%</span>
          <button onClick={() => setZoom(z => Math.min(3, z + 0.25))} className="p-1 rounded bg-white/5 text-cosmic-text/50 hover:text-white">
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          {zoom !== 1 && (
            <button onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }); }} className="text-[9px] text-cosmic-text/40 hover:text-white ml-1">
              {isHi ? 'रीसेट' : 'Reset'}
            </button>
          )}
        </div>

        {/* Undo */}
        {markers.length > 0 && (
          <button onClick={handleUndo} className="flex items-center gap-1 px-2 py-1 rounded bg-white/5 text-cosmic-text/50 hover:text-white text-xs">
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
            } catch (e) {
              console.error('Auto-detect failed:', e);
            } finally {
              setAutoDetecting(false);
            }
          }}
          className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-medium hover:bg-amber-500/20 transition-colors disabled:opacity-40"
        >
          {autoDetecting ? <Loader2 className="w-3 h-3 animate-spin" /> : <Sparkles className="w-3 h-3" />}
          {isHi ? 'AI पहचान' : 'AI Detect'}
        </button>

        <span className="text-[10px] text-cosmic-text/40 ml-auto">
          {isHi ? 'क्लिक=कमरा, स्क्रॉल=ज़ूम, Alt+ड्रैग=पैन' : 'Click=room, Scroll=zoom, Alt+drag=pan'}
        </span>
      </div>

      {/* Image Canvas */}
      <div
        ref={containerRef}
        className="relative border border-white/10 rounded-xl overflow-hidden bg-black"
        style={{ maxHeight: 500, cursor: isPanning ? 'grabbing' : 'crosshair' }}
        onWheel={handleWheel}
        onMouseDown={handlePanStart}
        onMouseMove={handlePanMove}
        onMouseUp={handlePanEnd}
        onMouseLeave={handlePanEnd}
      >
        <div style={{ transform: `scale(${zoom}) translate(${pan.x / zoom}px, ${pan.y / zoom}px)`, transformOrigin: 'center', transition: isPanning ? 'none' : 'transform 0.1s' }}>
        <img
          src={imageUrl}
          alt="Floor plan"
          className="w-full h-auto max-h-[500px] object-contain"
          draggable={false}
        />

        {/* Translucent 3x3 Grid Overlay */}
        {showGrid && (
          <div className="absolute inset-0 pointer-events-none">
            {/* Vertical lines at 1/3 and 2/3 */}
            <div className="absolute top-0 bottom-0 left-1/3 w-px bg-sacred-gold/25" />
            <div className="absolute top-0 bottom-0 left-2/3 w-px bg-sacred-gold/25" />
            {/* Horizontal lines at 1/3 and 2/3 */}
            <div className="absolute left-0 right-0 top-1/3 h-px bg-sacred-gold/25" />
            <div className="absolute left-0 right-0 top-2/3 h-px bg-sacred-gold/25" />
            {/* Direction labels */}
            <span className="absolute top-1 left-1 text-[9px] text-sacred-gold/40 font-bold">NW</span>
            <span className="absolute top-1 left-1/2 -translate-x-1/2 text-[9px] text-sacred-gold/40 font-bold">N</span>
            <span className="absolute top-1 right-1 text-[9px] text-sacred-gold/40 font-bold">NE</span>
            <span className="absolute top-1/2 -translate-y-1/2 left-1 text-[9px] text-sacred-gold/40 font-bold">W</span>
            <span className="absolute top-1/2 -translate-y-1/2 left-1/2 -translate-x-1/2 text-[9px] text-sacred-gold/40 font-bold">C</span>
            <span className="absolute top-1/2 -translate-y-1/2 right-1 text-[9px] text-sacred-gold/40 font-bold">E</span>
            <span className="absolute bottom-1 left-1 text-[9px] text-sacred-gold/40 font-bold">SW</span>
            <span className="absolute bottom-1 left-1/2 -translate-x-1/2 text-[9px] text-sacred-gold/40 font-bold">S</span>
            <span className="absolute bottom-1 right-1 text-[9px] text-sacred-gold/40 font-bold">SE</span>
            {/* North arrow */}
            <div
              className="absolute top-2 right-10 flex items-center gap-1"
              style={{ transform: `rotate(${northRotation}deg)`, transformOrigin: 'center' }}
            >
              <div className="w-0 h-0 border-l-[4px] border-l-transparent border-r-[4px] border-r-transparent border-b-[8px] border-b-red-500" />
              <span className="text-[8px] text-red-400 font-bold">N</span>
            </div>
          </div>
        )}

        {/* Click layer */}
        <div className="absolute inset-0" onClick={handleImageClick} />

        {/* Room Markers */}
        {markers.map((m) => {
          const rect = containerRef.current?.querySelector('img')?.getBoundingClientRect();
          const imgEl = containerRef.current?.querySelector('img');
          if (!imgEl) return null;
          const displayW = imgEl.clientWidth;
          const displayH = imgEl.clientHeight;
          const px = (m.x / imageWidth) * 100;
          const py = (m.y / imageHeight) * 100;
          const opt = ROOM_OPTIONS.find(r => r.key === m.room_type);

          return (
            <div
              key={m.id}
              className="absolute flex items-center gap-1 bg-black/80 border border-sacred-gold/40 rounded-lg px-2 py-1 -translate-x-1/2 -translate-y-1/2 pointer-events-auto z-10"
              style={{ left: `${px}%`, top: `${py}%` }}
            >
              <span className="text-sm">{opt?.icon || '🏠'}</span>
              <span className="text-[9px] text-white font-medium whitespace-nowrap">
                {isHi ? (opt?.hi || m.room_type) : (opt?.en || m.room_type)}
              </span>
              <button
                onClick={(e) => { e.stopPropagation(); onRemoveMarker(m.id); }}
                className="text-white/40 hover:text-red-400 ml-0.5"
              >
                <X className="w-3 h-3" />
              </button>
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
              <span className="text-[9px] text-sacred-gold font-semibold">
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
                className="w-full flex items-center gap-2 px-2 py-1.5 text-xs text-white hover:bg-white/10 rounded-lg transition-colors"
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
              <span key={m.id} className="flex items-center gap-1 px-2 py-1 bg-white/5 border border-white/10 rounded-lg text-[10px] text-cosmic-text">
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
