/**
 * TodaysSkyWidget — live concentric / diamond transit chart for the homepage.
 * Fetches today's planetary positions from GET /api/kundli/current-sky (no auth).
 */
import { useEffect, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import ConcentricChart from '@/components/kundli/ConcentricChart';

interface SkyPlanet {
  planet: string;
  sign: string;
  longitude: number;
  sign_degree: number;
  is_retrograde: boolean;
}

interface SkyData {
  date: string;
  lagna_longitude: number;
  lagna_sign: string;
  planets: SkyPlanet[];
}

export default function TodaysSkyWidget() {
  const { language } = useTranslation();
  const hi = language === 'hi';
  const [sky, setSky] = useState<SkyData | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch('/api/kundli/current-sky')
      .then(r => r.json())
      .then(setSky)
      .catch(() => setError(true));
  }, []);

  const formatted = sky
    ? new Date(sky.date).toLocaleDateString(hi ? 'hi-IN' : 'en-IN', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
      })
    : '';

  if (error) return null; // fail silently on homepage

  return (
    <div className="w-full max-w-lg mx-auto">
      {/* Header */}
      <div className="text-center mb-4">
        <p className="text-[11px] font-semibold text-sacred-gold-dark uppercase tracking-[4px] mb-1">
          {hi ? 'आज का आकाश' : "Today's Sky"}
        </p>
        <p className="text-xs text-cosmic-text/50">{formatted}</p>
      </div>

      {/* Chart */}
      {sky ? (
        <ConcentricChart
          natalPlanets={[]}
          transitPlanets={sky.planets.map(p => ({
            planet: p.planet,
            sign: p.sign,
            longitude: p.longitude,
            is_retrograde: p.is_retrograde,
          }))}
          lagnaLongitude={sky.lagna_longitude}
          size={480}
        />
      ) : (
        /* Skeleton */
        <div className="w-full aspect-square max-w-lg mx-auto rounded-full bg-sacred-gold/5 border border-sacred-gold/20 flex items-center justify-center">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-sacred-gold" />
        </div>
      )}

      {/* Lagna sign */}
      {sky && (
        <p className="text-center text-[11px] text-cosmic-text/50 mt-3">
          {hi ? `लग्न: ${sky.lagna_sign}` : `Lagna: ${sky.lagna_sign}`}
          {' · '}
          {hi ? 'स्थान: भारत' : 'Location: India'}
        </p>
      )}
    </div>
  );
}
