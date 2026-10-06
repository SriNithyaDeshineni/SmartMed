import { useState } from "react";
import { useNavigate } from "react-router-dom";
import medicines from "../data/medicines";

function MedicineSearch() {
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  const filteredMedicines = medicines.filter((medicine) =>
    medicine.brand.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="page-container">
      <div className="page-header">
        <button onClick={() => navigate("/dashboard")}>← Back</button>
        <h1>Search Medicine</h1>
      </div>

      <input
        className="search-box"
        type="text"
        placeholder="Search medicine..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="medicine-list">
        {filteredMedicines.map((medicine) => (
          <div className="medicine-card" key={medicine.id}>
            <h2>{medicine.brand}</h2>
            <p>{medicine.generic}</p>
            <p>{medicine.strength}</p>
            <p>{medicine.dosageForm}</p>

            <button
              onClick={() => navigate(`/medicine/${medicine.id}`)}
            >
              View Details
            </button>
          </div>
        ))}

        {filteredMedicines.length === 0 && (
          <p>No medicine found.</p>
        )}
      </div>
    </div>
  );
}

export default MedicineSearch;