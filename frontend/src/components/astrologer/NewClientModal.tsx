/**
 * NewClientModal — Sprint I.
 *
 * Single-submit flow: the astrologer fills one form, and the backend
 * creates the client row + generates Vedic + Lal Kitab + Numerology
 * kundlis in one transaction (POST /api/clients/generate-all).
 *
 * Photos (profile / left hand / right hand) are encoded as data URLs
 * client-side. 2MB limit per image enforced.
 */
import { useState, useRef, useEffect } from 'react';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  X, Camera, Loader2, Check, User as UserIcon, Phone, Calendar, MapPin,
  Hand, Sparkles, BookOpen, Hash, CheckCircle2,
} from 'lucide-react';

interface Props {
  isHi: boolean;
  onClose: () => void;
  onCreated: (clientId: string) => void;
}

interface Form {
  name: string;
  phone: string;
  birth_date: string;
  birth_time: string;
  birth_place: string;
  latitude: string;
  longitude: string;
  timezone_offset: string;
  gender: string;
  notes: string;
  profile_photo_url: string;
  left_hand_photo_url: string;
  right_hand_photo_url: string;
  generate_vedic: boolean;
  generate_lalkitab: boolean;
  generate_numerology: boolean;
}

const EMPTY: Form = {
  name: '', phone: '', birth_date: '', birth_time: '',
  birth_place: '', latitude: '', longitude: '', timezone_offset: '5.5',
  gender: 'male', notes: '',
  profile_photo_url: '', left_hand_photo_url: '', right_hand_photo_url: '',
  generate_vedic: true, generate_lalkitab: true, generate_numerology: true,
};

export default function NewClientModal({ isHi, onClose, onCreated }: Props) {
  const [form, setForm] = useState<Form>(EMPTY);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<string | null>(null);

  // Escape to close, body scroll lock
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape' && !submitting) onClose(); };
    document.addEventListener('keydown', onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [onClose, submitting]);

  const update = <K extends keyof Form>(key: K, val: Form[K]) => setForm((f) => ({ ...f, [key]: val }));

  const submit = async () => {
    setError(null);
    // Minimal validation — backend does the rest.
    if (!form.name.trim()) return setError(isHi ? 'नाम आवश्यक' : 'Name is required');
    if (!form.birth_date) return setError(isHi ? 'जन्म तिथि आवश्यक' : 'Birth date is required');
    if (!form.birth_time) return setError(isHi ? 'जन्म समय आवश्यक' : 'Birth time is required');
    if (!form.birth_place.trim()) return setError(isHi ? 'जन्म स्थान आवश्यक' : 'Birth place is required');
    if (!form.latitude || !form.longitude) {
      return setError(isHi ? 'अक्षांश/देशांतर आवश्यक (जन्म स्थान से स्वचालित भरें)' : 'Latitude/longitude required');
    }

    setSubmitting(true);
    setProgress(isHi ? 'ग्राहक बना रहे हैं…' : 'Creating client…');
    try {
      const payload = {
        name: form.name.trim(),
        phone: form.phone || null,
        birth_date: form.birth_date,
        birth_time: form.birth_time,
        birth_place: form.birth_place.trim(),
        latitude: parseFloat(form.latitude),
        longitude: parseFloat(form.longitude),
        timezone_offset: parseFloat(form.timezone_offset) || 5.5,
        gender: form.gender || 'male',
        notes: form.notes || null,
        profile_photo_url: form.profile_photo_url || null,
        left_hand_photo_url: form.left_hand_photo_url || null,
        right_hand_photo_url: form.right_hand_photo_url || null,
        generate_vedic: form.generate_vedic,
        generate_lalkitab: form.generate_lalkitab,
        generate_numerology: form.generate_numerology,
      };
      setProgress(isHi ? 'कुंडली तैयार कर रहे हैं…' : 'Generating charts…');
      const res: any = await api.post('/api/clients/generate-all', payload);
      if (res?.client?.id) {
        onCreated(res.client.id);
      } else {
        throw new Error('No client ID returned');
      }
    } catch (e: any) {
      setError(e?.message || (isHi ? 'सहेजने में विफल' : 'Failed to save'));
    }
    setSubmitting(false);
    setProgress(null);
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-start justify-center p-4 bg-black/60 backdrop-blur-sm overflow-y-auto"
      onClick={(e) => { if (e.target === e.currentTarget && !submitting) onClose(); }}
    >
      <div className="relative w-full max-w-3xl my-8 rounded-2xl bg-white border border-sacred-gold/30 shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-sacred-gold/20 p-5 rounded-t-2xl flex items-start justify-between gap-3 z-10">
          <div>
            <h2 className="text-xl font-semibold text-sacred-gold-dark flex items-center gap-2">
              <Sparkles className="w-5 h-5" />
              {isHi ? 'नया ग्राहक' : 'New Client'}
            </h2>
            <p className="text-xs text-muted-foreground mt-0.5">
              {isHi
                ? 'सबमिट करने पर सभी 3 कुंडलियाँ (वैदिक · लाल किताब · अंक) स्वतः बनेंगी।'
                : 'On submit, all 3 charts (Vedic · Lal Kitab · Numerology) are auto-generated.'}
            </p>
          </div>
          <button
            onClick={onClose}
            disabled={submitting}
            className="p-1.5 rounded-lg hover:bg-gray-100 disabled:opacity-50"
            aria-label={isHi ? 'बंद करें' : 'Close'}
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Body */}
        <div className="p-5 space-y-5">
          {/* Basic info */}
          <section>
            <h3 className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider mb-3">
              {isHi ? 'मूल जानकारी' : 'Basic Info'}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <Field label={isHi ? 'पूरा नाम *' : 'Full Name *'} icon={UserIcon}>
                <Input value={form.name} onChange={(e) => update('name', e.target.value)} className="border-sacred-gold/30" />
              </Field>
              <Field label={isHi ? 'फ़ोन' : 'Phone'} icon={Phone}>
                <Input value={form.phone} onChange={(e) => update('phone', e.target.value)} className="border-sacred-gold/30" />
              </Field>
              <Field label={isHi ? 'जन्म तिथि *' : 'Birth Date *'} icon={Calendar}>
                <Input type="date" value={form.birth_date} onChange={(e) => update('birth_date', e.target.value)} className="border-sacred-gold/30" />
              </Field>
              <Field label={isHi ? 'जन्म समय *' : 'Birth Time *'} icon={Calendar}>
                <Input type="time" step="1" value={form.birth_time} onChange={(e) => update('birth_time', e.target.value)} className="border-sacred-gold/30" />
              </Field>
              <Field label={isHi ? 'जन्म स्थान *' : 'Birth Place *'} icon={MapPin} span={2}>
                <Input
                  value={form.birth_place}
                  onChange={(e) => update('birth_place', e.target.value)}
                  placeholder={isHi ? 'उदा., नई दिल्ली, भारत' : 'e.g. New Delhi, India'}
                  className="border-sacred-gold/30"
                />
              </Field>
              <Field label={isHi ? 'अक्षांश *' : 'Latitude *'}>
                <Input type="number" step="0.0001" value={form.latitude} onChange={(e) => update('latitude', e.target.value)} className="border-sacred-gold/30" placeholder="28.6139" />
              </Field>
              <Field label={isHi ? 'देशांतर *' : 'Longitude *'}>
                <Input type="number" step="0.0001" value={form.longitude} onChange={(e) => update('longitude', e.target.value)} className="border-sacred-gold/30" placeholder="77.2090" />
              </Field>
              <Field label={isHi ? 'समय क्षेत्र' : 'Timezone'}>
                <Input type="number" step="0.25" value={form.timezone_offset} onChange={(e) => update('timezone_offset', e.target.value)} className="border-sacred-gold/30" />
              </Field>
              <Field label={isHi ? 'लिंग' : 'Gender'}>
                <select
                  value={form.gender}
                  onChange={(e) => update('gender', e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm"
                >
                  <option value="male">{isHi ? 'पुरुष' : 'Male'}</option>
                  <option value="female">{isHi ? 'महिला' : 'Female'}</option>
                  <option value="other">{isHi ? 'अन्य' : 'Other'}</option>
                </select>
              </Field>
            </div>
          </section>

          {/* Photos */}
          <section>
            <h3 className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider mb-3">
              {isHi ? 'चित्र (वैकल्पिक)' : 'Photos (optional)'}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <PhotoSlot
                label={isHi ? 'प्रोफ़ाइल फ़ोटो' : 'Profile Photo'}
                icon={UserIcon}
                value={form.profile_photo_url}
                onChange={(v) => update('profile_photo_url', v)}
                isHi={isHi}
              />
              <PhotoSlot
                label={isHi ? 'बायाँ हाथ' : 'Left Hand'}
                icon={Hand}
                value={form.left_hand_photo_url}
                onChange={(v) => update('left_hand_photo_url', v)}
                isHi={isHi}
              />
              <PhotoSlot
                label={isHi ? 'दायाँ हाथ' : 'Right Hand'}
                icon={Hand}
                value={form.right_hand_photo_url}
                onChange={(v) => update('right_hand_photo_url', v)}
                isHi={isHi}
              />
            </div>
            <p className="text-[11px] text-muted-foreground mt-2">
              {isHi
                ? 'हाथ की तस्वीरें हस्तरेखा विश्लेषण हेतु (2MB तक, JPG/PNG)।'
                : 'Hand photos are used for palmistry (up to 2MB, JPG/PNG).'}
            </p>
          </section>

          {/* Auto-generate toggles */}
          <section>
            <h3 className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider mb-3">
              {isHi ? 'स्वचालित कुंडली निर्माण' : 'Auto-Generate Charts'}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              <ToggleCard
                checked={form.generate_vedic}
                onChange={(v) => update('generate_vedic', v)}
                icon={Sparkles}
                title={isHi ? 'वैदिक कुंडली' : 'Vedic Kundli'}
              />
              <ToggleCard
                checked={form.generate_lalkitab}
                onChange={(v) => update('generate_lalkitab', v)}
                icon={BookOpen}
                title={isHi ? 'लाल किताब' : 'Lal Kitab'}
              />
              <ToggleCard
                checked={form.generate_numerology}
                onChange={(v) => update('generate_numerology', v)}
                icon={Hash}
                title={isHi ? 'अंक ज्योतिष' : 'Numerology'}
              />
            </div>
          </section>

          {/* Notes */}
          <section>
            <h3 className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider mb-2">
              {isHi ? 'नोट्स (वैकल्पिक)' : 'Notes (optional)'}
            </h3>
            <textarea
              value={form.notes}
              onChange={(e) => update('notes', e.target.value)}
              rows={2}
              className="w-full px-3 py-2 rounded-lg border border-sacred-gold/30 bg-white text-sm resize-none"
              placeholder={isHi ? 'संदर्भ, मुख्य चिंता, प्राथमिकताएँ…' : 'Context, primary concern, preferences…'}
            />
          </section>

          {error && (
            <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-800">
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-white border-t border-sacred-gold/20 p-4 rounded-b-2xl flex items-center justify-between gap-3">
          <div className="text-xs text-muted-foreground">
            {progress && <span className="inline-flex items-center gap-1.5"><Loader2 className="w-3 h-3 animate-spin" />{progress}</span>}
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={onClose} disabled={submitting} className="border-sacred-gold/30">
              {isHi ? 'रद्द करें' : 'Cancel'}
            </Button>
            <Button
              onClick={submit}
              disabled={submitting}
              className="bg-sacred-gold-dark text-white hover:bg-sacred-gold min-w-[180px]"
            >
              {submitting ? <Loader2 className="w-4 h-4 animate-spin mr-1.5" /> : <CheckCircle2 className="w-4 h-4 mr-1.5" />}
              {isHi ? 'बनाएं और कुंडली तैयार करें' : 'Create & Generate'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Field({ label, icon: Icon, span, children }: { label: string; icon?: any; span?: number; children: React.ReactNode }) {
  return (
    <div className={span === 2 ? 'sm:col-span-2' : ''}>
      <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wide block mb-1 flex items-center gap-1.5">
        {Icon && <Icon className="w-3 h-3" />}
        {label}
      </label>
      {children}
    </div>
  );
}

function ToggleCard({ checked, onChange, icon: Icon, title }: {
  checked: boolean; onChange: (v: boolean) => void; icon: any; title: string;
}) {
  return (
    <button
      onClick={() => onChange(!checked)}
      className={`flex items-center gap-2 p-3 rounded-lg border-2 transition-all text-left ${
        checked
          ? 'border-sacred-gold bg-sacred-gold/10'
          : 'border-gray-200 bg-white hover:border-sacred-gold/40'
      }`}
    >
      <Icon className={`w-4 h-4 ${checked ? 'text-sacred-gold-dark' : 'text-muted-foreground'}`} />
      <span className={`text-sm font-semibold flex-1 ${checked ? 'text-sacred-gold-dark' : 'text-foreground'}`}>
        {title}
      </span>
      {checked && <Check className="w-4 h-4 text-sacred-gold-dark" />}
    </button>
  );
}

function PhotoSlot({ label, icon: Icon, value, onChange, isHi }: {
  label: string; icon: any; value: string; onChange: (v: string) => void; isHi: boolean;
}) {
  const ref = useRef<HTMLInputElement>(null);
  const pick = (file: File | null) => {
    if (!file) return;
    if (file.size > 2 * 1024 * 1024) {
      alert(isHi ? 'फाइल 2MB से छोटी होनी चाहिए' : 'File must be under 2MB');
      return;
    }
    const reader = new FileReader();
    reader.onload = () => onChange(String(reader.result ?? ''));
    reader.readAsDataURL(file);
  };
  return (
    <div className="border-2 border-dashed border-sacred-gold/30 rounded-lg p-3 flex flex-col items-center gap-2">
      <input ref={ref} type="file" accept="image/*" className="hidden"
        onChange={(e) => pick(e.target.files?.[0] ?? null)} />
      {value ? (
        <div className="relative">
          <img src={value} alt="" className="w-20 h-20 object-cover rounded-lg border border-sacred-gold/40" />
          <button
            onClick={() => onChange('')}
            className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-red-500 text-white flex items-center justify-center text-xs"
            aria-label="Remove"
          >
            ×
          </button>
        </div>
      ) : (
        <div className="w-20 h-20 rounded-lg bg-sacred-gold/10 flex items-center justify-center">
          <Icon className="w-8 h-8 text-sacred-gold/50" />
        </div>
      )}
      <div className="text-center">
        <p className="text-xs font-semibold text-foreground flex items-center gap-1 justify-center">
          <Icon className="w-3 h-3" /> {label}
        </p>
        <button onClick={() => ref.current?.click()} className="text-[11px] text-sacred-gold-dark hover:underline mt-0.5 inline-flex items-center gap-1">
          <Camera className="w-3 h-3" />
          {value ? (isHi ? 'बदलें' : 'Change') : (isHi ? 'अपलोड' : 'Upload')}
        </button>
      </div>
    </div>
  );
}
