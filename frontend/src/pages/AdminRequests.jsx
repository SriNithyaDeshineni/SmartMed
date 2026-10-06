import { useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminRequests() {
  const navigate = useNavigate();

  const [requests, setRequests] = useState([
    {
      id: "SM-2026-00125",
      medicine: "Paracetamol",
      quantity: 10,
      user: "User 1",
      location: "Hyderabad",
      status: "Pending"
    },
    {
      id: "SM-2026-00126",
      medicine: "Amoxicillin",
      quantity: 5,
      user: "User 2",
      location: "Hyderabad",
      status: "Collected"
    },
    {
      id: "SM-2026-00127",
      medicine: "Cetirizine",
      quantity: 8,
      user: "User 3",
      location: "Hyderabad",
      status: "Pending"
    }
  ]);

  const updateStatus = (id) => {
    setRequests((currentRequests) =>
      currentRequests.map((request) =>
        request.id === id
          ? { ...request, status: "Collected" }
          : request
      )
    );
  };

  return (
    <div className="page-container">
      <button onClick={() => navigate("/admin/dashboard")}>
        ← Admin Dashboard
      </button>

      <div className="page-header">
        <h1>Collection Requests</h1>
      </div>

      <div className="admin-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Tracking ID</th>
              <th>Medicine</th>
              <th>Quantity</th>
              <th>User</th>
              <th>Location</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {requests.map((request) => (
              <tr key={request.id}>
                <td>{request.id}</td>
                <td>{request.medicine}</td>
                <td>{request.quantity}</td>
                <td>{request.user}</td>
                <td>{request.location}</td>
                <td>
                  <span
                    className={
                      request.status === "Collected"
                        ? "status collected"
                        : "status pending"
                    }
                  >
                    {request.status}
                  </span>
                </td>
                <td>
                  {request.status === "Pending" ? (
                    <button
                      className="small-button"
                      onClick={() => updateStatus(request.id)}
                    >
                      Mark Collected
                    </button>
                  ) : (
                    <span>Completed</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AdminRequests;