import { useNavigate } from 'react-router-dom';

export default function ExactAIAssistant() {
  const navigate = useNavigate();

  return (
    <section className="section">
      <div className="container split">
        <div className="card card-pad">
          <div className="kicker">AI Astrologer</div>
          <h2 className="section-title" style={{ fontSize: '2.2rem' }}>
            Your personal Vedic guide, powered by AI.
          </h2>
          <p className="section-subtitle" style={{ margin: '0 0 18px', maxWidth: 'none' }}>
            Ask about career, relationships, health, or remedies. Our AI Astrologer combines
            traditional Jyotish knowledge with modern language models to give you clear,
            personalized insights based on your birth chart.
          </p>
          <div className="list">
            <div className="list-item">
              <span>{'\uD83E\uDE90'}</span>
              <div>
                <b>Chart-aware:</b> Reads your Kundli and gives answers specific to your planetary positions.
              </div>
            </div>
            <div className="list-item">
              <span>{'\uD83D\uDCAC'}</span>
              <div>
                <b>Natural conversation:</b> Ask in plain language — get Vedic wisdom in return.
              </div>
            </div>
            <div className="list-item">
              <span>{'\uD83D\uDD2E'}</span>
              <div>
                <b>Remedies included:</b> Mantras, gemstones, and rituals tailored to your situation.
              </div>
            </div>
          </div>
          <div className="spacer-16" />
          <button className="btn btn-primary" onClick={() => navigate('/ai-chat')}>
            Try AI Astrologer
          </button>
        </div>
        <div className="mockup">
          <img src="/assets/phone-mockup.png" alt="AI Astrologer chat on phone" />
        </div>
      </div>
    </section>
  );
}
