import { useTranslation } from '@/lib/i18n';
import { useState, useEffect } from 'react';
import { Loader2, Briefcase, BookOpen, Star, Compass, Users } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface NavamshaCareerData {
  kundli_id?: string;
  person_name?: string;
  d9_lagna?: string;
  d9_lagna_hi?: string;
  d9_10th_house_sign?: string;
  d9_10th_house_sign_hi?: string;
  d9_10th_lord?: string;
  d9_10th_lord_sign?: string;
  d9_10th_lord_sign_hi?: string;
  profession_type_en?: string;
  profession_type_hi?: string;
  detailed_interpretation_en?: string;
  detailed_interpretation_hi?: string;
  supporting_planets_en?: string;
  supporting_planets_hi?: string;
  career_examples_en?: string[];
  career_examples_hi?: string[];
  sloka_ref?: string;
}

interface Props {
  kundliId: string;
  language?: string;
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-muted-foreground border-t border-border align-top w-[40%]';
const tdValCls    = 'p-1.5 text-xs text-foreground font-medium border-t border-border align-top break-words overflow-hidden';

export default function NavamshaCareerTab({ kundliId, language }: Props) {
  const { t } = useTranslation();
  const [data, setData] = useState<NavamshaCareerData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    (async () => {
      try {
        const res = await api.get(`/api/kundli/${kundliId}/navamsha-profession`);
        if (!cancelled) setData(res as NavamshaCareerData);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || t('auto.genericError'));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
    );
  }

  if (!data) return null;

  const professionType   = hi ? data.profession_type_hi   : data.profession_type_en;
  const interpretation   = hi ? data.detailed_interpretation_hi : data.detailed_interpretation_en;
  const supportingText   = hi ? data.supporting_planets_hi : data.supporting_planets_en;
  const examples         = (hi ? data.career_examples_hi : data.career_examples_en) ?? [];
  const d9Lagna          = hi ? (data.d9_lagna_hi || data.d9_lagna) : data.d9_lagna;
  const d910Sign         = hi ? (data.d9_10th_house_sign_hi || data.d9_10th_house_sign) : data.d9_10th_house_sign;
  const lordSign         = hi ? (data.d9_10th_lord_sign_hi || data.d9_10th_lord_sign) : data.d9_10th_lord_sign;

  return (
    <div className="space-y-4">

      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Briefcase className="w-6 h-6" />
          {hi ? 'नवांश वृत्ति विश्लेषण' : 'Navamsha Career Analysis'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi ? 'D9 चार्ट पर आधारित जीविका एवं व्यवसाय विश्लेषण' : 'Vocation analysis based on D9 (Navamsha) chart'}
        </p>
      </div>

      {/* 1 — Profession Type */}
      {professionType && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Star className="w-4 h-4" />
            <span>{hi ? 'मुख्य वृत्ति प्रकार' : 'Primary Vocation'}</span>
          </div>
          <div className="px-4 py-4">
            <p className="text-base font-semibold text-foreground leading-relaxed">{professionType}</p>
          </div>
        </div>
      )}

      {/* 2 — D9 Chart Facts */}
      {(d9Lagna || d910Sign || data.d9_10th_lord) && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Compass className="w-4 h-4" />
            <span>{hi ? 'नवांश (D9) ग्रह स्थिति' : 'Navamsha (D9) Positions'}</span>
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '40%' }} />
              <col style={{ width: '60%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{hi ? 'कारक' : 'Factor'}</th>
                <th className={thCls}>{hi ? 'मान' : 'Value'}</th>
              </tr>
            </thead>
            <tbody>
              {d9Lagna && (
                <tr>
                  <td className={tdCls}>{hi ? 'D9 लग्न' : 'D9 Lagna'}</td>
                  <td className={tdValCls}>{d9Lagna}</td>
                </tr>
              )}
              {d910Sign && (
                <tr>
                  <td className={tdCls}>{hi ? 'दशम भाव राशि' : '10th House Sign'}</td>
                  <td className={tdValCls}>{d910Sign}</td>
                </tr>
              )}
              {data.d9_10th_lord && (
                <tr>
                  <td className={tdCls}>{hi ? 'दशम स्वामी' : '10th Lord'}</td>
                  <td className={tdValCls}>{data.d9_10th_lord}</td>
                </tr>
              )}
              {lordSign && (
                <tr>
                  <td className={tdCls}>{hi ? 'स्वामी की राशि' : "Lord's Sign"}</td>
                  <td className={tdValCls}>{lordSign}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* 3 — Detailed Interpretation */}
      {interpretation && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <BookOpen className="w-4 h-4" />
            <span>{hi ? 'विस्तृत व्याख्या' : 'Detailed Interpretation'}</span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed">{interpretation}</p>
          </div>
        </div>
      )}

      {/* 4 — Supporting Planets */}
      {supportingText && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Users className="w-4 h-4" />
            <span>{hi ? 'सहायक ग्रह' : 'Supporting Planets'}</span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed">{supportingText}</p>
          </div>
        </div>
      )}

      {/* 5 — Career Examples */}
      {examples.length > 0 && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Briefcase className="w-4 h-4" />
            <span>{hi ? 'उपयुक्त करियर उदाहरण' : 'Career Examples'}</span>
            <span className="ml-auto text-[12px] font-normal opacity-80">{examples.length}</span>
          </div>
          <div className="px-4 py-3 flex flex-wrap gap-2">
            {examples.map((ex, i) => (
              <span
                key={i}
                className="px-2.5 py-1 rounded-full bg-sacred-gold/10 border border-sacred-gold/30 text-xs font-medium text-sacred-gold-dark"
              >
                {ex}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      {data.sloka_ref && (
        <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground italic pt-2 border-t border-border">
          <BookOpen className="w-3 h-3" />
          <span>{data.sloka_ref}</span>
        </div>
      )}
    </div>
  );
}
