import { useNavigate } from "react-router-dom";
import { 
  Activity, Search, ShieldCheck, 
  FileText, Users, MailCheck, Clock, 
  DownloadCloud, ClipboardEdit, SearchCheck, Send,
  ChevronRight, CheckCircle2
} from "lucide-react";

// ==========================================
// COMPONENTS PHỤ TRỢ (UI KIT)
// ==========================================

const Navbar = () => {
  const navigate = useNavigate();
  return (
    <nav className="fixed top-0 left-0 right-0 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate("/")}>
            <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center text-white font-bold shadow-md">
              <Activity size={18} />
            </div>
            <span className="font-bold text-xl text-white tracking-tight">DTU Tracker</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <button onClick={() => navigate("/")} className="text-blue-400 font-semibold">Trang chủ</button>
            <button onClick={() => navigate("/tra-cuu")} className="text-slate-300 hover:text-white font-medium transition-colors">Tra cứu</button>
            <button onClick={() => navigate("/dang-ky")} className="text-slate-300 hover:text-white font-medium transition-colors">Đăng ký</button>
          </div>
          <div>
            <button className="bg-blue-600 hover:bg-blue-500 text-white px-5 py-2.5 rounded-lg text-sm font-semibold transition-all shadow-md flex items-center gap-2">
              Đăng nhập <ChevronRight size={16} />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

const StatItem = ({ count, title, desc, icon: Icon, bgClass }) => (
  <div className={`${bgClass} p-6 rounded-xl shadow-md hover:-translate-y-2 hover:shadow-lg transition-all duration-300 group overflow-hidden relative text-white border border-white/10`}>
    <Icon size={120} className="absolute -bottom-6 -right-6 opacity-20 transform group-hover:scale-110 group-hover:-rotate-12 transition-all duration-500" />
    <div className="relative z-10">
      <div className="flex items-start justify-between mb-2">
        <span className="text-4xl font-extrabold tracking-tight drop-shadow-sm">{count}</span>
        <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
          <Icon size={24} className="text-white" />
        </div>
      </div>
      <h3 className="text-lg font-bold mb-1 drop-shadow-sm">{title}</h3>
      <p className="text-sm font-medium text-white/90 drop-shadow-sm">{desc}</p>
    </div>
  </div>
);

const StepCard = ({ step, title, desc, icon: Icon, theme, hasArrow }) => {
  const themeStyles = {
    emerald: {
      wrapper: "bg-emerald-50 border-emerald-300 hover:border-emerald-400 hover:shadow-emerald-200",
      icon: "bg-emerald-100 text-emerald-600",
      title: "text-emerald-800",
      number: "text-emerald-400",
      arrowHover: "group-hover:text-emerald-600 group-hover:border-emerald-400"
    },
    sky: {
      wrapper: "bg-sky-50 border-sky-300 hover:border-sky-400 hover:shadow-sky-200",
      icon: "bg-sky-100 text-sky-600",
      title: "text-sky-800",
      number: "text-sky-400",
      arrowHover: "group-hover:text-sky-600 group-hover:border-sky-400"
    },
    amber: {
      wrapper: "bg-amber-50 border-amber-300 hover:border-amber-400 hover:shadow-amber-200",
      icon: "bg-amber-100 text-amber-600",
      title: "text-amber-800",
      number: "text-amber-400",
      arrowHover: "group-hover:text-amber-600 group-hover:border-amber-400"
    },
    rose: {
      wrapper: "bg-rose-50 border-rose-300 hover:border-rose-400 hover:shadow-rose-200",
      icon: "bg-rose-100 text-rose-600",
      title: "text-rose-800",
      number: "text-rose-400",
      arrowHover: ""
    }
  };

  const currentTheme = themeStyles[theme];

  return (
    <div className={`relative p-8 rounded-2xl border-2 shadow-sm hover:-translate-y-2 hover:shadow-xl transition-all duration-300 group z-10 ${currentTheme.wrapper}`}>
      
      <div className="flex justify-between items-start mb-6">
        <div className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110 shadow-sm ${currentTheme.icon}`}>
          <Icon size={28} />
        </div>
        <span className={`text-4xl font-black transition-colors duration-300 ${currentTheme.number}`}>
          0{step}
        </span>
      </div>
      
      {hasArrow && (
        <div className={`hidden lg:flex absolute top-1/2 -right-8 -translate-y-1/2 z-20 items-center justify-center w-12 h-12 bg-white rounded-full border-2 border-slate-200 shadow-md text-slate-300 transition-colors duration-300 ${currentTheme.arrowHover}`}>
          <ChevronRight size={24} />
        </div>
      )}
      
      <h4 className={`text-xl font-bold mb-3 ${currentTheme.title}`}>{title}</h4>
      <p className="text-sm text-slate-700 leading-relaxed">{desc}</p>
    </div>
  );
};

// ==========================================
// TRANG CHỦ (MAIN PAGE)
// ==========================================

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-50 font-sans selection:bg-blue-200 selection:text-blue-900">
      <Navbar />

      {/* HERO SECTION */}
      <section className="relative pt-32 pb-36 bg-gradient-to-b from-blue-950 via-slate-900 to-slate-900 overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03]"></div>
        <div className="absolute top-0 right-0 -mr-40 -mt-40 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute bottom-0 left-20 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="flex flex-col lg:flex-row items-center gap-16">
            
            <div className="flex-1 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-800/80 border border-slate-700 text-sm font-medium mb-8 text-slate-300 shadow-sm backdrop-blur-sm">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
                Hệ thống đang hoạt động ổn định
              </div>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-white tracking-tight mb-6 leading-[1.1]">
                Tự Động Theo Dõi <br />
                <span className="text-blue-400">Danh Sách Thi DTU</span>
              </h1>
              <p className="text-lg text-slate-400 mb-10 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
                Giải pháp SaaS giúp sinh viên không bỏ lỡ lịch thi. Đăng ký thông tin một lần, hệ thống sẽ tự động quét và gửi cảnh báo trực tiếp qua Email của bạn ngay khi có dữ liệu mới.
              </p>
              <div className="flex flex-col sm:flex-row justify-center lg:justify-start gap-4">
                <button onClick={() => navigate("/dang-ky")} className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-xl font-bold shadow-[0_4px_14px_0_rgba(37,99,235,0.39)] hover:-translate-y-1 transition-all flex items-center justify-center gap-2">
                  Bắt Đầu Đăng Ký <ChevronRight size={20} />
                </button>
                <button onClick={() => navigate("/tra-cuu")} className="bg-slate-800/80 hover:bg-slate-700 text-white border border-slate-700 shadow-sm px-8 py-4 rounded-xl font-bold transition-all flex items-center justify-center gap-2 backdrop-blur-sm">
                  <Search size={20} /> Tra Cứu Dữ Liệu
                </button>
              </div>
            </div>

            <div className="flex-1 w-full max-w-2xl">
              <div className="bg-slate-900 rounded-2xl border border-slate-700 shadow-2xl overflow-hidden transform lg:rotate-y-[-5deg] lg:rotate-x-[2deg] hover:rotate-0 transition-transform duration-500">
                <div className="bg-slate-800 px-4 py-3 border-b border-slate-700/80 flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-rose-500"></div>
                    <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                    <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                  </div>
                  <div className="mx-auto bg-slate-900 px-4 py-1 rounded-md text-xs text-slate-400 border border-slate-700/80 flex items-center gap-2">
                    <ShieldCheck size={14} className="text-emerald-400"/> dtu-tracker.com/dashboard
                  </div>
                </div>
                <div className="p-5">
                  <div className="flex justify-between items-end mb-6">
                    <div>
                      <h3 className="text-white font-semibold text-lg">Luồng Hoạt Động Gần Nhất</h3>
                      <p className="text-slate-400 text-sm">Cập nhật 1 phút trước</p>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-slate-800/60 rounded-xl border border-slate-700/60">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-500/20 text-blue-400 rounded-lg"><FileText size={18} /></div>
                        <div>
                          <p className="text-slate-200 text-sm font-medium">CNT101_Midterm.pdf</p>
                          <p className="text-slate-400 text-xs">Phát hiện 2 khớp lệnh</p>
                        </div>
                      </div>
                      <span className="flex items-center gap-1 text-xs font-medium px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-md border border-emerald-500/20">
                        <CheckCircle2 size={12}/> Đã gửi Email
                      </span>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-slate-800/60 rounded-xl border border-slate-700/60">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-500/20 text-blue-400 rounded-lg"><FileText size={18} /></div>
                        <div>
                          <p className="text-slate-200 text-sm font-medium">PHY102_Final.xlsx</p>
                          <p className="text-slate-400 text-xs">Đang phân tích dữ liệu...</p>
                        </div>
                      </div>
                      <span className="flex items-center gap-1 text-xs font-medium px-2.5 py-1 bg-amber-500/10 text-amber-400 rounded-md border border-amber-500/20">
                        <Activity size={12} className="animate-spin"/> Đang xử lý
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* STATISTICS SECTION */}
      <section className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatItem 
            bgClass="bg-emerald-400"
            icon={FileText} count="124+" title="Tệp Thu Thập" desc="Được lưu trữ an toàn"
          />
          <StatItem 
            bgClass="bg-sky-400"
            icon={Users} count="430+" title="Sinh Viên" desc="Đã đăng ký hệ thống"
          />
          <StatItem 
            bgClass="bg-amber-400"
            icon={MailCheck} count="58+" title="Email Đã Gửi" desc="Thông báo thành công"
          />
          <StatItem 
            bgClass="bg-rose-400"
            icon={Clock} count="24/7" title="Tự Động Hóa" desc="Quét dữ liệu mỗi giờ"
          />
        </div>
      </section>

      {/* WORKFLOW SECTION */}
      <section className="py-24 bg-slate-50 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* ĐÃ FIX: Tiêu đề to hơn, mô tả in đậm và có màu */}
          <div className="text-center max-w-4xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-sm font-bold tracking-wide uppercase mb-6 shadow-sm">
              <Activity size={16} /> Workflow
            </div>
            
            {/* Tăng kích thước chữ lên text-5xl/6xl/7xl */}
            <h2 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-slate-900 mb-8 tracking-tight">
              Quy Trình <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Tự Động Hóa</span>
            </h2>
            
            {/* Đổi màu khung, màu chữ và làm đậm text */}
            <div className="bg-blue-50/80 backdrop-blur-sm border border-blue-200 px-8 py-5 rounded-2xl shadow-md inline-block">
              <p className="text-xl font-bold text-blue-800 leading-relaxed">
                Hệ thống thực hiện toàn bộ quy trình một cách khép kín từ khâu thu thập dữ liệu thô đến khi thông báo nằm gọn trong hộp thư của bạn.
              </p>
            </div>
          </div>
          
          <div className="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-slate-100 p-8 md:p-12 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-blue-50 rounded-full mix-blend-multiply filter blur-3xl opacity-50 -translate-y-1/2 translate-x-1/2"></div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative z-10">
              <StepCard 
                step="1" icon={DownloadCloud} hasArrow={true} theme="emerald"
                title="Cào Dữ Liệu" 
                desc="Tự động quét website đào tạo của DTU định kỳ để tải về các tệp lịch thi mới nhất." 
              />
              <StepCard 
                step="2" icon={ClipboardEdit} hasArrow={true} theme="sky"
                title="Ghi Nhận" 
                desc="Sinh viên cung cấp mã môn học, họ tên và Email thông qua biểu mẫu được bảo mật." 
              />
              <StepCard 
                step="3" icon={SearchCheck} hasArrow={true} theme="amber"
                title="So Khớp Thông Tin" 
                desc="Thuật toán phân tích và đối chiếu thông tin của bạn với hàng ngàn dữ liệu trong tệp." 
              />
              <StepCard 
                step="4" icon={Send} hasArrow={false} theme="rose"
                title="Gửi Thông Báo" 
                desc="Gửi Email tức thời kèm nội dung chi tiết về phòng thi, ngày giờ và đính kèm tệp gốc." 
              />
            </div>
          </div>

        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-slate-900 pt-16 pb-8 text-slate-400 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center pb-8 border-b border-slate-800/50">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center text-white font-bold text-sm">DT</div>
              <span className="font-bold text-xl text-white tracking-tight">DTU Tracker</span>
            </div>
            <div className="flex gap-6 text-sm">
              <button onClick={() => navigate("/tra-cuu")} className="hover:text-white transition-colors">Tra Cứu</button>
              <button onClick={() => navigate("/dang-ky")} className="hover:text-white transition-colors">Đăng Ký</button>
            </div>
          </div>
          <div className="text-center text-sm mt-8 flex flex-col sm:flex-row justify-between items-center">
            <p>© 2026 DTU Exam Crawler Notifier. All rights reserved.</p>
            <p className="mt-2 sm:mt-0 flex items-center gap-1">
              Phát triển bởi <span className="text-slate-200 font-medium">Tin</span>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}