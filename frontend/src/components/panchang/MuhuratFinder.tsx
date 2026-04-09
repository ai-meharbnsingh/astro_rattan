import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Search, Loader2, CalendarDays, Star, MapPin } from 'lucide-react';

interface MuhuratFinderProps {
  latitude: string;
  longitude: string;
  onLatChange: (val: string) => void;
  onLonChange: (val: string) => void;
}

interface MuhuratType {
  id: string;
  name: string;
}

interface MuhuratWindow {
  start_time: string;
  end_time: string;
  quality: string;
  factors?: string[];
}

interface MonthlyDay {
  date: string;
  has_muhurat: boolean;
  quality?: string;
  windows_count?: number;
}

function todayString(): string {
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}

function qualityIcon(quality: string) {
  switch (quality.toLowerCase()) {
    case 'excellent':
      return <Star className="h-4 w-4 fill-sacred-gold text-sacred-gold" />;
    case 'good':
      return <Star className="h-4 w-4 fill-green-400 text-green-400" />;
    case 'average':
    case 'neutral':
      return <Star className="h-4 w-4 fill-amber-400 text-amber-400" />;
    case 'poor':
    case 'inauspicious':
      return <Star className="h-4 w-4 fill-red-400 text-red-400" />;
    default:
      return <Star className="h-4 w-4 text-cosmic-text-secondary" />;
  }
}

function qualityLabel(quality: string): string {
  switch (quality.toLowerCase()) {
    case 'excellent':
      return 'bg-sacred-gold/15 text-sacred-gold border-sacred-gold/30';
    case 'good':
      return 'bg-green-500/15 text-green-400 border-green-500/30';
    case 'average':
    case 'neutral':
      return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
    case 'poor':
    case 'inauspicious':
      return 'bg-red-500/15 text-red-400 border-red-500/30';
    default:
      return 'bg-cosmic-text-secondary/15 text-cosmic-text-secondary border-cosmic-text-secondary/30';
  }
}

function qualityDotColor(quality?: string): string {
  if (!quality) return 'bg-cosmic-text-secondary/30';
  switch (quality.toLowerCase()) {
    case 'excellent':
      return 'bg-sacred-gold';
    case 'good':
      return 'bg-green-400';
    case 'average':
    case 'neutral':
      return 'bg-amber-400';
    case 'poor':
    case 'inauspicious':
      return 'bg-red-400';
    default:
      return 'bg-cosmic-text-secondary/30';
  }
}

function qualityTextColor(quality?: string): string {
  if (!quality) return 'text-cosmic-text-secondary';
  switch (quality.toLowerCase()) {
    case 'excellent':
      return 'text-sacred-gold';
    case 'good':
      return 'text-green-400';
    case 'average':
    case 'neutral':
      return 'text-amber-400';
    case 'poor':
    case 'inauspicious':
      return 'text-red-400';
    default:
      return 'text-cosmic-text-secondary';
  }
}

export default function MuhuratFinder({
  latitude,
  longitude,
  onLatChange,
  onLonChange,
}: MuhuratFinderProps) {
  const [muhuratTypes, setMuhuratTypes] = useState<MuhuratType[]>([]);
  const [selectedEventType, setSelectedEventType] = useState<string>('');
  const [muhuratDate, setMuhuratDate] = useState<string>(todayString());
  const [muhuratWindows, setMuhuratWindows] = useState<MuhuratWindow[]>([]);
  const [muhuratLoading, setMuhuratLoading] = useState<boolean>(false);
  const [monthlyView, setMonthlyView] = useState<MonthlyDay[]>([]);
  const [monthlyLoading, setMonthlyLoading] = useState<boolean>(false);
  const [showMonthly, setShowMonthly] = useState<boolean>(false);

  useEffect(() => {
    async function fetchTypes() {
      // Hardcoded muhurat types — API doesn't have this endpoint
      const types: MuhuratType[] = [
        { id: 'marriage', name: 'Marriage (Vivah)' },
        { id: 'griha_pravesh', name: 'Griha Pravesh' },
        { id: 'business_start', name: 'Business Start' },
        { id: 'travel', name: 'Travel' },
        { id: 'naming_ceremony', name: 'Naming Ceremony' },
        { id: 'mundan', name: 'Mundan' },
      ];
      setMuhuratTypes(types);
      setSelectedEventType(types[0].id);
    }
    fetchTypes();
  }, []);

  async function findMuhurat() {
    if (!selectedEventType || !muhuratDate) return;
    setMuhuratLoading(true);
    setMuhuratWindows([]);
    try {
      const params = new URLSearchParams({
        event_type: selectedEventType,
        date: muhuratDate,
        latitude,
        longitude,
      });
      const data = await api.get(`/api/muhurat/find?${params.toString()}`);
      setMuhuratWindows(Array.isArray(data.windows) ? data.windows : []);
    } catch {
      setMuhuratWindows([]);
    }
    setMuhuratLoading(false);
  }

  async function fetchMonthlyView() {
    if (!selectedEventType) return;
    setMonthlyLoading(true);
    setMonthlyView([]);
    setShowMonthly(true);
    try {
      const [year, month] = muhuratDate.split('-');
      const params = new URLSearchParams({
        event_type: selectedEventType,
        year,
        month,
        latitude,
        longitude,
      });
      const data = await api.get(`/api/muhurat/monthly?${params.toString()}`);
      setMonthlyView(Array.isArray(data) ? data : data.days ?? []);
    } catch {
      setMonthlyView([]);
    }
    setMonthlyLoading(false);
  }

  const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // Compute leading blanks for the monthly grid so day 1 lands on the correct weekday
  const firstDayOffset = monthlyView.length > 0
    ? new Date(monthlyView[0].date).getDay()
    : 0;

  return (
    <div className="flex flex-col gap-6">
      {/* Section title */}
      <div className="flex items-center gap-3">
        <span className="inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-0.5 rounded-full border bg-sacred-gold/10 text-sacred-gold border-sacred-gold/20">
          <Search className="h-3 w-3" />
          Muhurat Finder
        </span>
        <h3 className="text-lg font-semibold text-cosmic-text">
          Find Auspicious Times
        </h3>
      </div>

      {/* Search controls */}
      <Card className="bg-cosmic-card border-sacred-gold/10">
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            {/* Event type dropdown */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-cosmic-text-secondary">Event Type</label>
              <select
                value={selectedEventType}
                onChange={(e) => setSelectedEventType(e.target.value)}
                className="h-9 w-full rounded-md border border-sacred-gold/20 bg-cosmic-card px-3 text-sm text-cosmic-text focus:outline-none focus:ring-2 focus:ring-sacred-gold/30"
              >
                {muhuratTypes.length === 0 && (
                  <option value="">Loading...</option>
                )}
                {muhuratTypes.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Date picker */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-cosmic-text-secondary">Date</label>
              <input
                type="date"
                value={muhuratDate}
                onChange={(e) => setMuhuratDate(e.target.value)}
                className="h-9 w-full rounded-md border border-sacred-gold/20 bg-cosmic-card px-3 text-sm text-cosmic-text focus:outline-none focus:ring-2 focus:ring-sacred-gold/30"
              />
            </div>

            {/* Latitude */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-cosmic-text-secondary flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                Latitude
              </label>
              <input
                type="text"
                value={latitude}
                onChange={(e) => onLatChange(e.target.value)}
                placeholder="28.6139"
                className="h-9 w-full rounded-md border border-sacred-gold/20 bg-cosmic-card px-3 text-sm text-cosmic-text focus:outline-none focus:ring-2 focus:ring-sacred-gold/30"
              />
            </div>

            {/* Longitude */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-cosmic-text-secondary flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                Longitude
              </label>
              <input
                type="text"
                value={longitude}
                onChange={(e) => onLonChange(e.target.value)}
                placeholder="77.2090"
                className="h-9 w-full rounded-md border border-sacred-gold/20 bg-cosmic-card px-3 text-sm text-cosmic-text focus:outline-none focus:ring-2 focus:ring-sacred-gold/30"
              />
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap gap-3">
            <Button
              onClick={findMuhurat}
              disabled={muhuratLoading || !selectedEventType}
              className="bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20 hover:bg-sacred-gold/20"
            >
              {muhuratLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              Find Muhurat
            </Button>
            <Button
              onClick={fetchMonthlyView}
              disabled={monthlyLoading || !selectedEventType}
              variant="outline"
              className="border-sacred-gold/20 text-cosmic-text hover:bg-sacred-gold/10"
            >
              {monthlyLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <CalendarDays className="h-4 w-4" />
              )}
              Monthly View
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Muhurat windows results */}
      {muhuratWindows.length > 0 && (
        <div className="flex flex-col gap-3">
          <h4 className="text-sm font-medium text-cosmic-text-secondary">
            Auspicious Windows
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {muhuratWindows.map((w, idx) => (
              <Card key={idx} className="bg-cosmic-card border-sacred-gold/10">
                <CardContent>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="flex items-center gap-2">
                      {qualityIcon(w.quality)}
                      <span className="text-cosmic-text font-semibold text-sm">
                        {w.start_time} &ndash; {w.end_time}
                      </span>
                    </div>
                    <span
                      className={`inline-block text-xs font-medium px-2.5 py-0.5 rounded-full border capitalize ${qualityLabel(w.quality)}`}
                    >
                      {w.quality}
                    </span>
                  </div>
                  {w.factors && w.factors.length > 0 && (
                    <div className="flex flex-wrap gap-1.5">
                      {w.factors.map((factor, fi) => (
                        <span
                          key={fi}
                          className="text-xs px-2 py-0.5 rounded-full bg-sacred-gold/5 text-cosmic-text-secondary border border-sacred-gold/10"
                        >
                          {factor}
                        </span>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Empty state after search */}
      {!muhuratLoading && muhuratWindows.length === 0 && muhuratDate && selectedEventType && (
        <div /> // no output until user triggers search
      )}

      {/* Monthly calendar view */}
      {showMonthly && (
        <Card className="bg-cosmic-card border-sacred-gold/10">
          <CardContent>
            <div className="flex items-center gap-2 mb-4">
              <CalendarDays className="h-5 w-5 text-sacred-gold" />
              <h3 className="text-lg font-semibold text-cosmic-text">
                Monthly Muhurat Calendar
              </h3>
            </div>

            {monthlyLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-6 w-6 animate-spin text-sacred-gold" />
              </div>
            ) : monthlyView.length === 0 ? (
              <p className="text-sm text-cosmic-text-secondary italic">
                No data available for this month
              </p>
            ) : (
              <div className="grid grid-cols-7 gap-1">
                {/* Weekday headers */}
                {weekDays.map((day) => (
                  <div
                    key={day}
                    className="text-center text-xs font-medium text-cosmic-text-secondary py-2"
                  >
                    {day}
                  </div>
                ))}

                {/* Leading blanks */}
                {Array.from({ length: firstDayOffset }).map((_, i) => (
                  <div key={`blank-${i}`} />
                ))}

                {/* Day cells */}
                {monthlyView.map((day) => {
                  const dayNum = new Date(day.date).getDate();
                  return (
                    <div
                      key={day.date}
                      className={`relative flex flex-col items-center justify-center rounded-lg p-2 min-h-[3rem] border ${
                        day.has_muhurat
                          ? 'border-sacred-gold/20 bg-sacred-gold/5'
                          : 'border-transparent bg-cosmic-card'
                      }`}
                    >
                      <span
                        className={`text-sm font-medium ${
                          day.has_muhurat
                            ? qualityTextColor(day.quality)
                            : 'text-cosmic-text-secondary'
                        }`}
                      >
                        {dayNum}
                      </span>
                      {day.has_muhurat && (
                        <div className="flex items-center gap-1 mt-0.5">
                          <span
                            className={`w-1.5 h-1.5 rounded-full ${qualityDotColor(day.quality)}`}
                          />
                          {day.windows_count != null && day.windows_count > 0 && (
                            <span className="text-xs text-cosmic-text-secondary">
                              {day.windows_count}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
