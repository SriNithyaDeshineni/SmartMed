import { useNavigate } from "react-router-dom";

function AdminDashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>SmartMed Admin</h1>
          <p>Medicine Disposal Management</p>
        </div>

        <button onClick={() => navigate("/login")}>
          Logout
        </button>
      </header>

      <main className="dashboard-content">
        <h2>Admin Dashboard</h2>
        <p className="dashboard-subtitle">
          Monitor medicine collection and disposal activities.
        </p>

        <div className="stats">
          <div className="stat-card">
            <h3>Total Medicines</h3>
            <strong>1,250</strong>
          </div>

          <div className="stat-card">
            <h3>Pending Requests</h3>
            <strong>42</strong>
          </div>

          <div className="stat-card">
            <h3>Disposed</h3>
            <strong>1,102</strong>
          </div>

          <div className="stat-card">
            <h3>Total Quantity</h3>
            <strong>5,430</strong>
          </div>
        </div>

        <div className="admin-actions">
          <button onClick={() => navigate("/admin/requests")}>
            Collection Requests
          </button>

          <button onClick={() => navigate("/admin/batches")}>
            Medicine Batches
          </button>

          <button onClick={() => navigate("/admin/disposal")}>
            Disposal Status
          </button>
        </div>
      </main>
    </div>
  );
}

export default AdminDashboard;