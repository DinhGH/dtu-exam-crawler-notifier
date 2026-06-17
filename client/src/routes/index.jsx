import { Routes, Route, Navigate } from "react-router-dom";
import Register from "../pages/Register/Register";
import AuthRegister from "../pages/AuthRegister/AuthRegister";
import Login from "../pages/Login";
import Files from "../pages/Files/Files";
import Home from "../pages/Home/Home";
import ProtectedRoute from "../components/auth/ProtectedRoute";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route
        path="/register"
        element={
          <ProtectedRoute>
            <Register />
          </ProtectedRoute>
        }
      />
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
      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default Router;
