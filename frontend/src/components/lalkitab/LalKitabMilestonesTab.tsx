import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Loader2, Clock, ChevronDown, ChevronUp, Sparkles, AlertTriangle } from 'lucide-react';

interface Countdown { years: number; months: number; days: number; total_days: number; }
interface Milestone {
  age: number; theme: string; theme_en: string; theme_hi: string; icon: string;
  ruler: string; ruler_house: number; ruler_status: 'strong' | 'moderate' | 'weak';
  description_en: string; description_hi: string;
  prediction_en: string; prediction_hi: string;
  remedy_needed: boolean; remedy?: { en: string; hi: string };
  is_past: boolean; is_current: boolean; is_next: boolean;
  countdown?: Countdown;
}
interface MilestoneData {
  current_age: number; birth_date: string;
  next_milestone: Milestone | null;
  milestones: Milestone[];
}

interface Props { kundliId?: string; language: string; }

const PLANET_DOT: Record<string, string> = {
  Sun:'bg-orange-500', Moon:'bg-blue-300', Mars:'bg-red-500', Mercury:'bg-green-500',
  Jupiter:'bg-yellow-500', Venus:'bg-pink-400', Saturn:'bg-gray-500', Rahu:'bg-purple-600', Ketu:'bg-amber-700',
};

export default function LalKitabMilestonesTab({ kundliId, language }: Props) {
  const [data, setData] = useState<MilestoneData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [expandedAge, setExpandedAge] = useState<number | null>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    setError(false);
    api.get(`/api/lalkitab/milestones/${kundliId}`)
      .then(d => { setData(d); if (d.next_milestone) setExpandedAge(d.next_milestone.age); })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'कुंडली ID आवश्यक है।' : 'Save a Kundli first to see Age Milestones.'}
    </div>
  );

  if (loading) return (
    <div className="flex justify-center py-16">
      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
    </div>
  );

  if (error) return (
    <div className="text-center py-10 text-sm text-red-500">
      {hi ? 'मील का पत्थर लोड नहीं हो सका।' : 'Could not load milestone data. Please try again.'}
    </div>
  );

  if (!data) return null;

  const { next_milestone: next, milestones, current_age } = data;

  const statusColor = (s: string) =>
    s === 'strong' ? 'text-green-600 bg-green-50' :
    s === 'weak'   ? 'text-red-600 bg-red-50' :
                     'text-yellow-600 bg-yellow-50';

  return (
    <div className="space-y-6">
      {/* Hero — Next Milestone */}
      {next && (
        <div className="card-sacred rounded-2xl p-6 text-center bg-gradient-to-b from-sacred-gold/10 to-transparent">
          <div className="text-5xl mb-2">{next.icon}</div>
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
            {hi ? 'अगला जीवन मील का पत्थर' : 'Next Life Milestone'}
          </div>
          <div className="text-6xl font-bold text-sacred-gold mb-1">
            {next.age}
          </div>
          <div className="text-lg font-semibold text-foreground mb-1">
            {hi ? next.theme_hi : next.theme_en}
          </div>

          {next.countdown && next.countdown.total_days > 0 && (
            <div className="flex items-center justify-center gap-2 mt-2 mb-3">
              <span className="flex items-center gap-1 text-sm text-muted-foreground">
                <Clock className="w-3.5 h-3.5" />
                {hi
                  ? `${next.countdown.years}y ${next.countdown.months}m ${next.countdown.days}d में`
                  : `In ${next.countdown.years}y ${next.countdown.months}m ${next.countdown.days}d`}
              </span>
              <span className="w-2 h-2 rounded-full bg-sacred-gold animate-pulse" />
            </div>
          )}
          {next.countdown && next.countdown.total_days === 0 && (
            <div className="text-sm text-sacred-gold font-semibold mb-3">
              {hi ? '🔥 यह मील का पत्थर अभी सक्रिय है!' : '🔥 This milestone is active now!'}
            </div>
          )}

          <div className="bg-sacred-gold/5 rounded-xl p-3 text-sm text-foreground text-left mt-3">
            {hi ? next.prediction_hi : next.prediction_en}
          </div>

          {next.remedy_needed && next.remedy && (
            <div className="mt-3 flex items-start gap-2 bg-amber-50 border border-amber-200 rounded-xl p-3 text-left">
              <Sparkles className="w-4 h-4 text-amber-600 mt-0.5 shrink-0" />
              <div>
                <div className="text-xs font-semibold text-amber-700 mb-0.5">
                  {hi ? 'उपाय अनुशंसित' : 'Remedy Recommended'}
                </div>
                <div className="text-xs text-amber-600">
                  {hi ? next.remedy.hi : next.remedy.en}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Timeline */}
      <div>
        <div className="text-sm font-semibold text-foreground mb-3 px-1">
          {hi ? `आपकी वर्तमान आयु: ${current_age} वर्ष` : `Current Age: ${current_age} years`}
        </div>
        <div className="relative">
          <div className="absolute left-5 top-0 bottom-0 w-0.5 bg-sacred-gold/20" />
          <div className="space-y-2">
            {milestones.map((m) => {
              const expanded = expandedAge === m.age;
              return (
                <div
                  key={m.age}
                  className={`relative pl-12 ${m.is_past ? 'opacity-50' : ''}`}
                >
                  {/* Timeline dot */}
                  <div className={`absolute left-3 top-4 w-4 h-4 rounded-full border-2 flex items-center justify-center
                    ${m.is_next ? 'border-sacred-gold bg-sacred-gold shadow-lg shadow-sacred-gold/30' :
                      m.is_past ? 'border-gray-300 bg-gray-100' :
                      'border-sacred-gold/40 bg-white'}`}>
                    {m.is_past && <div className="w-1.5 h-1.5 rounded-full bg-gray-400" />}
                    {m.is_next && <div className="w-1.5 h-1.5 rounded-full bg-white" />}
                  </div>

                  <button
                    type="button"
                    onClick={() => setExpandedAge(expanded ? null : m.age)}
                    className={`w-full text-left border rounded-xl p-3 transition-all
                      ${m.is_next ? 'border-sacred-gold bg-sacred-gold/5 ring-1 ring-sacred-gold/30' :
                        m.is_past ? 'border-border bg-muted/30' :
                        'border-border bg-card hover:border-sacred-gold/40'}`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-xl">{m.icon}</span>
                        <div>
                          <div className="font-bold text-foreground text-sm">
                            {hi ? `${m.age} वर्ष — ${m.theme_hi}` : `Age ${m.age} — ${m.theme_en}`}
                          </div>
                          <div className="flex items-center gap-1.5 mt-0.5">
                            <span className={`w-2 h-2 rounded-full ${PLANET_DOT[m.ruler] || 'bg-gray-400'}`} />
                            <span className="text-xs text-muted-foreground">{m.ruler} H{m.ruler_house}</span>
                            <span className={`text-xs px-1.5 py-0.5 rounded ${statusColor(m.ruler_status)}`}>
                              {m.ruler_status}
                            </span>
                          </div>
                        </div>
                      </div>
                      {m.is_next && m.countdown && m.countdown.total_days > 0 && (
                        <span className="text-xs text-sacred-gold font-semibold">
                          {m.countdown.years > 0 ? `${m.countdown.years}y` : `${m.countdown.months}m`}
                        </span>
                      )}
                      {expanded ? <ChevronUp className="w-4 h-4 text-muted-foreground" /> : <ChevronDown className="w-4 h-4 text-muted-foreground" />}
                    </div>
                  </button>

                  {expanded && (
                    <div className="ml-1 border border-t-0 border-sacred-gold/20 rounded-b-xl bg-card p-3 space-y-2">
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        {hi ? m.description_hi : m.description_en}
                      </p>
                      <div className="bg-sacred-gold/5 rounded-lg p-2.5 text-xs text-foreground">
                        <div className="font-semibold text-sacred-gold mb-1">
                          {hi ? 'भविष्यवाणी' : 'Prediction'}
                        </div>
                        {hi ? m.prediction_hi : m.prediction_en}
                      </div>
                      {m.remedy_needed && m.remedy && (
                        <div className="flex items-start gap-1.5 bg-amber-50 rounded-lg p-2 text-xs text-amber-700">
                          <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                          {hi ? m.remedy.hi : m.remedy.en}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
