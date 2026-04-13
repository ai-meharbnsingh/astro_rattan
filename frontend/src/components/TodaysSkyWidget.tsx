/**
 * TodaysSkyWidget — live concentric / diamond transit chart for the homepage.
 * Fetches today's planetary positions from GET /api/kundli/current-sky (no auth).
 */
import { useEffect, useRef, useState } from 'react';
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
  const containerRef = useRef<HTMLDivElement>(null);
  const [chartSize, setChartSize] = useState(380);

  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        setChartSize(Math.min(480, containerRef.current.clientWidth - 32));
      }
    };
    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

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

  if (error) return (
    <div className="text-center py-8 text-gray-400">
      <p className="text-sm">Unable to load sky data</p>
      <button onClick={() => window.location.reload()} className="mt-2 text-xs text-sacred-gold hover:underline">
        Retry
      </button>
    </div>
  );

  return (
    <div ref={containerRef} className="w-full max-w-lg mx-auto">
      {/* Context heading for visitors */}
      <h2 className="text-2xl font-bold text-center mb-2">Today's Planetary Positions</h2>
      <p className="text-sm text-gray-500 text-center mb-6">Live positions of planets in the sky right now</p>

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
          size={chartSize}
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

      {/* CTA */}
      <p className="text-center mt-4">
        <a href="/kundli" className="text-sacred-gold hover:underline text-sm font-medium">
          See how today's sky affects your chart &rarr;
        </a>
      </p>
    </div>
  );
}
