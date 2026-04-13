import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Car, Sparkles, Loader2, Shield, Navigation, Palette } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';

interface VehicleNumerologyResult {
  vehicle_number: string;
  digits_extracted: string;
  letters_extracted: string;
  vibration: {
    number: number;
    digit_sum: number;
    letter_value: number;
  };
  prediction: {
    energy: string;
    prediction: string;
    driving_style: string;
    best_for: string;
    caution: string;
    lucky_directions: string[];
    vehicle_color: string[];
  };
  digit_analysis: Array<{
    position: number;
    digit: number;
    meaning: string;
  }>;
  special_combinations: Array<{
    type: string;
    digits: string;
    meaning: string;
  }>;
  owner_compatibility?: {
    owner_life_path: number;
    vehicle_number: number;
    is_favorable: boolean;
    recommendation: string;
  };
  lucky_days: string[];
  lucky_colors: string[];
}

interface Props {
  birthDate?: string;
}

export default function VehicleNumerology({ birthDate }: Props) {
  const { t, language } = useTranslation();
  const [vehicleNumber, setVehicleNumber] = useState('');
  const [ownerName, setOwnerName] = useState('');
  const [dob, setDob] = useState(birthDate || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VehicleNumerologyResult | null>(null);
  const [error, setError] = useState('');

  const analyzeVehicle = async () => {
    if (!vehicleNumber.trim()) return;
    setLoading(true);
    setResult(null);
    setError('');
    try {
      const data = await api.post('/api/numerology/vehicle', {
        vehicle_number: vehicleNumber.trim(),
        owner_name: ownerName.trim() || undefined,
        birth_date: dob || undefined,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : language === 'hi'
        ? 'वाहन अंकशास्त्र विश्लेषण विफल। कृपया पुनः प्रयास करें।'
        : 'Vehicle numerology analysis failed. Please try again.'
      );
    }
    setLoading(false);
  };

  const getComboTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'master_number': t('numerology.masterNumber'),
      'repeated_digit': t('numerology.repeatedDigit'),
      'ascending_sequence': t('numerology.ascendingSequence'),
      'descending_sequence': t('numerology.descendingSequence'),
    };
    return labels[type] || type;
  };

  const getComboBadgeColor = (type: string) => {
    switch (type) {
      case 'master_number':
        return 'bg-purple-100 text-purple-800 border-purple-300';
      case 'repeated_digit':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'ascending_sequence':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'descending_sequence':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Card */}
      <Card className="bg-cosmic-card border-0 shadow-soft max-w-2xl mx-auto">
        <CardContent className="p-6">
          <h3 className="font-display font-semibold text-cosmic-text mb-4 text-center flex items-center justify-center gap-2">
            <Car className="w-5 h-5 text-sacred-gold" />
            {t('numerology.vehicleAnalyzeHeading')}
          </h3>
          
          <div className="space-y-4">
            {/* Vehicle Number Input */}
            <div>
              <label className="block text-sm text-cosmic-text-secondary mb-1">
                {t('numerology.vehicleNumber')} <span className="text-red-600">*</span>
              </label>
              <Input
                placeholder={t('numerology.vehicleNumberPlaceholder')}
                value={vehicleNumber}
                onChange={(e) => setVehicleNumber(e.target.value)}
                className="bg-cosmic-card border-sacred-gold"
              />
              <p className="text-xs text-cosmic-text-secondary mt-1">
                {t('numerology.vehicleHelpText')}
              </p>
            </div>

            {/* Owner Name */}
            <div>
              <label className="block text-sm text-cosmic-text-secondary mb-1">
                {t('numerology.ownerName')} ({t('numerology.optional')})
              </label>
              <Input
                placeholder={language === 'hi' ? 'वाहन मालिक का नाम' : 'Vehicle owner\'s name'}
                value={ownerName}
                onChange={(e) => setOwnerName(e.target.value)}
                className="bg-cosmic-card border-sacred-gold"
              />
            </div>

            {/* Optional DOB */}
            <div>
              <label className="block text-sm text-cosmic-text-secondary mb-1">
                {language === 'hi' ? 'मालिक की जन्म तिथि (वैकल्पिक - अनुकूलता के लिए)' : 'Owner\'s Date of Birth (Optional - for compatibility)'}
              </label>
              <Input
                type="date"
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                className="bg-cosmic-card border-sacred-gold"
              />
            </div>

            <Button
              onClick={analyzeVehicle}
              disabled={loading || !vehicleNumber.trim()}
              className="w-full bg-sacred-gold text-cosmic-bg hover:bg-gray-50"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{language === 'hi' ? 'विश्लेषण हो रहा है...' : 'Analyzing...'}</>
              ) : (
                <><Car className="w-4 h-4 mr-2" />{t('numerology.analyzeVehicle')}</>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {error && (
        <div className="p-3 rounded-xl bg-red-50 border border-red-300 text-red-700 text-sm text-center max-w-xl mx-auto">
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6 max-w-4xl mx-auto">
          {/* Header */}
          <Card className="bg-cosmic-card border-0 shadow-soft-lg overflow-hidden">
            <div className="bg-gradient-to-r from-sacred-gold to-sacred-gold-dark px-6 py-4 text-center">
              <h4 className="font-display font-bold text-lg text-sacred-gold tracking-wide uppercase">
                {t('numerology.vehicleReport')}
              </h4>
              <p className="text-xl font-display font-bold text-cosmic-text mt-2">{result.vehicle_number}</p>
              {result.letters_extracted && (
                <p className="text-xs text-cosmic-text-secondary mt-1">
                  {language === 'hi' ? 'अक्षर' : 'Letters'}: {result.letters_extracted} | {language === 'hi' ? 'अंक' : 'Digits'}: {result.digits_extracted}
                </p>
              )}
            </div>
          </Card>

          {/* Vibration Number */}
          <div className="grid grid-cols-3 gap-4">
            <Card className="bg-cosmic-card border-0 shadow-soft">
              <CardContent className="p-4 text-center">
                <p className="text-xs text-cosmic-text-secondary mb-1">{t('numerology.vehicleVibration')}</p>
                <Badge className="text-2xl px-4 py-2 bg-sacred-gold text-cosmic-bg">{result.vibration.number}</Badge>
                <p className="text-xs text-cosmic-text-secondary mt-2">{result.prediction.energy}</p>
              </CardContent>
            </Card>
            <Card className="bg-cosmic-card border-0 shadow-soft">
              <CardContent className="p-4 text-center">
                <p className="text-xs text-cosmic-text-secondary mb-1">{t('numerology.digitSum')}</p>
                <Badge className="text-xl px-3 py-1 bg-blue-100 text-blue-700">{result.vibration.digit_sum}</Badge>
                <p className="text-xs text-cosmic-text-secondary mt-2">{language === 'hi' ? 'न्यूनीकरण से पहले' : 'Before reduction'}</p>
              </CardContent>
            </Card>
            <Card className="bg-cosmic-card border-0 shadow-soft">
              <CardContent className="p-4 text-center">
                <p className="text-xs text-cosmic-text-secondary mb-1">{t('numerology.letterValue')}</p>
                <Badge className="text-xl px-3 py-1 bg-purple-100 text-purple-700">{result.vibration.letter_value}</Badge>
                <p className="text-xs text-cosmic-text-secondary mt-2">{language === 'hi' ? 'पंजीकरण से' : 'From registration'}</p>
              </CardContent>
            </Card>
          </div>

          {/* Main Prediction */}
          <Card className="bg-cosmic-card border-0 shadow-soft-lg">
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-sacred-gold/20">
                <Sparkles className="w-5 h-5 text-sacred-gold" />
                <h4 className="font-display font-semibold text-cosmic-text">
                  {t('numerology.vehicleEnergy')}
                </h4>
                <Badge className="ml-auto bg-sacred-gold/20 text-sacred-gold border-sacred-gold">
                  {result.prediction.energy}
                </Badge>
              </div>

              <p className="text-sm text-cosmic-text-secondary leading-relaxed">
                {result.prediction.prediction}
              </p>

              <div className="grid md:grid-cols-2 gap-4 pt-3 border-t border-sacred-gold/20">
                <div className="flex items-start gap-3">
                  <Navigation className="w-5 h-5 text-sacred-gold shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-cosmic-text">{t('numerology.drivingStyle')}</p>
                    <p className="text-sm text-cosmic-text-secondary">{result.prediction.driving_style}</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Shield className="w-5 h-5 text-sacred-gold shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-cosmic-text">{t('numerology.caution')}</p>
                    <p className="text-sm text-cosmic-text-secondary">{result.prediction.caution}</p>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-sacred-gold/20">
                <p className="text-sm font-medium text-cosmic-text mb-1">{t('numerology.bestSuitedFor')}</p>
                <p className="text-sm text-cosmic-text-secondary">{result.prediction.best_for}</p>
              </div>
            </CardContent>
          </Card>

          {/* Lucky Elements */}
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="bg-cosmic-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Palette className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-cosmic-text">{t('numerology.luckyColors')}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {result.lucky_colors.map((color, i) => (
                    <Badge key={i} className="bg-green-100 text-green-800">
                      {color}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
            <Card className="bg-cosmic-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Navigation className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-cosmic-text">{t('numerology.luckyDirections')}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {result.prediction.lucky_directions.map((dir, i) => (
                    <Badge key={i} variant="outline" className="border-sacred-gold text-sacred-gold">
                      {dir}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Digit Analysis */}
          {result.digit_analysis.length > 0 && (
            <Card className="bg-cosmic-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-cosmic-text mb-3">{t('numerology.digitAnalysis')}</p>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                  {result.digit_analysis.map((item, i) => (
                    <div key={i} className="bg-sacred-gold/5 rounded-lg p-3 text-center border border-sacred-gold/10">
                      <Badge className="text-lg mb-1 bg-sacred-gold text-cosmic-bg">{item.digit}</Badge>
                      <p className="text-[10px] text-cosmic-text-secondary leading-tight">{item.meaning}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Special Combinations */}
          {result.special_combinations.length > 0 && (
            <Card className="bg-cosmic-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-cosmic-text mb-3">{t('numerology.specialPatterns')}</p>
                <div className="space-y-2">
                  {result.special_combinations.map((combo, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 bg-sacred-gold/5 rounded-lg">
                      <Badge className={getComboBadgeColor(combo.type)}>
                        {combo.digits}
                      </Badge>
                      <span className="text-sm text-cosmic-text-secondary">{getComboTypeLabel(combo.type)}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Owner Compatibility */}
          {result.owner_compatibility && (
            <Card className={`border-0 shadow-soft ${result.owner_compatibility.is_favorable ? 'bg-green-50/50' : 'bg-yellow-50/50'}`}>
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Shield className={`w-5 h-5 ${result.owner_compatibility.is_favorable ? 'text-green-600' : 'text-yellow-600'}`} />
                  <p className="text-sm font-medium text-cosmic-text">{t('numerology.ownerCompatibility')}</p>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'आपका जीवन पथ' : 'Your Life Path'}: {result.owner_compatibility.owner_life_path}</span>
                  <span className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'वाहन' : 'Vehicle'}: {result.owner_compatibility.vehicle_number}</span>
                </div>
                <Badge className={result.owner_compatibility.is_favorable 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
                }>
                  {result.owner_compatibility.is_favorable ? `✓ ${t('numerology.favorableMatch')}` : `⚠ ${t('numerology.neutralChallengingMatch')}`}
                </Badge>
                <p className="text-sm text-cosmic-text-secondary mt-2">{result.owner_compatibility.recommendation}</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
