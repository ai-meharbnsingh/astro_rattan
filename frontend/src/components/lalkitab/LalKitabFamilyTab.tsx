import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Loader2, Users, Link2, AlertTriangle, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface FamilyMember {
  kundli_id: string; name: string; relation: string;
  birth_date: string; shared_planets: string[];
  harmony_score: number; tension_planets: string[];
  support_planets: string[];
}
interface FamilyData {
  kundli_id: string; linked_members: FamilyMember[];
  family_harmony: number;
  dominant_planet: string | null;
  family_theme: { en: string; hi: string } | null;
}

interface Props { kundliId?: string; language: string; }

const PLANET_DOT: Record<string, string> = {
  Sun:'bg-orange-500', Moon:'bg-blue-300', Mars:'bg-red-500', Mercury:'bg-green-500',
  Jupiter:'bg-yellow-500', Venus:'bg-pink-400', Saturn:'bg-gray-500', Rahu:'bg-purple-600', Ketu:'bg-amber-700',
};
const RELATION_ICON: Record<string, string> = {
  father:'👨', mother:'👩', spouse:'💑', son:'👦', daughter:'👧',
  brother:'🧑', sister:'👧', grandfather:'👴', grandmother:'👵',
};

function HarmonyBar({ score }: { score: number }) {
  const color = score >= 70 ? 'bg-green-500' : score >= 40 ? 'bg-yellow-500' : 'bg-red-500';
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 bg-gray-100 rounded-full h-1.5">
        <div className={`h-1.5 rounded-full transition-all ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-xs font-semibold tabular-nums w-6">{score}</span>
    </div>
  );
}

export default function LalKitabFamilyTab({ kundliId, language }: Props) {
  const [data, setData] = useState<FamilyData | null>(null);
  const [loading, setLoading] = useState(false);
  const [linking, setLinking] = useState(false);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/lalkitab/family/${kundliId}`)
      .then(setData).catch(() => {}).finally(() => setLoading(false));
  }, [kundliId]);

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'परिवार विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to use Family Linking.'}
    </div>
  );

  if (loading) return (
    <div className="flex justify-center py-16">
      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
    </div>
  );

  if (!data) return null;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="text-center">
        <div className="text-3xl mb-1">👨‍👩‍👧‍👦</div>
        <h3 className="font-bold text-foreground">
          {hi ? 'ग्रह-गस्ती — परिवार लिंकिंग' : 'Grah-Gasti — Family Chart Linking'}
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          {hi
            ? 'परिवार के सदस्यों की कुंडलियों को जोड़कर ग्रह प्रभाव देखें'
            : 'Link family member charts to reveal cross-chart planetary interactions'}
        </p>
      </div>

      {/* Family harmony */}
      {data.linked_members.length > 0 && (
        <div className="card-sacred rounded-xl p-4 bg-sacred-gold/5 border border-sacred-gold/20">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
            {hi ? 'पारिवारिक सौहार्द स्कोर' : 'Family Harmony Score'}
          </div>
          <div className="flex items-center gap-3 mb-3">
            <div className="text-4xl font-bold text-sacred-gold">{data.family_harmony}</div>
            <div className="flex-1">
              <HarmonyBar score={data.family_harmony} />
              {data.family_theme && (
                <p className="text-xs text-muted-foreground mt-1 italic">
                  "{hi ? data.family_theme.hi : data.family_theme.en}"
                </p>
              )}
            </div>
          </div>
          {data.dominant_planet && (
            <div className="flex items-center gap-2 text-xs text-foreground">
              <span className={`w-2.5 h-2.5 rounded-full ${PLANET_DOT[data.dominant_planet] || 'bg-gray-400'}`} />
              <span>
                {hi
                  ? `${data.dominant_planet} आपके परिवार का प्रमुख ग्रह है`
                  : `${data.dominant_planet} is the dominant planet in your family`}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Member cards */}
      {data.linked_members.length > 0 ? (
        <div className="space-y-3">
          <div className="text-sm font-semibold text-foreground px-1">
            {hi ? `${data.linked_members.length} सदस्य जुड़े हुए हैं` : `${data.linked_members.length} member(s) linked`}
          </div>
          {data.linked_members.map((member) => (
            <div key={member.kundli_id} className="border border-border bg-card rounded-xl p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xl">{RELATION_ICON[member.relation] || '👤'}</span>
                  <div>
                    <div className="font-bold text-foreground text-sm">{member.name}</div>
                    <div className="text-xs text-muted-foreground capitalize">{member.relation}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-muted-foreground mb-1">
                    {hi ? 'सौहार्द' : 'Harmony'}
                  </div>
                  <HarmonyBar score={member.harmony_score} />
                </div>
              </div>

              {/* Shared planets */}
              {member.shared_planets.length > 0 && (
                <div className="mb-2">
                  <div className="text-xs font-semibold text-muted-foreground mb-1">
                    <Link2 className="w-3 h-3 inline mr-1" />
                    {hi ? 'साझा ग्रह' : 'Shared planets'}
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {member.shared_planets.map(p => (
                      <span key={p} className="flex items-center gap-1 text-xs bg-sacred-gold/10 text-sacred-gold px-1.5 py-0.5 rounded-full">
                        <span className={`w-1.5 h-1.5 rounded-full ${PLANET_DOT[p] || 'bg-gray-400'}`} />
                        {p}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Support & Tension */}
              <div className="grid grid-cols-2 gap-2">
                {member.support_planets.length > 0 && (
                  <div className="bg-green-50 rounded-lg p-2">
                    <div className="flex items-center gap-1 text-xs font-semibold text-green-700 mb-1">
                      <TrendingUp className="w-3 h-3" />
                      {hi ? 'सहयोग' : 'Support'}
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {member.support_planets.map(p => (
                        <span key={p} className="text-xs text-green-600">{p}</span>
                      ))}
                    </div>
                  </div>
                )}
                {member.tension_planets.length > 0 && (
                  <div className="bg-red-50 rounded-lg p-2">
                    <div className="flex items-center gap-1 text-xs font-semibold text-red-700 mb-1">
                      <TrendingDown className="w-3 h-3" />
                      {hi ? 'तनाव' : 'Tension'}
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {member.tension_planets.map(p => (
                        <span key={p} className="text-xs text-red-600">{p}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Empty state */
        <div className="border border-dashed border-border rounded-xl p-8 text-center">
          <Users className="w-10 h-10 text-muted-foreground/40 mx-auto mb-3" />
          <p className="text-sm font-semibold text-foreground mb-1">
            {hi ? 'कोई परिवार सदस्य नहीं जुड़ा' : 'No family members linked yet'}
          </p>
          <p className="text-xs text-muted-foreground mb-4">
            {hi
              ? 'परिवार के अन्य सदस्यों की कुंडली बनाएं और यहाँ जोड़ें'
              : 'Create Kundlis for family members and link them here to see cross-chart analysis'}
          </p>
          <div className="text-xs text-muted-foreground bg-muted/30 rounded-lg p-3 text-left space-y-1">
            <p>1. {hi ? 'परिवार के सदस्य का नाम + जन्म विवरण दर्ज करें' : 'Enter family member birth details'}</p>
            <p>2. {hi ? 'कुंडली सहेजें' : 'Save their Kundli'}</p>
            <p>3. {hi ? '"परिवार में जोड़ें" बटन दबाएं' : 'Click "Add to Family" in their Kundli'}</p>
          </div>
        </div>
      )}

      <div className="flex items-start gap-2 bg-amber-50 border border-amber-100 rounded-xl p-3">
        <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 shrink-0" />
        <p className="text-xs text-amber-700">
          {hi
            ? 'यह सुविधा अभी विकास में है। परिवार जोड़ने की पूर्ण कार्यक्षमता जल्द आएगी।'
            : 'Family linking is in development. Full add/link functionality coming soon.'}
        </p>
      </div>
    </div>
  );
}
