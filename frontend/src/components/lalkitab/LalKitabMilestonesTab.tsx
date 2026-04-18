import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { pickLang } from './safe-render';
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

interface SevenYearCycle {
  cycle_start_age: number;
  cycle_end_age: number;
  domain_en: string;
  domain_hi: string;
  ruler: string;
  focus_en: string;
  focus_hi: string;
  years_into: number;
  years_remaining: number;
}

interface SevenYearCycleData {
  active_cycle: SevenYearCycle | null;
  previous_cycle: SevenYearCycle | null;
  next_cycle: SevenYearCycle | null;
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

  const [cycleData, setCycleData] = useState<SevenYearCycleData | null>(null);
  const [cycleLoading, setCycleLoading] = useState(false);
  const [cycleError, setCycleError] = useState(false);

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    setError(false);
    api.get(`/api/lalkitab/milestones/${kundliId}`)
      .then(d => { setData(d); if (d.next_milestone) setExpandedAge(d.next_milestone.age); })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [kundliId]);

  useEffect(() => {
    if (!kundliId) return;
    setCycleLoading(true);
    setCycleError(false);
    api.get(`/api/lalkitab/seven-year-cycle/${kundliId}`)
      .then(d => setCycleData(d))
      .catch(() => setCycleError(true))
      .finally(() => setCycleLoading(false));
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
            {isNaN(Number(next.age)) ? 0 : next.age}
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
                  {pickLang(next.remedy, hi)}
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
                          {pickLang(m.remedy, hi)}
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

      {/* ── 7-Year Life Cycle Section ── */}
      <div className="pt-2">
        <div className="mb-4">
          <h3 className="text-lg font-sans font-bold text-sacred-gold">
            {hi ? 'सात वर्षीय जीवन चक्र' : '7-Year Life Cycle'}
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            {hi
              ? 'लाल किताब के अनुसार जीवन सात-सात वर्षों के चक्रों में बंटा है।'
              : 'According to Lal Kitab, life unfolds in 7-year cycles, each ruled by a different domain.'}
          </p>
        </div>

        {cycleLoading && (
          <div className="flex justify-center py-8">
            <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
          </div>
        )}

        {cycleError && !cycleLoading && (
          <div className="text-center py-6 text-sm text-red-500">
            {hi ? 'चक्र डेटा लोड नहीं हो सका।' : 'Could not load cycle data.'}
          </div>
        )}

        {!cycleLoading && !cycleError && cycleData && (
          <div className="flex flex-col sm:flex-row gap-3 items-stretch">

            {/* Previous cycle — faded */}
            {cycleData.previous_cycle && (
              <div className="flex-1 opacity-50 card-sacred rounded-xl border border-border p-4 bg-muted/30">
                <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-2">
                  {hi ? 'पिछला चक्र' : 'Previous Cycle'}
                </div>
                <div className="text-sm font-semibold text-foreground mb-0.5">
                  {hi ? cycleData.previous_cycle.domain_hi : cycleData.previous_cycle.domain_en}
                </div>
                <div className="text-xs text-muted-foreground mb-2">
                  {hi
                    ? `${isNaN(Number(cycleData.previous_cycle.cycle_start_age)) ? 0 : cycleData.previous_cycle.cycle_start_age}–${isNaN(Number(cycleData.previous_cycle.cycle_end_age)) ? 0 : cycleData.previous_cycle.cycle_end_age} वर्ष`
                    : `Age ${isNaN(Number(cycleData.previous_cycle.cycle_start_age)) ? 0 : cycleData.previous_cycle.cycle_start_age}–${isNaN(Number(cycleData.previous_cycle.cycle_end_age)) ? 0 : cycleData.previous_cycle.cycle_end_age}`}
                </div>
                <div className="flex items-center gap-1.5">
                  <span className={`w-2 h-2 rounded-full shrink-0 ${PLANET_DOT[cycleData.previous_cycle.ruler] || 'bg-gray-400'}`} />
                  <span className="text-xs text-muted-foreground">{cycleData.previous_cycle.ruler}</span>
                </div>
              </div>
            )}

            {/* Active cycle — prominent centre card */}
            {cycleData.active_cycle && (
              <div className="flex-[2] card-sacred rounded-xl border-2 border-sacred-gold bg-gradient-to-b from-sacred-gold/10 to-transparent p-5">
                <div className="flex items-center gap-2 mb-3">
                  <span className="w-2 h-2 rounded-full bg-sacred-gold animate-pulse" />
                  <span className="text-[10px] font-bold text-sacred-gold uppercase tracking-widest">
                    {hi ? 'सक्रिय चक्र' : 'Active Cycle'}
                  </span>
                </div>

                <div className="text-xl font-bold text-foreground mb-0.5">
                  {hi ? cycleData.active_cycle.domain_hi : cycleData.active_cycle.domain_en}
                </div>
                <div className="text-xs text-muted-foreground mb-3">
                  {hi
                    ? `${isNaN(Number(cycleData.active_cycle.cycle_start_age)) ? 0 : cycleData.active_cycle.cycle_start_age}–${isNaN(Number(cycleData.active_cycle.cycle_end_age)) ? 0 : cycleData.active_cycle.cycle_end_age} वर्ष`
                    : `Age ${isNaN(Number(cycleData.active_cycle.cycle_start_age)) ? 0 : cycleData.active_cycle.cycle_start_age}–${isNaN(Number(cycleData.active_cycle.cycle_end_age)) ? 0 : cycleData.active_cycle.cycle_end_age}`}
                </div>

                <div className="flex items-center gap-1.5 mb-3">
                  <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${PLANET_DOT[cycleData.active_cycle.ruler] || 'bg-gray-400'}`} />
                  <span className="text-sm font-semibold text-foreground">{cycleData.active_cycle.ruler}</span>
                </div>

                <p className="text-xs text-foreground/70 leading-relaxed mb-4">
                  {hi ? cycleData.active_cycle.focus_hi : cycleData.active_cycle.focus_en}
                </p>

                {/* Progress bar */}
                <div>
                  <div className="flex justify-between text-xs text-muted-foreground mb-1">
                    <span>
                      {hi
                        ? `${isNaN(Number(cycleData.active_cycle.years_into)) ? 0 : cycleData.active_cycle.years_into} वर्ष बीते`
                        : `${isNaN(Number(cycleData.active_cycle.years_into)) ? 0 : cycleData.active_cycle.years_into} yr in`}
                    </span>
                    <span>
                      {hi
                        ? `${isNaN(Number(cycleData.active_cycle.years_remaining)) ? 0 : cycleData.active_cycle.years_remaining} वर्ष शेष`
                        : `${isNaN(Number(cycleData.active_cycle.years_remaining)) ? 0 : cycleData.active_cycle.years_remaining} yr left`}
                    </span>
                  </div>
                  <div className="w-full h-2.5 bg-sacred-gold/15 rounded-full overflow-hidden border border-sacred-gold/20">
                    <div
                      className="h-full bg-sacred-gold rounded-full transition-all duration-700"
                      style={{
                        width: `${Math.min(100, Math.round(
                          (cycleData.active_cycle.years_into /
                            (cycleData.active_cycle.years_into + cycleData.active_cycle.years_remaining)) * 100
                        ))}%`
                      }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Next cycle — faded */}
            {cycleData.next_cycle && (
              <div className="flex-1 opacity-50 card-sacred rounded-xl border border-border p-4 bg-muted/30">
                <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-2">
                  {hi ? 'अगला चक्र' : 'Next Cycle'}
                </div>
                <div className="text-sm font-semibold text-foreground mb-0.5">
                  {hi ? cycleData.next_cycle.domain_hi : cycleData.next_cycle.domain_en}
                </div>
                <div className="text-xs text-muted-foreground mb-2">
                  {hi
                    ? `${isNaN(Number(cycleData.next_cycle.cycle_start_age)) ? 0 : cycleData.next_cycle.cycle_start_age}–${isNaN(Number(cycleData.next_cycle.cycle_end_age)) ? 0 : cycleData.next_cycle.cycle_end_age} वर्ष`
                    : `Age ${isNaN(Number(cycleData.next_cycle.cycle_start_age)) ? 0 : cycleData.next_cycle.cycle_start_age}–${isNaN(Number(cycleData.next_cycle.cycle_end_age)) ? 0 : cycleData.next_cycle.cycle_end_age}`}
                </div>
                <div className="flex items-center gap-1.5">
                  <span className={`w-2 h-2 rounded-full shrink-0 ${PLANET_DOT[cycleData.next_cycle.ruler] || 'bg-gray-400'}`} />
                  <span className="text-xs text-muted-foreground">{cycleData.next_cycle.ruler}</span>
                </div>
              </div>
            )}

          </div>
        )}
      </div>

    </div>
  );
}
