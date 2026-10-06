import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>SmartMed</h1>
          <p>Safe Medicine Disposal</p>
        </div>

        <button onClick={() => navigate("/login")}>Logout</button>
      </header>

      <main className="dashboard-content">
        <h2>Welcome to SmartMed</h2>
        <p className="dashboard-subtitle">
          Manage and safely dispose of your unused or expired medicines.
        </p>

        <div className="stats">
          <div className="stat-card">
            <h3>My Medicines</h3>
            <strong>5</strong>
          </div>

          <div className="stat-card">
            <h3>Pending Requests</h3>
            <strong>2</strong>
          </div>

          <div className="stat-card">
            <h3>Disposed</h3>
            <strong>8</strong>
          </div>
        </div>

        <div className="dashboard-actions">
          <button onClick={() => navigate("/medicines")}>
            Search Medicine
          </button>

          <button onClick={() => navigate("/add-medicine")}>
            Add Medicine for Disposal
          </button>

          <button onClick={() => navigate("/tracking")}>
            Track Disposal
          </button>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;