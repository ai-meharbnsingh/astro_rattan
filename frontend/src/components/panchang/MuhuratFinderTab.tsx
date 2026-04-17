import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { Loader2, ChevronLeft, ChevronRight, Search, CheckCircle2, AlertTriangle, AlertCircle } from 'lucide-react';

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
  sunrise: string;
  sunset: string;
  rahu_kaal: { start: string; end: string } | string;
  lagna_windows: LagnaWindow[];
}

interface MuhuratResult {
  activity: Activity;
  month: number;
  year: number;
  dates: MuhuratDate[];
  total_favorable: number;
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

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */
export default function MuhuratFinderTab({ language, t, latitude, longitude }: Props) {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loadingActivities, setLoadingActivities] = useState(true);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);

  const now = new Date();
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [year, setYear] = useState(now.getFullYear());

  const [results, setResults] = useState<MuhuratResult | null>(null);
  const [loadingResults, setLoadingResults] = useState(false);
  const [searched, setSearched] = useState(false);

  // Fetch activities on mount
  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoadingActivities(true);
      try {
        const data = await api.get(`/api/muhurat/activities?lang=${language}`);
        if (!cancelled && data?.activities) {
          setActivities(data.activities);
        }
      } catch {
        // silently fail — empty grid
      } finally {
        if (!cancelled) setLoadingActivities(false);
      }
    })();
    return () => { cancelled = true; };
  }, [language]);

  // Month navigation
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

  // Search muhurat
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
      const data = await api.get(`/api/muhurat/finder?${params}`);
      if (data) setResults(data as MuhuratResult);
    } catch {
      // keep results null — shows "no dates" message
    } finally {
      setLoadingResults(false);
    }
  };

  /* ================================================================ */
  /*  Render                                                           */
  /* ================================================================ */
  return (
    <div className="space-y-4">

      {/* ---- Section header ---- */}
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

      {/* ---- Activity grid ---- */}
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

      {/* ---- Month picker + Search button ---- */}
      {selectedActivity && (
        <Card className="border border-sacred-gold/20">
          <CardContent className="p-3 space-y-3">
            {/* Month navigation */}
            <div className="flex items-center justify-between">
              <Button variant="ghost" size="sm" onClick={goToPrevMonth} className="px-2">
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="font-semibold text-foreground">{monthLabel}</span>
              <Button variant="ghost" size="sm" onClick={goToNextMonth} className="px-2">
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>

            {/* Search button */}
            <Button
              onClick={handleSearch}
              disabled={loadingResults}
              className="w-full btn-sacred flex items-center justify-center gap-2"
            >
              {loadingResults
                ? <Loader2 className="w-4 h-4 animate-spin" />
                : <Search className="w-4 h-4" />
              }
              {language === 'hi' ? 'मुहूर्त खोजें' : 'Find Muhurat'}
            </Button>
          </CardContent>
        </Card>
      )}

      {/* ---- Loading spinner ---- */}
      {loadingResults && (
        <div className="flex justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        </div>
      )}

      {/* ---- Results ---- */}
      {!loadingResults && searched && (
        <div className="space-y-3">
          {/* Results header */}
          <div className="text-center">
            <p className="text-sm font-semibold text-foreground">
              {results && results.total_favorable > 0
                ? (language === 'hi'
                    ? `${results.total_favorable} शुभ तिथियाँ — ${results.activity.name_hindi} — ${monthLabel}`
                    : `${results.total_favorable} Auspicious Dates for ${results.activity.name} in ${monthLabel}`)
                : (language === 'hi'
                    ? `इस माह कोई शुभ तिथि नहीं मिली`
                    : `No auspicious dates found this month`)
              }
            </p>
          </div>

          {/* Date cards */}
          {results?.dates?.map((d, idx) => (
            <div
              key={`${d.date}-${idx}`}
              className="border border-sacred-gold/20 bg-[#FFF9F5] rounded-lg p-3 space-y-2"
            >
              {/* Date + Score */}
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="font-semibold text-foreground">
                    {formatDate(d.date, language)}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {language === 'hi' ? d.weekday_hindi : d.weekday}
                  </div>
                </div>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                  d.score >= 75
                    ? 'bg-green-100 text-green-700'
                    : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {d.score}/100
                </span>
              </div>

              {/* Tithi / Nakshatra / Paksha */}
              <div className="flex flex-wrap gap-1.5 text-xs">
                <span className="bg-orange-50 text-orange-700 px-2 py-0.5 rounded">
                  {d.tithi}
                </span>
                <span className="bg-purple-50 text-purple-700 px-2 py-0.5 rounded">
                  {d.nakshatra}
                </span>
                <span className="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded">
                  {d.paksha}
                </span>
              </div>

              {/* Sunrise / Sunset / Rahu Kaal */}
              <div className="grid grid-cols-3 gap-2 text-xs text-muted-foreground">
                <div>
                  <span className="font-medium text-foreground">
                    {language === 'hi' ? 'सूर्योदय' : 'Sunrise'}
                  </span>
                  <br />{d.sunrise}
                </div>
                <div>
                  <span className="font-medium text-foreground">
                    {language === 'hi' ? 'सूर्यास्त' : 'Sunset'}
                  </span>
                  <br />{d.sunset}
                </div>
                <div>
                  <span className="font-medium text-foreground flex items-center gap-0.5">
                    <AlertTriangle className="w-3 h-3 text-red-500" />
                    {language === 'hi' ? 'राहुकाल' : 'Rahu Kaal'}
                  </span>
                  <br />{typeof d.rahu_kaal === 'object' && d.rahu_kaal ? `${d.rahu_kaal.start} - ${d.rahu_kaal.end}` : String(d.rahu_kaal || '--')}
                </div>
              </div>

              {/* Lagna windows */}
              {d.lagna_windows && d.lagna_windows.length > 0 && (
                <div>
                  <div className="text-xs font-medium text-foreground mb-1">
                    {language === 'hi' ? 'शुभ लग्न' : 'Favorable Lagna Windows'}
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {d.lagna_windows.map((lw, i) => (
                      <span key={`${lw.lagna}-${i}`} className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs">
                        {lw.lagna}: {lw.start} – {lw.end}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Reasons good */}
              {d.reasons_good && d.reasons_good.length > 0 && (
                <div className="space-y-0.5">
                  {d.reasons_good.map((reason, i) => (
                    <div key={i} className="flex items-start gap-1 text-xs text-green-700">
                      <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                      <span>{language === 'hi' ? (d.reasons_good_hindi?.[i] || reason) : reason}</span>
                    </div>
                  ))}
                </div>
              )}

              {/* Reasons bad */}
              {d.reasons_bad && d.reasons_bad.length > 0 && (
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
          ))}

          {/* Empty state */}
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
    </div>
  );
}
