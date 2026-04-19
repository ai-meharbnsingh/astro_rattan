import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { Loader2, ChevronLeft, ChevronRight, ChevronDown, Search, CheckCircle2, AlertTriangle, AlertCircle, Navigation } from 'lucide-react';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */
interface Activity {
  key: string;
  name: string;
  name_hindi: string;
  icon: string;
  description: string;
  description_hindi: string;
}

interface LagnaWindow {
  lagna: string;
  start: string;
  end: string;
  degree?: number;
  ganda_sandhi?: string | null;
  warnings?: string[];
  safe_window?: { start: string; end: string };
}

interface LagnaScore {
  lagna: string;
  lord: string;
  score: number;
  start: string;
  end: string;
}

interface ChandraBalam {
  house: number;
  favorable: boolean;
  interpretation_en: string;
  interpretation_hi: string;
}

interface TaraBalam {
  tara: number;
  tara_name: string;
  favorable: boolean;
  interpretation_en: string;
  interpretation_hi: string;
}

interface HoraWindow {
  hora: string;
  lord: string;
  start: string;
  end: string;
}

interface MuhuratDate {
  date: string;
  weekday: string;
  weekday_hindi: string;
  tithi: string;
  nakshatra: string;
  paksha: string;
  score: number;
  reasons_good: string[];
  reasons_good_hindi?: string[];
  reasons_bad?: string[];
  reasons_bad_hindi?: string[];
  sunrise: string;
  sunset: string;
  rahu_kaal: { start: string; end: string } | string;
  lagna_windows: LagnaWindow[];
  lagnasuddhi?: LagnaScore | null;
  vivaha_quality?: number;
  vivaha_paryapta?: boolean;
  summary?: string;
  chandra_balam?: ChandraBalam | null;
  tara_balam?: TaraBalam | null;
  recommended_hora_windows?: HoraWindow[];
  muhurat_score?: number;
  quality?: string;
  dosha_cancellations?: string[];
}

interface MarriageSeasonCalendar {
  allowed_months: string[];
  forbidden_months: string[];
}

interface MuhuratResult {
  activity: Activity;
  month: number;
  year: number;
  dates: MuhuratDate[];
  total_favorable: number;
  marriage_season_calendar?: MarriageSeasonCalendar;
}

interface TravelDate {
  date: string;
  weekday: string;
  weekday_hindi: string;
  tithi: string;
  nakshatra: string;
  paksha: string;
  score: number;
  reasons_good: string[];
  reasons_bad: string[];
  sunrise: string;
  sunset: string;
  rahu_kaal: { start: string; end: string } | string;
}

interface TravelResult {
  direction: string;
  month: number;
  year: number;
  dates: TravelDate[];
  total_favorable: number;
  pushya_guide: { en: string; hi: string };
}

interface Props {
  language: string;
  t: (key: string) => string;
  latitude: string;
  longitude: string;
}

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */
const MONTH_NAMES_EN = [
  '', 'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];
const MONTH_NAMES_HI = [
  '', 'जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
  'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर',
];

const DIRECTIONS = [
  { key: 'NW', en: 'NW', hi: 'उत्तर-पश्चिम', row: 0, col: 0 },
  { key: 'N',  en: 'N',  hi: 'उत्तर',        row: 0, col: 1 },
  { key: 'NE', en: 'NE', hi: 'उत्तर-पूर्व',  row: 0, col: 2 },
  { key: 'W',  en: 'W',  hi: 'पश्चिम',       row: 1, col: 0 },
  { key: 'E',  en: 'E',  hi: 'पूर्व',        row: 1, col: 2 },
  { key: 'SW', en: 'SW', hi: 'दक्षिण-पश्चिम', row: 2, col: 0 },
  { key: 'S',  en: 'S',  hi: 'दक्षिण',       row: 2, col: 1 },
  { key: 'SE', en: 'SE', hi: 'दक्षिण-पूर्व', row: 2, col: 2 },
];

function formatDate(dateStr: string, language: string): string {
  try {
    const d = new Date(dateStr + 'T12:00:00');
    return d.toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-IN', {
      weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
    });
  } catch {
    return dateStr;
  }
}

function RahuKaalDisplay({ rahu_kaal }: { rahu_kaal: { start: string; end: string } | string }) {
  if (typeof rahu_kaal === 'object' && rahu_kaal) return <>{rahu_kaal.start} - {rahu_kaal.end}</>;
  return <>{String(rahu_kaal || '--')}</>;
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */
export default function MuhuratFinderTab({ language, t, latitude, longitude }: Props) {
  const [mode, setMode] = useState<'activity' | 'travel'>('activity');

  /* ---- Activity state ---- */
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loadingActivities, setLoadingActivities] = useState(true);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [results, setResults] = useState<MuhuratResult | null>(null);
  const [loadingResults, setLoadingResults] = useState(false);
  const [searched, setSearched] = useState(false);
  const [showPersonal, setShowPersonal] = useState(false);
  const [birthNakshatra, setBirthNakshatra] = useState<number | null>(null);
  const [birthMoonRashi, setBirthMoonRashi] = useState<number | null>(null);

  /* ---- Travel state ---- */
  const [selectedDirection, setSelectedDirection] = useState<string | null>(null);
  const [travelResults, setTravelResults] = useState<TravelResult | null>(null);
  const [loadingTravel, setLoadingTravel] = useState(false);
  const [travelSearched, setTravelSearched] = useState(false);

  /* ---- Shared month/year ---- */
  const now = new Date();
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [year, setYear] = useState(now.getFullYear());

  // Fetch activities on mount
  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoadingActivities(true);
      try {
        const data = await api.get(`/api/muhurat/activities?lang=${language}`);
        if (!cancelled && data?.activities) setActivities(data.activities);
      } catch {
        // silently fail
      } finally {
        if (!cancelled) setLoadingActivities(false);
      }
    })();
    return () => { cancelled = true; };
  }, [language]);

  const goToPrevMonth = () => {
    if (month === 1) { setMonth(12); setYear(y => y - 1); }
    else setMonth(m => m - 1);
  };
  const goToNextMonth = () => {
    if (month === 12) { setMonth(1); setYear(y => y + 1); }
    else setMonth(m => m + 1);
  };

  const monthLabel = language === 'hi'
    ? `${MONTH_NAMES_HI[month]} ${year}`
    : `${MONTH_NAMES_EN[month]} ${year}`;

  /* ---- Activity search ---- */
  const handleSearch = async () => {
    if (!selectedActivity) return;
    setLoadingResults(true);
    setSearched(true);
    setResults(null);
    try {
      const params = new URLSearchParams({
        activity: selectedActivity.key,
        month: String(month),
        year: String(year),
        latitude,
        longitude,
        lang: language,
      });
      if (birthNakshatra !== null) params.append('birth_nakshatra', String(birthNakshatra));
      if (birthMoonRashi !== null) params.append('birth_moon_rashi', String(birthMoonRashi));
      const data = await api.get(`/api/muhurat/finder?${params}`);
      if (data) setResults(data as MuhuratResult);
    } catch {
      // keep results null
    } finally {
      setLoadingResults(false);
    }
  };

  /* ---- Travel search ---- */
  const handleTravelSearch = async () => {
    if (!selectedDirection) return;
    setLoadingTravel(true);
    setTravelSearched(true);
    setTravelResults(null);
    try {
      const params = new URLSearchParams({
        direction: selectedDirection,
        month: String(month),
        year: String(year),
        latitude,
        longitude,
      });
      const data = await api.get(`/api/muhurat/travel?${params}`);
      if (data) setTravelResults(data as TravelResult);
    } catch {
      // keep results null
    } finally {
      setLoadingTravel(false);
    }
  };

  /* ================================================================ */
  /*  Render                                                           */
  /* ================================================================ */
  return (
    <div className="space-y-4">

      {/* ---- Mode toggle ---- */}
      <div className="flex rounded-lg border border-border overflow-hidden">
        <button
          type="button"
          onClick={() => setMode('activity')}
          className={`flex-1 py-2 text-sm font-semibold transition-colors ${
            mode === 'activity'
              ? 'bg-sacred-gold text-white'
              : 'bg-card text-muted-foreground hover:text-foreground'
          }`}
        >
          {language === 'hi' ? '🪔 कार्य मुहूर्त' : '🪔 Activity Muhurat'}
        </button>
        <button
          type="button"
          onClick={() => setMode('travel')}
          className={`flex-1 py-2 text-sm font-semibold transition-colors ${
            mode === 'travel'
              ? 'bg-sacred-gold text-white'
              : 'bg-card text-muted-foreground hover:text-foreground'
          }`}
        >
          {language === 'hi' ? '✈️ यात्रा मुहूर्त' : '✈️ Travel Muhurat'}
        </button>
      </div>

      {/* ================================================================ */}
      {/* ACTIVITY MODE                                                     */}
      {/* ================================================================ */}
      {mode === 'activity' && (
        <>
          <div className="text-center mb-2">
            <h3 className="text-lg font-bold text-foreground">
              {language === 'hi' ? 'शुभ मुहूर्त खोजक' : 'Auspicious Muhurat Finder'}
            </h3>
            <p className="text-sm text-muted-foreground">
              {language === 'hi'
                ? 'कार्य चुनें, माह चुनें, शुभ तिथियाँ पाएँ'
                : 'Select an activity, pick a month, find auspicious dates'}
            </p>
          </div>

          {/* Activity grid */}
          {loadingActivities ? (
            <div className="flex justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {activities.map(act => {
                const isSelected = selectedActivity?.key === act.key;
                return (
                  <button
                    key={act.key}
                    type="button"
                    onClick={() => { setSelectedActivity(act); setSearched(false); setResults(null); }}
                    className={`border rounded-xl p-3 cursor-pointer hover:border-sacred-gold transition-colors text-left ${
                      isSelected
                        ? 'border-sacred-gold bg-sacred-gold/5 ring-2 ring-sacred-gold'
                        : 'border-border bg-card'
                    }`}
                  >
                    <div className="text-2xl mb-1">{act.icon}</div>
                    <div className="font-semibold text-sm text-foreground leading-tight">
                      {language === 'hi' ? act.name_hindi : act.name}
                    </div>
                    <div className="text-xs text-muted-foreground mt-0.5 line-clamp-2">
                      {language === 'hi' ? act.description_hindi : act.description}
                    </div>
                  </button>
                );
              })}
            </div>
          )}

          {/* Month picker + search */}
          {selectedActivity && (
            <Card className="border border-sacred-gold/20">
              <CardContent className="p-3 space-y-3">
                <div className="flex items-center justify-between">
                  <Button variant="ghost" size="sm" onClick={goToPrevMonth} className="px-2">
                    <ChevronLeft className="w-4 h-4" />
                  </Button>
                  <span className="font-semibold text-foreground">{monthLabel}</span>
                  <Button variant="ghost" size="sm" onClick={goToNextMonth} className="px-2">
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                </div>

                {/* Personal options */}
                <div className="border-t border-border/40 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowPersonal(s => !s)}
                    className="w-full flex items-center justify-between text-sm text-muted-foreground hover:text-foreground py-1"
                  >
                    <span>
                      {language === 'hi' ? 'व्यक्तिगत मुहूर्त (वैकल्पिक)' : 'Personal Muhurat (optional)'}
                    </span>
                    <ChevronDown className={`w-4 h-4 transition-transform ${showPersonal ? 'rotate-180' : ''}`} />
                  </button>

                  {showPersonal && (
                    <div className="space-y-2 pt-2 border-t border-border/50">
                      <p className="text-xs text-muted-foreground">
                        {language === 'hi'
                          ? 'चन्द्रबल + तारा बल गणना के लिए जन्म विवरण दें'
                          : 'Enter for personalized Chandra Balam + Tara Balam scoring'}
                      </p>

                      <div className="space-y-1">
                        <label className="text-xs font-medium text-foreground">
                          {language === 'hi' ? 'जन्म नक्षत्र' : 'Birth Nakshatra'}
                        </label>
                        <select
                          value={birthNakshatra !== null ? String(birthNakshatra) : ''}
                          onChange={e => setBirthNakshatra(e.target.value === '' ? null : Number(e.target.value))}
                          className="w-full rounded-md border border-input bg-background px-2 py-1.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-sacred-gold"
                        >
                          <option value="">{language === 'hi' ? '-- चुनें --' : '-- Not set --'}</option>
                          {[
                            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
                            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni',
                            'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha',
                            'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha',
                            'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
                            'Uttara Bhadrapada', 'Revati',
                          ].map((name, idx) => (
                            <option key={idx} value={idx}>{idx + 1}. {name}</option>
                          ))}
                        </select>
                      </div>

                      <div className="space-y-1">
                        <label className="text-xs font-medium text-foreground">
                          {language === 'hi' ? 'जन्म चन्द्र राशि' : 'Birth Moon Sign'}
                        </label>
                        <select
                          value={birthMoonRashi !== null ? String(birthMoonRashi) : ''}
                          onChange={e => setBirthMoonRashi(e.target.value === '' ? null : Number(e.target.value))}
                          className="w-full rounded-md border border-input bg-background px-2 py-1.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-sacred-gold"
                        >
                          <option value="">{language === 'hi' ? '-- चुनें --' : '-- Not set --'}</option>
                          {[
                            'Aries / Mesh', 'Taurus / Vrishabha', 'Gemini / Mithuna', 'Cancer / Karka',
                            'Leo / Simha', 'Virgo / Kanya', 'Libra / Tula', 'Scorpio / Vrishchika',
                            'Sagittarius / Dhanu', 'Capricorn / Makara', 'Aquarius / Kumbha', 'Pisces / Meena',
                          ].map((name, idx) => (
                            <option key={idx} value={idx}>{name}</option>
                          ))}
                        </select>
                      </div>
                    </div>
                  )}
                </div>

                <Button
                  onClick={handleSearch}
                  disabled={loadingResults}
                  className="w-full btn-sacred flex items-center justify-center gap-2"
                >
                  {loadingResults ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                  {language === 'hi' ? 'मुहूर्त खोजें' : 'Find Muhurat'}
                </Button>
              </CardContent>
            </Card>
          )}

          {loadingResults && (
            <div className="flex justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
            </div>
          )}

          {!loadingResults && searched && (
            <div className="space-y-3">
              <div className="text-center">
                <p className="text-sm font-semibold text-foreground">
                  {results && results.total_favorable > 0
                    ? (language === 'hi'
                        ? `${results.total_favorable} शुभ तिथियाँ — ${results.activity.name_hindi} — ${monthLabel}`
                        : `${results.total_favorable} Auspicious Dates for ${results.activity.name} in ${monthLabel}`)
                    : (language === 'hi' ? 'इस माह कोई शुभ तिथि नहीं मिली' : 'No auspicious dates found this month')
                  }
                </p>
              </div>

              {/* Marriage season calendar */}
              {results?.activity?.key === 'marriage' && results?.marriage_season_calendar && (
                <div className="space-y-2 bg-pink-50 border border-pink-200 rounded-lg p-3">
                  <p className="text-xs font-bold text-pink-700">
                    {language === 'hi' ? 'अनुकूल माह' : 'Favorable Months'}
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {results.marriage_season_calendar.allowed_months?.map((m) => (
                      <span key={m} className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded-full">{m}</span>
                    ))}
                  </div>
                  {results.marriage_season_calendar.forbidden_months?.length > 0 && (
                    <>
                      <p className="text-xs font-bold text-pink-700 mt-2">
                        {language === 'hi' ? 'वर्जित माह' : 'Forbidden Months'}
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {results.marriage_season_calendar.forbidden_months.map((m) => (
                          <span key={m} className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded-full opacity-70">{m}</span>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              )}

              {/* Date cards */}
              {results?.dates?.map((d, idx) => (
                <MuhuratDateCard key={`${d.date}-${idx}`} d={d} language={language} activityKey={results?.activity?.key} />
              ))}

              {results && results.total_favorable === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Search className="w-8 h-8 mx-auto mb-2 opacity-40" />
                  <p className="text-sm">
                    {language === 'hi'
                      ? 'इस माह कोई शुभ मुहूर्त उपलब्ध नहीं है। अगला माह देखें।'
                      : 'No auspicious muhurat available this month. Try the next month.'}
                  </p>
                </div>
              )}
            </div>
          )}
        </>
      )}

      {/* ================================================================ */}
      {/* TRAVEL MODE                                                       */}
      {/* ================================================================ */}
      {mode === 'travel' && (
        <>
          <div className="text-center mb-2">
            <h3 className="text-lg font-bold text-foreground">
              {language === 'hi' ? 'यात्रा मुहूर्त' : 'Travel Muhurat'}
            </h3>
            <p className="text-sm text-muted-foreground">
              {language === 'hi'
                ? 'यात्रा की दिशा चुनें और शुभ तिथियाँ जानें'
                : 'Choose your travel direction and find auspicious dates'}
            </p>
          </div>

          {/* Compass direction picker */}
          <Card className="border border-sacred-gold/20">
            <CardContent className="p-4">
              <p className="text-xs font-semibold text-center text-muted-foreground mb-3">
                {language === 'hi' ? 'यात्रा की दिशा चुनें' : 'Select Travel Direction'}
              </p>

              {/* 3×3 compass grid — center is the compass icon */}
              <div className="grid grid-cols-3 gap-2 max-w-[220px] mx-auto">
                {[0, 1, 2].map(row => (
                  [0, 1, 2].map(col => {
                    const dir = DIRECTIONS.find(d => d.row === row && d.col === col);
                    if (!dir) {
                      // Center cell
                      return (
                        <div key={`${row}-${col}`} className="flex items-center justify-center h-14">
                          <Navigation className="w-6 h-6 text-sacred-gold opacity-60" />
                        </div>
                      );
                    }
                    const isSelected = selectedDirection === dir.key;
                    return (
                      <button
                        key={dir.key}
                        type="button"
                        onClick={() => { setSelectedDirection(dir.key); setTravelSearched(false); setTravelResults(null); }}
                        className={`h-14 rounded-xl border text-center transition-all font-semibold text-sm flex flex-col items-center justify-center gap-0.5 ${
                          isSelected
                            ? 'border-sacred-gold bg-sacred-gold/10 ring-2 ring-sacred-gold text-sacred-gold'
                            : 'border-border bg-card text-foreground hover:border-sacred-gold/60'
                        }`}
                      >
                        <span className="text-base leading-none">{dir.en}</span>
                        <span className="text-[9px] text-muted-foreground leading-none">
                          {language === 'hi' ? dir.hi : dir.en === 'N' ? 'North' : dir.en === 'S' ? 'South' : dir.en === 'E' ? 'East' : dir.en === 'W' ? 'West' : dir.en === 'NE' ? 'NE' : dir.en === 'NW' ? 'NW' : dir.en === 'SE' ? 'SE' : 'SW'}
                        </span>
                      </button>
                    );
                  })
                ))}
              </div>

              {/* Month picker */}
              <div className="flex items-center justify-between mt-4 border-t border-border/40 pt-3">
                <Button variant="ghost" size="sm" onClick={goToPrevMonth} className="px-2">
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <span className="font-semibold text-foreground text-sm">{monthLabel}</span>
                <Button variant="ghost" size="sm" onClick={goToNextMonth} className="px-2">
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>

              <Button
                onClick={handleTravelSearch}
                disabled={!selectedDirection || loadingTravel}
                className="w-full btn-sacred flex items-center justify-center gap-2 mt-3"
              >
                {loadingTravel ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                {language === 'hi' ? 'यात्रा मुहूर्त खोजें' : 'Find Travel Muhurat'}
              </Button>
            </CardContent>
          </Card>

          {loadingTravel && (
            <div className="flex justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
            </div>
          )}

          {!loadingTravel && travelSearched && (
            <div className="space-y-3">
              {/* Results header */}
              <div className="text-center">
                <p className="text-sm font-semibold text-foreground">
                  {travelResults && travelResults.total_favorable > 0
                    ? (language === 'hi'
                        ? `${travelResults.total_favorable} शुभ तिथियाँ — ${DIRECTIONS.find(d => d.key === travelResults.direction)?.hi || travelResults.direction} दिशा — ${monthLabel}`
                        : `${travelResults.total_favorable} Auspicious Dates for ${travelResults.direction} travel in ${monthLabel}`)
                    : (language === 'hi' ? 'इस माह कोई शुभ यात्रा तिथि नहीं मिली' : 'No auspicious travel dates found this month')
                  }
                </p>
              </div>

              {/* Pushya guide */}
              {travelResults?.pushya_guide && (
                <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-800">
                  ⭐ {language === 'hi' ? travelResults.pushya_guide.hi : travelResults.pushya_guide.en}
                </div>
              )}

              {/* Travel date cards */}
              {travelResults?.dates?.map((d, idx) => (
                <div
                  key={`${d.date}-${idx}`}
                  className="border border-sacred-gold/20 bg-[#FFF9F5] rounded-lg p-3 space-y-2"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="font-semibold text-foreground">{formatDate(d.date, language)}</div>
                      <div className="text-xs text-muted-foreground">
                        {language === 'hi' ? d.weekday_hindi : d.weekday}
                      </div>
                    </div>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                      d.score >= 90 ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {d.score}/100
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-1.5 text-xs">
                    <span className="bg-orange-50 text-orange-700 px-2 py-0.5 rounded">{d.tithi}</span>
                    <span className="bg-purple-50 text-purple-700 px-2 py-0.5 rounded">{d.nakshatra}</span>
                    <span className="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded">{d.paksha}</span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-xs text-muted-foreground">
                    <div>
                      <span className="font-medium text-foreground">{language === 'hi' ? 'सूर्योदय' : 'Sunrise'}</span>
                      <br />{d.sunrise}
                    </div>
                    <div>
                      <span className="font-medium text-foreground">{language === 'hi' ? 'सूर्यास्त' : 'Sunset'}</span>
                      <br />{d.sunset}
                    </div>
                    <div>
                      <span className="font-medium text-foreground flex items-center gap-0.5">
                        <AlertTriangle className="w-3 h-3 text-red-500" />
                        {language === 'hi' ? 'राहुकाल' : 'Rahu Kaal'}
                      </span>
                      <br /><RahuKaalDisplay rahu_kaal={d.rahu_kaal} />
                    </div>
                  </div>

                  {d.reasons_good?.length > 0 && (
                    <div className="space-y-0.5">
                      {d.reasons_good.map((reason, i) => (
                        <div key={i} className="flex items-start gap-1 text-xs text-green-700">
                          <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                          <span>{reason}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {d.reasons_bad?.length > 0 && (
                    <div className="space-y-0.5 mt-1 border-t border-red-100 pt-1">
                      {d.reasons_bad.map((reason, i) => (
                        <div key={i} className="flex items-start gap-1 text-xs text-red-600">
                          <AlertCircle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                          <span>{reason}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {travelResults && travelResults.total_favorable === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Navigation className="w-8 h-8 mx-auto mb-2 opacity-40" />
                  <p className="text-sm">
                    {language === 'hi'
                      ? 'इस माह इस दिशा में कोई शुभ यात्रा तिथि नहीं है। अगला माह देखें।'
                      : 'No auspicious travel dates for this direction this month. Try next month.'}
                  </p>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Shared date card for Activity results                              */
/* ------------------------------------------------------------------ */
function MuhuratDateCard({
  d,
  language,
  activityKey,
}: {
  d: MuhuratDate;
  language: string;
  activityKey?: string;
}) {
  return (
    <div className="border border-sacred-gold/20 bg-[#FFF9F5] rounded-lg p-3 space-y-2">
      <div className="flex items-start justify-between gap-2">
        <div>
          <div className="font-semibold text-foreground">
            {(() => {
              try {
                const dt = new Date(d.date + 'T12:00:00');
                return dt.toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-IN', {
                  weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
                });
              } catch { return d.date; }
            })()}
          </div>
          <div className="text-xs text-muted-foreground">
            {language === 'hi' ? d.weekday_hindi : d.weekday}
          </div>
        </div>
        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
          d.score >= 75 ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
        }`}>
          {d.score}/100
        </span>
      </div>

      <div className="flex flex-wrap gap-1.5 text-xs">
        <span className="bg-orange-50 text-orange-700 px-2 py-0.5 rounded">{d.tithi}</span>
        <span className="bg-purple-50 text-purple-700 px-2 py-0.5 rounded">{d.nakshatra}</span>
        <span className="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded">{d.paksha}</span>
      </div>

      <div className="grid grid-cols-3 gap-2 text-xs text-muted-foreground">
        <div>
          <span className="font-medium text-foreground">{language === 'hi' ? 'सूर्योदय' : 'Sunrise'}</span>
          <br />{d.sunrise}
        </div>
        <div>
          <span className="font-medium text-foreground">{language === 'hi' ? 'सूर्यास्त' : 'Sunset'}</span>
          <br />{d.sunset}
        </div>
        <div>
          <span className="font-medium text-foreground flex items-center gap-0.5">
            <AlertTriangle className="w-3 h-3 text-red-500" />
            {language === 'hi' ? 'राहुकाल' : 'Rahu Kaal'}
          </span>
          <br />
          {typeof d.rahu_kaal === 'object' && d.rahu_kaal
            ? `${d.rahu_kaal.start} - ${d.rahu_kaal.end}`
            : String(d.rahu_kaal || '--')}
        </div>
      </div>

      {d.lagna_windows?.length > 0 && (
        <div>
          <div className="text-xs font-medium text-foreground mb-1">
            {language === 'hi' ? 'शुभ लग्न' : 'Favorable Lagna Windows'}
          </div>
          <div className="flex flex-wrap gap-1.5">
            {d.lagna_windows.map((lw, i) => (
              <div
                key={`${lw.lagna}-${i}`}
                className={`px-2 py-1 rounded text-xs border ${
                  lw.ganda_sandhi
                    ? 'bg-red-50 text-red-700 border-red-200 opacity-75'
                    : 'bg-blue-50 text-blue-700 border-blue-100'
                }`}
              >
                <div className="flex items-center gap-1">
                  <span className="font-semibold">{lw.lagna}</span>
                  {lw.ganda_sandhi && (
                    <span
                      className="inline-flex items-center gap-0.5 px-1 py-0.5 rounded text-[9px] font-bold"
                      style={{
                        backgroundColor: lw.ganda_sandhi === 'ganda' ? 'rgba(239,68,68,0.2)' : 'rgba(168,85,247,0.2)',
                        color: lw.ganda_sandhi === 'ganda' ? '#dc2626' : '#a855f7',
                      }}
                    >
                      {language === 'hi'
                        ? (lw.ganda_sandhi === 'ganda' ? '⚠ गंडा' : '⚠ संधि')
                        : `⚠ ${lw.ganda_sandhi === 'ganda' ? 'Ganda' : 'Sandhi'}`}
                    </span>
                  )}
                </div>
                <div>{lw.start} – {lw.end}</div>
                {lw.safe_window && (
                  <div className="mt-0.5 text-green-700 bg-green-50 px-1.5 py-0.5 rounded text-[10px] border border-green-100">
                    {language === 'hi' ? 'सुरक्षित खिड़की' : 'Safe window'}: {lw.safe_window.start} – {lw.safe_window.end}
                  </div>
                )}
                {lw.warnings?.map((w, wi) => (
                  <span key={wi} className="block mt-0.5 text-orange-700 text-[10px]">⚠ {w}</span>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}

      {activityKey === 'marriage' && d.lagnasuddhi && (
        <div className="text-xs mt-2 pt-2 border-t border-pink-200 space-y-1">
          <p className="font-bold text-pink-700">
            {language === 'hi' ? 'सर्वश्रेष्ठ लग्न' : 'Best Lagna'}: {d.lagnasuddhi.lagna} ({language === 'hi' ? 'स्वामी' : 'Lord'}: {d.lagnasuddhi.lord})
          </p>
          <p className="text-muted-foreground">
            {language === 'hi' ? 'गुणवत्ता स्कोर' : 'Quality Score'}:
            <span className={`font-bold ml-1 ${
              d.lagnasuddhi.score >= 75 ? 'text-green-600'
              : d.lagnasuddhi.score >= 60 ? 'text-yellow-600'
              : 'text-red-600'
            }`}>
              {d.lagnasuddhi.score}
            </span>
          </p>
        </div>
      )}

      {activityKey === 'marriage' && d.vivaha_quality !== undefined && (
        <div className="text-xs mt-2">
          <span className={`px-2 py-1 rounded font-bold inline-block ${
            d.vivaha_quality >= 85 ? 'bg-green-100 text-green-700'
            : d.vivaha_quality >= 70 ? 'bg-yellow-100 text-yellow-700'
            : 'bg-red-100 text-red-700'
          }`}>
            {language === 'hi' ? 'विवाह गुणवत्ता' : 'Vivaha Quality'}: {d.vivaha_quality}/100
            {d.vivaha_paryapta === false && (
              <span className="ml-1">⚠️ {language === 'hi' ? 'पर्याप्त से कम' : 'Below Paryapta'}</span>
            )}
          </span>
        </div>
      )}

      {d.muhurat_score !== undefined && (
        <div className="text-xs mt-2">
          <span className="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800">
            {d.quality || 'Saamanya'} — {d.muhurat_score}/100
          </span>
          {d.dosha_cancellations?.length > 0 && (
            <p className="text-xs text-emerald-700 mt-1">✓ {d.dosha_cancellations.join(' • ')}</p>
          )}
        </div>
      )}

      {d.chandra_balam && (
        <div className="text-xs mt-2 p-2 bg-blue-50 rounded text-blue-700 border border-blue-100">
          <p className="font-semibold mb-0.5">
            🌙 {language === 'hi' ? 'चन्द्र बल' : 'Chandra Balam'} ({language === 'hi' ? 'भाव' : 'House'} {d.chandra_balam.house})
          </p>
          <p>{language === 'hi' ? d.chandra_balam.interpretation_hi : d.chandra_balam.interpretation_en}</p>
        </div>
      )}

      {d.tara_balam && (
        <div className="text-xs mt-2 p-2 bg-purple-50 rounded text-purple-700 border border-purple-100">
          <p className="font-semibold mb-0.5">
            ⭐ {language === 'hi' ? 'तारा बल' : 'Tara Balam'} ({d.tara_balam.tara_name})
          </p>
          <p>{language === 'hi' ? d.tara_balam.interpretation_hi : d.tara_balam.interpretation_en}</p>
        </div>
      )}

      {(activityKey === 'business_start' || activityKey === 'shop_opening') &&
       d.recommended_hora_windows?.length > 0 && (
        <div className="text-xs mt-2 p-2 bg-amber-50 border border-amber-200 rounded space-y-1">
          <p className="font-bold text-amber-700">
            🕐 {language === 'hi' ? 'सर्वश्रेष्ठ होरा खिड़कियाँ' : 'Best Hora Windows'}
          </p>
          {d.recommended_hora_windows.map((hw, i) => (
            <p key={i} className="text-amber-700">{hw.start} – {hw.end} ({hw.lord})</p>
          ))}
        </div>
      )}

      {d.reasons_good?.length > 0 && (
        <div className="space-y-0.5">
          {d.reasons_good.map((reason, i) => (
            <div key={i} className="flex items-start gap-1 text-xs text-green-700">
              <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 shrink-0" />
              <span>{language === 'hi' ? (d.reasons_good_hindi?.[i] || reason) : reason}</span>
            </div>
          ))}
        </div>
      )}

      {d.reasons_bad?.length > 0 && (
        <div className="space-y-0.5 mt-1 border-t border-red-100 pt-1">
          {d.reasons_bad.map((reason, i) => (
            <div key={i} className="flex items-start gap-1 text-xs text-red-600">
              <AlertCircle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
              <span>{language === 'hi' ? (d.reasons_bad_hindi?.[i] || reason) : reason}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
