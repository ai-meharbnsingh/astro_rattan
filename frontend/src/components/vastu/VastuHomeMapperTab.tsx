import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { LayoutGrid, Loader2, RotateCcw, Image as ImageIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import HomeGrid from './HomeGrid';
import HomeComplianceReport from './HomeComplianceReport';
import FloorplanUploader from './FloorplanUploader';
import FloorplanMapper, { ROOM_TYPE_ALIAS } from './FloorplanMapper';

// Client-side direction calc — mirrors backend pixel_to_direction
function calcDirection(x: number, y: number, w: number, h: number, northRot: number): string {
  const nx = (x - w / 2) / (w / 2);
  const ny = (y - h / 2) / (h / 2);
  const rad = (-northRot * Math.PI) / 180;
  const rx = nx * Math.cos(rad) - ny * Math.sin(rad);
  const ry = nx * Math.sin(rad) + ny * Math.cos(rad);
  const T = 1 / 3;
  const row = ry < -T ? 'N' : ry > T ? 'S' : 'C';
  const col = rx < -T ? 'W' : rx > T ? 'E' : 'C';
  const map: Record<string, string> = {
    'N-W': 'NW', 'N-C': 'N', 'N-E': 'NE',
    'C-W': 'W',  'C-C': 'Center', 'C-E': 'E',
    'S-W': 'SW', 'S-C': 'S', 'S-E': 'SE',
  };
  return map[`${row}-${col}`] ?? 'Center';
}

interface LayoutResult {
  overall_score: number;
  overall_label_en: string;
  overall_label_hi: string;
  total_rooms: number;
  ideal_count: number;
  acceptable_count: number;
  neutral_count: number;
  avoid_count: number;
  room_results: Array<{
    room_type: string;
    room_name_en: string;
    room_name_hi: string;
    assigned_direction: string;
    assigned_direction_en: string;
    assigned_direction_hi: string;
    compliance: string;
    score_contribution: number;
    ideal_directions: string[];
    ideal_directions_hi: string[];
    reason_en: string;
    reason_hi: string;
    tips_en: string[];
    tips_hi: string[];
    remedies: Record<string, unknown> | null;
    zone_devtas: Array<{ name: string; name_hi: string; mantra: string; nature: string }>;
  }>;
  center_status: { is_open: boolean; rooms: string[]; assessment_en: string; assessment_hi: string };
  missing_critical_rooms: Array<{ room_type: string; room_name_en: string; room_name_hi: string; ideal_directions: string[]; ideal_directions_hi: string[] }>;
  duplicate_warnings: Array<{ room_type: string; room_name_en: string; room_name_hi: string; count: number; message_en: string; message_hi: string }>;
  direction_summary: Record<string, { rooms: string[]; element: string; element_hi: string; status: string }>;
}

interface Props {
  data: {
    building_type?: string;
    entrance_analysis?: { direction?: string };
    room_placement?: { rooms?: Record<string, { ideal_directions?: string[]; acceptable_directions?: string[]; avoid_directions?: string[] }> };
  };
  initialMode?: 'grid' | 'floorplan';
}

const STORAGE_KEY = 'astro_vastu_room_layout';

function loadSaved(): Record<string, string[]> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch { /* ignore */ }
  return {};
}

function saveToDisk(assignments: Record<string, string[]>) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(assignments));
  } catch { /* ignore */ }
}

type MapperMode = 'grid' | 'floorplan';

interface FloorplanMarker {
  id: string;
  room_type: string;
  x: number;
  y: number;
}

export default function VastuHomeMapperTab({ data, initialMode = 'grid' }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [mode, setMode] = useState<MapperMode>(initialMode);
  const [assignments, setAssignments] = useState<Record<string, string[]>>(loadSaved);
  const [layoutResult, setLayoutResult] = useState<LayoutResult | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState('');

  // Floorplan state
  const [fpImageUrl, setFpImageUrl] = useState<string | null>(null);
  const [fpWidth, setFpWidth] = useState(0);
  const [fpHeight, setFpHeight] = useState(0);
  const [fpMarkers, setFpMarkers] = useState<FloorplanMarker[]>([]);
  const [northRotation, setNorthRotation] = useState(0);

  // Persist to localStorage
  useEffect(() => { saveToDisk(assignments); }, [assignments]);

  const gridRooms = Object.values(assignments).reduce((s, r) => s + r.length, 0);
  // main_entrance is not a room — exclude from count
  const fpRoomMarkers = fpMarkers.filter(m => m.room_type !== 'main_entrance');
  const totalRooms = mode === 'floorplan' ? fpRoomMarkers.length : gridRooms;

  const handleAssign = useCallback((direction: string, roomType: string) => {
    setAssignments(prev => {
      const current = prev[direction] || [];
      if (current.length >= 3) return prev;
      return { ...prev, [direction]: [...current, roomType] };
    });
    setLayoutResult(null);  // clear old results on change
  }, []);

  const handleRemove = useCallback((direction: string, roomType: string) => {
    setAssignments(prev => {
      const current = prev[direction] || [];
      const idx = current.indexOf(roomType);
      if (idx === -1) return prev;
      const updated = [...current];
      updated.splice(idx, 1);
      const next = { ...prev };
      if (updated.length === 0) {
        delete next[direction];
      } else {
        next[direction] = updated;
      }
      return next;
    });
    setLayoutResult(null);
  }, []);

  const handleReset = () => {
    const msg = language === 'hi'
      ? 'क्या आप सभी कमरे और नक्शा हटाना चाहते हैं?'
      : 'Remove all rooms and the uploaded map?';
    if (!window.confirm(msg)) return;
    setAssignments({});
    setLayoutResult(null);
    setError('');
    localStorage.removeItem(STORAGE_KEY);
    // Clear floorplan state too
    setFpImageUrl(null);
    setFpWidth(0);
    setFpHeight(0);
    setFpMarkers([]);
    setNorthRotation(0);
  };

  // Floorplan handlers
  const handleFpUploaded = useCallback((url: string, w: number, h: number) => {
    setFpImageUrl(url);
    setFpWidth(w);
    setFpHeight(h);
    setFpMarkers([]);
    setLayoutResult(null);
  }, []);

  const handleAddFpMarker = useCallback((roomType: string, x: number, y: number) => {
    setFpMarkers(prev => [...prev, { id: `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`, room_type: roomType, x, y }]);
    setLayoutResult(null);
  }, []);

  const handleRemoveFpMarker = useCallback((id: string) => {
    setFpMarkers(prev => prev.filter(m => m.id !== id));
    setLayoutResult(null);
  }, []);

  const handleAnalyze = async () => {
    setAnalyzing(true);
    setError('');
    try {
      if (mode === 'floorplan' && fpImageUrl) {
        // Separate entrance marker from room markers
        const entranceMarker = fpMarkers.find(m => m.room_type === 'main_entrance');
        const entranceDir = entranceMarker
          ? calcDirection(entranceMarker.x, entranceMarker.y, fpWidth, fpHeight, northRotation)
          : (data?.entrance_analysis?.direction || null);

        // Alias display types → valid Vastu API types, skip main_entrance
        const apiMarkers = fpMarkers
          .filter(m => m.room_type !== 'main_entrance')
          .map(m => ({
            room_type: ROOM_TYPE_ALIAS[m.room_type] ?? m.room_type,
            x: m.x,
            y: m.y,
          }));

        const payload = {
          image_url: fpImageUrl,
          image_width: fpWidth,
          image_height: fpHeight,
          north_rotation: northRotation,
          room_markers: apiMarkers,
          building_type: data?.building_type || 'residential',
          entrance_direction: entranceDir,
        };
        const result = await api.post('/api/vastu/analyze-floorplan', payload);
        setLayoutResult(result);
      } else {
        // Grid mode — send direction assignments
        const payload = {
          room_assignments: assignments,
          building_type: data?.building_type || 'residential',
          entrance_direction: data?.entrance_analysis?.direction || null,
        };
        const result = await api.post('/api/vastu/home-layout', payload);
        setLayoutResult(result);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  // Extract room placement data for compliance preview dots
  const rpData = data?.room_placement?.rooms;

  return (
    <div className="space-y-6">
      {/* Header + Mode Toggle */}
      <div className="bg-white/5 border border-white/10 rounded-xl p-5">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-bold text-sacred-gold flex items-center gap-2">
            <LayoutGrid className="w-5 h-5" />
            {isHi ? 'मेरे घर का नक्शा' : 'My Home Layout'}
          </h3>
          {totalRooms > 0 && (
            <button onClick={handleReset} className="flex items-center gap-1 text-sm text-cosmic-text/50 hover:text-red-400 transition-colors">
              <RotateCcw className="w-3 h-3" />
              {isHi ? 'रीसेट' : 'Reset'}
            </button>
          )}
        </div>

        {/* Mode Toggle */}
        <div className="flex gap-2 mb-3">
          <button
            onClick={() => { setMode('grid'); setLayoutResult(null); }}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              mode === 'grid'
                ? 'bg-sacred-gold/20 text-sacred-gold border border-sacred-gold/30'
                : 'bg-white/5 text-cosmic-text/50 border border-white/10 hover:border-white/20'
            }`}
          >
            <LayoutGrid className="w-3.5 h-3.5" />
            {isHi ? 'ग्रिड मोड' : 'Grid Mode'}
          </button>
          <button
            onClick={() => { setMode('floorplan'); setLayoutResult(null); }}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              mode === 'floorplan'
                ? 'bg-sacred-gold/20 text-sacred-gold border border-sacred-gold/30'
                : 'bg-white/5 text-cosmic-text/50 border border-white/10 hover:border-white/20'
            }`}
          >
            <ImageIcon className="w-3.5 h-3.5" />
            {isHi ? 'फ्लोर प्लान' : 'Floor Plan'}
          </button>
        </div>

        <p className="text-sm text-cosmic-text/60">
          {mode === 'grid'
            ? (isHi
                ? 'प्रत्येक क्षेत्र पर क्लिक करें और अपने कमरे जोड़ें — हरा=आदर्श, लाल=गलत'
                : 'Click each zone and add your rooms — green=ideal, red=misplaced')
            : (isHi
                ? 'अपने फ्लोर प्लान की फोटो अपलोड करें, फिर कमरे रखने के लिए क्लिक करें'
                : 'Upload your floor plan photo, then click to place rooms on it')
          }
        </p>
      </div>

      {/* Grid Mode */}
      {mode === 'grid' && (
        <HomeGrid
          assignments={assignments}
          onAssign={handleAssign}
          onRemove={handleRemove}
          layoutResult={layoutResult}
          roomPlacementData={rpData}
        />
      )}

      {/* Floorplan Mode */}
      {mode === 'floorplan' && (
        <>
          {!fpImageUrl ? (
            <FloorplanUploader onUploaded={handleFpUploaded} />
          ) : (
            <FloorplanMapper
              imageUrl={fpImageUrl}
              imageWidth={fpWidth}
              imageHeight={fpHeight}
              markers={fpMarkers}
              onAddMarker={handleAddFpMarker}
              onRemoveMarker={handleRemoveFpMarker}
              northRotation={northRotation}
              onNorthRotationChange={setNorthRotation}
            />
          )}
        </>
      )}

      {/* Analyze Button */}
      <div className="text-center">
        <Button
          onClick={handleAnalyze}
          disabled={analyzing || totalRooms < 2}
          className="bg-gradient-to-r from-sacred-gold to-amber-600 text-black font-bold px-8 py-3 text-sm"
        >
          {analyzing ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              {isHi ? 'विश्लेषण हो रहा है...' : 'Analyzing...'}
            </>
          ) : layoutResult ? (
            isHi ? `पुनः विश्लेषण (${totalRooms} कमरे)` : `Re-analyze (${totalRooms} rooms)`
          ) : (
            isHi ? `लेआउट विश्लेषण करें (${totalRooms} कमरे)` : `Analyze Layout (${totalRooms} rooms)`
          )}
        </Button>
        {totalRooms < 2 && (
          <p className="text-sm text-cosmic-text/40 mt-1">
            {isHi ? 'कम से कम 2 कमरे जोड़ें' : 'Assign at least 2 rooms'}
          </p>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Compliance Report */}
      {layoutResult && <HomeComplianceReport result={layoutResult} />}
    </div>
  );
}
