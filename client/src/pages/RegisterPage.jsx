import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  AlertCircle,
  Bell,
  BookOpen,
  CheckCircle2,
  Edit3,
  Hash,
  Loader2,
  Mail,
  Menu,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Trash2,
  User,
} from "lucide-react";

const registerSchema = z.object({
  fullName: z.string().trim().min(2, "Họ và tên phải có ít nhất 2 ký tự"),
  email: z.string().trim().email("Email chưa đúng định dạng, ví dụ: abc@dtu.edu.vn"),
  subjectCode: z
    .string()
    .trim()
    .min(3, "Mã môn học phải có ít nhất 3 ký tự")
    .regex(/^[A-Za-z]{2,5}\s?\d{2,4}[A-Za-z]?$/, "Mã môn học chưa đúng, ví dụ: CS 466"),
  subjectName: z.string().trim().min(3, "Tên môn học phải có ít nhất 3 ký tự"),
});

const initialSubscriptions = [
  { id: 31, fullName: "Dương Văn Bảo", email: "huynhdinh2k52707@gmail.com", subjectCode: "TOU 361" },
  { id: 32, fullName: "Dương Văn Bảo", email: "huynhdinh2k52707@gmail.com", subjectCode: "TOU 361" },
  { id: 33, fullName: "Dương Văn Bảo", email: "huynhdinh2k52707@gmail.com", subjectCode: "TOU 361" },
  { id: 34, fullName: "Nguyễn Kim Diệu", email: "huynhdinh2k52707@gmail.com", subjectCode: "KOR 206" },
  { id: 35, fullName: "Phan Văn An", email: "huynhdinh2k52707@gmail.com", subjectCode: "OB 253" },
  { id: 36, fullName: "Lê Ngọc Anh", email: "huynhdinh2k52707@gmail.com", subjectCode: "KOR 206" },
  { id: 37, fullName: "Phan Văn An", email: "huynhdinh2k52707@gmail.com", subjectCode: "OB 253" },
  { id: 38, fullName: "Nguyễn Thị Hoa", email: "student.hoa@dtu.edu.vn", subjectCode: "CS 201" },
  { id: 39, fullName: "Trần Minh Quân", email: "quan.tran@dtu.edu.vn", subjectCode: "ENG 302" },
];

const initials = (name) =>
  name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(-2)
    .toUpperCase();

const Navbar = ({ active = "register" }) => {
  const navigate = useNavigate();

  const navItemClass = (name) =>
    `relative rounded-full px-4 py-2 text-sm font-extrabold transition duration-200 ${
      active === name
        ? "bg-blue-600 text-white shadow-[0_10px_22px_rgba(37,99,235,0.28)]"
        : "text-slate-600 hover:bg-slate-100 hover:text-slate-950"
    }`;

  return (
    <nav className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/85 shadow-[0_8px_30px_rgba(15,23,42,0.06)] backdrop-blur-xl">
      <div className="mx-auto flex h-18 max-w-[1680px] items-center justify-between px-5 sm:px-8">
        <button
          type="button"
          onClick={() => navigate("/")}
          className="group flex items-center gap-3"
        >
          <span className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-blue-600 via-cyan-500 to-emerald-400 text-white shadow-[0_12px_24px_rgba(37,99,235,0.26)] transition group-hover:-translate-y-0.5">
            <Sparkles size={20} />
          </span>
          <span className="text-left">
            <span className="block text-lg font-black tracking-tight text-slate-950">
              DTU Exam Notifier
            </span>
            <span className="block text-xs font-bold uppercase tracking-[0.16em] text-slate-400">
              Exam tracking
            </span>
          </span>
        </button>

        <div className="flex items-center gap-2 sm:gap-3">
          <button
            type="button"
            onClick={() => navigate("/dang-ky")}
            className={navItemClass("register")}
          >
            Đăng ký theo dõi
          </button>
          <button
            type="button"
            onClick={() => navigate("/tra-cuu")}
            className={navItemClass("search")}
          >
            Danh sách tệp
          </button>
          <button
            type="button"
            className="hidden h-10 w-10 place-items-center rounded-full border border-slate-200 bg-white text-slate-500 shadow-sm transition hover:-translate-y-0.5 hover:text-blue-700 sm:grid"
            aria-label="Thông báo"
          >
            <Bell size={18} />
          </button>
          <button
            type="button"
            className="grid h-10 w-10 place-items-center rounded-full bg-slate-950 text-white shadow-sm transition hover:-translate-y-0.5 hover:bg-blue-700"
            aria-label="Menu"
          >
            <Menu size={18} />
          </button>
        </div>
      </div>
    </nav>
  );
};

const PageShell = ({ children }) => (
  <div className="min-h-screen bg-[#eef3f8] text-slate-950">
    <div className="pointer-events-none fixed inset-0 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_12%_12%,rgba(14,165,233,0.18),transparent_30%),radial-gradient(circle_at_86%_18%,rgba(16,185,129,0.16),transparent_28%),linear-gradient(90deg,rgba(15,23,42,0.045)_1px,transparent_1px),linear-gradient(180deg,rgba(15,23,42,0.045)_1px,transparent_1px)] bg-[length:100%_100%,100%_100%,38px_38px,38px_38px]" />
      <div className="absolute left-0 top-0 h-full w-[92px] border-r border-white/70 bg-white/45 shadow-[12px_0_40px_rgba(15,23,42,0.05)]" />
      <div className="absolute left-[92px] right-0 top-20 h-44 bg-gradient-to-r from-blue-600/10 via-white/20 to-emerald-400/10" />
    </div>
    <div className="relative z-10 flex min-h-screen flex-col">
      {children}
      <footer className="mt-auto border-t border-white/80 bg-white/60 py-6 text-center text-sm font-semibold text-slate-500 backdrop-blur">
        © 2026 DTU Exam Notifier. All rights reserved.
      </footer>
    </div>
  </div>
);

const Metric = ({ value, label, tone }) => (
  <div className="rounded-lg border border-white/70 bg-white/65 px-4 py-3 shadow-sm">
    <p className={`text-2xl font-black ${tone}`}>{value}</p>
    <p className="mt-1 text-xs font-bold uppercase tracking-[0.12em] text-slate-400">{label}</p>
  </div>
);

const Field = ({ icon: Icon, label, error, children }) => (
  <label className="block">
    <span className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-[0.11em] text-slate-600">
      <Icon size={15} className={error ? "text-rose-500" : "text-blue-600"} />
      {label}
    </span>
    {children}
    {error && (
      <span className="mt-2 flex items-center gap-1.5 text-sm font-bold text-rose-600">
        <AlertCircle size={15} />
        {error.message}
      </span>
    )}
  </label>
);

const inputClass = (hasError) =>
  `h-[52px] w-full rounded-lg border bg-slate-50/80 px-4 text-[15px] font-bold text-slate-800 outline-none shadow-inner transition duration-200 placeholder:font-semibold placeholder:text-slate-400 ${
    hasError
      ? "border-rose-300 focus:border-rose-500 focus:bg-white focus:ring-4 focus:ring-rose-100"
      : "border-slate-200 hover:border-blue-300 hover:bg-white focus:border-blue-600 focus:bg-white focus:ring-4 focus:ring-blue-100"
  }`;

export default function RegisterPage() {
  const [subscriptions, setSubscriptions] = useState(initialSubscriptions);
  const [isSuccess, setIsSuccess] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      fullName: "",
      email: "",
      subjectCode: "",
      subjectName: "",
    },
  });

  const totalSubscriptions = useMemo(() => subscriptions.length, [subscriptions]);

  const onSubmit = async (data) => {
    await new Promise((resolve) => setTimeout(resolve, 650));
    const nextRow = {
      id: Math.max(...subscriptions.map((item) => item.id)) + 1,
      fullName: data.fullName.trim(),
      email: data.email.trim(),
      subjectCode: data.subjectCode.trim().toUpperCase(),
    };
    setSubscriptions((current) => [nextRow, ...current]);
    setIsSuccess(true);
    reset();
  };

  const handleRefresh = () => {
    setIsRefreshing(true);
    window.setTimeout(() => setIsRefreshing(false), 600);
  };

  return (
    <PageShell>
      <Navbar />

      <main className="flex-1 px-5 py-8 sm:px-8">
        <div className="mx-auto grid max-w-[1680px] gap-7 xl:grid-cols-[0.92fr_1.32fr]">
          <section className="overflow-hidden rounded-xl border border-white/80 bg-white/82 shadow-[0_18px_55px_rgba(15,23,42,0.11)] backdrop-blur-xl">
            <div className="relative overflow-hidden border-b border-slate-200/80 bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900 px-6 py-7 text-white">
              <div className="absolute -right-12 -top-16 h-44 w-44 rounded-full bg-cyan-400/20 blur-2xl" />
              <div className="absolute bottom-0 left-0 h-1 w-full bg-gradient-to-r from-blue-500 via-cyan-400 to-emerald-400" />
              <div className="relative flex items-center gap-3">
                <span className="grid h-11 w-11 place-items-center rounded-xl bg-white/12 text-cyan-200 ring-1 ring-white/15">
                  <ShieldCheck size={22} />
                </span>
                <div>
                  <h1 className="text-2xl font-black tracking-tight">Đăng ký nhận lịch thi</h1>
                  <p className="mt-1 text-sm font-medium text-slate-300">
                    Nhập thông tin để hệ thống tự động gửi email khi có danh sách thi mới.
                  </p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 border-b border-slate-100 bg-slate-50/70 p-5">
              <Metric value={totalSubscriptions} label="Theo dõi" tone="text-blue-600" />
              <Metric value="24/7" label="Giám sát" tone="text-emerald-600" />
              <Metric value="Email" label="Kênh báo" tone="text-rose-500" />
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 p-6">
              {isSuccess && (
                <div className="flex items-start gap-3 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-emerald-800 shadow-sm">
                  <CheckCircle2 size={20} className="mt-0.5 shrink-0" />
                  <div>
                    <p className="font-black">Đăng ký thành công</p>
                    <p className="text-sm font-semibold text-emerald-700">
                      Cấu hình theo dõi đã được thêm vào danh sách giám sát.
                    </p>
                  </div>
                </div>
              )}

              <Field icon={User} label="Họ và tên *" error={errors.fullName}>
                <input type="text" placeholder="Nguyễn Văn A" {...register("fullName")} className={inputClass(errors.fullName)} />
              </Field>

              <Field icon={Mail} label="Email nhận thông báo *" error={errors.email}>
                <input type="email" placeholder="example@gmail.com" {...register("email")} className={inputClass(errors.email)} />
              </Field>

              <Field icon={Hash} label="Mã môn học *" error={errors.subjectCode}>
                <input type="text" placeholder="Ví dụ: CS 466" {...register("subjectCode")} className={`${inputClass(errors.subjectCode)} uppercase`} />
              </Field>

              <Field icon={BookOpen} label="Tên môn học *" error={errors.subjectName}>
                <input type="text" placeholder="Ví dụ: Perl & Python" {...register("subjectName")} className={inputClass(errors.subjectName)} />
              </Field>

              <button
                type="submit"
                disabled={isSubmitting}
                className="group flex h-[52px] w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-cyan-500 px-5 text-base font-black text-white shadow-[0_14px_28px_rgba(37,99,235,0.28)] transition duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_34px_rgba(14,165,233,0.34)] disabled:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    Đang kích hoạt...
                  </>
                ) : (
                  <>
                    <ShieldCheck size={20} className="transition group-hover:scale-110" />
                    Kích hoạt giám sát
                  </>
                )}
              </button>
            </form>
          </section>

          <section className="overflow-hidden rounded-xl border border-white/80 bg-white/82 shadow-[0_18px_55px_rgba(15,23,42,0.11)] backdrop-blur-xl">
            <div className="flex flex-col gap-4 border-b border-slate-200/80 bg-gradient-to-r from-white via-slate-50 to-blue-50/70 px-6 py-7 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="mb-2 inline-flex rounded-full bg-blue-600/10 px-3 py-1 text-xs font-black uppercase tracking-[0.14em] text-blue-700">
                  Monitoring
                </p>
                <h2 className="text-2xl font-black tracking-tight text-slate-950">
                  Danh sách đang giám sát
                </h2>
                <p className="mt-2 text-sm font-semibold text-slate-500">
                  Hiện có <span className="font-black text-slate-900">{totalSubscriptions}</span> cấu hình theo dõi
                </p>
              </div>
              <button
                type="button"
                onClick={handleRefresh}
                className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-4 text-sm font-black text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:text-blue-700 hover:shadow-md"
              >
                <RefreshCw size={16} className={isRefreshing ? "animate-spin text-blue-700" : "text-blue-700"} />
                Làm mới
              </button>
            </div>

            <div className="max-h-[612px] overflow-auto">
              <table className="w-full min-w-[900px] text-left">
                <thead className="sticky top-0 z-10 border-b border-slate-200 bg-slate-100/95 backdrop-blur">
                  <tr>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">ID</th>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Họ tên</th>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Email</th>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Mã môn</th>
                    <th className="px-6 py-4 text-right text-xs font-black uppercase tracking-[0.12em] text-slate-500">Thao tác</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 bg-white/70">
                  {subscriptions.map((item, index) => (
                    <tr key={item.id} className="group transition duration-200 hover:bg-blue-50/80">
                      <td className="px-6 py-5 font-mono text-sm font-black text-slate-400">#{item.id}</td>
                      <td className="px-6 py-5">
                        <div className="flex items-center gap-3">
                          <span className={`grid h-9 w-9 place-items-center rounded-full text-xs font-black text-white shadow-sm ${index % 3 === 0 ? "bg-blue-600" : index % 3 === 1 ? "bg-emerald-500" : "bg-rose-500"}`}>
                            {initials(item.fullName)}
                          </span>
                          <span className="font-black text-slate-950">{item.fullName}</span>
                        </div>
                      </td>
                      <td className="px-6 py-5 font-mono text-sm font-semibold text-slate-600">{item.email}</td>
                      <td className="px-6 py-5">
                        <span className="inline-flex rounded-md border border-blue-100 bg-blue-50 px-3 py-1.5 font-black text-blue-700 shadow-sm">
                          {item.subjectCode}
                        </span>
                      </td>
                      <td className="px-6 py-5">
                        <div className="flex justify-end gap-2">
                          <button
                            type="button"
                            className="inline-flex h-9 items-center gap-1.5 rounded-md border border-slate-200 bg-white px-3 text-sm font-black text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:text-blue-700"
                          >
                            <Edit3 size={15} />
                            Sửa
                          </button>
                          <button
                            type="button"
                            onClick={() => setSubscriptions((current) => current.filter((row) => row.id !== item.id))}
                            className="inline-flex h-9 items-center gap-1.5 rounded-md border border-rose-100 bg-rose-50 px-3 text-sm font-black text-rose-600 shadow-sm transition hover:-translate-y-0.5 hover:border-rose-200 hover:bg-rose-100"
                          >
                            <Trash2 size={15} />
                            Xóa
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </main>
    </PageShell>
  );
}
