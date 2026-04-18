import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Bookmark, Heart, Briefcase, Activity, Coins, Trash2, Loader2 } from 'lucide-react';
import { pickLang } from './safe-render';

interface Props {
  kundliId: string;
}

interface SavedPrediction {
  id: string;
  prediction_type: string;
  prediction_data: Record<string, any>;
  note: string;
  created_at: string | null;
}

const TYPE_CONFIG: Record<string, { icon: React.ElementType; labelEn: string; labelHi: string; color: string }> = {
  marriage: { icon: Heart,     labelEn: 'Marriage', labelHi: 'विवाह',   color: 'text-rose-600 bg-rose-500/10 border-rose-300/30' },
  career:   { icon: Briefcase, labelEn: 'Career',   labelHi: 'करियर',  color: 'text-blue-600 bg-blue-500/10 border-blue-300/30' },
  health:   { icon: Activity,  labelEn: 'Health',   labelHi: 'स्वास्थ्य', color: 'text-green-600 bg-green-500/10 border-green-300/30' },
  wealth:   { icon: Coins,     labelEn: 'Wealth',   labelHi: 'धन',     color: 'text-sacred-gold bg-sacred-gold/10 border-sacred-gold/30' },
};

function formatDate(iso: string | null): string {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

/** Render a brief summary of the prediction data based on its type */
function PredictionSummary({ type, data, isHi }: { type: string; data: Record<string, any>; isHi: boolean }) {
  const { t } = useTranslation();
  if (type === 'marriage') {
    return (
      <div className="space-y-1 text-sm text-foreground/80">
        <div>
          {t('auto.manglik')}{' '}
          <span className={data.is_manglik ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}>
            {data.is_manglik ? (t('auto.yes')) : (t('auto.no'))}
          </span>
        </div>
        {data.spouse_description && (
          <div className="line-clamp-2">
            {pickLang(data?.spouse_description, isHi)}
          </div>
        )}
      </div>
    );
  }
  if (type === 'career') {
    const opts = isHi ? data.career_options : data.career_options_en;
    return (
      <div className="text-sm text-foreground/80">
        {Array.isArray(opts) && opts.slice(0, 3).join(', ')}
      </div>
    );
  }
  if (type === 'health') {
    const areas = data.vulnerable_areas;
    return (
      <div className="text-sm text-foreground/80">
        {isHi
          ? (Array.isArray(areas) && areas.length > 0
              ? areas.slice(0, 2).map((a: any) => a.area_hi).join(', ')
              : 'सामान्य स्वास्थ्य')
          : (Array.isArray(areas) && areas.length > 0
              ? areas.slice(0, 2).map((a: any) => a.area_en).join(', ')
              : 'Good overall health')}
      </div>
    );
  }
  if (type === 'wealth') {
    return (
      <div className="text-sm text-foreground/80">
        {isHi
          ? `धन क्षमता: ${data.wealth_potential_hi ?? ''} (${data.wealth_score ?? 0}/100)`
          : `Wealth potential: ${data.wealth_potential_en ?? ''} (${data.wealth_score ?? 0}/100)`}
      </div>
    );
  }
  return null;
}

export default function LalKitabSavedPredictionsTab({ kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [predictions, setPredictions] = useState<SavedPrediction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    if (!kundliId) { setPredictions([]); setError(''); return; }
    setLoading(true);
    setError('');
    api.get(`/api/lalkitab/predictions/saved/${kundliId}`)
      .then((res: any) => setPredictions(Array.isArray(res?.predictions) ? res.predictions : []))
      .catch(() => setError(t('auto.failedToLoadSavedPre')))
      .finally(() => setLoading(false));
  }, [kundliId, isHi]);

  const handleDelete = async (id: string) => {
    setDeletingId(id);
    try {
      await api.delete(`/api/lalkitab/predictions/saved/${id}`);
      setPredictions((prev) => prev.filter((p) => p.id !== id));
    } catch {
      // ignore
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center py-20">
      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Bookmark className="w-5 h-5" />
          {t('lk.saved.title')}
        </h2>
        <p className="text-sm text-gray-500">{t('lk.saved.desc')}</p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
      )}

      {!loading && !error && predictions.length === 0 && (
        <div className="text-center py-16 text-gray-400">
          <Bookmark className="w-10 h-10 mx-auto mb-3 opacity-30" />
          <p className="text-sm">{t('lk.saved.empty')}</p>
        </div>
      )}

      {predictions.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2">
          {predictions.map((pred) => {
            const cfg = TYPE_CONFIG[pred.prediction_type] ?? TYPE_CONFIG.marriage;
            const Icon = cfg.icon;
            return (
              <div key={pred.id} className={`card-sacred rounded-xl border p-5 ${cfg.color}`}>
                {/* Type + date row */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <Icon className="w-4 h-4" />
                    <span className="text-sm font-semibold">
                      {isHi ? cfg.labelHi : cfg.labelEn}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-400">{formatDate(pred.created_at)}</span>
                    <button
                      onClick={() => handleDelete(pred.id)}
                      disabled={deletingId === pred.id}
                      className="p-1 rounded-lg hover:bg-red-500/10 text-gray-400 hover:text-red-600 transition-colors disabled:opacity-50"
                      title={t('lk.saved.delete')}
                    >
                      {deletingId === pred.id
                        ? <Loader2 className="w-4 h-4 animate-spin" />
                        : <Trash2 className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Prediction summary */}
                <PredictionSummary type={pred.prediction_type} data={pred.prediction_data} isHi={isHi} />

                {/* User note */}
                {pred.note && (
                  <div className="mt-3 pt-3 border-t border-current/10">
                    <p className="text-xs text-gray-500 mb-1">{t('lk.saved.note')}</p>
                    <p className="text-sm text-foreground/80 italic">"{pickLang(pred.note, isHi)}"</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
