import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import MedicineSearch from "./pages/MedicineSearch";
import MedicineDetails from "./pages/MedicineDetails";
import AddMedicine from "./pages/AddMedicine";
import DisposalGuidance from "./pages/DisposalGuidance";
import CollectionPoints from "./pages/CollectionPoints";
import RequestCollection from "./pages/RequestCollection";
import Tracking from "./pages/Tracking";
import AdminDashboard from "./pages/AdminDashboard";
import AdminRequests from "./pages/AdminRequests";
import AdminBatches from "./pages/AdminBatches";
import AdminDisposal from "./pages/AdminDisposal";
function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Default */}
        <Route path="/" element={<Navigate to="/login" />} />

        {/* Authentication */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* User Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Medicine */}
        <Route path="/medicines" element={<MedicineSearch />} />
        <Route path="/medicine/:id" element={<MedicineDetails />} />

        {/* Disposal */}
        <Route path="/add-medicine" element={<AddMedicine />} />
        <Route
          path="/disposal-guidance"
          element={<DisposalGuidance />}
        />
        <Route
  path="/collection-points"
  element={<CollectionPoints />}
/>

<Route
  path="/request-collection"
  element={<RequestCollection />}
/>

<Route
  path="/tracking"
  element={<Tracking />}
/>
<Route
  path="/admin/dashboard"
  element={<AdminDashboard />}
/>
<Route
  path="/admin/requests"
  element={<AdminRequests />}
/>
<Route
  path="/admin/batches"
  element={<AdminBatches />}
/>

<Route
  path="/admin/disposal"
  element={<AdminDisposal />}
/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;