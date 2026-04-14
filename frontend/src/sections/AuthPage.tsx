import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Stars, Mail, Lock, User, ChevronRight, Star, ShieldCheck, ArrowLeft, Phone, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

type RegStep = 'email' | 'otp' | 'details';
type ResetStep = 'email' | 'otp' | 'newpass' | 'done';

export default function AuthPage() {
  const navigate = useNavigate();
  const { login, register } = useAuth();
  const { t } = useTranslation();
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ name: '', email: '', password: '', phone: '' });
  const [isAstrologer, setIsAstrologer] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  // Password visibility state
  const [showLoginPassword, setShowLoginPassword] = useState(false);
  const [showRegisterPassword, setShowRegisterPassword] = useState(false);
  const [showResetPassword, setShowResetPassword] = useState(false);

  // OTP verification state
  const [regStep, setRegStep] = useState<RegStep>('email');
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [emailToken, setEmailToken] = useState('');
  const [countdown, setCountdown] = useState(0);
  const otpRefs = useRef<(HTMLInputElement | null)[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // OTP paste feedback
  const [otpPasted, setOtpPasted] = useState(false);

  // Forgot password state
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [resetStep, setResetStep] = useState<ResetStep>('email');
  const [resetEmail, setResetEmail] = useState('');
  const [resetOtp, setResetOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');

  const handleForgotPassword = async () => {
    if (!resetEmail) return;
    setLoading(true); setError('');
    try {
      await api.post('/api/auth/forgot-password', { email: resetEmail });
      setResetStep('otp');
      setSuccess(t('auth.resetCodeSentIfRegistered'));
    } catch (err) { setError(err instanceof Error ? err.message : t('auth.failed')); }
    finally { setLoading(false); }
  };

  const handleResetPassword = async () => {
    if (!resetOtp || !newPassword || newPassword.length < 8) { setError(t('auth.passwordMinLength')); return; }
    setLoading(true); setError('');
    try {
      await api.post('/api/auth/reset-password', { email: resetEmail, otp: resetOtp, new_password: newPassword });
      setResetStep('done');
      setSuccess(t('auth.passwordResetSuccess'));
    } catch (err) { setError(err instanceof Error ? err.message : t('auth.resetFailed')); }
    finally { setLoading(false); }
  };

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
    try { const data = await login(loginForm.email, loginForm.password); navigate(data.user?.role === 'admin' ? '/admin' : '/'); }
    catch (err) { setError(err instanceof Error ? err.message : t('auth.loginFailed')); }
    finally { setLoading(false); }
  };

  const handleSendOtp = async () => {
    if (!registerForm.email) return;
    setLoading(true); setError(''); setSuccess('');
    try {
      await api.post('/api/auth/send-otp', { email: registerForm.email });
      setRegStep('otp');
      setSuccess(t('auth.verificationCodeSent'));
      startCountdown();
    } catch (err) {
      setError(err instanceof Error ? err.message : t('auth.failedToSendVerificationCode'));
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
      setSuccess(t('auth.emailVerifiedCompleteRegistration'));
    } catch (err) {
      setError(err instanceof Error ? err.message : t('auth.invalidVerificationCode'));
    } finally { setLoading(false); }
  };

  const handleResendOtp = async () => {
    if (countdown > 0) return;
    await handleSendOtp();
  };

  const handleRegister = async () => {
    if (!registerForm.name || !registerForm.email || !registerForm.password || !emailToken) return;
    if (isAstrologer && !registerForm.phone.trim()) { setError(t('auth.phoneRequiredForAstrologerRegistration')); return; }
    setLoading(true); setError(''); setSuccess('');
    try {
      if (isAstrologer) {
        const data = await api.post('/api/auth/register-astrologer', {
          email: registerForm.email,
          password: registerForm.password,
          name: registerForm.name,
          email_token: emailToken,
          phone: registerForm.phone.trim(),
        });
        localStorage.setItem('astrorattan_token', data.token);
        if (data.refresh_token) localStorage.setItem('astrorattan_refresh_token', data.refresh_token);
        window.location.href = '/';
      } else {
        await register(registerForm.email, registerForm.password, registerForm.name, emailToken);
        navigate('/');
      }
    }
    catch (err) { setError(err instanceof Error ? err.message : t('auth.registrationFailed')); }
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
      setOtpPasted(true);
      setTimeout(() => setOtpPasted(false), 1200);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-24 px-4 sm:px-8 bg-transparent">
      <div className="w-full max-w-md mx-4 sm:mx-auto">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4 shadow-glow-gold">
            <Stars className="w-8 h-8 text-cosmic-bg" />
          </div>
          <h2 className="text-xl sm:text-2xl md:text-3xl font-sans font-bold text-cosmic-text mb-2">{t('auth.welcome')}</h2>
          <p className="text-cosmic-text-secondary">{t('auth.subtitle')}</p>
          <p className="text-xs text-gray-500 mt-2">{t('auth.dataEncrypted') || 'Your data is encrypted and never shared'}</p>
        </div>
        {error && <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-300 text-red-700 text-sm text-center">{error}</div>}
        {success && <div className="mb-4 p-3 rounded-xl bg-green-50 border border-green-300 text-green-700 text-sm text-center">{success}</div>}
        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid grid-cols-2 bg-cosmic-card mb-6 border border-sacred-gold">
            <TabsTrigger value="login" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary">{t('auth.signIn')}</TabsTrigger>
            <TabsTrigger value="register" onClick={() => { setRegStep('email'); setOtp(['','','','','','']); setEmailToken(''); setError(''); setSuccess(''); }} className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary">{t('auth.signUp')}</TabsTrigger>
          </TabsList>
          <TabsContent value="login" className="mt-0">
            <div className="space-y-3 sm:space-y-4">
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type="email" value={loginForm.email} onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })} placeholder={t('auth.email')} className="pl-10 input-sacred" />
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                <Input type={showLoginPassword ? 'text' : 'password'} value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} placeholder={t('auth.password')} onKeyDown={(e) => e.key === 'Enter' && handleLogin()} className="pl-10 pr-10 input-sacred" />
                <button type="button" onClick={() => setShowLoginPassword(!showLoginPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-sacred-gold hover:text-sacred-gold-dark transition-colors" tabIndex={-1}>
                  {showLoginPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <Button onClick={handleLogin} disabled={loading || !loginForm.email || !loginForm.password} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold disabled:opacity-50">
                {loading ? t('common.loading') : t('auth.signIn')}<ChevronRight className="w-5 h-5 ml-2" />
              </Button>
              <button onClick={() => { setShowForgotPassword(true); setResetStep('email'); setError(''); setSuccess(''); }} className="w-full text-center text-sm text-sacred-gold-dark font-medium hover:underline mt-2">
                {t('auth.forgotPassword')}
              </button>
            </div>
          </TabsContent>
          <TabsContent value="register" className="mt-0">
            {/* Step 1: Enter email */}
            {regStep === 'email' && (
              <div className="space-y-3 sm:space-y-4">
                <div className="text-center mb-2">
                  <ShieldCheck className="w-8 h-8 text-sacred-gold mx-auto mb-2" />
                  <p className="text-sm text-cosmic-text-secondary">{t('auth.enterEmailToReceiveCode')}</p>
                </div>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="email" value={registerForm.email} onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })} placeholder={t('auth.email')} onKeyDown={(e) => e.key === 'Enter' && handleSendOtp()} className="pl-10 input-sacred" />
                </div>
                <Button onClick={handleSendOtp} disabled={loading || !registerForm.email} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold disabled:opacity-50">
                  {loading ? t('common.loading') : t('auth.sendVerificationCode')}<ChevronRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            )}

            {/* Step 2: Enter OTP */}
            {regStep === 'otp' && (
              <div className="space-y-3 sm:space-y-4">
                <button onClick={() => { setRegStep('email'); setError(''); setSuccess(''); }} className="flex items-center gap-1 text-sm text-cosmic-text-secondary hover:text-sacred-gold transition-colors">
                  <ArrowLeft className="w-4 h-4" /> {t('auth.changeEmail')}
                </button>
                <div className="text-center mb-2">
                  <ShieldCheck className="w-8 h-8 text-sacred-gold mx-auto mb-2" />
                  <p className="text-sm text-cosmic-text-secondary">
                    {t('auth.enterOtp')}<br />
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
                      pattern="[0-9]*"
                      {...(i === 0 ? { autoComplete: 'one-time-code' } : {})}
                      maxLength={1}
                      value={digit}
                      onChange={(e) => handleOtpChange(i, e.target.value)}
                      onKeyDown={(e) => handleOtpKeyDown(i, e)}
                      className={`w-12 h-14 text-center text-xl font-bold rounded-lg border bg-cosmic-card text-cosmic-text focus:border-sacred-gold focus:ring-1 focus:ring-sacred-gold outline-none transition-all duration-200 ${
                        otpPasted ? 'border-green-500 ring-1 ring-green-400 bg-green-50' : 'border-sacred-gold'
                      }`}
                    />
                  ))}
                </div>
                {otpPasted && (
                  <p className="text-center text-sm text-green-600 font-medium animate-fadeIn">
                    {t('auth.codePasted')}
                  </p>
                )}
                <Button onClick={handleVerifyOtp} disabled={loading || otp.join('').length !== 6} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold disabled:opacity-50">
                  {loading ? t('common.loading') : t('auth.verifyCode')}<ShieldCheck className="w-5 h-5 ml-2" />
                </Button>
                <div className="text-center">
                  {countdown > 0 ? (
                    <p className="text-sm text-cosmic-text">{t('auth.resendIn')} {countdown}s</p>
                  ) : (
                    <button onClick={handleResendOtp} className="text-sm text-sacred-gold hover:underline">{t('auth.resendCode')}</button>
                  )}
                </div>
              </div>
            )}

            {/* Step 3: Complete registration */}
            {regStep === 'details' && (
              <div className="space-y-3 sm:space-y-4">
                <div className="text-center mb-2">
                  <div className="inline-flex items-center gap-2 bg-green-50 border border-green-300 rounded-full px-4 py-1.5 text-green-700 text-sm">
                    <ShieldCheck className="w-4 h-4" /> {registerForm.email} {t('auth.emailVerified')}
                  </div>
                </div>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type="text" value={registerForm.name} onChange={(e) => setRegisterForm({ ...registerForm, name: e.target.value })} placeholder={t('auth.fullName')} className="pl-10 input-sacred" />
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                  <Input type={showRegisterPassword ? 'text' : 'password'} value={registerForm.password} onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })} placeholder={t('auth.passwordMinLength')} onKeyDown={(e) => e.key === 'Enter' && handleRegister()} className="pl-10 pr-10 input-sacred" />
                  <button type="button" onClick={() => setShowRegisterPassword(!showRegisterPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-sacred-gold hover:text-sacred-gold-dark transition-colors" tabIndex={-1}>
                    {showRegisterPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {/* Astrologer toggle */}
                <button
                  onClick={() => setIsAstrologer(!isAstrologer)}
                  className={`w-full flex items-center gap-3 p-3 border transition-colors rounded-lg ${
                    isAstrologer
                      ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold-dark'
                      : 'border-gray-300 text-gray-600 hover:border-sacred-gold'
                  }`}
                >
                  <Star className={`w-5 h-5 ${isAstrologer ? 'text-sacred-gold-dark' : 'text-gray-400'}`} />
                  <span className="text-sm font-medium">{t('astrologer.registerAsAstrologer')}</span>
                  <div className={`ml-auto w-10 h-5 rounded-full transition-colors ${isAstrologer ? 'bg-sacred-gold-dark' : 'bg-gray-300'}`}>
                    <div className={`w-4 h-4 rounded-full bg-white shadow-sm transform transition-transform mt-0.5 ${isAstrologer ? 'translate-x-5 ml-[22px]' : 'ml-0.5'}`} />
                  </div>
                </button>
                {isAstrologer && (
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold" />
                    <Input type="tel" value={registerForm.phone} onChange={(e) => setRegisterForm({ ...registerForm, phone: e.target.value })} placeholder={t('auth.phoneNumberRequired')} className="pl-10 input-sacred" />
                  </div>
                )}
                <Button onClick={handleRegister} disabled={loading || !registerForm.name || !registerForm.password || (isAstrologer && !registerForm.phone.trim())} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold disabled:opacity-50">
                  {loading ? t('common.loading') : (isAstrologer ? t('astrologer.registerAsAstrologer') : t('auth.signUp'))}<ChevronRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            )}
          </TabsContent>
        </Tabs>

        {/* Forgot Password Flow */}
        {showForgotPassword && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-cosmic-bg backdrop-blur-sm px-4" onClick={() => setShowForgotPassword(false)}>
            <div className="bg-cosmic-bg border border-sacred-gold rounded-2xl p-6 max-w-sm w-full space-y-4" onClick={e => e.stopPropagation()}>
              <h3 className="text-lg font-sans text-sacred-gold-dark text-center">{t('auth.resetPassword')}</h3>
              {error && <p className="text-red-700 text-sm text-center">{error}</p>}
              {success && <p className="text-green-700 text-sm text-center">{success}</p>}

              {resetStep === 'email' && (
                <>
                  <Input type="email" value={resetEmail} onChange={e => setResetEmail(e.target.value)} placeholder={t('auth.yourEmail')} className="input-sacred" />
                  <Button onClick={handleForgotPassword} disabled={loading || !resetEmail} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold disabled:opacity-50">
                    {loading ? t('auth.sending') : t('auth.sendResetCode')}
                  </Button>
                </>
              )}

              {resetStep === 'otp' && (
                <>
                  <p className="text-sm text-cosmic-text text-center">{t('auth.enterOtp')} {resetEmail}</p>
                  <Input type="text" value={resetOtp} onChange={e => setResetOtp(e.target.value.replace(/\D/g, '').slice(0, 6))} placeholder="000000" maxLength={6} className="input-sacred text-center text-2xl tracking-widest" />
                  <div className="relative">
                    <Input type={showResetPassword ? 'text' : 'password'} value={newPassword} onChange={e => setNewPassword(e.target.value)} placeholder={t('auth.newPassword')} className="pr-10 input-sacred" />
                    <button type="button" onClick={() => setShowResetPassword(!showResetPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-sacred-gold hover:text-sacred-gold-dark transition-colors" tabIndex={-1}>
                      {showResetPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  <Button onClick={handleResetPassword} disabled={loading || resetOtp.length !== 6 || newPassword.length < 8} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold disabled:opacity-50">
                    {loading ? t('auth.resetting') : t('auth.resetPassword')}
                  </Button>
                </>
              )}

              {resetStep === 'done' && (
                <Button onClick={() => { setShowForgotPassword(false); setError(''); setSuccess(''); }} className="w-full bg-sacred-gold text-white hover:bg-sacred-gold/90 font-semibold">
                  {t('auth.backToLogin')}
                </Button>
              )}

              <button onClick={() => setShowForgotPassword(false)} className="w-full text-center text-sm text-cosmic-text hover:text-cosmic-text">{t('auth.cancel')}</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
