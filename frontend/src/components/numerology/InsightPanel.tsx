import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Sparkles, AlertTriangle, Zap, Briefcase, Grid3X3, Clock, Quote } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';

interface Problem {
  problem: string;
  problem_hi: string;
  source: string;
  action: string;
  action_hi: string;
}

interface Action {
  action: string;
  action_hi: string;
  why: string;
  why_hi: string;
}

interface LoshuIssue {
  missing_number: number;
  issue: string;
  issue_hi: string;
}

interface WeakPlane {
  plane: string;
  issue: string;
  issue_hi: string;
  fix: string;
  fix_hi: string;
}

interface Insights {
  core_profile: {
    traits: string[];
    traits_hi: string[];
    summary: string;
    summary_hi: string;
  };
  top_problems: Problem[];
  top_actions: Action[];
  success_path: {
    best_careers: string[];
    best_careers_hi: string[];
    avoid: string[];
    avoid_hi: string[];
    note: string;
    note_hi: string;
  };
  lo_shu_diagnosis: {
    missing_numbers: LoshuIssue[];
    fixes: string[];
    fixes_hi: string[];
    weak_planes: WeakPlane[];
    has_issues: boolean;
  };
  timeline_now: {
    age?: number;
    age_range?: string;
    age_range_hi?: string;
    pinnacle_number?: number;
    phase_name?: string;
    phase_name_hi?: string;
    personal_year: number;
    personal_year_theme: string;
    personal_year_theme_hi: string;
    combined_advice: string;
    combined_advice_hi: string;
  };
  affirmation: string;
  affirmation_hi: string;
}

interface Props {
  insights: Insights;
}

export default function InsightPanel({ insights }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const p = (en: string, hi: string) => (isHi ? (hi || en) : (en || hi));
  const arr = (en: string[], hi: string[]) => (isHi ? (hi?.length ? hi : en) : (en?.length ? en : hi));

  return (
    <div className="space-y-5 w-full">
      {/* HEADER */}
      <div className="text-center">
        <Heading as={4} variant={4}>
          {isHi ? 'आपका मास्टर प्रोफाइल' : 'Your Master Profile'}
        </Heading>
        <p className="text-xs text-muted-foreground mt-1">
          {isHi ? 'आपके नंबरों से गहन व्यक्तित्व विश्लेषण' : 'Deep personality analysis from your numbers'}
        </p>
      </div>

      {/* CORE PROFILE */}
      <Card className="bg-gradient-to-br from-sacred-gold/10 to-sacred-gold/5 border-sacred-gold/30">
        <CardContent className="p-5">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-5 h-5 text-sacred-gold" />
            <span className="text-sm font-semibold text-foreground">
              {isHi ? 'मुख्य व्यक्तित्व' : 'Core Personality'}
            </span>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed mb-4">
            {p(insights.core_profile.summary, insights.core_profile.summary_hi)}
          </p>
          <div className="flex flex-wrap gap-2">
            {arr(insights.core_profile.traits, insights.core_profile.traits_hi).map((trait, i) => (
              <Badge key={i} className="bg-sacred-gold/20 text-sacred-gold-dark border-sacred-gold/40 text-xs px-3 py-1">
                {trait}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* TOP PROBLEMS */}
      {insights.top_problems.length > 0 && (
        <Card className="bg-card border-red-200/60">
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-3">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              <span className="text-sm font-semibold text-foreground">
                {isHi ? 'आपकी मुख्य चुनौतियां' : 'Your Main Challenges'}
              </span>
            </div>
            <div className="space-y-3">
              {insights.top_problems.map((prob, i) => (
                <div key={i} className="rounded-lg bg-red-50/60 border border-red-100 p-3">
                  <div className="flex items-start gap-2 mb-1">
                    <span className="flex-shrink-0 w-5 h-5 rounded-full bg-red-100 text-red-600 text-xs flex items-center justify-center font-bold mt-0.5">
                      {i + 1}
                    </span>
                    <p className="text-sm font-medium text-red-800">
                      {p(prob.problem, prob.problem_hi)}
                    </p>
                  </div>
                  <p className="text-xs text-muted-foreground ml-7">
                    <span className="text-red-500 font-medium">{prob.source}</span>
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* TOP ACTIONS */}
      {insights.top_actions.length > 0 && (
        <Card className="bg-card border-green-200/60">
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-3">
              <Zap className="w-5 h-5 text-green-600" />
              <span className="text-sm font-semibold text-foreground">
                {isHi ? 'अभी 3 काम करें' : 'Top 3 Actions to Take Now'}
              </span>
            </div>
            <div className="space-y-3">
              {insights.top_actions.map((act, i) => (
                <div key={i} className="rounded-lg bg-green-50/60 border border-green-100 p-3">
                  <div className="flex items-start gap-2">
                    <span className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 text-green-700 text-xs flex items-center justify-center font-bold mt-0.5">
                      {i + 1}
                    </span>
                    <div>
                      <p className="text-sm text-green-900 font-medium leading-snug">
                        {p(act.action, act.action_hi)}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {p(act.why, act.why_hi)}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* SUCCESS PATH */}
      <Card className="bg-card border-0 shadow-soft">
        <CardContent className="p-5">
          <div className="flex items-center gap-2 mb-3">
            <Briefcase className="w-5 h-5 text-sacred-gold" />
            <span className="text-sm font-semibold text-foreground">
              {isHi ? 'सफलता का मार्ग' : 'Your Success Path'}
            </span>
          </div>
          <p className="text-xs text-muted-foreground mb-3">
            {p(insights.success_path.note, insights.success_path.note_hi)}
          </p>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-xs font-semibold text-green-700 mb-2">
                {isHi ? '✅ सर्वश्रेष्ठ करियर' : '✅ Best Careers'}
              </p>
              <ul className="space-y-1">
                {arr(insights.success_path.best_careers, insights.success_path.best_careers_hi).map((c, i) => (
                  <li key={i} className="text-xs text-muted-foreground flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400 shrink-0" />
                    {c}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-xs font-semibold text-red-600 mb-2">
                {isHi ? '❌ इनसे बचें' : '❌ Avoid'}
              </p>
              <ul className="space-y-1">
                {arr(insights.success_path.avoid, insights.success_path.avoid_hi).map((c, i) => (
                  <li key={i} className="text-xs text-muted-foreground flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-400 shrink-0" />
                    {c}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* LO SHU DIAGNOSIS */}
      {insights.lo_shu_diagnosis.has_issues && (
        <Card className="bg-card border-amber-200/60">
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-3">
              <Grid3X3 className="w-5 h-5 text-amber-600" />
              <span className="text-sm font-semibold text-foreground">
                {isHi ? 'लो शू निदान' : 'Lo Shu Diagnosis'}
              </span>
            </div>
            {insights.lo_shu_diagnosis.missing_numbers.length > 0 && (
              <div className="space-y-2 mb-3">
                {insights.lo_shu_diagnosis.missing_numbers.map((mn, i) => (
                  <div key={i} className="flex items-start gap-2 text-xs text-muted-foreground">
                    <Badge className="bg-amber-100 text-amber-800 border-amber-300 shrink-0 text-xs px-1.5">
                      {isHi ? `अनुपस्थित ${mn.missing_number}` : `Missing ${mn.missing_number}`}
                    </Badge>
                    <span>{p(mn.issue, mn.issue_hi)}</span>
                  </div>
                ))}
              </div>
            )}
            {insights.lo_shu_diagnosis.weak_planes.map((wp, i) => (
              <div key={i} className="rounded bg-amber-50/50 border border-amber-100 p-2 text-xs mb-2">
                <span className="font-medium text-amber-800 capitalize">{wp.plane} plane: </span>
                <span className="text-muted-foreground">{p(wp.issue, wp.issue_hi)}</span>
                <div className="mt-1 text-amber-700">{isHi ? '→ ' : '→ '}{p(wp.fix, wp.fix_hi)}</div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* TIMELINE NOW */}
      <Card className="bg-card border-purple-200/60">
        <CardContent className="p-5">
          <div className="flex items-center gap-2 mb-3">
            <Clock className="w-5 h-5 text-purple-600" />
            <span className="text-sm font-semibold text-foreground">
              {isHi ? 'अभी का समय' : 'Your Current Phase'}
            </span>
          </div>
          <div className="flex flex-wrap gap-2 mb-3">
            {insights.timeline_now.age_range && (
              <Badge className="bg-purple-100 text-purple-800 border-purple-200 text-xs">
                {isHi ? (insights.timeline_now.age_range_hi || insights.timeline_now.age_range) : insights.timeline_now.age_range}
              </Badge>
            )}
            {insights.timeline_now.pinnacle_number && (
              <Badge className="bg-sacred-gold/20 text-sacred-gold-dark border-sacred-gold/40 text-xs">
                {isHi ? `शिखर ${insights.timeline_now.pinnacle_number}` : `Pinnacle ${insights.timeline_now.pinnacle_number}`}
                {insights.timeline_now.phase_name && ` — ${p(insights.timeline_now.phase_name, insights.timeline_now.phase_name_hi || '')}`}
              </Badge>
            )}
            <Badge className="bg-blue-100 text-blue-800 border-blue-200 text-xs">
              {isHi ? `व्यक्तिगत वर्ष ${insights.timeline_now.personal_year}` : `Personal Year ${insights.timeline_now.personal_year}`}
              {insights.timeline_now.personal_year_theme && ` — ${p(insights.timeline_now.personal_year_theme, insights.timeline_now.personal_year_theme_hi)}`}
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {p(insights.timeline_now.combined_advice, insights.timeline_now.combined_advice_hi)}
          </p>
        </CardContent>
      </Card>

      {/* AFFIRMATION */}
      <Card className="bg-gradient-to-br from-sacred-gold/15 to-purple-50/30 border-sacred-gold/20">
        <CardContent className="p-5 text-center">
          <Quote className="w-6 h-6 text-sacred-gold mx-auto mb-2 opacity-60" />
          <p className="text-sm italic text-foreground leading-relaxed font-medium">
            {isHi ? (insights.affirmation_hi || insights.affirmation) : insights.affirmation}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
