import { useEffect, useMemo, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Calendar, AlertTriangle, Shield, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';

interface SankrantiRow {
  rashi_index: number;
  rashi: string;
  rashi_hindi: string;
  ingress_utc: string;
  ingress_local: string;
  restriction_window: {
    start_local: string;
    end_local: string;
    hours_before: number;
    hours_after: number;
  };
  punyakaal?: {
    start_local: string;
    end_local: string;
    heuristic: boolean;
    note_en?: string;
    note_hi?: string;
  };
  sankranti_type?: {
    name_en: string;
    name_hi: string;
    day_en: string;
    day_hi: string;
    description_en: string;
    description_hi: string;
  };
  amritkaal?: {
    start_local: string;
    end_local: string;
    duration_minutes: number;
    is_classical: boolean;
    note_en?: string;
  };
  ayana?: {
    ayana_en: string;
    ayana_hi: string;
    note_en: string;
    note_hi: string;
  };
  makar_special?: {
    uttarayan_en: string;
    uttarayan_hi: string;
    mela_note_en: string;
    mela_note_hi: string;
  };
  sign_effects?: {
    effect_en: string;
    effect_hi: string;
  };
}

interface SankrantiPayload {
  year: number;
  tz_offset_hours: number;
  ordered_from_mesha: boolean;
  sankrantis: SankrantiRow[];
}

interface Props {
  language: string;
  t: (key: string) => string;
  latitude: number;
  longitude: number;
  selectedDate: string;
}

export default function SankrantiTab({ language, t, latitude, longitude, selectedDate }: Props) {
  const initialYear = useMemo(() => {
    const d = new Date(selectedDate);
    return Number.isFinite(d.getTime()) ? d.getFullYear() : new Date().getFullYear();
  }, [selectedDate]);

  const [year, setYear] = useState<number>(initialYear);
  const [data, setData] = useState<SankrantiPayload | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => setYear(initialYear), [initialYear]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api.get(`/api/panchang/sankranti?year=${year}&latitude=${latitude}&longitude=${longitude}`)
      .then((res: any) => {
        if (cancelled) return;
        const payload = (res?.data ?? res) as SankrantiPayload;
        setData(payload && Array.isArray(payload.sankrantis) ? payload : null);
      })
      .catch(() => { if (!cancelled) setData(null); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [year, latitude, longitude]);

  const rows = data?.sankrantis || [];

  return (
    <div className="space-y-6">
      <Card className="card-sacred border-sacred-gold/30">
        <CardContent className="p-4">
          <div className="flex items-start justify-between gap-3 flex-wrap">
            <div className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-sacred-gold" />
              <h3 className="text-lg font-bold text-foreground">
                {language === 'hi' ? 'संक्रांति (सूर्य-राशि प्रवेश)' : 'Sankranti (Sun Ingress)'}
              </h3>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                className="px-3 py-1.5 rounded-lg border bg-card/50 hover:bg-card transition text-sm"
                onClick={() => setYear((y) => Math.max(1900, y - 1))}
              >
                {language === 'hi' ? 'पिछला' : 'Prev'}
              </button>
              <div className="px-3 py-1.5 rounded-lg border bg-card/50 text-sm font-semibold">
                {year}
              </div>
              <button
                type="button"
                className="px-3 py-1.5 rounded-lg border bg-card/50 hover:bg-card transition text-sm"
                onClick={() => setYear((y) => Math.min(2100, y + 1))}
              >
                {language === 'hi' ? 'अगला' : 'Next'}
              </button>
            </div>
          </div>

          <div className="mt-4 flex items-start gap-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <AlertTriangle className="h-5 w-5 text-amber-600 mt-0.5" />
            <div className="text-sm text-foreground/80">
              <div className="font-semibold">
                {language === 'hi' ? 'संक्रांति के आसपास 16+16 घंटे वर्जित' : 'Avoid major ceremonies ±16 hours around Sankranti'}
              </div>
              <div className="text-xs text-muted-foreground mt-0.5">
                {language === 'hi'
                  ? 'यह सूची API से गणना की गई है। पुण्यकाल अभी heuristic है; शास्त्रीय प्रहर-आधारित नियम P2 में आएँगे।'
                  : 'This list is computed by the API. Punyakaal is currently heuristic; classical prahar-based rules are pending (P2).'}
              </div>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin h-8 w-8 border-2 border-sacred-gold border-t-transparent rounded-full mx-auto" />
            </div>
          ) : rows.length === 0 ? (
            <div className="text-center py-10 text-muted-foreground">
              {t('auto.noDataAvailable')}
            </div>
          ) : (
            <div className="mt-4 rounded-xl border overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{language === 'hi' ? 'राशि' : 'Rashi'}</TableHead>
                    <TableHead>{language === 'hi' ? 'प्रवेश (स्थानीय)' : 'Ingress (Local)'}</TableHead>
                    <TableHead>{language === 'hi' ? 'वर्जित विंडो' : 'Restriction Window'}</TableHead>
                    <TableHead className="hidden md:table-cell">{language === 'hi' ? 'पुण्यकाल' : 'Punyakaal'}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rows.map((r) => {
                    const rashiName = language === 'hi' ? (r.rashi_hindi || r.rashi) : (r.rashi || r.rashi_hindi);
                    const puny = r.punyakaal;
                    const sType = r.sankranti_type;
                    const amrit = r.amritkaal;
                    const ayana = r.ayana;
                    const makar = r.makar_special;
                    const fx = r.sign_effects;
                    return (
                      <TableRow key={`${r.rashi_index}-${r.ingress_utc}`}>
                        <TableCell className="font-semibold">
                          <div className="flex items-center gap-2 flex-wrap">
                            <Sparkles className="h-4 w-4 text-sacred-gold shrink-0" />
                            {rashiName}
                            {sType && (
                              <span className="text-[10px] px-2 py-0.5 rounded-full bg-sacred-gold/15 text-sacred-gold border border-sacred-gold/30 font-medium">
                                {language === 'hi' ? sType.name_hi : sType.name_en}
                              </span>
                            )}
                          </div>
                          {fx && (
                            <div className="text-[11px] italic text-muted-foreground mt-1">
                              {language === 'hi' ? fx.effect_hi : fx.effect_en}
                            </div>
                          )}
                        </TableCell>
                        <TableCell>
                          <div className="text-sm">{r.ingress_local}</div>
                          <div className="text-[11px] text-muted-foreground">UTC: {r.ingress_utc}</div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Shield className="h-4 w-4 text-red-600" />
                            <div className="text-sm">
                              {r.restriction_window.start_local} → {r.restriction_window.end_local}
                            </div>
                          </div>
                          <div className="text-[11px] text-muted-foreground">
                            {language === 'hi'
                              ? `${r.restriction_window.hours_before}+${r.restriction_window.hours_after} घंटे`
                              : `${r.restriction_window.hours_before}+${r.restriction_window.hours_after} hours`}
                          </div>
                        </TableCell>
                        <TableCell className="hidden md:table-cell">
                          {puny ? (
                            <div className="text-sm">
                              <div>
                                {puny.start_local} → {puny.end_local}{' '}
                                {puny.heuristic && (
                                  <span className="ml-2 text-[10px] px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-700 border border-amber-500/20">
                                    {language === 'hi' ? 'अनुमानित' : 'Heuristic'}
                                  </span>
                                )}
                              </div>
                              {(puny.note_hi || puny.note_en) && (
                                <div className="text-[11px] text-muted-foreground mt-0.5">
                                  {language === 'hi' ? (puny.note_hi || puny.note_en) : (puny.note_en || puny.note_hi)}
                                </div>
                              )}
                            </div>
                          ) : (
                            <span className="text-sm text-muted-foreground">—</span>
                          )}
                          {amrit && (
                            <div className="mt-2 text-[11px] text-foreground/80">
                              <span className="font-semibold text-emerald-700">
                                {language === 'hi' ? 'अमृतकाल:' : 'Amritkaal:'}
                              </span>{' '}
                              {amrit.start_local} → {amrit.end_local}
                              {amrit.note_en && (
                                <span className="ml-1 text-muted-foreground">({amrit.note_en})</span>
                              )}
                            </div>
                          )}
                          {ayana && (
                            <div className="mt-1.5 text-[11px] text-blue-700/80">
                              {language === 'hi' ? ayana.ayana_hi : ayana.ayana_en}
                            </div>
                          )}
                          {makar && (
                            <div className="mt-1.5 text-[11px] px-2 py-1 rounded-lg bg-sacred-gold/10 border border-sacred-gold/25 text-foreground/80">
                              {language === 'hi' ? makar.uttarayan_hi : makar.uttarayan_en}
                            </div>
                          )}
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

