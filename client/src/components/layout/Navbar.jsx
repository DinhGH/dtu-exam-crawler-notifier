/* eslint-disable react-hooks/set-state-in-effect */
/* eslint-disable no-undef */
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Menu, X, LogOut } from "lucide-react";
import { Button } from "../ui/Button";
import { useState, useEffect } from "react";
import { Modal } from "../ui/Modal";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const [username] = useState(localStorage.getItem("username") || "");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setIsAuthenticated(false);
    navigate("/login");
    setIsLogoutModalOpen(false);
  };

  const navLinks = [
    { name: "Trang chủ", path: "/home" },
    { name: "Đăng ký theo dõi", path: "/register" },
    { name: "Danh sách tệp", path: "/files" },
  ];

  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("token"),
  );

  useEffect(() => {
    setIsAuthenticated(!!localStorage.getItem("token"));
  }, [location]);

  return (
    <>
      <header className="sticky top-0 z-40 w-full border-b border-gray-200 bg-white/95 backdrop-blur">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link
            to="/home"
            className="flex items-center space-x-2 font-bold text-blue-600"
          >
            <span>DTU Exam Notifier</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            {isAuthenticated &&
              navLinks.map((link) => {
                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                      location.pathname === link.path
                        ? "text-blue-600"
                        : "text-gray-700 hover:text-gray-900"
                    }`}
                  >
                    {link.name}
                  </Link>
                );
              })}
            {isAuthenticated && username && (
              <span className="text-sm font-medium text-[#000000]">
                Xin chào, {username}
              </span>
            )}
            {isAuthenticated && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsLogoutModalOpen(true)}
                className="rounded-full text-gray-700 hover:text-red-600"
                title="Đăng xuất"
              >
                <LogOut className="h-5 w-5" />
              </Button>
            )}
          </nav>

          {/* Mobile Menu Button */}
          <div className="flex items-center md:hidden space-x-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="h-5 w-5 text-gray-700" />
              ) : (
                <Menu className="h-5 w-5 text-gray-700" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && isAuthenticated && (
          <div className="md:hidden border-t border-gray-200 bg-white">
            <nav className="flex flex-col p-4 space-y-2">
              {navLinks.map((link) => {
                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    className={`px-3 py-2 rounded-md text-base font-medium ${
                      location.pathname === link.path
                        ? "bg-blue-50 text-blue-600"
                        : "text-gray-700 hover:bg-gray-50"
                    }`}
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {link.name}
                  </Link>
                );
              })}
              <button
                onClick={() => {
                  setIsLogoutModalOpen(true);
                  setIsMenuOpen(false);
                }}
                className="px-3 py-2 rounded-md text-base font-medium text-red-600 hover:bg-red-50 text-left flex items-center space-x-2"
              >
                <LogOut className="h-5 w-5" />
                <span>Đăng xuất</span>
              </button>
            </nav>
          </div>
        )}
      </header>
      {isLogoutModalOpen && (
        <Modal
          isOpen={isLogoutModalOpen}
          onClose={() => setIsLogoutModalOpen(false)}
          title="Xác nhận đăng xuất"
        >
          <div className="space-y-4">
            <p className="text-gray-600">
              Bạn có chắc chắn muốn đăng xuất khỏi hệ thống?
            </p>
            <div className="flex justify-end space-x-3">
              <Button
                variant="ghost"
                onClick={() => setIsLogoutModalOpen(false)}
              >
                Hủy
              </Button>
              <Button
                className="bg-red-600 hover:bg-red-700 text-white"
                onClick={handleLogout}
              >
                Đăng xuất
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </>
  );
};

export { Navbar };
