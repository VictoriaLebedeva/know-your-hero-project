import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Reviews from "./pages/Reviews";
import AddReview from "./pages/AddReview";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/reviews" />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/reviews" element={<Reviews />} />
        <Route path="/reviews/new" element={<AddReview />} />
      </Routes>
    </Router>
  );
}

export default App;
