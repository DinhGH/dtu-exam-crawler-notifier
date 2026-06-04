import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import SearchPage from "./pages/SearchPage"; // <-- Nhớ import file mới
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dang-ky" element={<RegisterPage />} />
        <Route path="/tra-cuu" element={<SearchPage />} /> {/* <-- Mở comment dòng này */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;