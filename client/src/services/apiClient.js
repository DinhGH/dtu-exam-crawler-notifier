import axios from "axios";
import { toast } from "sonner";

const apiClient = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "https://dtu-exam-crawler-notifier.onrender.com/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor for authentication
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      "Đã có lỗi xảy ra";

    toast.error(message);

    return Promise.reject(error);
  },
);

export default apiClient;
