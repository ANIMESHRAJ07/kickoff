import { useEffect, useState } from 'react';
import axios from 'axios';

const initialForm = {
  full_name: '',
  sap_id: '',
  phone: '',
  branch: '',
};

const apiUrl = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');

const pastEventPhotos = [
  ['/past-events/event%201.png', 'LAST MINUTE C', 'Students gathering for KICKOFF'],
  ['/past-events/event%202.png', 'WEB3', 'Teams building under pressure'],
  ['/past-events/event%203.png', 'KICKOFF 23', 'Ideas taking shape on stage'],
  ['/past-events/event%204.png', 'DRUNK N CODE', 'A room full of curious minds'],
  ['/past-events/event%205.png', 'FACEBOOK- CAPTURE THE FLAG', 'Late-night collaboration and code'],
  ['/past-events/event%206.png', 'AWARDING OUR WINNERS', 'Sharing knowledge, sharing tools'],
  ['/past-events/event%207.png', 'IDEA N PROTOTYPE', 'Learning by making together'],
  ['/past-events/event%208.png', 'CODEGENX SHOWCASE', 'The community starts here'],
  ['/past-events/event%209.png', 'LAST MINUTE DSA', 'From first sketch to working project'],
  ['/past-events/event%2010.png', 'LAST MINUTE DSA', 'Celebrating what students create'],
];

function App() {
  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState({ type: '', message: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activePhoto, setActivePhoto] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setActivePhoto((currentPhoto) => (currentPhoto + 1) % pastEventPhotos.length);
    }, 4000);

    return () => window.clearInterval(timer);
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((currentForm) => ({ ...currentForm, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setStatus({ type: '', message: '' });

    try {
      await axios.post(`${apiUrl}/registrations`, form);
      setForm(initialForm);
      setStatus({
        type: 'success',
        message: 'You are registered. Your details have been saved.',
      });
    } catch (error) {
      const message = error.response?.data?.detail;
      const readableMessage = Array.isArray(message)
        ? message.map((item) => item.msg).join(' ')
        : message;
      setStatus({
        type: 'error',
        message: readableMessage || 'Registration could not be completed. Please try again.',
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="site-shell">
      <nav className="site-nav" aria-label="Main navigation">
        <a className="brand" href="#top">CodeGenX<span>/ DIT</span></a>
        <div className="nav-links">
          <a href="#about">Why CodeGenX</a>
          <a href="#past-events">Past events</a>
          <a className="nav-cta" href="#register">Register <span aria-hidden="true">-&gt;</span></a>
        </div>
      </nav>

      <section className="landing-hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow">CODEGENX / Est. 2012</p>
          <h1 className="event-title"><span>KICKOFF</span><strong>'26</strong></h1>
          <p className="hero-lede">Meet. Create. Connect.</p>
          <p className="hero-description">A first step into the people, projects, and possibilities of CodeGenX, DIT University's oldest technical club.</p>
          <div className="hero-actions">
            <a className="primary-btn hero-button" href="#register">Reserve your place <span aria-hidden="true">-&gt;</span></a>
            <span className="hero-note">25 SEP / 04-06 PM / VISVESVARAYA 105</span>
          </div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="hero-orbit orbit-one" />
          <div className="hero-orbit orbit-two" />
          <span className="hero-year">26</span>
          <span className="hero-star">✦</span>
        </div>
      </section>

      <section className="about-section" id="about">
        <div className="section-intro">
          <p className="section-label">The reason we gather</p>
          <h2>Technical curiosity, made collective.</h2>
        </div>
        <div className="about-copy">
          <p>Founded in 2012, CodeGenX is the oldest technical club at DIT University. For more than a decade, it has been a place where beginners meet builders, questions become projects, and students find their people.</p>
          <p>We believe technology is best learned together: through conversation, experimentation, and the confidence to start before you feel ready.</p>
          <div className="about-stats"><strong>2012</strong><span>Founded at DIT University</span><strong>01</strong><span>Community for every curious mind</span></div>
        </div>
      </section>

      <section className="past-events" id="past-events">
        <div className="past-photo" aria-roledescription="carousel" aria-label="Past CodeGenX events">
          {pastEventPhotos.map(([src, , alt], index) => (
            <img className={index === activePhoto ? 'past-slide active' : 'past-slide'} key={src} src={src} alt={alt} />
          ))}
          <span className="photo-caption">{pastEventPhotos[activePhoto][1]}</span>
          <button className="carousel-control previous" type="button" onClick={() => setActivePhoto((activePhoto - 1 + pastEventPhotos.length) % pastEventPhotos.length)} aria-label="Previous event photo">&lt;</button>
          <button className="carousel-control next" type="button" onClick={() => setActivePhoto((activePhoto + 1) % pastEventPhotos.length)} aria-label="Next event photo">&gt;</button>
          <div className="carousel-dots" aria-label="Choose event photo">
            {pastEventPhotos.map(([, name], index) => (
              <button className={index === activePhoto ? 'carousel-dot active' : 'carousel-dot'} type="button" key={name} onClick={() => setActivePhoto(index)} aria-label={`Show ${name}`} aria-pressed={index === activePhoto} />
            ))}
          </div>
        </div>
        <div className="past-copy">
          <p className="section-label">Past events</p>
          <h2>Every event leaves a spark.</h2>
          <p>CodeGenX events bring students together to learn, build, and share without the pressure to already know everything.</p>
          <p>From first conversations to ambitious projects, every gathering is a chance to find your people and start something useful.</p>
          <p>KICKOFF ’26 is the next chapter.</p>
          <a className="text-link" href="#register">Be part of the next one <span aria-hidden="true">-&gt;</span></a>
        </div>
      </section>

      <section className="registration-section" id="register" aria-labelledby="registration-title">
        <div className="registration-intro">
          <p className="section-label">KICKOFF ’26 / 25 September</p>
          <h2 id="registration-title">Join the room.</h2>
          <p>Visvesvaraya 105, DIT University<br />04 PM - 06 PM</p>
        </div>
        <div className="form-panel">
        <div className="form-heading">
          <p className="section-label">Reserve your place</p>
          <p>Complete your details and we will take care of the rest.</p>
        </div>

        <form onSubmit={handleSubmit}>
          <label>
            Full name
            <input name="full_name" value={form.full_name} onChange={handleChange} required minLength="2" maxLength="120" placeholder="Aarav Sharma" />
          </label>
          <label>
            SAP ID
            <input name="sap_id" value={form.sap_id} onChange={handleChange} required minLength="2" maxLength="40" placeholder="Your SAP ID" />
          </label>
          <div className="field-row">
            <label>
              Phone
              <input name="phone" type="tel" value={form.phone} onChange={handleChange} required minLength="7" maxLength="30" placeholder="9876543210" />
            </label>
            <label>
              Branch
              <input name="branch" value={form.branch} onChange={handleChange} required minLength="2" maxLength="160" placeholder="Computer Science" />
            </label>
          </div>
          <button className="primary-btn" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Submitting...' : 'Complete registration'}
            <span aria-hidden="true">-&gt;</span>
          </button>
        </form>

        {status.message && (
          <p className={`form-status ${status.type}`} role="status">{status.message}</p>
        )}
        </div>
      </section>

      <footer className="site-footer">
        <a className="brand" href="#top">CodeGenX<span>/ DIT</span></a>
        <p>Meet. Create. Connect. Since 2012.</p>
        <div className="social-links">
          <a href="https://www.linkedin.com/company/codegenx-ditu/posts/?feedView=all" target="_blank" rel="noreferrer">LinkedIn <span aria-hidden="true">↗</span></a>
          <a href="https://www.instagram.com/codegenx/" target="_blank" rel="noreferrer">Instagram <span aria-hidden="true">↗</span></a>
        </div>
      </footer>
    </main>
  );
}

export default App;
