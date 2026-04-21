import { useState, useRef, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Upload, Image as ImageIcon, X, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';

interface Props {
  onUploaded: (imageUrl: string, width: number, height: number) => void;
}

export default function FloorplanUploader({ onUploaded }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFile = useCallback(async (file: File) => {
    setError('');
    if (!file.type.match(/^image\/(png|jpe?g|webp)$/)) {
      setError(t('auto.onlyPNGJPGOrWebPFile'));
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError(t('auto.fileExceeds5MBLimit'));
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
      setError(err instanceof Error ? err.message : t('auto.uploadFailed'));
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
        className={`border-2 border-dashed rounded-xl p-4 sm:p-8 text-center cursor-pointer transition-all min-h-[120px] flex items-center justify-center ${
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
            <p className="text-sm text-foreground">{t('auto.uploading')}</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-sacred-gold/10 flex items-center justify-center">
              <Upload className="w-6 h-6 text-sacred-gold" />
            </div>
            <div>
              <p className="text-sm sm:text-base font-semibold text-foreground">
                {t('auto.uploadFloorPlan')}
              </p>
              <p className="text-xs sm:text-sm text-foreground/50 mt-1">
                {t('auto.pNGJPGOrWebPDragDrop')}
              </p>
            </div>
            <div className="flex items-center gap-2 text-xs sm:text-sm text-foreground/40">
              <ImageIcon className="w-3 h-3" />
              {t('auto.phonePhotosWorkToo')}
            </div>
          </div>
        )}
      </div>
      {error && (
        <div className="flex items-center gap-2 px-3 py-2 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm">
          <X className="w-3 h-3 flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  );
}
