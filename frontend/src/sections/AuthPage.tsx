import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Stars, Mail, Lock, User, ChevronRight, Star, ShieldCheck, ArrowLeft } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

type RegStep = 'email' | 'otp' | 'details';

export default function AuthPage() {
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const { t } = useTranslation();
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ name: '', email: '', password: '' });
  const [isAstrologer, setIsAstrologer] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  // OTP verification state
  const [regStep, setRegStep] = useState<RegStep>('email');
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [emailToken, setEmailToken] = useState('');
  const [countdown, setCountdown] = useState(0);
  const otpRefs = useRef<(HTMLInputElement | null)[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const startCountdown = () => {
    setCountdown(60);
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) { clearInterval(timerRef.current!); return 0; }
        return prev - 1;
      });
    }, 1000);
  };

  const handleLogin = async () => {
    if (!loginForm.email || !loginForm.password) return;
    setLoading(true); setError('');
    try { await login(loginForm.email, loginForm.password); navigate('/'); }
    catch (err) { setError(err instanceof Error ? err.message : 'Login failed'); }
    finally { setLoading(false); }
  };

  const handleSendOtp = async () => {
    if (!registerForm.email) return;
    setLoading(true); setError(''); setSuccess('');
    try {
      await api.post('/api/auth/send-otp', { email: registerForm.email });
      setRegStep('otp');
      setSuccess('Verification code sent to your email');
      startCountdown();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send verification code');
    } finally { setLoading(false); }
  };

  const handleVerifyOtp = async () => {
    const otpValue = otp.join('');
    if (otpValue.length !== 6) return;
    setLoading(true); setError(''); setSuccess('');
    try {
      const data = await api.post('/api/auth/verify-otp', { email: registerForm.email, otp: otpValue });
      setEmailToken(data.email_token);
      setRegStep('details');
      setSuccess('Email verified! Complete your registration.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid verification code');
    } finally { setLoading(false); }
  };

  const handleResendOtp = async () => {
    if (countdown > 0) return;
    await handleSendOtp();
  };

  const handleRegister = async () => {
    if (!registerForm.name || !registerForm.email || !registerForm.password || !emailToken) return;
    setLoading(true); setError(''); setSuccess('');
    try {
      if (isAstrologer) {
        const data = await api.post('/api/auth/register-astrologer', {
          email: registerForm.email,
          password: registerForm.password,
          name: registerForm.name,
          email_token: emailToken,
        });
        localStorage.setItem('astrovedic_token', data.token);
        window.location.href = '/astrologer-panel';
      } else {
        await register(registerForm.email, registerForm.password, registerForm.name, emailToken);
        navigate('/');
      }
    }
    catch (err) { setError(err instanceof Error ? err.message : 'Registration failed'); }
    finally { setLoading(false); }
  };

  const handleOtpChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return; // digits only
    const newOtp = [...otp];
    newOtp[index] = value.slice(-1); // take last char
    setOtp(newOtp);
    // Auto-focus next input
    if (value && index < 5) {
      otpRefs.current[index + 1]?.focus();
    }
  };

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      otpRefs.current[index - 1]?.focus();
    }
    if (e.key === 'Enter' && otp.join('').length === 6) {
      handleVerifyOtp();
    }
  };

  const handleOtpPaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    if (pasted.length === 6) {
      setOtp(pasted.split(''));
      otpRefs.current[5]?.focus();
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-24 px-4 bg-transparent">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4 shadow-glow-gold">
            <Stars className="w-8 h-8 text-cosmic-bg" />
          </div>
          <h2 className="text-2xl sm:text-3xl font-sacred font-bold text-cosmic-text mb-2">{t('auth.welcome')}</h2>
          <p className="text-cosmic-text-secondary">{t('auth.subtitle')}</p>
        </div>
        {error && <div className="mb-4 p-3 rounded-xl bg-red-900/30 border border-red-500/30 text-red-400 text-sm text-center">{error}</div>}
        {success && <div className="mb-4 p-3 rounded-xl bg-green-900/30 border border-green-500/30 text-green-400 text-sm text-center">{success}</div>}
        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid grid-cols-2 bg-cosmic-card mb-6 border border-sacred-gold/10">
            <TabsTrigger value="login" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary">{t('auth.signIn')}</TabsTrigger>
            <TabsTrigger value="register" onClick={() => { setRegStep('email'); setOtp(['','','','','','']); setEmailToken(''); setError(''); setSuccess(''); }} className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary">{t('auth.signUp')}</TabsTrigger>
          </TabsList>
          <TabsContent value="login" className="mt-0">
            <div className="space-y-4">
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="email" value={loginForm.email} onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })} placeholder={t('auth.email')} className="pl-10 input-sacred" />
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="password" value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} placeholder={t('auth.password')} onKeyDown={(e) => e.key === 'Enter' && handleLogin()} className="pl-10 input-sacred" />
              </div>
              <Button onClick={handleLogin} disabled={loading || !loginForm.email || !loginForm.password} className="w-full btn-sacred disabled:opacity-50">
                {loading ? t('common.loading') : t('auth.signIn')}<ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </TabsContent>
          <TabsContent value="register" className="mt-0">
            {/* Step 1: Enter email */}
            {regStep === 'email' && (
              <div className="space-y-4">
                <div className="text-center mb-2">
                  <ShieldCheck className="w-8 h-8 text-sacred-gold mx-auto mb-2" />
                  <p className="text-sm text-cosmic-text-secondary">Enter your email to receive a verification code</p>
                </div>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="email" value={registerForm.email} onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })} placeholder={t('auth.email')} onKeyDown={(e) => e.key === 'Enter' && handleSendOtp()} className="pl-10 input-sacred" />
                </div>
                <Button onClick={handleSendOtp} disabled={loading || !registerForm.email} className="w-full btn-sacred disabled:opacity-50">
                  {loading ? t('common.loading') : 'Send Verification Code'}<ChevronRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            )}

            {/* Step 2: Enter OTP */}
            {regStep === 'otp' && (
              <div className="space-y-4">
                <button onClick={() => { setRegStep('email'); setError(''); setSuccess(''); }} className="flex items-center gap-1 text-sm text-cosmic-text-secondary hover:text-sacred-gold transition-colors">
                  <ArrowLeft className="w-4 h-4" /> Change email
                </button>
                <div className="text-center mb-2">
                  <ShieldCheck className="w-8 h-8 text-sacred-gold mx-auto mb-2" />
                  <p className="text-sm text-cosmic-text-secondary">
                    Enter the 6-digit code sent to<br />
                    <span className="text-sacred-gold font-medium">{registerForm.email}</span>
                  </p>
                </div>
                {/* OTP input boxes */}
                <div className="flex justify-center gap-2" onPaste={handleOtpPaste}>
                  {otp.map((digit, i) => (
                    <input
                      key={i}
                      ref={(el) => { otpRefs.current[i] = el; }}
                      type="text"
                      inputMode="numeric"
                      maxLength={1}
                      value={digit}
                      onChange={(e) => handleOtpChange(i, e.target.value)}
                      onKeyDown={(e) => handleOtpKeyDown(i, e)}
                      className="w-12 h-14 text-center text-xl font-bold rounded-lg border border-sacred-gold/30 bg-cosmic-card text-cosmic-text focus:border-sacred-gold focus:ring-1 focus:ring-sacred-gold outline-none transition-colors"
                    />
                  ))}
                </div>
                <Button onClick={handleVerifyOtp} disabled={loading || otp.join('').length !== 6} className="w-full btn-sacred disabled:opacity-50">
                  {loading ? t('common.loading') : 'Verify Code'}<ShieldCheck className="w-5 h-5 ml-2" />
                </Button>
                <div className="text-center">
                  {countdown > 0 ? (
                    <p className="text-sm text-cosmic-text-muted">Resend code in {countdown}s</p>
                  ) : (
                    <button onClick={handleResendOtp} className="text-sm text-sacred-gold hover:underline">Resend verification code</button>
                  )}
                </div>
              </div>
            )}

            {/* Step 3: Complete registration */}
            {regStep === 'details' && (
              <div className="space-y-4">
                <div className="text-center mb-2">
                  <div className="inline-flex items-center gap-2 bg-green-900/20 border border-green-500/30 rounded-full px-4 py-1.5 text-green-400 text-sm">
                    <ShieldCheck className="w-4 h-4" /> {registerForm.email} verified
                  </div>
                </div>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="text" value={registerForm.name} onChange={(e) => setRegisterForm({ ...registerForm, name: e.target.value })} placeholder={t('auth.fullName')} className="pl-10 input-sacred" />
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="password" value={registerForm.password} onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })} placeholder={t('auth.password') + ' (min 8 characters)'} onKeyDown={(e) => e.key === 'Enter' && handleRegister()} className="pl-10 input-sacred" />
                </div>
                {/* Astrologer toggle */}
                <button
                  onClick={() => setIsAstrologer(!isAstrologer)}
                  className={`w-full flex items-center gap-3 p-3 border transition-colors rounded-lg ${
                    isAstrologer
                      ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold'
                      : 'border-sacred-gold/20 text-cosmic-text-secondary hover:border-sacred-gold/40'
                  }`}
                >
                  <Star className={`w-5 h-5 ${isAstrologer ? 'text-sacred-gold' : 'text-cosmic-text-muted'}`} />
                  <span className="text-sm font-medium">{t('astrologer.registerAsAstrologer')}</span>
                  <div className={`ml-auto w-10 h-5 rounded-full transition-colors ${isAstrologer ? 'bg-sacred-gold' : 'bg-cosmic-surface'}`}>
                    <div className={`w-4 h-4 rounded-full bg-[#e8e0d4] shadow-sm transform transition-transform mt-0.5 ${isAstrologer ? 'translate-x-5.5 ml-[22px]' : 'ml-0.5'}`} />
                  </div>
                </button>
                <Button onClick={handleRegister} disabled={loading || !registerForm.name || !registerForm.password} className="w-full btn-sacred disabled:opacity-50">
                  {loading ? t('common.loading') : (isAstrologer ? t('astrologer.registerAsAstrologer') : t('auth.signUp'))}<ChevronRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
