import { useNavigate, useParams } from "react-router-dom";
import medicines from "../data/medicines";

function MedicineDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const medicine = medicines.find(
    (item) => item.id === Number(id)
  );

  if (!medicine) {
    return <h2>Medicine not found</h2>;
  }

  return (
    <div className="page-container">
      <button onClick={() => navigate("/medicines")}>
        ← Back
      </button>

      <div className="medicine-details">
        <h1>{medicine.brand}</h1>

        <div className="details-grid">
          <p><strong>Generic:</strong> {medicine.generic}</p>
          <p><strong>Strength:</strong> {medicine.strength}</p>
          <p><strong>Manufacturer:</strong> {medicine.manufacturer}</p>
          <p><strong>Dosage Form:</strong> {medicine.dosageForm}</p>
          <p><strong>Drug Class:</strong> {medicine.drugClass}</p>
          <p><strong>Indication:</strong> {medicine.indication}</p>
        </div>

        <button
          onClick={() => navigate(`/add-medicine?id=${medicine.id}`)}
        >
          Add for Disposal
        </button>
      </div>
    </div>
  );
}

export default MedicineDetails;