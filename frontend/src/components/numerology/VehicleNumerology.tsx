import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Car, Sparkles, Loader2, Shield, Navigation, Palette } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";

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
    energy_hi?: string;
    prediction_hi?: string;
    driving_style_hi?: string;
    best_for_hi?: string;
    caution_hi?: string;
    lucky_directions_hi?: string[];
    vehicle_color_hi?: string[];
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
  const isHi = language === 'hi';
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
      setError(err instanceof Error ? err.message : t('numerology.errorVehicle'));
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
        return 'bg-gray-100 text-foreground border-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Card */}
      <Card className="bg-card border-sacred-gold/20 shadow-soft max-w-4xl mx-auto">
        <CardContent className="p-6">
          <h3 className="font-semibold text-foreground mb-4 text-center flex items-center justify-center gap-2">
            <Car className="w-5 h-5 text-sacred-gold" />
            {t('numerology.vehicleAnalyzeHeading')}
          </h3>
          
          <div className="space-y-4">
            {/* Vehicle Number Input */}
            <div>
              <label className="block text-sm text-muted-foreground mb-1">
                {t('numerology.vehicleNumber')} <span className="text-red-600">*</span>
              </label>
              <Input
                placeholder={t('numerology.vehicleNumberPlaceholder')}
                value={vehicleNumber}
                onChange={(e) => setVehicleNumber(e.target.value)}
                className="bg-card border-sacred-gold"
              />
              <p className="text-xs text-muted-foreground mt-1">
                {t('numerology.vehicleHelpText')}
              </p>
            </div>

            {/* Owner Name */}
            <div>
              <label className="block text-sm text-muted-foreground mb-1">
                {t('numerology.ownerName')} ({t('numerology.optional')})
              </label>
              <Input
                placeholder={t('numerology.ownerName')}
                value={ownerName}
                onChange={(e) => setOwnerName(e.target.value)}
                className="bg-card border-sacred-gold"
              />
            </div>

            {/* Optional DOB */}
            <div>
              <label className="block text-sm text-muted-foreground mb-1">
                {t('numerology.dobOptionalCompatibility')}
              </label>
              <Input
                type="date"
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                className="bg-card border-sacred-gold"
              />
            </div>

            <Button
              onClick={analyzeVehicle}
              disabled={loading || !vehicleNumber.trim()}
              className="w-full bg-sacred-gold text-background hover:bg-gray-50"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('numerology.analyzing')}</>
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
        <div className="space-y-6 w-full">
          {/* Header */}
          <Card className="bg-card border-0 shadow-soft-lg overflow-hidden">
            <div className="bg-gradient-to-r from-sacred-gold to-sacred-gold-dark px-6 py-4 text-center">
              <Heading as={4} variant={4}>
                {t('numerology.vehicleReport')}
              </Heading>
              <p className="text-xl font-bold text-foreground mt-2">{result.vehicle_number}</p>
              {result.letters_extracted && (
                <p className="text-xs text-muted-foreground mt-1">
                  {t('numerology.letters')}: {result.letters_extracted} | {t('numerology.digits')}: {result.digits_extracted}
                </p>
              )}
            </div>
          </Card>

          {/* Vibration Number */}
          <div className="grid grid-cols-3 gap-4">
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4 text-center">
                <p className="text-xs text-muted-foreground mb-1">{t('numerology.vehicleVibration')}</p>
                <Badge className="text-2xl px-4 py-2 bg-sacred-gold text-background">{result.vibration.number}</Badge>
                <p className="text-xs text-muted-foreground mt-2">{isHi ? result.prediction.energy_hi || result.prediction.energy : result.prediction.energy}</p>
              </CardContent>
            </Card>
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4 text-center">
                <p className="text-xs text-muted-foreground mb-1">{t('numerology.digitSum')}</p>
                <Badge className="text-xl px-3 py-1 bg-blue-100 text-blue-700">{result.vibration.digit_sum}</Badge>
                <p className="text-xs text-muted-foreground mt-2">{t('numerology.beforeReduction')}</p>
              </CardContent>
            </Card>
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4 text-center">
                <p className="text-xs text-muted-foreground mb-1">{t('numerology.letterValue')}</p>
                <Badge className="text-xl px-3 py-1 bg-purple-100 text-purple-700">{result.vibration.letter_value}</Badge>
                <p className="text-xs text-muted-foreground mt-2">{t('numerology.fromRegistration')}</p>
              </CardContent>
            </Card>
          </div>

          {/* Main Prediction */}
          <Card className="bg-card border-0 shadow-soft-lg">
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-sacred-gold/20">
                <Sparkles className="w-5 h-5 text-sacred-gold" />
                <Heading as={4} variant={4}>
                  {t('numerology.vehicleEnergy')}
                </Heading>
                <Badge className="ml-auto bg-sacred-gold/20 text-sacred-gold border-sacred-gold">
                  {isHi ? result.prediction.energy_hi || result.prediction.energy : result.prediction.energy}
                </Badge>
              </div>

              <p className="text-sm text-muted-foreground leading-relaxed">
                {isHi ? result.prediction.prediction_hi || result.prediction.prediction : result.prediction.prediction}
              </p>

              <div className="grid md:grid-cols-2 gap-4 pt-3 border-t border-sacred-gold/20">
                <div className="flex items-start gap-3">
                  <Navigation className="w-5 h-5 text-sacred-gold shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-foreground">{t('numerology.drivingStyle')}</p>
                    <p className="text-sm text-muted-foreground">{isHi ? result.prediction.driving_style_hi || result.prediction.driving_style : result.prediction.driving_style}</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Shield className="w-5 h-5 text-sacred-gold shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-foreground">{t('numerology.caution')}</p>
                    <p className="text-sm text-muted-foreground">{isHi ? result.prediction.caution_hi || result.prediction.caution : result.prediction.caution}</p>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-sacred-gold/20">
                <p className="text-sm font-medium text-foreground mb-1">{t('numerology.bestSuitedFor')}</p>
                <p className="text-sm text-muted-foreground">{isHi ? result.prediction.best_for_hi || result.prediction.best_for : result.prediction.best_for}</p>
              </div>
            </CardContent>
          </Card>

          {/* Lucky Elements */}
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Palette className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-foreground">{t('numerology.luckyColors')}</p>
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
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Navigation className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-foreground">{t('numerology.luckyDirections')}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {(isHi ? result.prediction.lucky_directions_hi || result.prediction.lucky_directions : result.prediction.lucky_directions).map((dir, i) => (
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
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-3">{t('numerology.digitAnalysis')}</p>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                  {result.digit_analysis.map((item, i) => (
                    <div key={i} className="bg-sacred-gold/5 rounded-lg p-3 text-center border border-sacred-gold/10">
                      <Badge className="text-lg mb-1 bg-sacred-gold text-background">{item.digit}</Badge>
                      <p className="text-[10px] text-muted-foreground leading-tight">{item.meaning}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Special Combinations */}
          {result.special_combinations.length > 0 && (
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-3">{t('numerology.specialPatterns')}</p>
                <div className="space-y-2">
                  {result.special_combinations.map((combo, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 bg-sacred-gold/5 rounded-lg">
                      <Badge className={getComboBadgeColor(combo.type)}>
                        {combo.digits}
                      </Badge>
                      <Text variant="muted" as="span">{getComboTypeLabel(combo.type)}</Text>
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
                  <p className="text-sm font-medium text-foreground">{t('numerology.ownerCompatibility')}</p>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <Text variant="muted" as="span">{t('numerology.yourLifePath')}: {result.owner_compatibility.owner_life_path}</Text>
                  <Text variant="muted" as="span">{t('numerology.vehicle')}: {result.owner_compatibility.vehicle_number}</Text>
                </div>
                <Badge className={result.owner_compatibility.is_favorable 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
                }>
                  {result.owner_compatibility.is_favorable ? `✓ ${t('numerology.favorableMatch')}` : `⚠ ${t('numerology.neutralChallengingMatch')}`}
                </Badge>
                <p className="text-sm text-muted-foreground mt-2">{result.owner_compatibility.recommendation}</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}