import { useState } from 'react';
import { Loader2, Eye, MapPin, HelpCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';

interface MookResult {
  numbers_entered: number[];
  sum: number;
  derived_number: number;
  question_topic: {
    topic: string;
    topic_hi: string;
    detail: string;
    detail_hi: string;
    category: string;
  } | null;
  lost_item_location: {
    location: string;
    location_hi: string;
    hint: string;
    hint_hi: string;
  } | null;
  method: string;
  method_hi: string;
}

export default function MookPrashna() {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const p = (en: string, hi: string) => (isHi ? (hi || en) : (en || hi));

  const [digits, setDigits] = useState<string[]>(Array(9).fill(''));
  const [result, setResult] = useState<MookResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const allFilled = digits.every((d) => d !== '' && !isNaN(Number(d)));

  const handleChange = (idx: number, val: string) => {
    const sanitized = val.replace(/\D/g, '').slice(-1);
    const next = [...digits];
    next[idx] = sanitized;
    setDigits(next);
  };

  const calculate = async () => {
    if (!allFilled) return;
    setLoading(true);
    setResult(null);
    setError('');
    try {
      const numbers = digits.map(Number);
      const data = await api.post('/api/numerology/mook-prashna', { numbers }) as MookResult;
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : (isHi ? 'त्रुटि हुई' : 'Calculation failed'));
    }
    setLoading(false);
  };

  const reset = () => {
    setDigits(Array(9).fill(''));
    setResult(null);
    setError('');
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-1">
        <Heading as={3} variant={3}>
          {isHi ? 'मूक प्रश्न & खोई वस्तु' : 'Mook Prashna & Khoyi Vastu'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi
            ? 'बिना बोले 9 अंक लिखें — आपका मन क्या सोच रहा है?'
            : 'Write 9 random numbers without thinking — reveal what your mind is asking'}
        </p>
      </div>

      {/* Instructions */}
      <Card className="bg-amber-50/60 border-amber-200/60">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <HelpCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="space-y-1 text-xs text-amber-800 leading-relaxed">
              {isHi ? (
                <>
                  <p><strong>विधि:</strong> मन में कोई प्रश्न रखें। बिना सोचे 9 अंक (0-9) लिखें।</p>
                  <p>सभी 9 अंकों का योग + 3 = आपका प्रश्न संख्या</p>
                  <p>यह प्रकट करता है: आप किस बारे में सोच रहे हैं और खोई वस्तु कहाँ है।</p>
                </>
              ) : (
                <>
                  <p><strong>Method:</strong> Hold a question in mind. Write 9 numbers (0–9) spontaneously, without thinking.</p>
                  <p>Sum of all 9 numbers + 3 = your derived number</p>
                  <p>Reveals: what topic you are thinking about AND where a lost item may be.</p>
                </>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Input Grid */}
      <Card className="bg-card border-sacred-gold/20 shadow-soft">
        <CardContent className="p-6 space-y-5">
          <p className="text-sm font-medium text-foreground text-center">
            {isHi ? '9 अंक लिखें (0 से 9)' : 'Enter 9 numbers (0 to 9)'}
          </p>
          <div className="grid grid-cols-9 gap-2">
            {digits.map((d, i) => (
              <Input
                key={i}
                value={d}
                onChange={(e) => handleChange(i, e.target.value)}
                maxLength={1}
                inputMode="numeric"
                className="text-center text-lg font-bold p-0 h-12 border-sacred-gold/40 focus:border-sacred-gold"
                placeholder="·"
              />
            ))}
          </div>
          <div className="flex gap-3">
            <Button
              onClick={calculate}
              disabled={loading || !allFilled}
              className="flex-1 bg-sacred-gold text-background hover:bg-sacred-gold/90"
            >
              {loading
                ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{isHi ? 'गणना...' : 'Calculating...'}</>
                : <><Eye className="w-4 h-4 mr-2" />{isHi ? 'प्रकट करें' : 'Reveal'}</>
              }
            </Button>
            <Button variant="outline" onClick={reset} className="border-sacred-gold/40">
              {isHi ? 'रीसेट' : 'Reset'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {error && (
        <div className="p-3 rounded-xl bg-red-50 border border-red-300 text-red-700 text-sm text-center">
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-4">
          {/* Derived Number */}
          <div className="flex items-center justify-center gap-4 py-3 bg-sacred-gold/10 rounded-xl border border-sacred-gold/30">
            <div className="text-center">
              <p className="text-xs text-muted-foreground">{isHi ? 'योग' : 'Sum'}</p>
              <p className="text-xl font-bold text-foreground">{result.sum}</p>
            </div>
            <span className="text-muted-foreground">+3 =</span>
            <div className="text-center">
              <p className="text-xs text-muted-foreground">{isHi ? 'प्रश्न संख्या' : 'Derived No.'}</p>
              <Badge className="text-2xl px-4 py-1 bg-sacred-gold text-background font-bold">
                {result.derived_number}
              </Badge>
            </div>
          </div>

          {/* Question Topic */}
          {result.question_topic && (
            <Card className="bg-gradient-to-br from-purple-50/80 to-purple-50/30 border-purple-200/60">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-center gap-2">
                  <HelpCircle className="w-5 h-5 text-purple-600" />
                  <span className="text-sm font-semibold text-purple-900">
                    {isHi ? 'आपका प्रश्न विषय' : 'Your Question Topic'}
                  </span>
                  <Badge className="ml-auto bg-purple-100 text-purple-700 border-purple-300 text-xs">
                    {result.question_topic.category}
                  </Badge>
                </div>
                <p className="text-base font-semibold text-purple-900">
                  {p(result.question_topic.topic, result.question_topic.topic_hi)}
                </p>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {p(result.question_topic.detail, result.question_topic.detail_hi)}
                </p>
              </CardContent>
            </Card>
          )}

          {/* Lost Item Location */}
          {result.lost_item_location && (
            <Card className="bg-gradient-to-br from-green-50/80 to-green-50/30 border-green-200/60">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-green-600" />
                  <span className="text-sm font-semibold text-green-900">
                    {isHi ? 'खोई वस्तु — संभावित स्थान' : 'Lost Item — Likely Location'}
                  </span>
                </div>
                <p className="text-base font-semibold text-green-900">
                  {p(result.lost_item_location.location, result.lost_item_location.location_hi)}
                </p>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {p(result.lost_item_location.hint, result.lost_item_location.hint_hi)}
                </p>
              </CardContent>
            </Card>
          )}

          {/* Method note */}
          <p className="text-center text-xs text-muted-foreground">
            {p(result.method, result.method_hi)}
          </p>
        </div>
      )}
    </div>
  );
}
