import { useNavigate } from 'react-router-dom';

export default function ExactStats() {
  const navigate = useNavigate();

  return (
    <section className="section">
      <div className="container">
        <div className="feature-strip">
          <div className="icon-card" style={{ cursor: 'pointer' }} onClick={() => navigate('/kundli')}>
            <div className="icon-circle">{'\u2727'}</div>
            <h3>Kundli</h3>
            <p>North Indian chart preview, houses, dosha insights, and instant astrology report flow.</p>
          </div>
          <div className="icon-card" style={{ cursor: 'pointer' }} onClick={() => navigate('/horoscope')}>
            <div className="icon-circle">{'\u263D'}</div>
            <h3>Horoscope</h3>
            <p>Daily, weekly, monthly, and yearly guidance with a calm editorial layout.</p>
          </div>
          <div className="icon-card" style={{ cursor: 'pointer' }} onClick={() => navigate('/consultation')}>
            <div className="icon-circle">{'\u2665'}</div>
            <h3>Matching</h3>
            <p>Compatibility score, guna milan summary, and marriage-friendly explanation blocks.</p>
          </div>
          <div className="icon-card" style={{ cursor: 'pointer' }} onClick={() => navigate('/panchang')}>
            <div className="icon-circle">{'\u231B'}</div>
            <h3>Muhurat</h3>
            <p>Auspicious timing for marriage, griha pravesh, travel, and puja planning.</p>
          </div>
          <div className="icon-card" style={{ cursor: 'pointer' }} onClick={() => navigate('/library')}>
            <div className="icon-circle">{'\uD83D\uDCDC'}</div>
            <h3>Library</h3>
            <p>Gita, mantras, aarti, pooja vidhi, vrat katha, and daily spiritual reading pages.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
