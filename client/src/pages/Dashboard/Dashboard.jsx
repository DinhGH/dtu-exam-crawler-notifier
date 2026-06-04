import { useState, useEffect } from "react";
import { dashboardService } from "../../services/dashboardService";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../components/ui/Card";
import { LoadingSpinner } from "../../components/ui/LoadingSpinner";
import { EmptyState } from "../../components/ui/EmptyState";
import { FileText, Mail, Users, Activity } from "lucide-react";

function StatCard({ title, value, icon: Icon, description }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <div className="rounded-full bg-blue-100 p-2 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
          <Icon className="h-5 w-5" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value ?? "-"}</div>
        <p className="text-xs text-gray-500 dark:text-gray-400">
          {description}
        </p>
      </CardContent>
    </Card>
  );
}

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [filesOverTime, setFilesOverTime] = useState([]);
  const [emailsOverTime, setEmailsOverTime] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    setLoading(true);
    try {
      const [statsData, filesData, emailsData] = await Promise.all([
        dashboardService.getStats(),
        dashboardService.getFilesOverTime(),
        dashboardService.getEmailsOverTime(),
      ]);
      setStats(statsData);
      setFilesOverTime(filesData || []);
      setEmailsOverTime(emailsData || []);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12 flex justify-center">
        <LoadingSpinner size={48} />
      </div>
    );
  }

  if (!stats || Object.keys(stats).length === 0) {
    return (
      <div className="container mx-auto px-4 py-12">
        <EmptyState
          icon={Activity}
          title="Không có dữ liệu"
          description="Hiện chưa có thống kê nào. Vui lòng quay lại sau."
          action={
            <button
              onClick={fetchData}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Thử lại
            </button>
          }
        />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-6">
        Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          title="Tổng danh sách thi"
          value={stats.total_files ?? "-"}
          icon={FileText}
          description="Tổng số file danh sách thi đã cào"
        />
        <StatCard
          title="Tổng lượt đăng ký"
          value={stats.total_subscriptions ?? "-"}
          icon={Users}
          description="Người dùng đăng ký theo dõi"
        />
        <StatCard
          title="Email đã gửi"
          value={stats.total_emails ?? "-"}
          icon={Mail}
          description="Tổng số email thông báo đã gửi"
        />
        <StatCard
          title="Tỷ lệ thành công"
          value={stats.success_rate ? `${stats.success_rate}%` : "-"}
          icon={Activity}
          description="Tỷ lệ gửi email thành công"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>File được thêm theo thời gian</CardTitle>
            <CardDescription>Thống kê số file mới theo ngày</CardDescription>
          </CardHeader>
          <CardContent>
            {filesOverTime.length > 0 ? (
              <div className="space-y-3">
                {filesOverTime.slice(0, 7).map((item, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {item.date || "Unknown"}
                    </span>
                    <div className="flex items-center gap-3">
                      <div className="h-2 w-24 bg-gray-200 dark:bg-gray-700 rounded overflow-hidden">
                        <div
                          className="h-full bg-blue-600"
                          style={{
                            width: `${Math.min(
                              (item.count /
                                (Math.max(
                                  ...filesOverTime.map((x) => x.count),
                                ) || 1)) *
                                100,
                              100,
                            )}%`,
                          }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {item.count}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 dark:text-gray-400">
                Không có dữ liệu
              </p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Email đã gửi theo thời gian</CardTitle>
            <CardDescription>
              Thống kê số email đã gửi theo ngày
            </CardDescription>
          </CardHeader>
          <CardContent>
            {emailsOverTime.length > 0 ? (
              <div className="space-y-3">
                {emailsOverTime.slice(0, 7).map((item, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {item.date || "Unknown"}
                    </span>
                    <div className="flex items-center gap-3">
                      <div className="h-2 w-24 bg-gray-200 dark:bg-gray-700 rounded overflow-hidden">
                        <div
                          className="h-full bg-green-600"
                          style={{
                            width: `${Math.min(
                              (item.count /
                                (Math.max(
                                  ...emailsOverTime.map((x) => x.count),
                                ) || 1)) *
                                100,
                              100,
                            )}%`,
                          }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {item.count}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 dark:text-gray-400">
                Không có dữ liệu
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
