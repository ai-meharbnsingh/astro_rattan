import { useNavigate } from 'react-router-dom';

export default function ExactQuickLinks() {
  const navigate = useNavigate();

  return (
    <section className="section">
      <div className="container center">
        <div className="kicker">Quick Entry Points</div>
        <h2 className="section-title">Choose your starting journey</h2>
        <p className="section-subtitle">
          Use these clean paths instead of dumping everything on one page.
        </p>
        <div className="tools">
          <div className="tool-card">
            <h4>Free Janam Kundli</h4>
            <p>Birth details form, chart preview, yogas, and AI interpretation blocks.</p>
            <div className="spacer-16" />
            <button className="btn btn-primary" onClick={() => navigate('/kundli')}>
              Open Page
            </button>
          </div>
          <div className="tool-card">
            <h4>Ask AI Astrologer</h4>
            <p>Chat interface with personalized answers and remedy recommendations.</p>
            <div className="spacer-16" />
            <button className="btn btn-primary" onClick={() => navigate('/ai-chat')}>
              Open Page
            </button>
          </div>
          <div className="tool-card">
            <h4>Today's Panchang</h4>
            <p>Daily timing cards, fast calculators, and a dedicated muhurat page.</p>
            <div className="spacer-16" />
            <button className="btn btn-primary" onClick={() => navigate('/panchang')}>
              Open Page
            </button>
          </div>
          <div className="tool-card">
            <h4>Spiritual Library</h4>
            <p>Bhagavad Gita, mantra sections, and evergreen content for SEO and retention.</p>
            <div className="spacer-16" />
            <button className="btn btn-primary" onClick={() => navigate('/library')}>
              Open Page
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
