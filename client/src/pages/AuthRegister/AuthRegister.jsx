import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import apiClient from "../../services/apiClient";
import { toast } from "sonner";

const AuthRegister = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast.error("Mật khẩu không khớp!");
      return;
    }
    try {
      await apiClient.post("/auth/register", {
        username,
        email,
        password,
      });
      toast.success("Đăng ký tài khoản thành công!");
      navigate("/login");
    } catch (error) {
      console.error("Registration failed:", error);
      toast.error(error.response?.data?.detail || "Đăng ký thất bại.");
    }
  };

  return (
    <div className="h-[calc(100vh-150px)] flex items-center justify-center bg-white overflow-hidden">
      <div className="bg-[#fafbfb] p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Đăng Ký Tài Khoản
        </h2>
        <form onSubmit={handleRegister}>
          <div className="mb-4">
            <Input
              label="Tên đăng nhập"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <Input
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <Input
              label="Mật khẩu"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="mb-6">
            <Input
              label="Nhập lại mật khẩu"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full">
            Đăng Ký
          </Button>
        </form>
        <p className="mt-4 text-center text-sm">
          Đã có tài khoản?{" "}
          <button
            type="button"
            onClick={() => navigate("/login")}
            className="text-blue-600 hover:underline"
          >
            Đăng nhập
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthRegister;
