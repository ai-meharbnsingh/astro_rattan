import { useState, useRef, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Upload, Image as ImageIcon, X, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';

interface Props {
  onUploaded: (imageUrl: string, width: number, height: number) => void;
}

export default function FloorplanUploader({ onUploaded }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFile = useCallback(async (file: File) => {
    setError('');
    if (!file.type.match(/^image\/(png|jpe?g|webp)$/)) {
      setError(isHi ? 'केवल PNG, JPG, या WebP फ़ाइल अपलोड करें' : 'Only PNG, JPG, or WebP files allowed');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError(isHi ? 'फ़ाइल 5MB से बड़ी है' : 'File exceeds 5MB limit');
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const result = await api.postForm('/api/vastu/upload-floorplan', formData);

      // Get image dimensions
      const img = new window.Image();
      img.onload = () => {
        onUploaded(result.image_url, img.naturalWidth, img.naturalHeight);
      };
      img.onerror = () => {
        onUploaded(result.image_url, 800, 600); // fallback
      };
      img.src = result.image_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  }, [isHi, onUploaded]);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const onSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  return (
    <div className="space-y-3">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
          dragging
            ? 'border-sacred-gold bg-sacred-gold/10'
            : 'border-white/15 bg-white/5 hover:border-sacred-gold/40'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          onChange={onSelect}
          className="hidden"
        />
        {uploading ? (
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="w-8 h-8 text-sacred-gold animate-spin" />
            <p className="text-sm text-cosmic-text">{isHi ? 'अपलोड हो रहा है...' : 'Uploading...'}</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-sacred-gold/10 flex items-center justify-center">
              <Upload className="w-6 h-6 text-sacred-gold" />
            </div>
            <div>
              <p className="text-sm font-semibold text-cosmic-text">
                {isHi ? 'फ्लोर प्लान अपलोड करें' : 'Upload Floor Plan'}
              </p>
              <p className="text-xs text-cosmic-text/50 mt-1">
                {isHi
                  ? 'PNG, JPG, या WebP — खींचकर छोड़ें या क्लिक करें — अधिकतम 5MB'
                  : 'PNG, JPG, or WebP — drag & drop or click — max 5MB'}
              </p>
            </div>
            <div className="flex items-center gap-2 text-[10px] text-cosmic-text/40">
              <ImageIcon className="w-3 h-3" />
              {isHi ? 'फ़ोन से ली गई फोटो भी चलेगी' : 'Phone photos work too'}
            </div>
          </div>
        )}
      </div>
      {error && (
        <div className="flex items-center gap-2 px-3 py-2 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-xs">
          <X className="w-3 h-3 flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  );
}
