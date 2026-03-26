import { useMemo, useState } from 'react';
import { ExternalLink, Copy, Video, X } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface VideoSessionPanelProps {
  title: string;
  subtitle: string;
  videoLink: string;
  roomName: string;
  onClose?: () => void;
}

export default function VideoSessionPanel({
  title,
  subtitle,
  videoLink,
  roomName,
  onClose,
}: VideoSessionPanelProps) {
  const [copied, setCopied] = useState(false);

  const embedLink = useMemo(() => {
    if (videoLink.includes('#')) return videoLink;
    return `${videoLink}#config.prejoinPageEnabled=false`;
  }, [videoLink]);

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(videoLink);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  };

  return (
    <Card className="bg-white border border-minimal-indigo/10 shadow-soft">
      <CardContent className="p-4 sm:p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-minimal-indigo/10 px-3 py-1 text-xs font-medium text-minimal-indigo">
              <Video className="h-3.5 w-3.5" />
              Live Video Session
            </div>
            <h3 className="mt-3 text-xl font-display font-semibold text-minimal-gray-900">{title}</h3>
            <p className="mt-1 text-sm text-minimal-gray-500">{subtitle}</p>
            <p className="mt-2 text-xs text-minimal-gray-400">Room: {roomName}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button
              type="button"
              variant="outline"
              className="border-minimal-gray-200"
              onClick={copyLink}
            >
              <Copy className="mr-2 h-4 w-4" />
              {copied ? 'Copied' : 'Copy Link'}
            </Button>
            <Button
              type="button"
              variant="outline"
              className="border-minimal-gray-200"
              onClick={() => window.open(videoLink, '_blank', 'noopener,noreferrer')}
            >
              <ExternalLink className="mr-2 h-4 w-4" />
              Open Tab
            </Button>
            {onClose && (
              <Button type="button" variant="ghost" onClick={onClose}>
                <X className="mr-2 h-4 w-4" />
                Close
              </Button>
            )}
          </div>
        </div>

        <div className="mt-4 overflow-hidden rounded-2xl border border-minimal-gray-200 bg-minimal-gray-50">
          <iframe
            title={title}
            src={embedLink}
            className="aspect-video w-full"
            allow="camera; microphone; display-capture; fullscreen; clipboard-read; clipboard-write"
            referrerPolicy="strict-origin-when-cross-origin"
          />
        </div>
      </CardContent>
    </Card>
  );
}
