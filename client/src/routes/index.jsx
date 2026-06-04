import { Routes, Route } from "react-router-dom";
import Register from "../pages/Register/Register";
import Files from "../pages/Files/Files";

const Router = () => {
  return (
    <Routes>
      <Route path="/register" element={<Register />} />
      <Route path="/files" element={<Files />} />
    </Routes>
  );
};

export default Router;
