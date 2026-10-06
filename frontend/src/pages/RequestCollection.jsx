import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

function RequestCollection() {
  const navigate = useNavigate();
  const location = useLocation();

  const collectionPoint = location.state?.collectionPoint;

  const [quantity, setQuantity] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();

    navigate("/tracking", {
      state: {
        trackingId: "SM-2026-00125",
        quantity: quantity,
        collectionPoint: collectionPoint
      }
    });
  };

  return (
    <div className="page-container">
      <button onClick={() => navigate("/collection-points")}>
        ← Back
      </button>

      <div className="form-card">
        <h1>Collection Request</h1>

        <div className="request-info">
          <h3>Medicine</h3>
          <p>Paracetamol 500 mg</p>

          <h3>Collection Point</h3>

          {collectionPoint ? (
            <>
              <p>{collectionPoint.name}</p>
              <p>{collectionPoint.location}</p>
            </>
          ) : (
            <p>No collection point selected</p>
          )}
        </div>

        <form onSubmit={handleSubmit}>
          <label>Quantity</label>

          <input
            type="number"
            min="1"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />

          <button type="submit">
            Submit Collection Request
          </button>
        </form>
      </div>
    </div>
  );
}

export default RequestCollection;