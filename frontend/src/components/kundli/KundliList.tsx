import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sparkles, ChevronRight, Clock, Trash2, AlertTriangle } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

interface KundliListProps {
  savedKundlis: any[];
  onLoadKundli: (kundli: any) => void;
  onNewKundli: () => void;
  onPrashnaKundli: () => void;
  onDeleteKundli?: () => void;
}

export default function KundliList({
  savedKundlis,
  onLoadKundli,
  onNewKundli,
  onPrashnaKundli,
  onDeleteKundli,
}: KundliListProps) {
  const { t } = useTranslation();
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [showDeleteAllConfirm, setShowDeleteAllConfirm] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const handleDelete = async (kundliId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this kundli?')) return;
    
    setDeletingId(kundliId);
    try {
      await api.delete(`/api/kundli/${kundliId}`);
      onDeleteKundli?.();
    } catch (err: any) {
      alert('Failed to delete: ' + (err.message || 'Unknown error'));
    } finally {
      setDeletingId(null);
    }
  };

  const handleDeleteAll = async () => {
    setDeleteLoading(true);
    try {
      await api.delete('/api/kundli/user/all');
      setShowDeleteAllConfirm(false);
      onDeleteKundli?.();
    } catch (err: any) {
      alert('Failed to delete: ' + (err.message || 'Unknown error'));
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-24 px-4">
      <div className="text-center mb-8">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-8 h-8 text-cosmic-bg" />
        </div>
        <h3 className="text-2xl font-display font-bold text-sacred-brown mb-2">My Kundlis</h3>
        <p className="text-sacred-text-secondary">Your saved birth charts</p>
      </div>

      {/* Delete All Confirmation Modal */}
      {showDeleteAllConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-cosmic-surface rounded-xl border border-red-500/30 p-6 max-w-md w-full shadow-xl">
            <div className="flex items-center gap-3 mb-4 text-red-400">
              <AlertTriangle className="w-8 h-8" />
              <h4 className="text-lg font-bold">Delete All Kundlis?</h4>
            </div>
            <p className="text-cosmic-text-secondary mb-6">
              This will permanently delete all {savedKundlis.length} saved kundlis. This action cannot be undone.
            </p>
            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={() => setShowDeleteAllConfirm(false)}
                className="flex-1"
              >
                Cancel
              </Button>
              <Button
                onClick={handleDeleteAll}
                disabled={deleteLoading}
                className="flex-1 bg-red-500 hover:bg-red-600 text-white"
              >
                {deleteLoading ? 'Deleting...' : 'Delete All'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-3 mb-6">
        {savedKundlis.map((k: any) => (
          <div
            key={k.id}
            className="group relative p-4 bg-sacred-cream rounded-xl border border-sacred-gold/20 hover:border-sacred-gold/50 transition-all"
          >
            <button onClick={() => onLoadKundli(k)} className="w-full text-left">
              <div className="flex items-center justify-between pr-10">
                <div>
                  <h4 className="font-display font-semibold text-sacred-brown">{k.person_name}</h4>
                  <p className="text-sm text-sacred-text-secondary">{k.birth_date} | {k.birth_time} | {k.birth_place}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-sacred-gold" />
              </div>
            </button>
            
            {/* Delete Button */}
            <button
              onClick={(e) => handleDelete(k.id, e)}
              disabled={deletingId === k.id}
              className="absolute right-3 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 flex items-center justify-center text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
              title="Delete Kundli"
            >
              {deletingId === k.id ? (
                <div className="w-4 h-4 border-2 border-red-500/30 border-t-red-400 rounded-full animate-spin" />
              ) : (
                <Trash2 className="w-4 h-4" />
              )}
            </button>
          </div>
        ))}

        {savedKundlis.length === 0 && (
          <p className="text-center text-sacred-text-secondary py-8">No saved kundlis yet</p>
        )}
      </div>

      {/* Delete All Button (only if kundlis exist) */}
      {savedKundlis.length > 0 && (
        <button
          onClick={() => setShowDeleteAllConfirm(true)}
          className="w-full mb-4 p-3 rounded-xl border border-red-500/30 text-red-400 hover:bg-red-500/100/10 transition-colors text-sm flex items-center justify-center gap-2"
        >
          <Trash2 className="w-4 h-4" />
          Delete All Kundlis ({savedKundlis.length})
        </button>
      )}

      <Button onClick={onNewKundli} className="w-full btn-sacred">
        <Sparkles className="w-5 h-5 mr-2" />Generate New Kundli
      </Button>
      
      <Button onClick={onPrashnaKundli} variant="outline" className="w-full mt-3 border-sacred-gold/50 text-sacred-brown hover:bg-sacred-gold/10">
        <Clock className="w-5 h-5 mr-2 text-sacred-gold" />{t('kundli.prashnaKundli')}
        <span className="ml-2 text-xs text-sacred-text-secondary">{t('kundli.prashnaSubtitle')}</span>
      </Button>
    </div>
  );
}
