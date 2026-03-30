import { useNavigate } from 'react-router-dom';

export default function ExactHero() {
  const navigate = useNavigate();

  return (
    <section className="hero">
      <div className="container hero-grid">
        <div className="hero-copy">
          <div className="hero-eyebrow">
            <span style={{ fontSize: '1.1rem' }}>{'\u0950'}</span>
            Template 2 Style &middot; Light Vedic Luxury
          </div>
          <h1>Know Your Karma.<br />Shape Your Future.</h1>
          <p>
            A complete copy-paste website template inspired by your preferred light, parchment-style
            astrology design. It uses the same generated images, warm tones, calm spacing, and a
            cleaner flow than AstroSage.
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
            <img src="/assets/feature-mockups.png" alt="Feature mockups" />
          </div>
          <div className="grid-2">
            <div className="visual-card">
              <img src="/assets/asset-pack-1.png" alt="Asset pack" />
            </div>
            <div className="visual-card">
              <img src="/assets/template-board-2.png" alt="Template board" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
