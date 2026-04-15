import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { X, Download, Briefcase, Heart, Activity, User, AlertTriangle, Lock, Star, BookOpen, Hash, Loader2 } from 'lucide-react';
import InteractiveKundli from '@/components/InteractiveKundli';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { useNavigate } from 'react-router-dom';

interface FreeKundliModalProps {
  data: any;
  onClose: () => void;
  language: string;
}

const API_BASE = import.meta.env.VITE_API_URL || '';

export default function FreeKundliModal({ data, onClose, language }: FreeKundliModalProps) {
  const navigate = useNavigate();
  const [downloading, setDownloading] = useState<string | null>(null);
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  // Lock body scroll + escape key to close
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = '';
      window.removeEventListener('keydown', onKey);
    };
  }, [onClose]);

  const handleDownload = async (lang: 'en' | 'hi') => {
    if (!data?.guest_id) return;
    setDownloading(lang);
    try {
      const url = `${API_BASE}/api/kundli/free-preview/${data.guest_id}/pdf?lang=${lang}`;
      window.open(url, '_blank');
    } finally {
      setTimeout(() => setDownloading(null), 1000);
    }
  };

  const handleUnlock = () => {
    onClose();
    navigate('/kundli');
  };

  const identity = data?.identity || {};
  const planets = data?.planets || [];
  const lifeSnapshot = data?.life_snapshot || {};
  const currentDasha = data?.current_dasha || {};
  const problems = data?.problems || [];
  const lalkitabTeaser = data?.lalkitab_teaser || {};
  const panchangTeaser = data?.panchang_teaser || {};
  const numerologyTeaser = data?.numerology_teaser || {};
  const rawChartData = data?.chart_data || { planets: {}, houses: [], ascendant: null };
  const hasChart = rawChartData.ascendant && (Array.isArray(rawChartData.planets) ? rawChartData.planets.length > 0 : Object.keys(rawChartData.planets || {}).length > 0);

  // Convert planets from API dict format to InteractiveKundli's expected array format
  const planetsArray = Array.isArray(rawChartData.planets)
    ? rawChartData.planets
    : Object.entries(rawChartData.planets || {}).map(([name, data]: [string, any]) => ({
        planet: name,
        sign: data.sign || '',
        house: data.house || 0,
        longitude: data.longitude || 0,
        sign_degree: data.sign_degree || 0,
        nakshatra: data.nakshatra || '',
        status: data.status || '',
        is_retrograde: data.is_retrograde || false,
      }));

  const chartData = {
    planets: planetsArray,
    houses: rawChartData.houses || [],
    ascendant: rawChartData.ascendant || { sign: 'Aries', longitude: 0 },
  };

  const lifeCards = [
    { key: 'career', icon: Briefcase, label: l('Career', '\u0915\u0930\u093F\u092F\u0930'), color: 'text-blue-600' },
    { key: 'marriage', icon: Heart, label: l('Marriage', '\u0935\u093F\u0935\u093E\u0939'), color: 'text-pink-600' },
    { key: 'health', icon: Activity, label: l('Health', '\u0938\u094D\u0935\u093E\u0938\u094D\u0925\u094D\u092F'), color: 'text-green-600' },
    { key: 'personality', icon: User, label: l('Personality', '\u0935\u094D\u092F\u0915\u094D\u0924\u093F\u0924\u094D\u0935'), color: 'text-purple-600' },
  ];

  return createPortal(
    <div className="fixed inset-0 z-[9999] flex items-start justify-center px-1" style={{ top: '64px' }} onClick={onClose}>
      {/* Backdrop — covers full screen including behind header */}
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" />

      {/* Modal Card — full viewport width, below header */}
      <div
        className="relative z-10 overflow-y-auto bg-white rounded-xl shadow-2xl" style={{ width: 'calc(100vw - 8px)', maxHeight: 'calc(100vh - 72px)' }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header / Close + Download */}
        <div className="sticky top-0 z-20 bg-white border-b border-sacred-gold/20 px-6 py-4 flex items-center justify-between rounded-t-2xl">
          <div className="flex items-center gap-3">
            <h2 className="text-lg font-bold text-sacred-gold-dark">
              {l('Your Free Kundli Preview', '\u0906\u092A\u0915\u0940 \u092E\u0941\u092B\u094D\u0924 \u0915\u0941\u0902\u0921\u0932\u0940 \u091D\u0932\u0915')}
            </h2>
          </div>
          <div className="flex items-center gap-2">
            {/* Download buttons */}
            <button
              onClick={() => handleDownload('en')}
              disabled={downloading === 'en'}
              className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-sacred-gold/40 text-sacred-gold-dark hover:bg-sacred-gold/10 transition-colors disabled:opacity-50"
            >
              {downloading === 'en' ? <Loader2 className="w-3 h-3 animate-spin" /> : <Download className="w-3 h-3" />}
              English PDF
            </button>
            <button
              onClick={() => handleDownload('hi')}
              disabled={downloading === 'hi'}
              className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-sacred-gold/40 text-sacred-gold-dark hover:bg-sacred-gold/10 transition-colors disabled:opacity-50"
            >
              {downloading === 'hi' ? <Loader2 className="w-3 h-3 animate-spin" /> : <Download className="w-3 h-3" />}
              {'\u0939\u093F\u0902\u0926\u0940'} PDF
            </button>
            {/* Close */}
            <button
              onClick={onClose}
              className="ml-2 p-1.5 rounded-full hover:bg-gray-100 transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>
        </div>

        <div className="px-6 py-5">
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">

            {/* LEFT COLUMN: Charts + Planet Table (60% on desktop) */}
            <div className="lg:col-span-3 space-y-6">

              {/* Section: Three Charts */}
              {hasChart && (
                <section>
                  <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                    <Star className="w-4 h-4" />
                    {l('Kundli Charts', '\u0915\u0941\u0902\u0921\u0932\u0940 \u091A\u093E\u0930\u094D\u091F')}
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    {/* Main Kundli (Lagna Chart) */}
                    <div className="border border-sacred-gold/20 rounded-lg p-2 bg-white/50">
                      <p className="text-xs font-semibold text-sacred-gold-dark text-center mb-1">
                        {l('Lagna Kundli', '\u0932\u0917\u094D\u0928 \u0915\u0941\u0902\u0921\u0932\u0940')}
                      </p>
                      <div className="w-full aspect-square max-w-[260px] mx-auto">
                        <InteractiveKundli chartData={chartData} compact />
                      </div>
                    </div>

                    {/* Moon Chart (Chandra Kundli) */}
                    <div className="border border-sacred-gold/20 rounded-lg p-2 bg-white/50">
                      <p className="text-xs font-semibold text-sacred-gold-dark text-center mb-1">
                        {l('Chandra Kundli', '\u091A\u0902\u0926\u094D\u0930 \u0915\u0941\u0902\u0921\u0932\u0940')}
                      </p>
                      <div className="w-full aspect-square max-w-[260px] mx-auto">
                        <InteractiveKundli
                          chartData={{
                            ...chartData,
                            houses: (() => {
                              const moonData = (chartData.planets || []).find((p: any) => p.planet === 'Moon');
                              const moonHouse = moonData?.house || 1;
                              const offset = moonHouse - 1;
                              return (chartData.houses || []).map((h: any) => ({
                                ...h,
                                number: ((h.number - 1 - offset + 12) % 12) + 1,
                              }));
                            })(),
                          }}
                          compact
                        />
                      </div>
                    </div>

                    {/* Lal Kitab Kundli */}
                    <div className="border border-sacred-gold/20 rounded-lg p-2 bg-white/50">
                      <p className="text-xs font-semibold text-sacred-gold-dark text-center mb-1">
                        {l('Lal Kitab Kundli', '\u0932\u093E\u0932 \u0915\u093F\u0924\u093E\u092C \u0915\u0941\u0902\u0921\u0932\u0940')}
                      </p>
                      <div className="w-full aspect-square max-w-[260px] mx-auto">
                        <InteractiveKundli chartData={chartData} compact />
                      </div>
                      <p className="text-[10px] text-center text-muted-foreground mt-1">
                        {l('Lal Kitab house system', '\u0932\u093E\u0932 \u0915\u093F\u0924\u093E\u092C \u092D\u093E\u0935 \u092A\u0926\u094D\u0927\u0924\u093F')}
                      </p>
                    </div>
                  </div>
                </section>
              )}

              {/* Section: Planet Table */}
              {planets.length > 0 && (
                <section>
                  <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                    <Star className="w-4 h-4" />
                    {l('Planet Positions', '\u0917\u094D\u0930\u0939 \u0938\u094D\u0925\u093F\u0924\u093F')}
                  </h3>
                  <div className="rounded-lg border border-sacred-gold/20 overflow-hidden">
                    <Table>
                      <TableHeader>
                        <TableRow className="bg-sacred-gold/10">
                          <TableHead className="text-sacred-gold-dark text-xs">{l('Planet', '\u0917\u094D\u0930\u0939')}</TableHead>
                          <TableHead className="text-sacred-gold-dark text-xs">{l('Sign', '\u0930\u093E\u0936\u093F')}</TableHead>
                          <TableHead className="text-sacred-gold-dark text-xs">{l('House', '\u092D\u093E\u0935')}</TableHead>
                          <TableHead className="text-sacred-gold-dark text-xs">{l('Degree', '\u0905\u0902\u0936')}</TableHead>
                          <TableHead className="text-sacred-gold-dark text-xs">{l('Nakshatra', '\u0928\u0915\u094D\u0937\u0924\u094D\u0930')}</TableHead>
                          <TableHead className="text-sacred-gold-dark text-xs">{l('Status', '\u0938\u094D\u0925\u093F\u0924\u093F')}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {planets.map((p: any, i: number) => (
                          <TableRow key={i}>
                            <TableCell className="text-sm font-medium">{p.planet}</TableCell>
                            <TableCell className="text-sm">{p.sign}</TableCell>
                            <TableCell className="text-sm">{p.house}</TableCell>
                            <TableCell className="text-sm font-mono">{p.degree_dms || (p.degree != null ? `${Number(p.degree).toFixed(2)}\u00b0` : '\u2014')}</TableCell>
                            <TableCell className="text-sm">{p.nakshatra || '\u2014'}</TableCell>
                            <TableCell className="text-sm">
                              {p.retrograde && <span className="text-red-500 font-bold mr-1">R</span>}
                              {p.status || '\u2014'}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </section>
              )}
            </div>

            {/* RIGHT COLUMN: Identity, Life Snapshot, Dasha, Problems, Teasers (40% on desktop) */}
            <div className="lg:col-span-2 space-y-6">

              {/* Section: Identity Snapshot */}
              <section>
                <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                  <Star className="w-4 h-4" />
                  {l('Identity Snapshot', '\u092A\u0939\u091A\u093E\u0928 \u0938\u093E\u0930\u093E\u0902\u0936')}
                </h3>
                <div className="grid grid-cols-2 gap-2 mb-3">
                  {[
                    { label: l('Lagna', '\u0932\u0917\u094D\u0928'), value: identity.lagna },
                    { label: l('Rashi', '\u0930\u093E\u0936\u093F'), value: identity.rashi },
                    { label: l('Nakshatra', '\u0928\u0915\u094D\u0937\u0924\u094D\u0930'), value: identity.nakshatra },
                    { label: l('Moon Sign', '\u091A\u0902\u0926\u094D\u0930 \u0930\u093E\u0936\u093F'), value: identity.moon_sign },
                  ].map((item, i) => (
                    <div key={i} className="rounded-lg bg-sacred-gold/10 border border-sacred-gold/20 px-3 py-2 text-center">
                      <p className="text-[10px] uppercase tracking-wider text-sacred-gold-dark/60 font-semibold">{item.label}</p>
                      <p className="text-sm font-bold text-sacred-gold-dark mt-0.5">{item.value || '\u2014'}</p>
                    </div>
                  ))}
                </div>
                {identity.summary && (
                  <p className="text-sm text-gray-700 leading-relaxed">{identity.summary}</p>
                )}
              </section>

              {/* Section: Life Snapshot (4 cards) */}
              {Object.keys(lifeSnapshot).length > 0 && (
                <section>
                  <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                    <Star className="w-4 h-4" />
                    {l('Life Snapshot', '\u091C\u0940\u0935\u0928 \u091D\u0932\u0915')}
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    {lifeCards.map(({ key, icon: Icon, label, color }) => {
                      const content = lifeSnapshot[key];
                      if (!content) return null;
                      return (
                        <div key={key} className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 p-3">
                          <div className="flex items-center gap-2 mb-1.5">
                            <Icon className={`w-4 h-4 ${color}`} />
                            <span className="text-sm font-semibold text-gray-800">{label}</span>
                          </div>
                          <p className="text-xs text-gray-600 line-clamp-2 leading-relaxed">{content}</p>
                        </div>
                      );
                    })}
                  </div>
                </section>
              )}

              {/* Section: Current Dasha */}
              {currentDasha.mahadasha && (
                <section>
                  <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                    <Star className="w-4 h-4" />
                    {l('Current Dasha', '\u0935\u0930\u094D\u0924\u092E\u093E\u0928 \u0926\u0936\u093E')}
                  </h3>
                  <div className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 p-4">
                    <div className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-2">
                      <span className="px-2 py-0.5 rounded bg-sacred-gold/20 text-sacred-gold-dark text-xs font-bold">
                        {currentDasha.mahadasha}
                      </span>
                      <span className="text-gray-400">{'\u2192'}</span>
                      <span className="px-2 py-0.5 rounded bg-sacred-gold/15 text-sacred-gold-dark text-xs font-bold">
                        {currentDasha.antardasha || '\u2014'}
                      </span>
                    </div>
                    {currentDasha.summary && (
                      <p className="text-xs text-gray-600 leading-relaxed">{currentDasha.summary}</p>
                    )}
                  </div>
                </section>
              )}

              {/* Section: Problem Highlights */}
              {problems.length > 0 && (
                <section>
                  <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    {l('Problem Highlights', '\u0938\u092E\u0938\u094D\u092F\u093E \u092E\u0941\u0916\u094D\u092F \u0905\u0902\u0936')}
                  </h3>
                  <div className="space-y-2">
                    {problems.slice(0, 3).map((prob: any, i: number) => (
                      <div key={i} className="rounded-lg border border-amber-200 bg-amber-50 p-3 flex items-start gap-2">
                        <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 shrink-0" />
                        <div>
                          <p className="text-sm font-semibold text-amber-800">{prob.title || prob.problem || `Issue ${i + 1}`}</p>
                          {prob.detail && <p className="text-xs text-amber-700 mt-0.5">{prob.detail}</p>}
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {/* Section: Lal Kitab Teaser */}
              <section>
                <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                  <BookOpen className="w-4 h-4" />
                  {l('Lal Kitab Remedy', '\u0932\u093E\u0932 \u0915\u093F\u0924\u093E\u092C \u0909\u092A\u093E\u092F')}
                  <Lock className="w-3.5 h-3.5 text-gray-400" />
                </h3>
                <div className="rounded-lg border border-sacred-gold/20 bg-gradient-to-r from-red-50/50 to-orange-50/50 p-4">
                  {lalkitabTeaser.remedy ? (
                    <p className="text-sm text-gray-700">{lalkitabTeaser.remedy}</p>
                  ) : (
                    <p className="text-sm text-gray-500 italic">{l('Lal Kitab remedies available in full report', '\u0932\u093E\u0932 \u0915\u093F\u0924\u093E\u092C \u0909\u092A\u093E\u092F \u092A\u0942\u0930\u094D\u0923 \u0930\u093F\u092A\u094B\u0930\u094D\u091F \u092E\u0947\u0902 \u0909\u092A\u0932\u092C\u094D\u0927')}</p>
                  )}
                  <p className="text-xs text-gray-400 mt-2 flex items-center gap-1">
                    <Lock className="w-3 h-3" />
                    {l('More remedies in full report', '\u092A\u0942\u0930\u094D\u0923 \u0930\u093F\u092A\u094B\u0930\u094D\u091F \u092E\u0947\u0902 \u0914\u0930 \u0909\u092A\u093E\u092F')}
                  </p>
                </div>
              </section>

              {/* Section: Panchang Teaser */}
              <section>
                <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                  <Star className="w-4 h-4" />
                  {l('Panchang', '\u092A\u0902\u091A\u093E\u0902\u0917')}
                  <Lock className="w-3.5 h-3.5 text-gray-400" />
                </h3>
                <div className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 p-4">
                  <div className="flex gap-4 text-sm">
                    {panchangTeaser.tithi && (
                      <div>
                        <span className="text-xs text-sacred-gold-dark/60 font-semibold">{l('Tithi', '\u0924\u093F\u0925\u093F')}: </span>
                        <span className="font-medium text-gray-800">{panchangTeaser.tithi}</span>
                      </div>
                    )}
                    {panchangTeaser.nakshatra && (
                      <div>
                        <span className="text-xs text-sacred-gold-dark/60 font-semibold">{l('Nakshatra', '\u0928\u0915\u094D\u0937\u0924\u094D\u0930')}: </span>
                        <span className="font-medium text-gray-800">{panchangTeaser.nakshatra}</span>
                      </div>
                    )}
                  </div>
                  <p className="text-xs text-gray-400 mt-2 flex items-center gap-1">
                    <Lock className="w-3 h-3" />
                    {l('Daily Muhurat available in full Panchang', '\u092A\u0942\u0930\u094D\u0923 \u092A\u0902\u091A\u093E\u0902\u0917 \u092E\u0947\u0902 \u0926\u0948\u0928\u093F\u0915 \u092E\u0941\u0939\u0942\u0930\u094D\u0924 \u0909\u092A\u0932\u092C\u094D\u0927')}
                  </p>
                </div>
              </section>

              {/* Section: Numerology Teaser */}
              <section>
                <h3 className="text-base font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
                  <Hash className="w-4 h-4" />
                  {l('Numerology', '\u0905\u0902\u0915 \u0936\u093E\u0938\u094D\u0924\u094D\u0930')}
                  <Lock className="w-3.5 h-3.5 text-gray-400" />
                </h3>
                <div className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 p-4">
                  {numerologyTeaser.life_path != null && (
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-xs text-sacred-gold-dark/60 font-semibold">{l('Life Path Number', '\u091C\u0940\u0935\u0928 \u092A\u0925 \u0905\u0902\u0915')}: </span>
                      <span className="text-lg font-bold text-sacred-gold-dark">{numerologyTeaser.life_path}</span>
                    </div>
                  )}
                  {numerologyTeaser.summary && (
                    <p className="text-sm text-gray-700">{numerologyTeaser.summary}</p>
                  )}
                </div>
              </section>
            </div>

          </div>
        </div>

        {/* CTA - Sticky bottom */}
        <div className="sticky bottom-0 z-20 bg-white border-t border-sacred-gold/20 px-6 py-4 rounded-b-2xl">
          <button
            onClick={handleUnlock}
            className="w-full py-3 bg-sacred-gold-dark text-white rounded-xl font-bold text-base hover:bg-[#a0581a] transition-all shadow-lg shadow-sacred-gold/30 flex items-center justify-center gap-2"
          >
            <Star className="w-5 h-5" />
            {l('Unlock Full Kundli Analysis', '\u092A\u0942\u0930\u094D\u0923 \u0915\u0941\u0902\u0921\u0932\u0940 \u0935\u093F\u0936\u094D\u0932\u0947\u0937\u0923 \u0905\u0928\u0932\u0949\u0915 \u0915\u0930\u0947\u0902')}
          </button>
          <p className="text-center text-xs text-gray-400 mt-2">
            {l(
              'Full Lal Kitab \u00b7 Detailed Predictions \u00b7 Timeline \u00b7 Complete Remedies',
              '\u092A\u0942\u0930\u094D\u0923 \u0932\u093E\u0932 \u0915\u093F\u0924\u093E\u092C \u00b7 \u0935\u093F\u0938\u094D\u0924\u0943\u0924 \u092D\u0935\u093F\u0937\u094D\u092F\u0935\u093E\u0923\u0940 \u00b7 \u0938\u092E\u092F\u0930\u0947\u0916\u093E \u00b7 \u092A\u0942\u0930\u094D\u0923 \u0909\u092A\u093E\u092F'
            )}
          </p>
        </div>
      </div>
    </div>,
    document.body
  );
}
