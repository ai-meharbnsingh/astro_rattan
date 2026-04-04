import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import {
  Flame, Trophy, Star, BookOpen, Crown, Scroll, Bot, Calendar,
  ShoppingBag, Phone, Sparkles, Hash, Layers, Award, CheckCircle,
  Lock, ChevronDown, ChevronUp, Loader2, Zap, Target
} from 'lucide-react';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface BadgeData {
  id: string;
  name: string;
  description: string;
  icon: string;
  earned: boolean;
  earned_at: string | null;
}

interface KarmaProfileData {
  user_id: string;
  total_points: number;
  current_streak: number;
  longest_streak: number;
  last_activity_date: string | null;
  level: number;
  badges: BadgeData[];
  next_level_points: number | null;
}

interface TransactionData {
  id: string;
  points: number;
  action_type: string;
  description: string | null;
  created_at: string;
}

interface ModuleData {
  id: string;
  title: string;
  description: string | null;
  category: string;
  order_index: number;
  content_json: string | null;
  points_reward: number;
  completed: boolean;
}

interface LeaderboardEntry {
  rank: number;
  user_id: string;
  name: string;
  total_points: number;
  level: number;
  current_streak: number;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const LEVEL_THRESHOLDS = [0, 100, 300, 600, 1000, 2000, 3500, 5000, 7500, 10000];

const ICON_MAP: Record<string, React.ReactNode> = {
  scroll: <Scroll className="w-6 h-6" />,
  bot: <Bot className="w-6 h-6" />,
  calendar: <Calendar className="w-6 h-6" />,
  flame: <Flame className="w-6 h-6" />,
  fire: <Flame className="w-6 h-6" />,
  'book-open': <BookOpen className="w-6 h-6" />,
  'shopping-bag': <ShoppingBag className="w-6 h-6" />,
  phone: <Phone className="w-6 h-6" />,
  sparkles: <Sparkles className="w-6 h-6" />,
  hash: <Hash className="w-6 h-6" />,
  layers: <Layers className="w-6 h-6" />,
  crown: <Crown className="w-6 h-6" />,
};

const ACTION_LABELS: Record<string, string> = {
  daily_login: 'Daily Check-in',
  kundli_generated: 'Kundli Generated',
  ai_chat: 'AI Chat',
  panchang_viewed: 'Panchang Viewed',
  shop_purchase: 'Shop Purchase',
  consultation_completed: 'Consultation',
  library_read: 'Library Read',
  prashnavali_used: 'Prashnavali',
  learning_completed: 'Learning Module',
};

const CATEGORY_LABELS: Record<string, string> = {
  basics: 'Basics',
  kundli: 'Kundli',
  panchang: 'Panchang',
  doshas: 'Doshas',
  remedies: 'Remedies',
  advanced: 'Advanced',
};

// ---------------------------------------------------------------------------
// Tabs
// ---------------------------------------------------------------------------

type TabKey = 'journey' | 'badges' | 'learning' | 'leaderboard';

const TABS: { key: TabKey; label: string; icon: React.ReactNode }[] = [
  { key: 'journey', label: 'My Journey', icon: <Zap className="w-4 h-4" /> },
  { key: 'badges', label: 'Badges', icon: <Award className="w-4 h-4" /> },
  { key: 'learning', label: 'Learning', icon: <BookOpen className="w-4 h-4" /> },
  { key: 'leaderboard', label: 'Leaderboard', icon: <Trophy className="w-4 h-4" /> },
];

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function GamificationPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [activeTab, setActiveTab] = useState<TabKey>('journey');
  const [loading, setLoading] = useState(true);
  const [checkinLoading, setCheckinLoading] = useState(false);

  // Data
  const [profile, setProfile] = useState<KarmaProfileData | null>(null);
  const [transactions, setTransactions] = useState<TransactionData[]>([]);
  const [badges, setBadges] = useState<BadgeData[]>([]);
  const [modules, setModules] = useState<ModuleData[]>([]);
  const [modulesCompleted, setModulesCompleted] = useState(0);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [expandedModule, setExpandedModule] = useState<string | null>(null);
  const [completingModule, setCompletingModule] = useState<string | null>(null);

  // Load data
  useEffect(() => {
    if (!isAuthenticated) { setLoading(false); return; }
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      const [profileRes, txRes, badgesRes, modulesRes, lbRes] = await Promise.allSettled([
        api.get('/api/karma/profile'),
        api.get('/api/karma/transactions'),
        api.get('/api/badges'),
        api.get('/api/learning/modules'),
        api.get('/api/karma/leaderboard'),
      ]);
      if (cancelled) return;
      if (profileRes.status === 'fulfilled') setProfile(profileRes.value);
      if (txRes.status === 'fulfilled') setTransactions(txRes.value?.transactions || []);
      if (badgesRes.status === 'fulfilled') setBadges(badgesRes.value?.badges || []);
      if (modulesRes.status === 'fulfilled') {
        setModules(modulesRes.value?.modules || []);
        setModulesCompleted(modulesRes.value?.total_completed || 0);
      }
      if (lbRes.status === 'fulfilled') setLeaderboard(lbRes.value?.leaderboard || []);
      setLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  const handleCheckin = async () => {
    setCheckinLoading(true);
    try {
      const res = await api.post('/api/karma/checkin', {});
      // Refresh profile
      const updated = await api.get('/api/karma/profile');
      setProfile(updated);
      const txRes = await api.get('/api/karma/transactions');
      setTransactions(txRes?.transactions || []);
    } catch {
      // ignore
    }
    setCheckinLoading(false);
  };

  const handleCompleteModule = async (moduleId: string) => {
    setCompletingModule(moduleId);
    try {
      await api.post(`/api/learning/complete/${moduleId}`, {});
      // Refresh
      const [modulesRes, profileRes] = await Promise.all([
        api.get('/api/learning/modules'),
        api.get('/api/karma/profile'),
      ]);
      setModules(modulesRes?.modules || []);
      setModulesCompleted(modulesRes?.total_completed || 0);
      setProfile(profileRes);
    } catch {
      // ignore
    }
    setCompletingModule(null);
  };

  // Auth gate
  if (authLoading) {
    return (
      <div className="min-h-screen bg-cosmic-bg bg-mandala flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-cosmic-bg bg-mandala flex items-center justify-center px-4">
        <div className="card-sacred p-8 text-center max-w-md">
          <Star className="w-12 h-12 text-sacred-gold mx-auto mb-4" />
          <h2 className="text-2xl font-sacred text-sacred-gold mb-2">Astro Journey</h2>
          <p className="text-cosmic-text/70 mb-6">
            Sign in to start earning karma points, unlock badges, and track your spiritual learning path.
          </p>
          <a href="/login" className="btn-sacred px-6 py-3 inline-block">Sign In</a>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-cosmic-bg bg-mandala flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  const currentLevel = profile?.level ?? 1;
  const currentPoints = profile?.total_points ?? 0;
  const prevThreshold = LEVEL_THRESHOLDS[currentLevel - 1] ?? 0;
  const nextThreshold = profile?.next_level_points ?? LEVEL_THRESHOLDS[9];
  const progressPct = nextThreshold > prevThreshold
    ? Math.min(((currentPoints - prevThreshold) / (nextThreshold - prevThreshold)) * 100, 100)
    : 100;

  return (
    <section className="min-h-screen bg-cosmic-bg bg-mandala pt-24 pb-16 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-sacred text-sacred-gold mb-2">Astro Journey</h1>
          <p className="text-cosmic-text/60">Earn karma, unlock badges, and master Vedic astrology</p>
        </div>

        {/* Tab Bar */}
        <div className="flex justify-center gap-2 mb-8 flex-wrap">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-full font-sacred text-sm transition-all
                ${activeTab === tab.key
                  ? 'bg-sacred-gold text-cosmic-bg shadow-lg shadow-sacred-gold/30'
                  : 'border border-sacred-gold/20 text-cosmic-text/70 hover:border-sacred-gold/50 hover:text-sacred-gold'
                }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>

        {/* ============================================================ */}
        {/* MY JOURNEY TAB */}
        {/* ============================================================ */}
        {activeTab === 'journey' && (
          <div className="space-y-6">
            {/* Stats Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Karma Points */}
              <div className="card-sacred p-6 text-center border border-sacred-gold/20">
                <Star className="w-8 h-8 text-sacred-gold mx-auto mb-2" />
                <p className="text-3xl font-sacred text-sacred-gold">{currentPoints.toLocaleString()}</p>
                <p className="text-cosmic-text/60 text-sm">Karma Points</p>
              </div>

              {/* Streak */}
              <div className="card-sacred p-6 text-center border border-sacred-gold/20">
                <Flame className="w-8 h-8 text-orange-400 mx-auto mb-2" />
                <p className="text-3xl font-sacred text-orange-400">{profile?.current_streak ?? 0}</p>
                <p className="text-cosmic-text/60 text-sm">
                  Day Streak {profile?.longest_streak ? `(Best: ${profile.longest_streak})` : ''}
                </p>
              </div>

              {/* Daily Check-in */}
              <div className="card-sacred p-6 text-center border border-sacred-gold/20">
                <Target className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
                <button
                  onClick={handleCheckin}
                  disabled={checkinLoading}
                  className="btn-sacred px-6 py-2 text-sm mt-1 disabled:opacity-50"
                >
                  {checkinLoading ? (
                    <Loader2 className="w-4 h-4 animate-spin inline mr-2" />
                  ) : null}
                  Daily Check-in (+10 pts)
                </button>
              </div>
            </div>

            {/* Level Progress */}
            <div className="card-sacred p-6 border border-sacred-gold/20">
              <div className="flex items-center justify-between mb-3">
                <span className="font-sacred text-sacred-gold text-lg">Level {currentLevel}</span>
                <span className="text-cosmic-text/60 text-sm">
                  {currentLevel < 10
                    ? `${currentPoints.toLocaleString()} / ${nextThreshold.toLocaleString()} pts`
                    : 'MAX LEVEL'}
                </span>
              </div>
              <div className="w-full bg-cosmic-bg rounded-full h-3 overflow-hidden border border-sacred-gold/10">
                <div
                  className="h-full bg-gradient-to-r from-sacred-gold/80 to-sacred-gold rounded-full transition-all duration-700"
                  style={{ width: `${progressPct}%` }}
                />
              </div>
              {currentLevel < 10 && (
                <p className="text-cosmic-text/50 text-xs mt-2">
                  {(nextThreshold - currentPoints).toLocaleString()} points to Level {currentLevel + 1}
                </p>
              )}
            </div>

            {/* Recent Transactions */}
            <div className="card-sacred p-6 border border-sacred-gold/20">
              <h3 className="font-sacred text-sacred-gold text-lg mb-4">Recent Activity</h3>
              {transactions.length === 0 ? (
                <p className="text-cosmic-text/50 text-sm">No activity yet. Start exploring to earn points!</p>
              ) : (
                <div className="space-y-3 max-h-80 overflow-y-auto">
                  {transactions.slice(0, 15).map((tx) => (
                    <div key={tx.id} className="flex items-center justify-between py-2 border-b border-sacred-gold/10 last:border-0">
                      <div>
                        <p className="text-cosmic-text text-sm">{tx.description || ACTION_LABELS[tx.action_type] || tx.action_type}</p>
                        <p className="text-cosmic-text/40 text-xs">{new Date(tx.created_at).toLocaleDateString()}</p>
                      </div>
                      <span className="text-sacred-gold font-sacred text-sm">+{tx.points}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ============================================================ */}
        {/* BADGES TAB */}
        {/* ============================================================ */}
        {activeTab === 'badges' && (
          <div>
            <p className="text-cosmic-text/60 text-center mb-6">
              {badges.filter(b => b.earned).length} of {badges.length} badges earned
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              {badges.map((badge) => (
                <div
                  key={badge.id}
                  className={`card-sacred p-5 text-center border transition-all ${
                    badge.earned
                      ? 'border-sacred-gold/50 shadow-lg shadow-sacred-gold/20'
                      : 'border-sacred-gold/10 opacity-50'
                  }`}
                >
                  <div className={`w-14 h-14 rounded-full mx-auto mb-3 flex items-center justify-center ${
                    badge.earned
                      ? 'bg-sacred-gold/20 text-sacred-gold'
                      : 'bg-cosmic-bg text-cosmic-text/30'
                  }`}>
                    {badge.earned
                      ? (ICON_MAP[badge.icon] || <Star className="w-6 h-6" />)
                      : <Lock className="w-6 h-6" />}
                  </div>
                  <h4 className={`font-sacred text-sm mb-1 ${badge.earned ? 'text-sacred-gold' : 'text-cosmic-text/40'}`}>
                    {badge.name}
                  </h4>
                  <p className="text-cosmic-text/50 text-xs leading-snug">{badge.description}</p>
                  {badge.earned && badge.earned_at && (
                    <p className="text-sacred-gold/60 text-xs mt-2">
                      Earned {new Date(badge.earned_at).toLocaleDateString()}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ============================================================ */}
        {/* LEARNING TAB */}
        {/* ============================================================ */}
        {activeTab === 'learning' && (
          <div>
            <p className="text-cosmic-text/60 text-center mb-6">
              {modulesCompleted} of {modules.length} modules completed
            </p>
            {modules.length === 0 ? (
              <div className="card-sacred p-8 text-center border border-sacred-gold/20">
                <BookOpen className="w-10 h-10 text-sacred-gold/40 mx-auto mb-3" />
                <p className="text-cosmic-text/50">Learning modules coming soon. Check back later!</p>
              </div>
            ) : (
              <div className="space-y-4">
                {modules.map((mod) => {
                  const isExpanded = expandedModule === mod.id;
                  let content: { sections?: { title: string; body: string }[] } | null = null;
                  try {
                    content = mod.content_json ? JSON.parse(mod.content_json) : null;
                  } catch {
                    content = null;
                  }

                  return (
                    <div
                      key={mod.id}
                      className={`card-sacred border transition-all ${
                        mod.completed ? 'border-emerald-500/30' : 'border-sacred-gold/20'
                      }`}
                    >
                      {/* Header */}
                      <button
                        onClick={() => setExpandedModule(isExpanded ? null : mod.id)}
                        className="w-full flex items-center justify-between p-5 text-left"
                      >
                        <div className="flex items-center gap-3 flex-1 min-w-0">
                          {mod.completed ? (
                            <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                          ) : (
                            <BookOpen className="w-5 h-5 text-sacred-gold/60 flex-shrink-0" />
                          )}
                          <div className="min-w-0">
                            <h4 className="font-sacred text-sacred-gold text-sm truncate">{mod.title}</h4>
                            <p className="text-cosmic-text/50 text-xs">
                              {CATEGORY_LABELS[mod.category] || mod.category} &middot; {mod.points_reward} pts
                            </p>
                          </div>
                        </div>
                        {isExpanded ? (
                          <ChevronUp className="w-4 h-4 text-cosmic-text/40 flex-shrink-0" />
                        ) : (
                          <ChevronDown className="w-4 h-4 text-cosmic-text/40 flex-shrink-0" />
                        )}
                      </button>

                      {/* Expanded Content */}
                      {isExpanded && (
                        <div className="px-5 pb-5 border-t border-sacred-gold/10 pt-4">
                          {mod.description && (
                            <p className="text-cosmic-text/70 text-sm mb-4">{mod.description}</p>
                          )}
                          {content?.sections?.map((sec, i) => (
                            <div key={i} className="mb-4">
                              <h5 className="text-sacred-gold font-sacred text-sm mb-1">{sec.title}</h5>
                              <p className="text-cosmic-text/60 text-sm leading-relaxed">{sec.body}</p>
                            </div>
                          ))}
                          {!mod.completed && (
                            <button
                              onClick={() => handleCompleteModule(mod.id)}
                              disabled={completingModule === mod.id}
                              className="btn-sacred px-5 py-2 text-sm mt-2 disabled:opacity-50"
                            >
                              {completingModule === mod.id ? (
                                <Loader2 className="w-4 h-4 animate-spin inline mr-2" />
                              ) : (
                                <CheckCircle className="w-4 h-4 inline mr-2" />
                              )}
                              Complete (+{mod.points_reward} pts)
                            </button>
                          )}
                          {mod.completed && (
                            <span className="text-emerald-400 text-sm flex items-center gap-1">
                              <CheckCircle className="w-4 h-4" /> Completed
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* ============================================================ */}
        {/* LEADERBOARD TAB */}
        {/* ============================================================ */}
        {activeTab === 'leaderboard' && (
          <div>
            {leaderboard.length === 0 ? (
              <div className="card-sacred p-8 text-center border border-sacred-gold/20">
                <Trophy className="w-10 h-10 text-sacred-gold/40 mx-auto mb-3" />
                <p className="text-cosmic-text/50">No leaderboard data yet. Be the first to earn karma!</p>
              </div>
            ) : (
              <div className="card-sacred border border-sacred-gold/20 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-sacred-gold/20">
                        <th className="text-left px-5 py-3 text-sacred-gold/70 font-sacred text-sm">Rank</th>
                        <th className="text-left px-5 py-3 text-sacred-gold/70 font-sacred text-sm">Name</th>
                        <th className="text-right px-5 py-3 text-sacred-gold/70 font-sacred text-sm">Points</th>
                        <th className="text-right px-5 py-3 text-sacred-gold/70 font-sacred text-sm">Level</th>
                        <th className="text-right px-5 py-3 text-sacred-gold/70 font-sacred text-sm hidden sm:table-cell">Streak</th>
                      </tr>
                    </thead>
                    <tbody>
                      {leaderboard.map((entry) => (
                        <tr key={entry.user_id} className="border-b border-sacred-gold/10 last:border-0 hover:bg-sacred-gold/5 transition-colors">
                          <td className="px-5 py-3">
                            <span className={`font-sacred text-lg ${
                              entry.rank === 1 ? 'text-yellow-400' :
                              entry.rank === 2 ? 'text-[#b8b0a4]' :
                              entry.rank === 3 ? 'text-amber-600' :
                              'text-cosmic-text/60'
                            }`}>
                              {entry.rank === 1 ? '1' : entry.rank === 2 ? '2' : entry.rank === 3 ? '3' : `${entry.rank}`}
                              {entry.rank <= 3 && (
                                <Trophy className="w-4 h-4 inline ml-1" />
                              )}
                            </span>
                          </td>
                          <td className="px-5 py-3 text-cosmic-text text-sm">{entry.name}</td>
                          <td className="px-5 py-3 text-right text-sacred-gold font-sacred text-sm">{entry.total_points.toLocaleString()}</td>
                          <td className="px-5 py-3 text-right text-cosmic-text/70 text-sm">Lv.{entry.level}</td>
                          <td className="px-5 py-3 text-right text-orange-400 text-sm hidden sm:table-cell">
                            {entry.current_streak > 0 && (
                              <>
                                <Flame className="w-3 h-3 inline mr-1" />
                                {entry.current_streak}
                              </>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
