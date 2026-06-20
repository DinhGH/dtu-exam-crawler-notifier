import { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";
import { toast } from "sonner";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await apiClient.post("/auth/login", {
        username: username,
        password: password,
      });
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);
      localStorage.setItem("username", username);
      toast.success("Đăng nhập thành công!");
      navigate("/home");
    } catch (error) {
      console.error("Login failed:", error);
      toast.error(
        error.response?.data?.detail ||
          "Tên đăng nhập hoặc mật khẩu không chính xác.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-150px)] flex items-center justify-center bg-white overflow-hidden">
      <div className="bg-[#fafbfb] p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">Đăng Nhập</h2>
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <Input
              label="Tên đăng nhập"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="mb-6">
            <Input
              label="Mật khẩu"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Đang xử lý..." : "Đăng Nhập"}
          </Button>
        </form>
        <p className="mt-4 text-center text-sm">
          Chưa có tài khoản?{" "}
          <button
            type="button"
            onClick={() => navigate("/auth-register")}
            className="text-blue-600 hover:underline"
          >
            Đăng ký
          </button>
        </p>
      </div>
    </div>
  );
};

export default Login;
