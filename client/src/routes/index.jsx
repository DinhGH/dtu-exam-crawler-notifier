import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home/Home";
import Register from "../pages/Register/Register";
import Search from "../pages/Search/Search";
import Files from "../pages/Files/Files";
import Dashboard from "../pages/Dashboard/Dashboard";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="/search" element={<Search />} />
      <Route path="/files" element={<Files />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
};

export default Router;
