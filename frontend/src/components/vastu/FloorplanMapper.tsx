import { useState, useRef, useCallback, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { X, Grid3X3, Compass, ZoomIn, ZoomOut, Undo2, Sparkles, Loader2, Move, MousePointer } from 'lucide-react';

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

/** Extract clientX/clientY from either mouse or touch events */
const getEventCoords = (e: React.MouseEvent | React.TouchEvent) => {
  if ('touches' in e && e.touches.length > 0) {
    return { clientX: e.touches[0].clientX, clientY: e.touches[0].clientY };
  }
  if ('changedTouches' in e && e.changedTouches.length > 0) {
    return { clientX: e.changedTouches[0].clientX, clientY: e.changedTouches[0].clientY };
  }
  if ('clientX' in e) {
    return { clientX: e.clientX, clientY: e.clientY };
  }
  return { clientX: 0, clientY: 0 };
};

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
  const [gridOffset, setGridOffset] = useState({ x: 0, y: 0 }); // % offset for grid/brahmasthana
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const panStart = useRef({ x: 0, y: 0, panX: 0, panY: 0 });
  const [autoDetecting, setAutoDetecting] = useState(false);
  const [editingMarkerId, setEditingMarkerId] = useState<string | null>(null);
  const [aiDone, setAiDone] = useState(false);
  const [mobileMode, setMobileMode] = useState<'pan' | 'place'>('place');
  const touchStartRef = useRef<{ x: number; y: number; time: number } | null>(null);
  const isTouchPanningRef = useRef(false);

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

  // ── Touch event handlers ─────────────────────────────────────────────
  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      const coords = getEventCoords(e);
      touchStartRef.current = { x: coords.clientX, y: coords.clientY, time: Date.now() };
      // In pan mode, start panning immediately on single finger
      if (mobileMode === 'pan') {
        e.preventDefault();
        setIsPanning(true);
        isTouchPanningRef.current = true;
        panStart.current = { x: coords.clientX, y: coords.clientY, panX: pan.x, panY: pan.y };
      }
    } else if (e.touches.length === 2) {
      // Two-finger drag always pans regardless of mode
      e.preventDefault();
      const midX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
      const midY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
      setIsPanning(true);
      isTouchPanningRef.current = true;
      panStart.current = { x: midX, y: midY, panX: pan.x, panY: pan.y };
    }
  }, [pan, mobileMode]);

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (e.touches.length === 2) {
      e.preventDefault();
      const midX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
      const midY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
      setPan({
        x: panStart.current.panX + (midX - panStart.current.x),
        y: panStart.current.panY + (midY - panStart.current.y),
      });
      return;
    }
    if (isTouchPanningRef.current && e.touches.length === 1) {
      e.preventDefault();
      const coords = getEventCoords(e);
      setPan({
        x: panStart.current.panX + (coords.clientX - panStart.current.x),
        y: panStart.current.panY + (coords.clientY - panStart.current.y),
      });
    }
  }, []);

  const handleTouchEnd = useCallback((e: React.TouchEvent) => {
    if (isTouchPanningRef.current) {
      setIsPanning(false);
      isTouchPanningRef.current = false;
      touchStartRef.current = null;
      return;
    }
    // Detect tap (not a drag) — open room selector in place mode
    if (mobileMode === 'place' && touchStartRef.current && e.changedTouches.length > 0) {
      const coords = getEventCoords(e);
      const dx = coords.clientX - touchStartRef.current.x;
      const dy = coords.clientY - touchStartRef.current.y;
      const dt = Date.now() - touchStartRef.current.time;
      const dist = Math.sqrt(dx * dx + dy * dy);
      // Tap = less than 10px movement and under 300ms
      if (dist < 10 && dt < 300) {
        setEditingMarkerId(null);
        const container = containerRef.current;
        if (container) {
          // Find the inner image wrapper (first child div inside container)
          const innerWrapper = container.querySelector('[data-image-wrapper]') as HTMLElement;
          if (innerWrapper) {
            const rect = innerWrapper.getBoundingClientRect();
            const scaleX = imageWidth / rect.width;
            const scaleY = imageHeight / rect.height;
            const x = Math.round((coords.clientX - rect.left) * scaleX);
            const y = Math.round((coords.clientY - rect.top) * scaleY);
            setClickPos({ x, y });
          }
        }
      }
    }
    touchStartRef.current = null;
  }, [mobileMode, imageWidth, imageHeight]);

  const handleUndo = useCallback(() => {
    if (markers.length > 0) {
      onRemoveMarker(markers[markers.length - 1].id);
    }
  }, [markers, onRemoveMarker]);

  const handleImageClick = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    // Close any open edit dropdown first
    setEditingMarkerId(null);
    // If a room selector popup is already open, just close it (don't open a new one)
    if (clickPos) {
      setClickPos(null);
      return;
    }
    const rect = e.currentTarget.getBoundingClientRect();
    const scaleX = imageWidth / rect.width;
    const scaleY = imageHeight / rect.height;
    const x = Math.round((e.clientX - rect.left) * scaleX);
    const y = Math.round((e.clientY - rect.top) * scaleY);
    setClickPos({ x, y });
  }, [imageWidth, imageHeight, clickPos]);

  const selectRoom = useCallback((roomType: string) => {
    if (clickPos) {
      onAddMarker(roomType, clickPos.x, clickPos.y);
      setClickPos(null);
    }
  }, [clickPos, onAddMarker]);

  // Close dropdown/popup when clicking outside the entire component
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setClickPos(null);
        setEditingMarkerId(null);
      }
    };
    // Also close on Escape key
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setClickPos(null);
        setEditingMarkerId(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEsc);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEsc);
    };
  }, []);

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-wrap items-center gap-2">
        {/* Mobile mode toggle (visible on touch devices) */}
        <div className="flex items-center gap-1 sm:hidden">
          <button
            onClick={() => setMobileMode('place')}
            className={`flex items-center gap-1 min-w-[40px] min-h-[40px] px-2 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              mobileMode === 'place' ? 'bg-sacred-gold/20 text-sacred-gold border border-sacred-gold/40' : 'bg-white/5 text-foreground/40 border border-white/10'
            }`}
          >
            <MousePointer className="w-3.5 h-3.5" />
            {t('auto.place')}
          </button>
          <button
            onClick={() => setMobileMode('pan')}
            className={`flex items-center gap-1 min-w-[40px] min-h-[40px] px-2 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              mobileMode === 'pan' ? 'bg-sacred-gold/20 text-sacred-gold border border-sacred-gold/40' : 'bg-white/5 text-foreground/40 border border-white/10'
            }`}
          >
            <Move className="w-3.5 h-3.5" />
            {t('auto.pan')}
          </button>
        </div>

        {/* North rotation */}
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Compass className="w-4 h-4 text-sacred-gold flex-shrink-0" />
          <label className="text-sm text-foreground/60">{t('auto.north')}</label>
          <input
            type="range"
            min={0}
            max={359}
            value={northRotation}
            onChange={(e) => onNorthRotationChange(parseInt(e.target.value))}
            className="w-full sm:w-24 accent-amber-500"
          />
          <span className="text-sm text-sacred-gold font-mono w-8">{northRotation}°</span>
          <span className="text-sm text-foreground/40">
            {northRotation === 0 ? '↑' : northRotation < 90 ? '↗' : northRotation === 90 ? '→' : northRotation < 180 ? '↘' : northRotation === 180 ? '↓' : northRotation < 270 ? '↙' : northRotation === 270 ? '←' : '↖'}
          </span>
        </div>

        {/* Grid toggle */}
        <button
          onClick={() => setShowGrid(!showGrid)}
          className={`flex items-center gap-1 min-w-[40px] min-h-[40px] px-2 py-1.5 rounded text-sm transition-colors ${
            showGrid ? 'bg-sacred-gold/20 text-sacred-gold' : 'bg-white/5 text-foreground/40'
          }`}
        >
          <Grid3X3 className="w-3.5 h-3.5" />
          {t('auto.grid')}
        </button>

        {/* Grid position — move Brahmasthana */}
        {showGrid && (
          <div className="flex items-center gap-1">
            <span className="text-xs text-foreground/50 mr-1">{t('auto.center')}</span>
            <button onClick={() => setGridOffset(o => ({ ...o, y: o.y - 3 }))} className="min-w-[28px] min-h-[28px] flex items-center justify-center rounded bg-white/5 text-foreground/50 hover:text-sacred-gold text-xs" title="Move up">↑</button>
            <button onClick={() => setGridOffset(o => ({ ...o, y: o.y + 3 }))} className="min-w-[28px] min-h-[28px] flex items-center justify-center rounded bg-white/5 text-foreground/50 hover:text-sacred-gold text-xs" title="Move down">↓</button>
            <button onClick={() => setGridOffset(o => ({ ...o, x: o.x - 3 }))} className="min-w-[28px] min-h-[28px] flex items-center justify-center rounded bg-white/5 text-foreground/50 hover:text-sacred-gold text-xs" title="Move left">←</button>
            <button onClick={() => setGridOffset(o => ({ ...o, x: o.x + 3 }))} className="min-w-[28px] min-h-[28px] flex items-center justify-center rounded bg-white/5 text-foreground/50 hover:text-sacred-gold text-xs" title="Move right">→</button>
            {(gridOffset.x !== 0 || gridOffset.y !== 0) && (
              <button onClick={() => setGridOffset({ x: 0, y: 0 })} className="text-xs text-foreground/40 hover:text-white ml-1">{t('auto.reset')}</button>
            )}
          </div>
        )}

        {/* Zoom controls */}
        <div className="flex items-center gap-1">
          <button onClick={() => setZoom(z => Math.max(0.5, z - 0.25))} className="min-w-[40px] min-h-[40px] flex items-center justify-center rounded bg-white/5 text-foreground/50 hover:text-white">
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-sm text-foreground/40 w-10 text-center">{Math.round(zoom * 100)}%</span>
          <button onClick={() => setZoom(z => Math.min(3, z + 0.25))} className="min-w-[40px] min-h-[40px] flex items-center justify-center rounded bg-white/5 text-foreground/50 hover:text-white">
            <ZoomIn className="w-4 h-4" />
          </button>
          {zoom !== 1 && (
            <button onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }); }} className="text-sm text-foreground/40 hover:text-white ml-1 min-h-[40px] flex items-center">
              {t('auto.reset')}
            </button>
          )}
        </div>

        {/* Undo */}
        {markers.length > 0 && (
          <button onClick={handleUndo} className="flex items-center gap-1 min-w-[40px] min-h-[40px] px-2 py-1.5 rounded bg-white/5 text-foreground/50 hover:text-white text-sm">
            <Undo2 className="w-3.5 h-3.5" />
            {t('auto.undo')}
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
              /* auto-detect failed — manual fallback shown */
              setAiDone(true); // still show manual hint on failure
            } finally {
              setAutoDetecting(false);
            }
          }}
          className="flex items-center gap-1 min-w-[40px] min-h-[40px] px-2.5 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 text-sm font-medium hover:bg-amber-500/20 transition-colors disabled:opacity-40"
        >
          {autoDetecting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
          {t('auto.aIDetect')}
        </button>

        <span className="text-[10px] text-foreground/40 ml-auto hidden sm:inline">
          {t('auto.clickAddRoomClickMar')}
        </span>
      </div>

      {/* AI Done — Manual Edit Hint */}
      {aiDone && markers.length > 0 && (
        <div className="flex items-center gap-2 px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg">
          <Sparkles className="w-4 h-4 text-amber-400 flex-shrink-0" />
          <p className="text-xs text-amber-300">
            {t('auto.aIDetectedMarkersLen')}
          </p>
        </div>
      )}
      {aiDone && markers.length === 0 && (
        <div className="flex items-center gap-2 px-3 py-2 bg-blue-500/10 border border-blue-500/20 rounded-lg">
          <Compass className="w-4 h-4 text-blue-400 flex-shrink-0" />
          <p className="text-xs text-blue-300">
            {t('auto.aICouldNotDetectRoom')}
          </p>
        </div>
      )}

      {/* Image Canvas */}
      <div
        ref={containerRef}
        className="relative border border-white/10 rounded-xl overflow-hidden bg-black flex items-center justify-center touch-none"
        style={{ cursor: isPanning ? 'grabbing' : 'crosshair' }}
        onMouseDown={handlePanStart}
        onMouseMove={handlePanMove}
        onMouseUp={handlePanEnd}
        onMouseLeave={handlePanEnd}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {/* Inner wrapper sized exactly to the image aspect ratio — prevents grid/markers
            from bleeding into letterbox black areas that object-contain would create */}
        <div data-image-wrapper style={{
          transform: `scale(${zoom}) translate(${pan.x / zoom}px, ${pan.y / zoom}px)`,
          transformOrigin: 'center',
          transition: isPanning ? 'none' : 'transform 0.1s',
          position: 'relative',
          maxWidth: '100%',
          aspectRatio: `${imageWidth} / ${imageHeight}`,
          flexShrink: 0,
        }} className="max-h-[50vh] sm:max-h-[500px]">
        <img
          src={imageUrl}
          alt="Floor plan"
          style={{ width: '100%', height: '100%', display: 'block' }}
          draggable={false}
        />

        {/* Translucent 3x3 Grid Overlay — offset by gridOffset */}
        {showGrid && (
          <div className="absolute inset-0 pointer-events-none" style={{
            transform: `translate(${gridOffset.x}%, ${gridOffset.y}%)`,
          }}>
            {/* Grid lines — fixed pixel zone boundaries */}
            <div className="absolute top-0 bottom-0 left-1/3 w-px bg-sacred-gold/50" />
            <div className="absolute top-0 bottom-0 left-2/3 w-px bg-sacred-gold/50" />
            <div className="absolute left-0 right-0 top-1/3 h-px bg-sacred-gold/50" />
            <div className="absolute left-0 right-0 top-2/3 h-px bg-sacred-gold/50" />

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
                  className="absolute text-xs font-extrabold text-amber-300 bg-black/60 rounded px-1 py-0.5 leading-none"
                  style={{
                    left: `${x}%`,
                    top: `${y}%`,
                    transform: 'translate(-50%, -50%)',
                    textShadow: '0 0 6px rgba(0,0,0,0.9)',
                    letterSpacing: '0.05em',
                  }}
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
                      {t('auto.changeRoomType')}
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

        {/* Click Position — Room Selector Popup (with edge collision avoidance) */}
        {clickPos && (() => {
          const pctX = (clickPos.x / imageWidth) * 100;
          const pctY = (clickPos.y / imageHeight) * 100;
          // Flip popup left if too close to right edge, flip up if too close to bottom
          const flipH = pctX > 70; // popup is ~176px (w-44), flip if in right 30%
          const flipV = pctY > 60; // popup is ~200px max-height, flip if in bottom 40%
          return (
          <div
            className="absolute z-20 bg-[#1a1a2e] border border-sacred-gold/30 rounded-xl shadow-2xl p-1 max-h-[200px] overflow-y-auto w-44"
            style={{
              left: `${pctX}%`,
              top: `${pctY}%`,
              transform: `translate(${flipH ? '-100%' : '-50%'}, ${flipV ? 'calc(-100% - 4px)' : '4px'})`,
            }}
          >
            <div className="px-2 py-1 flex items-center justify-between border-b border-white/10 mb-1">
              <span className="text-sm text-sacred-gold font-semibold">
                {t('auto.selectRoom')}
              </span>
              <button onClick={() => setClickPos(null)} className="text-foreground/40 hover:text-white">
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
          );
        })()}
        </div>{/* close zoom transform div */}
      </div>

      {/* Markers Summary */}
      {markers.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {markers.map(m => {
            const opt = ROOM_OPTIONS.find(r => r.key === m.room_type);
            return (
              <span key={m.id} className="flex items-center gap-1 px-2 py-1 bg-white/5 border border-white/10 rounded-lg text-sm text-foreground">
                {opt?.icon} {isHi ? opt?.hi : opt?.en}
                <button onClick={() => onRemoveMarker(m.id)} className="text-foreground/30 hover:text-red-400 ml-1">
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
