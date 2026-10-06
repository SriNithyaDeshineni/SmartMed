import { useNavigate, useSearchParams } from "react-router-dom";
import { useState } from "react";
import medicines from "../data/medicines";

function AddMedicine() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const medicineId = searchParams.get("id");

  const medicine = medicines.find(
    (item) => item.id === Number(medicineId)
  );

  const [quantity, setQuantity] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [condition, setCondition] = useState("Good");
  const [reason, setReason] = useState("Expired");

  const handleSubmit = (e) => {
    e.preventDefault();

    const today = new Date();
    const expiry = new Date(expiryDate);

    if (expiry < today) {
      navigate("/disposal-guidance");
    } else {
      alert("This medicine is not expired.");
    }
  };

  return (
    <div className="page-container">
      <button onClick={() => navigate(-1)}>
        ← Back
      </button>

      <div className="form-card">
        <h1>Add Medicine for Disposal</h1>

        {medicine && (
          <div className="selected-medicine">
            <h2>{medicine.brand}</h2>
            <p>
              {medicine.generic} · {medicine.strength}
            </p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <label>Quantity</label>
          <input
            type="number"
            min="1"
            placeholder="Enter quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />

          <label>Expiry Date</label>
          <input
            type="date"
            value={expiryDate}
            onChange={(e) => setExpiryDate(e.target.value)}
            required
          />

          <label>Condition</label>
          <select
            value={condition}
            onChange={(e) => setCondition(e.target.value)}
          >
            <option>Good</option>
            <option>Damaged</option>
            <option>Opened</option>
          </select>

          <label>Reason</label>

          <div className="radio-group">
            <label>
              <input
                type="radio"
                value="Expired"
                checked={reason === "Expired"}
                onChange={(e) => setReason(e.target.value)}
              />
              Expired
            </label>

            <label>
              <input
                type="radio"
                value="Unused"
                checked={reason === "Unused"}
                onChange={(e) => setReason(e.target.value)}
              />
              Unused
            </label>
          </div>

          <button type="submit">
            Check Disposal Status
          </button>
        </form>
      </div>
    </div>
  );
}

export default AddMedicine;