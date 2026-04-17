import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { User, Sparkles, Loader2, Calculator } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

interface NameNumerologyResult {
  name: string;
  name_type: string;
  name_parts: {
    first_name: string;
    last_name: string;
    total_parts: number;
  };
  numerology: {
    pythagorean: { number: number; calculation: string };
    chaldean: { number: number; calculation: string };
    soul_urge: { number: number; description: string };
    personality: { number: number; description: string };
  };
  first_name_analysis?: {
    name: string;
    number: number;
    traits: string[];
  };
  last_name_analysis?: {
    name: string;
    number: number;
    meaning: string;
  };
  predictions: {
    primary: {
      title: string;
      ruling_planet: string;
      traits: string[];
      career: string;
      relationships: string;
      health: string;
      lucky_colors: string[];
      lucky_days: string[];
      advice: string;
    };
    soul_urge: string;
    personality: string;
  };
  letter_breakdown: Array<{
    letter: string;
    pythagorean: number;
    chaldean: number;
    is_vowel: boolean;
  }>;
  life_path_compatibility?: {
    life_path: number;
    name_number: number;
    is_compatible: boolean;
    compatibility_note: string;
  };
}

interface Props {
  birthDate?: string;
}

export default function NameNumerology({ birthDate }: Props) {
  const { t } = useTranslation();
  const [fullName, setFullName] = useState('');
  const [nameType, setNameType] = useState('full_name');
  const [dob, setDob] = useState(birthDate || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<NameNumerologyResult | null>(null);
  const [error, setError] = useState('');

  const analyzeName = async () => {
    if (!fullName.trim()) return;
    setLoading(true);
    setResult(null);
    setError('');
    try {
      const data = await api.post('/api/numerology/name', {
        full_name: fullName.trim(),
        birth_date: dob || undefined,
        name_type: nameType,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : t('numerology.errorName'));
    }
    setLoading(false);
  };

  const getNameTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'full_name': t('numerology.fullNameOption'),
      'first_name': t('numerology.firstNameOption'),
      'last_name': t('numerology.lastNameOption'),
      'business_name': t('numerology.businessNameOption'),
    };
    return labels[type] || type;
  };

  return (
    <div className="space-y-6">
      {/* Input Card */}
      <Card className="bg-card border-0 shadow-soft max-w-2xl mx-auto">
        <CardContent className="p-6">
          <h3 className="font-semibold text-foreground mb-4 text-center flex items-center justify-center gap-2">
            <User className="w-5 h-5 text-sacred-gold" />
            {t('numerology.nameAnalyzeHeading')}
          </h3>
          
          <div className="space-y-4">
            {/* Name Type Selector */}
            <div>
              <label className="block text-sm text-muted-foreground mb-1">{t('numerology.nameType')}</label>
              <Select value={nameType} onValueChange={setNameType}>
                <SelectTrigger className="bg-card border-sacred-gold">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="full_name">{t('numerology.fullNameOption')}</SelectItem>
                  <SelectItem value="first_name">{t('numerology.firstNameOption')}</SelectItem>
                  <SelectItem value="last_name">{t('numerology.lastNameOption')}</SelectItem>
                  <SelectItem value="business_name">{t('numerology.businessNameOption')}</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Name Input */}
            <div>
              <label className="block text-sm text-muted-foreground mb-1">
                {t('numerology.enterName')} <span className="text-red-600">*</span>
              </label>
              <Input
                placeholder={t('numerology.enterName')}
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
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
              onClick={analyzeName}
              disabled={loading || !fullName.trim()}
              className="w-full bg-sacred-gold text-background hover:bg-gray-50"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('numerology.analyzing')}</>
              ) : (
                <><Calculator className="w-4 h-4 mr-2" />{t('numerology.analyzeName')}</>
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
                {t('numerology.nameReport')}
              </Heading>
              <p className="text-sm text-foreground mt-1">{result.name}</p>
              <Badge className="mt-2 bg-sacred-gold/20 text-sacred-gold border-sacred-gold">
                {getNameTypeLabel(result.name_type)}
              </Badge>
            </div>
          </Card>

          {/* Core Numbers Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { 
                label: t('numerology.pythagorean'), 
                value: result.numerology.pythagorean.number, 
                sub: result.numerology.pythagorean.calculation,
                color: 'bg-purple-100 text-purple-700' 
              },
              { 
                label: t('numerology.chaldean'), 
                value: result.numerology.chaldean.number, 
                sub: result.numerology.chaldean.calculation,
                color: 'bg-blue-100 text-blue-700' 
              },
              { 
                label: t('numerology.soulUrge'), 
                value: result.numerology.soul_urge.number, 
                sub: result.numerology.soul_urge.description,
                color: 'bg-green-100 text-green-800' 
              },
              { 
                label: t('numerology.personality'), 
                value: result.numerology.personality.number, 
                sub: result.numerology.personality.description,
                color: 'bg-yellow-100 text-yellow-700' 
              },
            ].map((item) => (
              <Card key={item.label} className="bg-card border-0 shadow-soft">
                <CardContent className="p-4 text-center">
                  <p className="text-xs text-muted-foreground mb-1">{item.label}</p>
                  <Badge className={`text-xl px-3 py-1 ${item.color}`}>{item.value}</Badge>
                  <p className="text-[10px] text-muted-foreground mt-1 leading-tight">{item.sub}</p>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Primary Prediction */}
          <Card className="bg-card border-0 shadow-soft-lg">
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-sacred-gold/20">
                <Sparkles className="w-5 h-5 text-sacred-gold" />
                <Heading as={4} variant={4}>
                  {result.predictions.primary.title} {t('numerology.energy')}
                </Heading>
                <Badge className="ml-auto bg-sacred-gold/20 text-sacred-gold border-sacred-gold">
                  {t('numerology.rulingPlanet')}: {result.predictions.primary.ruling_planet}
                </Badge>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-foreground mb-2">{t('numerology.keyTraits')}</p>
                  <div className="flex flex-wrap gap-2">
                    {result.predictions.primary.traits.map((trait, i) => (
                      <Badge key={i} variant="outline" className="border-sacred-gold/30 text-muted-foreground">
                        {trait}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground mb-2">{t('numerology.luckyElements')}</p>
                  <div className="space-y-1 text-sm">
                    <p className="text-muted-foreground">
                      <span className="text-sacred-gold">{t('numerology.luckyColors')}:</span> {result.predictions.primary.lucky_colors.join(', ')}
                    </p>
                    <p className="text-muted-foreground">
                      <span className="text-sacred-gold">{t('numerology.luckyDays')}:</span> {result.predictions.primary.lucky_days.join(', ')}
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-3 pt-3 border-t border-sacred-gold/20">
                <div>
                  <p className="text-sm font-medium text-foreground mb-1">{t('numerology.careerGuidance')}</p>
                  <p className="text-sm text-muted-foreground">{result.predictions.primary.career}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground mb-1">{t('numerology.relationshipInsights')}</p>
                  <p className="text-sm text-muted-foreground">{result.predictions.primary.relationships}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground mb-1">{t('numerology.healthNotes')}</p>
                  <p className="text-sm text-muted-foreground">{result.predictions.primary.health}</p>
                </div>
              </div>

              <div className="bg-sacred-gold/10 rounded-lg p-4 border border-sacred-gold/20">
                <p className="text-sm font-medium text-sacred-gold-dark mb-1">{t('numerology.spiritualAdvice')}</p>
                <p className="text-sm text-muted-foreground italic">{result.predictions.primary.advice}</p>
              </div>
            </CardContent>
          </Card>

          {/* Name Parts Analysis */}
          {(result.first_name_analysis || result.last_name_analysis) && (
            <div className="grid md:grid-cols-2 gap-4">
              {result.first_name_analysis && (
                <Card className="bg-card border-0 shadow-soft">
                  <CardContent className="p-4">
                    <p className="text-sm font-medium text-foreground mb-2">{t('numerology.firstNameAnalysis')}: {result.first_name_analysis.name}</p>
                    <Badge className="bg-purple-100 text-purple-700 mb-2">{t('numerology.number')} {result.first_name_analysis.number}</Badge>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {result.first_name_analysis.traits.slice(0, 5).map((trait, i) => (
                        <span key={i} className="text-xs bg-sacred-gold/10 text-sacred-gold-dark px-2 py-0.5 rounded">
                          {trait}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
              {result.last_name_analysis && (
                <Card className="bg-card border-0 shadow-soft">
                  <CardContent className="p-4">
                    <p className="text-sm font-medium text-foreground mb-2">{t('numerology.lastNameAnalysis')}: {result.last_name_analysis.name}</p>
                    <Badge className="bg-blue-100 text-blue-700 mb-2">{t('numerology.number')} {result.last_name_analysis.number}</Badge>
                    <p className="text-xs text-muted-foreground mt-2">{result.last_name_analysis.meaning}</p>
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {/* Life Path Compatibility */}
          {result.life_path_compatibility && (
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-3">{t('numerology.lifePathCompatibility')}</p>
                <div className="flex items-center justify-between mb-2">
                  <Text variant="muted" as="span">{t('numerology.nameNumber')}: {result.life_path_compatibility.name_number}</Text>
                  <Text variant="muted" as="span">{t('numerology.lifePathShort')}: {result.life_path_compatibility.life_path}</Text>
                </div>
                <Badge className={result.life_path_compatibility.is_compatible 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
                }>
                  {result.life_path_compatibility.is_compatible ? t('numerology.compatible') : t('numerology.needsAttention')}
                </Badge>
                <p className="text-sm text-muted-foreground mt-2">{result.life_path_compatibility.compatibility_note}</p>
              </CardContent>
            </Card>
          )}

          {/* Letter Breakdown */}
          {result.letter_breakdown.length > 0 && (
            <Card className="bg-card border-0 shadow-soft">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-foreground mb-3">{t('numerology.letterBreakdown')}</p>
                <div className="overflow-x-auto">
                  <Table className="w-full text-sm">
                    <TableHeader>
                      <TableRow className="border-b border-sacred-gold/20">
                        <TableHead className="text-left py-2 text-muted-foreground">{t('numerology.letter')}</TableHead>
                        <TableHead className="text-center py-2 text-muted-foreground">{t('numerology.pythagorean')}</TableHead>
                        <TableHead className="text-center py-2 text-muted-foreground">{t('numerology.chaldean')}</TableHead>
                        <TableHead className="text-center py-2 text-muted-foreground">{t('numerology.type')}</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {result.letter_breakdown.map((item, i) => (
                        <TableRow key={i} className="border-b border-sacred-gold/10">
                          <TableCell className="py-2 font-medium">{item.letter}</TableCell>
                          <TableCell className="py-2 text-center">{item.pythagorean}</TableCell>
                          <TableCell className="py-2 text-center">{item.chaldean}</TableCell>
                          <TableCell className="py-2 text-center">
                            <Badge variant="outline" className={item.is_vowel 
                              ? 'border-green-300 text-green-700 text-xs' 
                              : 'border-blue-300 text-blue-700 text-xs'
                            }>
                              {item.is_vowel ? t('numerology.vowel') : t('numerology.consonant')}
                            </Badge>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}