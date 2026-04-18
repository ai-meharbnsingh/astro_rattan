/**
 * AstrologerDashboard — P3.5 Professional client management.
 *
 * A CRM-style dashboard for astrologers. Four top-level areas:
 *
 *   1. Overview hero — metrics cards + chart-type mix + top 5 clients
 *   2. Activity feed — merged stream across all clients (notes + kundlis + consultations)
 *   3. Clients — rich table with search, filter by chart type, per-row actions
 *   4. Consultations — scheduled + active + completed, create/update/cancel
 *
 * Styling inherits the sacred-gold / amber theme used throughout the LK
 * surfaces so the dashboard feels native to this app rather than a
 * generic Bootstrap panel.
 */
import { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '@/lib/i18n';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Heading } from '@/components/ui/heading';
import {
  Users, Calendar as CalIcon, BookOpen, NotebookPen, Activity,
  ChevronRight, Search, Plus, Loader2, Clock, CheckCircle2, XCircle,
  Phone, MapPin, Filter, RefreshCw, Sparkles, TrendingUp, User as UserIcon,
} from 'lucide-react';

// ─────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────

interface OverviewMetrics {
  total_clients: number;
  new_clients_30d: number;
  new_clients_7d: number;
  total_kundlis: number;
  total_notes: number;
  upcoming_consultations: number;
  consultations_by_status: Record<string, number>;
}
interface TopClient {
  id: string;
  name: string;
  phone: string | null;
  kundli_count: number;
  note_count: number;
  last_activity: string | null;
}
interface Overview {
  metrics: OverviewMetrics;
  chart_types: Array<{ chart_type: string; count: number }>;
  top_clients: TopClient[];
}

interface ActivityEvent {
  kind: 'kundli_generated' | 'note_added' | 'consultation' | string;
  timestamp: string | null;
  client_id: string | null;
  client_name: string | null;
  title_en: string;
  title_hi: string;
  detail: string | null;
  ref_id: string;
  ref_type: string;
  status?: string;
  chart_context?: string;
}

interface Consultation {
  id: string;
  client_id: string | null;
  client_name: string | null;
  client_phone: string | null;
  type: string;
  status: string;
  scheduled_at: string | null;
  duration_minutes: number | null;
  notes: string | null;
  created_at: string | null;
}

interface ClientRow {
  id: string;
  name: string;
  phone: string | null;
  birth_date: string | null;
  birth_place: string | null;
  kundli_count: number;
}

// ─────────────────────────────────────────────────────────────
// Style tokens — mirrors sacred-gold system used across LK tabs
// ─────────────────────────────────────────────────────────────

const STATUS_STYLES: Record<string, string> = {
  scheduled: 'bg-sacred-gold/15 text-sacred-gold-dark border-sacred-gold/40',
  confirmed: 'bg-blue-100 text-blue-800 border-blue-300',
  active:    'bg-emerald-100 text-emerald-800 border-emerald-400 animate-pulse',
  completed: 'bg-green-100 text-green-800 border-green-300',
  cancelled: 'bg-gray-100 text-gray-600 border-gray-300',
  no_show:   'bg-red-100 text-red-700 border-red-300',
  pending:   'bg-amber-100 text-amber-800 border-amber-300',
};

const EVENT_ICON: Record<string, any> = {
  kundli_generated: BookOpen,
  note_added: NotebookPen,
  consultation: CalIcon,
};

const EVENT_TINT: Record<string, string> = {
  kundli_generated: 'bg-sacred-gold/15 text-sacred-gold-dark',
  note_added: 'bg-violet-100 text-violet-700',
  consultation: 'bg-blue-100 text-blue-700',
};

// ─────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────

export default function AstrologerDashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [activeTab, setActiveTab] = useState<'overview' | 'clients' | 'activity' | 'consultations' | 'settings' | 'feedback'>('overview');
  const [overview, setOverview] = useState<Overview | null>(null);
  const [activity, setActivity] = useState<ActivityEvent[]>([]);
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [clients, setClients] = useState<ClientRow[]>([]);

  const [loading, setLoading] = useState(false);
  const [clientSearch, setClientSearch] = useState('');
  const [consultationFilter, setConsultationFilter] = useState<string>('');

  // Sprint I modal state — re-declare here (was silently dropped in a prior merge)
  const [showNewClient, setShowNewClient] = useState(false);
  const [quickViewClientId, setQuickViewClientId] = useState<string | null>(null);

  // ── Permission guard ──
  const isAllowed = user?.role === 'astrologer' || user?.role === 'admin';

  // ── Loaders ──
  const loadOverview = useCallback(() => {
    setLoading(true);
    api.get('/api/astrologer/dashboard')
      .then((res: any) => setOverview(res as Overview))
      .catch(() => setOverview(null))
      .finally(() => setLoading(false));
  }, []);

  const loadActivity = useCallback(() => {
    api.get('/api/astrologer/activity-feed?limit=50')
      .then((res: any) => setActivity(Array.isArray(res?.events) ? res.events : []))
      .catch(() => setActivity([]));
  }, []);

  const loadConsultations = useCallback(() => {
    const q = consultationFilter ? `?status=${encodeURIComponent(consultationFilter)}` : '';
    api.get(`/api/astrologer/consultations${q}`)
      .then((res: any) => setConsultations(Array.isArray(res?.consultations) ? res.consultations : []))
      .catch(() => setConsultations([]));
  }, [consultationFilter]);

  const loadClients = useCallback((q = '') => {
    api.get(`/api/clients?search=${encodeURIComponent(q)}`)
      .then((res: any) => setClients(Array.isArray(res) ? res : []))
      .catch(() => setClients([]));
  }, []);

  useEffect(() => {
    if (!isAllowed) return;
    loadOverview();
    loadActivity();
    loadConsultations();
    loadClients();
  }, [isAllowed, loadOverview, loadActivity, loadConsultations, loadClients]);

  useEffect(() => { if (isAllowed) loadConsultations(); }, [consultationFilter, loadConsultations, isAllowed]);

  // Debounced client search
  useEffect(() => {
    if (!isAllowed) return;
    const handle = setTimeout(() => loadClients(clientSearch), 250);
    return () => clearTimeout(handle);
  }, [clientSearch, loadClients, isAllowed]);

  const refreshAll = () => {
    loadOverview(); loadActivity(); loadConsultations(); loadClients(clientSearch);
  };

  // ── Guard rendering ──
  if (!isAllowed) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center pt-28 pb-12 px-4">
        <div className="text-center max-w-md">
          <Sparkles className="w-12 h-12 text-sacred-gold mx-auto mb-3" />
          <h2 className="text-xl font-sans font-semibold text-sacred-gold mb-2">
            {isHi ? 'केवल ज्योतिषियों के लिए' : 'Astrologer access only'}
          </h2>
          <p className="text-sm text-muted-foreground">
            {isHi
              ? 'यह पेशेवर डैशबोर्ड केवल पंजीकृत ज्योतिषियों के लिए उपलब्ध है।'
              : 'This professional dashboard is available only to registered astrologers.'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-12 space-y-6">
      {/* ── Page header ── */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <Heading as={1} variant={2} className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-sacred-gold" />
            {isHi ? 'पेशेवर डैशबोर्ड' : 'Professional Dashboard'}
          </Heading>
          <p className="text-sm text-muted-foreground mt-1">
            {isHi
              ? 'आपके ग्राहक, कुंडलियाँ, परामर्श एवं नोट्स — एक ही स्थान पर।'
              : 'Your clients, kundlis, consultations, and notes — all in one place.'}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            onClick={refreshAll}
            className="border-sacred-gold text-sacred-gold-dark hover:bg-sacred-gold/10"
          >
            <RefreshCw className="w-4 h-4 mr-1.5" />
            {isHi ? 'रीफ्रेश' : 'Refresh'}
          </Button>
          <Button
            onClick={() => setShowNewClient(true)}
            className="bg-sacred-gold-dark text-white hover:bg-sacred-gold"
          >
            <Plus className="w-4 h-4 mr-1.5" />
            {isHi ? 'नया ग्राहक' : 'Add Client'}
          </Button>
        </div>
      </div>

      {/* ── Tab switcher ── */}
      <div className="flex gap-1 border-b border-sacred-gold/20 flex-wrap">
        {([
          { key: 'overview', labelEn: 'Overview', labelHi: 'सारांश', icon: TrendingUp },
          { key: 'clients', labelEn: 'Clients', labelHi: 'ग्राहक', icon: Users },
          { key: 'activity', labelEn: 'Activity', labelHi: 'गतिविधि', icon: Activity },
          { key: 'consultations', labelEn: 'Consultations', labelHi: 'परामर्श', icon: CalIcon },
        ] as const).map((tab) => {
          const isActive = activeTab === tab.key;
          const Icon = tab.icon;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold border-b-2 transition-colors ${
                isActive
                  ? 'border-sacred-gold text-sacred-gold-dark'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              <Icon className="w-4 h-4" />
              {isHi ? tab.labelHi : tab.labelEn}
            </button>
          );
        })}
      </div>

      {loading && !overview && (
        <div className="flex justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
        </div>
      )}

      {/* ── Overview ── */}
      {activeTab === 'overview' && overview && (
        <OverviewPanel
          overview={overview}
          isHi={isHi}
          onOpenClient={(id) => setQuickViewClientId(id)}
          upcomingList={consultations.filter((c) => c.scheduled_at && new Date(c.scheduled_at) >= new Date() && ['scheduled', 'confirmed', 'active'].includes(c.status))}
          clientList={clients}
        />
      )}

      {/* ── Clients ── */}
      {activeTab === 'clients' && (
        <ClientsPanel
          clients={clients}
          search={clientSearch}
          onSearchChange={setClientSearch}
          isHi={isHi}
          onOpenClient={(id) => setQuickViewClientId(id)}
        />
      )}

      {/* ── Activity ── */}
      {activeTab === 'activity' && (
        <ActivityPanel events={activity} isHi={isHi} onOpenClient={(id) => setQuickViewClientId(id)} />
      )}

      {/* ── Consultations ── */}
      {activeTab === 'consultations' && (
        <ConsultationsPanel
          consultations={consultations}
          clients={clients}
          statusFilter={consultationFilter}
          onStatusFilterChange={setConsultationFilter}
          isHi={isHi}
          onReload={loadConsultations}
        />
      )}

      {/* ── Sprint I — Settings (astrologer profile + password + avatar) ── */}
      {activeTab === 'settings' && (
        <AstrologerSettingsPanel isHi={isHi} user={user} />
      )}

      {/* ── Sprint I — Feedback ── */}
      {activeTab === 'feedback' && (
        <FeedbackPanel isHi={isHi} onOpenFeedback={() => navigate('/feedback')} />
      )}

      {/* ── Sprint I — Modals ── */}
      {showNewClient && (
        <NewClientModal
          isHi={isHi}
          onClose={() => setShowNewClient(false)}
          onCreated={(clientId) => {
            setShowNewClient(false);
            refreshAll();
            setQuickViewClientId(clientId);
          }}
        />
      )}
      {quickViewClientId && (
        <ClientQuickViewModal
          clientId={quickViewClientId}
          isHi={isHi}
          onClose={() => setQuickViewClientId(null)}
          onOpenFullProfile={(id) => { setQuickViewClientId(null); navigate(`/client/${id}`); }}
        />
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Feedback panel — thin wrapper that links to existing /feedback
// ─────────────────────────────────────────────────────────────

function FeedbackPanel({ isHi, onOpenFeedback }: { isHi: boolean; onOpenFeedback: () => void }) {
  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-card p-6">
      <div className="flex items-start gap-3 mb-4">
        <MessageCircleIcon className="w-6 h-6 text-sacred-gold shrink-0 mt-0.5" />
        <div>
          <h3 className="text-lg font-semibold text-sacred-gold-dark">
            {isHi ? 'प्रतिक्रिया एवं सुझाव' : 'Feedback & Suggestions'}
          </h3>
          <p className="text-sm text-muted-foreground mt-1">
            {isHi
              ? 'कोई समस्या या सुझाव? हमें बताएं — हम इस प्लेटफ़ॉर्म को निरंतर बेहतर बनाते हैं।'
              : 'Found a bug or have a feature idea? Let us know — this platform evolves with your input.'}
          </p>
        </div>
      </div>
      <div className="flex gap-2">
        <Button onClick={onOpenFeedback} className="bg-sacred-gold-dark text-white hover:bg-sacred-gold">
          <MessageCircleIcon className="w-4 h-4 mr-1.5" />
          {isHi ? 'प्रतिक्रिया भेजें' : 'Send Feedback'}
        </Button>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Overview sub-panel
// ─────────────────────────────────────────────────────────────

function OverviewPanel({ overview, isHi, onOpenClient, upcomingList, clientList }: {
  overview: Overview;
  isHi: boolean;
  onOpenClient: (id: string) => void;
  upcomingList?: Consultation[];
  clientList?: ClientRow[];
}) {
  const m = overview.metrics;
  const consultationsTotal = Object.values(m.consultations_by_status ?? {}).reduce((a, b) => a + (b || 0), 0);
  const kundlisDelta = m.total_kundlis > 0 ? Math.round((m.new_clients_7d / Math.max(m.total_clients, 1)) * 100) : 0;

  // Nexlio-style metric cards with +% deltas
  const cards = [
    {
      label_en: 'Total Clients', label_hi: 'कुल ग्राहक',
      value: m.total_clients,
      delta: m.new_clients_7d > 0 ? `+${m.new_clients_7d}` : null,
      deltaColor: 'emerald',
      icon: Users,
      iconBg: 'bg-sacred-gold/15 text-sacred-gold-dark',
    },
    {
      label_en: 'Consultations', label_hi: 'परामर्श',
      value: consultationsTotal,
      delta: m.upcoming_consultations > 0 ? `${m.upcoming_consultations} ${isHi ? 'आगामी' : 'upcoming'}` : null,
      deltaColor: 'blue',
      icon: CalIcon,
      iconBg: 'bg-blue-100 text-blue-700',
    },
    {
      label_en: 'Upcoming Today', label_hi: 'आज आगामी',
      value: m.upcoming_consultations,
      delta: null,
      deltaColor: 'orange',
      icon: Clock,
      iconBg: 'bg-orange-100 text-orange-700',
    },
    {
      label_en: 'Total Kundlis', label_hi: 'कुल कुंडलियाँ',
      value: m.total_kundlis,
      delta: kundlisDelta > 0 ? `+${kundlisDelta}%` : null,
      deltaColor: 'emerald',
      icon: BookOpen,
      iconBg: 'bg-violet-100 text-violet-700',
    },
  ];

  // Simple activity chart — bucket chart_types as monthly bars (reuse
  // available data without a new endpoint). If we have less than 2
  // buckets, hide the chart gracefully.
  const chartMax = Math.max(1, ...overview.chart_types.map((c) => c.count));

  return (
    <div className="space-y-5">
      {/* Nexlio-style metric cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {cards.map((c) => {
          const Icon = c.icon;
          const deltaTone =
            c.deltaColor === 'emerald' ? 'text-emerald-700 bg-emerald-50' :
            c.deltaColor === 'blue' ? 'text-blue-700 bg-blue-50' :
            c.deltaColor === 'orange' ? 'text-orange-700 bg-orange-50' :
            'text-sacred-gold-dark bg-sacred-gold/10';
          return (
            <div key={c.label_en} className="rounded-xl border border-sacred-gold/20 bg-card p-4 hover:shadow-md hover:border-sacred-gold/50 transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${c.iconBg}`}>
                  <Icon className="w-4 h-4" />
                </div>
                {c.delta && (
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${deltaTone}`}>
                    {c.delta}
                  </span>
                )}
              </div>
              <p className="text-3xl font-bold text-foreground leading-tight">{c.value}</p>
              <p className="text-xs text-muted-foreground mt-0.5">
                {isHi ? c.label_hi : c.label_en}
              </p>
            </div>
          );
        })}
      </div>

      {/* 2-col layout: chart (2/3) + upcoming meetings (1/3) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* LEFT — activity chart (chart-type mix rendered as bars) */}
        <div className="lg:col-span-2 rounded-xl border border-sacred-gold/20 bg-card p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-sacred-gold-dark uppercase tracking-wider flex items-center gap-2">
                <TrendingUp className="w-4 h-4" />
                {isHi ? 'गतिविधि अवलोकन' : 'Activity Overview'}
              </h3>
              <p className="text-[11px] text-muted-foreground mt-0.5">
                {isHi ? 'चार्ट प्रकार के अनुसार कुंडली वितरण' : 'Kundli distribution by chart type'}
              </p>
            </div>
          </div>
          {overview.chart_types.length === 0 ? (
            <div className="py-12 text-center text-sm text-muted-foreground">
              {isHi ? 'अभी तक कोई डेटा नहीं' : 'No data yet — generate your first chart'}
            </div>
          ) : (
            <div className="flex items-end justify-around gap-4 h-48 px-4 pt-2">
              {overview.chart_types.map((c) => {
                const h = Math.max(4, (c.count / chartMax) * 100);
                return (
                  <div key={c.chart_type} className="flex-1 flex flex-col items-center gap-2 group">
                    <div className="relative w-full max-w-[80px] flex-1 flex items-end">
                      <div
                        className="w-full rounded-t-md bg-gradient-to-t from-sacred-gold to-amber-400 hover:from-sacred-gold-dark hover:to-sacred-gold transition-colors"
                        style={{ height: `${h}%` }}
                      />
                      <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-bold text-sacred-gold-dark opacity-0 group-hover:opacity-100 transition-opacity">
                        {c.count}
                      </span>
                    </div>
                    <span className="text-[11px] font-semibold text-foreground uppercase tracking-wide">
                      {c.chart_type}
                    </span>
                    <span className="text-[10px] text-muted-foreground">{c.count}</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* RIGHT — upcoming meetings list */}
        <div className="rounded-xl border border-sacred-gold/20 bg-card p-5">
          <h3 className="text-sm font-bold text-sacred-gold-dark uppercase tracking-wider flex items-center gap-2 mb-3">
            <CalIcon className="w-4 h-4" />
            {isHi ? 'आगामी परामर्श' : 'Upcoming Meetings'}
          </h3>
          {!upcomingList || upcomingList.length === 0 ? (
            <div className="py-8 text-center text-xs text-muted-foreground">
              {isHi ? 'कोई निर्धारित परामर्श नहीं।' : 'No upcoming consultations.'}
            </div>
          ) : (
            <div className="space-y-2">
              {upcomingList.slice(0, 5).map((c) => {
                const when = c.scheduled_at ? new Date(c.scheduled_at) : null;
                const relative = when ? formatRelativeDay(when, isHi) : '';
                return (
                  <button
                    key={c.id}
                    onClick={() => c.client_id && onOpenClient(c.client_id)}
                    className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-sacred-gold/10 transition-colors text-left border border-transparent hover:border-sacred-gold/30"
                  >
                    <div className="w-8 h-8 rounded-full bg-sacred-gold-dark text-white flex items-center justify-center text-xs font-bold shrink-0">
                      {(c.client_name ?? '?').slice(0, 1).toUpperCase()}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-semibold text-foreground truncate">
                        {c.client_name ?? (isHi ? 'अज्ञात' : 'Unknown')}
                      </p>
                      <p className="text-[10px] text-muted-foreground">
                        {when ? when.toLocaleTimeString(isHi ? 'hi-IN' : 'en-IN', { hour: '2-digit', minute: '2-digit' }) : '—'} · {relative} · {c.type}
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Client List table (compact Nexlio "Lead List" style) */}
      <div className="rounded-xl border border-sacred-gold/20 bg-card">
        <div className="p-4 border-b border-sacred-gold/20 flex items-center justify-between">
          <h3 className="text-sm font-bold text-sacred-gold-dark uppercase tracking-wider flex items-center gap-2">
            <Users className="w-4 h-4" />
            {isHi ? 'ग्राहक सूची' : 'Client List'}
          </h3>
          <span className="text-xs text-muted-foreground">
            {(clientList?.length ?? 0)} {isHi ? 'कुल' : 'total'}
          </span>
        </div>
        {!clientList || clientList.length === 0 ? (
          <div className="py-10 text-center text-sm text-muted-foreground">
            {isHi ? 'कोई ग्राहक नहीं — "नया ग्राहक" पर क्लिक करें' : 'No clients yet — click "Add Client" to start'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-sacred-gold/5 border-b border-sacred-gold/20">
                <tr className="text-left text-[10px] uppercase tracking-wider text-muted-foreground">
                  <th className="px-4 py-2 font-semibold">{isHi ? 'नाम' : 'Name'}</th>
                  <th className="px-4 py-2 font-semibold hidden sm:table-cell">{isHi ? 'फ़ोन' : 'Phone'}</th>
                  <th className="px-4 py-2 font-semibold hidden md:table-cell">{isHi ? 'जन्म' : 'Birth'}</th>
                  <th className="px-4 py-2 font-semibold text-right">{isHi ? 'कुंडलियाँ' : 'Charts'}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-sacred-gold/10">
                {clientList.slice(0, 8).map((c) => (
                  <tr
                    key={c.id}
                    onClick={() => onOpenClient(c.id)}
                    className="hover:bg-sacred-gold/5 cursor-pointer transition-colors"
                  >
                    <td className="px-4 py-2.5">
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-full bg-sacred-gold-dark text-white flex items-center justify-center text-xs font-bold">
                          {c.name.slice(0, 1).toUpperCase()}
                        </div>
                        <span className="font-medium text-foreground">{c.name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-2.5 text-xs text-muted-foreground hidden sm:table-cell">{c.phone ?? '—'}</td>
                    <td className="px-4 py-2.5 text-xs text-muted-foreground hidden md:table-cell">{c.birth_date ?? '—'}</td>
                    <td className="px-4 py-2.5 text-right">
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-sacred-gold/15 text-sacred-gold-dark font-semibold text-xs">
                        {c.kundli_count}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {clientList.length > 8 && (
              <div className="p-3 border-t border-sacred-gold/10 text-center">
                <p className="text-xs text-muted-foreground">
                  {isHi
                    ? `${clientList.length - 8} और ग्राहक — "Clients" टैब देखें`
                    : `${clientList.length - 8} more — see "Clients" tab`}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function formatRelativeDay(d: Date, isHi: boolean): string {
  const now = new Date();
  const diffMs = d.getTime() - now.getTime();
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return isHi ? 'आज' : 'Today';
  if (diffDays === 1) return isHi ? 'कल' : 'Tomorrow';
  if (diffDays === -1) return isHi ? 'कल (बीता)' : 'Yesterday';
  if (diffDays < 7 && diffDays > 0) return isHi ? `${diffDays} दिन में` : `in ${diffDays} days`;
  return d.toLocaleDateString(isHi ? 'hi-IN' : 'en-IN', { month: 'short', day: 'numeric' });
}

// ─────────────────────────────────────────────────────────────
// Clients panel
// ─────────────────────────────────────────────────────────────

function ClientsPanel({ clients, search, onSearchChange, isHi, onOpenClient }: {
  clients: ClientRow[]; search: string; onSearchChange: (s: string) => void; isHi: boolean; onOpenClient: (id: string) => void;
}) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder={isHi ? 'नाम या फ़ोन से खोजें…' : 'Search by name or phone…'}
            className="pl-9 border-sacred-gold/30 focus:border-sacred-gold"
          />
        </div>
      </div>
      {clients.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          {isHi ? 'कोई ग्राहक नहीं मिला।' : 'No clients found.'}
        </div>
      ) : (
        <div className="rounded-xl border border-sacred-gold/20 bg-card overflow-hidden">
          <table className="w-full">
            <thead className="bg-sacred-gold/10 border-b border-sacred-gold/20">
              <tr className="text-left text-[11px] uppercase tracking-wider text-sacred-gold-dark">
                <th className="px-4 py-2 font-semibold">{isHi ? 'नाम' : 'Name'}</th>
                <th className="px-4 py-2 font-semibold hidden sm:table-cell">{isHi ? 'फ़ोन' : 'Phone'}</th>
                <th className="px-4 py-2 font-semibold hidden md:table-cell">{isHi ? 'जन्म' : 'Birth'}</th>
                <th className="px-4 py-2 font-semibold hidden lg:table-cell">{isHi ? 'स्थान' : 'Place'}</th>
                <th className="px-4 py-2 font-semibold text-right">{isHi ? 'कुंडलियाँ' : 'Kundlis'}</th>
                <th className="px-4 py-2"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-sacred-gold/10">
              {clients.map((c) => (
                <tr
                  key={c.id}
                  onClick={() => onOpenClient(c.id)}
                  className="hover:bg-sacred-gold/5 cursor-pointer transition-colors"
                >
                  <td className="px-4 py-3 font-semibold text-foreground">{c.name}</td>
                  <td className="px-4 py-3 text-sm text-muted-foreground hidden sm:table-cell">
                    {c.phone ?? '—'}
                  </td>
                  <td className="px-4 py-3 text-sm text-muted-foreground hidden md:table-cell">
                    {c.birth_date ?? '—'}
                  </td>
                  <td className="px-4 py-3 text-sm text-muted-foreground hidden lg:table-cell truncate max-w-[180px]">
                    {c.birth_place ?? '—'}
                  </td>
                  <td className="px-4 py-3 text-sm text-right">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-sacred-gold/15 text-sacred-gold-dark font-semibold text-xs">
                      {c.kundli_count}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <ChevronRight className="w-4 h-4 text-sacred-gold inline" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Activity feed panel
// ─────────────────────────────────────────────────────────────

function ActivityPanel({ events, isHi, onOpenClient }: {
  events: ActivityEvent[]; isHi: boolean; onOpenClient: (id: string) => void;
}) {
  if (events.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        {isHi ? 'अभी तक कोई गतिविधि नहीं।' : 'No activity yet.'}
      </div>
    );
  }
  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-card p-5">
      <ol className="relative border-l-2 border-sacred-gold/20 space-y-3 ml-2">
        {events.map((ev) => {
          const Icon = EVENT_ICON[ev.kind] ?? Activity;
          const tint = EVENT_TINT[ev.kind] ?? 'bg-gray-100 text-gray-700';
          const ts = ev.timestamp ? new Date(ev.timestamp) : null;
          return (
            <li key={`${ev.ref_type}-${ev.ref_id}`} className="ml-4">
              <span className={`absolute -left-[13px] w-6 h-6 rounded-full flex items-center justify-center ${tint} border-2 border-background`}>
                <Icon className="w-3 h-3" />
              </span>
              <div className="pb-2">
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <p className="text-sm font-semibold text-foreground">
                    {isHi ? ev.title_hi : ev.title_en}
                    {ev.client_name && (
                      <>
                        <span className="text-muted-foreground font-normal"> · </span>
                        <button
                          onClick={() => ev.client_id && onOpenClient(ev.client_id)}
                          className="text-sacred-gold-dark hover:underline"
                        >
                          {ev.client_name}
                        </button>
                      </>
                    )}
                  </p>
                  {ts && (
                    <span className="text-[11px] text-muted-foreground shrink-0">
                      {ts.toLocaleString(isHi ? 'hi-IN' : 'en-IN', {
                        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
                      })}
                    </span>
                  )}
                </div>
                {ev.detail && (
                  <p className="text-xs text-muted-foreground mt-0.5">{ev.detail}</p>
                )}
                {ev.status && (
                  <span className={`inline-block mt-1 text-[10px] px-1.5 py-0.5 rounded-full border font-semibold uppercase ${STATUS_STYLES[ev.status] ?? 'bg-gray-100 border-gray-300'}`}>
                    {ev.status}
                  </span>
                )}
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Consultations panel (with inline create form)
// ─────────────────────────────────────────────────────────────

function ConsultationsPanel({ consultations, clients, statusFilter, onStatusFilterChange, isHi, onReload }: {
  consultations: Consultation[];
  clients: ClientRow[];
  statusFilter: string;
  onStatusFilterChange: (s: string) => void;
  isHi: boolean;
  onReload: () => void;
}) {
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState<{
    client_id: string; type: string; scheduled_at: string; duration_minutes: number; notes: string;
  }>({ client_id: '', type: 'chat', scheduled_at: '', duration_minutes: 30, notes: '' });
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    if (!form.client_id) return;
    setSaving(true);
    try {
      await api.post('/api/astrologer/consultations', {
        client_id: form.client_id,
        type: form.type,
        scheduled_at: form.scheduled_at || null,
        duration_minutes: form.duration_minutes,
        notes: form.notes || null,
        status: 'scheduled',
      });
      setForm({ client_id: '', type: 'chat', scheduled_at: '', duration_minutes: 30, notes: '' });
      setCreating(false);
      onReload();
    } catch (e) {
      console.error('Failed to create consultation', e);
    }
    setSaving(false);
  };

  const updateStatus = async (id: string, newStatus: string) => {
    try {
      await api.patch(`/api/astrologer/consultations/${id}`, { status: newStatus });
      onReload();
    } catch (e) { console.error(e); }
  };

  const cancel = async (id: string) => {
    if (!confirm(isHi ? 'क्या आप वाकई परामर्श रद्द करना चाहते हैं?' : 'Cancel this consultation?')) return;
    try {
      await api.delete(`/api/astrologer/consultations/${id}`);
      onReload();
    } catch (e) { console.error(e); }
  };

  return (
    <div className="space-y-4">
      {/* Filter + new button */}
      <div className="flex items-center justify-between gap-2 flex-wrap">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            {isHi ? 'स्थिति' : 'Status'}
          </span>
          {(['', 'scheduled', 'confirmed', 'active', 'completed', 'cancelled'] as const).map((s) => (
            <button
              key={s || 'all'}
              onClick={() => onStatusFilterChange(s)}
              className={`text-xs px-2.5 py-1 rounded-full border font-semibold transition-colors ${
                statusFilter === s
                  ? 'bg-sacred-gold-dark text-white border-sacred-gold-dark'
                  : 'bg-white border-sacred-gold/30 text-sacred-gold-dark hover:bg-sacred-gold/10'
              }`}
            >
              {s === '' ? (isHi ? 'सभी' : 'All') : s}
            </button>
          ))}
        </div>
        <Button
          onClick={() => setCreating((v) => !v)}
          className="bg-sacred-gold-dark text-white hover:bg-sacred-gold"
        >
          <Plus className="w-4 h-4 mr-1" />
          {isHi ? 'नया परामर्श' : 'New consultation'}
        </Button>
      </div>

      {/* Inline create form */}
      {creating && (
        <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-4 space-y-3">
          <h4 className="font-semibold text-sacred-gold-dark flex items-center gap-2">
            <Plus className="w-4 h-4" /> {isHi ? 'नया परामर्श बुक करें' : 'Book a new consultation'}
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">{isHi ? 'ग्राहक' : 'Client'}</label>
              <select
                value={form.client_id}
                onChange={(e) => setForm((f) => ({ ...f, client_id: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
              >
                <option value="">{isHi ? 'चुनें…' : 'Select…'}</option>
                {clients.map((c) => <option key={c.id} value={c.id}>{c.name}{c.phone ? ` (${c.phone})` : ''}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">{isHi ? 'प्रकार' : 'Type'}</label>
              <select
                value={form.type}
                onChange={(e) => setForm((f) => ({ ...f, type: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
              >
                <option value="chat">Chat</option>
                <option value="audio">Audio</option>
                <option value="video">Video</option>
                <option value="in_person">In Person</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">{isHi ? 'तिथि/समय' : 'Scheduled at'}</label>
              <Input
                type="datetime-local"
                value={form.scheduled_at}
                onChange={(e) => setForm((f) => ({ ...f, scheduled_at: e.target.value }))}
                className="border-sacred-gold/30"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">{isHi ? 'अवधि (मिनट)' : 'Duration (min)'}</label>
              <Input
                type="number" min={5} max={480} step={5}
                value={form.duration_minutes}
                onChange={(e) => setForm((f) => ({ ...f, duration_minutes: parseInt(e.target.value) || 30 }))}
                className="border-sacred-gold/30"
              />
            </div>
          </div>
          <div>
            <label className="text-xs font-semibold text-muted-foreground uppercase block mb-1">{isHi ? 'नोट्स' : 'Notes'}</label>
            <textarea
              value={form.notes}
              onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
              rows={2}
              className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm resize-none"
              placeholder={isHi ? 'विषय, प्रश्न, एजेंडा…' : 'Agenda, questions, topic…'}
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setCreating(false)} className="border-sacred-gold/30">
              {isHi ? 'रद्द करें' : 'Cancel'}
            </Button>
            <Button disabled={!form.client_id || saving} onClick={submit} className="bg-sacred-gold-dark text-white hover:bg-sacred-gold">
              {saving
                ? <Loader2 className="w-4 h-4 animate-spin" />
                : (isHi ? 'बुक करें' : 'Book')}
            </Button>
          </div>
        </div>
      )}

      {/* List */}
      {consultations.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground rounded-xl border border-dashed border-sacred-gold/30">
          {isHi ? 'कोई परामर्श नहीं।' : 'No consultations.'}
        </div>
      ) : (
        <div className="space-y-2">
          {consultations.map((c) => {
            const when = c.scheduled_at ? new Date(c.scheduled_at) : null;
            return (
              <div key={c.id} className="rounded-xl border border-sacred-gold/20 bg-card p-4">
                <div className="flex items-start justify-between gap-3 flex-wrap">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="font-semibold text-foreground">
                        {c.client_name || (isHi ? 'अज्ञात ग्राहक' : 'Unknown client')}
                      </span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full border font-semibold uppercase ${STATUS_STYLES[c.status] ?? 'bg-gray-100 border-gray-300'}`}>
                        {c.status}
                      </span>
                      <span className="text-xs text-muted-foreground uppercase">{c.type}</span>
                    </div>
                    <div className="text-xs text-muted-foreground flex items-center gap-2 flex-wrap">
                      {when && (
                        <span className="inline-flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {when.toLocaleString(isHi ? 'hi-IN' : 'en-IN', {
                            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
                          })}
                        </span>
                      )}
                      {c.duration_minutes && <span>· {c.duration_minutes} min</span>}
                      {c.client_phone && <span className="inline-flex items-center gap-1"><Phone className="w-3 h-3" />{c.client_phone}</span>}
                    </div>
                    {c.notes && (
                      <p className="text-sm text-foreground/80 mt-2 line-clamp-2">{c.notes}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-1 shrink-0">
                    {c.status === 'scheduled' && (
                      <button
                        onClick={() => updateStatus(c.id, 'confirmed')}
                        className="text-xs px-2 py-1 rounded-lg bg-blue-100 text-blue-800 hover:bg-blue-200 transition-colors"
                      >
                        {isHi ? 'पुष्टि' : 'Confirm'}
                      </button>
                    )}
                    {(c.status === 'scheduled' || c.status === 'confirmed') && (
                      <button
                        onClick={() => updateStatus(c.id, 'active')}
                        className="text-xs px-2 py-1 rounded-lg bg-emerald-100 text-emerald-800 hover:bg-emerald-200 transition-colors"
                      >
                        {isHi ? 'शुरू' : 'Start'}
                      </button>
                    )}
                    {c.status === 'active' && (
                      <button
                        onClick={() => updateStatus(c.id, 'completed')}
                        className="text-xs px-2 py-1 rounded-lg bg-green-100 text-green-800 hover:bg-green-200 transition-colors inline-flex items-center gap-1"
                      >
                        <CheckCircle2 className="w-3 h-3" /> {isHi ? 'पूर्ण' : 'Complete'}
                      </button>
                    )}
                    {c.status !== 'completed' && c.status !== 'cancelled' && (
                      <button
                        onClick={() => cancel(c.id)}
                        className="text-xs px-2 py-1 rounded-lg bg-gray-100 text-gray-600 hover:bg-red-100 hover:text-red-700 transition-colors inline-flex items-center gap-1"
                      >
                        <XCircle className="w-3 h-3" /> {isHi ? 'रद्द' : 'Cancel'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
