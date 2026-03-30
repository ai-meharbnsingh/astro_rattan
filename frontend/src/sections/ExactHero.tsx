import { useNavigate } from 'react-router-dom';

export default function ExactHero() {
  const navigate = useNavigate();

  return (
    <section className="hero">
      <div className="container hero-grid">
        <div className="hero-copy">
          <div className="hero-eyebrow">
            <span style={{ fontSize: '1.1rem' }}>{'\u0950'}</span>
            Vedic Astrology &middot; Ancient Wisdom
          </div>
          <h1>Know Your Karma.<br />Shape Your Future.</h1>
          <p>
            Explore your birth chart, consult AI-powered astrologers, and discover auspicious
            timings rooted in centuries of Vedic tradition. Accurate Kundli generation, daily
            Panchang, and personalized horoscopes — all in one place.
          </p>
          <div className="hero-actions">
            <button className="btn btn-primary" onClick={() => navigate('/kundli')}>
              Generate Free Kundli
            </button>
            <button className="btn btn-secondary" onClick={() => navigate('/ai-chat')}>
              Ask AI Astrologer
            </button>
          </div>
          <div className="stats">
            <div className="stat"><strong>500K+</strong><span>Kundlis Generated</span></div>
            <div className="stat"><strong>120+</strong><span>Expert Astrologers</span></div>
            <div className="stat"><strong>4.9/5</strong><span>Client Rating</span></div>
            <div className="stat"><strong>1998</strong><span>Tradition Since</span></div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="visual-card">
            <img src="/assets/sage-rishi.png" alt="Vedic sage in meditation" />
          </div>
        </div>
      </div>
    </section>
  );
}
