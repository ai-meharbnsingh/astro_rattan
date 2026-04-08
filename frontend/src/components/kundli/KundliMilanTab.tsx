import { useState } from 'react';
import { Loader2, Heart, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

interface KundliMilanTabProps {
  savedKundlis: any[];
  currentKundliId?: string;
}

const KOOT_ORDER = ['Varna', 'Vasya', 'Tara', 'Yoni', 'Graha Maitri', 'Gana', 'Bhakoot', 'Nadi'];

const KOOT_LABELS_HI: Record<string, string> = {
  Varna: 'वर्ण', Vasya: 'वश्य', Tara: 'तारा', Yoni: 'योनि',
  'Graha Maitri': 'ग्रह मैत्री', Gana: 'गण', Bhakoot: 'भकूट', Nadi: 'नाड़ी',
};

const GUNA_DETAIL_ROWS = [
  { key: 'nakshatra', en: 'Nakshatra', hi: 'नक्षत्र' },
  { key: 'rashi', en: 'Rashi', hi: 'राशि' },
  { key: 'varna', en: 'Varna', hi: 'वर्ण' },
  { key: 'vasya', en: 'Vasya', hi: 'वश्य' },
  { key: 'yoni', en: 'Yoni', hi: 'योनि' },
  { key: 'gana', en: 'Gana', hi: 'गण' },
  { key: 'nadi', en: 'Nadi', hi: 'नाड़ी' },
  { key: 'lord', en: 'Nakshatra Lord', hi: 'नक्षत्र स्वामी' },
];

export default function KundliMilanTab({ savedKundlis, currentKundliId }: KundliMilanTabProps) {
  const { t, language } = useTranslation();
  const [person1Id, setPerson1Id] = useState(currentKundliId || '');
  const [person2Id, setPerson2Id] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleMatch = async () => {
    if (!person1Id || !person2Id) return;
    if (person1Id === person2Id) {
      setError(language === 'hi' ? 'दोनों कुंडली अलग होनी चाहिए' : 'Please select two different kundlis');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const data = await api.post('/api/kundli/match', {
        kundli_id_1: person1Id,
        kundli_id_2: person2Id,
      });
      setResult(data);
    } catch (e: any) {
      setError(e.message || 'Match failed');
    }
    setLoading(false);
  };

  const getScoreColor = (total: number) => {
    if (total >= 24) return { bg: '#d1fae5', text: '#065f46', border: '#059669' };
    if (total >= 18) return { bg: '#fef3c7', text: '#92400e', border: '#d97706' };
    return { bg: '#fee2e2', text: '#991b1b', border: '#dc2626' };
  };

  const getScoreIcon = (total: number) => {
    if (total >= 24) return <CheckCircle className="w-6 h-6" style={{ color: '#059669' }} />;
    if (total >= 18) return <AlertTriangle className="w-6 h-6" style={{ color: '#d97706' }} />;
    return <XCircle className="w-6 h-6" style={{ color: '#dc2626' }} />;
  };

  return (
    <div className="space-y-6">
      {/* Selection Panel */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-6">
        <h4 className="font-display font-semibold text-sacred-brown mb-4 flex items-center gap-2">
          <Heart className="w-5 h-5 text-sacred-gold" />
          {language === 'hi' ? 'कुंडली मिलान (अष्टकूट गुण मिलान)' : 'Kundli Milan (Ashtakoot Gun Milan)'}
        </h4>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          {/* Person 1 */}
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--ink-light)' }}>
              {language === 'hi' ? 'वर (Person 1)' : 'Groom (Person 1)'}
            </label>
            <select
              value={person1Id}
              onChange={(e) => setPerson1Id(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border text-sm"
              style={{ borderColor: 'var(--cosmic-border)', backgroundColor: 'var(--cosmic-surface)', color: 'var(--ink)' }}
            >
              <option value="">{language === 'hi' ? '— कुंडली चुनें —' : '— Select Kundli —'}</option>
              {savedKundlis.map((k: any) => (
                <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
              ))}
            </select>
          </div>

          {/* Person 2 */}
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--ink-light)' }}>
              {language === 'hi' ? 'वधू (Person 2)' : 'Bride (Person 2)'}
            </label>
            <select
              value={person2Id}
              onChange={(e) => setPerson2Id(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border text-sm"
              style={{ borderColor: 'var(--cosmic-border)', backgroundColor: 'var(--cosmic-surface)', color: 'var(--ink)' }}
            >
              <option value="">{language === 'hi' ? '— कुंडली चुनें —' : '— Select Kundli —'}</option>
              {savedKundlis.map((k: any) => (
                <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
              ))}
            </select>
          </div>
        </div>

        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

        <Button
          onClick={handleMatch}
          disabled={!person1Id || !person2Id || loading}
          className="bg-sacred-gold text-white hover:bg-sacred-gold-dark"
        >
          {loading ? (
            <><Loader2 className="w-4 h-4 animate-spin mr-2" />{language === 'hi' ? 'मिलान हो रहा है...' : 'Matching...'}</>
          ) : (
            <><Heart className="w-4 h-4 mr-2" />{language === 'hi' ? 'कुंडली मिलान करें' : 'Match Kundlis'}</>
          )}
        </Button>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-4">
          {/* Score Header */}
          <div
            className="rounded-xl p-6 border-2 text-center"
            style={{
              backgroundColor: getScoreColor(result.total_score).bg,
              borderColor: getScoreColor(result.total_score).border,
            }}
          >
            <div className="flex items-center justify-center gap-3 mb-2">
              {getScoreIcon(result.total_score)}
              <span className="text-4xl font-bold font-mono" style={{ color: getScoreColor(result.total_score).text }}>
                {result.total_score}/36
              </span>
            </div>
            <p className="text-lg font-semibold" style={{ color: getScoreColor(result.total_score).text }}>
              {result.recommendation}
            </p>
            <p className="text-sm mt-1" style={{ color: getScoreColor(result.total_score).text }}>
              {result.person1} & {result.person2} — {result.compatibility_percentage}% {language === 'hi' ? 'अनुकूलता' : 'Compatibility'}
            </p>

            {/* Progress bar */}
            <div className="mt-3 h-3 bg-white/50 rounded-full overflow-hidden max-w-md mx-auto">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: `${result.compatibility_percentage}%`,
                  backgroundColor: getScoreColor(result.total_score).border,
                }}
              />
            </div>
          </div>

          {/* 8-Koot Breakdown */}
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
            <h4 className="font-display font-semibold text-sacred-brown mb-3">
              {language === 'hi' ? 'अष्टकूट विवरण' : '8-Koot Breakdown'}
            </h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-slate-100">
                    <th className="text-left p-2 font-medium text-slate-600">#</th>
                    <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'कूट' : 'Koot'}</th>
                    <th className="text-center p-2 font-medium text-slate-600">{language === 'hi' ? 'प्राप्त' : 'Score'}</th>
                    <th className="text-center p-2 font-medium text-slate-600">{language === 'hi' ? 'अधिकतम' : 'Max'}</th>
                    <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'विवरण' : 'Description'}</th>
                  </tr>
                </thead>
                <tbody>
                  {KOOT_ORDER.map((koot, i) => {
                    const data = result.koot_scores?.[koot];
                    if (!data) return null;
                    const isFull = data.score === data.max;
                    const isZero = data.score === 0;
                    return (
                      <tr key={koot} className="border-b border-slate-100">
                        <td className="p-2 text-slate-400">{i + 1}</td>
                        <td className="p-2 font-semibold">
                          {language === 'hi' ? KOOT_LABELS_HI[koot] || koot : koot}
                        </td>
                        <td className="p-2 text-center">
                          <span
                            className="inline-block px-2 py-0.5 rounded-full text-xs font-bold"
                            style={{
                              backgroundColor: isFull ? '#d1fae5' : isZero ? '#fee2e2' : '#fef3c7',
                              color: isFull ? '#065f46' : isZero ? '#991b1b' : '#92400e',
                            }}
                          >
                            {data.score}
                          </span>
                        </td>
                        <td className="p-2 text-center text-slate-400">{data.max}</td>
                        <td className="p-2 text-xs text-slate-500">{data.description}</td>
                      </tr>
                    );
                  })}
                </tbody>
                <tfoot>
                  <tr className="bg-slate-50 font-semibold">
                    <td className="p-2" />
                    <td className="p-2">{language === 'hi' ? 'कुल' : 'Total'}</td>
                    <td className="p-2 text-center text-lg" style={{ color: getScoreColor(result.total_score).text }}>
                      {result.total_score}
                    </td>
                    <td className="p-2 text-center">36</td>
                    <td className="p-2" />
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>

          {/* Guna Details */}
          {result.person1_details && result.person2_details && (
            <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
              <h4 className="font-display font-semibold text-sacred-brown mb-3">
                {language === 'hi' ? 'गुण विवरण' : 'Guna Details'}
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-slate-100">
                      <th className="text-left p-2 font-medium text-slate-600">
                        {language === 'hi' ? 'गुण' : 'Property'}
                      </th>
                      <th className="text-center p-2 font-medium text-slate-600">
                        {result.person1 || (language === 'hi' ? 'वर' : 'Person 1')}
                      </th>
                      <th className="text-center p-2 font-medium text-slate-600">
                        {result.person2 || (language === 'hi' ? 'वधू' : 'Person 2')}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {GUNA_DETAIL_ROWS.map((row) => {
                      const val1 = result.person1_details[row.key] ?? '-';
                      const val2 = result.person2_details[row.key] ?? '-';
                      const isMatch = val1 === val2;
                      return (
                        <tr key={row.key} className="border-b border-slate-100">
                          <td className="p-2 font-semibold">
                            {language === 'hi' ? row.hi : row.en}
                          </td>
                          <td
                            className="p-2 text-center"
                            style={{
                              backgroundColor: isMatch ? '#f0fdf4' : undefined,
                              color: isMatch ? '#166534' : undefined,
                            }}
                          >
                            {val1}
                          </td>
                          <td
                            className="p-2 text-center"
                            style={{
                              backgroundColor: isMatch ? '#f0fdf4' : undefined,
                              color: isMatch ? '#166534' : undefined,
                            }}
                          >
                            {val2}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Dosha Checks */}
          {result.doshas && result.doshas.length > 0 && (
            <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
              <h4 className="font-display font-semibold text-sacred-brown mb-3">
                {language === 'hi' ? 'दोष जांच एवं निवारण' : 'Dosha Checks & Cancellation'}
              </h4>
              <div className="space-y-3">
                {result.doshas.map((dosha: any, idx: number) => (
                  <div
                    key={idx}
                    className="rounded-lg border p-3"
                    style={{
                      borderColor: !dosha.present ? '#86efac' : dosha.cancelled ? '#fcd34d' : '#fca5a5',
                      backgroundColor: !dosha.present ? '#f0fdf4' : dosha.cancelled ? '#fffbeb' : '#fef2f2',
                    }}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-sm text-sacred-brown">{dosha.name}</span>
                      <span
                        className="text-xs px-2 py-0.5 rounded-full font-medium"
                        style={{
                          backgroundColor: !dosha.present ? '#dcfce7' : dosha.cancelled ? '#fef3c7' : '#fee2e2',
                          color: !dosha.present ? '#166534' : dosha.cancelled ? '#92400e' : '#991b1b',
                        }}
                      >
                        {!dosha.present
                          ? (language === 'hi' ? 'दोष नहीं' : 'No Dosha')
                          : dosha.cancelled
                            ? (language === 'hi' ? 'दोष निवारित' : 'Dosha Cancelled')
                            : (language === 'hi' ? 'दोष उपस्थित' : 'Dosha Present')}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600">{dosha.description}</p>
                    {dosha.cancelled && dosha.cancel_reasons?.length > 0 && (
                      <div className="mt-1 text-xs text-amber-700">
                        <strong>{language === 'hi' ? 'निवारण कारण:' : 'Cancellation:'}</strong>{' '}
                        {dosha.cancel_reasons.join('; ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
