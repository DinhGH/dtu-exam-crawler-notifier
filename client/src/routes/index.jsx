import { Routes, Route, Navigate } from "react-router-dom";
import Register from "../pages/Register/Register";
import AuthRegister from "../pages/AuthRegister/AuthRegister";
import Login from "../pages/Login";
import Files from "../pages/Files/Files";
import ProtectedRoute from "../components/auth/ProtectedRoute";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/register" element={<Register />} />
      <Route path="/auth-register" element={<AuthRegister />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/files"
        element={
          <ProtectedRoute>
            <Files />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default Router;
