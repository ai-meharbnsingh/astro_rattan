import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/lib/api';
import { Save, Loader2, KeyRound, User, Phone, Calendar, MapPin, Check } from 'lucide-react';

export default function ProfileEditPanel() {
  const { t, language } = useTranslation();
  const { user, refreshUser } = useAuth();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [dob, setDob] = useState('');
  const [gender, setGender] = useState('');
  const [city, setCity] = useState('');

  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  // Password change
  const [showPwForm, setShowPwForm] = useState(false);
  const [currentPw, setCurrentPw] = useState('');
  const [newPw, setNewPw] = useState('');
  const [pwSaving, setPwSaving] = useState(false);
  const [pwMsg, setPwMsg] = useState('');

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setPhone(user.phone || '');
      setDob(user.date_of_birth || '');
      setGender(user.gender || '');
      setCity(user.city || '');
    }
  }, [user]);

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSaved(false);
    try {
      await api.patch('/api/auth/profile', { name, phone, date_of_birth: dob, gender, city });
      setSaved(true);
      if (refreshUser) refreshUser();
      setTimeout(() => setSaved(false), 3000);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : l('Failed to save', 'सहेजने में विफल'));
    }
    setSaving(false);
  };

  const handlePasswordChange = async () => {
    if (newPw.length < 6) { setPwMsg(l('Min 6 characters', 'न्यूनतम 6 अक्षर')); return; }
    setPwSaving(true);
    setPwMsg('');
    try {
      await api.post('/api/auth/change-password', { current_password: currentPw, new_password: newPw });
      setPwMsg(l('Password updated!', 'पासवर्ड अपडेट हो गया!'));
      setCurrentPw('');
      setNewPw('');
      setShowPwForm(false);
    } catch (e: unknown) {
      setPwMsg(e instanceof Error ? e.message : l('Failed', 'विफल'));
    }
    setPwSaving(false);
  };

  const inputClass = 'w-full px-3 py-2 rounded-lg bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none';

  return (
    <div className="border border-sacred-gold rounded-xl p-5 bg-cosmic-bg">
      <h3 className="text-sm font-semibold uppercase tracking-wider text-sacred-gold-dark mb-4 flex items-center gap-2">
        <User className="w-4 h-4" />
        {l('My Profile', 'मेरी प्रोफ़ाइल')}
      </h3>

      <div className="space-y-3">
        <div>
          <label className="text-xs text-cosmic-text-secondary mb-1 block">{l('Name', 'नाम')}</label>
          <input type="text" value={name} onChange={e => setName(e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="text-xs text-cosmic-text-secondary mb-1 flex items-center gap-1"><Phone className="w-3 h-3" />{l('Phone', 'फ़ोन')}</label>
          <input type="tel" value={phone} onChange={e => setPhone(e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="text-xs text-cosmic-text-secondary mb-1 flex items-center gap-1"><Calendar className="w-3 h-3" />{l('Date of Birth', 'जन्म तिथि')}</label>
          <input type="date" value={dob} onChange={e => setDob(e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="text-xs text-cosmic-text-secondary mb-1 block">{l('Gender', 'लिंग')}</label>
          <select value={gender} onChange={e => setGender(e.target.value)} className={inputClass}>
            <option value="">{l('Select', 'चुनें')}</option>
            <option value="male">{l('Male', 'पुरुष')}</option>
            <option value="female">{l('Female', 'महिला')}</option>
            <option value="other">{l('Other', 'अन्य')}</option>
          </select>
        </div>
        <div>
          <label className="text-xs text-cosmic-text-secondary mb-1 flex items-center gap-1"><MapPin className="w-3 h-3" />{l('City', 'शहर')}</label>
          <input type="text" value={city} onChange={e => setCity(e.target.value)} className={inputClass} />
        </div>

        {error && <p className="text-xs text-red-600">{error}</p>}

        <button onClick={handleSave} disabled={saving}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-sacred-gold-dark text-white rounded-lg font-medium text-sm hover:bg-sacred-gold transition-all disabled:opacity-50">
          {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : saved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
          {saving ? l('Saving...', 'सहेज रहे...') : saved ? l('Saved!', 'सहेजा गया!') : l('Save Profile', 'प्रोफ़ाइल सहेजें')}
        </button>
      </div>

      {/* Password Change */}
      <div className="mt-4 pt-4 border-t border-cosmic-border">
        {!showPwForm ? (
          <button onClick={() => setShowPwForm(true)}
            className="flex items-center gap-2 text-sm text-sacred-gold-dark hover:underline">
            <KeyRound className="w-3.5 h-3.5" />
            {l('Change Password', 'पासवर्ड बदलें')}
          </button>
        ) : (
          <div className="space-y-2">
            <input type="password" placeholder={l('Current password', 'वर्तमान पासवर्ड')}
              value={currentPw} onChange={e => setCurrentPw(e.target.value)} className={inputClass} />
            <input type="password" placeholder={l('New password (min 6)', 'नया पासवर्ड (न्यूनतम 6)')}
              value={newPw} onChange={e => setNewPw(e.target.value)} className={inputClass} />
            {pwMsg && <p className="text-xs text-sacred-gold-dark">{pwMsg}</p>}
            <div className="flex gap-2">
              <button onClick={handlePasswordChange} disabled={pwSaving}
                className="flex-1 px-3 py-2 bg-sacred-gold-dark text-white rounded-lg text-sm font-medium disabled:opacity-50">
                {pwSaving ? l('Updating...', 'अपडेट हो रहा...') : l('Update Password', 'पासवर्ड अपडेट करें')}
              </button>
              <button onClick={() => { setShowPwForm(false); setPwMsg(''); }}
                className="px-3 py-2 border border-cosmic-border text-cosmic-text rounded-lg text-sm">
                {l('Cancel', 'रद्द')}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Account info */}
      <div className="mt-4 pt-3 border-t border-cosmic-border text-xs text-cosmic-text-secondary space-y-1">
        <p>{l('Email', 'ईमेल')}: {user?.email}</p>
        <p>{l('Role', 'भूमिका')}: {user?.role}</p>
      </div>
    </div>
  );
}
