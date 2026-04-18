import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { pickLang } from '@/components/lalkitab/safe-render';
import { Loader2, ArrowRight, Moon, Zap, Crown, Eye, Swords, Plane, Shield } from 'lucide-react';

interface Props { kundliId?: string; language: string; }

const PLANET_DOT: Record<string, string> = {
  Sun:'bg-orange-500', Moon:'bg-blue-300', Mars:'bg-red-500', Mercury:'bg-green-500',
  Jupiter:'bg-yellow-500', Venus:'bg-pink-400', Saturn:'bg-gray-500', Rahu:'bg-purple-600', Ketu:'bg-amber-700',
};

export default function LalKitabTechnicalTab({ kundliId, language }: Props) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    setLoadError(null);
    api.get(`/api/lalkitab/technical/${kundliId}`)
      .then(setData)
      .catch((err) => {
        console.error('Failed to load technical data:', err);
        const msg = err instanceof Error ? err.message : (typeof err === 'string' ? err : 'Unknown error');
        setLoadError(msg);
      })
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to see technical analysis.'}
    </div>
  );
  if (loading) return <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 animate-spin text-sacred-gold" /></div>;
  if (loadError && !data) return (
    <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
      {hi ? 'डेटा लोड करने में त्रुटि' : 'Failed to load data'}: {loadError}
    </div>
  );
  if (!data) return null;

  const { chalti_gaadi, dhur_dhur_aage, soya_ghar, planet_statuses, muththi, kayam } = data;

  const trainStatusColor: Record<string, string> = {
    smooth: 'bg-green-100 text-green-700',
    dangerous: 'bg-red-100 text-red-700',
    stalled: 'bg-orange-100 text-orange-700',
    drifting: 'bg-yellow-100 text-yellow-700',
    uncontrolled: 'bg-red-50 text-red-600',
    moving: 'bg-blue-100 text-blue-700',
    empty: 'bg-gray-100 text-gray-600',
  };

  const directionColor: Record<string, string> = {
    benefic: 'bg-green-100 text-green-700',
    malefic: 'bg-red-100 text-red-700',
    neutral: 'bg-gray-100 text-gray-600',
  };

  return (
    <div className="space-y-6">
      {loadError && (
        <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
          {hi ? 'डेटा लोड करने में त्रुटि' : 'Failed to load data'}: {loadError}
        </div>
      )}

      {/* ── 1. CHALTI GAADI ── */}
      <div className="card-sacred rounded-xl p-4">
        <h3 className="font-bold text-sacred-gold mb-3 flex items-center gap-2">
          🚂 {hi ? 'चलती गाड़ी (जीवन-ट्रेन)' : 'Chalti Gaadi (Life Train)'}
        </h3>
        <div className="flex items-center gap-2 mb-3 overflow-x-auto pb-1">
          {/* Engine */}
          <div className="flex-1 min-w-[80px] border border-sacred-gold/30 rounded-xl p-3 text-center bg-sacred-gold/5">
            <div className="text-xs text-muted-foreground mb-1">{hi ? 'इंजन (H1)' : 'Engine (H1)'}</div>
            <div className={`font-bold text-sm ${chalti_gaadi.engine ? 'text-foreground' : 'text-muted-foreground'}`}>
              {chalti_gaadi.engine?.planet || '—'}
            </div>
          </div>
          <div className="flex items-center gap-1 text-muted-foreground shrink-0">
            <ArrowRight className="w-4 h-4" />
            <ArrowRight className="w-4 h-4 -ml-2" />
          </div>
          {/* Passenger */}
          <div className="flex-1 min-w-[80px] border border-sacred-gold/30 rounded-xl p-3 text-center bg-sacred-gold/5">
            <div className="text-xs text-muted-foreground mb-1">{hi ? 'यात्री (H7)' : 'Passenger (H7)'}</div>
            <div className={`font-bold text-sm ${chalti_gaadi.passenger ? 'text-foreground' : 'text-muted-foreground'}`}>
              {chalti_gaadi.passenger?.planet || '—'}
            </div>
          </div>
          <div className="flex items-center gap-1 text-muted-foreground shrink-0">
            <ArrowRight className="w-4 h-4" />
          </div>
          {/* Brakes */}
          <div className="flex-1 min-w-[80px] border border-red-200 rounded-xl p-3 text-center bg-red-50/30">
            <div className="text-xs text-muted-foreground mb-1">{hi ? 'ब्रेक (H8)' : 'Brakes (H8)'}</div>
            <div className={`font-bold text-sm ${chalti_gaadi.brakes ? 'text-foreground' : 'text-muted-foreground'}`}>
              {chalti_gaadi.brakes?.planet || '—'}
            </div>
          </div>
        </div>
        <div className={`inline-flex px-3 py-1 rounded-full text-sm font-semibold mb-2 ${trainStatusColor[chalti_gaadi.train_status] || 'bg-gray-100 text-gray-600'}`}>
          {(chalti_gaadi.train_status ?? 'unknown').toUpperCase()}
        </div>
        <p className="text-sm text-muted-foreground leading-relaxed">
          {pickLang(chalti_gaadi.interpretation, hi)}
        </p>
      </div>

      {/* ── 2. DHUR-DHUR-AAGE ── */}
      <div className="card-sacred rounded-xl p-4">
        <h3 className="font-bold text-sacred-gold mb-1 flex items-center gap-2">
          <Zap className="w-4 h-4" /> {hi ? 'धुर-धुर-आगे (द पुश)' : 'Dhur-Dhur-Aage (The Push)'}
        </h3>
        <p className="text-xs text-muted-foreground mb-3">
          {hi ? 'N-1 घर का ग्रह N घर के ग्रह को धकेलता है।' : 'Planet in house N-1 pushes planet in house N.'}
        </p>
        {dhur_dhur_aage.pushes?.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            {hi ? 'कोई धक्का संबंध नहीं मिला।' : 'No consecutive house push relationships found.'}
          </p>
        ) : (
          <>
            {dhur_dhur_aage.most_pushful_planet && (
              <div className="flex flex-wrap gap-2 mb-3">
                <span className="text-xs px-2 py-1 bg-orange-50 text-orange-700 rounded-full">
                  {hi ? `सबसे ताकतवर: ${dhur_dhur_aage.most_pushful_planet}` : `Most Forceful: ${dhur_dhur_aage.most_pushful_planet}`}
                </span>
                {dhur_dhur_aage.most_pushed_planet && (
                  <span className="text-xs px-2 py-1 bg-purple-50 text-purple-700 rounded-full">
                    {hi ? `सबसे दबाव में: ${dhur_dhur_aage.most_pushed_planet}` : `Most Pushed: ${dhur_dhur_aage.most_pushed_planet}`}
                  </span>
                )}
              </div>
            )}
            <div className="space-y-2">
              {dhur_dhur_aage.pushes?.map((push: any, i: number) => (
                <div key={i} className="flex items-center gap-2 text-sm border border-border rounded-lg p-2.5">
                  <span className="font-semibold text-foreground">{push.pusher}</span>
                  <span className="text-xs text-muted-foreground">H{isNaN(Number(push.pusher_house)) ? 0 : push.pusher_house}</span>
                  <ArrowRight className="w-3.5 h-3.5 text-muted-foreground" />
                  <span className="font-semibold text-foreground">{push.receiver}</span>
                  <span className="text-xs text-muted-foreground">H{isNaN(Number(push.receiver_house)) ? 0 : push.receiver_house}</span>
                  <span className={`ml-auto text-xs px-2 py-0.5 rounded-full ${directionColor[push.direction] || ''}`}>
                    {push.direction}
                  </span>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* ── 3. SOYA GHAR ── */}
      <div className="card-sacred rounded-xl p-4">
        <h3 className="font-bold text-sacred-gold mb-3 flex items-center gap-2">
          <Moon className="w-4 h-4" /> {hi ? 'सोया घर (निष्क्रिय घर)' : 'Soya Ghar (Sleeping Houses)'}
        </h3>
        <div className="grid grid-cols-6 sm:grid-cols-12 gap-1 mb-3">
          {Array.from({length:12}, (_,i) => i+1).map(h => {
            const awake = soya_ghar.awake_houses?.includes(h);
            return (
              <div key={h} className={`aspect-square flex items-center justify-center rounded text-xs font-bold
                ${awake ? 'bg-sacred-gold/20 text-sacred-gold border border-sacred-gold/40' : 'bg-gray-100 text-gray-400 border border-gray-200'}`}>
                {h}
              </div>
            );
          })}
        </div>
        <div className="flex gap-3 text-xs mb-3">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-sacred-gold/20 border border-sacred-gold/40" />{hi?'जागता':'Awake'}</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-gray-100 border border-gray-200" />{hi?'सोता':'Sleeping'}</span>
        </div>
        {soya_ghar.sleeping_house_effects?.length > 0 && (
          <div className="space-y-2 mt-2">
            {soya_ghar.sleeping_house_effects.map((item: any) => (
              <div key={item.house} className="border border-border rounded-lg p-2.5">
                <div className="font-semibold text-xs text-foreground mb-1">
                  {hi ? `घर ${item.house}:` : `House ${item.house}:`} {pickLang(item.effect, hi)}
                </div>
                <div className="text-xs text-green-700">
                  💊 {pickLang(item.remedy, hi)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── 4. PLANET STATUSES ── */}
      <div className="card-sacred rounded-xl p-4">
        <h3 className="font-bold text-sacred-gold mb-3">
          {hi ? '🏛️ ग्रह स्थिति वर्गीकरण' : '🏛️ Planet Status Classification'}
        </h3>
        <div className="space-y-2">
          {planet_statuses?.filter((p: any) =>
            p.status.sarkari || p.status.bhedi || p.status.zakhmi || p.status.pardesi || p.status.gair_sarkari
          ).map((p: any) => (
            <div key={typeof p.planet === 'string' ? p.planet : pickLang(p.planet, false)} className="border border-border rounded-lg p-2.5">
              <div className="flex items-center gap-2 mb-1.5">
                <span className={`w-2.5 h-2.5 rounded-full ${PLANET_DOT[typeof p.planet === 'string' ? p.planet : pickLang(p.planet, false)] || 'bg-gray-400'}`} />
                <span className="font-semibold text-sm">{typeof p.planet === 'string' ? p.planet : pickLang(p.planet, false)}</span>
                <span className="text-xs text-muted-foreground">H{p.house}</span>
                <div className="flex flex-wrap gap-1 ml-1">
                  {p.status.sarkari && <span className="text-xs px-1.5 py-0.5 bg-yellow-100 text-yellow-700 rounded flex items-center gap-0.5"><Crown className="w-3 h-3" />{hi?'सरकारी':'Sarkari'}</span>}
                  {p.status.gair_sarkari && <span className="text-xs px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded">Gair-Sarkari</span>}
                  {p.status.bhedi && <span className="text-xs px-1.5 py-0.5 bg-gray-200 text-gray-700 rounded flex items-center gap-0.5"><Eye className="w-3 h-3" />{hi?'भेदी':'Bhedi'}</span>}
                  {p.status.zakhmi && <span className="text-xs px-1.5 py-0.5 bg-red-100 text-red-700 rounded flex items-center gap-0.5"><Swords className="w-3 h-3" />{hi?'ज़ख्मी':'Zakhmi'}</span>}
                  {p.status.pardesi && <span className="text-xs px-1.5 py-0.5 bg-purple-100 text-purple-700 rounded flex items-center gap-0.5"><Plane className="w-3 h-3" />{hi?'परदेसी':'Pardesi'}</span>}
                </div>
              </div>
              {Object.values(p.status.details).map((detail: any, di: number) => (
                <p key={di} className="text-xs text-muted-foreground leading-relaxed">{detail}</p>
              ))}
            </div>
          ))}
          {planet_statuses?.filter((p: any) =>
            p.status.sarkari || p.status.bhedi || p.status.zakhmi || p.status.pardesi || p.status.gair_sarkari
          ).length === 0 && (
            <p className="text-sm text-muted-foreground">{hi ? 'कोई विशेष ग्रह वर्गीकरण नहीं।' : 'No special planet classifications found.'}</p>
          )}
        </div>
      </div>

      {/* ── 5. MUTH-THI ── */}
      <div className="card-sacred rounded-xl p-4">
        <h3 className="font-bold text-sacred-gold mb-3">
          ✊ {hi ? 'मुठ्ठी विश्लेषण (स्व-निर्मित बनाम पैतृक)' : 'Muth-Thi Analysis (Self-Made vs Ancestral)'}
        </h3>
        <div className="grid grid-cols-2 gap-3 mb-3">
          <div className="bg-green-50 border border-green-200 rounded-xl p-3 text-center">
            <div className="text-2xl mb-1">✊</div>
            <div className="text-xs font-semibold text-green-700 mb-2">{hi ? 'हाथ में (H1-6)' : 'In Hand (H1-6)'}</div>
            {muththi.in_hand?.length > 0 ? (
              <div className="flex flex-wrap justify-center gap-1">
                {muththi.in_hand.map((p: string) => (
                  <span key={p} className="text-xs px-1.5 py-0.5 bg-white border border-green-200 rounded text-green-700">{p}</span>
                ))}
              </div>
            ) : <span className="text-xs text-muted-foreground">{hi?'कोई नहीं':'None'}</span>}
          </div>
          <div className="bg-orange-50 border border-orange-200 rounded-xl p-3 text-center">
            <div className="text-2xl mb-1">🤲</div>
            <div className="text-xs font-semibold text-orange-700 mb-2">{hi ? 'हाथ के बाहर (H7-12)' : 'Out of Hand (H7-12)'}</div>
            {muththi.out_hand?.length > 0 ? (
              <div className="flex flex-wrap justify-center gap-1">
                {muththi.out_hand.map((p: string) => (
                  <span key={p} className="text-xs px-1.5 py-0.5 bg-white border border-orange-200 rounded text-orange-700">{p}</span>
                ))}
              </div>
            ) : <span className="text-xs text-muted-foreground">{hi?'कोई नहीं':'None'}</span>}
          </div>
        </div>
        <div className="text-center mb-2">
          <span className="inline-block px-3 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold font-bold text-sm">
            {hi ? muththi.archetype_hi : muththi.archetype}
          </span>
        </div>
        <p className="text-sm text-foreground text-center leading-relaxed">
          {hi ? muththi.verdict_hi : muththi.verdict}
        </p>
        {muththi.recommendation && (
          <div className="mt-3 flex items-start gap-2 bg-amber-50 border border-amber-200 rounded-xl p-3 text-xs text-amber-700">
            <span className="shrink-0">🙏</span>
            {pickLang(muththi.recommendation, hi)}
          </div>
        )}
      </div>

      {/* ── 6. KAYAM GRAH ── */}
      <div className="card-sacred rounded-xl p-4">
        <h3 className="font-bold text-sacred-gold mb-1 flex items-center gap-2">
          <Shield className="w-4 h-4" />
          {hi ? 'कायम ग्रह (स्थापित ग्रह)' : 'Kayam Grah (Established Planets)'}
        </h3>
        <p className="text-xs text-muted-foreground mb-3">
          {hi
            ? 'ये ग्रह इतने दृढ़ हैं कि शत्रु ग्रह इन्हें कमज़ोर नहीं कर सकते।'
            : 'These planets are so strongly placed that enemy planets cannot weaken them.'}
        </p>
        {kayam && kayam.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {(kayam as string[]).map((planet) => (
              <div
                key={planet}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-sacred-gold/40 bg-sacred-gold/10"
              >
                <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${PLANET_DOT[planet] ?? 'bg-gray-400'}`} />
                <span className="text-sm font-semibold text-sacred-gold">
                  {hi
                    ? ({ Sun:'सूर्य', Moon:'चंद्र', Mars:'मंगल', Mercury:'बुध', Jupiter:'गुरु', Venus:'शुक्र', Saturn:'शनि', Rahu:'राहु', Ketu:'केतु' } as Record<string,string>)[planet] ?? planet
                    : planet}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            {hi
              ? 'इस कुंडली में कोई भी ग्रह पूरी तरह स्थापित नहीं है।'
              : 'No planets are fully established in this chart.'}
          </p>
        )}
      </div>

    </div>
  );
}
