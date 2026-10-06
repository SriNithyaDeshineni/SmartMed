import { useLocation, useNavigate } from "react-router-dom";

function Tracking() {
  const navigate = useNavigate();
  const location = useLocation();

  const trackingId =
    location.state?.trackingId || "SM-2026-00125";

  return (
    <div className="page-container">
      <button onClick={() => navigate("/dashboard")}>
        ← Dashboard
      </button>

      <div className="tracking-card">
        <h1>Medicine Disposal Tracking</h1>

        <div className="tracking-id">
          <p>Tracking ID</p>
          <h2>{trackingId}</h2>
        </div>

        <div className="timeline">

          <div className="timeline-item completed">
            <div className="circle">✓</div>
            <div>
              <h3>Submitted</h3>
              <p>Collection request submitted</p>
            </div>
          </div>

          <div className="timeline-line"></div>

          <div className="timeline-item">
            <div className="circle">2</div>
            <div>
              <h3>Collected</h3>
              <p>Waiting for collection</p>
            </div>
          </div>

          <div className="timeline-line"></div>

          <div className="timeline-item">
            <div className="circle">3</div>
            <div>
              <h3>Handed Over</h3>
              <p>Pending handover</p>
            </div>
          </div>

          <div className="timeline-line"></div>

          <div className="timeline-item">
            <div className="circle">4</div>
            <div>
              <h3>Under Treatment</h3>
              <p>Pending authorized processing</p>
            </div>
          </div>

          <div className="timeline-line"></div>

          <div className="timeline-item">
            <div className="circle">5</div>
            <div>
              <h3>Disposed</h3>
              <p>Final disposal status</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default Tracking;