import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminBatches() {
  const navigate = useNavigate();

  const [batches, setBatches] = useState([
    {
      id: "BATCH-1024",
      medicines: 12,
      quantity: 58,
      center: "SmartMed Collection Center",
      status: "Collected"
    },
    {
      id: "BATCH-1025",
      medicines: 8,
      quantity: 34,
      center: "Green Medicine Collection Point",
      status: "Handed Over"
    }
  ]);

  const updateBatch = (id) => {
    setBatches((current) =>
      current.map((batch) =>
        batch.id === id
          ? {
              ...batch,
              status:
                batch.status === "Collected"
                  ? "Handed Over"
                  : "Disposed"
            }
          : batch
      )
    );
  };

  return (
    <div className="page-container">
      <button onClick={() => navigate("/admin/dashboard")}>
        ← Admin Dashboard
      </button>

      <div className="page-header">
        <h1>Medicine Batches</h1>
      </div>

      <div className="batch-grid">
        {batches.map((batch) => (
          <div className="batch-card" key={batch.id}>
            <h2>{batch.id}</h2>

            <p>
              <strong>Medicines:</strong> {batch.medicines}
            </p>

            <p>
              <strong>Total Quantity:</strong> {batch.quantity}
            </p>

            <p>
              <strong>Collection Center:</strong> {batch.center}
            </p>

            <p>
              <strong>Status:</strong> {batch.status}
            </p>

            {batch.status !== "Disposed" && (
              <button
                className="small-button"
                onClick={() => updateBatch(batch.id)}
              >
                {batch.status === "Collected"
                  ? "Mark Handed Over"
                  : "Mark Disposed"}
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default AdminBatches;