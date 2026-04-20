import { useState } from 'react';
import { Loader2, Plus, Trash2, Clock, Star, ChevronDown, ChevronUp, AlertCircle, CheckCircle, History } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
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
  { value: 'marriage',      label: 'Marriage' },
  { value: 'child_birth',   label: 'Child Birth' },
  { value: 'job_start',     label: 'Job Start' },
  { value: 'job_loss',      label: 'Job Loss' },
  { value: 'accident',      label: 'Accident' },
  { value: 'education',     label: 'Education (Degree/Admission)' },
  { value: 'foreign_travel',label: 'Foreign Travel' },
  { value: 'property',      label: 'Property Purchase' },
  { value: 'father_death',  label: "Father's Death" },
  { value: 'mother_death',  label: "Mother's Death" },
  { value: 'health_issue',  label: 'Serious Health Issue' },
];

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdWrapCls   = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

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

  const [birthDate, setBirthDate]       = useState(initialDate || '');
  const [timeStart, setTimeStart]       = useState('06:00');
  const [timeEnd, setTimeEnd]           = useState('09:00');
  const [latitude, setLatitude]         = useState(initialPlace?.lat?.toString() || '');
  const [longitude, setLongitude]       = useState(initialPlace?.lon?.toString() || '');
  const [placeName, setPlaceName]       = useState(initialPlace?.name || '');
  const [stepMinutes, setStepMinutes]   = useState(2);
  const [events, setEvents]             = useState<LifeEvent[]>([{ date: '', type: 'marriage' }]);
  const [result, setResult]             = useState<RectificationResult | null>(null);
  const [loading, setLoading]           = useState(false);
  const [error, setError]               = useState('');
  const [expandedIdx, setExpandedIdx]   = useState<number | null>(null);

  const addEvent    = () => setEvents([...events, { date: '', type: 'marriage' }]);
  const removeEvent = (idx: number) => { if (events.length > 1) setEvents(events.filter((_, i) => i !== idx)); };
  const updateEvent = (idx: number, field: keyof LifeEvent, value: string) => {
    const updated = [...events];
    updated[idx] = { ...updated[idx], [field]: value };
    setEvents(updated);
  };

  const handleSubmit = async () => {
    setError(''); setResult(null);
    if (!birthDate)          { setError('Please enter the birth date.'); return; }
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

  const confidenceColor = (c: string) => {
    if (c === 'high')   return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    if (c === 'medium') return 'bg-amber-100 text-amber-800 border-amber-300';
    return 'bg-red-100 text-red-800 border-red-300';
  };

  const scoreColor = (s: number) =>
    s >= 70 ? 'text-emerald-600' : s >= 40 ? 'text-amber-600' : 'text-red-500';

  return (
    <div className="space-y-4">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <History className="w-6 h-6" />
          {hi ? 'जन्म समय शोधन (बी.टी.आर)' : 'Birth Time Rectification (BTR)'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi ? 'महत्वपूर्ण जीवन घटनाओं के माध्यम से अपने सटीक जन्म समय का निर्धारण करें' : 'Determine your precise birth time using major life events'}
        </p>
      </div>

      {/* ── Header ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Clock className="w-4 h-4" />
          <span>{hi ? 'जन्म समय शोधन' : 'Birth Time Rectification'}</span>
        </div>
        <div className="px-4 py-3">
          <p className="text-xs text-muted-foreground leading-relaxed">
            {hi
              ? 'यदि आपका जन्म समय निश्चित नहीं है, तो अपने जीवन की प्रमुख घटनाएँ दर्ज करें। प्रणाली दशा और गोचर विश्लेषण से सबसे संभावित जन्म समय ढूँढेगी।'
              : 'If your exact birth time is unknown, enter major life events below. The system tests multiple birth times and scores how well Dasha + Transit analysis explains each event.'}
          </p>
        </div>
      </div>

      {/* ── Birth Details ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Clock className="w-4 h-4" />
          <span>{hi ? 'जन्म विवरण' : 'Birth Details'}</span>
        </div>
        <div className="p-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-medium text-foreground mb-1">{hi ? 'जन्म तिथि' : 'Birth Date'}</label>
              <Input type="date" value={birthDate} onChange={e => setBirthDate(e.target.value)} className="bg-white border-border text-sm" />
            </div>
            <div>
              <label className="block text-xs font-medium text-foreground mb-1">{hi ? 'समय शुरू' : 'Time Window Start'}</label>
              <Input type="time" value={timeStart} onChange={e => setTimeStart(e.target.value)} className="bg-white border-border text-sm" />
            </div>
            <div>
              <label className="block text-xs font-medium text-foreground mb-1">{hi ? 'समय समाप्त' : 'Time Window End'}</label>
              <Input type="time" value={timeEnd} onChange={e => setTimeEnd(e.target.value)} className="bg-white border-border text-sm" />
            </div>
            <div>
              <label className="block text-xs font-medium text-foreground mb-1">{hi ? 'जन्म स्थान' : 'Birth Place'}</label>
              <Input type="text" value={placeName} onChange={e => setPlaceName(e.target.value)} placeholder={hi ? 'शहर का नाम' : 'City name'} className="bg-white border-border text-sm" />
            </div>
            <div>
              <label className="block text-xs font-medium text-foreground mb-1">{hi ? 'अक्षांश' : 'Latitude'}</label>
              <Input type="number" step="0.0001" value={latitude} onChange={e => setLatitude(e.target.value)} placeholder="28.6139" className="bg-white border-border text-sm" />
            </div>
            <div>
              <label className="block text-xs font-medium text-foreground mb-1">{hi ? 'देशांतर' : 'Longitude'}</label>
              <Input type="number" step="0.0001" value={longitude} onChange={e => setLongitude(e.target.value)} placeholder="77.2090" className="bg-white border-border text-sm" />
            </div>
          </div>
          <div className="flex items-center gap-3">
            <label className="text-xs font-medium text-foreground whitespace-nowrap">
              {hi ? 'चरण (मिनट)' : 'Step (minutes)'}:
            </label>
            <select
              value={stepMinutes}
              onChange={e => setStepMinutes(Number(e.target.value))}
              className="bg-white border border-border rounded-lg px-3 py-1.5 text-foreground text-sm focus:border-primary focus:outline-none"
            >
              <option value={1}>1 min (precise, slower)</option>
              <option value={2}>2 min (recommended)</option>
              <option value={5}>5 min (fast)</option>
            </select>
          </div>
        </div>
      </div>

      {/* ── Life Events ── */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Star className="w-4 h-4" />
          <span>{hi ? 'जीवन की घटनाएँ' : 'Life Events'}</span>
          <button
            onClick={addEvent}
            className="ml-auto flex items-center gap-1 text-[12px] font-normal bg-white/20 hover:bg-white/30 px-2 py-0.5 rounded transition-colors"
          >
            <Plus className="w-3 h-3" /> {hi ? 'घटना जोड़ें' : 'Add Event'}
          </button>
        </div>
        <div className="p-4 space-y-2">
          {events.map((ev, idx) => (
            <div key={idx} className="flex items-center gap-2 bg-white rounded-lg p-2 border border-border/50">
              <span className="text-xs text-muted-foreground w-5 text-center font-bold">{idx + 1}</span>
              <select
                value={ev.type}
                onChange={e => updateEvent(idx, 'type', e.target.value)}
                className="flex-1 bg-transparent border border-border rounded px-2 py-1.5 text-sm focus:border-primary focus:outline-none"
              >
                {EVENT_TYPES.map(et => (
                  <option key={et.value} value={et.value}>{et.label}</option>
                ))}
              </select>
              <Input
                type="date"
                value={ev.date}
                onChange={e => updateEvent(idx, 'date', e.target.value)}
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
          <p className="text-[11px] text-muted-foreground italic mt-1">
            {hi
              ? 'अधिक घटनाएँ = अधिक सटीक परिणाम। कम से कम 3-4 घटनाएँ दर्ज करें।'
              : 'More events = more accurate results. Enter at least 3-4 events for best accuracy.'}
          </p>
        </div>
      </div>

      {/* ── Submit ── */}
      <div className="flex items-center gap-4 px-1">
        <Button onClick={handleSubmit} disabled={loading} className="gap-2">
          {loading ? (
            <><Loader2 className="w-4 h-4 animate-spin" />{hi ? 'विश्लेषण हो रहा है...' : 'Analyzing...'}</>
          ) : (
            <><Star className="w-4 h-4" />{hi ? 'जन्म समय ज्ञात करें' : 'Find Birth Time'}</>
          )}
        </Button>
        {error && (
          <div className="flex items-center gap-1 text-red-600 text-sm">
            <AlertCircle className="w-4 h-4" />{error}
          </div>
        )}
      </div>

      {/* ── Results ── */}
      {result && (
        <div className="space-y-4">

          {/* Summary */}
          <div className={ohContainer}>
            <div className={ohHeader}>
              <CheckCircle className="w-4 h-4" />
              <span>{hi ? 'परिणाम' : 'Results'}</span>
              <span className={`ml-auto text-[11px] font-semibold px-2 py-0.5 rounded border ${confidenceColor(result.confidence)}`}>
                {result.confidence === 'high'
                  ? (hi ? 'उच्च विश्वास' : 'HIGH CONFIDENCE')
                  : result.confidence === 'medium'
                    ? (hi ? 'मध्यम विश्वास' : 'MEDIUM CONFIDENCE')
                    : (hi ? 'कम विश्वास' : 'LOW CONFIDENCE')}
              </span>
            </div>
            <div className="p-4 space-y-3">
              {result.best_time && (
                <div className="flex items-center gap-3 bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
                  <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
                  <span className="text-sm font-semibold text-foreground">
                    {hi ? 'सर्वोत्तम जन्म समय' : 'Best Birth Time'}:
                  </span>
                  <span className="text-lg font-bold text-sacred-gold-dark">{result.best_time}</span>
                  {result.candidates[0] && (
                    <span className="text-xs text-muted-foreground">
                      ({hi ? 'लग्न' : 'Lagna'}: {result.candidates[0].lagna})
                    </span>
                  )}
                </div>
              )}
              <p className="text-xs text-muted-foreground leading-relaxed">{result.analysis_summary}</p>
            </div>
          </div>

          {/* Top Candidates */}
          <div className={ohContainer}>
            <div className={ohHeader}>
              <Star className="w-4 h-4" />
              <span>{hi ? 'शीर्ष उम्मीदवार' : 'Top Candidates'}</span>
              <span className="ml-auto text-[12px] font-normal opacity-80">{result.candidates.length}</span>
            </div>
            <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
              <colgroup>
                <col style={{ width: '6%' }} />
                <col style={{ width: '14%' }} />
                <col style={{ width: '10%' }} />
                <col style={{ width: '20%' }} />
                <col style={{ width: '42%' }} />
                <col style={{ width: '8%' }} />
              </colgroup>
              <thead>
                <tr>
                  <th className={thCls}>#</th>
                  <th className={thCls}>{hi ? 'समय' : 'Time'}</th>
                  <th className={thCls}>{hi ? 'अंक' : 'Score'}</th>
                  <th className={thCls}>{hi ? 'लग्न' : 'Lagna'}</th>
                  <th className={thCls}>{hi ? 'नक्षत्र' : 'Nakshatra'}</th>
                  <th className={thCls}>{hi ? 'विवरण' : 'Detail'}</th>
                </tr>
              </thead>
              <tbody>
                {result.candidates.map((c, idx) => {
                  const isExpanded = expandedIdx === idx;
                  const isBest = idx === 0;
                  return (
                    <>
                      <tr key={idx} className={isBest ? 'bg-sacred-gold/5' : ''}>
                        <td className={`${tdCls} font-bold text-center ${isBest ? 'text-sacred-gold-dark' : ''}`}>{idx + 1}</td>
                        <td className={`${tdCls} font-bold ${isBest ? 'text-sacred-gold-dark' : ''}`}>{c.birth_time}</td>
                        <td className={`${tdCls} text-center font-bold ${scoreColor(c.score)}`}>{c.score}</td>
                        <td className={tdCls}>
                          <span className="font-medium">{c.lagna}</span>
                          <span className="text-muted-foreground ml-1 text-[10px]">({c.lagna_degree}°)</span>
                        </td>
                        <td className={tdWrapCls}>{c.nakshatra}</td>
                        <td className={`${tdCls} text-center`}>
                          <button
                            onClick={() => setExpandedIdx(isExpanded ? null : idx)}
                            className="p-1 rounded hover:bg-muted/40 transition-colors"
                          >
                            {isExpanded
                              ? <ChevronUp className="w-3.5 h-3.5 text-primary" />
                              : <ChevronDown className="w-3.5 h-3.5 text-primary" />}
                          </button>
                        </td>
                      </tr>
                      {isExpanded && c.event_matches.length > 0 && (
                        <tr key={`${idx}-detail`}>
                          <td colSpan={6} className="px-4 py-3 bg-muted/30 border-t border-border">
                            <p className="text-[10px] font-bold text-primary uppercase tracking-wide mb-2">
                              {hi ? 'घटना विश्लेषण' : 'Event Analysis'}
                            </p>
                            <div className="space-y-2">
                              {c.event_matches.map((em, emIdx) => (
                                <div key={emIdx} className="flex items-start gap-2 py-1 border-t border-border/30 first:border-0">
                                  <span className={`text-xs font-bold w-8 text-right shrink-0 ${scoreColor(em.score)}`}>
                                    {em.score}
                                  </span>
                                  <div className="flex-1 min-w-0">
                                    <span className="text-xs font-medium text-foreground capitalize">
                                      {em.event.replace('_', ' ')}
                                    </span>
                                    <span className="text-xs text-muted-foreground ml-1">({em.date})</span>
                                    <p className="text-[10px] text-muted-foreground mt-0.5 leading-relaxed">{em.explanation}</p>
                                    <p className="text-[10px] text-muted-foreground/70">{hi ? 'दशा' : 'Dasha'}: {em.dasha}</p>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </td>
                        </tr>
                      )}
                    </>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
