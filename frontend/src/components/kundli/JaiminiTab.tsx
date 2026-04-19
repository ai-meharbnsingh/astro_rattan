import { Loader2, Star, Crown, Eye, Clock, Wallet, ChevronDown, ChevronRight, Sparkles } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateBackend } from '@/lib/backend-translations';
import { useState, Fragment } from 'react';

interface JaiminiTabProps {
  data: any;
  loading: boolean;
}

const thL = 'p-2 text-left   text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const thC = 'p-2 text-center text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdL = 'p-2 text-xs text-foreground border-t border-border';
const tdC = 'p-2 text-xs text-foreground border-t border-border text-center';

const SPECIAL_LAGNAS = [
  { key: 'arudha_lagna',   icon: Star,   title_en: 'Arudha Lagna (AL)',  title_hi: 'आरूढ़ लग्न',   desc_en: 'How the world perceives you',     desc_hi: 'संसार आपको कैसे देखता है' },
  { key: 'upapada_lagna',  icon: Eye,    title_en: 'Upapada Lagna (UL)', title_hi: 'उपपद लग्न',   desc_en: 'Marriage & spouse indicator',     desc_hi: 'विवाह और जीवनसाथी सूचक' },
  { key: 'karakamsha',     icon: Crown,  title_en: 'Karakamsha',         title_hi: 'कारकांश',      desc_en: "Soul's journey (AK in D9)",       desc_hi: 'आत्मा की यात्रा (AK नवांश में)' },
  { key: 'hora_lagna',     icon: Wallet, title_en: 'Hora Lagna',         title_hi: 'होरा लग्न',    desc_en: 'Wealth & financial status',       desc_hi: 'धन और आर्थिक स्थिति' },
  { key: 'ghatika_lagna',  icon: Clock,  title_en: 'Ghatika Lagna',      title_hi: 'घटिका लग्न',   desc_en: 'Power, authority & social status',desc_hi: 'शक्ति, अधिकार और सामाजिक स्थिति' },
  { key: 'varnada_lagna',  icon: Star,   title_en: 'Varnada Lagna',      title_hi: 'वर्णद लग्न',   desc_en: 'Purpose & dharmic calling',       desc_hi: 'उद्देश्य और धार्मिक कर्तव्य' },
];

export default function JaiminiTab({ data, loading }: JaiminiTabProps) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const [expandedDasha, setExpandedDasha] = useState<number | null>(null);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('common.loading')}</span>
      </div>
    );
  }

  if (!data) return <p className="text-center text-foreground py-8">{t('common.noData')}</p>;

  return (
    <div className="space-y-6">

      {/* Chara Karakas */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
          <Crown className="w-4 h-4" />
          <span>{t('auto.charaKarakas7Variabl')}</span>
        </div>
        <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '5%' }} /><col style={{ width: '28%' }} />
            <col style={{ width: '18%' }} /><col style={{ width: '12%' }} />
            <col style={{ width: '37%' }} />
          </colgroup>
          <thead><tr>
            <th className={thC}>#</th>
            <th className={thL}>{t('auto.karaka')}</th>
            <th className={thL}>{t('auto.planet')}</th>
            <th className={thC}>{t('auto.degree')}</th>
            <th className={thL.replace('text-left', 'text-right')}>{t('auto.significance')}</th>
          </tr></thead>
          <tbody>
            {(data.chara_karakas || []).map((k: any, i: number) => (
              <tr key={k.karaka} className={i === 0 ? 'bg-amber-50/40' : ''}>
                <td className={`${tdC} text-muted-foreground`}>{i + 1}</td>
                <td className={`${tdL} font-semibold`} style={{ color: i === 0 ? '#92400e' : undefined }}>
                  {k.karaka} — {isHi ? k.name_hi : k.name_en}
                </td>
                <td className={`${tdL} font-semibold`}>{translatePlanet(k.planet, language)}</td>
                <td className={`${tdC} font-mono`}>{k.degree}°</td>
                <td className={`${tdL} text-muted-foreground text-right`}>{translateBackend(k.significance, language)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Special Lagnas */}
      {data.special_lagnas && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Star className="w-4 h-4" />
            <span>{t('auto.specialLagnas')}</span>
          </div>
          <div className="p-4 grid grid-cols-1 sm:grid-cols-3 gap-4">
            {SPECIAL_LAGNAS.map(({ key, icon: Icon, title_en, title_hi, desc_en, desc_hi }) => {
              const lagna = data.special_lagnas[key];
              if (!lagna) return null;
              return (
                <div key={key} className="rounded-xl border border-border p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Icon className="w-4 h-4 text-primary shrink-0" />
                    <p className="text-sm font-semibold text-foreground">{isHi ? title_hi : title_en}</p>
                  </div>
                  <p className="text-xl font-bold text-primary">{translateSign(lagna.sign, language)}</p>
                  <div className="flex items-center justify-between mt-1">
                    <p className="text-xs text-muted-foreground">{t('auto.houseLagnaHouse')}</p>
                    {lagna.atmakaraka && (
                      <span className="text-[10px] bg-muted text-primary px-1.5 py-0.5 rounded font-bold uppercase">AK: {translatePlanet(lagna.atmakaraka, language)}</span>
                    )}
                  </div>
                  <p className="text-[11px] text-muted-foreground mt-2 italic leading-snug">{isHi ? desc_hi : desc_en}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Karakamsha Detail */}
      {data.special_lagnas?.karakamsha?.planet_houses && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Crown className="w-4 h-4" />
            <span>{t('auto.karakamshaAnalysisSo')}</span>
          </div>
          <div className="p-4">
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {Object.entries(data.special_lagnas.karakamsha.planet_houses).map(([planet, house]: [string, any]) => (
                <div key={planet} className="rounded-lg border border-border p-2.5 flex flex-col items-center">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase">{translatePlanet(planet, language)}</span>
                  <span className="text-lg font-black text-primary mt-1">{t('auto.hHouse')}</span>
                </div>
              ))}
            </div>
            <p className="text-[10px] text-muted-foreground mt-3 italic text-center uppercase tracking-widest">{t('auto.akNavamshaNote')}</p>
          </div>
        </div>
      )}

      {/* Indu Lagna */}
      {data.indu_lagna && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Wallet className="w-4 h-4" />
            <span>{t('auto.induLagnaWealthIndic')}</span>
          </div>
          <div className="p-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="rounded-lg border border-border p-3">
              <p className="text-xs text-muted-foreground">{t('auto.induLagnaSign')}</p>
              <p className="text-lg font-bold text-primary mt-0.5">{translateSign(data.indu_lagna.indu_lagna_sign, language)}</p>
            </div>
            <div className="rounded-lg border border-border p-3">
              <p className="text-xs text-muted-foreground">{t('auto.house')}</p>
              <p className="text-lg font-bold text-foreground mt-0.5">{data.indu_lagna.indu_lagna_house}</p>
            </div>
            <div className="rounded-lg border border-border p-3">
              <p className="text-xs text-muted-foreground">{t('auto.9thLordLagna')}</p>
              <p className="text-lg font-bold text-foreground mt-0.5">{translatePlanet(data.indu_lagna.ninth_lord_lagna, language)}</p>
            </div>
            <div className="rounded-lg border border-border p-3">
              <p className="text-xs text-muted-foreground">{t('auto.9thLordMoon')}</p>
              <p className="text-lg font-bold text-foreground mt-0.5">{translatePlanet(data.indu_lagna.ninth_lord_moon, language)}</p>
            </div>
          </div>
        </div>
      )}

      {/* Chara Dasha */}
      {data.chara_dasha?.periods && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Clock className="w-4 h-4" />
            <span>{t('auto.charaDashaSignBasedT')}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '5%' }} /><col style={{ width: '18%' }} />
              <col style={{ width: '12%' }} /><col style={{ width: '15%' }} />
              <col style={{ width: '8%' }} /><col style={{ width: '21%' }} />
              <col style={{ width: '21%' }} />
            </colgroup>
            <thead><tr>
              <th className={thC}></th>
              <th className={thL}>{t('auto.sign')}</th>
              <th className={thL}>{t('auto.type')}</th>
              <th className={thL}>{t('auto.lord')}</th>
              <th className={thC}>{t('auto.years')}</th>
              <th className={thL}>{t('auto.start')}</th>
              <th className={thL}>{t('auto.end')}</th>
            </tr></thead>
            <tbody>
              {data.chara_dasha.periods.map((p: any, i: number) => {
                const isCurrent  = i === data.chara_dasha.current_period_index;
                const isExpanded = expandedDasha === i;
                return (
                  <Fragment key={i}>
                    <tr
                      onClick={() => setExpandedDasha(isExpanded ? null : i)}
                      className={`cursor-pointer ${isCurrent ? 'bg-amber-50/60 font-semibold' : 'hover:bg-muted/20'}`}
                    >
                      <td className={`${tdC} text-muted-foreground`}>
                        {isExpanded ? <ChevronDown className="w-3 h-3 mx-auto" /> : <ChevronRight className="w-3 h-3 mx-auto" />}
                      </td>
                      <td className={tdL}>
                        {translateSign(p.sign, language)}
                        {isCurrent && <span className="ml-1 text-[10px] text-amber-700 font-semibold">← {t('auto.current')}</span>}
                      </td>
                      <td className={tdL}>
                        {p.sign_type && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded font-semibold" style={{
                            backgroundColor: p.sign_type === 'Cardinal' ? '#dbeafe' : p.sign_type === 'Fixed' ? '#fef3c7' : '#d1fae5',
                            color: p.sign_type === 'Cardinal' ? '#1e40af' : p.sign_type === 'Fixed' ? '#92400e' : '#065f46',
                          }}>
                            {isHi ? p.sign_type_hi : p.sign_type}
                          </span>
                        )}
                      </td>
                      <td className={`${tdL} font-medium text-muted-foreground`}>{translatePlanet(p.lord, language)}</td>
                      <td className={`${tdC} font-mono`}>{p.years}</td>
                      <td className={`${tdL} font-mono`}>{p.start_date}</td>
                      <td className={`${tdL} font-mono`}>{p.end_date}</td>
                    </tr>
                    {isExpanded && p.antardashas && (
                      <tr>
                        <td colSpan={7} className="p-3 border-t border-border bg-muted/20">
                          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
                            {p.antardashas.map((ad: any, j: number) => (
                              <div key={j} className="rounded border border-border p-2 flex flex-col items-center">
                                <span className="text-xs font-bold text-foreground">{translateSign(ad.sign, language)}</span>
                                <span className="text-[10px] text-muted-foreground mt-1 font-mono">{ad.start_date}</span>
                              </div>
                            ))}
                          </div>
                        </td>
                      </tr>
                    )}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Jaimini Drishti */}
      {data.jaimini_drishti?.sign_aspects && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Eye className="w-4 h-4" />
            <span>{t('auto.jaiminiDrishtiSignBa')}</span>
          </div>
          <div className="p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {Object.entries(data.jaimini_drishti.sign_aspects).map(([sign, targets]: [string, any]) => (
              <div key={sign} className="rounded-lg border border-border p-2">
                <span className="font-semibold text-sm text-foreground">{translateSign(sign, language)}</span>
                <span className="text-sm text-muted-foreground mx-1">→</span>
                <span className="text-sm text-muted-foreground">{(targets as string[]).map((tgt: string) => translateSign(tgt, language)).join(', ')}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Jaimini Yogas */}
      {data.jaimini_yogas && data.jaimini_yogas.length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Star className="w-4 h-4" />
            <span>{t('auto.jaiminiYogas')}</span>
          </div>
          <div className="p-4 space-y-2">
            {data.jaimini_yogas.map((yoga: any, i: number) => (
              <div key={i} className="rounded-lg border border-emerald-200 bg-emerald-50/40 p-3">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-sm text-emerald-800">{isHi ? yoga.name_hi : yoga.name_en}</span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${yoga.strength === 'Strong' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                    {yoga.strength === 'Strong' ? t('auto.strong') : t('auto.weak')}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{isHi ? yoga.description_hi : yoga.description_en}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Longevity */}
      {data.longevity && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Clock className="w-4 h-4" />
            <span>{t('auto.longevityCalculation')}</span>
          </div>
          <div className="p-4 space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="rounded-lg border p-3 text-center" style={{
                backgroundColor: data.longevity.category === 'Purna' ? '#d1fae5' : data.longevity.category === 'Madhyama' ? '#fef3c7' : '#fee2e2',
                borderColor: data.longevity.category === 'Purna' ? '#059669' : data.longevity.category === 'Madhyama' ? '#d97706' : '#dc2626',
              }}>
                <p className="text-xl font-bold" style={{ color: data.longevity.category === 'Purna' ? '#065f46' : data.longevity.category === 'Madhyama' ? '#92400e' : '#991b1b' }}>
                  {translateBackend(data.longevity.category, language)}
                </p>
                <p className="text-xs mt-1" style={{ color: data.longevity.category === 'Purna' ? '#065f46' : data.longevity.category === 'Madhyama' ? '#92400e' : '#991b1b' }}>
                  {isHi ? data.longevity.description_hi : data.longevity.description_en}
                </p>
              </div>
              <div className="rounded-lg border border-border p-3">
                <p className="text-xs text-muted-foreground">{t('auto.lagnaSign')}</p>
                <p className="font-semibold text-foreground mt-0.5">{translateSign(data.longevity.lagna_sign, language)} ({data.longevity.lagna_modality})</p>
              </div>
              <div className="rounded-lg border border-border p-3">
                <p className="text-xs text-muted-foreground">{t('auto.8thLord')}</p>
                <p className="font-semibold text-foreground mt-0.5">{translatePlanet(data.longevity.eighth_lord, language)} {t('auto.in')} {translateSign(data.longevity.eighth_lord_sign, language)} ({data.longevity.eighth_modality})</p>
              </div>
            </div>
            {(data.longevity.note_hi || data.longevity.note_en) && (
              <p className="text-xs text-muted-foreground italic">{isHi ? data.longevity.note_hi : data.longevity.note_en}</p>
            )}
          </div>
        </div>
      )}

      {/* Argala */}
      {data.argala?.house_argalas && data.argala.house_argalas.length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Eye className="w-4 h-4" />
            <span>{t('auto.argalaPlanetaryInter')}</span>
          </div>
          <div className="p-4 space-y-2">
            {data.argala.house_argalas.map((ha: any) => (
              <div key={ha.house} className="rounded-lg border border-border p-3">
                <p className="text-sm font-semibold mb-2 px-2 py-0.5 rounded bg-orange-100 text-orange-800 inline-block">{t('table.house')} {ha.house}</p>
                <div className="space-y-2">
                  {ha.argalas.map((a: any, i: number) => (
                    <div key={i} className="rounded border border-border/50 p-2 bg-muted/10">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-muted-foreground">
                          {translateBackend(a.type, language)} — {a.planets.map((p: string) => translatePlanet(p, language)).join(', ')} (H{a.from_house})
                        </span>
                        <div className="flex items-center gap-1.5">
                          {a.nature && (
                            <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                              a.nature === 'Shubha' ? 'bg-emerald-100 text-emerald-700' :
                              a.nature === 'Paapa'  ? 'bg-red-100 text-red-700' :
                                                      'bg-amber-100 text-amber-700'
                            }`}>{isHi ? a.nature_hi : a.nature_en}</span>
                          )}
                          <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${a.blocked ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'}`}>
                            {a.status === 'Blocked' ? t('auto.blocked') : t('auto.active')}
                          </span>
                        </div>
                      </div>
                      {(a.detail_en || a.detail_hi) && <p className="text-xs text-muted-foreground mt-1">{isHi ? a.detail_hi : a.detail_en}</p>}
                      {(a.remedy_en || a.remedy_hi) && (
                        <p className="text-xs mt-1 italic text-purple-700"><strong>{t('auto.remedy')}</strong> {isHi ? a.remedy_hi : a.remedy_en}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Nadi Insights */}
      {data.nadi_insights && data.nadi_insights.length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            <span>{t('auto.nadiAstrologyInsight')}</span>
            <span className="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/20 border border-white/30 font-bold uppercase tracking-widest">{t('auto.ancient')}</span>
          </div>
          <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.nadi_insights.map((n: any, i: number) => (
              <div key={i} className="rounded-xl border border-border p-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-semibold text-primary">{isHi ? n.title_hi : n.title_en}</p>
                  {n.house && <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-orange-100 text-orange-800">H{n.house}</span>}
                </div>
                <p className="text-xs text-foreground leading-relaxed italic mb-3">"{isHi ? n.desc_hi : n.desc_en}"</p>
                <div className="flex flex-wrap gap-1.5">
                  {n.planets.map((p: string) => (
                    <span key={p} className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-primary font-bold uppercase">{translatePlanet(p, language)}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
