import { useState, useEffect } from 'react';
import {
  Star, MessageSquare, Send, CheckCircle2, Clock,
  ChevronDown, ChevronUp, X,
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from '@/lib/i18n';

// ── Types ─────────────────────────────────────────────────────────────────────
interface FeedbackRecord {
  id: string;
  rating_interface: number | null;
  rating_reports: number | null;
  rating_calculations: number | null;
  feedback_text: string | null;
  status: 'open' | 'closed';
  action_taken: 'yes' | 'no' | 'NR';
  admin_remarks: string | null;
  created_at: string;
}

// ── StarRating (interactive) ──────────────────────────────────────────────────
function StarRating({
  value, onChange, label, sublabel,
}: {
  value: number; onChange: (v: number) => void; label: string; sublabel: string;
}) {
  const { t } = useTranslation();
  const labels = ['', t('feedback.rating.poor'), t('feedback.rating.fair'), t('feedback.rating.good'), t('feedback.rating.great'), t('feedback.rating.excellent')];
  const [hover, setHover] = useState(0);
  const active = hover || value;
  return (
    <div className="flex items-start gap-4">
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-cosmic-text">{label}</p>
        <p className="text-xs text-gray-400 mt-0.5">{sublabel}</p>
      </div>
      <div className="flex items-center gap-1 shrink-0">
        {[1, 2, 3, 4, 5].map(i => (
          <button
            key={i}
            type="button"
            onClick={() => onChange(value === i ? 0 : i)}
            onMouseEnter={() => setHover(i)}
            onMouseLeave={() => setHover(0)}
            className="transition-transform hover:scale-110 focus:outline-none"
          >
            <Star
              className={`w-7 h-7 transition-colors ${
                i <= active
                  ? 'text-sacred-gold-dark fill-current'
                  : 'text-gray-200 hover:text-gray-300'
              }`}
            />
          </button>
        ))}
        <span className="ml-2 w-16 text-xs text-gray-400">
          {active > 0 ? labels[active] : ''}
        </span>
      </div>
    </div>
  );
}

// ── StarDisplay (read-only, compact) ─────────────────────────────────────────
function StarDisplay({ value }: { value: number | null }) {
  const { t } = useTranslation();
  if (!value) return <span className="text-xs text-gray-300">—</span>;
  return (
    <span className="inline-flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map(i => (
        <Star
          key={i}
          className={`w-3 h-3 ${i <= value ? 'text-sacred-gold-dark fill-current' : 'text-gray-200'}`}
        />
      ))}
    </span>
  );
}

// ── Badges ────────────────────────────────────────────────────────────────────
function StatusBadge({ status }: { status: 'open' | 'closed' }) {
  const { t } = useTranslation();
  return status === 'closed' ? (
    <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-green-50 border border-green-200 text-green-700 font-medium">
      <CheckCircle2 className="w-3 h-3" /> {t('feedback.status.resolved')}
    </span>
  ) : (
    <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-700 font-medium">
      <Clock className="w-3 h-3" /> {t('feedback.status.open')}
    </span>
  );
}

function ActionBadge({ action }: { action: 'yes' | 'no' | 'NR' }) {
  const styles = {
    yes: 'bg-green-50 border-green-200 text-green-700',
    no:  'bg-red-50 border-red-200 text-red-600',
    NR:  'bg-gray-50 border-gray-200 text-gray-500',
  };
  const { t } = useTranslation();
  const labels = { yes: t('feedback.action.yes'), no: t('feedback.action.no'), NR: t('feedback.action.nr') };
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${styles[action]}`}>
      {labels[action]}
    </span>
  );
}

// ── FeedbackHistoryCard ───────────────────────────────────────────────────────
function FeedbackHistoryCard({
  item,
  onClosed,
}: {
  item: FeedbackRecord;
  onClosed: (id: string) => void;
}) {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(false);
  const [closing, setClosing] = useState(false);

  const handleClose = async () => {
    setClosing(true);
    try {
      await api.patch(`/api/feedback/${item.id}/close`, {});
      onClosed(item.id);
    } catch (e) { console.error(e); }
    setClosing(false);
  };

  const hasLongText = (item.feedback_text?.length ?? 0) > 130;

  return (
    <div className="border border-sacred-gold/20 rounded-xl p-4 bg-white/60 hover:shadow-sm transition-all">
      {/* Header row */}
      <div className="flex items-center justify-between gap-3 flex-wrap mb-3">
        <div className="flex flex-wrap gap-1.5 items-center">
          <StatusBadge status={item.status} />
          <ActionBadge action={item.action_taken} />
          <span className="text-xs text-gray-400">
            {new Date(item.created_at).toLocaleDateString('en-IN', {
              day: 'numeric', month: 'short', year: 'numeric',
            })}
          </span>
        </div>
        {item.status === 'open' && (
          <button
            onClick={handleClose}
            disabled={closing}
            className="flex items-center gap-1 text-xs px-3 py-1.5 border border-green-300 text-green-700 hover:bg-green-50 rounded-lg transition-colors disabled:opacity-50 font-medium"
          >
            {closing ? (
              <span className="animate-spin inline-block w-3 h-3 border border-green-500 border-t-transparent rounded-full" />
            ) : (
              <CheckCircle2 className="w-3.5 h-3.5" />
            )}
            {closing ? t('feedback.saving') : t('feedback.markResolved')}
          </button>
        )}
      </div>

      {/* Ratings row */}
      <div className="grid grid-cols-3 gap-3 mb-3">
        {[
          { label: t('feedback.interface'), val: item.rating_interface },
          { label: t('feedback.reports'), val: item.rating_reports },
          { label: t('feedback.calculations'), val: item.rating_calculations },
        ].map(r => (
          <div key={r.label}>
            <p className="text-[10px] text-gray-400 uppercase tracking-wider mb-1">{r.label}</p>
            <StarDisplay value={r.val} />
          </div>
        ))}
      </div>

      {/* Feedback text */}
      {item.feedback_text && (
        <div className="mb-3">
          <p className={`text-sm text-gray-600 leading-relaxed ${expanded ? '' : 'line-clamp-2'}`}>
            {item.feedback_text}
          </p>
          {hasLongText && (
            <button
              onClick={() => setExpanded(v => !v)}
              className="mt-1 flex items-center gap-0.5 text-xs text-sacred-gold-dark hover:underline"
            >
              {expanded
                ? <><ChevronUp className="w-3 h-3" /> {t('feedback.showLess')}</>
                : <><ChevronDown className="w-3 h-3" /> {t('feedback.readMore')}</>}
            </button>
          )}
        </div>
      )}

      {/* Admin remarks */}
      {item.admin_remarks && (
        <div className="bg-blue-50 border border-blue-100 rounded-lg px-4 py-3">
          <p className="text-[10px] font-semibold text-blue-500 uppercase tracking-wider mb-1">
            {t('feedback.adminResponse')}
          </p>
          <p className="text-sm text-blue-800">{item.admin_remarks}</p>
        </div>
      )}
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function FeedbackPage() {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const { t } = useTranslation();

  const [ratingInterface, setRatingInterface] = useState(0);
  const [ratingReports, setRatingReports] = useState(0);
  const [ratingCalc, setRatingCalc] = useState(0);
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const [history, setHistory] = useState<FeedbackRecord[]>([]);
  const [histLoading, setHistLoading] = useState(true);

  useEffect(() => {
    if (!loading && !isAuthenticated) navigate('/login');
  }, [loading, isAuthenticated, navigate]);

  useEffect(() => {
    if (isAuthenticated) {
      api.get('/api/feedback/my')
        .then(setHistory)
        .catch(console.error)
        .finally(() => setHistLoading(false));
    }
  }, [isAuthenticated]);

  const handleSubmit = async () => {
    if (!ratingInterface && !ratingReports && !ratingCalc && !text.trim()) {
      setSubmitError(t('feedback.validation.oneRequired'));
      return;
    }
    setSubmitting(true); setSubmitError('');
    try {
      await api.post('/api/feedback', {
        rating_interface:    ratingInterface || null,
        rating_reports:      ratingReports  || null,
        rating_calculations: ratingCalc     || null,
        feedback_text:       text.trim()    || null,
      });
      setRatingInterface(0); setRatingReports(0); setRatingCalc(0); setText('');
      setSubmitted(true);
      setTimeout(() => setSubmitted(false), 5000);
      // refresh history
      api.get('/api/feedback/my').then(setHistory).catch(console.error);
    } catch (e: any) {
      setSubmitError(e.message || t('feedback.submitFailed'));
    }
    setSubmitting(false);
  };

  const handleClosed = (id: string) => {
    setHistory(prev => prev.map(f => f.id === id ? { ...f, status: 'closed' as const } : f));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-sacred-gold" />
      </div>
    );
  }

  const openCount   = history.filter(f => f.status === 'open').length;
  const closedCount = history.filter(f => f.status === 'closed').length;

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 max-w-2xl mx-auto">

      {/* Page header */}
      <div className="flex items-center gap-3 mb-8">
        <MessageSquare className="w-7 h-7 text-sacred-gold-dark" />
        <div>
          <h1 className="text-2xl font-sans font-semibold text-cosmic-text">{t('feedback.title')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">{t('feedback.subtitle')}</p>
        </div>
      </div>

      {/* ── Submit form ──────────────────────────────────────────────── */}
      <div className="border border-sacred-gold/30 rounded-2xl bg-white/60 backdrop-blur-sm p-6 mb-8 shadow-sm">
        <h2 className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wider mb-5">
          {t('feedback.rateYourExperience')}
        </h2>

        <div className="space-y-5 divide-y divide-gray-100">
          <StarRating
            value={ratingInterface}
            onChange={setRatingInterface}
            label={t('feedback.interface')}
            sublabel={t('feedback.interfaceHelp')}
          />
          <div className="pt-5">
            <StarRating
              value={ratingReports}
              onChange={setRatingReports}
              label={t('feedback.reports')}
              sublabel={t('feedback.reportsHelp')}
            />
          </div>
          <div className="pt-5">
            <StarRating
              value={ratingCalc}
              onChange={setRatingCalc}
              label={t('feedback.calculations')}
              sublabel={t('feedback.calculationsHelp')}
            />
          </div>
        </div>

        {/* Text area */}
        <div className="mt-6">
          <label className="block text-sm font-medium text-cosmic-text mb-2">
            {t('feedback.overall')}
            <span className="ml-1 text-xs font-normal text-gray-400">({t('feedback.optional')})</span>
          </label>
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder={t('feedback.placeholder')}
            rows={4}
            maxLength={2000}
            className="w-full px-4 py-3 border border-sacred-gold/30 rounded-xl bg-white text-cosmic-text text-sm focus:outline-none focus:ring-2 focus:ring-sacred-gold/40 resize-none placeholder:text-gray-300"
          />
          <div className="flex items-center justify-between mt-1">
            {submitError
              ? <p className="text-xs text-red-500 flex items-center gap-1"><X className="w-3 h-3" />{submitError}</p>
              : <span />}
            <p className="text-xs text-gray-400">{text.length}/2000</p>
          </div>
        </div>

        {/* Success banner */}
        {submitted && (
          <div className="flex items-center gap-2 mt-4 bg-green-50 border border-green-200 text-green-700 text-sm rounded-xl px-4 py-3">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            {t('feedback.thankYou')}
          </div>
        )}

        <button
          onClick={handleSubmit}
          disabled={submitting}
          className="mt-4 flex items-center gap-2 px-6 py-2.5 bg-sacred-gold-dark text-white rounded-xl hover:opacity-90 transition-all font-medium disabled:opacity-50 text-sm"
        >
          {submitting ? (
            <span className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full inline-block" />
          ) : (
            <Send className="w-4 h-4" />
          )}
          {submitting ? t('feedback.submitting') : t('feedback.submit')}
        </button>
      </div>

      {/* ── History ──────────────────────────────────────────────────── */}
      <div>
        <div className="flex items-center gap-3 mb-4">
          <h2 className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wider">
            {t('feedback.history')}
          </h2>
          {history.length > 0 && (
            <div className="flex gap-1.5 text-[10px]">
              {openCount > 0 && (
                <span className="px-2 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-700">
                  {openCount} {t('feedback.open')}
                </span>
              )}
              {closedCount > 0 && (
                <span className="px-2 py-0.5 rounded-full bg-green-50 border border-green-200 text-green-700">
                  {closedCount} {t('feedback.resolved')}
                </span>
              )}
            </div>
          )}
        </div>

        {histLoading ? (
          <div className="flex justify-center py-10">
            <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-sacred-gold" />
          </div>
        ) : history.length === 0 ? (
          <div className="text-center py-14 border border-dashed border-sacred-gold/30 rounded-2xl">
            <MessageSquare className="w-8 h-8 text-gray-300 mx-auto mb-3" />
            <p className="text-sm text-gray-400">{t('feedback.empty')}</p>
            <p className="text-xs text-gray-300 mt-1">{t('feedback.emptySub')}</p>
          </div>
        ) : (
          <div className="space-y-3">
            {history.map(f => (
              <FeedbackHistoryCard key={f.id} item={f} onClosed={handleClosed} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
