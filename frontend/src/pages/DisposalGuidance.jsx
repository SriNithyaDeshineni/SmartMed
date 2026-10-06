import { useNavigate } from "react-router-dom";

function DisposalGuidance() {
  const navigate = useNavigate();

  return (
    <div className="page-container">
      <button onClick={() => navigate("/dashboard")}>
        ← Dashboard
      </button>

      <div className="guidance-card">
        <div className="warning-icon">!</div>

        <h1>Medicine Requires Appropriate Disposal</h1>

        <p>
          This medicine has been identified as expired or
          otherwise submitted for disposal.
        </p>

        <div className="guidance-box">
          <h3>What should you do?</h3>

          <p>
            Use an appropriate medicine take-back or authorized
            disposal channel.
          </p>

          <p>
            Do not dispose of medicines through inappropriate
            household disposal routes.
          </p>
        </div>

        <button
          onClick={() => navigate("/collection-points")}
        >
          Find Collection Points
        </button>
      </div>
    </div>
  );
}

export default DisposalGuidance;