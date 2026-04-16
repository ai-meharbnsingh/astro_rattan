import { useState } from 'react';
import { Loader2, Plus, Trash2, Clock, Star, ChevronDown, ChevronUp, AlertCircle, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

// ── Types ────────────────────────────────────────────────────

interface LifeEvent {
  date: string;
  type: string;
}

interface EventMatch {
  event: string;
  date: string;
  score: number;
  explanation: string;
  dasha: string;
}

interface Candidate {
  birth_time: string;
  score: number;
  lagna: string;
  lagna_degree: number;
  nakshatra: string;
  event_matches: EventMatch[];
}

interface RectificationResult {
  candidates: Candidate[];
  best_time: string | null;
  confidence: 'high' | 'medium' | 'low';
  analysis_summary: string;
}

// ── Constants ────────────────────────────────────────────────

const EVENT_TYPES = [
  { value: 'marriage', label: 'Marriage' },
  { value: 'child_birth', label: 'Child Birth' },
  { value: 'job_start', label: 'Job Start' },
  { value: 'job_loss', label: 'Job Loss' },
  { value: 'accident', label: 'Accident' },
  { value: 'education', label: 'Education (Degree/Admission)' },
  { value: 'foreign_travel', label: 'Foreign Travel' },
  { value: 'property', label: 'Property Purchase' },
  { value: 'father_death', label: 'Father\'s Death' },
  { value: 'mother_death', label: 'Mother\'s Death' },
  { value: 'health_issue', label: 'Serious Health Issue' },
];

interface BirthRectificationProps {
  birthDate?: string;
  birthPlace?: { lat: number; lon: number; name?: string };
  language: string;
  t: (key: string) => string;
}

// ── Component ────────────────────────────────────────────────

export default function BirthRectification({
  birthDate: initialDate,
  birthPlace: initialPlace,
  language,
  t,
}: BirthRectificationProps) {
  const hi = language === 'hi';

  // Form state
  const [birthDate, setBirthDate] = useState(initialDate || '');
  const [timeStart, setTimeStart] = useState('06:00');
  const [timeEnd, setTimeEnd] = useState('09:00');
  const [latitude, setLatitude] = useState(initialPlace?.lat?.toString() || '');
  const [longitude, setLongitude] = useState(initialPlace?.lon?.toString() || '');
  const [placeName, setPlaceName] = useState(initialPlace?.name || '');
  const [stepMinutes, setStepMinutes] = useState(2);
  const [events, setEvents] = useState<LifeEvent[]>([{ date: '', type: 'marriage' }]);

  // Result state
  const [result, setResult] = useState<RectificationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);

  // ── Event list management ────────────────────────────────
  const addEvent = () => {
    setEvents([...events, { date: '', type: 'marriage' }]);
  };

  const removeEvent = (idx: number) => {
    if (events.length <= 1) return;
    setEvents(events.filter((_, i) => i !== idx));
  };

  const updateEvent = (idx: number, field: keyof LifeEvent, value: string) => {
    const updated = [...events];
    updated[idx] = { ...updated[idx], [field]: value };
    setEvents(updated);
  };

  // ── Submit ───────────────────────────────────────────────
  const handleSubmit = async () => {
    setError('');
    setResult(null);

    // Validation
    if (!birthDate) { setError('Please enter the birth date.'); return; }
    if (!timeStart || !timeEnd) { setError('Please set the time window.'); return; }
    if (!latitude || !longitude) { setError('Please enter birth place coordinates.'); return; }
    const validEvents = events.filter((e) => e.date && e.type);
    if (validEvents.length === 0) { setError('Please add at least one life event with a date.'); return; }

    setLoading(true);
    try {
      const data = await api.post('/api/kundli/birth-rectification', {
        birth_date: birthDate,
        time_window_start: timeStart,
        time_window_end: timeEnd,
        birth_place: { lat: parseFloat(latitude), lon: parseFloat(longitude) },
        life_events: validEvents,
        step_minutes: stepMinutes,
      });
      setResult(data as RectificationResult);
    } catch (err: any) {
      setError(err?.message || 'Failed to calculate rectification.');
    }
    setLoading(false);
  };

  // ── Confidence badge color ───────────────────────────────
  const confidenceColor = (c: string) => {
    if (c === 'high') return 'bg-green-100 text-green-800 border-green-300';
    if (c === 'medium') return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    return 'bg-red-100 text-red-800 border-red-300';
  };

  const scoreColor = (s: number) => {
    if (s >= 70) return 'text-green-600';
    if (s >= 40) return 'text-yellow-600';
    return 'text-red-500';
  };

  // ── Render ───────────────────────────────────────────────
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-muted rounded-xl border border-border p-4">
        <div className="flex items-center gap-2 mb-2">
          <Clock className="w-5 h-5 text-primary" />
          <Heading as={4} variant={4}>
            {hi ? 'जन्म समय शोधन' : 'Birth Time Rectification'}
          </Heading>
        </div>
        <p className="text-sm text-foreground/70">
          {hi
            ? 'यदि आपका जन्म समय निश्चित नहीं है, तो अपने जीवन की प्रमुख घटनाएँ दर्ज करें। प्रणाली दशा और गोचर विश्लेषण से सबसे संभावित जन्म समय ढूँढेगी।'
            : 'If your exact birth time is unknown, enter major life events below. The system tests multiple birth times and scores how well Dasha + Transit analysis explains each event.'}
        </p>
      </div>

      {/* Form */}
      <div className="bg-muted rounded-xl border border-border p-4 space-y-4">
        <Heading as={4} variant={4}>{hi ? 'जन्म विवरण' : 'Birth Details'}</Heading>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Birth Date */}
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              {hi ? 'जन्म तिथि' : 'Birth Date'}
            </label>
            <Input
              type="date"
              value={birthDate}
              onChange={(e) => setBirthDate(e.target.value)}
              className="bg-white border-border text-sm"
            />
          </div>

          {/* Time Window Start */}
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              {hi ? 'समय शुरू' : 'Time Window Start'}
            </label>
            <Input
              type="time"
              value={timeStart}
              onChange={(e) => setTimeStart(e.target.value)}
              className="bg-white border-border text-sm"
            />
          </div>

          {/* Time Window End */}
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              {hi ? 'समय समाप्त' : 'Time Window End'}
            </label>
            <Input
              type="time"
              value={timeEnd}
              onChange={(e) => setTimeEnd(e.target.value)}
              className="bg-white border-border text-sm"
            />
          </div>

          {/* Place Name */}
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              {hi ? 'जन्म स्थान' : 'Birth Place'}
            </label>
            <Input
              type="text"
              value={placeName}
              onChange={(e) => setPlaceName(e.target.value)}
              placeholder={hi ? 'शहर का नाम' : 'City name'}
              className="bg-white border-border text-sm"
            />
          </div>

          {/* Latitude */}
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              {hi ? 'अक्षांश' : 'Latitude'}
            </label>
            <Input
              type="number"
              step="0.0001"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              placeholder="28.6139"
              className="bg-white border-border text-sm"
            />
          </div>

          {/* Longitude */}
          <div>
            <label className="block text-xs font-medium text-foreground mb-1">
              {hi ? 'देशांतर' : 'Longitude'}
            </label>
            <Input
              type="number"
              step="0.0001"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              placeholder="77.2090"
              className="bg-white border-border text-sm"
            />
          </div>
        </div>

        {/* Step size */}
        <div className="flex items-center gap-3">
          <label className="text-xs font-medium text-foreground whitespace-nowrap">
            {hi ? 'चरण (मिनट)' : 'Step (minutes)'}:
          </label>
          <select
            value={stepMinutes}
            onChange={(e) => setStepMinutes(Number(e.target.value))}
            className="bg-white border border-border rounded-lg px-3 py-1.5 text-foreground text-sm focus:border-primary focus:outline-none"
          >
            <option value={1}>1 min (precise, slower)</option>
            <option value={2}>2 min (recommended)</option>
            <option value={5}>5 min (fast)</option>
          </select>
        </div>
      </div>

      {/* Life Events */}
      <div className="bg-muted rounded-xl border border-border p-4 space-y-3">
        <div className="flex items-center justify-between">
          <Heading as={4} variant={4}>{hi ? 'जीवन की घटनाएँ' : 'Life Events'}</Heading>
          <Button
            variant="outline"
            size="sm"
            onClick={addEvent}
            className="gap-1 text-xs"
          >
            <Plus className="w-3.5 h-3.5" /> {hi ? 'घटना जोड़ें' : 'Add Event'}
          </Button>
        </div>

        {events.map((ev, idx) => (
          <div key={idx} className="flex items-center gap-2 bg-white rounded-lg p-2 border border-border/50">
            <span className="text-xs text-foreground/50 w-6 text-center font-bold">{idx + 1}</span>
            <select
              value={ev.type}
              onChange={(e) => updateEvent(idx, 'type', e.target.value)}
              className="flex-1 bg-transparent border border-border rounded px-2 py-1.5 text-sm focus:border-primary focus:outline-none"
            >
              {EVENT_TYPES.map((et) => (
                <option key={et.value} value={et.value}>{et.label}</option>
              ))}
            </select>
            <Input
              type="date"
              value={ev.date}
              onChange={(e) => updateEvent(idx, 'date', e.target.value)}
              className="w-40 text-sm border-border"
            />
            <button
              onClick={() => removeEvent(idx)}
              className="p-1.5 text-red-400 hover:text-red-600 transition-colors disabled:opacity-30"
              disabled={events.length <= 1}
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        ))}

        <p className="text-xs text-foreground/50 mt-1">
          {hi
            ? 'अधिक घटनाएँ = अधिक सटीक परिणाम। कम से कम 3-4 घटनाएँ दर्ज करें।'
            : 'More events = more accurate results. Enter at least 3-4 events for best accuracy.'}
        </p>
      </div>

      {/* Submit */}
      <div className="flex items-center gap-4">
        <Button
          onClick={handleSubmit}
          disabled={loading}
          className="gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              {hi ? 'विश्लेषण हो रहा है...' : 'Analyzing...'}
            </>
          ) : (
            <>
              <Star className="w-4 h-4" />
              {hi ? 'जन्म समय ज्ञात करें' : 'Find Birth Time'}
            </>
          )}
        </Button>
        {error && (
          <div className="flex items-center gap-1 text-red-600 text-sm">
            <AlertCircle className="w-4 h-4" />
            {error}
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-4">
          {/* Summary */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <div className="flex items-center justify-between mb-3">
              <Heading as={4} variant={4}>
                {hi ? 'परिणाम' : 'Results'}
              </Heading>
              <span className={`px-2.5 py-1 text-xs font-bold rounded border ${confidenceColor(result.confidence)}`}>
                {result.confidence === 'high'
                  ? (hi ? 'उच्च विश्वास' : 'HIGH CONFIDENCE')
                  : result.confidence === 'medium'
                    ? (hi ? 'मध्यम विश्वास' : 'MEDIUM CONFIDENCE')
                    : (hi ? 'कम विश्वास' : 'LOW CONFIDENCE')}
              </span>
            </div>

            {result.best_time && (
              <div className="bg-white rounded-lg p-3 border border-primary/20 mb-3">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-sm font-semibold text-foreground">
                    {hi ? 'सर्वोत्तम जन्म समय' : 'Best Birth Time'}:
                  </span>
                  <span className="text-lg font-bold text-primary">{result.best_time}</span>
                  {result.candidates[0] && (
                    <span className="text-sm text-foreground/60 ml-2">
                      ({hi ? 'लग्न' : 'Lagna'}: {result.candidates[0].lagna})
                    </span>
                  )}
                </div>
              </div>
            )}

            <p className="text-sm text-foreground/70">{result.analysis_summary}</p>
          </div>

          {/* Candidates Table */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <Heading as={4} variant={4} className="mb-3">
              {hi ? 'शीर्ष उम्मीदवार' : 'Top Candidates'}
            </Heading>
            <div className="overflow-x-auto">
              <Table className="w-full text-xs">
                <TableHeader className="bg-muted">
                  <TableRow>
                    <TableHead className="text-left p-2 text-primary font-medium">#</TableHead>
                    <TableHead className="text-left p-2 text-primary font-medium">
                      {hi ? 'समय' : 'Time'}
                    </TableHead>
                    <TableHead className="text-center p-2 text-primary font-medium">
                      {hi ? 'अंक' : 'Score'}
                    </TableHead>
                    <TableHead className="text-left p-2 text-primary font-medium">
                      {hi ? 'लग्न' : 'Lagna'}
                    </TableHead>
                    <TableHead className="text-left p-2 text-primary font-medium">
                      {hi ? 'नक्षत्र' : 'Nakshatra'}
                    </TableHead>
                    <TableHead className="text-center p-2 text-primary font-medium">
                      {hi ? 'विवरण' : 'Details'}
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody className="divide-y divide-border/30">
                  {result.candidates.map((c, idx) => {
                    const isExpanded = expandedIdx === idx;
                    return (
                      <tr key={idx} className="group">
                        <TableCell className="p-2 align-top">
                          <div>
                            <div className={`flex items-center gap-1 ${idx === 0 ? 'text-primary font-bold' : 'text-foreground'}`}>
                              <span className="p-2 font-bold">{idx + 1}</span>
                            </div>
                            {/* Expandable detail rows */}
                            {isExpanded && c.event_matches.length > 0 && (
                              <div className="mt-2 ml-2 bg-white rounded-lg border border-border/50 p-2 col-span-6" style={{ gridColumn: '1 / -1' }}>
                                <p className="text-[10px] font-bold text-primary uppercase tracking-wide mb-1">
                                  {hi ? 'घटना विश्लेषण' : 'Event Analysis'}
                                </p>
                                {c.event_matches.map((em, emIdx) => (
                                  <div key={emIdx} className="flex items-start gap-2 py-1 border-t border-border/20 first:border-0">
                                    <span className={`text-xs font-bold w-8 text-right ${scoreColor(em.score)}`}>
                                      {em.score}
                                    </span>
                                    <div className="flex-1">
                                      <span className="text-xs font-medium text-foreground capitalize">
                                        {em.event.replace('_', ' ')}
                                      </span>
                                      <span className="text-xs text-foreground/50 ml-1">({em.date})</span>
                                      <p className="text-[10px] text-foreground/60 mt-0.5">{em.explanation}</p>
                                      <p className="text-[10px] text-foreground/40">{hi ? 'दशा' : 'Dasha'}: {em.dasha}</p>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        </TableCell>
                        <TableCell className="p-2 align-top">
                          <span className={`font-bold text-sm ${idx === 0 ? 'text-primary' : 'text-foreground'}`}>
                            {c.birth_time}
                          </span>
                        </TableCell>
                        <TableCell className="p-2 text-center align-top">
                          <span className={`font-bold text-sm ${scoreColor(c.score)}`}>
                            {c.score}
                          </span>
                        </TableCell>
                        <TableCell className="p-2 align-top">
                          <span className="text-sm text-foreground">{c.lagna}</span>
                          <span className="text-[10px] text-foreground/40 ml-1">({c.lagna_degree}°)</span>
                        </TableCell>
                        <TableCell className="p-2 align-top">
                          <span className="text-sm text-foreground">{c.nakshatra}</span>
                        </TableCell>
                        <TableCell className="p-2 text-center align-top">
                          <button
                            onClick={() => setExpandedIdx(isExpanded ? null : idx)}
                            className="p-1 rounded hover:bg-primary/10 transition-colors"
                          >
                            {isExpanded
                              ? <ChevronUp className="w-4 h-4 text-primary" />
                              : <ChevronDown className="w-4 h-4 text-primary" />}
                          </button>
                        </TableCell>
                      </tr>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
