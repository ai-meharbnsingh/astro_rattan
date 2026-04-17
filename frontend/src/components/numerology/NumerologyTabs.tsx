import { useState } from 'react';
import { Hash, Sparkles, Loader2, Phone, User, Car, Home } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { useAuth } from '@/hooks/useAuth';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import ClientSelector, { autoRegisterClient } from '@/components/ClientSelector';
import type { ClientData } from '@/components/ClientSelector';
import NameNumerology from './NameNumerology';
import VehicleNumerology from './VehicleNumerology';
import HouseNumerology from './HouseNumerology';
import { Heading } from "@/components/ui/heading";

interface NumerologyPredictions {
  life_path: string;
  destiny: string;
  soul_urge: string;
  personality: string;
}

interface NumerologyResult {
  life_path: number;
  expression?: number;
  destiny?: number;
  soul_urge: number;
  personality: number;
  predictions?: string[] | NumerologyPredictions;
  summary?: string;

  // Upgraded core numerology fields
  birthday_number?: number;
  maturity_number?: number;
  karmic_debts?: Array<any>;
  hidden_passion?: any;
  subconscious_self?: any;
  karmic_lessons?: Array<any>;

  pinnacles?: any;
  challenges?: any;
  life_cycles?: any;

  loshu_grid?: number[][];
  loshu_values?: Record<number, string>;
  loshu_arrows?: any;
  loshu_planes?: any;
  missing_numbers?: Array<any>;
  repeated_numbers?: Array<any>;
}

interface MobileCombination {
  pair: string;
  type: 'Benefic' | 'Neutral' | 'Malefic';
  description?: string;
}

interface AreaAffirmation {
  area: string;
  affirmation: string;
}

interface MobileNumerologyResult {
  phone_number: string;
  name?: string;
  birth_date?: string;
  compound_number: number;
  mobile_total: number;
  mobile_total_prediction?: string;
  recommended_totals?: number[];
  loshu_grid?: (number | null)[][];
  vedic_grid?: (number | null)[][];
  lucky_colours?: string[];
  unlucky_colours?: string[];
  lucky_numbers?: number[];
  unlucky_numbers?: number[];
  neutral_numbers?: number[];
  missing_numbers?: number[];
  combinations?: MobileCombination[];
  is_recommended?: boolean;
  recommendation_message?: string;
  predictions?: string[];
  affirmations?: AreaAffirmation[];
}

type TabType = 'life_path' | 'mobile' | 'name' | 'vehicle' | 'house';

const tabConfig = [
  { id: 'life_path' as TabType, labelKey: 'numerology.lifePath', icon: Hash },
  { id: 'mobile' as TabType, labelKey: 'numerology.mobileHeading', icon: Phone },
  { id: 'name' as TabType, labelKey: 'numerology.nameHeading', icon: User },
  { id: 'vehicle' as TabType, labelKey: 'numerology.vehicleHeading', icon: Car },
  { id: 'house' as TabType, labelKey: 'numerology.houseHeading', icon: Home },
];

export default function NumerologyTabs() {
  const { t, language } = useTranslation();
  const { user } = useAuth();
  const isAstrologer = user?.role === 'astrologer';
  const [activeTab, setActiveTab] = useState<TabType>('life_path');
  const isHi = language === 'hi';

  const pick = (obj: any, key: string): string => {
    if (!obj) return '';
    const hi = obj[`${key}_hi`];
    const en = obj[key];
    return (isHi ? (hi ?? en) : (en ?? hi)) ?? '';
  };

  // Life Path states
  const [isNewClient, setIsNewClient] = useState(true);
  const [selectedClient, setSelectedClient] = useState<ClientData | null>(null);
  const [numName, setNumName] = useState('');
  const [numDob, setNumDob] = useState('');
  const [numResult, setNumResult] = useState<NumerologyResult | null>(null);
  const [forecastResult, setForecastResult] = useState<any | null>(null);
  const [numLoading, setNumLoading] = useState(false);
  const [error, setError] = useState('');

  // Mobile states
  const [firstName, setFirstName] = useState('');
  const [middleName, setMiddleName] = useState('');
  const [lastName, setLastName] = useState('');
  const [mobileCountryCode, setMobileCountryCode] = useState('+91');
  const [mobilePhone, setMobilePhone] = useState('');
  const [mobileDob, setMobileDob] = useState('');
  const [selectedAreas, setSelectedAreas] = useState<string[]>([]);
  const [mobileResult, setMobileResult] = useState<MobileNumerologyResult | null>(null);
  const [mobileLoading, setMobileLoading] = useState(false);
  const [mobileIsNewClient, setMobileIsNewClient] = useState(true);
  const [mobileSelectedClient, setMobileSelectedClient] = useState<ClientData | null>(null);

  const handleClientSelect = (client: ClientData | null) => {
    setSelectedClient(client);
    if (client) {
      setNumName(client.name || '');
      setNumDob(client.birth_date || '');
    }
  };

  const handleClientToggle = (isNew: boolean) => {
    setIsNewClient(isNew);
    if (isNew) {
      setSelectedClient(null);
      setNumName('');
      setNumDob('');
    }
  };

  const handleMobileClientSelect = (client: ClientData | null) => {
    setMobileSelectedClient(client);
    if (client) {
      const nameParts = (client.name || '').split(' ');
      setFirstName(nameParts[0] || '');
      setMiddleName(nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : '');
      setLastName(nameParts.length > 1 ? nameParts[nameParts.length - 1] : '');
      setMobileDob(client.birth_date || '');
      if (client.phone) {
        const phoneStr = client.phone || '';
        if (phoneStr.startsWith('+91')) { setMobileCountryCode('+91'); setMobilePhone(phoneStr.slice(3)); }
        else if (phoneStr.startsWith('+1')) { setMobileCountryCode('+1'); setMobilePhone(phoneStr.slice(2)); }
        else if (phoneStr.startsWith('+44')) { setMobileCountryCode('+44'); setMobilePhone(phoneStr.slice(3)); }
        else { setMobilePhone(phoneStr.replace(/^\+\d{1,3}/, '')); }
      }
    }
  };

  const handleMobileClientToggle = (isNew: boolean) => {
    setMobileIsNewClient(isNew);
    if (isNew) {
      setMobileSelectedClient(null);
      setFirstName(''); setMiddleName(''); setLastName('');
      setMobileDob(''); setMobilePhone('');
    }
  };

  const calculateNumerology = async () => {
    if (!numName.trim() || !numDob) return;
    setNumLoading(true);
    setNumResult(null);
    setForecastResult(null);
    setError('');
    try {
      const [core, forecast] = await Promise.all([
        api.post('/api/numerology/calculate', { name: numName.trim(), birth_date: numDob }),
        api.post('/api/numerology/forecast', { name: numName.trim(), birth_date: numDob }),
      ]);
      const data = core as any;
      if (data.predictions && typeof data.predictions === 'string') {
        data.predictions = [data.predictions];
      }
      setNumResult(data);
      setForecastResult(forecast as any);
      if (isAstrologer && isNewClient && !selectedClient) {
        autoRegisterClient({ name: numName.trim(), birth_date: numDob });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : t('numerology.error.calculationFailed'));
    }
    setNumLoading(false);
  };

  const toggleArea = (area: string) => {
    setSelectedAreas((prev) =>
      prev.includes(area) ? prev.filter((a) => a !== area) : [...prev, area]
    );
  };

  const analyzeMobile = async () => {
    if (!mobilePhone.trim() || !firstName.trim() || !mobileDob) return;
    setMobileLoading(true);
    setMobileResult(null);
    setError('');
    try {
      const fullName = [firstName.trim(), middleName.trim(), lastName.trim()].filter(Boolean).join(' ');
      const digitsOnly = mobilePhone.trim().replace(/\D/g, '');
      const fullPhone = `${mobileCountryCode}${digitsOnly}`;
      const data = await api.post('/api/numerology/mobile', {
        phone_number: fullPhone,
        name: fullName,
        birth_date: mobileDob,
        areas_of_struggle: selectedAreas,
      });
      setMobileResult(data);
      if (isAstrologer && mobileIsNewClient && !mobileSelectedClient) {
        autoRegisterClient({ name: fullName, phone: fullPhone, birth_date: mobileDob });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : t('numerology.error.mobileAnalysisFailed'));
    }
    setMobileLoading(false);
  };

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-3 rounded-xl bg-red-50 border border-red-300 text-red-700 text-sm text-center max-w-xl mx-auto">
          {error}
        </div>
      )}

      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as TabType)} className="space-y-6">
        <TabsList className="grid grid-cols-5 h-auto p-1 gap-1">
          {tabConfig.map((tab) => (
            <TabsTrigger
              key={tab.id}
              value={tab.id}
              className="min-w-0 min-h-[58px] px-1 py-2 text-[11px] md:text-xs font-medium flex flex-col items-center justify-center gap-1 leading-tight data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
            >
              <tab.icon className="w-3.5 h-3.5" />
              <span className="truncate max-w-full">{t(tab.labelKey)}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {/* Life Path Tab */}
        <TabsContent value="life_path" className="max-w-xl mx-auto space-y-6">
          <Card className="bg-card border-0 shadow-soft">
            <CardContent className="p-6">
              <Heading as={3} variant={3}>{t('numerology.calculateNumbers')}</Heading>
              {isAstrologer && (
                <ClientSelector
                  onSelectClient={handleClientSelect}
                  isNewClient={isNewClient}
                  onToggle={handleClientToggle}
                />
              )}
              <div className="space-y-3">
                <Input placeholder={t('numerology.fullName')} value={numName} onChange={(e) => setNumName(e.target.value)} className="bg-card border-sacred-gold" />
                <Input type="date" value={numDob} onChange={(e) => setNumDob(e.target.value)} className="bg-card border-sacred-gold" />
                <Button onClick={calculateNumerology} disabled={numLoading || !numName.trim() || !numDob} className="w-full bg-sacred-gold text-background hover:bg-gray-50 dark">
                  {numLoading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('common.calculating')}</> : <><Hash className="w-4 h-4 mr-2" />{t('numerology.calculate')}</>}
                </Button>
              </div>
            </CardContent>
          </Card>

	          {numResult && (
	            <Card className="bg-card border-0 shadow-soft-lg">
	              <CardContent className="p-6 space-y-6">
	                <Heading as={4} variant={4}>{t('numerology.report')}</Heading>
	                <div className="grid grid-cols-2 gap-4 mb-4">
                  {[
                    { label: t('numerology.lifePath'), value: numResult.life_path, color: 'bg-purple-100 text-purple-700' },
                    { label: t('numerology.destiny'), value: numResult.destiny ?? numResult.expression, color: 'bg-blue-100 text-blue-700' },
                    { label: t('numerology.soulUrge'), value: numResult.soul_urge, color: 'bg-green-100 text-green-800' },
                    { label: t('numerology.personality'), value: numResult.personality, color: 'bg-yellow-100 text-yellow-700' },
                  ].map((n) => (
                    <div key={n.label} className="text-center p-3 rounded-xl bg-card">
                      <p className="text-sm text-muted-foreground mb-1">{n.label}</p>
                      <Badge className={`text-lg px-3 py-1 ${n.color}`}>{n.value}</Badge>
                    </div>
                  ))}
                </div>
                {numResult.summary && <p className="text-sm text-muted-foreground text-center">{numResult.summary}</p>}
	                {numResult.predictions && (
                  Array.isArray(numResult.predictions) ? (
                    numResult.predictions.length > 0 && (
                      <div className="mt-4">
                        <p className="text-sm font-medium text-foreground mb-2">{t('numerology.predictions')}:</p>
                        <ul className="space-y-1">
                          {numResult.predictions.map((p, i) => (
                            <li key={i} className="text-sm text-muted-foreground flex gap-2">
                              <Sparkles className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />{p}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )
                  ) : (
                    <div className="mt-4 space-y-3">
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.predictions')}:</p>
                      {[
                        { key: 'life_path' as const, label: t('numerology.lifePath'), headerColor: 'bg-purple-100 text-purple-800', borderColor: 'border-purple-300' },
                        { key: 'destiny' as const, label: t('numerology.destiny'), headerColor: 'bg-blue-100 text-blue-800', borderColor: 'border-blue-300' },
                        { key: 'soul_urge' as const, label: t('numerology.soulUrge'), headerColor: 'bg-green-100 text-green-800', borderColor: 'border-green-300' },
                        { key: 'personality' as const, label: t('numerology.personality'), headerColor: 'bg-yellow-100 text-yellow-800', borderColor: 'border-yellow-500' },
                      ].map((section) => {
                        const text = (numResult.predictions as NumerologyPredictions)[section.key];
                        if (!text) return null;
                        return (
                          <div key={section.key} className={`rounded-xl border ${section.borderColor} overflow-hidden`}>
                            <div className={`px-4 py-2 ${section.headerColor} font-medium text-sm flex items-center gap-2`}>
                              <Sparkles className="w-4 h-4 shrink-0" />
                              {section.label} {t('numerology.number')}
                            </div>
                            <div className="px-4 py-3">
                              <p className="text-sm text-muted-foreground leading-relaxed">{text}</p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )
	                )}

                {/* New Core Numbers */}
                {(numResult.birthday_number != null || numResult.maturity_number != null) && (
                  <div className="space-y-3">
                    <Heading as={5} variant={5}>{t('numerology.coreNumbers')}</Heading>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {numResult.birthday_number != null && (
                        <div className="rounded-xl border border-sacred-gold/25 bg-sacred-gold/5 p-4">
                          <p className="text-sm font-medium text-foreground">{t('numerology.birthdayNumber')}</p>
                          <div className="flex items-center justify-between mt-2">
                            <Badge className="text-lg bg-sacred-gold text-background">{numResult.birthday_number}</Badge>
                            {numResult.birthday_prediction?.title && (
                              <span className="text-xs text-muted-foreground">
                                {isHi ? numResult.birthday_prediction.title_hi : numResult.birthday_prediction.title}
                              </span>
                            )}
                          </div>
                          {numResult.birthday_prediction?.talent && (
                            <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                              {isHi ? numResult.birthday_prediction.talent_hi : numResult.birthday_prediction.talent}
                            </p>
                          )}
                        </div>
                      )}
                      {numResult.maturity_number != null && (
                        <div className="rounded-xl border border-sacred-gold/25 bg-sacred-gold/5 p-4">
                          <p className="text-sm font-medium text-foreground">{t('numerology.maturityNumber')}</p>
                          <div className="flex items-center justify-between mt-2">
                            <Badge className="text-lg bg-sacred-gold-dark text-white">{numResult.maturity_number}</Badge>
                            {numResult.maturity_prediction?.title && (
                              <span className="text-xs text-muted-foreground">
                                {isHi ? numResult.maturity_prediction.title_hi : numResult.maturity_prediction.title}
                              </span>
                            )}
                          </div>
                          {numResult.maturity_prediction?.theme && (
                            <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                              {isHi ? numResult.maturity_prediction.theme_hi : numResult.maturity_prediction.theme}
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Karmic Debts (only show when present) */}
                {!!numResult.karmic_debts?.length && (
                  <div className="space-y-3">
                    <Heading as={5} variant={5}>{t('numerology.karmicDebts')}</Heading>
                    <div className="space-y-2">
                      {numResult.karmic_debts.map((d: any, i: number) => (
                        <div key={i} className="rounded-xl border border-red-200 bg-red-50 p-4">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-semibold text-red-800">
                              {t('numerology.number')} {d.number}
                            </p>
                            {d.source && (
                              <span className="text-xs text-red-700">
                                {t('numerology.source')}: {isHi ? (d.source_hi || d.source) : d.source}
                              </span>
                            )}
                          </div>
                          {(d.title || d.meaning) && (
                            <p className="text-xs text-red-700 mt-2 leading-relaxed">
                              <span className="font-medium">{isHi ? (d.title_hi || d.title) : d.title}</span>
                              {d.meaning ? `: ${isHi ? (d.meaning_hi || d.meaning) : d.meaning}` : ''}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Hidden Passion + Subconscious Self */}
                {(numResult.hidden_passion || numResult.subconscious_self) && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {numResult.hidden_passion && (
                      <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                        <p className="text-sm font-medium text-foreground">{t('numerology.hiddenPassion')}</p>
                        <div className="flex items-center justify-between mt-2">
                          <Badge className="text-lg bg-amber-100 text-amber-800">{numResult.hidden_passion.number}</Badge>
                          {numResult.hidden_passion.title && (
                            <span className="text-xs text-muted-foreground">
                              {isHi ? (numResult.hidden_passion.title_hi || numResult.hidden_passion.title) : numResult.hidden_passion.title}
                            </span>
                          )}
                        </div>
                        {numResult.hidden_passion.meaning && (
                          <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                            {isHi ? (numResult.hidden_passion.meaning_hi || numResult.hidden_passion.meaning) : numResult.hidden_passion.meaning}
                          </p>
                        )}
                      </div>
                    )}
                    {numResult.subconscious_self && (
                      <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                        <p className="text-sm font-medium text-foreground">{t('numerology.subconsciousSelf')}</p>
                        <div className="flex items-center justify-between mt-2">
                          <Badge className="text-lg bg-indigo-100 text-indigo-800">{numResult.subconscious_self.number}</Badge>
                          {numResult.subconscious_self.title && (
                            <span className="text-xs text-muted-foreground">
                              {isHi ? (numResult.subconscious_self.title_hi || numResult.subconscious_self.title) : numResult.subconscious_self.title}
                            </span>
                          )}
                        </div>
                        {numResult.subconscious_self.meaning && (
                          <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                            {isHi ? (numResult.subconscious_self.meaning_hi || numResult.subconscious_self.meaning) : numResult.subconscious_self.meaning}
                          </p>
                        )}
                        {!!numResult.subconscious_self.missing_numbers?.length && (
                          <p className="text-xs text-muted-foreground mt-2">
                            {t('numerology.missingNumbers')}: {numResult.subconscious_self.missing_numbers.join(', ')}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Karmic Lessons */}
                {!!numResult.karmic_lessons?.length && (
                  <div className="space-y-3">
                    <Heading as={5} variant={5}>{t('numerology.karmicLessons')}</Heading>
                    <div className="space-y-2">
                      {numResult.karmic_lessons.map((l: any, i: number) => (
                        <div key={i} className="rounded-xl border border-sacred-gold/25 bg-sacred-gold/5 p-4">
                          <p className="text-sm font-semibold text-foreground">
                            {t('numerology.number')} {l.number}
                          </p>
                          {l.lesson && (
                            <p className="text-xs text-muted-foreground mt-1">
                              {isHi ? (l.lesson_hi || l.lesson) : l.lesson}
                            </p>
                          )}
                          {l.remedy && (
                            <p className="text-xs text-muted-foreground mt-2">
                              <span className="font-medium">{t('numerology.remedy')}:</span> {isHi ? (l.remedy_hi || l.remedy) : l.remedy}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Forecast (Personal + Universal) */}
                {forecastResult && (
                  <div className="space-y-3">
                    <Heading as={5} variant={5}>{t('numerology.forecast')}</Heading>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                        <p className="text-sm font-medium text-foreground">{t('numerology.personalForecast')}</p>
                        <p className="text-xs text-muted-foreground mt-2">
                          {t('numerology.personalYear')}: <span className="font-semibold text-foreground">{forecastResult.personal_year}</span>
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {t('numerology.personalMonth')}: <span className="font-semibold text-foreground">{forecastResult.personal_month}</span>
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {t('numerology.personalDay')}: <span className="font-semibold text-foreground">{forecastResult.personal_day}</span>
                        </p>
                        {forecastResult.predictions?.personal_day?.description && (
                          <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                            {pick(forecastResult.predictions.personal_day, 'description')}
                          </p>
                        )}
                      </div>
                      <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                        <p className="text-sm font-medium text-foreground">{t('numerology.universalForecast')}</p>
                        <p className="text-xs text-muted-foreground mt-2">
                          {t('numerology.universalYear')}: <span className="font-semibold text-foreground">{forecastResult.universal_year}</span>
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {t('numerology.universalMonth')}: <span className="font-semibold text-foreground">{forecastResult.universal_month}</span>
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {t('numerology.universalDay')}: <span className="font-semibold text-foreground">{forecastResult.universal_day}</span>
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Pinnacles / Challenges / Life Cycles */}
                {(numResult.pinnacles?.pinnacles || numResult.challenges?.challenges || numResult.life_cycles?.cycles) && (
                  <div className="space-y-4">
                    {!!numResult.pinnacles?.pinnacles?.length && (
                      <div className="space-y-2">
                        <Heading as={5} variant={5}>{t('numerology.pinnacles')}</Heading>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {numResult.pinnacles.pinnacles.map((p: any, i: number) => (
                            <div key={i} className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                              <p className="text-sm font-semibold text-foreground">{t('numerology.pinnacle')} {i + 1}</p>
                              <p className="text-xs text-muted-foreground mt-1">{t('numerology.period')}: {p.period}</p>
                              <Badge className="mt-2 bg-purple-100 text-purple-800">{p.number}</Badge>
                              {p.prediction?.title && (
                                <p className="text-xs text-muted-foreground mt-2">
                                  {isHi ? (p.prediction.title_hi || p.prediction.title) : p.prediction.title}
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {!!numResult.challenges?.challenges?.length && (
                      <div className="space-y-2">
                        <Heading as={5} variant={5}>{t('numerology.challengesTitle')}</Heading>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {numResult.challenges.challenges.map((c: any, i: number) => (
                            <div key={i} className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                              <p className="text-sm font-semibold text-foreground">{t('numerology.challenge')} {i + 1}</p>
                              <p className="text-xs text-muted-foreground mt-1">{t('numerology.period')}: {c.period}</p>
                              <Badge className="mt-2 bg-blue-100 text-blue-800">{c.number}</Badge>
                              {c.prediction?.title && (
                                <p className="text-xs text-muted-foreground mt-2">
                                  {isHi ? (c.prediction.title_hi || c.prediction.title) : c.prediction.title}
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {!!numResult.life_cycles?.cycles?.length && (
                      <div className="space-y-2">
                        <Heading as={5} variant={5}>{t('numerology.lifeCyclesTitle')}</Heading>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                          {numResult.life_cycles.cycles.map((c: any, i: number) => (
                            <div key={i} className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                              <p className="text-sm font-semibold text-foreground">{t('numerology.lifeCycle')} {i + 1}</p>
                              <p className="text-xs text-muted-foreground mt-1">{c.period}</p>
                              <Badge className="mt-2 bg-green-100 text-green-800">{c.number}</Badge>
                              {c.prediction?.title && (
                                <p className="text-xs text-muted-foreground mt-2">
                                  {isHi ? (c.prediction.title_hi || c.prediction.title) : c.prediction.title}
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Lo Shu Grid + Arrows + Planes */}
                {(numResult.loshu_grid && numResult.loshu_values) && (
                  <div className="space-y-4">
                    <Heading as={5} variant={5}>{t('numerology.loshuGrid')}</Heading>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-start">
                      <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                        <div className="grid grid-cols-3 gap-2">
                          {numResult.loshu_grid.flat().map((cell: number, idx: number) => {
                            const v = numResult.loshu_values?.[cell] || '';
                            const strengthNums = new Set<number>((numResult.loshu_arrows?.arrows_of_strength || []).flatMap((a: any) => a.numbers || []));
                            const weaknessNums = new Set<number>((numResult.loshu_arrows?.arrows_of_weakness || []).flatMap((a: any) => a.numbers || []));
                            const isStrength = strengthNums.has(cell);
                            const isWeakness = weaknessNums.has(cell);
                            const isMissing = !v;
                            const boxClass = isStrength
                              ? 'border-green-300 bg-green-50'
                              : isWeakness
                                ? 'border-red-300 bg-red-50'
                                : 'border-sacred-gold/25 bg-card';
                            return (
                              <div key={idx} className={`rounded-lg border ${boxClass} p-2 text-center`}>
                                <p className="text-[10px] text-muted-foreground">{cell}</p>
                                <p className={`text-sm font-semibold ${isMissing ? 'text-muted-foreground' : 'text-foreground'}`}>
                                  {v || t('report.notAvailable')}
                                </p>
                              </div>
                            );
                          })}
                        </div>
                        <p className="text-[11px] text-muted-foreground mt-3">
                          {t('numerology.loshuLegend')}
                        </p>
                      </div>

                      <div className="space-y-3">
                        {!!numResult.loshu_arrows?.arrows_of_strength?.length && (
                          <div className="rounded-xl border border-green-200 bg-green-50 p-4">
                            <p className="text-sm font-semibold text-green-800">{t('numerology.arrowsOfStrength')}</p>
                            <div className="mt-2 space-y-2">
                              {numResult.loshu_arrows.arrows_of_strength.map((a: any) => (
                                <div key={a.key} className="text-xs text-green-800">
                                  <span className="font-medium">{isHi ? (a.name_hi || a.name) : a.name}</span>
                                  {a.meaning ? `: ${isHi ? (a.meaning_hi || a.meaning) : a.meaning}` : ''}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        {!!numResult.loshu_arrows?.arrows_of_weakness?.length && (
                          <div className="rounded-xl border border-red-200 bg-red-50 p-4">
                            <p className="text-sm font-semibold text-red-800">{t('numerology.arrowsOfWeakness')}</p>
                            <div className="mt-2 space-y-2">
                              {numResult.loshu_arrows.arrows_of_weakness.map((a: any) => (
                                <div key={a.key} className="text-xs text-red-800">
                                  <span className="font-medium">{isHi ? (a.name_hi || a.name) : a.name}</span>
                                  {a.missing_meaning ? `: ${isHi ? (a.missing_meaning_hi || a.missing_meaning) : a.missing_meaning}` : ''}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {numResult.loshu_planes && (
                          <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                            <p className="text-sm font-semibold text-foreground">{t('numerology.planes')}</p>
                            <div className="mt-2 grid grid-cols-3 gap-2">
                              {(['mental', 'emotional', 'practical'] as const).map((k) => (
                                <div key={k} className="rounded-lg border border-sacred-gold/20 bg-sacred-gold/5 p-2 text-center">
                                  <p className="text-[10px] text-muted-foreground">
                                    {isHi ? (numResult.loshu_planes[k]?.name_hi || numResult.loshu_planes[k]?.name) : numResult.loshu_planes[k]?.name}
                                  </p>
                                  <p className="text-sm font-semibold text-foreground">
                                    {numResult.loshu_planes[k]?.score} ({numResult.loshu_planes[k]?.percentage}%)
                                  </p>
                                </div>
                              ))}
                            </div>
                            {(numResult.loshu_planes.interpretation || numResult.loshu_planes.interpretation_hi) && (
                              <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                                {pick(numResult.loshu_planes, 'interpretation')}
                              </p>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Missing Numbers Remedies (DOB) */}
                {!!numResult.missing_numbers?.length && (
                  <div className="space-y-3">
                    <Heading as={5} variant={5}>{t('numerology.missingNumbers')}</Heading>
                    <div className="space-y-2">
                      {numResult.missing_numbers.map((m: any) => (
                        <div key={m.number} className="rounded-xl border border-sacred-gold/25 bg-sacred-gold/5 p-4">
                          <p className="text-sm font-semibold text-foreground">{t('numerology.number')} {m.number}</p>
                          {m.meaning && <p className="text-xs text-muted-foreground mt-1">{pick(m, 'meaning')}</p>}
                          {m.remedy && (
                            <p className="text-xs text-muted-foreground mt-2">
                              <span className="font-medium">{t('numerology.remedy')}:</span> {pick(m, 'remedy')}
                            </p>
                          )}
                          <div className="mt-2 grid grid-cols-2 gap-2 text-[11px] text-muted-foreground">
                            {m.color && <div>{t('numerology.color')}: {pick(m, 'color')}</div>}
                            {m.gemstone && <div>{t('numerology.gemstone')}: {pick(m, 'gemstone')}</div>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Repeated Numbers */}
                {!!numResult.repeated_numbers?.length && (
                  <div className="space-y-3">
                    <Heading as={5} variant={5}>{t('numerology.repeatedNumbers')}</Heading>
                    <div className="space-y-2">
                      {numResult.repeated_numbers.map((r: any) => (
                        <div key={r.number} className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                          <p className="text-sm font-semibold text-foreground">{t('numerology.number')} {r.number}</p>
                          <p className="text-xs text-muted-foreground mt-1">{t('numerology.count')}: {r.count}</p>
                          {r.meaning && <p className="text-xs text-muted-foreground mt-1">{pick(r, 'meaning')}</p>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
	              </CardContent>
	            </Card>
	          )}
      </TabsContent>

      {/* Mobile Tab */}
      <TabsContent value="mobile" className="max-w-2xl mx-auto space-y-6">
          <Card className="bg-card border-0 shadow-soft">
            <CardContent className="p-6">
              <Heading as={3} variant={3}>{t('numerology.mobileAnalyzeHeading')}</Heading>
              {isAstrologer && (
                <ClientSelector
                  onSelectClient={handleMobileClientSelect}
                  isNewClient={mobileIsNewClient}
                  onToggle={handleMobileClientToggle}
                />
              )}
              <div className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="block text-sm text-muted-foreground mb-1">{t('numerology.firstName')} <span className="text-red-600">*</span></label>
                    <Input placeholder={t('numerology.firstName')} value={firstName} onChange={(e) => setFirstName(e.target.value)} className="bg-card border-sacred-gold" />
                  </div>
                  <div>
                    <label className="block text-sm text-muted-foreground mb-1">{t('numerology.middleName')}</label>
                    <Input placeholder={`${t('numerology.middleName')} ${t('numerology.optional')}`} value={middleName} onChange={(e) => setMiddleName(e.target.value)} className="bg-card border-sacred-gold" />
                  </div>
                  <div>
                    <label className="block text-sm text-muted-foreground mb-1">{t('numerology.lastName')}</label>
                    <Input placeholder={t('numerology.lastName')} value={lastName} onChange={(e) => setLastName(e.target.value)} className="bg-card border-sacred-gold" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm text-muted-foreground mb-1">{t('numerology.mobileNumber')} <span className="text-red-600">*</span></label>
                  <div className="flex gap-2">
                    <Select value={mobileCountryCode} onValueChange={setMobileCountryCode}>
                      <SelectTrigger className="w-24 bg-card border-sacred-gold shrink-0">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="+91">+91</SelectItem>
                        <SelectItem value="+1">+1</SelectItem>
                        <SelectItem value="+44">+44</SelectItem>
                        <SelectItem value="+61">+61</SelectItem>
                        <SelectItem value="+971">+971</SelectItem>
                        <SelectItem value="+65">+65</SelectItem>
                        <SelectItem value="+49">+49</SelectItem>
                        <SelectItem value="+33">+33</SelectItem>
                        <SelectItem value="+81">+81</SelectItem>
                        <SelectItem value="+86">+86</SelectItem>
                      </SelectContent>
                    </Select>
                    <div className="relative flex-1">
                      <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                      <Input placeholder="9876543210" value={mobilePhone} onChange={(e) => setMobilePhone(e.target.value.replace(/\D/g, ''))} className="bg-card border-sacred-gold pl-10" maxLength={15} />
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-sm text-muted-foreground mb-1">{t('numerology.dateOfBirth')} <span className="text-red-600">*</span></label>
                  <Input type="date" value={mobileDob} onChange={(e) => setMobileDob(e.target.value)} className="bg-card border-sacred-gold" />
                </div>

                <div>
                  <label className="block text-sm text-muted-foreground mb-2">{t('numerology.areaOfStruggle')}</label>
                  <div className="flex flex-wrap gap-3">
                    {['Health', 'Relationship', 'Career', 'Money', 'Job'].map((area) => (
                      <label
                        key={area}
                        onClick={() => toggleArea(area)}
                        className={`inline-flex items-center gap-2 px-3 py-2 rounded-lg border cursor-pointer transition-all text-sm ${
                          selectedAreas.includes(area)
                            ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold-dark font-medium'
                            : 'border-gray-300 bg-white text-muted-foreground hover:border-sacred-gold'
                        }`}
                      >
                        <input type="checkbox" checked={selectedAreas.includes(area)} onChange={() => {}} className="sr-only" />
                        {t('numerology.struggle.' + area.toLowerCase())}
                      </label>
                    ))}
                  </div>
                </div>

                <Button onClick={analyzeMobile} disabled={mobileLoading || !mobilePhone.trim() || !firstName.trim() || !mobileDob} className="w-full bg-sacred-gold text-background hover:bg-gray-50 dark">
                  {mobileLoading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('numerology.analyzing')}</> : <><Phone className="w-4 h-4 mr-2" />{t('numerology.analyzeMobileButton')}</>}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Mobile Results */}
          {mobileResult && (
            <Card className="bg-card border-0 shadow-soft-lg">
              <CardContent className="p-6 space-y-4">
                <div className="text-center pb-4 border-b border-sacred-gold/20">
                  <Heading as={4} variant={4}>{t('numerology.reportHeader')}</Heading>
                  <p className="text-sm text-foreground mt-1">{mobileResult.phone_number}</p>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-3 bg-sacred-gold/5 rounded-lg">
                    <p className="text-xs text-muted-foreground mb-1">{t('numerology.mobile.compound')}</p>
                    <Badge className="text-lg bg-purple-100 text-purple-700">{mobileResult.compound_number}</Badge>
                  </div>
                  <div className="text-center p-3 bg-sacred-gold/5 rounded-lg">
                    <p className="text-xs text-muted-foreground mb-1">{t('numerology.mobile.total')}</p>
                    <Badge className="text-lg bg-sacred-gold text-background">{mobileResult.mobile_total}</Badge>
                  </div>
                  <div className="text-center p-3 bg-sacred-gold/5 rounded-lg">
                    <p className="text-xs text-muted-foreground mb-1">{t('numerology.mobile.status')}</p>
                    <Badge className={mobileResult.is_recommended ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                      {mobileResult.is_recommended ? t('numerology.mobile.status.good') : t('numerology.mobile.status.caution')}
                    </Badge>
                  </div>
                </div>

                {mobileResult.recommendation_message && (
                  <div className={`p-3 rounded-lg text-center text-sm ${mobileResult.is_recommended ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                    {mobileResult.recommendation_message}
                  </div>
                )}
              </CardContent>
            </Card>
          )}
      </TabsContent>

      {/* Name Tab */}
      <TabsContent value="name"><NameNumerology birthDate={numDob} /></TabsContent>

      {/* Vehicle Tab */}
      <TabsContent value="vehicle"><VehicleNumerology birthDate={numDob} /></TabsContent>

      {/* House Tab */}
      <TabsContent value="house"><HouseNumerology birthDate={numDob} /></TabsContent>
    </Tabs>
  </div>
  );
}
