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
  const { t, language } = useTranslation();
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [showDeleteAllConfirm, setShowDeleteAllConfirm] = useState(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const handleDelete = async (kundliId: string) => {
    setDeletingId(kundliId);
    try {
      await api.delete(`/api/kundli/${kundliId}`);
      setDeleteConfirmId(null);
      onDeleteKundli?.();
    } catch (err: any) {
      alert((language === 'hi' ? 'हटाने में विफल: ' : 'Failed to delete: ') + (err.message || 'Unknown error'));
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
      alert((language === 'hi' ? 'हटाने में विफल: ' : 'Failed to delete: ') + (err.message || 'Unknown error'));
    } finally {
      setDeleteLoading(false);
    }
  };

  // Find the name for single-delete confirmation
  const deleteConfirmKundli = deleteConfirmId ? savedKundlis.find(k => k.id === deleteConfirmId) : null;

  return (
    <div className="max-w-2xl mx-auto py-24 px-4">
      <div className="text-center mb-8">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-8 h-8 text-cosmic-bg" />
        </div>
        <h3 className="text-2xl font-display font-bold text-sacred-brown mb-2">{language === 'hi' ? 'मेरी कुंडलियाँ' : 'My Kundlis'}</h3>
        <p className="text-cosmic-text">{language === 'hi' ? 'आपकी सहेजी गई जन्म कुंडलियाँ' : 'Your saved birth charts'}</p>
      </div>

      {/* Delete All Confirmation Modal */}
      {showDeleteAllConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-cosmic-surface rounded-xl border border-red-300 p-6 max-w-md w-full shadow-xl">
            <div className="flex items-center gap-3 mb-4 text-red-400">
              <AlertTriangle className="w-8 h-8" />
              <h4 className="text-lg font-bold">{language === 'hi' ? 'सभी कुंडलियाँ हटाएं?' : 'Delete All Kundlis?'}</h4>
            </div>
            <p className="text-cosmic-text-secondary mb-6">
              {language === 'hi' ? `यह स्थायी रूप से सभी ${savedKundlis.length} कुंडलियाँ हटा देगा।` : `This will permanently delete all ${savedKundlis.length} saved kundlis. This action cannot be undone.`}
            </p>
            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={() => setShowDeleteAllConfirm(false)}
                className="flex-1"
              >
                {language === 'hi' ? 'रद्द करें' : 'Cancel'}
              </Button>
              <Button
                onClick={handleDeleteAll}
                disabled={deleteLoading}
                className="flex-1 bg-red-500 hover:bg-red-600 text-white"
              >
                {deleteLoading ? (language === 'hi' ? 'हटा रहे हैं...' : 'Deleting...') : (language === 'hi' ? 'सभी हटाएं' : 'Delete All')}
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Single Delete Confirmation Modal */}
      {deleteConfirmId && deleteConfirmKundli && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-cosmic-surface rounded-xl border border-red-300 p-6 max-w-md w-full shadow-xl">
            <div className="flex items-center gap-3 mb-4 text-red-400">
              <AlertTriangle className="w-6 h-6" />
              <h4 className="text-lg font-bold">{language === 'hi' ? 'कुंडली हटाएं?' : 'Delete Kundli?'}</h4>
            </div>
            <p className="text-cosmic-text-secondary mb-6">
              {language === 'hi'
                ? `क्या आप "${deleteConfirmKundli.person_name}" की कुंडली हटाना चाहते हैं? यह क्रिया पूर्ववत नहीं की जा सकती।`
                : `Are you sure you want to delete the kundli for "${deleteConfirmKundli.person_name}"? This action cannot be undone.`}
            </p>
            <div className="flex gap-3">
              <Button
                variant="outline"
                onClick={() => setDeleteConfirmId(null)}
                className="flex-1"
              >
                {language === 'hi' ? 'रद्द करें' : 'Cancel'}
              </Button>
              <Button
                onClick={() => handleDelete(deleteConfirmId)}
                disabled={deletingId === deleteConfirmId}
                className="flex-1 bg-red-500 hover:bg-red-600 text-white"
              >
                {deletingId === deleteConfirmId
                  ? (language === 'hi' ? 'हटा रहे हैं...' : 'Deleting...')
                  : (language === 'hi' ? 'हटाएं' : 'Delete')}
              </Button>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-3 mb-6">
        {savedKundlis.map((k: any) => (
          <div
            key={k.id}
            className="group relative p-4 bg-sacred-cream rounded-xl border border-sacred-gold hover:border-sacred-gold transition-all"
          >
            <button onClick={() => onLoadKundli(k)} className="w-full text-left">
              <div className="flex items-center justify-between pr-10">
                <div>
                  <h4 className="font-display font-semibold text-sacred-brown">{k.person_name}</h4>
                  <p className="text-sm text-cosmic-text">{k.birth_date} | {k.birth_time} | {k.birth_place}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-sacred-gold" />
              </div>
            </button>

            {/* Delete Button — always visible on mobile, hover on desktop */}
            <button
              onClick={(e) => { e.stopPropagation(); setDeleteConfirmId(k.id); }}
              disabled={deletingId === k.id}
              className="absolute right-3 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-red-500 hover:bg-red-600 border border-red-300 flex items-center justify-center text-white opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity"
              title={language === 'hi' ? 'कुंडली हटाएं' : 'Delete Kundli'}
            >
              {deletingId === k.id ? (
                <div className="w-4 h-4 border-2 border-red-300 border-t-red-400 rounded-full animate-spin" />
              ) : (
                <Trash2 className="w-4 h-4" />
              )}
            </button>
          </div>
        ))}

        {savedKundlis.length === 0 && (
          <p className="text-center text-cosmic-text py-8">{language === 'hi' ? 'अभी तक कोई कुंडली नहीं' : 'No saved kundlis yet'}</p>
        )}
      </div>

      {/* Delete All Button (only if kundlis exist) */}
      {savedKundlis.length > 0 && (
        <button
          onClick={() => setShowDeleteAllConfirm(true)}
          className="w-full mb-4 p-3 rounded-xl border border-red-300 text-red-400 hover:bg-red-500 transition-colors text-sm flex items-center justify-center gap-2"
        >
          <Trash2 className="w-4 h-4" />
          {language === 'hi' ? `सभी कुंडलियाँ हटाएं (${savedKundlis.length})` : `Delete All Kundlis (${savedKundlis.length})`}
        </button>
      )}

      <Button onClick={onNewKundli} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold">
        <Sparkles className="w-5 h-5 mr-2" />{language === 'hi' ? 'नई कुंडली बनाएं' : 'Generate New Kundli'}
      </Button>

      <Button onClick={onPrashnaKundli} variant="outline" className="w-full mt-3 border-sacred-gold text-sacred-brown hover:bg-sacred-gold/10">
        <Clock className="w-5 h-5 mr-2 text-sacred-gold" />{t('kundli.prashnaKundli')}
        <span className="ml-2 text-sm text-cosmic-text">{t('kundli.prashnaSubtitle')}</span>
      </Button>
    </div>
  );
}
