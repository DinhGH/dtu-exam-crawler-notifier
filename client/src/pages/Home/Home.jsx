import { Link } from "react-router-dom";
import { Button } from "../../components/ui/Button";
import { CheckCircle, FileText, Mail, ShieldCheck } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../components/ui/Card";

const Home = () => {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
          Hệ thống tự động theo dõi và thông báo{" "}
          <span className="text-blue-600">danh sách thi DTU</span>
        </h1>
        <p className="text-xl text-gray-600  mb-8 max-w-2xl mx-auto">
          Nhận thông báo ngay khi có danh sách thi mới từ Đại học Duy Tân. Tự
          động cào dữ liệu và gửi email thông báo.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link to="/register">
            <Button size="lg">Đăng ký theo dõi</Button>
          </Link>
          <Link to="/search">
            <Button variant="outline" size="lg">
              Tra cứu danh sách thi
            </Button>
          </Link>
        </div>
      </section>

      {/* Process Section */}
      <section className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">
          Quy trình hoạt động
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {[
            {
              icon: FileText,
              title: "Cào dữ liệu",
              desc: "Tự động cào dữ liệu từ website DTU",
            },
            {
              icon: FileText,
              title: "Xử lý dữ liệu",
              desc: "Phân tích và lưu vào database",
            },
            {
              icon: CheckCircle,
              title: "Đối chiếu",
              desc: "So sánh với danh sách đăng ký",
            },
            {
              icon: Mail,
              title: "Gửi Email",
              desc: "Tự động gửi thông báo qua email",
            },
          ].map((item, index) => (
            <Card key={index} className="text-center">
              <CardHeader>
                <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30">
                  <item.icon className="h-6 w-6" />
                </div>
                <CardTitle>{item.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>{item.desc}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">
          Tính năng nổi bật
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: ShieldCheck,
              title: "Tự động hóa",
              desc: "Hoạt động 24/7 mà không cần can thiệp thủ công",
            },
            {
              icon: Mail,
              title: "Thông báo ngay",
              desc: "Gửi email ngay khi có danh sách thi mới",
            },
            {
              icon: CheckCircle,
              title: "Chính xác",
              desc: "Đảm bảo dữ liệu chính xác và cập nhật",
            },
          ].map((item, index) => (
            <Card key={index}>
              <CardHeader>
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30">
                  <item.icon className="h-6 w-6" />
                </div>
                <CardTitle>{item.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>{item.desc}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Home;
