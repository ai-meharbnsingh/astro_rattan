import { useNavigate } from 'react-router-dom';

export default function ExactRecommended() {
  const navigate = useNavigate();

  return (
    <section className="section">
      <div className="container">
        <div className="quote">
          &ldquo;The planets give results. We help users understand them with clarity, warmth, and modern flow.&rdquo;
        </div>
      </div>
    </section>
  );
}
