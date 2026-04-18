/**
 * P2.12 — Calculation Detail Panel.
 *
 * Shows the raw calculation steps (degrees, ayanamsa, house-lord,
 * step-by-step derivations) so a professional astrologer can verify
 * the software against a manual ephemeris lookup.
 *
 * Fetches GET /api/lalkitab/calculation-details/{kundliId} and
 * renders an accordion with copyable JSON per section.
 */

import { useEffect, useState, useMemo } from 'react';
import { api } from '@/lib/api';
import SourceBadge, { type SourceValue } from './SourceBadge';
import {
  Copy, Check, ChevronDown, Loader2, X,
  FileJson, ScanSearch,
} from 'lucide-react';

interface Props {
  kundliId: string;
  visible: boolean;
  onToggle: () => void;
  isHi?: boolean;
}

interface PlanetRow {
  planet: string;
  longitude: number | null;
  sign: string;
  sign_degree: number | null;
  dms: string | null;
  deg: number | null;
  min: number | null;
  sec: number | null;
  nakshatra: string | null;
  nakshatra_pada: number | null;
  vedic_house: number | null;
  lk_house: number;
  retrograde: boolean;
  is_combust: boolean;
  is_vargottama: boolean;
  is_sandhi: boolean;
  status: string;
}

interface CalcDetail {
  kundli_id: string;
  birth_date: string;
  birth_time: string;
  ayanamsa: { system: string; value_degrees: number | null; sidereal_offset_dms: string | null; note_en: string; note_hi: string; source: SourceValue };
  ascendant: { longitude: number | null; sign: string | null; sign_degree: number | null; dms: string | null; note_en: string; note_hi: string; source: SourceValue };
  planets: PlanetRow[];
  houses: Record<string, { sign: string; planets: string[] }>;
  bunyaad: any;
  takkar: any;
  masnui: any;
  aspects: any;
  friend_tables: Record<string, { pakka_ghar: number; bunyaad_house: number; friends: string[]; enemies: string[] }>;
  source_references: Record<string, { source: SourceValue; note_en: string; note_hi: string }>;
  source: SourceValue;
}

function CopyButton({ payload, isHi }: { payload: any; isHi: boolean }) {
  const [copied, setCopied] = useState(false);
  const onCopy = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* no-op */
    }
  };
  return (
    <button
      type="button"
      onClick={onCopy}
      className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded border border-border text-muted-foreground hover:bg-foreground/5"
      title={isHi ? 'JSON कॉपी करें' : 'Copy JSON'}
    >
      {copied ? <Check className="w-3 h-3 text-green-600" /> : <Copy className="w-3 h-3" />}
      {copied ? (isHi ? 'कॉपी हुआ' : 'Copied') : (isHi ? 'कॉपी' : 'Copy')}
    </button>
  );
}

function Section({
  title_en, title_hi, sourceRef, isHi, data, children, defaultOpen,
}: {
  title_en: string;
  title_hi: string;
  sourceRef?: { source: SourceValue; note_en: string; note_hi: string };
  isHi: boolean;
  data: any;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  return (
    <details open={defaultOpen} className="rounded-xl border border-border bg-background overflow-hidden">
      <summary className="cursor-pointer px-3 py-2 flex items-center gap-2 hover:bg-foreground/5">
        <ChevronDown className="w-3.5 h-3.5 text-muted-foreground transition-transform [details[open]_&]:rotate-180" />
        <span className="text-sm font-semibold text-foreground">
          {isHi ? title_hi : title_en}
        </span>
        {sourceRef && <SourceBadge source={sourceRef.source} size="xs" />}
        <span className="ml-auto flex items-center gap-2">
          <CopyButton payload={data} isHi={isHi} />
        </span>
      </summary>
      <div className="p-3 border-t border-border">
        {sourceRef && (
          <p className="text-[11px] text-muted-foreground mb-2 italic">
            {isHi ? sourceRef.note_hi : sourceRef.note_en}
          </p>
        )}
        {children}
      </div>
    </details>
  );
}

export default function CalculationDetailPanel({ kundliId, visible, onToggle, isHi: propIsHi }: Props) {
  const [data, setData] = useState<CalcDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isHi = Boolean(propIsHi);

  useEffect(() => {
    if (!visible || !kundliId || data) return;
    setLoading(true);
    setError(null);
    api.get(`/api/lalkitab/calculation-details/${kundliId}`)
      .then((res: any) => setData(res as CalcDetail))
      .catch((e: any) => {
        setError(e?.message || (isHi ? 'विवरण लोड नहीं हुआ' : 'Could not load details'));
      })
      .finally(() => setLoading(false));
  }, [visible, kundliId, data, isHi]);

  const refs = data?.source_references ?? ({} as CalcDetail['source_references']);

  const fullJson = useMemo(() => data ?? {}, [data]);

  if (!visible) return null;

  return (
    <div className="rounded-xl border-2 border-sacred-gold/40 bg-card">
      <div className="flex items-center gap-3 px-4 py-3 border-b border-sacred-gold/20 bg-sacred-gold/5">
        <ScanSearch className="w-5 h-5 text-sacred-gold" />
        <div className="flex-1">
          <h3 className="font-semibold text-sacred-gold text-sm">
            {isHi ? 'गणना विवरण (व्यावसायिक सत्यापन)' : 'Calculation Details (Professional Verification)'}
          </h3>
          <p className="text-xs text-muted-foreground">
            {isHi
              ? 'पंडित या सॉफ़्टवेयर ऑडिटर के लिए — प्रत्येक गणना का कच्चा डेटा और स्रोत टैग।'
              : 'For pandits or software auditors — raw values, source tags, and step-by-step derivations.'}
          </p>
        </div>
        {data && <CopyButton payload={fullJson} isHi={isHi} />}
        <button
          type="button"
          aria-label={isHi ? 'बंद करें' : 'Close'}
          onClick={onToggle}
          className="p-1 rounded-full hover:bg-foreground/10"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="p-4 space-y-3">
        {loading && (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-5 h-5 animate-spin text-sacred-gold mr-2" />
            <span className="text-sm text-muted-foreground">
              {isHi ? 'विवरण लोड हो रहा है...' : 'Loading details...'}
            </span>
          </div>
        )}

        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {data && (
          <>
            {/* Ayanamsa */}
            <Section
              title_en="Ayanamsa & Sidereal Offset"
              title_hi="अयनांश एवं सायन ऑफसेट"
              sourceRef={refs.ayanamsa}
              isHi={isHi}
              data={data.ayanamsa}
              defaultOpen
            >
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <div className="text-xs text-muted-foreground">{isHi ? 'प्रणाली' : 'System'}</div>
                  <div className="font-mono text-foreground">{data.ayanamsa.system}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">{isHi ? 'मान (डिग्री)' : 'Value (deg)'}</div>
                  <div className="font-mono text-foreground">{data.ayanamsa.value_degrees ?? '—'}</div>
                </div>
                <div className="col-span-2">
                  <div className="text-xs text-muted-foreground">{isHi ? 'सायन ऑफसेट' : 'Sidereal offset (DMS)'}</div>
                  <div className="font-mono text-foreground">{data.ayanamsa.sidereal_offset_dms ?? '—'}</div>
                </div>
              </div>
            </Section>

            {/* Ascendant */}
            <Section
              title_en="Ascendant (for reference)"
              title_hi="लग्न (संदर्भ हेतु)"
              sourceRef={refs.planet_longitudes}
              isHi={isHi}
              data={data.ascendant}
            >
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <div className="text-xs text-muted-foreground">{isHi ? 'राशि' : 'Sign'}</div>
                  <div className="font-mono text-foreground">{data.ascendant.sign ?? '—'}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">{isHi ? 'देशांतर' : 'Longitude'}</div>
                  <div className="font-mono text-foreground">{data.ascendant.longitude ?? '—'}</div>
                </div>
                <div className="col-span-2">
                  <div className="text-xs text-muted-foreground">DMS</div>
                  <div className="font-mono text-foreground">{data.ascendant.dms ?? '—'}</div>
                </div>
              </div>
            </Section>

            {/* Planet longitudes */}
            <Section
              title_en="Planet Longitudes (Sidereal)"
              title_hi="ग्रह देशांतर (सायन)"
              sourceRef={refs.planet_longitudes}
              isHi={isHi}
              data={data.planets}
              defaultOpen
            >
              <div className="overflow-x-auto">
                <table className="w-full text-xs border-collapse">
                  <thead>
                    <tr className="bg-foreground/5 text-foreground">
                      <th className="text-left p-1.5">{isHi ? 'ग्रह' : 'Planet'}</th>
                      <th className="text-left p-1.5">DMS</th>
                      <th className="text-left p-1.5">{isHi ? 'राशि' : 'Sign'}</th>
                      <th className="text-left p-1.5">{isHi ? 'नक्षत्र' : 'Nakshatra'}</th>
                      <th className="text-center p-1.5">{isHi ? 'पाद' : 'Pada'}</th>
                      <th className="text-center p-1.5">LK H</th>
                      <th className="text-center p-1.5">{isHi ? 'स्थिति' : 'Flags'}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.planets.map((p) => (
                      <tr key={p.planet} className="border-t border-border">
                        <td className="p-1.5 font-semibold">{p.planet}</td>
                        <td className="p-1.5 font-mono">{p.dms ?? '—'}</td>
                        <td className="p-1.5">{p.sign || '—'}</td>
                        <td className="p-1.5">{p.nakshatra ?? '—'}</td>
                        <td className="p-1.5 text-center">{p.nakshatra_pada ?? '—'}</td>
                        <td className="p-1.5 text-center font-mono">{p.lk_house || '—'}</td>
                        <td className="p-1.5 text-center text-[10px]">
                          {p.retrograde && <span className="mr-1 text-amber-600">R</span>}
                          {p.is_combust && <span className="mr-1 text-red-600">C</span>}
                          {p.is_vargottama && <span className="mr-1 text-green-700">V</span>}
                          {p.is_sandhi && <span className="mr-1 text-purple-600">S</span>}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-[10px] text-muted-foreground mt-2">
                R = {isHi ? 'वक्री' : 'Retrograde'} · C = {isHi ? 'अस्त' : 'Combust'} · V = Vargottama · S = Sandhi
              </p>
            </Section>

            {/* LK Houses */}
            <Section
              title_en="LK Fixed Houses (Aries=H1)"
              title_hi="लाल किताब स्थिर भाव (मेष=H1)"
              sourceRef={refs.lk_houses}
              isHi={isHi}
              data={data.houses}
            >
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                {Object.entries(data.houses).map(([hNum, h]) => (
                  <div key={hNum} className="rounded border border-border p-2">
                    <div className="font-semibold text-foreground">H{hNum} · {h.sign}</div>
                    <div className="text-muted-foreground">
                      {h.planets.length ? h.planets.join(', ') : (isHi ? '— खाली —' : '— empty —')}
                    </div>
                  </div>
                ))}
              </div>
            </Section>

            {/* Friend/Enemy tables + Bunyaad */}
            <Section
              title_en="Bunyaad (Foundation) — Friend/Enemy Resolution"
              title_hi="बुनियाद — मित्र/शत्रु व्याख्या"
              sourceRef={refs.bunyaad}
              isHi={isHi}
              data={{ friend_tables: data.friend_tables, bunyaad: data.bunyaad }}
            >
              <p className="text-xs text-muted-foreground mb-2">
                {isHi
                  ? 'प्रत्येक ग्रह की बुनियाद = पक्का घर से 9वाँ। उस भाव में मित्र/शत्रु की गणना देखिए।'
                  : 'Each planet\u2019s bunyaad = 9th house from its pakka ghar. See which friends/enemies occupy that house.'}
              </p>
              <div className="overflow-x-auto">
                <table className="w-full text-xs border-collapse">
                  <thead>
                    <tr className="bg-foreground/5">
                      <th className="text-left p-1.5">{isHi ? 'ग्रह' : 'Planet'}</th>
                      <th className="text-center p-1.5">{isHi ? 'पक्का घर' : 'Pakka Ghar'}</th>
                      <th className="text-center p-1.5">{isHi ? 'बुनियाद' : 'Bunyaad H'}</th>
                      <th className="text-left p-1.5">{isHi ? 'मित्र' : 'Friends'}</th>
                      <th className="text-left p-1.5">{isHi ? 'शत्रु' : 'Enemies'}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(data.friend_tables).map(([planet, t]) => (
                      <tr key={planet} className="border-t border-border">
                        <td className="p-1.5 font-semibold">{planet}</td>
                        <td className="p-1.5 text-center font-mono">{t.pakka_ghar}</td>
                        <td className="p-1.5 text-center font-mono">{t.bunyaad_house}</td>
                        <td className="p-1.5 text-green-700">{t.friends.join(', ') || '—'}</td>
                        <td className="p-1.5 text-red-700">{t.enemies.join(', ') || '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <details className="mt-3">
                <summary className="text-xs font-semibold cursor-pointer text-sacred-gold">
                  {isHi ? 'पूरा बुनियाद परिणाम (JSON)' : 'Full bunyaad result (JSON)'}
                </summary>
                <pre className="mt-2 max-h-64 overflow-auto text-[10px] bg-foreground/5 p-2 rounded">
                  {JSON.stringify(data.bunyaad, null, 2)}
                </pre>
              </details>
            </Section>

            {/* Takkar */}
            <Section
              title_en="Takkar (Axis Confrontations)"
              title_hi="टकराव (अक्ष)"
              sourceRef={refs.takkar}
              isHi={isHi}
              data={data.takkar}
            >
              <pre className="max-h-64 overflow-auto text-[10px] bg-foreground/5 p-2 rounded">
                {JSON.stringify(data.takkar, null, 2)}
              </pre>
            </Section>

            {/* Masnui */}
            <Section
              title_en="Masnui (Artificial Planets)"
              title_hi="मसनूई (कृत्रिम ग्रह)"
              sourceRef={refs.masnui}
              isHi={isHi}
              data={data.masnui}
            >
              <pre className="max-h-64 overflow-auto text-[10px] bg-foreground/5 p-2 rounded">
                {JSON.stringify(data.masnui, null, 2)}
              </pre>
            </Section>

            {/* Aspects */}
            <Section
              title_en="LK Aspects"
              title_hi="लाल किताब दृष्टि"
              sourceRef={refs.aspects}
              isHi={isHi}
              data={data.aspects}
            >
              <pre className="max-h-64 overflow-auto text-[10px] bg-foreground/5 p-2 rounded">
                {JSON.stringify(data.aspects, null, 2)}
              </pre>
            </Section>

            {/* Source references summary */}
            <Section
              title_en="Source References (provenance tags)"
              title_hi="स्रोत संदर्भ (प्रमाणिकता टैग)"
              isHi={isHi}
              data={data.source_references}
            >
              <div className="space-y-1.5 text-xs">
                {Object.entries(data.source_references).map(([key, v]) => (
                  <div key={key} className="flex items-center gap-2 flex-wrap">
                    <FileJson className="w-3 h-3 text-muted-foreground" />
                    <span className="font-mono text-foreground">{key}</span>
                    <SourceBadge source={v.source} size="xs" />
                    <span className="text-muted-foreground">
                      — {isHi ? v.note_hi : v.note_en}
                    </span>
                  </div>
                ))}
              </div>
            </Section>
          </>
        )}
      </div>
    </div>
  );
}
