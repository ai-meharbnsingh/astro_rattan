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

  // Life Path states
  const [isNewClient, setIsNewClient] = useState(true);
  const [selectedClient, setSelectedClient] = useState<ClientData | null>(null);
  const [numName, setNumName] = useState('');
  const [numDob, setNumDob] = useState('');
  const [numResult, setNumResult] = useState<NumerologyResult | null>(null);
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

  const comboTypeLabel = (type: 'Benefic' | 'Neutral' | 'Malefic') =>
    language === 'hi'
      ? type === 'Benefic'
        ? 'शुभ'
        : type === 'Neutral'
          ? 'सामान्य'
          : 'पापी'
      : type;

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
    setError('');
    try {
      const data = await api.post('/api/numerology/calculate', { name: numName.trim(), birth_date: numDob });
      if (data.predictions && typeof data.predictions === 'string') {
        data.predictions = [data.predictions];
      }
      setNumResult(data);
      if (isAstrologer && isNewClient && !selectedClient) {
        autoRegisterClient({ name: numName.trim(), birth_date: numDob });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Numerology calculation failed. Please try again.');
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
      setError(err instanceof Error ? err.message : 'Mobile numerology analysis failed. Please try again.');
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
              <CardContent className="p-6">
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
                              {section.label} Number
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
                        {area}
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
                    <p className="text-xs text-muted-foreground mb-1">Compound</p>
                    <Badge className="text-lg bg-purple-100 text-purple-700">{mobileResult.compound_number}</Badge>
                  </div>
                  <div className="text-center p-3 bg-sacred-gold/5 rounded-lg">
                    <p className="text-xs text-muted-foreground mb-1">Total</p>
                    <Badge className="text-lg bg-sacred-gold text-background">{mobileResult.mobile_total}</Badge>
                  </div>
                  <div className="text-center p-3 bg-sacred-gold/5 rounded-lg">
                    <p className="text-xs text-muted-foreground mb-1">Status</p>
                    <Badge className={mobileResult.is_recommended ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                      {mobileResult.is_recommended ? 'Good' : 'Caution'}
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