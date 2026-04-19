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

interface PredictionEntry {
  theme?: string;
  theme_hi?: string;
  description?: string;
  description_hi?: string;
  focus_areas?: string[];
  focus_areas_hi?: string[];
  advice?: string;
  advice_hi?: string;
  lucky_months?: number[];
}

interface NumerologyPredictions {
  life_path: string | PredictionEntry;
  destiny: string | PredictionEntry;
  soul_urge: string | PredictionEntry;
  personality: string | PredictionEntry;
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
  compound_number: number;
  mobile_total: number;

  // Prediction & qualities
  prediction?: Record<string, any>;
  lucky_qualities?: string[];
  challenges?: string[];
  best_for?: string;
  compatibility_numbers?: number[];

  // Lucky / Unlucky
  lucky_colors?: string[];
  unlucky_colors?: string[];
  lucky_numbers?: number[];
  unlucky_numbers?: number[];
  neutral_numbers?: number[];

  // Missing numbers (simple digit list OR enriched objects from DOB analysis)
  missing_numbers?: number[] | Array<{ number: number; meaning?: string; meaning_hi?: string; remedy?: string; remedy_hi?: string; color?: string; color_hi?: string; gemstone?: string; gemstone_hi?: string }>;

  // Mobile combinations
  mobile_combinations?: MobileCombination[];
  has_malefic?: boolean;
  benefic_count?: number;
  malefic_count?: number;
  recommendation?: string;

  // Affirmations (dict keyed by area)
  affirmations?: Record<string, string> | AreaAffirmation[];

  // Vibration / legacy
  vibration_number?: number;
  total_sum?: number;

  // DOB-based
  loshu_grid?: number[][];
  loshu_values?: Record<number, string>;
  loshu_arrows?: any;
  loshu_planes?: any;
  vedic_grid?: number[][];
  vedic_values?: Record<number, string>;
  repeated_numbers?: Array<{ number: number; count: number; meaning?: string; meaning_hi?: string }>;
  recommended_totals?: number[];
  is_recommended?: boolean;
  life_path?: number;

  // Backward compat aliases
  recommendation_message?: string;
  combinations?: MobileCombination[];
  lucky_colours?: string[];
  unlucky_colours?: string[];
  predictions?: string[];
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

      {/* Kundli-style user info header — shown after result is ready */}
      {numResult && numName && (
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-2">
          <div className="flex items-center gap-3 min-w-0">
            <div className="min-w-0">
              <h3 className="font-bold text-xl sm:text-2xl text-sacred-brown truncate">{numName} — {t('numerology.lifePath')}</h3>
              <p className="text-sm text-gray-500 truncate">{numDob}</p>
            </div>
          </div>
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
        <TabsContent value="life_path" className="space-y-6">
          <div className="max-w-4xl mx-auto">
          <Card className="bg-card border-sacred-gold/20 shadow-soft">
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
        </div>

	          {numResult && (
	            <Card className="bg-card border-sacred-gold/10 shadow-soft-lg">
	              <CardContent className="p-6 space-y-8">
	                <Heading as={4} variant={4} className="text-center">{t('numerology.report')}</Heading>
	                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
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
                        const pred = (numResult.predictions as NumerologyPredictions)[section.key];
                        if (!pred) return null;
                        const isStructured = typeof pred === 'object';
                        const theme = isStructured ? pick(pred as any, 'theme') : '';
                        const description = isStructured ? pick(pred as any, 'description') : (pred as string);
                        const focusAreas: string[] = isStructured
                          ? ((isHi && (pred as any).focus_areas_hi) ? (pred as any).focus_areas_hi : (pred as any).focus_areas) || []
                          : [];
                        const advice = isStructured ? pick(pred as any, 'advice') : '';
                        const luckyMonths: number[] = isStructured ? (pred as any).lucky_months || [] : [];
                        return (
                          <div key={section.key} className={`rounded-xl border ${section.borderColor} overflow-hidden`}>
                            <div className={`px-4 py-2 ${section.headerColor} font-medium text-sm flex items-center gap-2`}>
                              <Sparkles className="w-4 h-4 shrink-0" />
                              {section.label} {t('numerology.number')}
                              {theme && <span className="ml-auto text-xs font-normal opacity-80">{theme}</span>}
                            </div>
                            <div className="px-4 py-3 space-y-2">
                              {description && <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>}
                              {!!focusAreas.length && (
                                <p className="text-xs text-muted-foreground">
                                  <span className="font-medium text-foreground">{isHi ? 'फोकस क्षेत्र' : 'Focus Areas'}:</span>{' '}
                                  {Array.isArray(focusAreas) ? focusAreas.join(', ') : focusAreas}
                                </p>
                              )}
                              {advice && (
                                <p className="text-xs text-muted-foreground">
                                  <span className="font-medium text-foreground">{isHi ? 'सलाह' : 'Advice'}:</span>{' '}
                                  {advice}
                                </p>
                              )}
                              {!!luckyMonths.length && (
                                <div className="flex gap-1 items-center flex-wrap">
                                  <span className="text-xs text-muted-foreground font-medium">{isHi ? 'भाग्यशाली महीने' : 'Lucky Months'}:</span>
                                  {luckyMonths.map((m: number) => (
                                    <Badge key={m} className="bg-sacred-gold/20 text-sacred-gold-dark text-[10px] px-1.5 py-0">{m}</Badge>
                                  ))}
                                </div>
                              )}
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

                {/* Personal Year (from calculate endpoint) */}
                {numResult.personal_year != null && numResult.personal_year_prediction && (
                  <div className="space-y-2">
                    <Heading as={5} variant={5}>{isHi ? 'वर्तमान व्यक्तिगत वर्ष' : 'Current Personal Year'}</Heading>
                    <div className="rounded-xl border border-sacred-gold/25 bg-white p-4 space-y-2">
                      <div className="flex items-center gap-3">
                        <Badge className="text-xl px-3 py-1 bg-sacred-gold text-background">{numResult.personal_year}</Badge>
                        {numResult.personal_year_prediction?.theme && (
                          <span className="text-sm font-medium text-sacred-gold-dark">
                            {pick(numResult.personal_year_prediction, 'theme')}
                          </span>
                        )}
                      </div>
                      {numResult.personal_year_prediction?.description && (
                        <p className="text-xs text-muted-foreground leading-relaxed">
                          {pick(numResult.personal_year_prediction, 'description')}
                        </p>
                      )}
                      {numResult.personal_year_prediction?.advice && (
                        <p className="text-xs text-muted-foreground">
                          <span className="font-medium text-foreground">{isHi ? 'सलाह' : 'Advice'}:</span>{' '}
                          {pick(numResult.personal_year_prediction, 'advice')}
                        </p>
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
                        {numResult.hidden_passion.tie_detected && !!numResult.hidden_passion.tied_numbers?.length && (
                          <div className="mt-2 border-t border-amber-200 pt-2">
                            <p className="text-[10px] text-amber-700 font-medium">
                              {isHi ? 'बंधे हुए अंक' : 'Tied with'}: {numResult.hidden_passion.tied_numbers.join(', ')}
                            </p>
                            {numResult.hidden_passion.tied_meanings && Object.keys(numResult.hidden_passion.tied_meanings).length > 1 && (
                              <div className="mt-1 space-y-1">
                                {Object.entries(numResult.hidden_passion.tied_meanings).map(([n, m]: [string, any]) => (
                                  <p key={n} className="text-[10px] text-muted-foreground">
                                    <span className="font-medium text-foreground">{n}:</span>{' '}
                                    {isHi ? (m.meaning_hi || m.meaning) : m.meaning}
                                  </p>
                                ))}
                              </div>
                            )}
                          </div>
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
                      <div className="rounded-xl border border-sacred-gold/25 bg-white p-4 space-y-2">
                        <p className="text-sm font-medium text-foreground">{t('numerology.personalForecast')}</p>

                        {/* Personal Year */}
                        <div>
                          <p className="text-xs text-muted-foreground">
                            {t('numerology.personalYear')}: <span className="font-semibold text-foreground">{forecastResult.personal_year}</span>
                            {forecastResult.predictions?.personal_year?.theme && (
                              <span className="ml-1 text-sacred-gold-dark font-medium">
                                · {pick(forecastResult.predictions.personal_year, 'theme')}
                              </span>
                            )}
                          </p>
                          {forecastResult.predictions?.personal_year?.description && (
                            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                              {pick(forecastResult.predictions.personal_year, 'description')}
                            </p>
                          )}
                          {forecastResult.predictions?.personal_year?.focus_areas && (
                            <p className="text-xs text-muted-foreground mt-1">
                              <span className="font-medium text-foreground">{isHi ? 'फोकस क्षेत्र' : 'Focus Areas'}:</span>{' '}
                              {pick(forecastResult.predictions.personal_year, 'focus_areas')}
                            </p>
                          )}
                          {forecastResult.predictions?.personal_year?.advice && (
                            <p className="text-xs text-muted-foreground mt-1">
                              <span className="font-medium text-foreground">{isHi ? 'सलाह' : 'Advice'}:</span>{' '}
                              {pick(forecastResult.predictions.personal_year, 'advice')}
                            </p>
                          )}
                          {!!forecastResult.predictions?.personal_year?.lucky_months?.length && (
                            <div className="mt-2 flex flex-wrap gap-1 items-center">
                              <span className="text-xs text-muted-foreground font-medium">{isHi ? 'भाग्यशाली महीने' : 'Lucky Months'}:</span>
                              {forecastResult.predictions.personal_year.lucky_months.map((m: number) => (
                                <Badge key={m} className="bg-sacred-gold/20 text-sacred-gold-dark text-[10px] px-1.5 py-0">{m}</Badge>
                              ))}
                            </div>
                          )}
                        </div>

                        {/* Personal Month */}
                        <div className="pt-2 border-t border-sacred-gold/10">
                          <p className="text-xs text-muted-foreground">
                            {t('numerology.personalMonth')}: <span className="font-semibold text-foreground">{forecastResult.personal_month}</span>
                            {forecastResult.predictions?.personal_month?.theme && (
                              <span className="ml-1 text-sacred-gold-dark font-medium">
                                · {pick(forecastResult.predictions.personal_month, 'theme')}
                              </span>
                            )}
                          </p>
                          {forecastResult.predictions?.personal_month?.description && (
                            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                              {pick(forecastResult.predictions.personal_month, 'description')}
                            </p>
                          )}
                        </div>

                        {/* Personal Day */}
                        <div className="pt-2 border-t border-sacred-gold/10">
                          <p className="text-xs text-muted-foreground">
                            {t('numerology.personalDay')}: <span className="font-semibold text-foreground">{forecastResult.personal_day}</span>
                          </p>
                          {forecastResult.predictions?.personal_day?.description && (
                            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                              {pick(forecastResult.predictions.personal_day, 'description')}
                            </p>
                          )}
                        </div>
                      </div>

                      <div className="rounded-xl border border-sacred-gold/25 bg-white p-4 space-y-2">
                        <p className="text-sm font-medium text-foreground">{t('numerology.universalForecast')}</p>

                        {/* Universal Year */}
                        <div>
                          <p className="text-xs text-muted-foreground">
                            {t('numerology.universalYear')}: <span className="font-semibold text-foreground">{forecastResult.universal_year}</span>
                            {forecastResult.predictions?.universal_year?.theme && (
                              <span className="ml-1 text-sacred-gold-dark font-medium">
                                · {pick(forecastResult.predictions.universal_year, 'theme')}
                              </span>
                            )}
                          </p>
                          {forecastResult.predictions?.universal_year?.description && (
                            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                              {pick(forecastResult.predictions.universal_year, 'description')}
                            </p>
                          )}
                          {forecastResult.predictions?.universal_year?.advice && (
                            <p className="text-xs text-muted-foreground mt-1">
                              <span className="font-medium text-foreground">{isHi ? 'सलाह' : 'Advice'}:</span>{' '}
                              {pick(forecastResult.predictions.universal_year, 'advice')}
                            </p>
                          )}
                        </div>

                        {/* Universal Month */}
                        <div className="pt-2 border-t border-sacred-gold/10">
                          <p className="text-xs text-muted-foreground">
                            {t('numerology.universalMonth')}: <span className="font-semibold text-foreground">{forecastResult.universal_month}</span>
                            {forecastResult.predictions?.universal_month?.theme && (
                              <span className="ml-1 text-sacred-gold-dark font-medium">
                                · {pick(forecastResult.predictions.universal_month, 'theme')}
                              </span>
                            )}
                          </p>
                        </div>

                        {/* Universal Day */}
                        <div className="pt-2 border-t border-sacred-gold/10">
                          <p className="text-xs text-muted-foreground">
                            {t('numerology.universalDay')}: <span className="font-semibold text-foreground">{forecastResult.universal_day}</span>
                            {forecastResult.predictions?.universal_day?.theme && (
                              <span className="ml-1 text-sacred-gold-dark font-medium">
                                · {pick(forecastResult.predictions.universal_day, 'theme')}
                              </span>
                            )}
                          </p>
                        </div>
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
                              <p className="text-xs text-muted-foreground mt-1">
                                {t('numerology.period')}: {isHi ? (p.period_hi || p.period) : p.period}
                              </p>
                              <Badge className="mt-2 bg-purple-100 text-purple-800">{p.number}</Badge>
                              {p.prediction?.title && (
                                <p className="text-xs text-muted-foreground mt-2 font-medium">
                                  {isHi ? (p.prediction.title_hi || p.prediction.title) : p.prediction.title}
                                </p>
                              )}
                              {p.prediction?.opportunity && (
                                <p className="text-xs text-green-700 mt-1 leading-relaxed">
                                  ✦ {isHi ? (p.prediction.opportunity_hi || p.prediction.opportunity) : p.prediction.opportunity}
                                </p>
                              )}
                              {p.prediction?.lesson && (
                                <p className="text-xs text-amber-700 mt-1 leading-relaxed">
                                  ◈ {isHi ? (p.prediction.lesson_hi || p.prediction.lesson) : p.prediction.lesson}
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
                              <p className="text-xs text-muted-foreground mt-1">
                                {t('numerology.period')}: {isHi ? (c.period_hi || c.period) : c.period}
                              </p>
                              <Badge className="mt-2 bg-blue-100 text-blue-800">{c.number}</Badge>
                              {c.prediction?.title && (
                                <p className="text-xs text-muted-foreground mt-2 font-medium">
                                  {isHi ? (c.prediction.title_hi || c.prediction.title) : c.prediction.title}
                                </p>
                              )}
                              {c.prediction?.obstacle && (
                                <p className="text-xs text-green-700 mt-1 leading-relaxed">
                                  ✦ {isHi ? (c.prediction.obstacle_hi || c.prediction.obstacle) : c.prediction.obstacle}
                                </p>
                              )}
                              {c.prediction?.growth && (
                                <p className="text-xs text-amber-700 mt-1 leading-relaxed">
                                  ◈ {isHi ? (c.prediction.growth_hi || c.prediction.growth) : c.prediction.growth}
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
                              <p className="text-xs text-muted-foreground mt-1">
                                {isHi ? (c.period_hi || c.period) : c.period}
                              </p>
                              {c.stage_note && (
                                <p className="text-[10px] text-blue-600 italic mt-0.5">
                                  {isHi ? (c.stage_note_hi || c.stage_note) : c.stage_note}
                                </p>
                              )}
                              <Badge className="mt-2 bg-green-100 text-green-800">{c.number}</Badge>
                              {c.prediction?.title && (
                                <p className="text-xs text-muted-foreground mt-2 font-medium">
                                  {isHi ? (c.prediction.title_hi || c.prediction.title) : c.prediction.title}
                                </p>
                              )}
                              {c.prediction?.theme && (
                                <p className="text-xs text-green-700 mt-1 leading-relaxed">
                                  ✦ {isHi ? (c.prediction.theme_hi || c.prediction.theme) : c.prediction.theme}
                                </p>
                              )}
                              {c.prediction?.advice && (
                                <p className="text-xs text-amber-700 mt-1 leading-relaxed">
                                  ◈ {isHi ? (c.prediction.advice_hi || c.prediction.advice) : c.prediction.advice}
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
                            const count = v ? v.length : 0;
                            const strengthNums = new Set<number>((numResult.loshu_arrows?.arrows_of_strength || []).flatMap((a: any) => a.numbers || []));
                            const weaknessNums = new Set<number>((numResult.loshu_arrows?.arrows_of_weakness || []).flatMap((a: any) => a.numbers || []));
                            const isStrength = strengthNums.has(cell);
                            const isWeakness = weaknessNums.has(cell);
                            const isPresent = count > 0;
                            const boxClass = isStrength
                              ? 'border-green-400 bg-green-50'
                              : isWeakness
                                ? 'border-red-300 bg-red-50'
                                : isPresent
                                  ? 'border-sacred-gold/40 bg-sacred-gold/5'
                                  : 'border-gray-200 bg-gray-50';
                            return (
                              <div key={idx} className={`rounded-lg border-2 ${boxClass} p-3 text-center`}>
                                <p className={`text-lg font-bold ${isPresent ? 'text-foreground' : 'text-gray-300'}`}>{cell}</p>
                                {count > 1 && <p className="text-[10px] text-sacred-gold-dark font-medium">×{count}</p>}
                              </div>
                            );
                          })}
                        </div>
                        <p className="text-[10px] text-muted-foreground mt-3 flex gap-3 justify-center">
                          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-green-400 inline-block" /> {isHi ? 'शक्ति' : 'Strength'}</span>
                          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-red-300 inline-block" /> {isHi ? 'कमज़ोरी' : 'Weakness'}</span>
                          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-gray-200 inline-block" /> {isHi ? 'अनुपस्थित' : 'Absent'}</span>
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
                                  {numResult.loshu_planes[k]?.interpretation && (
                                    <p className="text-[9px] text-muted-foreground mt-1 italic leading-tight">
                                      {isHi ? (numResult.loshu_planes[k]?.interpretation_hi || numResult.loshu_planes[k]?.interpretation) : numResult.loshu_planes[k]?.interpretation}
                                    </p>
                                  )}
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
                    <div className="flex items-center gap-2">
                      <Heading as={5} variant={5}>{t('numerology.missingNumbers')}</Heading>
                      {(numResult as any).missing_numbers_source && (
                        <Badge className="bg-gray-100 text-gray-600 text-[10px] font-normal">
                          {isHi ? 'स्रोत: जन्म तिथि' : 'Source: Birth Date'}
                        </Badge>
                      )}
                    </div>
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
      <TabsContent value="mobile" className="space-y-6">
          <div className="max-w-4xl mx-auto">
          <Card className="bg-card border-sacred-gold/20 shadow-soft">
            <CardContent className="p-6">
              <Heading as={3} variant={3} className="mb-6">{t('numerology.mobileAnalyzeHeading')}</Heading>
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
              </div>
            </CardContent>
          </Card>
        </div>

          {/* Mobile Results */}
          {mobileResult && (
            <div className="space-y-4">
            {/* Header: Compound / Total / Status */}
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

                {/* Recommendation message */}
                {(mobileResult.recommendation || mobileResult.recommendation_message) && (
                  <div className={`p-3 rounded-lg text-center text-sm ${mobileResult.is_recommended ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                    {mobileResult.recommendation || mobileResult.recommendation_message}
                  </div>
                )}

                {/* Life Path + Recommended Totals */}
                {(mobileResult.life_path != null || !!mobileResult.recommended_totals?.length) && (
                  <div className="flex flex-wrap gap-3 items-center justify-center">
                    {mobileResult.life_path != null && (
                      <div className="text-center p-2 bg-purple-50 rounded-lg">
                        <p className="text-[10px] text-muted-foreground">{t('numerology.mobile.lifePath')}</p>
                        <Badge className="bg-purple-100 text-purple-700">{mobileResult.life_path}</Badge>
                      </div>
                    )}
                    {!!mobileResult.recommended_totals?.length && (
                      <div className="text-center p-2 bg-blue-50 rounded-lg">
                        <p className="text-[10px] text-muted-foreground">{t('numerology.mobile.recommendedTotals')}</p>
                        <div className="flex gap-1 mt-1 justify-center">
                          {mobileResult.recommended_totals.map((n) => (
                            <Badge key={n} className={`text-xs ${mobileResult.mobile_total === n ? 'bg-green-200 text-green-800' : 'bg-blue-100 text-blue-700'}`}>{n}</Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Prediction & Qualities */}
            {(mobileResult.prediction || mobileResult.lucky_qualities || mobileResult.challenges || mobileResult.best_for) && (
              <Card className="bg-card border-0 shadow-soft">
                <CardContent className="p-6 space-y-4">
                  <Heading as={5} variant={5}>{t('numerology.mobile.prediction')}</Heading>

                  {mobileResult.prediction && (
                    <div className="text-sm text-muted-foreground leading-relaxed">
                      {typeof mobileResult.prediction === 'string'
                        ? mobileResult.prediction
                        : (isHi
                            ? (mobileResult.prediction.description_hi || mobileResult.prediction.description || mobileResult.prediction.title_hi || mobileResult.prediction.title || JSON.stringify(mobileResult.prediction))
                            : (mobileResult.prediction.description || mobileResult.prediction.title || JSON.stringify(mobileResult.prediction))
                          )}
                    </div>
                  )}

                  {!!mobileResult.lucky_qualities?.length && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.luckyQualities')}</p>
                      <div className="flex flex-wrap gap-2">
                        {mobileResult.lucky_qualities.map((q, i) => (
                          <Badge key={i} className="bg-green-100 text-green-800 text-xs">{q}</Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {!!mobileResult.challenges?.length && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.challenges')}</p>
                      <div className="flex flex-wrap gap-2">
                        {mobileResult.challenges.map((c, i) => (
                          <Badge key={i} className="bg-red-100 text-red-800 text-xs">{c}</Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {mobileResult.best_for && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-1">{t('numerology.mobile.bestFor')}</p>
                      <p className="text-sm text-muted-foreground">{mobileResult.best_for}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Lucky / Unlucky Numbers */}
            {(!!mobileResult.lucky_numbers?.length || !!mobileResult.unlucky_numbers?.length || !!mobileResult.neutral_numbers?.length) && (
              <Card className="bg-card border-0 shadow-soft">
                <CardContent className="p-6 space-y-4">
                  {!!mobileResult.lucky_numbers?.length && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.luckyNumbers')}</p>
                      <div className="flex flex-wrap gap-2">
                        {mobileResult.lucky_numbers.map((n) => (
                          <Badge key={n} className="bg-green-100 text-green-800 text-sm px-3 py-1">{n}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  {!!mobileResult.unlucky_numbers?.length && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.unluckyNumbers')}</p>
                      <div className="flex flex-wrap gap-2">
                        {mobileResult.unlucky_numbers.map((n) => (
                          <Badge key={n} className="bg-red-100 text-red-800 text-sm px-3 py-1">{n}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  {!!mobileResult.neutral_numbers?.length && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.neutralNumbers')}</p>
                      <div className="flex flex-wrap gap-2">
                        {mobileResult.neutral_numbers.map((n) => (
                          <Badge key={n} className="bg-gray-100 text-gray-700 text-sm px-3 py-1">{n}</Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Compatibility Numbers */}
                  {!!mobileResult.compatibility_numbers?.length && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.compatibilityNumbers')}</p>
                      <div className="flex flex-wrap gap-2">
                        {mobileResult.compatibility_numbers.map((n) => (
                          <Badge key={n} className="bg-blue-100 text-blue-700 text-sm px-3 py-1">{n}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Lucky / Unlucky Colors */}
            {(!!((mobileResult.lucky_colors || mobileResult.lucky_colours)?.length) || !!((mobileResult.unlucky_colors || mobileResult.unlucky_colours)?.length)) && (
              <Card className="bg-card border-0 shadow-soft">
                <CardContent className="p-6 space-y-4">
                  {!!((mobileResult.lucky_colors || mobileResult.lucky_colours)?.length) && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.luckyColors')}</p>
                      <div className="flex flex-wrap gap-2">
                        {(mobileResult.lucky_colors || mobileResult.lucky_colours || []).map((c, i) => (
                          <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-green-50 border border-green-200 text-sm text-green-800">
                            <span className="w-3 h-3 rounded-full border border-green-300" style={{ backgroundColor: c.toLowerCase().replace(/\s+/g, '') }} />
                            {c}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {!!((mobileResult.unlucky_colors || mobileResult.unlucky_colours)?.length) && (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">{t('numerology.mobile.unluckyColors')}</p>
                      <div className="flex flex-wrap gap-2">
                        {(mobileResult.unlucky_colors || mobileResult.unlucky_colours || []).map((c, i) => (
                          <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-red-50 border border-red-200 text-sm text-red-800">
                            <span className="w-3 h-3 rounded-full border border-red-300" style={{ backgroundColor: c.toLowerCase().replace(/\s+/g, '') }} />
                            {c}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Mobile Combinations (Pair Analysis) */}
            {!!((mobileResult.mobile_combinations || mobileResult.combinations)?.length) && (() => {
              const combos = mobileResult.mobile_combinations || mobileResult.combinations || [];
              return (
                <Card className="bg-card border-0 shadow-soft">
                  <CardContent className="p-6 space-y-4">
                    <Heading as={5} variant={5}>{t('numerology.mobile.pairAnalysis')}</Heading>

                    {/* Stats bar */}
                    <div className="flex gap-3 justify-center text-sm">
                      <span className="px-3 py-1 rounded-full bg-green-100 text-green-800">
                        {t('numerology.mobile.beneficCount')}: {mobileResult.benefic_count ?? combos.filter(c => c.type === 'Benefic').length}
                      </span>
                      <span className="px-3 py-1 rounded-full bg-red-100 text-red-800">
                        {t('numerology.mobile.maleficCount')}: {mobileResult.malefic_count ?? combos.filter(c => c.type === 'Malefic').length}
                      </span>
                    </div>

                    {/* Table */}
                    <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="bg-sacred-gold/10">
                            <th className="px-4 py-2 text-left font-medium text-foreground">{t('numerology.mobile.pair')}</th>
                            <th className="px-4 py-2 text-left font-medium text-foreground">{t('numerology.mobile.type')}</th>
                          </tr>
                        </thead>
                        <tbody>
                          {combos.map((c, i) => (
                            <tr key={i} className={`border-t border-sacred-gold/10 ${c.type === 'Benefic' ? 'bg-green-50/50' : c.type === 'Malefic' ? 'bg-red-50/50' : ''}`}>
                              <td className="px-4 py-2 font-mono text-foreground">{c.pair}</td>
                              <td className="px-4 py-2">
                                <Badge className={
                                  c.type === 'Benefic' ? 'bg-green-100 text-green-800' :
                                  c.type === 'Malefic' ? 'bg-red-100 text-red-800' :
                                  'bg-gray-100 text-gray-700'
                                }>{t(`numerology.compatibility.${c.type.toLowerCase() as 'benefic' | 'neutral' | 'malefic'}`)}</Badge>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CardContent>
                </Card>
              );
            })()}

            {/* Lo Shu Grid */}
            {mobileResult.loshu_grid && mobileResult.loshu_values && (
              <Card className="bg-card border-0 shadow-soft">
                <CardContent className="p-6 space-y-4">
                  <Heading as={5} variant={5}>{t('numerology.mobile.loshuGrid')}</Heading>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-start">
                    {/* Grid */}
                    <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                      <div className="grid grid-cols-3 gap-2">
                        {mobileResult.loshu_grid.flat().map((cell: number, idx: number) => {
                          const v = mobileResult.loshu_values?.[cell] || '';
                          const count = v ? v.length : 0; // "99" = 2 occurrences, "9" = 1
                          const strengthNums = new Set<number>((mobileResult.loshu_arrows?.arrows_of_strength || []).flatMap((a: any) => a.numbers || []));
                          const weaknessNums = new Set<number>((mobileResult.loshu_arrows?.arrows_of_weakness || []).flatMap((a: any) => a.numbers || []));
                          const isStrength = strengthNums.has(cell);
                          const isWeakness = weaknessNums.has(cell);
                          const isPresent = count > 0;
                          const boxClass = isStrength
                            ? 'border-green-400 bg-green-50'
                            : isWeakness
                              ? 'border-red-300 bg-red-50'
                              : isPresent
                                ? 'border-sacred-gold/40 bg-sacred-gold/5'
                                : 'border-gray-200 bg-gray-50';
                          return (
                            <div key={idx} className={`rounded-lg border-2 ${boxClass} p-3 text-center`}>
                              <p className={`text-lg font-bold ${isPresent ? 'text-foreground' : 'text-gray-300'}`}>{cell}</p>
                              {count > 1 && <p className="text-[10px] text-sacred-gold-dark font-medium">×{count}</p>}
                            </div>
                          );
                        })}
                      </div>
                      <p className="text-[10px] text-muted-foreground mt-3 flex gap-3 justify-center">
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-green-400 inline-block" /> {isHi ? 'शक्ति' : 'Strength'}</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-red-300 inline-block" /> {isHi ? 'कमज़ोरी' : 'Weakness'}</span>
                        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-gray-200 inline-block" /> {isHi ? 'अनुपस्थित' : 'Absent'}</span>
                      </p>
                    </div>

                    {/* Arrows + Planes */}
                    <div className="space-y-3">
                      {!!mobileResult.loshu_arrows?.arrows_of_strength?.length && (
                        <div className="rounded-xl border border-green-200 bg-green-50 p-4">
                          <p className="text-sm font-semibold text-green-800">{t('numerology.arrowsOfStrength')}</p>
                          <div className="mt-2 space-y-2">
                            {mobileResult.loshu_arrows.arrows_of_strength.map((a: any) => (
                              <div key={a.key} className="text-xs text-green-800">
                                <span className="font-medium">{isHi ? (a.name_hi || a.name) : a.name}</span>
                                {a.meaning ? `: ${isHi ? (a.meaning_hi || a.meaning) : a.meaning}` : ''}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      {!!mobileResult.loshu_arrows?.arrows_of_weakness?.length && (
                        <div className="rounded-xl border border-red-200 bg-red-50 p-4">
                          <p className="text-sm font-semibold text-red-800">{t('numerology.arrowsOfWeakness')}</p>
                          <div className="mt-2 space-y-2">
                            {mobileResult.loshu_arrows.arrows_of_weakness.map((a: any) => (
                              <div key={a.key} className="text-xs text-red-800">
                                <span className="font-medium">{isHi ? (a.name_hi || a.name) : a.name}</span>
                                {a.missing_meaning ? `: ${isHi ? (a.missing_meaning_hi || a.missing_meaning) : a.missing_meaning}` : ''}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Lo Shu Planes */}
                      {mobileResult.loshu_planes && (
                        <div className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                          <p className="text-sm font-semibold text-foreground">{t('numerology.planes')}</p>
                          <div className="mt-3 space-y-3">
                            {(['mental', 'emotional', 'practical'] as const).map((k) => {
                              const plane = mobileResult.loshu_planes?.[k];
                              if (!plane) return null;
                              const pct = plane.percentage ?? 0;
                              const colorMap = { mental: 'bg-blue-500', emotional: 'bg-pink-500', practical: 'bg-amber-500' };
                              return (
                                <div key={k}>
                                  <div className="flex justify-between text-xs mb-1">
                                    <span className="text-muted-foreground">{isHi ? (plane.name_hi || plane.name) : plane.name}</span>
                                    <span className="font-medium text-foreground">{plane.score} ({pct}%)</span>
                                  </div>
                                  <div className="w-full h-2 rounded-full bg-gray-200 overflow-hidden">
                                    <div className={`h-full rounded-full ${colorMap[k]}`} style={{ width: `${Math.min(pct, 100)}%` }} />
                                  </div>
                                  {plane.interpretation && (
                                    <p className="text-[9px] text-muted-foreground mt-1 italic">
                                      {isHi ? (plane.interpretation_hi || plane.interpretation) : plane.interpretation}
                                    </p>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                          {(mobileResult.loshu_planes.interpretation || mobileResult.loshu_planes.interpretation_hi) && (
                            <p className="text-xs text-muted-foreground mt-3 leading-relaxed">
                              {pick(mobileResult.loshu_planes, 'interpretation')}
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Vedic Grid */}
            {mobileResult.vedic_grid && mobileResult.vedic_values && (
              <Card className="bg-card border-0 shadow-soft">
                <CardContent className="p-6 space-y-4">
                  <Heading as={5} variant={5}>{t('numerology.mobile.vedicGrid')}</Heading>
                  <div className="rounded-xl border border-sacred-gold/25 bg-white p-4 max-w-xs mx-auto">
                    <div className="grid grid-cols-3 gap-2">
                      {mobileResult.vedic_grid.flat().map((cell: number, idx: number) => {
                        const v = mobileResult.vedic_values?.[cell] || '';
                        const isMissing = !v;
                        return (
                          <div key={idx} className={`rounded-lg border border-sacred-gold/25 p-2 text-center ${isMissing ? 'bg-gray-50' : 'bg-sacred-gold/5'}`}>
                            <p className="text-[10px] text-muted-foreground">{cell}</p>
                            <p className={`text-sm font-semibold ${isMissing ? 'text-muted-foreground' : 'text-foreground'}`}>
                              {v || '-'}
                            </p>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Missing Numbers with interpretations */}
            {!!mobileResult.missing_numbers?.length && (
              <Card className="bg-card border-0 shadow-soft">
                <CardContent className="p-6 space-y-3">
                  <Heading as={5} variant={5}>{t('numerology.mobile.missingNumbers')}</Heading>
                  {(() => {
                    const nums = mobileResult.missing_numbers!;
                    // Check if enriched objects (from DOB analysis) or simple digit list
                    const isEnriched = nums.length > 0 && typeof nums[0] === 'object' && nums[0] !== null;
                    if (isEnriched) {
                      return (
                        <div className="space-y-2">
                          {(nums as Array<any>).map((m: any) => (
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
                      );
                    }
                    // Simple digit list
                    return (
                      <div className="flex flex-wrap gap-2">
                        {(nums as number[]).map((n) => (
                          <Badge key={n} className="bg-gray-100 text-gray-700 text-sm px-3 py-1">{n}</Badge>
                        ))}
                      </div>
                    );
                  })()}
                </CardContent>
              </Card>
            )}

            {/* Repeated Numbers */}
            {!!mobileResult.repeated_numbers?.length && (
              <Card className="bg-card border-0 shadow-soft">
                <CardContent className="p-6 space-y-3">
                  <Heading as={5} variant={5}>{t('numerology.mobile.repeatedNumbers')}</Heading>
                  <div className="space-y-2">
                    {mobileResult.repeated_numbers.map((r: any) => (
                      <div key={r.number} className="rounded-xl border border-sacred-gold/25 bg-white p-4">
                        <p className="text-sm font-semibold text-foreground">{t('numerology.number')} {r.number}</p>
                        <p className="text-xs text-muted-foreground mt-1">{t('numerology.count')}: {r.count}</p>
                        {r.meaning && <p className="text-xs text-muted-foreground mt-1">{pick(r, 'meaning')}</p>}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Affirmations */}
            {mobileResult.affirmations && (() => {
              // API returns either a dict {area: text} or an array [{area, affirmation}]
              const aff = mobileResult.affirmations;
              const entries: Array<{area: string; text: string}> = Array.isArray(aff)
                ? aff.map((a: any) => ({ area: a.area, text: a.affirmation }))
                : Object.entries(aff).map(([area, text]) => ({ area, text: text as string }));
              if (!entries.length) return null;
              return (
                <Card className="bg-card border-0 shadow-soft">
                  <CardContent className="p-6 space-y-3">
                    <Heading as={5} variant={5}>{t('numerology.mobile.affirmations')}</Heading>
                    <div className="space-y-3">
                      {entries.map((e) => (
                        <div key={e.area} className="rounded-xl border border-sacred-gold/25 bg-sacred-gold/5 p-4">
                          <p className="text-sm font-semibold text-foreground capitalize">{t(`numerology.struggle.${e.area}` as any) || e.area}</p>
                          <p className="text-xs text-muted-foreground mt-1 leading-relaxed italic">&ldquo;{e.text}&rdquo;</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              );
            })()}
            </div>
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
