import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Home, Sparkles, Loader2, Heart, Briefcase, Users, HeartPulse, Compass } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";

interface HouseNumerologyResult {
  address: string;
  house_number: {
    raw: string;
    numeric: number;
    vibration: number;
  };
  street_name?: {
    name: string;
    numerology: number;
    influence: string;
  };
  prediction: {
    energy: string;
    prediction: string;
    best_for: string;
    family_life: string;
    career_impact: string;
    relationships: string;
    health: string;
    vastu_tip: string;
    lucky_colors: string[];
    remedies: string[];
  };
  digit_analysis: Array<{
    digit: number;
    meaning: string;
  }>;
  resident_compatibility?: {
    resident_life_path: number;
    house_number: number;
    is_ideal: boolean;
    compatibility_score: string;
    recommendation: string;
  };
  remedies: string[];
  enhancement_tips: string[];
}

interface Props {
  birthDate?: string;
}

export default function HouseNumerology({ birthDate }: Props) {
  const { t } = useTranslation();
  const [address, setAddress] = useState('');
  const [dob, setDob] = useState(birthDate || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<HouseNumerologyResult | null>(null);
  const [error, setError] = useState('');

  const analyzeHouse = async () => {
    if (!address.trim()) return;
    setLoading(true);
    setResult(null);
    setError('');
    try {
      const data = await api.post('/api/numerology/house', {
        address: address.trim(),
        birth_date: dob || undefined,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : t('numerology.errorHouse'));
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      {/* Input Card */}
      <Card className="bg-card border-sacred-gold/20 shadow-soft max-w-4xl mx-auto">
        <CardContent className="p-6">
          <h3 className="font-semibold text-foreground mb-4 text-center flex items-center justify-center gap-2">
            <Home className="w-5 h-5 text-sacred-gold" />
            {t('numerology.houseAnalyzeHeading')}
          </h3>
          
          <div className="space-y-4">
            {/* Address Input */}
            <div>
              <label className="block text-sm text-muted-foreground mb-1">
                {t('numerology.fullAddress')} <span className="text-red-600">*</span>
              </label>
              <Input
                placeholder={t('numerology.addressPlaceholder')}
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                className="bg-card border-sacred-gold"
              />
              <p className="text-xs text-muted-foreground mt-1">
                {t('numerology.addressHelpText')}
              </p>
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
              onClick={analyzeHouse}
              disabled={loading || !address.trim()}
              className="w-full bg-sacred-gold text-background hover:bg-gray-50"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('numerology.analyzing')}</>
              ) : (
                <><Home className="w-4 h-4 mr-2" />{t('numerology.analyzeHouse')}</>
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
                {t('numerology.houseReport')}
              </Heading>
              <p className="text-sm text-foreground mt-1">{result.address}</p>
              <div className="flex items-center justify-center gap-4 mt-3">
                <Badge className="text-xl px-4 py-1 bg-sacred-gold text-background">
                  {t('numerology.house')} #{result.house_number.raw}
                </Badge>
                <Badge className="text-lg px-3 py-1 bg-purple-100 text-purple-700">
                  {t('numerology.vehicleVibration')}: {result.house_number.vibration}
                </Badge>
              </div>
            </div>
          </Card>

          {/* Energy Badge */}
          <div className="flex justify-center">
            <Badge className="text-lg px-6 py-2 bg-sacred-gold/20 text-sacred-gold border-sacred-gold">
              {result.prediction.energy}
            </Badge>
          </div>

          {/* Main Prediction */}
          <Card className="bg-card border-0 shadow-soft-lg">
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-sacred-gold/20">
                <Sparkles className="w-5 h-5 text-sacred-gold" />
                <Heading as={4} variant={4}>
                  {t('numerology.homeEnergy')}
                </Heading>
              </div>

              <p className="text-sm text-muted-foreground leading-relaxed">
                {result.prediction.prediction}
              </p>

              <div className="pt-3 border-t border-sacred-gold/20">
                <p className="text-sm font-medium text-foreground mb-1">{t('numerology.bestSuitedFor')}</p>
                <p className="text-sm text-muted-foreground">{result.prediction.best_for}</p>
              </div>
            </CardContent>
          </Card>

          {/* Life Areas Grid */}
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Users className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-foreground">{t('numerology.familyLife')}</p>
                </div>
                <p className="text-sm text-muted-foreground">{result.prediction.family_life}</p>
              </CardContent>
            </Card>
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Briefcase className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-foreground">{t('numerology.careerImpact')}</p>
                </div>
                <p className="text-sm text-muted-foreground">{result.prediction.career_impact}</p>
              </CardContent>
            </Card>
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Heart className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-foreground">{t('numerology.relationships')}</p>
                </div>
                <p className="text-sm text-muted-foreground">{result.prediction.relationships}</p>
              </CardContent>
            </Card>
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <HeartPulse className="w-4 h-4 text-sacred-gold" />
                  <p className="text-sm font-medium text-foreground">{t('numerology.health')}</p>
                </div>
                <p className="text-sm text-muted-foreground">{result.prediction.health}</p>
              </CardContent>
            </Card>
          </div>

          {/* Vastu Tip */}
          <Card className="bg-amber-50/50 border-amber-200">
            <CardContent className="p-4">
              <div className="flex items-start gap-3">
                <Compass className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-amber-800 mb-1">{t('numerology.vastuTip')}</p>
                  <p className="text-sm text-amber-700">{result.prediction.vastu_tip}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Lucky Colors */}
          <Card className="bg-card border-0 shadow-soft">
            <CardContent className="p-4">
              <p className="text-sm font-medium text-foreground mb-3">{t('numerology.luckyColors')}</p>
              <div className="flex flex-wrap gap-2">
                {result.prediction.lucky_colors.map((color, i) => (
                  <Badge key={i} className="bg-sacred-gold/20 text-sacred-gold-dark border-sacred-gold px-3 py-1">
                    {color}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Digit Analysis */}
          {result.digit_analysis.length > 0 && (
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-3">{t('numerology.houseBreakdown')}</p>
                <div className="flex flex-wrap gap-3">
                  {result.digit_analysis.map((item, i) => (
                    <div key={i} className="bg-sacred-gold/5 rounded-lg p-3 border border-sacred-gold/10 min-w-[100px]">
                      <Badge className="text-lg mb-1 bg-sacred-gold text-background">{item.digit}</Badge>
                      <p className="text-[10px] text-muted-foreground leading-tight">{item.meaning}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Street Name Analysis */}
          {result.street_name && (
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-2">{t('numerology.streetInfluence')}</p>
                <div className="flex items-center gap-2 mb-2">
                  <Text variant="muted" as="span">{result.street_name.name}</Text>
                  <Badge variant="outline" className="border-sacred-gold text-sacred-gold">
                    {t('numerology.number')} {result.street_name.numerology}
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground">{result.street_name.influence}</p>
              </CardContent>
            </Card>
          )}

          {/* Resident Compatibility */}
          {result.resident_compatibility && (
            <Card className={`border-0 shadow-soft ${result.resident_compatibility.is_ideal ? 'bg-green-50/50' : 'bg-yellow-50/50'}`}>
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Heart className={`w-5 h-5 ${result.resident_compatibility.is_ideal ? 'text-green-600' : 'text-yellow-600'}`} />
                  <p className="text-sm font-medium text-foreground">{t('numerology.residentCompatibility')}</p>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <Text variant="muted" as="span">{t('numerology.yourLifePath')}: {result.resident_compatibility.resident_life_path}</Text>
                  <Text variant="muted" as="span">{t('numerology.house')}: {result.resident_compatibility.house_number}</Text>
                </div>
                <Badge className={result.resident_compatibility.is_ideal 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
                }>
                  {result.resident_compatibility.compatibility_score}
                </Badge>
                <p className="text-sm text-muted-foreground mt-2">{result.resident_compatibility.recommendation}</p>
              </CardContent>
            </Card>
          )}

          {/* Remedies */}
          {result.remedies.length > 0 && (
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-3">{t('numerology.remedies')}</p>
                <ul className="space-y-2">
                  {result.remedies.map((remedy, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <Sparkles className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />
                      {remedy}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Enhancement Tips */}
          {result.enhancement_tips.length > 0 && (
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-3">{t('numerology.enhancementTips')}</p>
                <ul className="space-y-2">
                  {result.enhancement_tips.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <Compass className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />
                      {tip}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}