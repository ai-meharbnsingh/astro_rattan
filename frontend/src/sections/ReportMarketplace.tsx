import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  FileText, 
  Heart, 
  Briefcase, 
  Activity, 
  Calendar, 
  Sparkles,
  Check,
  Loader2,
  ArrowRight,
  Lock
} from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface Kundli {
  id: string;
  person_name: string;
  birth_date: string;
  birth_place: string;
}

interface ReportType {
  id: string;
  name: string;
  description: string;
  price: number;
  icon: React.ReactNode;
  features: string[];
  color: string;
}

const REPORT_TYPES: ReportType[] = [
  {
    id: 'full_kundli',
    name: 'Complete Kundli Analysis',
    description: 'Comprehensive 30+ page report covering all aspects of your birth chart',
    price: 999,
    icon: <FileText className="w-6 h-6" />,
    features: [
      'Detailed planetary positions',
      'House-by-house analysis',
      'Dasha periods timeline',
      'Dosha assessment',
      'Remedies & recommendations',
      'io-gita basin analysis',
      'Life predictions'
    ],
    color: 'bg-sacred-gold'
  },
  {
    id: 'marriage',
    name: 'Marriage & Compatibility',
    description: 'Deep insights into relationships, marriage timing, and partner compatibility',
    price: 799,
    icon: <Heart className="w-6 h-6" />,
    features: [
      'Marriage timing predictions',
      'Partner characteristics',
      'Mangal dosha analysis',
      'Compatibility factors',
      'Auspicious dates',
      'Relationship remedies'
    ],
    color: 'bg-rose-500'
  },
  {
    id: 'career',
    name: 'Career & Finance',
    description: 'Professional growth, wealth potential, and optimal career paths',
    price: 799,
    icon: <Briefcase className="w-6 h-6" />,
    features: [
      'Career path analysis',
      'Wealth yoga identification',
      'Best industries/sectors',
      'Promotion timelines',
      'Business vs job suitability',
      'Financial remedies'
    ],
    color: 'bg-emerald-500'
  },
  {
    id: 'health',
    name: 'Health & Wellness',
    description: 'Health tendencies, preventive measures, and vitality analysis',
    price: 699,
    icon: <Activity className="w-6 h-6" />,
    features: [
      'Health prone areas',
      'Vital organ analysis',
      'Preventive measures',
      'Ayurvedic constitution',
      'Best dietary practices',
      'Health timelines'
    ],
    color: 'bg-amber-500'
  },
  {
    id: 'yearly',
    name: 'Yearly Guidance',
    description: '12-month forecast with monthly predictions and important dates',
    price: 599,
    icon: <Calendar className="w-6 h-6" />,
    features: [
      'Month-by-month forecast',
      'Favorable periods',
      'Challenging transits',
      'Important dates',
      'Remedies for the year',
      'Opportunity windows'
    ],
    color: 'bg-violet-500'
  }
];

export default function ReportMarketplace() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [kundlis, setKundlis] = useState<Kundli[]>([]);
  const [selectedKundli, setSelectedKundli] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState<string | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    
    api.get('/api/kundli/list')
      .then(data => {
        const list = Array.isArray(data) ? data : data.kundlis || [];
        setKundlis(list);
        if (list.length > 0) {
          setSelectedKundli(list[0].id);
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load kundlis');
        setLoading(false);
      });
  }, [isAuthenticated]);

  const handleRequestReport = async (reportType: string) => {
    if (!selectedKundli) {
      setError('Please select a kundli first');
      return;
    }
    
    setRequesting(reportType);
    setError('');
    
    try {
      // Request the report
      const reportData = await api.post('/api/reports/request', {
        kundli_id: selectedKundli,
        report_type: reportType
      });
      
      const reportId = reportData.report?.id;
      if (!reportId) {
        throw new Error('Failed to create report');
      }
      
      // Initiate payment
      const paymentData = await api.post('/api/payments/report/initiate', {
        report_id: reportId,
        provider: 'razorpay'
      });
      
      // Redirect to payment
      if (paymentData.payment_url) {
        window.location.href = paymentData.payment_url;
      } else if (paymentData.razorpay_key_id) {
        // Handle Razorpay checkout
        const rzOptions = {
          key: paymentData.razorpay_key_id,
          amount: paymentData.amount * 100,
          currency: 'INR',
          name: 'AstroVedic',
          description: `${REPORT_TYPES.find(r => r.id === reportType)?.name} Report`,
          order_id: paymentData.provider_payment_id,
          handler: function() {
            navigate('/profile?tab=reports');
          },
          prefill: {
            name: '',
            email: '',
          },
          theme: {
            color: '#4f46e5'
          }
        };
        
        const razorpayScript = document.createElement('script');
        razorpayScript.src = 'https://checkout.razorpay.com/v1/checkout.js';
        razorpayScript.onload = () => {
          // @ts-ignore
          const rzp = new window.Razorpay(rzOptions);
          rzp.open();
        };
        document.body.appendChild(razorpayScript);
      } else {
        // COD or test mode - redirect to profile
        navigate('/profile?tab=reports');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to request report');
      setRequesting(null);
    }
  };

  const formatPrice = (price: number) => 
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

  if (!isAuthenticated) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <Lock className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-cosmic-text mb-2">Sign In Required</h2>
        <p className="text-cosmic-text-secondary mb-6">Please log in to purchase personalized reports.</p>
        <Button onClick={() => navigate('/login')} className="bg-sacred-gold text-[#1a1a2e]">
          Sign In
        </Button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
      </div>
    );
  }

  if (kundlis.length === 0) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <FileText className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-cosmic-text mb-2">No Kundlis Found</h2>
        <p className="text-cosmic-text-secondary mb-6">Generate a kundli first to purchase personalized reports.</p>
        <Button onClick={() => navigate('/kundli')} className="bg-sacred-gold text-[#1a1a2e]">
          Generate Kundli <ArrowRight className="w-4 h-4 ml-2" />
        </Button>
      </div>
    );
  }

  return (
    <section className="max-w-6xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-4">
          <Sparkles className="w-4 h-4" />Premium Reports
        </div>
        <h1 className="text-3xl sm:text-4xl font-display font-bold text-cosmic-text mb-3">
          Personalized <span className="text-gradient-indigo">Astrology Reports</span>
        </h1>
        <p className="text-cosmic-text-secondary max-w-2xl mx-auto">
          Unlock deep insights with our comprehensive PDF reports. Generated using advanced Vedic astrology 
          and the io-gita analysis engine.
        </p>
      </div>

      {/* Kundli Selector */}
      <Card className="mb-8 border-0 shadow-soft bg-cosmic-card">
        <CardContent className="p-6">
          <label className="text-sm font-medium text-cosmic-text mb-3 block">
            Select Kundli for Report
          </label>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-3">
            {kundlis.map((kundli) => (
              <button
                key={kundli.id}
                onClick={() => setSelectedKundli(kundli.id)}
                className={`p-4 rounded-xl border-2 text-left transition-all ${
                  selectedKundli === kundli.id 
                    ? 'border-sacred-gold bg-sacred-gold/5' 
                    : 'border-sacred-gold/15 hover:border-cosmic-text-muted'
                }`}
              >
                <p className="font-semibold text-cosmic-text">{kundli.person_name}</p>
                <p className="text-sm text-cosmic-text-secondary">{kundli.birth_date}</p>
                <p className="text-xs text-cosmic-text-muted">{kundli.birth_place}</p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-red-900/20 text-red-400 text-sm text-center">
          {error}
        </div>
      )}

      {/* Report Types */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {REPORT_TYPES.map((report) => (
          <Card key={report.id} className="group border-0 shadow-soft hover:shadow-soft-lg transition-all flex flex-col">
            <CardContent className="p-6 flex flex-col flex-1">
              {/* Icon & Price */}
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 rounded-xl ${report.color} text-[#e8e0d4] flex items-center justify-center`}>
                  {report.icon}
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-cosmic-text">{formatPrice(report.price)}</p>
                  <Badge variant="outline" className="text-xs">PDF Download</Badge>
                </div>
              </div>

              {/* Title & Description */}
              <h3 className="text-lg font-display font-semibold text-cosmic-text mb-2">
                {report.name}
              </h3>
              <p className="text-sm text-cosmic-text-secondary mb-4 flex-1">
                {report.description}
              </p>

              {/* Features */}
              <ul className="space-y-2 mb-6">
                {report.features.map((feature, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-cosmic-text-secondary">
                    <Check className="w-4 h-4 text-green-500 mt-0.5 shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <Button 
                onClick={() => handleRequestReport(report.id)}
                disabled={requesting === report.id || !selectedKundli}
                className={`w-full ${report.color} text-[#e8e0d4] hover:opacity-90`}
              >
                {requesting === report.id ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Processing...</>
                ) : (
                  <>Get Report <ArrowRight className="w-4 h-4 ml-2" /></>
                )}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Trust Badges */}
      <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        <div className="p-4">
          <p className="text-2xl font-bold text-sacred-gold">30+</p>
          <p className="text-sm text-cosmic-text-secondary">Pages per report</p>
        </div>
        <div className="p-4">
          <p className="text-2xl font-bold text-sacred-gold">100%</p>
          <p className="text-sm text-cosmic-text-secondary">Personalized</p>
        </div>
        <div className="p-4">
          <p className="text-2xl font-bold text-sacred-gold">PDF</p>
          <p className="text-sm text-cosmic-text-secondary">Instant download</p>
        </div>
        <div className="p-4">
          <p className="text-2xl font-bold text-sacred-gold">24/7</p>
          <p className="text-sm text-cosmic-text-secondary">Available</p>
        </div>
      </div>
    </section>
  );
}
