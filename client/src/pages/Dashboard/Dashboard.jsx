import { useState, useEffect } from "react";
import { dashboardService } from "../../services/dashboardService";
import { LoadingSpinner } from "../../components/ui/LoadingSpinner";
import {
  AreaChart, Area,
  BarChart, Bar,
  XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from "recharts";
import {
  FolderOpen, Users, Database,
  Clock, TrendingUp, Mail, RefreshCw,
} from "lucide-react";

// ─── Stat Card ────────────────────────────────────────────────────────────────
const StatCard = ({ icon: Icon, label, value, sub, color }) => (
  <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-5 flex items-start gap-4">
    <div className={`flex-shrink-0 w-11 h-11 rounded-lg flex items-center justify-center ${color}`}>
      <Icon className="h-5 w-5 text-white" />
    </div>
    <div className="min-w-0">
      <p className="text-sm text-gray-500 truncate">{label}</p>
      <p className="text-2xl font-bold text-gray-900 mt-0.5">
        {value !== null && value !== undefined
          ? Number(value).toLocaleString("vi-VN")
          : <span className="text-gray-300 text-lg">Đang tải...</span>}
      </p>
      {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
    </div>
  </div>
);

// ─── Custom Tooltip ───────────────────────────────────────────────────────────
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-lg px-3 py-2 text-sm">
      <p className="font-semibold text-gray-700 mb-1">{label}</p>
      {payload.map((p) => (
        <p key={p.name} style={{ color: p.color }}>
          {p.name}: <span className="font-bold">{p.value}</span>
        </p>
      ))}
    </div>
  );
};

// ─── Format ngày từ ISO sang DD/MM ───────────────────────────────────────────
const toLabel = (dateStr) => {
  if (!dateStr) return "";
  try {
    const d = new Date(dateStr);
    return `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}`;
  } catch { return dateStr; }
};

// ─── Dashboard ────────────────────────────────────────────────────────────────
const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [filesChart, setFilesChart] = useState([]);
  const [emailsChart, setEmailsChart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);

  const loadData = async (isRefresh = false) => {
    isRefresh ? setRefreshing(true) : setLoading(true);
    try {
      const [statsData, filesData, emailsData] = await Promise.all([
        dashboardService.getStats(),
        dashboardService.getFilesOverTime(),
        dashboardService.getEmailsOverTime(),
      ]);
      setStats(statsData);
      setFilesChart((filesData || []).map((d) => ({ ...d, label: toLabel(d.date) })));
      setEmailsChart((emailsData || []).map((d) => ({ ...d, label: toLabel(d.date) })));
      setLastUpdated(new Date());
    } catch (err) {
      console.error("Dashboard load error:", err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  const formatTime = (d) => {
    if (!d) return "-";
    return new Intl.DateTimeFormat("vi-VN", {
      hour: "2-digit", minute: "2-digit", second: "2-digit",
      day: "2-digit", month: "2-digit", year: "numeric",
      hour12: false,
    }).format(d);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <LoadingSpinner size={40} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900">Tổng quan hệ thống</h1>
          <p className="text-sm text-gray-500 mt-1">Theo dõi hoạt động thu thập dữ liệu và thông báo</p>
        </div>
        <div className="flex items-center gap-3">
          {lastUpdated && (
            <span className="flex items-center gap-1.5 text-xs text-gray-400">
              <Clock className="h-3.5 w-3.5" /> {formatTime(lastUpdated)}
            </span>
          )}
          <button
            onClick={() => loadData(true)}
            disabled={refreshing}
            className="inline-flex items-center gap-2 px-3 py-2 border border-gray-200 bg-white rounded-md text-sm text-gray-600 hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? "animate-spin" : ""}`} />
            Làm mới
          </button>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <StatCard
          icon={FolderOpen}
          label="Tổng số tệp đã thu thập"
          value={stats?.file_count}
          sub="Tệp danh sách thi từ website DTU"
          color="bg-blue-500"
        />
        <StatCard
          icon={Users}
          label="Sinh viên đăng ký theo dõi"
          value={stats?.subscription_count}
          sub="Lượt đăng ký nhận thông báo"
          color="bg-emerald-500"
        />
        <StatCard
          icon={Database}
          label="Tổng bản ghi lịch thi"
          value={stats?.schedule_count}
          sub="Dữ liệu đã xử lý và lưu trữ"
          color="bg-violet-500"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Tệp theo ngày */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-5">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp className="h-4 w-4 text-blue-500" />
            <h2 className="font-semibold text-gray-800">Tệp thu thập theo ngày</h2>
          </div>
          {filesChart.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={filesChart} margin={{ top: 4, right: 16, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="gradFiles" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.15} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="label" tick={{ fontSize: 11, fill: "#94a3b8" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: "#94a3b8" }} axisLine={false} tickLine={false} allowDecimals={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="count" name="Tệp" stroke="#3b82f6" strokeWidth={2} fill="url(#gradFiles)" dot={{ r: 3, fill: "#3b82f6" }} activeDot={{ r: 5 }} />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex flex-col items-center justify-center h-40 text-gray-400 gap-2">
              <TrendingUp className="h-8 w-8 opacity-30" />
              <span className="text-sm">Chưa có dữ liệu</span>
            </div>
          )}
        </div>

        {/* Email theo ngày */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-5">
          <div className="flex items-center gap-2 mb-5">
            <Mail className="h-4 w-4 text-violet-500" />
            <h2 className="font-semibold text-gray-800">Email thông báo theo ngày</h2>
          </div>
          {emailsChart.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={emailsChart} margin={{ top: 4, right: 16, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="label" tick={{ fontSize: 11, fill: "#94a3b8" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: "#94a3b8" }} axisLine={false} tickLine={false} allowDecimals={false} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" name="Email" fill="#8b5cf6" radius={[4, 4, 0, 0]} maxBarSize={40} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex flex-col items-center justify-center h-40 text-gray-400 gap-2">
              <Mail className="h-8 w-8 opacity-30" />
              <span className="text-sm">Chưa có dữ liệu</span>
            </div>
          )}
        </div>
      </div>

      {/* Thông tin thu thập gần nhất */}
      {stats?.latest_crawl_time && (
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
          <div className="flex items-center gap-3 text-sm text-gray-600">
            <Clock className="h-4 w-4 text-blue-500 flex-shrink-0" />
            <span>
              Lần thu thập dữ liệu gần nhất:{" "}
              <span className="font-semibold text-gray-900">
                {new Intl.DateTimeFormat("vi-VN", {
                  timeZone: "Asia/Ho_Chi_Minh",
                  day: "2-digit", month: "2-digit", year: "numeric",
                  hour: "2-digit", minute: "2-digit", hour12: false,
                }).format(new Date(stats.latest_crawl_time))}
              </span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
