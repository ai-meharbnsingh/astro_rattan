import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Scale, AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';

interface Props {
  kundliId: string;
}

interface Debt {
  id: string;
  debt_type: string;
  planet: string;
  description: string;
  indication: string;
  remedy: string;
  active: boolean;
}

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

// English translations for the 8 debt types (DB data is Hindi-only)
const DEBT_EN: Record<string, { type: string; description: string; indication: string; remedy: string }> = {
  'पितृ ऋण':      { type: "Pitru Rin (Father's Debt)",          description: 'Karmic debt related to father or ancestors',          indication: 'Sun afflicted, conflict with father, eye problems',           remedy: 'Keep Gangajal in a copper vessel, seek father\'s blessings' },
  'मातृ ऋण':      { type: "Matru Rin (Mother's Debt)",           description: 'Karmic debt related to mother',                       indication: 'Moon afflicted, conflict with mother, mental stress',          remedy: 'Keep a square piece of silver, serve and care for mother' },
  'भ्रातृ ऋण':    { type: "Bhratu Rin (Sibling's Debt)",         description: 'Karmic debt related to brothers and sisters',         indication: 'Mars afflicted, disputes with brothers, blood ailments',      remedy: 'Donate red lentils (masoor dal), respect siblings' },
  'देव ऋण':       { type: "Dev Rin (Divine/Guru's Debt)",        description: 'Karmic debt to deities or spiritual teacher',         indication: 'Jupiter afflicted, issues related to children',               remedy: 'Worship the Peepal tree, feed a Brahmin' },
  'स्त्री ऋण':   { type: "Stri Rin (Women's Debt)",             description: 'Karmic debt related to women',                        indication: 'Venus afflicted, marital problems',                           remedy: 'Serve a cow, respect and honour your wife' },
  'शत्रु ऋण':    { type: "Shatru Rin (Enemy's Debt)",           description: 'Karmic debt related to enemies or past actions',      indication: 'Saturn afflicted, delayed success, physical pain',            remedy: 'Donate oil on Saturdays, feed roti to a black dog' },
  'पितामह ऋण':   { type: "Pitamah Rin (Grandfather's Debt)",    description: 'Karmic debt to ancestors or maternal grandfather',    indication: 'Rahu afflicted, hidden enemies, addiction tendencies',        remedy: 'Drop 400g lead into flowing water, respect maternal grandfather' },
  'प्रपितामह ऋण':{ type: "Prapitamah Rin (Great-Grandfather's Debt)", description: 'Karmic debt to great-grandparents or ancestors', indication: 'Ketu afflicted, spiritual confusion, fear of untimely events', remedy: 'Feed jaggery to monkeys, apply saffron tilak' },
};

const PLANET_COLOR: Record<string, string> = {
  sun:     'bg-orange-400/15 text-orange-700',
  moon:    'bg-blue-400/15 text-blue-700',
  mars:    'bg-red-400/15 text-red-700',
  mercury: 'bg-green-400/15 text-green-700',
  jupiter: 'bg-yellow-400/15 text-yellow-700',
  venus:   'bg-pink-400/15 text-pink-700',
  saturn:  'bg-gray-400/15 text-gray-700',
  rahu:    'bg-purple-400/15 text-purple-700',
  ketu:    'bg-indigo-400/15 text-indigo-700',
};

export default function LalKitabRinTab({ kundliId }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [debts, setDebts] = useState<Debt[]>([]);
  const [afflicted, setAfflicted] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!kundliId) {
      setDebts([]);
      setAfflicted([]);
      setError('');
      return;
    }
    setLoading(true);
    setError('');
    api.get(`/api/lalkitab/rin/${kundliId}`)
      .then((res: any) => {
        setDebts(Array.isArray(res?.debts) ? res.debts : []);
        setAfflicted(Array.isArray(res?.afflicted_planets) ? res.afflicted_planets : []);
      })
      .catch(() => setError(t('auto.failedToLoadDebtData')))
      .finally(() => setLoading(false));
  }, [kundliId, isHi]);

  const activeDebts = debts.filter((d) => d.active);
  const inactiveDebts = debts.filter((d) => !d.active);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Scale className="w-5 h-5" />
          {t('auto.lalKitabRinKarmicDeb')}
        </h2>
        <p className="text-sm text-gray-500">
          {t('auto.pastLifeKarmicDebtsT')}
        </p>
      </div>

      {/* Afflicted planets notice */}
      {!loading && afflicted.length > 0 && (
        <div className="flex items-start gap-3 p-4 rounded-xl border border-red-300/30 bg-red-500/5">
          <AlertCircle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
          <div>
            <p className="text-sm font-semibold text-red-700 mb-1">
              {t('auto.afflictedPlanetsIn6t')}
            </p>
            <div className="flex flex-wrap gap-2">
              {afflicted.map((p) => (
                <span key={p} className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${PLANET_COLOR[p] ?? 'bg-gray-100 text-gray-600'}`}>
                  {isHi ? (PLANET_HI[p] ?? p) : p.charAt(0).toUpperCase() + p.slice(1)}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Summary */}
      {!loading && debts.length > 0 && (
        <div className="flex gap-3">
          <div className="flex-1 p-3 rounded-xl bg-red-500/8 border border-red-300/20 text-center">
            <p className="text-2xl font-bold text-red-600">{activeDebts.length}</p>
            <p className="text-xs text-gray-500 mt-0.5">{t('auto.activeDebts')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-green-500/8 border border-green-300/20 text-center">
            <p className="text-2xl font-bold text-green-600">{inactiveDebts.length}</p>
            <p className="text-xs text-gray-500 mt-0.5">{t('auto.inactiveDebts')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-sacred-gold/8 border border-sacred-gold/20 text-center">
            <p className="text-2xl font-bold text-sacred-gold">{debts.length}</p>
            <p className="text-xs text-gray-500 mt-0.5">{t('auto.totalDebts')}</p>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Active Debts */}
      {!loading && activeDebts.length > 0 && (
        <div>
          <h3 className="font-sans font-semibold text-red-700 mb-3 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            {t('auto.activeDebtsRemediesR')}
          </h3>
          <div className="space-y-4">
            {activeDebts.map((debt) => (
              <DebtCard key={debt.id} debt={debt} isHi={isHi} />
            ))}
          </div>
        </div>
      )}

      {/* Inactive Debts */}
      {!loading && inactiveDebts.length > 0 && (
        <div>
          <h3 className="font-sans font-semibold text-green-700 mb-3 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            {t('auto.inactiveDebtsNotCurr')}
          </h3>
          <div className="space-y-3">
            {inactiveDebts.map((debt) => (
              <DebtCard key={debt.id} debt={debt} isHi={isHi} />
            ))}
          </div>
        </div>
      )}

      {!loading && !error && debts.length === 0 && (
        <div className="text-center py-12 text-gray-400 text-sm">
          {t('auto.noDebtDataAvailable')}
        </div>
      )}
    </div>
  );
}

function DebtCard({ debt, isHi }: { debt: Debt; isHi: boolean }) {
  const PLANET_COLOR: Record<string, string> = {
    sun: 'bg-orange-400/15 text-orange-700', moon: 'bg-blue-400/15 text-blue-700',
    mars: 'bg-red-400/15 text-red-700', mercury: 'bg-green-400/15 text-green-700',
    jupiter: 'bg-yellow-400/15 text-yellow-700', venus: 'bg-pink-400/15 text-pink-700',
    saturn: 'bg-gray-400/15 text-gray-700', rahu: 'bg-purple-400/15 text-purple-700',
    ketu: 'bg-indigo-400/15 text-indigo-700',
  };
  const PLANET_HI: Record<string, string> = {
    sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
    jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
  };

  return (
    <div
      className={`card-sacred rounded-xl border p-4 ${
        debt.active
          ? 'border-red-300/40 bg-red-500/5'
          : 'border-gray-200/50 bg-white/20'
      }`}
    >
      {/* Title row */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <h4 className="font-sans font-semibold text-foreground">{debt.debt_type}</h4>
          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${PLANET_COLOR[debt.planet] ?? 'bg-gray-100 text-gray-600'}`}>
            {isHi ? (PLANET_HI[debt.planet] ?? debt.planet) : debt.planet.charAt(0).toUpperCase() + debt.planet.slice(1)}
          </span>
        </div>
        {debt.active ? (
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-500/10 text-red-700 text-xs font-semibold border border-red-300/30">
            <AlertCircle className="w-3 h-3" />
            {t('auto.active')}
          </span>
        ) : (
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-green-500/10 text-green-700 text-xs font-medium border border-green-300/30">
            <CheckCircle2 className="w-3 h-3" />
            {t('auto.inactive')}
          </span>
        )}
      </div>

      {/* Description */}
      <p className="text-sm text-foreground/80 mb-3 leading-relaxed">
        {isHi ? debt.description : (DEBT_EN[debt.debt_type]?.description ?? debt.description)}
      </p>

      {/* Indication */}
      {debt.indication && (
        <div className="mb-3 p-3 rounded-lg bg-sacred-gold/5 border border-sacred-gold/15">
          <p className="text-xs font-semibold text-sacred-gold mb-1">
            {t('auto.indication')}
          </p>
          <p className="text-xs text-foreground/70 leading-snug">
            {isHi ? debt.indication : (DEBT_EN[debt.debt_type]?.indication ?? debt.indication)}
          </p>
        </div>
      )}

      {/* Remedy */}
      <div className="p-3 rounded-lg bg-green-500/5 border border-green-300/20">
        <p className="text-xs font-semibold text-green-700 mb-1">
          {t('auto.remedy')}
        </p>
        <p className="text-xs text-foreground/70 leading-snug">
          {isHi ? debt.remedy : (DEBT_EN[debt.debt_type]?.remedy ?? debt.remedy)}
        </p>
      </div>
    </div>
  );
}
