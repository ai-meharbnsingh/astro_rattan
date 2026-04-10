import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import {
  PLANETS,
  MIRROR_HOUSES,
  PLANET_EFFECTS_IN_HOUSES,
} from './lalkitab-data';
import { BookOpen, Layers, Eye } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}

interface HiddenRule {
  en: string;
  hi: string;
}

const HIDDEN_INFLUENCE_RULES: HiddenRule[] = [
  {
    en: 'If a house is empty, its mirror house lord controls it.',
    hi: 'यदि कोई भाव खाली है, तो उसके दर्पण भाव का स्वामी उसे नियंत्रित करता है।',
  },
  {
    en: 'Planets in 3rd house affect 9th house fortune directly.',
    hi: 'तीसरे भाव के ग्रह सीधे 9वें भाव के भाग्य को प्रभावित करते हैं।',
  },
  {
    en: 'A planet in its Pakka Ghar activates its full power for good or ill.',
    hi: 'पक्का घर में ग्रह अच्छे या बुरे के लिए अपनी पूर्ण शक्ति सक्रिय करता है।',
  },
  {
    en: 'Two enemy planets in the same house cancel each other\'s good effects.',
    hi: 'एक ही भाव में दो शत्रु ग्रह एक-दूसरे के शुभ प्रभावों को रद्द कर देते हैं।',
  },
  {
    en: 'An empty 7th house is governed by the planet in the 1st house.',
    hi: 'खाली 7वें भाव को 1ले भाव के ग्रह द्वारा नियंत्रित किया जाता है।',
  },
  {
    en: 'Planets sleeping (dormant) get activated when their Pakka Ghar is triggered.',
    hi: 'सोए हुए (निष्क्रिय) ग्रह तब सक्रिय होते हैं जब उनका पक्का घर सक्रिय होता है।',
  },
];

interface CrossHouseRule {
  fromHouse: number;
  toHouse: number;
  domainEn: string;
  domainHi: string;
  effectEn: string;
  effectHi: string;
}

const CROSS_HOUSE_RULES: CrossHouseRule[] = [
  {
    fromHouse: 1,
    toHouse: 7,
    domainEn: 'marriage & partnerships',
    domainHi: 'विवाह और साझेदारी',
    effectEn: 'Planet in 1st house directly influences 7th house marriage prospects.',
    effectHi: '1ले भाव का ग्रह सीधे 7वें भाव के विवाह की संभावनाओं को प्रभावित करता है।',
  },
  {
    fromHouse: 4,
    toHouse: 10,
    domainEn: 'career & status',
    domainHi: 'करियर और स्थिति',
    effectEn: 'Planet in 4th house shapes 10th house career and public image.',
    effectHi: '4थे भाव का ग्रह 10वें भाव के करियर और सार्वजनिक छवि को आकार देता है।',
  },
  {
    fromHouse: 5,
    toHouse: 9,
    domainEn: 'luck & fortune',
    domainHi: 'भाग्य और सौभाग्य',
    effectEn: 'Planet in 5th house activates 9th house luck and spiritual merit.',
    effectHi: '5वें भाव का ग्रह 9वें भाव के भाग्य और आध्यात्मिक पुण्य को सक्रिय करता है।',
  },
  {
    fromHouse: 2,
    toHouse: 8,
    domainEn: 'inheritance & longevity',
    domainHi: 'विरासत और दीर्घायु',
    effectEn: 'Planet in 2nd house controls 8th house inheritance and transformation.',
    effectHi: '2रे भाव का ग्रह 8वें भाव की विरासत और परिवर्तन को नियंत्रित करता है।',
  },
  {
    fromHouse: 3,
    toHouse: 9,
    domainEn: 'fortune & dharma',
    domainHi: 'भाग्य और धर्म',
    effectEn: 'Planet in 3rd house influences 9th house dharma and long journeys.',
    effectHi: '3रे भाव का ग्रह 9वें भाव के धर्म और लंबी यात्राओं को प्रभावित करता है।',
  },
  {
    fromHouse: 6,
    toHouse: 12,
    domainEn: 'expenses & losses',
    domainHi: 'खर्च और हानि',
    effectEn: 'Planet in 6th house triggers 12th house expenses and foreign travel.',
    effectHi: '6ठे भाव का ग्रह 12वें भाव के खर्च और विदेश यात्रा को सक्रिय करता है।',
  },
  {
    fromHouse: 7,
    toHouse: 1,
    domainEn: 'self & personality',
    domainHi: 'स्वयं और व्यक्तित्व',
    effectEn: 'Planet in 7th house reflects back on 1st house personality and health.',
    effectHi: '7वें भाव का ग्रह 1ले भाव के व्यक्तित्व और स्वास्थ्य पर प्रभाव डालता है।',
  },
  {
    fromHouse: 10,
    toHouse: 4,
    domainEn: 'home & mother',
    domainHi: 'घर और माता',
    effectEn: 'Planet in 10th house impacts 4th house domestic peace and property.',
    effectHi: '10वें भाव का ग्रह 4थे भाव की घरेलू शांति और संपत्ति को प्रभावित करता है।',
  },
];

export default function LalKitabRulesTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const getPlanetLabel = (key: string) => {
    const planet = PLANETS.find((p) => p.key === key);
    if (!planet) return key;
    return isHi ? planet.hi : planet.en;
  };

  // Build a house-to-planets map for quick lookup
  const housePlanets = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (let h = 1; h <= 12; h++) map[h] = [];
    for (const [planet, house] of Object.entries(chartData.planetPositions)) {
      if (house != null && map[house]) {
        map[house].push(planet);
      }
    }
    return map;
  }, [chartData.planetPositions]);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="font-sans text-2xl text-sacred-gold flex items-center gap-2">
          <BookOpen className="w-6 h-6" />
          {t('lk.rules.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.rules.desc')}</p>
      </div>

      {/* Mirror House Axis */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4">
          {t('lk.rules.mirrorAxis')}
        </h3>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {MIRROR_HOUSES.map(([h1, h2]) => {
            const planetsH1 = housePlanets[h1] ?? [];
            const planetsH2 = housePlanets[h2] ?? [];
            const hasMutual = planetsH1.length > 0 && planetsH2.length > 0;

            return (
              <div
                key={`${h1}-${h2}`}
                className={`card-sacred rounded-xl border transition-all ${
                  hasMutual
                    ? 'border-sacred-gold/40 bg-sacred-gold/5'
                    : 'border-sacred-gold/20'
                }`}
              >
                {/* Two halves with arrow in center */}
                <div className="flex items-stretch">
                  {/* Left house */}
                  <div className="flex-1 p-4 text-center">
                    <p className="text-sm text-cosmic-text/70 mb-1">
                      {isHi ? 'भाव' : 'House'}
                    </p>
                    <p className="text-2xl font-sans font-bold text-sacred-gold">
                      {h1}
                    </p>
                    <div className="mt-2 space-y-1">
                      {planetsH1.length > 0 ? (
                        planetsH1.map((p) => (
                          <span
                            key={p}
                            className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mr-1"
                          >
                            {getPlanetLabel(p)}
                          </span>
                        ))
                      ) : (
                        <span className="text-sm text-cosmic-text/60 italic">
                          {isHi ? 'खाली' : 'Empty'}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Center arrow */}
                  <div className="flex items-center justify-center px-2">
                    <span className="text-sacred-gold/60 text-xl">&#10231;</span>
                  </div>

                  {/* Right house */}
                  <div className="flex-1 p-4 text-center">
                    <p className="text-sm text-cosmic-text/70 mb-1">
                      {isHi ? 'भाव' : 'House'}
                    </p>
                    <p className="text-2xl font-sans font-bold text-sacred-gold">
                      {h2}
                    </p>
                    <div className="mt-2 space-y-1">
                      {planetsH2.length > 0 ? (
                        planetsH2.map((p) => (
                          <span
                            key={p}
                            className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mr-1"
                          >
                            {getPlanetLabel(p)}
                          </span>
                        ))
                      ) : (
                        <span className="text-sm text-cosmic-text/60 italic">
                          {isHi ? 'खाली' : 'Empty'}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Explanation */}
                <div className="border-t border-sacred-gold/10 p-3">
                  {hasMutual ? (
                    <p className="text-sm text-sacred-gold/80 text-center">
                      {isHi
                        ? `भाव ${h1} और भाव ${h2} के ग्रह परस्पर प्रभाव डालते हैं`
                        : `Planets in House ${h1} and House ${h2} have mutual influence`}
                    </p>
                  ) : (
                    <p className="text-sm text-cosmic-text/60 text-center">
                      {isHi
                        ? `भाव ${h1} का ग्रह भाव ${h2} को प्रभावित करता है`
                        : `Planet in House ${h1} affects House ${h2}`}
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Separator */}
      <div className="border-t border-sacred-gold/10" />

      {/* Hidden Influence */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4 flex items-center gap-2">
          <Eye className="w-5 h-5" />
          {t('lk.rules.hiddenInfluence')}
        </h3>

        <div className="grid gap-3 sm:grid-cols-2">
          {HIDDEN_INFLUENCE_RULES.map((rule, idx) => (
            <div
              key={idx}
              className="card-sacred rounded-xl p-4 border border-sacred-gold/20"
            >
              <p className="text-sm text-cosmic-text/80">
                {isHi ? rule.hi : rule.en}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Separator */}
      <div className="border-t border-sacred-gold/10" />

      {/* Cross-House Effects */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5" />
          {t('lk.rules.crossEffect')}
        </h3>

        <div className="space-y-4">
          {CROSS_HOUSE_RULES.map((rule, idx) => {
            const planetsFrom = housePlanets[rule.fromHouse] ?? [];
            const hasPlanets = planetsFrom.length > 0;

            return (
              <div
                key={idx}
                className={`card-sacred rounded-xl p-4 border border-sacred-gold/20 ${
                  hasPlanets ? 'bg-sacred-gold/5' : ''
                }`}
              >
                {/* House labels */}
                <div className="flex items-center gap-3 mb-2 flex-wrap">
                  <span className="px-2.5 py-1 rounded-lg bg-sacred-gold/10 text-sacred-gold text-sm font-sans font-medium">
                    {isHi ? 'भाव' : 'House'} {rule.fromHouse}
                  </span>
                  <span className="text-sacred-gold/40">&#10230;</span>
                  <span className="px-2.5 py-1 rounded-lg bg-sacred-gold/10 text-sacred-gold text-sm font-sans font-medium">
                    {isHi ? 'भाव' : 'House'} {rule.toHouse}
                  </span>
                  <span className="text-sm text-cosmic-text/60">
                    ({isHi ? rule.domainHi : rule.domainEn})
                  </span>
                </div>

                {/* Rule text */}
                <p className="text-sm text-cosmic-text/70">
                  {isHi ? rule.effectHi : rule.effectEn}
                </p>

                {/* Applied chart data */}
                {hasPlanets && (
                  <div className="mt-3 pt-3 border-t border-sacred-gold/10">
                    <p className="text-sm text-cosmic-text/70 mb-1.5">
                      {isHi
                        ? `भाव ${rule.fromHouse} में वर्तमान ग्रह:`
                        : `Current planets in House ${rule.fromHouse}:`}
                    </p>
                    <div className="flex gap-2 flex-wrap">
                      {planetsFrom.map((p) => {
                        const effect =
                          PLANET_EFFECTS_IN_HOUSES[p]?.[rule.fromHouse];
                        return (
                          <div key={p} className="flex-1 min-w-[200px]">
                            <span className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/15 text-sacred-gold text-sm font-medium mb-1">
                              {getPlanetLabel(p)}
                            </span>
                            {effect && (
                              <p className="text-sm text-cosmic-text/60">
                                {isHi ? effect.hi : effect.en}
                              </p>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
