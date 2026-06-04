import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { 
  Activity, ChevronRight, User, Mail, 
  Hash, BookOpen, AlertCircle, Loader2, CheckCircle2, ArrowLeft, ShieldCheck // <-- Đã thêm ShieldCheck vào đây
} from "lucide-react";

// ==========================================
// 1. KHỞI TẠO SCHEMA KIỂM TRA DỮ LIỆU
// ==========================================
const registerSchema = z.object({
  fullName: z.string().min(2, "Họ và tên phải có ít nhất 2 ký tự"),
  email: z.string().email("Vui lòng nhập đúng định dạng Email (VD: abc@dtu.edu.vn)"),
  subjectCode: z.string().min(3, "Mã môn học không hợp lệ (VD: CS101)"),
  subjectName: z.string().min(3, "Tên môn học không hợp lệ (VD: Software Engineering)")
});

// ==========================================
// 2. COMPONENT NAVBAR
// ==========================================
const Navbar = () => {
  const navigate = useNavigate();
  return (
    <nav className="fixed top-0 left-0 right-0 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate("/")}>
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold shadow-md">
              <Activity size={18} />
            </div>
            <span className="font-bold text-xl text-white tracking-tight">DTU Tracker</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <button onClick={() => navigate("/")} className="text-slate-300 hover:text-white font-medium transition-colors">Trang chủ</button>
            <button onClick={() => navigate("/tra-cuu")} className="text-slate-300 hover:text-white font-medium transition-colors">Tra cứu</button>
            <button onClick={() => navigate("/dang-ky")} className="text-blue-400 font-semibold">Đăng ký</button>
          </div>
        </div>
      </div>
    </nav>
  );
};

// ==========================================
// 3. TRANG ĐĂNG KÝ CHÍNH
// ==========================================
export default function RegisterPage() {
  const navigate = useNavigate();
  const [isSuccess, setIsSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data) => {
    console.log("Dữ liệu gửi đi:", data);
    await new Promise((resolve) => setTimeout(resolve, 1500));
    setIsSuccess(true);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col font-sans selection:bg-blue-200 selection:text-blue-900 relative overflow-hidden">
      
      {/* Background Decorators */}
      <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03]"></div>
      <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-blue-600/20 rounded-full mix-blend-screen filter blur-[100px] animate-blob pointer-events-none"></div>
      <div className="absolute bottom-[-10%] left-[-5%] w-[600px] h-[600px] bg-indigo-600/10 rounded-full mix-blend-screen filter blur-[120px] animate-blob animation-delay-2000 pointer-events-none"></div>

      <Navbar />

      <main className="flex-grow pt-28 pb-12 px-4 sm:px-6 lg:px-8 flex items-center justify-center relative z-10">
        
        <div className="max-w-[1000px] w-full bg-white rounded-[2.5rem] shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)] overflow-hidden flex flex-col lg:flex-row border border-slate-700/30">
          
          {/* CỘT TRÁI: Branding */}
          <div className="lg:w-5/12 relative bg-gradient-to-br from-slate-800 via-slate-900 to-blue-950 p-10 lg:p-12 flex flex-col justify-between overflow-hidden">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
            
            <div className="relative z-10">
              <button 
                onClick={() => navigate("/")}
                className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors text-sm font-medium mb-12 group"
              >
                <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" /> Quay lại trang chủ
              </button>
              
              <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-6 leading-tight tracking-tight">
                Đăng Ký Theo Dõi <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">
                  Danh Sách Thi
                </span>
              </h2>
              <p className="text-slate-400 leading-relaxed mb-10 text-sm md:text-base">
                Chỉ cần điền thông tin một lần, hệ thống thông minh của chúng tôi sẽ hoạt động ngầm 24/7 để báo tin cho bạn sớm nhất.
              </p>

              <div className="space-y-5">
                <div className="flex items-center gap-4 text-slate-300 bg-slate-800/40 p-3.5 rounded-2xl border border-slate-700/50 backdrop-blur-sm">
                  <div className="bg-emerald-500/20 p-2 rounded-xl text-emerald-400">
                    <CheckCircle2 size={20} />
                  </div>
                  <span className="font-medium text-sm">Hoàn toàn tự động 24/7</span>
                </div>
                <div className="flex items-center gap-4 text-slate-300 bg-slate-800/40 p-3.5 rounded-2xl border border-slate-700/50 backdrop-blur-sm">
                  <div className="bg-blue-500/20 p-2 rounded-xl text-blue-400">
                    <Mail size={20} />
                  </div>
                  <span className="font-medium text-sm">Nhận thông báo qua Email</span>
                </div>
                <div className="flex items-center gap-4 text-slate-300 bg-slate-800/40 p-3.5 rounded-2xl border border-slate-700/50 backdrop-blur-sm">
                  <div className="bg-amber-500/20 p-2 rounded-xl text-amber-400">
                    <ShieldCheck size={20} />
                  </div>
                  <span className="font-medium text-sm">Bảo mật thông tin tối đa</span>
                </div>
              </div>
            </div>
          </div>

          {/* CỘT PHẢI: Form */}
          <div className="lg:w-7/12 p-10 lg:p-14 bg-white relative">
            {!isSuccess ? (
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="mb-8">
                  <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight">Thông tin sinh viên</h3>
                  <p className="text-slate-500 text-sm mt-2">Vui lòng nhập chính xác để hệ thống có thể đối chiếu dữ liệu.</p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-2">Họ và tên</label>
                    <div className="relative group">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 group-focus-within:text-blue-600 transition-colors">
                        <User size={18} />
                      </div>
                      <input
                        type="text"
                        placeholder="VD: Nguyễn Văn A"
                        {...register("fullName")}
                        className={`w-full pl-11 pr-4 py-3.5 bg-slate-50 border rounded-xl outline-none transition-all text-slate-700 font-medium placeholder:font-normal placeholder:text-slate-400 ${
                          errors.fullName 
                            ? "border-red-400 focus:bg-white focus:border-red-500 focus:ring-[4px] focus:ring-red-500/15" 
                            : "border-slate-200 focus:bg-white focus:border-blue-500 focus:ring-[4px] focus:ring-blue-500/15 hover:border-slate-300 shadow-sm"
                        }`}
                      />
                    </div>
                    {errors.fullName && (
                      <p className="mt-2 text-sm text-red-500 flex items-center gap-1.5 font-medium animate-in slide-in-from-top-1">
                        <AlertCircle size={14} /> {errors.fullName.message}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-2">Địa chỉ Email</label>
                    <div className="relative group">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 group-focus-within:text-blue-600 transition-colors">
                        <Mail size={18} />
                      </div>
                      <input
                        type="text"
                        placeholder="VD: sinhvien@dtu.edu.vn"
                        {...register("email")}
                        className={`w-full pl-11 pr-4 py-3.5 bg-slate-50 border rounded-xl outline-none transition-all text-slate-700 font-medium placeholder:font-normal placeholder:text-slate-400 ${
                          errors.email 
                            ? "border-red-400 focus:bg-white focus:border-red-500 focus:ring-[4px] focus:ring-red-500/15" 
                            : "border-slate-200 focus:bg-white focus:border-blue-500 focus:ring-[4px] focus:ring-blue-500/15 hover:border-slate-300 shadow-sm"
                        }`}
                      />
                    </div>
                    {errors.email && (
                      <p className="mt-2 text-sm text-red-500 flex items-center gap-1.5 font-medium animate-in slide-in-from-top-1">
                        <AlertCircle size={14} /> {errors.email.message}
                      </p>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Mã môn học</label>
                      <div className="relative group">
                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 group-focus-within:text-blue-600 transition-colors">
                          <Hash size={18} />
                        </div>
                        <input
                          type="text"
                          placeholder="VD: CNT101"
                          {...register("subjectCode")}
                          className={`w-full pl-11 pr-4 py-3.5 uppercase bg-slate-50 border rounded-xl outline-none transition-all text-slate-700 font-medium placeholder:font-normal placeholder:text-slate-400 ${
                            errors.subjectCode 
                              ? "border-red-400 focus:bg-white focus:border-red-500 focus:ring-[4px] focus:ring-red-500/15" 
                              : "border-slate-200 focus:bg-white focus:border-blue-500 focus:ring-[4px] focus:ring-blue-500/15 hover:border-slate-300 shadow-sm"
                          }`}
                        />
                      </div>
                      {errors.subjectCode && (
                        <p className="mt-2 text-sm text-red-500 flex items-center gap-1.5 font-medium animate-in slide-in-from-top-1">
                          <AlertCircle size={14} /> {errors.subjectCode.message}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Tên môn học</label>
                      <div className="relative group">
                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 group-focus-within:text-blue-600 transition-colors">
                          <BookOpen size={18} />
                        </div>
                        <input
                          type="text"
                          placeholder="VD: Nhập môn lập trình"
                          {...register("subjectName")}
                          className={`w-full pl-11 pr-4 py-3.5 bg-slate-50 border rounded-xl outline-none transition-all text-slate-700 font-medium placeholder:font-normal placeholder:text-slate-400 ${
                            errors.subjectName 
                              ? "border-red-400 focus:bg-white focus:border-red-500 focus:ring-[4px] focus:ring-red-500/15" 
                              : "border-slate-200 focus:bg-white focus:border-blue-500 focus:ring-[4px] focus:ring-blue-500/15 hover:border-slate-300 shadow-sm"
                          }`}
                        />
                      </div>
                      {errors.subjectName && (
                        <p className="mt-2 text-sm text-red-500 flex items-center gap-1.5 font-medium animate-in slide-in-from-top-1">
                          <AlertCircle size={14} /> {errors.subjectName.message}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="pt-6">
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 px-4 rounded-xl transition-all duration-300 shadow-[0_8px_15px_rgba(37,99,235,0.2)] hover:shadow-[0_15px_25px_rgba(37,99,235,0.4)] hover:-translate-y-1 flex justify-center items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none"
                    >
                      {isSubmitting ? (
                        <>
                          <Loader2 size={20} className="animate-spin" /> Đang thiết lập theo dõi...
                        </>
                      ) : (
                        <>
                          Xác Nhận Đăng Ký <ChevronRight size={20} />
                        </>
                      )}
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center animate-in zoom-in-95 duration-500 p-8">
                <div className="w-24 h-24 bg-emerald-100 rounded-full flex items-center justify-center mb-8 shadow-inner relative">
                  <div className="absolute inset-0 bg-emerald-400 rounded-full animate-ping opacity-20"></div>
                  <CheckCircle2 size={48} className="text-emerald-500 relative z-10" />
                </div>
                <h3 className="text-3xl font-extrabold text-slate-900 mb-4 tracking-tight">Thành Công Tuyệt Đối!</h3>
                <p className="text-slate-600 mb-10 max-w-sm text-lg">
                  Hệ thống đã ghi nhận thông tin. Bạn có thể yên tâm làm việc khác, Email thông báo sẽ được gửi đi ngay khi có dữ liệu mới.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 w-full justify-center">
                  <button 
                    onClick={() => setIsSuccess(false)}
                    className="px-8 py-3.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl transition-colors w-full sm:w-auto"
                  >
                    Thêm môn khác
                  </button>
                  <button 
                    onClick={() => navigate("/")}
                    className="px-8 py-3.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl transition-all shadow-[0_8px_15px_rgba(37,99,235,0.2)] hover:shadow-[0_12px_20px_rgba(37,99,235,0.4)] hover:-translate-y-0.5 w-full sm:w-auto"
                  >
                    Về trang chủ
                  </button>
                </div>
              </div>
            )}
            
          </div>
        </div>
      </main>
    </div>
  );
}