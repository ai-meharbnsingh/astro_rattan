import { useState, useEffect } from 'react';
import { Sparkles, X } from 'lucide-react';
import { api } from '@/lib/api';
import type { PlanetData } from '@/components/InteractiveKundli';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { PLANET_ASPECTS, toDMS } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateLabel, translateNakshatra } from '@/lib/backend-translations';
import type { SidePanelState } from '@/hooks/useKundliData';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';
import SlokaHover from './SlokaHover';

function PlanetPropertiesSection({ kundliId, language }: { kundliId: string; language: string }) {
  const [data, setData] = useState<any>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/planet-properties`)
      .then(res => { if (!cancelled) setData(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (!data?.planets || typeof data.planets !== 'object') return null;

  const planetEntries = Object.entries(data.planets as Record<string, any>);
  if (planetEntries.length === 0) return null;

  const dni = data.day_night_indicator;
  const mgs = data.mercury_gender_state;

  return (
    <div className="mt-6 space-y-4">
      {/* ── Parent Indicators (Adhyaya 2 Day/Night Rule) ── */}
      {dni && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border flex items-center gap-2">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'पितृ-मातृ कारक (दिन/रात्रि नियम)' : 'Parent Indicators (Day/Night Rule)'}
            </span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${
              dni.day_night_chart === 'day'
                ? 'bg-amber-100 text-amber-800'
                : 'bg-indigo-100 text-indigo-800'
            }`}>
              {hi ? dni.day_night_chart_hi : (dni.day_night_chart === 'day' ? 'Day Chart' : 'Night Chart')}
            </span>
          </div>
          <div className="p-3 grid grid-cols-2 gap-3 text-xs">
            <div className="bg-card rounded-lg p-2.5 border border-border">
              <p className="text-foreground/60 mb-1">{hi ? 'पिता-कारक' : 'Father Indicator'}</p>
              <p className="font-semibold text-foreground text-sm">{translatePlanet(dni.father_indicator?.planet, language)}</p>
              <p className="text-foreground/70 mt-1 leading-snug">
                {hi ? dni.father_indicator?.reason_hi : dni.father_indicator?.reason_en}
              </p>
            </div>
            <div className="bg-card rounded-lg p-2.5 border border-border">
              <p className="text-foreground/60 mb-1">{hi ? 'माता-कारक' : 'Mother Indicator'}</p>
              <p className="font-semibold text-foreground text-sm">{translatePlanet(dni.mother_indicator?.planet, language)}</p>
              <p className="text-foreground/70 mt-1 leading-snug">
                {hi ? dni.mother_indicator?.reason_hi : dni.mother_indicator?.reason_en}
              </p>
            </div>
          </div>
          {dni.sloka_ref && (
            <SlokaHover slokaRef={dni.sloka_ref} language={language} className="px-3 pb-2 text-[10px] text-foreground/40 italic" />
          )}
        </div>
      )}

      {/* ── Mercury Gender State (Adhyaya 2 Hermaphrodite Rule) ── */}
      {mgs && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border flex items-center gap-2">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'बुध लिंग-अवस्था' : 'Mercury Gender State'}
            </span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${
              mgs.effective_gender === 'male'
                ? 'bg-blue-100 text-blue-800'
                : mgs.effective_gender === 'female'
                  ? 'bg-pink-100 text-pink-800'
                  : 'bg-slate-100 text-slate-700'
            }`}>
              {hi ? mgs.effective_gender_hi : mgs.effective_gender}
            </span>
          </div>
          <div className="p-3 text-xs text-foreground/80">
            <p>{hi ? mgs.reason_hi : mgs.reason_en}</p>
            {mgs.conjunct_planets?.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {mgs.conjunct_planets.map((p: string) => (
                  <span key={p} className="px-1.5 py-0.5 bg-muted rounded text-[10px] font-medium text-foreground">
                    {translatePlanet(p, language)}
                  </span>
                ))}
              </div>
            )}
          </div>
          {mgs.sloka_ref && (
            <SlokaHover slokaRef={mgs.sloka_ref} language={language} className="px-3 pb-2 text-[10px] text-foreground/40 italic" />
          )}
        </div>
      )}

      {/* ── Mercury Hermaphrodite Extended Note ── */}
      {data.planets?.Mercury?.hermaphrodite_note && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'बुध नपुंसक प्रकृति (विस्तृत)' : 'Mercury Hermaphrodite Nature (Extended)'}
            </span>
          </div>
          <div className="p-3 text-xs text-foreground/80 space-y-1">
            {(() => {
              const note = data.planets.Mercury.hermaphrodite_note;
              return (
                <>
                  <p>{hi ? note.reason_hi : note.reason_en}</p>
                  {note.conjunct_planets?.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-1">
                      {note.conjunct_planets.map((p: string) => (
                        <span key={p} className="px-1.5 py-0.5 bg-muted rounded text-[10px] font-medium">
                          {translatePlanet(p, language)}
                        </span>
                      ))}
                    </div>
                  )}
                  {note.sloka_ref && (
                    <SlokaHover slokaRef={note.sloka_ref} language={language} className="text-[10px] text-foreground/40 italic mt-1" />
                  )}
                </>
              );
            })()}
          </div>
        </div>
      )}

      {/* ── Sign Triads — Deva / Manava / Rakshasa (Phaladeepika Adh. 1) ── */}
      {data.lagna_triad?.triad && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border flex items-center gap-2">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'राशि त्रिगुण वर्गीकरण' : 'Sign Triads — Deva / Manava / Rakshasa'}
            </span>
          </div>
          <div className="p-3 space-y-2">
            {/* Lagna triad badge */}
            <div className="flex items-start gap-2 text-xs">
              <span className="text-foreground/60 shrink-0">{hi ? 'लग्न राशि:' : 'Lagna sign:'}</span>
              <span className={`font-bold px-2 py-0.5 rounded ${
                data.lagna_triad.triad === 'Deva' ? 'bg-amber-100 text-amber-800'
                : data.lagna_triad.triad === 'Manava' ? 'bg-blue-100 text-blue-800'
                : 'bg-red-100 text-red-800'
              }`}>
                {hi ? data.lagna_triad.triad_hi : data.lagna_triad.triad}
              </span>
              <span className="text-foreground/70 leading-snug">
                {hi ? data.lagna_triad.triad_nature_hi : data.lagna_triad.triad_nature_en}
              </span>
            </div>
            {/* Per-planet triads (compact inline) */}
            <div className="flex flex-wrap gap-1.5">
              {Object.entries(data.planets as Record<string, any>).map(([pname, p]: [string, any]) =>
                p.sign_triad?.triad ? (
                  <span key={pname} className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                    p.sign_triad.triad === 'Deva' ? 'bg-amber-50 text-amber-700 border border-amber-200'
                    : p.sign_triad.triad === 'Manava' ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'bg-red-50 text-red-700 border border-red-200'
                  }`} title={hi ? p.sign_triad.triad_nature_hi : p.sign_triad.triad_nature_en}>
                    {translatePlanet(pname, language)} — {hi ? p.sign_triad.triad_hi : p.sign_triad.triad}
                  </span>
                ) : null
              )}
            </div>
            {/* Legend */}
            {data.sign_triads_legend && (
              <div className="grid grid-cols-3 gap-2 mt-1">
                {Object.entries(data.sign_triads_legend as Record<string, { en: string; hi: string }>).map(([key, val]) => (
                  <div key={key} className={`rounded p-1.5 text-[10px] ${
                    key === 'Deva' ? 'bg-amber-50 border border-amber-200 text-amber-800'
                    : key === 'Manava' ? 'bg-blue-50 border border-blue-200 text-blue-800'
                    : 'bg-red-50 border border-red-200 text-red-800'
                  }`}>
                    <span className="font-bold block">{key}</span>
                    <span className="leading-snug">{hi ? val.hi : val.en}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
          <div className="px-3 pb-2 text-[10px] text-foreground/40 italic">
            <SlokaHover slokaRef="Phaladeepika Adh. 1" language={language}>{'Phaladeepika Adh. 1'}</SlokaHover>
          </div>
        </div>
      )}

      {/* ── Planet Properties Table (Stage / Guna / Baladi / Metal / Grain / Tree) ── */}
      <div className="rounded-xl border border-sacred-gold/20 overflow-x-auto bg-transparent">
        <div className="px-4 py-2 bg-muted border-b border-border">
          <span className="text-xs font-semibold text-primary uppercase tracking-wide">
            {hi ? 'ग्रह गुण — धातु, अन्न, वृक्ष' : 'Planet Properties — Metal, Grain, Tree'}
          </span>
        </div>
        <table className="table-sacred w-full text-xs">
          <thead className="bg-muted/50">
            <tr>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'ग्रह' : 'Planet'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'अवस्था' : 'Stage'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'गुण' : 'Guna'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'बलादि' : 'Baladi'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'धातु' : 'Metal'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'अन्न' : 'Grain'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'वृक्ष' : 'Tree'}</th>
            </tr>
          </thead>
          <tbody>
            {planetEntries.map(([planetName, p]: [string, any]) => (
              <tr key={planetName} className="border-t border-border">
                <td className="p-1.5 font-medium text-foreground">{translatePlanet(planetName, language)}</td>
                <td className="p-1.5 text-foreground/80">
                  {hi ? (p.stage_of_life?.stage_hi || p.stage_of_life?.stage) : p.stage_of_life?.stage}
                </td>
                <td className="p-1.5 text-foreground/80">
                  {hi ? (p.guna?.guna_hi || p.guna?.guna) : p.guna?.guna}
                </td>
                <td className="p-1.5 text-foreground/80">
                  {hi ? (p.baladi_avastha?.name_hi || p.baladi_avastha?.stage) : p.baladi_avastha?.stage}
                </td>
                <td className="p-1.5 text-foreground/70">
                  {hi ? (p.metal_hi || p.metal_en || '—') : (p.metal_en || '—')}
                </td>
                <td className="p-1.5 text-foreground/70">
                  {hi ? (p.grain_hi || p.grain_en || '—') : (p.grain_en || '—')}
                </td>
                <td className="p-1.5 text-foreground/70">
                  {hi ? (p.tree_hi || p.tree_en || '—') : (p.tree_en || '—')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function PanchadhaMaitriSection({ kundliId, language }: { kundliId: string; language: string }) {
  const [data, setData] = useState<any>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/panchadha-maitri`)
      .then(res => { if (!cancelled) setData(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (!data?.relations || (data.relations as any[]).length === 0) return null;

  const relationColor = (rel: string) => {
    if (!rel) return 'bg-slate-100 text-slate-600';
    const r = rel.toLowerCase();
    if (r.includes('great friend')) return 'bg-emerald-100 text-emerald-800';
    if (r.includes('friend')) return 'bg-green-100 text-green-800';
    if (r.includes('great enemy')) return 'bg-red-100 text-red-800';
    if (r.includes('enemy')) return 'bg-orange-100 text-orange-800';
    return 'bg-slate-100 text-slate-700';
  };

  return (
    <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
        {hi ? 'पंचधा मैत्री' : 'Panchadha Maitri (Compound Relations)'}
      </div>
      <table className="table-sacred w-full text-xs">
        <thead className="bg-muted/50">
          <tr>
            <th className="text-left p-1.5 text-primary font-medium">{hi ? 'ग्रह' : 'Planet'}</th>
            <th className="text-left p-1.5 text-primary font-medium">{hi ? 'अन्य' : 'With'}</th>
            <th className="text-left p-1.5 text-primary font-medium">{hi ? 'संबंध' : 'Relation'}</th>
          </tr>
        </thead>
        <tbody>
          {(data.relations as any[]).map((r: any, i: number) => (
            <tr key={i} className="border-t border-border">
              <td className="p-1.5 font-medium text-foreground">{translatePlanet(r.planet1, language)}</td>
              <td className="p-1.5 text-foreground/80">{translatePlanet(r.planet2, language)}</td>
              <td className="p-1.5">
                <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${relationColor(r.combined_relation)}`}>
                  {hi ? (r.combined_relation_hi || r.combined_relation) : r.combined_relation}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const PARAMOCHHA: Record<string, { sign: string; deg: number }> = {
  Sun:     { sign: 'Aries',      deg: 10 },
  Moon:    { sign: 'Taurus',     deg: 3  },
  Mars:    { sign: 'Capricorn',  deg: 28 },
  Mercury: { sign: 'Virgo',      deg: 15 },
  Jupiter: { sign: 'Cancer',     deg: 5  },
  Venus:   { sign: 'Pisces',     deg: 27 },
  Saturn:  { sign: 'Libra',      deg: 20 },
};

const NATURAL_BENEFICS_SET = new Set(['Jupiter', 'Venus', 'Moon', 'Mercury']);

interface PlanetsTabProps {
  planets: any[];
  result: any;
  kundliId: string;
  sidePanel: SidePanelState;
  setSidePanel: (v: SidePanelState) => void;
  handlePlanetClick: (planet: PlanetData) => void;
  handleHouseClick: (house: number, sign: string, planets: PlanetData[]) => void;
  language: string;
  t: (key: string) => string;
  HOUSE_SIGNIFICANCE: Record<number, string>;
}

function AstrologyTheorySection({ language }: { language: string }) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  const concepts = [
    {
      title: l('The 9 Planets (Grahas) — The Actors', '9 ग्रह (अभिनेता)'),
      items: [
        { name: l('Sun (Surya)', 'सूर्य'), desc: l('Represents soul, ego, father, authority, and health.', 'आत्मा, अहंकार, पिता, अधिकार और स्वास्थ्य का प्रतिनिधित्व करता है।') },
        { name: l('Moon (Chandra)', 'चंद्र'), desc: l('Represents mind, emotions, mother, and mental peace.', 'मन, भावनाओं, माता और मानसिक शांति का प्रतिनिधित्व करता है।') },
        { name: l('Mars (Mangal)', 'मंगल'), desc: l('Represents courage, energy, siblings, and land.', 'साहस, ऊर्जा, भाई-बहनों और भूमि का प्रतिनिधित्व करता है।') },
        { name: l('Mercury (Budh)', 'बुध'), desc: l('Represents intellect, communication, business, and speech.', 'बुद्धि, संचार, व्यापार और वाणी का प्रतिनिधित्व करता है।') },
        { name: l('Jupiter (Guru)', 'गुरु'), desc: l('Represents wisdom, luck, children, wealth, and spirituality.', 'ज्ञान, भाग्य, संतान, धन और आध्यात्मिकता का प्रतिनिधित्व करता है।') },
        { name: l('Venus (Shukra)', 'शुक्र'), desc: l('Represents love, luxury, marriage, beauty, and art.', 'प्रेम, विलासिता, विवाह, सुंदरता और कला का प्रतिनिधित्व करता है।') },
        { name: l('Saturn (Shani)', 'शनि'), desc: l('Represents discipline, karma, longevity, and obstacles.', 'अनुशासन, कर्म, दीर्घायु और बाधाओं का प्रतिनिधित्व करता है।') },
        { name: l('Rahu & Ketu', 'राहु और केतु'), desc: l('Shadow planets representing worldly desires and spiritual liberation.', 'साया ग्रह जो सांसारिक इच्छाओं और आध्यात्मिक मुक्ति का प्रतिनिधित्व करते हैं।') },
      ],
    },
    {
      title: l('The 12 Houses (Bhavas) — The Stage', '12 भाव (मंच)'),
      items: [
        { name: l('1st House (Lagna)', 'प्रथम भाव (लग्न)'), desc: l('Self, appearance, personality, and life path.', 'स्वयं, रूप, व्यक्तित्व और जीवन पथ।') },
        { name: l('2nd House', 'द्वितीय भाव'), desc: l('Wealth, family, speech, and early education.', 'धन, परिवार, वाणी और प्रारंभिक शिक्षा।') },
        { name: l('4th House', 'चतुर्थ भाव'), desc: l('Home, mother, happiness, and properties.', 'घर, माता, सुख और संपत्ति।') },
        { name: l('7th House', 'सप्तम भाव'), desc: l('Marriage, partnerships, and business.', 'विवाह, साझेदारी और व्यापार।') },
        { name: l('9th House', 'नवम भाव'), desc: l('Luck, dharma, father, and long travels.', 'भाग्य, धर्म, पिता और लंबी यात्राएं।') },
        { name: l('10th House', 'दशम भाव'), desc: l('Career, status, power, and social contribution.', 'करियर, प्रतिष्ठा, शक्ति और सामाजिक योगदान।') },
      ],
    },
    {
      title: l('The 12 Signs (Rashis) — The Costumes', '12 राशियां (वेशभूषा)'),
      desc: l(
        'Signs provide the "flavor" or behavior of a planet. For example, Sun in Leo (own sign) is strong and comfortable, while Sun in Libra (debilitated) is weak and uncomfortable.',
        'राशियां ग्रहों को "स्वभाव" या व्यवहार प्रदान करती हैं। उदाहरण के लिए, सिंह राशि में सूर्य (स्वराशि) मजबूत और सहज होता है, जबकि तुला राशि में सूर्य (नीच) कमजोर और असहज होता है।'
      ),
    },
    {
      title: l('27 Nakshatras — The Detail', '27 नक्षत्र (सूक्ष्म विवरण)'),
      desc: l(
        'Nakshatras provide micro-details. While a sign tells you the general behavior, the Nakshatra reveals the specific quality of the mind and destiny.',
        'नक्षत्र सूक्ष्म विवरण प्रदान करते हैं। जबकि एक राशि आपको सामान्य व्यवहार बताती है, नक्षत्र मन और भाग्य की विशिष्ट गुणवत्ता को प्रकट करता है।'
      ),
    },
  ];

  return (
    <div className="mt-8 space-y-6">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {l('How to Read Your Chart (The Theater Metaphor)', 'अपनी कुंडली कैसे पढ़ें (थिएटर रूपक)')}
        </Heading>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
            <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-2">{l('1. The Actors (Planets)', '1. अभिनेता (ग्रह)')}</h5>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l('Planets are the "Who". They represent different parts of your personality and life (Ego, Emotions, Wisdom).', 'ग्रह "कौन" हैं। वे आपके व्यक्तित्व और जीवन के विभिन्न हिस्सों (अहंकार, भावनाओं, ज्ञान) का प्रतिनिधित्व करते हैं।')}
            </p>
          </div>
          <div className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
            <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-2">{l('2. The Costumes (Signs)', '2. वेशभूषा (राशियां)')}</h5>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l('Signs are the "How". They show how a planet behaves. A strong sign makes the actor perform well; a weak one makes them struggle.', 'राशियां "कैसे" हैं। वे दिखाती हैं कि एक ग्रह कैसे व्यवहार करता है। एक मजबूत राशि अभिनेता को अच्छा प्रदर्शन करने के लिए प्रेरित करती है; एक कमजोर राशि उन्हें संघर्ष कराती है।')}
            </p>
          </div>
          <div className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
            <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-2">{l('3. The Stage (Houses)', '3. मंच (भाव)')}</h5>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l('Houses are the "Where". They represent the specific area of life where the planet’s energy will manifest (Career, Home, Marriage).', 'भाव "कहाँ" हैं। वे जीवन के उस विशिष्ट क्षेत्र का प्रतिनिधित्व करते हैं जहाँ ग्रह की ऊर्जा प्रकट होगी (करियर, घर, विवाह)।')}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {concepts.map((concept, idx) => (
            <div key={idx} className="space-y-3">
              <h4 className="text-sm font-bold text-primary flex items-center gap-2 border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
                {concept.title}
              </h4>
              {concept.items ? (
                <div className="space-y-2.5">
                  {concept.items.map((item, i) => (
                    <div key={i} className="text-xs">
                      <span className="font-bold text-sacred-gold-dark">{item.name}:</span>{' '}
                      <span className="text-foreground/70">{item.desc}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {concept.desc}
                </p>
              )}
            </div>
          ))}
        </div>

        <div className="mt-8 p-4 bg-sacred-gold-dark/[0.03] rounded-lg border border-sacred-gold/20">
          <h4 className="text-xs font-bold text-sacred-gold-dark uppercase mb-3">{l('Example: Sun in Leo in 10th House', 'उदाहरण: 10वें भाव में सिंह राशि का सूर्य')}</h4>
          <p className="text-xs text-foreground/80 leading-relaxed">
            {l(
              'If the Sun (The Actor of Authority) is in Leo (A Strong Costume) in the 10th House (The Career Stage), it means you likely have natural leadership and status in your professional life.',
              'यदि सूर्य (अधिकार का अभिनेता) 10वें भाव (करियर मंच) में सिंह राशि (एक मजबूत वेशभूषा) में है, तो इसका अर्थ है कि आपके पेशेवर जीवन में प्राकृतिक नेतृत्व और प्रतिष्ठा होने की संभावना है।'
            )}
          </p>
        </div>

        <div className="mt-6 pt-4 border-t border-sacred-gold/20">
          <p className="text-[11px] text-foreground/50 italic text-center">
            {l(
              'Note: These are general significations. A planet’s actual result in your life depends on its strength, lordship, and the aspects it receives.',
              'नोट: ये सामान्य फल हैं। आपके जीवन में ग्रह का वास्तविक परिणाम उसकी शक्ति, स्वामित्व और उस पर पड़ने वाली दृष्टियों पर निर्भर करता है।'
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function PlanetsTab({
  planets, result, kundliId, sidePanel, setSidePanel,
  handlePlanetClick, handleHouseClick,
  language, t, HOUSE_SIGNIFICANCE,
}: PlanetsTabProps) {
  const SIGNS_ORDER = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];

  const toPlanetEntry = (p: any): PlanetEntry => ({
    planet: p.planet,
    sign: p.sign || p.current_sign || '',
    sign_degree: Number(p.sign_degree ?? p.degree ?? 0) || 0,
    status: typeof p.status === 'string' ? p.status : '',
    is_retrograde: !!p.is_retrograde,
    is_combust: !!p.is_combust,
    is_vargottama: !!p.is_vargottama,
    is_exalted: !!p.is_exalted,
    is_debilitated: !!p.is_debilitated,
  } as any);

  const ascSign =
    String(result?.chart_data?.ascendant?.sign || '').trim()
    || String(planets.find((p: any) => p.planet === 'Lagna' || p.planet === 'Ascendant')?.sign || '').trim()
    || SIGNS_ORDER[0];

  return (
    <div className="space-y-4">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {language === 'hi' ? 'ग्रह' : 'Planets'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {language === 'hi'
            ? 'यहाँ ग्रहों की स्थिति, राशि/भाव, नक्षत्र और दृष्टि दिखती है। चार्ट/तालिका में किसी ग्रह या भाव पर क्लिक करके तुरंत विवरण देखें।'
            : 'See planetary placements with sign/house, nakshatra, and aspects. Click any planet or house in the chart/table for instant details.'}
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
      {/* Kundli Chart (Report-style SVG) */}
      <div className="xl:col-span-1">
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.chart')}
          </div>
          <div className="p-3 flex justify-center">
            <div className="w-full max-w-[460px] xl:max-w-[380px] aspect-square">
              <KundliChartSVG
                planets={planets.map(toPlanetEntry)}
                ascendantSign={ascSign}
                language={language}
                className="w-full h-full"
                showHouseNumbers={false}
                showRashiNumbers
                rashiNumberPlacement="corner"
                showAscendantMarker={false}
                onPlanetClick={(pl) => handlePlanetClick(pl as any)}
                onHouseClick={(house, sign, housePlanets) => handleHouseClick(house, sign, housePlanets as any)}
              />
            </div>
          </div>
          <p className="text-xs text-muted-foreground text-center pb-3">
            {t('kundli.clickInfo')}
          </p>
        </div>
      </div>

      {/* Side Panel + Table */}
      <div className="xl:col-span-2 min-w-0 space-y-6">
        {sidePanel ? (
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden animate-in fade-in slide-in-from-right-4 duration-300">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
            <span>
              {sidePanel.type === 'planet'
                ? `${translatePlanet(sidePanel.planet?.planet || '', language)}${(sidePanel.planet?.status || '').toLowerCase().includes('retrograde') ? ' (R)' : ''} — ${t('kundli.details')}`
                : t('kundli.houseDetails')}
            </span>
              <button
                onClick={() => setSidePanel(null)}
                className="text-white/90 hover:text-white transition-colors"
                aria-label={t('common.close')}
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="p-4 max-h-[420px] overflow-auto">

            {sidePanel.type === 'planet' && sidePanel.planet && (() => {
              const p = sidePanel.planet;
              const status = p.status?.toLowerCase() || '';
              const pmo = PARAMOCHHA[p.planet];
              const isParamochha = !!pmo && p.sign === pmo.sign && p.sign_degree != null && Math.abs(p.sign_degree - pmo.deg) <= 1;
              const strengthLabel = isParamochha
                ? 'Paramochha ★'
                : status.includes('exalted') ? 'Exalted' : status.includes('debilitated') ? 'Debilitated' : status.includes('own') ? 'Own Sign' : p.status || t('kundli.transit');
              const strengthColor = isParamochha
                ? 'text-yellow-600 font-bold'
                : status.includes('exalted') ? 'text-green-500' : status.includes('debilitated') ? 'text-red-500' : status.includes('own') ? 'text-blue-500' : 'text-foreground';
              const moonAspectors = p.planet === 'Moon'
                ? planets.filter(op =>
                    op.planet !== 'Moon' &&
                    (PLANET_ASPECTS[op.planet] || [7]).some(offset =>
                      ((op.house - 1 + offset) % 12) + 1 === p.house
                    )
                  )
                : [];
              const aspects = (PLANET_ASPECTS[p.planet] || [7]).map((offset) => {
                const targetHouse = ((p.house - 1 + offset) % 12) + 1;
                return `${t('table.house')} ${targetHouse}`;
              });

              return (
                <div className="space-y-3">
                  <p className="text-xs text-muted-foreground">
                    {language === 'hi'
                      ? 'यह ग्रह किस राशि में है, किस भाव में बैठा है, और कौन-कौन से भावों पर दृष्टि डाल रहा है — उससे फल तय होता है।'
                      : 'Results depend on the planet’s sign, house placement, and the houses it aspects.'}
                  </p>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-card rounded-lg p-3 border border-sacred-gold/20">
                      <p className="text-xs text-muted-foreground">{t('kundli.sign')}</p>
                      <p className="font-semibold text-foreground">{translateSign(p.sign, language)}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3 border border-sacred-gold/20">
                      <p className="text-xs text-muted-foreground">{t('kundli.degree')}</p>
                      <p className="font-semibold text-foreground">{p.sign_degree != null ? toDMS(p.sign_degree) : '\u2014'}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3 border border-sacred-gold/20">
                      <p className="text-xs text-muted-foreground">{t('kundli.house')}</p>
                      <p className="font-semibold text-foreground">{p.house}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3 border border-sacred-gold/20">
                      <p className="text-xs text-muted-foreground">{t('kundli.nakshatra')}</p>
                      <p className="font-semibold text-foreground">
                        {translateNakshatra(p.nakshatra, language) || t('common.noData')}
                        {p.nakshatra_pada ? ` (${t('auto.pada')} ${p.nakshatra_pada})` : ''}
                      </p>
                    </div>
                  </div>
                  <div className="bg-card rounded-lg p-3 border border-sacred-gold/20">
                    <p className="text-xs text-muted-foreground">{t('kundli.strength')}</p>
                    <p className={`font-semibold ${strengthColor}`}>{translateLabel(strengthLabel, language)}</p>
                    {isParamochha && (
                      <div className="text-[10px] text-yellow-600 italic mt-0.5">
                        <SlokaHover slokaRef="Phaladeepika Adh. 1" language={language}>
                          {language === 'hi' ? 'परमोच्च — अधिकतम उच्च बल' : 'Paramochha — maximum exaltation degree (Phaladeepika Adh. 1)'}
                        </SlokaHover>
                      </div>
                    )}
                  </div>
                  <div className="bg-card rounded-lg p-3 border border-sacred-gold/20">
                    <p className="text-xs text-muted-foreground">{t('kundli.aspects')}</p>
                    <p className="font-semibold text-foreground text-sm">{aspects.join(', ')}</p>
                  </div>
                  {moonAspectors.length > 0 && (
                    <div className="bg-card rounded-lg p-3 border border-sacred-gold/20 col-span-2">
                      <div className="text-xs text-muted-foreground mb-2">
                        <SlokaHover slokaRef="Phaladeepika Adh. 18" language={language}>
                          {language === 'hi' ? 'चन्द्र पर ग्रह-दृष्टि (फलदीपिका अ. 18)' : 'Planets aspecting Moon (Phaladeepika Adh. 18)'}
                        </SlokaHover>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {moonAspectors.map(op => {
                          const isBen = NATURAL_BENEFICS_SET.has(op.planet);
                          return (
                            <span key={op.planet} className={`text-[10px] font-semibold px-2 py-0.5 rounded ${isBen ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
                              {translatePlanet(op.planet, language)} {isBen ? '✦' : '✗'}
                            </span>
                          );
                        })}
                      </div>
                    </div>
                  )}
                  <div className="bg-card rounded-lg p-3 border border-sacred-gold/20">
                    <p className="text-xs text-muted-foreground">{t('kundli.housePlacement')}</p>
                    <p className="text-sm text-foreground/90">
                      {translatePlanet(p.planet, language)} — {t('kundli.house')} {p.house} ({HOUSE_SIGNIFICANCE[p.house] || t('common.noData')})
                    </p>
                  </div>
                </div>
              );
            })()}

            {sidePanel.type === 'house' && (
              <div className="space-y-2">
                <div className="grid grid-cols-3 gap-2">
                  <div className="bg-card rounded-lg p-2.5 border border-sacred-gold/20">
                    <p className="text-xs text-muted-foreground">{t('kundli.houseNumber')}</p>
                    <p className="font-semibold text-foreground">{sidePanel.house}</p>
                  </div>
                  <div className="bg-card rounded-lg p-2.5 border border-sacred-gold/20">
                    <p className="text-xs text-muted-foreground">{t('kundli.sign')}</p>
                    <p className="font-semibold text-foreground">{translateSign(sidePanel.sign || '', language)}</p>
                  </div>
                  <div className="bg-card rounded-lg p-2.5 border border-sacred-gold/20">
                    <p className="text-xs text-muted-foreground">{t('kundli.significance')}</p>
                    <p className="text-sm font-semibold text-foreground leading-snug">
                      {HOUSE_SIGNIFICANCE[sidePanel.house || 0] || t('common.noData')}
                    </p>
                  </div>
                </div>
                <div className="bg-card rounded-lg p-2.5 border border-sacred-gold/20">
                  <p className="text-xs text-muted-foreground mb-1">
                    {t('kundli.planetsInHouse')} <span className="font-semibold text-foreground/70">({(sidePanel.planets || []).length})</span>
                  </p>
                  {(sidePanel.planets || []).length > 0 ? (
                    <div className="flex flex-wrap gap-1.5">
                      {(sidePanel.planets || []).map((p) => (
                        <button
                          key={p.planet}
                          className="px-2 py-1 rounded-full border border-border bg-muted/20 hover:bg-muted/40 text-xs text-foreground transition-colors"
                          onClick={() => setSidePanel({ type: 'planet', planet: p })}
                        >
                          {translatePlanet(p.planet, language)}{(p.status || '').toLowerCase().includes('retrograde') ? '*' : ''}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-foreground">{t('kundli.noPlanets')}</p>
                  )}
                </div>
              </div>
            )}
            </div>
          </div>
        ) : (
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
              {t('kundli.details')}
            </div>
            <div className="p-8 flex flex-col items-center justify-center min-h-[200px]">
              <Sparkles className="w-8 h-8 text-primary mb-3" />
              <p className="text-foreground text-sm text-center">
                {t('kundli.clickInfo')}
              </p>
            </div>
          </div>
        )}

        {/* Planet table */}
        <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('section.detailedPlanetPositions')}
          </div>
          <Table className="w-full text-xs">
            <TableHeader className="bg-muted/40">
              <TableRow>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.house')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.status')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planets.map((planet: any, index: number) => (
                <TableRow
                  key={index}
                  className={`border-t border-border cursor-pointer transition-colors ${
                    sidePanel?.type === 'planet' && sidePanel.planet?.planet === planet.planet
                      ? 'bg-sacred-gold/10'
                      : 'hover:bg-sacred-gold/[0.04]'
                  }`}
                  onClick={() => handlePlanetClick(planet)}
                >
                  <TableCell className="p-1.5 text-foreground font-medium">
                    {translatePlanet(planet.planet, language)}
                    {(planet.status || '').toLowerCase().includes('retrograde') && <span className="text-red-500 ml-0.5" title={t('kundli.retrograde')}>*</span>}
                  </TableCell>
                  <TableCell className="p-1.5 text-foreground">{translateSign(planet.sign, language)}</TableCell>
                  <TableCell className="p-1.5 text-foreground">{planet.house}</TableCell>
                  <TableCell className="p-1.5 text-foreground">
                    {translateNakshatra(planet.nakshatra, language) || '\u2014'}
                    {planet.nakshatra_pada ? ` (${t('auto.p')}${planet.nakshatra_pada})` : ''}
                  </TableCell>
                  <TableCell className="p-1.5">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-100 text-green-800' : 'bg-card text-foreground'}`}>
                      {translateLabel(planet.status, language)}
                    </span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {/* Planet Properties & Panchadha Maitri */}
        {kundliId && <PlanetPropertiesSection kundliId={kundliId} language={language} />}
        {kundliId && <PanchadhaMaitriSection kundliId={kundliId} language={language} />}
      </div>
      </div>

      {/* Astrology Theory Section — General educational summary */}
      <AstrologyTheorySection language={language} />
    </div>
  );
}
