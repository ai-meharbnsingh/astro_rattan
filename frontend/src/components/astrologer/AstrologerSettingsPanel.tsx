/**
 * AstrologerSettingsPanel — Sprint I.
 *
 * Settings tab inside the Professional Dashboard. Lets the astrologer:
 *   - Upload / change profile photo (avatar_url on users)
 *   - Edit name / phone / city / DOB / gender
 *   - Change password
 *
 * Styling matches the sacred-gold palette used across the LK surfaces.
 */
import { useState, useRef } from 'react';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Camera, Save, Check, Loader2, Lock, User as UserIcon, Phone, MapPin, Calendar, Eye, EyeOff } from 'lucide-react';

interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: string;
  phone: string | null;
  avatar_url: string | null;
}

interface Props {
  isHi: boolean;
  user: AuthUser | null | undefined;
}

export default function AstrologerSettingsPanel({ isHi, user }: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  // ── Profile form ──
  const [profile, setProfile] = useState({
    name: user?.name ?? '',
    phone: user?.phone ?? '',
    avatar_url: user?.avatar_url ?? '',
    city: '',
    date_of_birth: '',
    gender: '',
  });
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileSaved, setProfileSaved] = useState(false);
  const [uploading, setUploading] = useState(false);

  // ── Password form ──
  const [pw, setPw] = useState({ current: '', next: '', confirm: '' });
  const [pwSaving, setPwSaving] = useState(false);
  const [pwMessage, setPwMessage] = useState<{ kind: 'ok' | 'err'; text: string } | null>(null);
  const [showPw, setShowPw] = useState(false);

  const onFilePick = (file: File | null) => {
    if (!file) return;
    if (file.size > 2 * 1024 * 1024) {
      alert(isHi ? 'फाइल 2MB से छोटी होनी चाहिए' : 'File must be under 2MB');
      return;
    }
    setUploading(true);
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = String(reader.result ?? '');
      setProfile((p) => ({ ...p, avatar_url: dataUrl }));
      setUploading(false);
    };
    reader.onerror = () => setUploading(false);
    reader.readAsDataURL(file);
  };

  const saveProfile = async () => {
    setProfileSaving(true);
    setProfileSaved(false);
    try {
      const body: Record<string, any> = {};
      if (profile.name) body.name = profile.name;
      if (profile.phone) body.phone = profile.phone;
      if (profile.avatar_url !== null) body.avatar_url = profile.avatar_url;
      if (profile.city) body.city = profile.city;
      if (profile.date_of_birth) body.date_of_birth = profile.date_of_birth;
      if (profile.gender) body.gender = profile.gender;
      await api.patch('/api/auth/profile', body);
      setProfileSaved(true);
      setTimeout(() => setProfileSaved(false), 2000);
    } catch (e) {
      console.error(e);
    }
    setProfileSaving(false);
  };

  const savePassword = async () => {
    setPwMessage(null);
    if (!pw.current || !pw.next) {
      setPwMessage({ kind: 'err', text: isHi ? 'सभी फ़ील्ड भरें' : 'Fill all fields' });
      return;
    }
    if (pw.next !== pw.confirm) {
      setPwMessage({ kind: 'err', text: isHi ? 'नए पासवर्ड मेल नहीं खाते' : 'New passwords do not match' });
      return;
    }
    if (pw.next.length < 8) {
      setPwMessage({ kind: 'err', text: isHi ? 'पासवर्ड कम से कम 8 अक्षर' : 'Password must be at least 8 characters' });
      return;
    }
    setPwSaving(true);
    try {
      await api.post('/api/auth/change-password', {
        current_password: pw.current,
        new_password: pw.next,
      });
      setPwMessage({ kind: 'ok', text: isHi ? 'पासवर्ड बदल दिया गया' : 'Password updated' });
      setPw({ current: '', next: '', confirm: '' });
    } catch (e: any) {
      setPwMessage({ kind: 'err', text: e?.message || (isHi ? 'विफल' : 'Failed') });
    }
    setPwSaving(false);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* ── Profile card ── */}
      <div className="rounded-xl border border-sacred-gold/20 bg-card p-6">
        <h3 className="text-lg font-semibold text-sacred-gold-dark flex items-center gap-2 mb-4">
          <UserIcon className="w-5 h-5" />
          {isHi ? 'प्रोफ़ाइल' : 'Profile'}
        </h3>

        {/* Avatar */}
        <div className="flex items-center gap-4 mb-6">
          <div className="relative">
            {profile.avatar_url ? (
              <img
                src={profile.avatar_url}
                alt=""
                className="w-20 h-20 rounded-full object-cover border-2 border-sacred-gold/40"
              />
            ) : (
              <div className="w-20 h-20 rounded-full bg-sacred-gold-dark text-white flex items-center justify-center text-2xl font-bold border-2 border-sacred-gold/40">
                {(profile.name || user?.email || '?').slice(0, 1).toUpperCase()}
              </div>
            )}
            {uploading && (
              <div className="absolute inset-0 rounded-full bg-black/40 flex items-center justify-center">
                <Loader2 className="w-5 h-5 animate-spin text-white" />
              </div>
            )}
          </div>
          <div className="flex-1">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => onFilePick(e.target.files?.[0] ?? null)}
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-sacred-gold/30 hover:bg-sacred-gold/10 text-sm font-semibold text-sacred-gold-dark disabled:opacity-50"
            >
              <Camera className="w-3.5 h-3.5" />
              {profile.avatar_url
                ? (isHi ? 'फ़ोटो बदलें' : 'Change photo')
                : (isHi ? 'फ़ोटो अपलोड करें' : 'Upload photo')}
            </button>
            {profile.avatar_url && (
              <button
                onClick={() => setProfile((p) => ({ ...p, avatar_url: '' }))}
                className="ml-2 text-xs text-red-600 hover:underline"
              >
                {isHi ? 'हटाएं' : 'Remove'}
              </button>
            )}
            <p className="text-[11px] text-muted-foreground mt-1">
              {isHi ? 'JPG / PNG · 2MB तक' : 'JPG / PNG · up to 2MB'}
            </p>
          </div>
        </div>

        {/* Fields */}
        <div className="space-y-3">
          <Field label={isHi ? 'पूरा नाम' : 'Full Name'} icon={UserIcon}>
            <Input
              value={profile.name}
              onChange={(e) => setProfile((p) => ({ ...p, name: e.target.value }))}
              className="border-sacred-gold/30"
            />
          </Field>
          <div className="text-sm text-muted-foreground pl-1">
            <span className="font-semibold">Email:</span> {user?.email || '—'} <span className="text-xs">({isHi ? 'पढ़ने योग्य' : 'read-only'})</span>
          </div>
          <Field label={isHi ? 'फ़ोन' : 'Phone'} icon={Phone}>
            <Input
              value={profile.phone}
              onChange={(e) => setProfile((p) => ({ ...p, phone: e.target.value }))}
              className="border-sacred-gold/30"
            />
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label={isHi ? 'शहर' : 'City'} icon={MapPin}>
              <Input
                value={profile.city}
                onChange={(e) => setProfile((p) => ({ ...p, city: e.target.value }))}
                className="border-sacred-gold/30"
                placeholder={isHi ? 'वैकल्पिक' : 'Optional'}
              />
            </Field>
            <Field label={isHi ? 'जन्म तिथि' : 'Date of birth'} icon={Calendar}>
              <Input
                type="date"
                value={profile.date_of_birth}
                onChange={(e) => setProfile((p) => ({ ...p, date_of_birth: e.target.value }))}
                className="border-sacred-gold/30"
              />
            </Field>
          </div>
          <Field label={isHi ? 'लिंग' : 'Gender'} icon={UserIcon}>
            <select
              value={profile.gender}
              onChange={(e) => setProfile((p) => ({ ...p, gender: e.target.value }))}
              className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
            >
              <option value="">{isHi ? 'चुनें' : 'Select'}</option>
              <option value="male">{isHi ? 'पुरुष' : 'Male'}</option>
              <option value="female">{isHi ? 'महिला' : 'Female'}</option>
              <option value="other">{isHi ? 'अन्य' : 'Other'}</option>
            </select>
          </Field>
        </div>

        <Button
          onClick={saveProfile}
          disabled={profileSaving}
          className="w-full mt-4 bg-sacred-gold-dark text-white hover:bg-sacred-gold disabled:opacity-50"
        >
          {profileSaving ? <Loader2 className="w-4 h-4 animate-spin mr-1.5" /> :
           profileSaved ? <Check className="w-4 h-4 mr-1.5" /> : <Save className="w-4 h-4 mr-1.5" />}
          {profileSaving ? (isHi ? 'सहेज रहे हैं…' : 'Saving…')
            : profileSaved ? (isHi ? 'सहेजा गया' : 'Saved')
            : (isHi ? 'प्रोफ़ाइल सहेजें' : 'Save Profile')}
        </Button>
      </div>

      {/* ── Password card ── */}
      <div className="rounded-xl border border-sacred-gold/20 bg-card p-6">
        <h3 className="text-lg font-semibold text-sacred-gold-dark flex items-center gap-2 mb-4">
          <Lock className="w-5 h-5" />
          {isHi ? 'पासवर्ड बदलें' : 'Change Password'}
        </h3>

        <div className="space-y-3">
          <Field label={isHi ? 'वर्तमान पासवर्ड' : 'Current Password'}>
            <div className="relative">
              <Input
                type={showPw ? 'text' : 'password'}
                value={pw.current}
                onChange={(e) => setPw((p) => ({ ...p, current: e.target.value }))}
                className="border-sacred-gold/30 pr-10"
                autoComplete="current-password"
              />
              <button
                type="button"
                onClick={() => setShowPw((v) => !v)}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </Field>
          <Field label={isHi ? 'नया पासवर्ड' : 'New Password'}>
            <Input
              type={showPw ? 'text' : 'password'}
              value={pw.next}
              onChange={(e) => setPw((p) => ({ ...p, next: e.target.value }))}
              className="border-sacred-gold/30"
              autoComplete="new-password"
              placeholder={isHi ? 'कम से कम 8 अक्षर' : 'At least 8 characters'}
            />
          </Field>
          <Field label={isHi ? 'नया पासवर्ड पुष्टि' : 'Confirm New Password'}>
            <Input
              type={showPw ? 'text' : 'password'}
              value={pw.confirm}
              onChange={(e) => setPw((p) => ({ ...p, confirm: e.target.value }))}
              className="border-sacred-gold/30"
              autoComplete="new-password"
            />
          </Field>
        </div>

        {pwMessage && (
          <div className={`mt-3 p-2 rounded-lg text-sm ${
            pwMessage.kind === 'ok' ? 'bg-green-50 text-green-800 border border-green-200'
                                     : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            {pwMessage.text}
          </div>
        )}

        <Button
          onClick={savePassword}
          disabled={pwSaving}
          className="w-full mt-4 bg-sacred-gold-dark text-white hover:bg-sacred-gold disabled:opacity-50"
        >
          {pwSaving ? <Loader2 className="w-4 h-4 animate-spin mr-1.5" /> : <Lock className="w-4 h-4 mr-1.5" />}
          {isHi ? 'पासवर्ड अपडेट करें' : 'Update Password'}
        </Button>
      </div>
    </div>
  );
}

function Field({ label, icon: Icon, children }: { label: string; icon?: any; children: React.ReactNode }) {
  return (
    <div>
      <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wide block mb-1 flex items-center gap-1.5">
        {Icon && <Icon className="w-3 h-3" />}
        {label}
      </label>
      {children}
    </div>
  );
}
