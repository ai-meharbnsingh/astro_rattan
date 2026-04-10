import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Hash, Sparkles, Loader2, Phone } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { useAuth } from '@/hooks/useAuth';
import ClientSelector, { autoRegisterClient } from '@/components/ClientSelector';
import type { ClientData } from '@/components/ClientSelector';

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

export default function NumerologyTarot() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const isAstrologer = user?.role === 'astrologer';

  // Client selector state
  const [isNewClient, setIsNewClient] = useState(true);
  const [selectedClient, setSelectedClient] = useState<ClientData | null>(null);

  // Numerology
  const [numName, setNumName] = useState('');
  const [numDob, setNumDob] = useState('');
  const [numResult, setNumResult] = useState<NumerologyResult | null>(null);
  const [numLoading, setNumLoading] = useState(false);

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

  // Mobile Numerology
  const [firstName, setFirstName] = useState('');
  const [middleName, setMiddleName] = useState('');
  const [lastName, setLastName] = useState('');
  const [mobileCountryCode, setMobileCountryCode] = useState('+91');
  const [mobilePhone, setMobilePhone] = useState('');
  const [mobileDob, setMobileDob] = useState('');
  const [selectedAreas, setSelectedAreas] = useState<string[]>([]);
  const [mobileResult, setMobileResult] = useState<MobileNumerologyResult | null>(null);
  const [mobileLoading, setMobileLoading] = useState(false);

  // Mobile section client selector state
  const [mobileIsNewClient, setMobileIsNewClient] = useState(true);
  const [mobileSelectedClient, setMobileSelectedClient] = useState<ClientData | null>(null);

  const handleMobileClientSelect = (client: ClientData | null) => {
    setMobileSelectedClient(client);
    if (client) {
      const nameParts = (client.name || '').split(' ');
      setFirstName(nameParts[0] || '');
      setMiddleName(nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : '');
      setLastName(nameParts.length > 1 ? nameParts[nameParts.length - 1] : '');
      setMobileDob(client.birth_date || '');
      if (client.phone) {
        // Try to parse country code from phone
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

  // Error state for user feedback
  const [error, setError] = useState('');

  const calculateNumerology = async () => {
    if (!numName.trim() || !numDob) return;
    setNumLoading(true);
    setNumResult(null);
    setError('');
    try {
      const data = await api.post('/api/numerology/calculate', { name: numName.trim(), birth_date: numDob });
      // Normalize predictions: API may return string (old), array (old), or dict (new)
      if (data.predictions && typeof data.predictions === 'string') {
        data.predictions = [data.predictions];
      }
      setNumResult(data);
      // Auto-register new client for astrologers
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
      // Auto-register new client for astrologers
      if (isAstrologer && mobileIsNewClient && !mobileSelectedClient) {
        autoRegisterClient({ name: fullName, phone: fullPhone, birth_date: mobileDob });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Mobile numerology analysis failed. Please try again.');
    }
    setMobileLoading(false);
  };

  return (
    <section className="max-w-4xl mx-auto py-24 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold text-sacred-gold text-sm font-medium mb-4">
          <Sparkles className="w-4 h-4" />{t('numerology.badge')}
        </div>
        <h2 className="text-3xl sm:text-4xl font-display font-bold text-cosmic-text mb-2">
          {t('numerology.heading')}<span className="text-gradient-indigo"> {t('numerology.headingHighlight')}</span>
        </h2>
        <p className="text-cosmic-text-secondary">{t('numerology.subtitle')}</p>
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl bg-red-900 border border-red-500 text-red-400 text-sm text-center max-w-xl mx-auto">
          {error}
        </div>
      )}

      <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl mx-auto">
        <CardContent className="p-6">
          <h3 className="font-display font-semibold text-cosmic-text mb-4 text-center">{t('numerology.calculateNumbers')}</h3>
          {isAstrologer && (
            <ClientSelector
              onSelectClient={handleClientSelect}
              isNewClient={isNewClient}
              onToggle={handleClientToggle}
            />
          )}
          <div className="space-y-3">
            <Input placeholder={t('numerology.fullName')} value={numName} onChange={(e) => setNumName(e.target.value)} className="bg-cosmic-card border-sacred-gold" />
            <Input type="date" value={numDob} onChange={(e) => setNumDob(e.target.value)} className="bg-cosmic-card border-sacred-gold" />
            <Button onClick={calculateNumerology} disabled={numLoading || !numName.trim() || !numDob} className="w-full bg-sacred-gold text-cosmic-bg hover:bg-sacred-gold-dark">
              {numLoading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('common.calculating')}</> : <><Hash className="w-4 h-4 mr-2" />{t('numerology.calculate')}</>}
            </Button>
          </div>
        </CardContent>
      </Card>
          {numResult && (
            <Card className="mt-6 bg-cosmic-card border-0 shadow-soft-lg max-w-xl mx-auto">
              <CardContent className="p-6">
                <h4 className="font-display font-semibold text-cosmic-text mb-4 text-center">{t('numerology.report')}</h4>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  {[
                    { label: t('numerology.lifePath'), value: numResult.life_path, color: 'bg-purple-100 text-purple-700' },
                    { label: t('numerology.destiny'), value: numResult.destiny ?? numResult.expression, color: 'bg-blue-100 text-blue-700' },
                    { label: t('numerology.soulUrge'), value: numResult.soul_urge, color: 'bg-green-500 text-green-400' },
                    { label: t('numerology.personality'), value: numResult.personality, color: 'bg-yellow-100 text-yellow-700' },
                  ].map((n) => (
                    <div key={n.label} className="text-center p-3 rounded-xl bg-cosmic-card">
                      <p className="text-sm text-cosmic-text-secondary mb-1">{n.label}</p>
                      <Badge className={`text-lg px-3 py-1 ${n.color}`}>{n.value}</Badge>
                    </div>
                  ))}
                </div>
                {numResult.summary && <p className="text-sm text-cosmic-text-secondary text-center">{numResult.summary}</p>}
                {numResult.predictions && (
                  Array.isArray(numResult.predictions) ? (
                    /* Old format: array of strings */
                    numResult.predictions.length > 0 && (
                      <div className="mt-4">
                        <p className="text-sm font-medium text-cosmic-text mb-2">{t('numerology.predictions')}:</p>
                        <ul className="space-y-1">
                          {numResult.predictions.map((p, i) => (
                            <li key={i} className="text-sm text-cosmic-text-secondary flex gap-2">
                              <Sparkles className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />{p}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )
                  ) : (
                    /* New format: dict with life_path, destiny, soul_urge, personality */
                    <div className="mt-4 space-y-3">
                      <p className="text-sm font-medium text-cosmic-text mb-2">{t('numerology.predictions')}:</p>
                      {[
                        { key: 'life_path' as const, label: t('numerology.lifePath'), headerColor: 'bg-purple-500 text-purple-400', borderColor: 'border-purple-500' },
                        { key: 'destiny' as const, label: t('numerology.destiny'), headerColor: 'bg-blue-500 text-blue-400', borderColor: 'border-blue-500' },
                        { key: 'soul_urge' as const, label: t('numerology.soulUrge'), headerColor: 'bg-green-500 text-green-400', borderColor: 'border-green-500' },
                        { key: 'personality' as const, label: t('numerology.personality'), headerColor: 'bg-yellow-500 text-yellow-400', borderColor: 'border-yellow-500' },
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
                              <p className="text-sm text-cosmic-text-secondary leading-relaxed">{text}</p>
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

          {/* Mobile Number Numerology Section */}
          <div className="mt-10 pt-8 border-t border-sacred-gold">
            <div className="text-center mb-6">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold text-sacred-gold text-sm font-medium mb-3">
                <Phone className="w-4 h-4" />Mobile Number Numerology
              </div>
              <p className="text-sm text-cosmic-text-secondary">Discover the hidden vibration of your mobile number</p>
            </div>
            <Card className="bg-cosmic-card border-0 shadow-soft max-w-2xl mx-auto">
              <CardContent className="p-6">
                <h3 className="font-display font-semibold text-cosmic-text mb-4 text-center">Analyze Your Mobile Number</h3>
                {isAstrologer && (
                  <ClientSelector
                    onSelectClient={handleMobileClientSelect}
                    isNewClient={mobileIsNewClient}
                    onToggle={handleMobileClientToggle}
                  />
                )}
                <div className="space-y-4">
                  {/* Name Fields */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div>
                      <label className="block text-sm text-cosmic-text-secondary mb-1">First Name <span className="text-red-400">*</span></label>
                      <Input
                        placeholder="First Name"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        className="bg-cosmic-card border-sacred-gold"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-cosmic-text-secondary mb-1">Middle Name</label>
                      <Input
                        placeholder="Middle Name (optional)"
                        value={middleName}
                        onChange={(e) => setMiddleName(e.target.value)}
                        className="bg-cosmic-card border-sacred-gold"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-cosmic-text-secondary mb-1">Last Name</label>
                      <Input
                        placeholder="Last Name"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                        className="bg-cosmic-card border-sacred-gold"
                      />
                    </div>
                  </div>

                  {/* Mobile Number with Country Code */}
                  <div>
                    <label className="block text-sm text-cosmic-text-secondary mb-1">Mobile Number <span className="text-red-400">*</span></label>
                    <div className="flex gap-2">
                      <Select value={mobileCountryCode} onValueChange={setMobileCountryCode}>
                        <SelectTrigger className="w-24 bg-cosmic-card border-sacred-gold shrink-0">
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
                        <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cosmic-text-secondary" />
                        <Input
                          placeholder="9876543210"
                          value={mobilePhone}
                          onChange={(e) => setMobilePhone(e.target.value.replace(/\D/g, ''))}
                          className="bg-cosmic-card border-sacred-gold pl-10"
                          maxLength={15}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Date of Birth */}
                  <div>
                    <label className="block text-sm text-cosmic-text-secondary mb-1">Date of Birth <span className="text-red-400">*</span></label>
                    <Input
                      type="date"
                      value={mobileDob}
                      onChange={(e) => setMobileDob(e.target.value)}
                      className="bg-cosmic-card border-sacred-gold"
                    />
                  </div>

                  {/* Area of Struggle */}
                  <div>
                    <label className="block text-sm text-cosmic-text-secondary mb-2">Area of Struggle</label>
                    <div className="flex flex-wrap gap-3">
                      {['Health', 'Relationship', 'Career', 'Money', 'Job'].map((area) => (
                        <label
                          key={area}
                          className={`inline-flex items-center gap-2 px-3 py-2 rounded-lg border cursor-pointer transition-all text-sm ${
                            selectedAreas.includes(area)
                              ? 'border-sacred-gold bg-sacred-gold text-sacred-gold'
                              : 'border-sacred-gold bg-cosmic-card text-cosmic-text-secondary hover:border-sacred-gold'
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={selectedAreas.includes(area)}
                            onChange={() => toggleArea(area)}
                            className="sr-only"
                          />
                          <div className={`w-4 h-4 rounded border flex items-center justify-center shrink-0 ${
                            selectedAreas.includes(area)
                              ? 'border-sacred-gold bg-sacred-gold'
                              : 'border-sacred-gold bg-transparent'
                          }`}>
                            {selectedAreas.includes(area) && (
                              <svg className="w-3 h-3 text-cosmic-bg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                              </svg>
                            )}
                          </div>
                          {area}
                        </label>
                      ))}
                    </div>
                  </div>

                  <Button
                    onClick={analyzeMobile}
                    disabled={mobileLoading || !mobilePhone.trim() || !firstName.trim() || !mobileDob}
                    className="w-full bg-sacred-gold text-cosmic-bg hover:bg-sacred-gold-dark"
                  >
                    {mobileLoading ? (
                      <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Analyzing...</>
                    ) : (
                      <><Phone className="w-4 h-4 mr-2" />Analyze Mobile Number</>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* ── Mobile Numerology Results ── */}
            {mobileResult && (
              <div className="mt-6 space-y-6 max-w-2xl mx-auto">

                {/* Section 1: Report Header */}
                <Card className="bg-cosmic-card border-0 shadow-soft-lg overflow-hidden">
                  <div className="bg-gradient-to-r from-sacred-gold to-sacred-gold-dark px-6 py-4 text-center border-b border-sacred-gold">
                    <h4 className="font-display font-bold text-lg text-sacred-gold tracking-wide uppercase">Mobile Numerology Report</h4>
                    {mobileResult.name && <p className="text-sm text-cosmic-text mt-1">{mobileResult.name}</p>}
                    {mobileResult.birth_date && (
                      <p className="text-sm text-cosmic-text-secondary mt-1">Date of Birth: {mobileResult.birth_date}</p>
                    )}
                  </div>

                  <CardContent className="p-6 space-y-6">

                    {/* Section 2: Loshu Grid & Vedic Grid */}
                    {(mobileResult.loshu_grid || mobileResult.vedic_grid) && (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                        {mobileResult.loshu_grid && (
                          <div>
                            <p className="text-sm font-medium text-cosmic-text mb-2 text-center">Loshu Grid</p>
                            <div className="grid grid-cols-3 border border-sacred-gold rounded-lg overflow-hidden">
                              {mobileResult.loshu_grid.flat().map((cell, i) => (
                                <div
                                  key={`loshu-${i}`}
                                  className="aspect-square flex items-center justify-center border border-sacred-gold text-center"
                                >
                                  <span className={`text-lg font-display font-semibold ${cell != null ? 'text-sacred-gold' : 'text-cosmic-text-secondary'}`}>
                                    {cell != null ? cell : '-'}
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        {mobileResult.vedic_grid && (
                          <div>
                            <p className="text-sm font-medium text-cosmic-text mb-2 text-center">Vedic Grid</p>
                            <div className="grid grid-cols-3 border border-sacred-gold rounded-lg overflow-hidden">
                              {mobileResult.vedic_grid.flat().map((cell, i) => (
                                <div
                                  key={`vedic-${i}`}
                                  className="aspect-square flex items-center justify-center border border-sacred-gold text-center"
                                >
                                  <span className={`text-lg font-display font-semibold ${cell != null ? 'text-sacred-gold' : 'text-cosmic-text-secondary'}`}>
                                    {cell != null ? cell : '-'}
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Section 3: Mobile Number Prediction Details */}
                    <div className="rounded-xl border border-sacred-gold overflow-hidden">
                      <div className="px-4 py-2 bg-sacred-gold text-sacred-gold font-medium text-sm flex items-center gap-2">
                        <Sparkles className="w-4 h-4 shrink-0" />Prediction Details
                      </div>
                      <div className="divide-y divide-sacred-gold">
                        {/* Mobile Number */}
                        <div className="flex justify-between px-4 py-3">
                          <span className="text-sm text-cosmic-text-secondary">Your Mobile Number</span>
                          <span className="text-sm font-medium text-cosmic-text">{mobileResult.phone_number}</span>
                        </div>
                        {/* Compound Number */}
                        <div className="flex justify-between px-4 py-3">
                          <span className="text-sm text-cosmic-text-secondary">Compound Number</span>
                          <span className="text-sm font-medium text-sacred-gold">{mobileResult.compound_number}</span>
                        </div>
                        {/* Mobile Total + Prediction */}
                        <div className="px-4 py-3">
                          <div className="flex justify-between mb-1">
                            <span className="text-sm text-cosmic-text-secondary">Mobile Number Total</span>
                            <span className="text-sm font-medium text-sacred-gold">{mobileResult.mobile_total}</span>
                          </div>
                          {mobileResult.mobile_total_prediction && (
                            <p className="text-sm text-cosmic-text-secondary leading-relaxed mt-1">{mobileResult.mobile_total_prediction}</p>
                          )}
                        </div>
                        {/* Recommended Totals */}
                        {mobileResult.recommended_totals && mobileResult.recommended_totals.length > 0 && (
                          <div className="flex items-center justify-between px-4 py-3">
                            <span className="text-sm text-cosmic-text-secondary">Recommended Totals</span>
                            <div className="flex flex-wrap gap-1.5">
                              {mobileResult.recommended_totals.map((n) => (
                                <Badge key={n} className="bg-sacred-gold text-sacred-gold border-sacred-gold px-2 py-0.5 text-sm">{n}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Lucky Colours */}
                        {mobileResult.lucky_colours && mobileResult.lucky_colours.length > 0 && (
                          <div className="flex items-start justify-between px-4 py-3 gap-3">
                            <span className="text-sm text-cosmic-text-secondary shrink-0">Lucky Colours</span>
                            <div className="flex flex-wrap gap-1.5 justify-end">
                              {mobileResult.lucky_colours.map((c) => (
                                <Badge key={c} className="bg-green-500 text-green-400 border-green-500 px-2 py-0.5 text-sm">{c}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Un-Lucky Colours */}
                        {mobileResult.unlucky_colours && mobileResult.unlucky_colours.length > 0 && (
                          <div className="flex items-start justify-between px-4 py-3 gap-3">
                            <span className="text-sm text-cosmic-text-secondary shrink-0">Un-Lucky Colours</span>
                            <div className="flex flex-wrap gap-1.5 justify-end">
                              {mobileResult.unlucky_colours.map((c) => (
                                <Badge key={c} className="bg-zinc-700 text-zinc-300 border-zinc-600 px-2 py-0.5 text-sm">{c}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Lucky Numbers */}
                        {mobileResult.lucky_numbers && mobileResult.lucky_numbers.length > 0 && (
                          <div className="flex items-center justify-between px-4 py-3">
                            <span className="text-sm text-cosmic-text-secondary">Lucky Numbers</span>
                            <div className="flex flex-wrap gap-1.5">
                              {mobileResult.lucky_numbers.map((n) => (
                                <Badge key={n} className="bg-green-500 text-green-400 border-green-500 px-2 py-0.5 text-sm">{n}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Unlucky Numbers */}
                        {mobileResult.unlucky_numbers && mobileResult.unlucky_numbers.length > 0 && (
                          <div className="flex items-center justify-between px-4 py-3">
                            <span className="text-sm text-cosmic-text-secondary">Unlucky Numbers</span>
                            <div className="flex flex-wrap gap-1.5">
                              {mobileResult.unlucky_numbers.map((n) => (
                                <Badge key={n} className="bg-red-500 text-red-400 border-red-500 px-2 py-0.5 text-sm">{n}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Neutral Numbers */}
                        {mobileResult.neutral_numbers && mobileResult.neutral_numbers.length > 0 && (
                          <div className="flex items-center justify-between px-4 py-3">
                            <span className="text-sm text-cosmic-text-secondary">Neutral Numbers</span>
                            <div className="flex flex-wrap gap-1.5">
                              {mobileResult.neutral_numbers.map((n) => (
                                <Badge key={n} className="bg-zinc-500 text-zinc-400 border-zinc-500 px-2 py-0.5 text-sm">{n}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        {/* Missing Numbers */}
                        {mobileResult.missing_numbers && mobileResult.missing_numbers.length > 0 && (
                          <div className="flex items-center justify-between px-4 py-3">
                            <span className="text-sm text-cosmic-text-secondary">Missing Numbers</span>
                            <div className="flex flex-wrap gap-1.5">
                              {mobileResult.missing_numbers.map((n) => (
                                <Badge key={n} className="bg-transparent text-cosmic-text-secondary border border-dashed border-sacred-gold px-2 py-0.5 text-sm">{n}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Section 4: Mobile Combinations */}
                    {mobileResult.combinations && mobileResult.combinations.length > 0 && (
                      <div className="rounded-xl border border-sacred-gold overflow-hidden">
                        <div className="px-4 py-2 bg-sacred-gold text-sacred-gold font-medium text-sm flex items-center gap-2">
                          <Hash className="w-4 h-4 shrink-0" />Mobile Combinations
                        </div>
                        <div className="overflow-x-auto">
                          <table className="w-full text-sm">
                            <thead>
                              <tr className="border-b border-sacred-gold">
                                <th className="text-left px-4 py-2 text-cosmic-text-secondary font-medium">Pair</th>
                                <th className="text-left px-4 py-2 text-cosmic-text-secondary font-medium">Type</th>
                                <th className="text-left px-4 py-2 text-cosmic-text-secondary font-medium">Description</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-sacred-gold">
                              {mobileResult.combinations.map((combo, i) => (
                                <tr key={i}>
                                  <td className="px-4 py-2 font-mono text-cosmic-text">{combo.pair}</td>
                                  <td className="px-4 py-2">
                                    <Badge className={`text-sm px-2 py-0.5 ${
                                      combo.type === 'Benefic'
                                        ? 'bg-green-500 text-green-400 border-green-500'
                                        : combo.type === 'Neutral'
                                          ? 'bg-amber-500 text-amber-400 border-amber-500'
                                          : 'bg-red-500 text-red-400 border-red-500'
                                    }`}>
                                      {combo.type}
                                    </Badge>
                                  </td>
                                  <td className="px-4 py-2 text-cosmic-text-secondary text-sm">{combo.description || '-'}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                        {/* Recommendation Banner */}
                        {mobileResult.recommendation_message && (
                          <div className={`px-4 py-3 text-sm font-medium text-center ${
                            mobileResult.is_recommended
                              ? 'bg-green-500 text-green-400 border-t border-green-500'
                              : 'bg-red-500 text-red-400 border-t border-red-500'
                          }`}>
                            {mobileResult.recommendation_message}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Section 5: Predictions */}
                    {mobileResult.prediction && (
                      <div className="rounded-xl border border-sacred-gold overflow-hidden">
                        <div className="px-4 py-2 bg-sacred-gold text-sacred-gold font-medium text-sm flex items-center gap-2">
                          <Sparkles className="w-4 h-4 shrink-0" />Predictions
                        </div>
                        <div className="px-4 py-3">
                          <ul className="space-y-2">
                            {(Array.isArray(mobileResult.prediction) ? mobileResult.prediction : mobileResult.prediction.split('. ').filter((s: string) => s.trim())).map((pred: string, i: number) => (
                              <li key={i} className="text-sm text-cosmic-text-secondary flex gap-2">
                                <span className="text-sacred-gold shrink-0 mt-0.5">&#8226;</span>
                                <span>{pred.endsWith('.') ? pred : pred + '.'}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}

                    {/* Section 6: Area of Struggle Affirmations */}
                    {mobileResult.affirmations && typeof mobileResult.affirmations === 'object' && Object.keys(mobileResult.affirmations).length > 0 && (
                      <div className="space-y-3">
                        <p className="text-sm font-medium text-cosmic-text flex items-center gap-2">
                          <Sparkles className="w-4 h-4 text-sacred-gold" />Affirmations for Your Areas of Struggle
                        </p>
                        {Object.entries(mobileResult.affirmations).map(([area, text]: [string, any], i: number) => (
                          <div key={i} className="rounded-xl border border-sacred-gold overflow-hidden">
                            <div className="px-4 py-2 bg-sacred-gold font-medium text-sm text-sacred-gold border-b border-sacred-gold capitalize">
                              {area}
                            </div>
                            <div className="px-4 py-3">
                              <p className="text-sm text-cosmic-text-secondary leading-relaxed italic">{text}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                  </CardContent>
                </Card>
              </div>
            )}
          </div>
    </section>
  );
}
