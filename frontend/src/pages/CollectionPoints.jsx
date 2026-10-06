import { useNavigate } from "react-router-dom";

function CollectionPoints() {
  const navigate = useNavigate();

  const collectionPoints = [
    {
      id: 1,
      name: "SmartMed Collection Center",
      location: "Hyderabad",
      distance: "1.2 km"
    },
    {
      id: 2,
      name: "Green Medicine Collection Point",
      location: "Hyderabad",
      distance: "2.4 km"
    },
    {
      id: 3,
      name: "Community Medicine Center",
      location: "Hyderabad",
      distance: "3.1 km"
    }
  ];

  const selectPoint = (point) => {
    navigate("/request-collection", {
      state: { collectionPoint: point }
    });
  };

  return (
    <div className="page-container">
      <button onClick={() => navigate("/disposal-guidance")}>
        ← Back
      </button>

      <div className="page-header">
        <h1>Collection Points</h1>
      </div>

      <p className="page-description">
        Select a registered collection point for your medicine.
      </p>

      <div className="collection-list">
        {collectionPoints.map((point) => (
          <div className="collection-card" key={point.id}>
            <div>
              <h2>{point.name}</h2>
              <p>{point.location}</p>
              <p>{point.distance} away</p>
            </div>

            <button onClick={() => selectPoint(point)}>
              Select
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CollectionPoints;