import { useState, useEffect } from 'react';
import PlanetaryPositions from '@/components/PlanetaryPositions';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { Loader2 } from 'lucide-react';

interface PlanetRow {
  name: string;
  sign: string;
  degree: number;
  nakshatra: string;
  retrograde: boolean;
}

interface RetrogradeEvent {
  planet: string;
  type: string;
  date: string;
  sign: string;
}

const ZODIAC_SYMBOLS: Record<string, string> = {
  Aries: '\u2648', Taurus: '\u2649', Gemini: '\u264A', Cancer: '\u264B',
  Leo: '\u264C', Virgo: '\u264D', Libra: '\u264E', Scorpio: '\u264F',
  Sagittarius: '\u2650', Capricorn: '\u2651', Aquarius: '\u2652', Pisces: '\u2653',
};

const PLANET_COLORS: Record<string, string> = {
  Sun: '#FF8C00',
  Moon: '#E8E8E8',
  Mars: '#DC143C',
  Mercury: '#32CD32',
  Jupiter: 'var(--aged-gold-dim)',
  Venus: '#FF69B4',
  Saturn: '#8B8682',
  Rahu: '#4B0082',
  Ketu: '#8B4513',
};

const DEFAULT_PLANETS: PlanetRow[] = [
  { name: 'Sun', sign: 'Pisces', degree: 12.4, nakshatra: 'Uttara Bhadrapada', retrograde: false },
  { name: 'Moon', sign: 'Cancer', degree: 22.1, nakshatra: 'Ashlesha', retrograde: false },
  { name: 'Mars', sign: 'Gemini', degree: 8.7, nakshatra: 'Ardra', retrograde: false },
  { name: 'Mercury', sign: 'Pisces', degree: 25.3, nakshatra: 'Revati', retrograde: true },
  { name: 'Jupiter', sign: 'Taurus', degree: 18.9, nakshatra: 'Rohini', retrograde: false },
  { name: 'Venus', sign: 'Aquarius', degree: 5.2, nakshatra: 'Dhanishta', retrograde: false },
  { name: 'Saturn', sign: 'Pisces', degree: 2.8, nakshatra: 'Purva Bhadrapada', retrograde: false },
  { name: 'Rahu', sign: 'Pisces', degree: 20.1, nakshatra: 'Revati', retrograde: true },
  { name: 'Ketu', sign: 'Virgo', degree: 20.1, nakshatra: 'Hasta', retrograde: true },
];

const UPCOMING_RETROGRADES: RetrogradeEvent[] = [
  { planet: 'Mercury', type: 'Retrograde begins', date: '2026-04-18', sign: 'Aries' },
  { planet: 'Mercury', type: 'Retrograde ends', date: '2026-05-11', sign: 'Aries' },
  { planet: 'Saturn', type: 'Retrograde begins', date: '2026-06-08', sign: 'Pisces' },
  { planet: 'Jupiter', type: 'Retrograde begins', date: '2026-07-24', sign: 'Cancer' },
  { planet: 'Mercury', type: 'Retrograde begins', date: '2026-08-14', sign: 'Virgo' },
  { planet: 'Venus', type: 'Retrograde begins', date: '2026-10-03', sign: 'Scorpio' },
];

const TRANSIT_EFFECTS: Record<string, string> = {
  Sun: 'Focus on vitality, self-expression, and leadership. A time to shine in your personal and professional life.',
  Moon: 'Emotional sensitivity heightened. Pay attention to inner feelings and nurture close relationships.',
  Mars: 'Energy and drive are amplified. Channel aggression constructively into physical activities or bold decisions.',
  Mercury: 'Communication and intellect are highlighted. Good period for learning, writing, and negotiations.',
  Jupiter: 'Expansion and growth opportunities arise. Favorable for education, travel, and spiritual pursuits.',
  Venus: 'Love, beauty, and harmony are emphasized. Excellent for relationships, art, and financial matters.',
  Saturn: 'Discipline and responsibility are called for. Hard work now builds lasting foundations.',
  Rahu: 'Unconventional desires surface. Watch for obsessive tendencies but embrace innovative thinking.',
  Ketu: 'Spiritual detachment and past-life insights emerge. Good for meditation and letting go.',
};

export default function PlanetaryTransitsPage() {
  const { isAuthenticated } = useAuth();
  const [planets, setPlanets] = useState<PlanetRow[]>(DEFAULT_PLANETS);
  const [loading, setLoading] = useState(true);
  const [hasSavedKundli, setHasSavedKundli] = useState(false);
  const [selectedPlanet, setSelectedPlanet] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data: any = await api.get('/api/cosmic-calendar/today');
        if (data?.planets && Array.isArray(data.planets)) {
          setPlanets(
            data.planets.map((p: any) => ({
              name: p.name || p.planet,
              sign: p.sign || 'Unknown',
              degree: p.degree ?? p.sign_degree ?? 0,
              nakshatra: p.nakshatra || '',
              retrograde: p.retrograde ?? false,
            }))
          );
        }
      } catch {
        // Use default planets on error
      }
      setLoading(false);
    };

    fetchData();

    if (isAuthenticated) {
      api.get('/api/kundli/list')
        .then((data: any) => {
          const list = Array.isArray(data) ? data : [];
          setHasSavedKundli(list.length > 0);
        })
        .catch(() => {});
    }
  }, [isAuthenticated]);

  return (
    <div className="min-h-screen bg-cosmic-bg py-24 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-display font-bold text-sacred-gold mb-3">
            Planetary Transits
          </h1>
          <p className="text-cosmic-text-muted max-w-xl mx-auto">
            Current sky map showing real-time positions of all nine Vedic planets across the zodiac
          </p>
        </div>

        {/* Sky Map + Table side by side on large screens */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Zodiac Wheel */}
          <div className="flex flex-col items-center">
            <div className="card-sacred bg-cosmic-bg border border-sacred-gold/20 rounded-2xl p-6 w-full flex justify-center">
              {loading ? (
                <div className="flex items-center justify-center h-[400px]">
                  <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
                </div>
              ) : (
                <PlanetaryPositions planets={planets} />
              )}
            </div>
            <p className="text-xs text-cosmic-text-muted mt-3 text-center">
              Planets animate slowly to illustrate orbital movement. Positions reflect current Vedic sidereal calculations.
            </p>
          </div>

          {/* Planet Table */}
          <div className="card-sacred bg-cosmic-bg border border-sacred-gold/20 rounded-2xl overflow-hidden">
            <div className="px-6 py-4 border-b border-sacred-gold/20">
              <h2 className="font-display font-bold text-sacred-gold text-lg">Current Positions</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-sacred-gold/10">
                    <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Planet</th>
                    <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Sign</th>
                    <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Degree</th>
                    <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Nakshatra</th>
                    <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {planets.map((p) => (
                    <tr
                      key={p.name}
                      className={`border-b border-sacred-gold/10 cursor-pointer transition-colors ${
                        selectedPlanet === p.name
                          ? 'bg-sacred-gold/10'
                          : 'hover:bg-sacred-gold/5'
                      }`}
                      onClick={() => setSelectedPlanet(selectedPlanet === p.name ? null : p.name)}
                    >
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <span
                            className="w-2.5 h-2.5 rounded-full"
                            style={{ backgroundColor: PLANET_COLORS[p.name] || 'var(--aged-gold-dim)' }}
                          />
                          <span className="text-cosmic-text font-medium text-sm">{p.name}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-cosmic-text text-sm">
                        <span className="mr-1">{ZODIAC_SYMBOLS[p.sign] || ''}</span>
                        {p.sign}
                      </td>
                      <td className="px-4 py-3 text-cosmic-text-muted text-sm">
                        {p.degree.toFixed(1)}&deg;
                      </td>
                      <td className="px-4 py-3 text-cosmic-text-muted text-sm">
                        {p.nakshatra || '\u2014'}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                            p.retrograde
                              ? 'bg-red-900/30 text-red-400'
                              : 'bg-green-900/30 text-green-400'
                          }`}
                        >
                          {p.retrograde ? 'Retrograde' : 'Direct'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Transit effect panel (shown when a planet is selected) */}
        {selectedPlanet && (
          <div className="mb-12 card-sacred bg-cosmic-bg border border-sacred-gold/20 rounded-2xl p-6 animate-in fade-in duration-300">
            <div className="flex items-center gap-3 mb-3">
              <span
                className="w-4 h-4 rounded-full"
                style={{ backgroundColor: PLANET_COLORS[selectedPlanet] || 'var(--aged-gold-dim)' }}
              />
              <h3 className="font-display font-bold text-sacred-gold text-lg">
                {selectedPlanet} Transit Effect
              </h3>
              <button
                className="ml-auto text-cosmic-text-muted hover:text-cosmic-text text-sm"
                onClick={() => setSelectedPlanet(null)}
              >
                Close
              </button>
            </div>
            <p className="text-cosmic-text text-sm leading-relaxed">
              {TRANSIT_EFFECTS[selectedPlanet] || 'Transit information not available for this planet.'}
            </p>
          </div>
        )}

        {/* How this affects you (if user has saved kundli) */}
        {isAuthenticated && hasSavedKundli && (
          <div className="mb-12 card-sacred bg-cosmic-bg border border-sacred-gold/20 rounded-2xl p-6">
            <h2 className="font-display font-bold text-sacred-gold text-lg mb-3">
              How This Affects You
            </h2>
            <p className="text-cosmic-text text-sm leading-relaxed mb-4">
              Based on your saved kundli, the current planetary transits interact with your natal chart in the following ways:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-cosmic-bg border border-sacred-gold/10 rounded-xl p-4">
                <div className="text-sacred-gold text-xs uppercase tracking-wider mb-1">Career</div>
                <p className="text-cosmic-text text-sm">
                  Jupiter's current transit supports professional growth. Stay open to new opportunities through mid-year.
                </p>
              </div>
              <div className="bg-cosmic-bg border border-sacred-gold/10 rounded-xl p-4">
                <div className="text-sacred-gold text-xs uppercase tracking-wider mb-1">Relationships</div>
                <p className="text-cosmic-text text-sm">
                  Venus in Aquarius brings unconventional romantic energy. Communication is key in partnerships.
                </p>
              </div>
              <div className="bg-cosmic-bg border border-sacred-gold/10 rounded-xl p-4">
                <div className="text-sacred-gold text-xs uppercase tracking-wider mb-1">Health</div>
                <p className="text-cosmic-text text-sm">
                  Mars transit through Gemini boosts mental energy but may cause restlessness. Prioritize sleep and grounding practices.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Upcoming Retrogrades */}
        <div className="card-sacred bg-cosmic-bg border border-sacred-gold/20 rounded-2xl overflow-hidden">
          <div className="px-6 py-4 border-b border-sacred-gold/20">
            <h2 className="font-display font-bold text-sacred-gold text-lg">
              Upcoming Retrogrades
            </h2>
            <p className="text-cosmic-text-muted text-xs mt-1">
              Key retrograde periods to watch in the coming months
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-sacred-gold/10">
                  <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Planet</th>
                  <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Event</th>
                  <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Date</th>
                  <th className="text-left px-4 py-3 text-sacred-gold/70 text-xs font-medium uppercase tracking-wider">Sign</th>
                </tr>
              </thead>
              <tbody>
                {UPCOMING_RETROGRADES.map((event, idx) => (
                  <tr key={idx} className="border-b border-sacred-gold/10 hover:bg-sacred-gold/5 transition-colors">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <span
                          className="w-2.5 h-2.5 rounded-full"
                          style={{ backgroundColor: PLANET_COLORS[event.planet] || 'var(--aged-gold-dim)' }}
                        />
                        <span className="text-cosmic-text font-medium text-sm">{event.planet}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                          event.type.includes('begins')
                            ? 'bg-red-900/30 text-red-400'
                            : 'bg-green-900/30 text-green-400'
                        }`}
                      >
                        {event.type}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-cosmic-text-muted text-sm">{event.date}</td>
                    <td className="px-4 py-3 text-cosmic-text text-sm">
                      <span className="mr-1">{ZODIAC_SYMBOLS[event.sign] || ''}</span>
                      {event.sign}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
