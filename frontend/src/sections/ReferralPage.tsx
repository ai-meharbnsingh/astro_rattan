import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Loader2, Copy, Check, Users, DollarSign, Clock, Gift, Share2, Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';

interface ReferralStats {
  total_referrals: number;
  total_earnings: number;
  pending_earnings: number;
  paid_earnings: number;
}

interface Earning {
  id: number;
  date: string;
  referred_user: string;
  order_amount: number;
  commission: number;
  status: string;
}

const formatPrice = (price: number) =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);

export default function ReferralPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [referralCode, setReferralCode] = useState('');
  const [stats, setStats] = useState<ReferralStats>({ total_referrals: 0, total_earnings: 0, pending_earnings: 0, paid_earnings: 0 });
  const [earnings, setEarnings] = useState<Earning[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [copied, setCopied] = useState(false);
  const [linkCopied, setLinkCopied] = useState(false);

  // Apply referral code state
  const [applyCode, setApplyCode] = useState('');
  const [applyMsg, setApplyMsg] = useState('');
  const [applyError, setApplyError] = useState(false);
  const [validating, setValidating] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) { setLoading(false); return; }
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      const [codeRes, statsRes, earningsRes] = await Promise.allSettled([
        api.get('/api/referral/my-code'),
        api.get('/api/referral/stats'),
        api.get('/api/referral/earnings'),
      ]);
      if (!cancelled) {
        if (codeRes.status === 'fulfilled' && codeRes.value?.code) {
          setReferralCode(codeRes.value.code);
        }
        if (statsRes.status === 'fulfilled') {
          const s = statsRes.value;
          setStats({
            total_referrals: s.total_referrals ?? 0,
            total_earnings: s.total_earnings ?? 0,
            pending_earnings: s.pending_earnings ?? 0,
            paid_earnings: s.paid_earnings ?? 0,
          });
        }
        if (earningsRes.status === 'fulfilled') {
          const list = Array.isArray(earningsRes.value) ? earningsRes.value : earningsRes.value?.earnings || [];
          setEarnings(list);
        }
        setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, [isAuthenticated]);

  const generateCode = async () => {
    setGenerating(true);
    try {
      const res = await api.post('/api/referral/generate', {});
      if (res?.code) setReferralCode(res.code);
    } catch { /* empty */ }
    setGenerating(false);
  };

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(referralCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch { /* empty */ }
  };

  const copyLink = async () => {
    const link = `${window.location.origin}/login?ref=${referralCode}`;
    try {
      await navigator.clipboard.writeText(link);
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 2000);
    } catch { /* empty */ }
  };

  const validateAndApply = async () => {
    if (!applyCode.trim()) return;
    setValidating(true);
    setApplyMsg('');
    setApplyError(false);
    try {
      await api.post('/api/referral/apply', { code: applyCode.trim() });
      setApplyMsg('Referral code applied successfully!');
      setApplyError(false);
      setApplyCode('');
    } catch (err) {
      setApplyMsg(err instanceof Error ? err.message : 'Invalid referral code');
      setApplyError(true);
    }
    setValidating(false);
  };

  if (!isAuthenticated && !authLoading) {
    return (
      <div className="max-w-4xl mx-auto py-24 px-4 text-center">
        <Gift className="w-16 h-16 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-display font-bold text-cosmic-text mb-2">Sign In Required</h2>
        <p className="text-cosmic-text-secondary">Please log in to access the referral program.</p>
      </div>
    );
  }

  if (loading || authLoading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
      </div>
    );
  }

  const shareLink = `${window.location.origin}/login?ref=${referralCode}`;

  const statCards = [
    { label: 'Total Referrals', value: stats.total_referrals, icon: Users, color: 'bg-purple-500/20 text-purple-400', isCurrency: false },
    { label: 'Total Earnings', value: stats.total_earnings, icon: DollarSign, color: 'bg-green-500/20 text-green-400', isCurrency: true },
    { label: 'Pending Earnings', value: stats.pending_earnings, icon: Clock, color: 'bg-yellow-500/20 text-yellow-400', isCurrency: true },
    { label: 'Paid Earnings', value: stats.paid_earnings, icon: DollarSign, color: 'bg-blue-500/20 text-blue-400', isCurrency: true },
  ];

  const steps = [
    { step: '1', title: 'Share Your Code', description: 'Share your unique referral code or link with friends and family.' },
    { step: '2', title: 'Friend Signs Up', description: 'Your friend creates an account using your referral code.' },
    { step: '3', title: 'You Earn 10%', description: 'Earn 10% commission on every order your referred friend places.' },
  ];

  return (
    <section className="max-w-4xl mx-auto py-24 px-4">
      {/* Page Header */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-sacred font-bold text-gradient-gold mb-2">Refer & Earn</h1>
        <p className="text-cosmic-text-secondary text-lg">Share the cosmic wisdom and earn rewards for every referral.</p>
      </div>

      {/* Referral Code Display Card */}
      <Card className="bg-cosmic-card border-sacred-gold/20 shadow-soft mb-8">
        <CardContent className="p-6">
          <h3 className="font-sacred font-semibold text-cosmic-text mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-sacred-gold" />
            Your Referral Code
          </h3>
          {referralCode ? (
            <div className="space-y-4">
              {/* Code display */}
              <div className="flex items-center gap-3">
                <div className="flex-1 bg-cosmic-bg border border-sacred-gold/20 rounded-xl px-5 py-3 text-center">
                  <span className="text-2xl font-bold tracking-widest text-sacred-gold font-sacred">{referralCode}</span>
                </div>
                <Button
                  onClick={copyCode}
                  className="bg-sacred-gold text-white hover:bg-sacred-gold-dark shrink-0"
                >
                  {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                </Button>
              </div>

              {/* Share link */}
              <div>
                <label className="text-sm font-medium text-cosmic-text-secondary mb-2 block flex items-center gap-1">
                  <Share2 className="w-4 h-4" /> Share Link
                </label>
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-cosmic-bg border border-sacred-gold/20 rounded-xl px-4 py-2.5 text-sm text-cosmic-text-secondary truncate">
                    {shareLink}
                  </div>
                  <Button
                    onClick={copyLink}
                    variant="outline"
                    className="border-sacred-gold/20 text-sacred-gold hover:bg-sacred-gold/10 shrink-0"
                  >
                    {linkCopied ? <Check className="w-4 h-4 mr-1" /> : <Copy className="w-4 h-4 mr-1" />}
                    {linkCopied ? 'Copied' : 'Copy Link'}
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-6">
              <p className="text-cosmic-text-secondary mb-4">You don't have a referral code yet. Generate one to start earning!</p>
              <Button
                onClick={generateCode}
                disabled={generating}
                className="bg-sacred-gold text-white hover:bg-sacred-gold-dark"
              >
                {generating ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Sparkles className="w-4 h-4 mr-2" />}
                {generating ? 'Generating...' : 'Generate My Code'}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Stats Dashboard */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        {statCards.map((s) => (
          <Card key={s.label} className="bg-cosmic-card border-sacred-gold/20 shadow-soft">
            <CardContent className="p-4 text-center">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center mx-auto mb-2 ${s.color}`}>
                <s.icon className="w-5 h-5" />
              </div>
              <p className="text-2xl font-bold text-cosmic-text">
                {s.isCurrency ? formatPrice(s.value) : s.value}
              </p>
              <p className="text-xs text-cosmic-text-secondary">{s.label}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Earnings Table */}
      <Card className="bg-cosmic-card border-sacred-gold/20 shadow-soft mb-8">
        <CardContent className="p-4">
          <h3 className="font-sacred font-semibold text-cosmic-text mb-4 px-2">Referral Earnings</h3>
          {earnings.length === 0 ? (
            <div className="text-center py-8">
              <DollarSign className="w-10 h-10 text-cosmic-text-muted mx-auto mb-2" />
              <p className="text-cosmic-text-secondary">No earnings yet. Share your code to start earning!</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Referred User</TableHead>
                  <TableHead>Order Amount</TableHead>
                  <TableHead>Commission</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {earnings.map((e) => (
                  <TableRow key={e.id}>
                    <TableCell className="text-sm text-cosmic-text-secondary">
                      {new Date(e.date).toLocaleDateString()}
                    </TableCell>
                    <TableCell className="font-medium text-cosmic-text">{e.referred_user}</TableCell>
                    <TableCell className="text-cosmic-text">{formatPrice(e.order_amount)}</TableCell>
                    <TableCell className="text-sacred-gold font-semibold">{formatPrice(e.commission)}</TableCell>
                    <TableCell>
                      <Badge
                        variant="outline"
                        className={
                          e.status === 'paid'
                            ? 'border-green-500/30 text-green-400'
                            : e.status === 'pending'
                            ? 'border-yellow-500/30 text-yellow-400'
                            : ''
                        }
                      >
                        {e.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* How It Works */}
      <Card className="bg-cosmic-card border-sacred-gold/20 shadow-soft mb-8">
        <CardContent className="p-6">
          <h3 className="font-sacred font-semibold text-cosmic-text mb-6 text-center text-xl">How It Works</h3>
          <div className="grid sm:grid-cols-3 gap-6">
            {steps.map((s) => (
              <div key={s.step} className="text-center">
                <div className="w-12 h-12 rounded-full bg-sacred-gold/20 text-sacred-gold font-bold text-xl flex items-center justify-center mx-auto mb-3">
                  {s.step}
                </div>
                <h4 className="font-semibold text-cosmic-text mb-1">{s.title}</h4>
                <p className="text-sm text-cosmic-text-secondary">{s.description}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Apply Referral Code */}
      <Card className="bg-cosmic-card border-sacred-gold/20 shadow-soft">
        <CardContent className="p-6">
          <h3 className="font-sacred font-semibold text-cosmic-text mb-4 flex items-center gap-2">
            <Gift className="w-5 h-5 text-sacred-gold" />
            Apply a Referral Code
          </h3>
          <p className="text-sm text-cosmic-text-secondary mb-4">
            Have a referral code from a friend? Enter it below to link your account.
          </p>
          {applyMsg && (
            <div className={`mb-4 p-3 rounded-xl text-sm text-center ${applyError ? 'bg-red-900/20 text-red-400' : 'bg-green-900/20 text-green-400'}`}>
              {applyMsg}
            </div>
          )}
          <div className="flex items-center gap-3">
            <Input
              value={applyCode}
              onChange={(e) => setApplyCode(e.target.value)}
              placeholder="Enter referral code"
              className="bg-cosmic-bg border-sacred-gold/15 flex-1"
            />
            <Button
              onClick={validateAndApply}
              disabled={validating || !applyCode.trim()}
              className="bg-sacred-gold text-white hover:bg-sacred-gold-dark shrink-0"
            >
              {validating ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
              {validating ? 'Validating...' : 'Validate & Apply'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </section>
  );
}
