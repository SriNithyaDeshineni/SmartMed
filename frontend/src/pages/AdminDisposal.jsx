import { useNavigate } from "react-router-dom";

function AdminDisposal() {
  const navigate = useNavigate();

  const disposalRecords = [
    {
      id: "BATCH-1024",
      quantity: 58,
      facility: "Authorized Disposal Facility",
      status: "Under Treatment"
    },
    {
      id: "BATCH-1025",
      quantity: 34,
      facility: "Authorized Disposal Facility",
      status: "Disposed"
    }
  ];

  return (
    <div className="page-container">
      <button onClick={() => navigate("/admin/dashboard")}>
        ← Admin Dashboard
      </button>

      <div className="page-header">
        <h1>Disposal Status</h1>
      </div>

      <div className="admin-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Batch ID</th>
              <th>Quantity</th>
              <th>Facility</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {disposalRecords.map((record) => (
              <tr key={record.id}>
                <td>{record.id}</td>
                <td>{record.quantity}</td>
                <td>{record.facility}</td>
                <td>
                  <span
                    className={
                      record.status === "Disposed"
                        ? "status collected"
                        : "status pending"
                    }
                  >
                    {record.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AdminDisposal;