import { useNavigate } from 'react-router-dom';

export default function ExactDaily() {
  const navigate = useNavigate();

  return (
    <section className="section">
      <div className="container split">
        <div className="card card-pad">
          <div className="kicker">Astrology Engine</div>
          <h2 className="section-title" style={{ fontSize: '2.5rem' }}>
            Everything important, but not cluttered.
          </h2>
          <p className="section-subtitle" style={{ margin: '0 0 18px', maxWidth: 'none' }}>
            A complete Vedic astrology platform with clean cards, softer hierarchy, and
            separate destination pages for each feature.
          </p>
          <div className="panel-grid">
            <div>
              <div className="info-box">
                <h4>Core Modules</h4>
                <p>
                  Kundli Generation, Horoscope, Dosha Analysis, Matching, Dasha, D9/D10, Panchang,
                  Muhurat, AI Chat, Spiritual Library, Consultation, and Shop.
                </p>
              </div>
              <div className="spacer-16" />
              <div className="info-box">
                <h4>Recommended Stack</h4>
                <p>
                  React + FastAPI + Swiss Ephemeris + Gemini AI. Real-time calculations
                  with modern architecture.
                </p>
              </div>
            </div>
            <div>
              <div className="list">
                <div className="list-item">
                  <span>{'\uD83E\uDE90'}</span>
                  <div>
                    <b>Kundli Engine:</b> Birth chart, divisional charts, dasha tables, and clean
                    report previews.
                  </div>
                </div>
                <div className="list-item">
                  <span>{'\uD83E\uDD16'}</span>
                  <div>
                    <b>AI Assistant:</b> Chat-style answers to jobs, marriage, timing, and remedies.
                  </div>
                </div>
                <div className="list-item">
                  <span>{'\uD83D\uDDD3'}</span>
                  <div>
                    <b>Panchang:</b> Tithi, nakshatra, yoga, karana, Rahu Kaal, sunrise, and muhurat
                    finder.
                  </div>
                </div>
                <div className="list-item">
                  <span>{'\uD83D\uDECD'}</span>
                  <div>
                    <b>Shop:</b> Gemstones, bracelets, rudraksha, yantras, and bundled consultations.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="mockup">
          <img src="/assets/sage-rishi-2.png" alt="Vedic sage illustration" />
        </div>
      </div>
    </section>
  );
}
