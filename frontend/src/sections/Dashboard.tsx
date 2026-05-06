/**
 * Dashboard — personal home for role == 'user'.
 *
 * After the P3.5 role-split, this surface has ONE job: show a regular
 * user their saved kundlis + profile panel + "New Kundli" CTA. No CRM.
 *
 * Role-aware redirects:
 *   astrologer → /astrologer (richer CRM)
 *   admin      → /admin      (platform management)
 *   user       → stays here
 */
import { useTranslation } from '@/lib/i18n';
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, BookOpen, ChevronRight, User, Star, Calendar, MapPin } from 'lucide-react';
import ProfileEditPanel from '@/components/ProfileEditPanel';
import { Button } from '@/components/ui/button';
import { api, formatDate } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { Heading } from '@/components/ui/heading';

interface KundliSummary {
  id: string;
  person_name: string;
  birth_date: string;
  birth_time: string;
  birth_place: string;
  created_at: string;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const { t } = useTranslation();

  // ── Role-aware redirects ──
  // astrologer → /astrologer; admin → /admin; user → stays here.
  // Admin takes precedence over astrologer when a user happens to hold
  // both flags (super-admin using the astrologer CRM is less common than
  // an admin needing platform tools).
  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return; }
    if (user?.role === 'admin') { navigate('/admin', { replace: true }); return; }
    if (user?.role === 'astrologer') { navigate('/astrologer', { replace: true }); return; }
  }, [isAuthenticated, user?.role, navigate]);

  const [kundlis, setKundlis] = useState<KundliSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const fetchKundlis = useCallback(async () => {
    setLoading(true);
    setFetchError(null);
    try {
      const data = await api.get('/api/kundli');
      setKundlis(Array.isArray(data) ? data : []);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : '';
      setFetchError(msg === 'Not authenticated' ? t('dashboard.sessionExpired') : t('dashboard.loadFailed'));
    }
    setLoading(false);
  }, [t]);

  useEffect(() => {
    // Only fetch if this is a regular user — admins/astrologers will have
    // already been redirected away, so avoid an unnecessary API call.
    if (isAuthenticated && user?.role !== 'admin' && user?.role !== 'astrologer') {
      fetchKundlis();
    }
  }, [isAuthenticated, user?.role, fetchKundlis]);

  // While redirect is in flight, show nothing (prevents a flash of the
  // user view for astrologers/admins).
  if (user?.role === 'admin' || user?.role === 'astrologer') {
    return null;
  }

  return (
    <div className="min-h-[100dvh] pt-28 pb-16 px-4 max-w-5xl mx-auto">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-8">
        <div>
          <Heading as={1} variant={1}>
            {user?.name ? `${t('dashboard.welcome')}, ${user.name}` : t('nav.dashboard')}
          </Heading>
          <p className="text-sm text-muted-foreground mt-1">
            {kundlis.length} {kundlis.length === 1
              ? t('dashboard.chart')
              : t('dashboard.charts')} {t('dashboard.saved')}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            onClick={() => navigate('/kundli')}
            className="bg-sacred-gold-dark text-background hover:bg-sacred-gold text-sm uppercase tracking-wider px-4 py-2 rounded-lg"
          >
            <Plus className="w-4 h-4 mr-1" /> {t('dashboard.newKundli')}
          </Button>
          <Button
            onClick={() => navigate('/lal-kitab')}
            variant="outline"
            className="border-sacred-gold text-sacred-gold-dark text-sm uppercase tracking-wider px-4 py-2 rounded-lg"
          >
            <BookOpen className="w-4 h-4 mr-1" /> {t('nav.lalKitab')}
          </Button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* LEFT — Saved kundlis */}
        <div className="flex-1 min-w-0">
          <Heading as={2} variant={6} className="uppercase tracking-wider mb-4">
            {t('dashboard.myCharts') || 'My Charts'}
          </Heading>

          {loading && (
            <div className="space-y-3">
              {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="flex items-center gap-4 p-4 border border-sacred-gold rounded-lg">
                  <div className="w-10 h-10 animate-pulse bg-sacred-gold/15 rounded" />
                  <div className="flex-1 space-y-2">
                    <div className="h-4 w-32 animate-pulse bg-sacred-gold/15 rounded" />
                    <div className="h-3 w-48 animate-pulse bg-sacred-gold/15 rounded" />
                  </div>
                </div>
              ))}
            </div>
          )}

          {!loading && fetchError && (
            <div className="text-center py-12 rounded-lg border border-red-200 bg-red-50">
              <p className="text-red-700 mb-2">{fetchError}</p>
              <button
                onClick={fetchKundlis}
                className="px-4 py-2 bg-sacred-gold-dark text-white rounded-lg text-sm hover:bg-sacred-gold"
              >
                {t('common.retry')}
              </button>
            </div>
          )}

          {!loading && !fetchError && kundlis.length === 0 && (
            <div className="text-center py-16 border border-dashed border-sacred-gold rounded-lg">
              <Star className="w-12 h-12 text-sacred-gold mx-auto mb-4" />
              <p className="text-foreground mb-2 font-semibold">
                {t('dashboard.noCharts') || 'No saved charts yet'}
              </p>
              <p className="text-sm text-muted-foreground mb-6">
                {t('dashboard.createPrompt') || 'Start by generating your first kundli.'}
              </p>
              <Button
                onClick={() => navigate('/kundli')}
                className="bg-sacred-gold-dark text-background hover:bg-sacred-gold text-sm uppercase tracking-wider rounded-lg"
              >
                <Plus className="w-4 h-4 mr-1" /> {t('dashboard.createFirst') || 'Generate First Kundli'}
              </Button>
            </div>
          )}

          {!loading && !fetchError && kundlis.length > 0 && (
            <div className="space-y-2">
              {kundlis.map((k) => (
                <div
                  key={k.id}
                  onClick={() => navigate('/kundli', { state: { loadKundliId: k.id } })}
                  className="flex items-center justify-between p-4 border border-sacred-gold hover:border-sacred-gold-dark hover:bg-sacred-gold/5 transition-colors bg-background rounded-lg cursor-pointer group"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-sacred-gold-dark border border-sacred-gold rounded-full flex items-center justify-center shrink-0">
                      <User className="w-5 h-5 text-white" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-foreground truncate">{k.person_name}</p>
                      <p className="text-xs text-muted-foreground flex items-center gap-2 flex-wrap">
                        {k.birth_date && (
                          <span className="inline-flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            {formatDate(k.birth_date)} {k.birth_time}
                          </span>
                        )}
                        {k.birth_place && (
                          <span className="inline-flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {k.birth_place}
                          </span>
                        )}
                      </p>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-sacred-gold group-hover:translate-x-0.5 transition-transform shrink-0" />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* RIGHT — Profile edit */}
        <div className="w-full lg:w-80 shrink-0">
          <ProfileEditPanel />
        </div>
      </div>
    </div>
  );
}
