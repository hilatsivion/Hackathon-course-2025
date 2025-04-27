import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FormPage from "./pages/FormPage/FormPage";
import PredicationPage from "./pages/PredicationPage/PredicationPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FormPage />} />
        <Route path="/dashboard" element={<PredicationPage />} />
      </Routes>
    </Router>
  );
}

export default App;
