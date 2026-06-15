import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity,
  Bell,
  BookOpen,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  Clock,
  FileText,
  Hash,
  MapPin,
  Menu,
  RefreshCw,
  Search,
  SearchX,
  Sparkles,
  User,
} from "lucide-react";

const examRows = [
  {
    id: 1,
    studentName: "Nguyễn Văn Tín",
    subjectCode: "OB 253",
    subjectName: "Tổng quan Hành vi Tổ chức trong Du lịch",
    examDate: "29/05/2026",
    examTime: "17:18",
    room: "B-D-F",
    sourceFile: "Tổng quan Hành vi Tổ chức trong Du lịch OB 253 (B-D-F) (17:18 29/05/2026)",
  },
  {
    id: 2,
    studentName: "Trần Thị Bé",
    subjectCode: "HRM 303",
    subjectName: "Quản trị Nhân lực trong Du lịch",
    examDate: "29/05/2026",
    examTime: "17:17",
    room: "B-D-F",
    sourceFile: "Quản trị Nhân lực trong Du lịch HRM 303 (B-D-F) (17:17 29/05/2026)",
  },
  {
    id: 3,
    studentName: "Lê Hoàng Vũ",
    subjectCode: "POS 351",
    subjectName: "Chủ nghĩa Xã hội Khoa học",
    examDate: "29/05/2026",
    examTime: "17:17",
    room: "L-P-T",
    sourceFile: "Chủ nghĩa Xã hội Khoa học POS 351 (L-P-T) (17:17 29/05/2026)",
  },
  {
    id: 4,
    studentName: "Phạm Văn Minh",
    subjectCode: "CS 201",
    subjectName: "Cấu trúc dữ liệu và giải thuật",
    examDate: "29/05/2026",
    examTime: "09:22",
    room: "HL-HX-JD-JJ-LF",
    sourceFile: "CS 201 (HL-HX-JD-JJ-LF) (09:22 29/05/2026)",
  },
  {
    id: 5,
    studentName: "Đỗ Thị Hương",
    subjectCode: "CS 100",
    subjectName: "Giới thiệu về Khoa học Máy tính",
    examDate: "29/05/2026",
    examTime: "09:22",
    room: "B-D",
    sourceFile: "Giới thiệu về Khoa học Máy tính CS 100 (B-D) (09:22 29/05/2026)",
  },
  {
    id: 6,
    studentName: "Hoàng Văn Tuấn",
    subjectCode: "CR 424",
    subjectName: "Lập trình Ứng dụng cho các Thiết bị Di động",
    examDate: "29/05/2026",
    examTime: "09:22",
    room: "B-D-F",
    sourceFile: "Lập trình Ứng dụng cho các Thiết bị Di động CR 424 (B-D-F) (09:22 29/05/2026)",
  },
  {
    id: 7,
    studentName: "Nguyễn Văn Tín",
    subjectCode: "MGT 301",
    subjectName: "Quản trị học",
    examDate: "30/05/2026",
    examTime: "07:30",
    room: "A-C-E",
    sourceFile: "Quản trị học MGT 301 (A-C-E) (07:30 30/05/2026)",
  },
  {
    id: 8,
    studentName: "Trần Thị Bé",
    subjectCode: "ENG 302",
    subjectName: "Tiếng Anh chuyên ngành",
    examDate: "30/05/2026",
    examTime: "13:00",
    room: "P-203",
    sourceFile: "Tiếng Anh chuyên ngành ENG 302 (P-203) (13:00 30/05/2026)",
  },
  {
    id: 9,
    studentName: "Lê Hoàng Vũ",
    subjectCode: "ACC 205",
    subjectName: "Kế toán tài chính",
    examDate: "31/05/2026",
    examTime: "09:15",
    room: "K-101",
    sourceFile: "Kế toán tài chính ACC 205 (K-101) (09:15 31/05/2026)",
  },
  {
    id: 10,
    studentName: "Phạm Văn Minh",
    subjectCode: "MIS 202",
    subjectName: "Hệ thống thông tin quản lý",
    examDate: "31/05/2026",
    examTime: "15:30",
    room: "H-305",
    sourceFile: "Hệ thống thông tin quản lý MIS 202 (H-305) (15:30 31/05/2026)",
  },
  {
    id: 11,
    studentName: "Đỗ Thị Hương",
    subjectCode: "LAW 101",
    subjectName: "Pháp luật đại cương",
    examDate: "01/06/2026",
    examTime: "07:30",
    room: "D-404",
    sourceFile: "Pháp luật đại cương LAW 101 (D-404) (07:30 01/06/2026)",
  },
  {
    id: 12,
    studentName: "Hoàng Văn Tuấn",
    subjectCode: "STA 220",
    subjectName: "Xác suất thống kê",
    examDate: "01/06/2026",
    examTime: "10:00",
    room: "F-202",
    sourceFile: "Xác suất thống kê STA 220 (F-202) (10:00 01/06/2026)",
  },
];

const ITEMS_PER_PAGE = 8;

const normalize = (value) =>
  value
    .toString()
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");

const initials = (name) =>
  name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(-2)
    .toUpperCase();

const Navbar = ({ active = "search" }) => {
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
        <button type="button" onClick={() => navigate("/")} className="group flex items-center gap-3">
          <span className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-blue-600 via-cyan-500 to-emerald-400 text-white shadow-[0_12px_24px_rgba(37,99,235,0.26)] transition group-hover:-translate-y-0.5">
            <Sparkles size={20} />
          </span>
          <span className="text-left">
            <span className="block text-lg font-black tracking-tight text-slate-950">DTU Exam Notifier</span>
            <span className="block text-xs font-bold uppercase tracking-[0.16em] text-slate-400">Exam tracking</span>
          </span>
        </button>

        <div className="flex items-center gap-2 sm:gap-3">
          <button type="button" onClick={() => navigate("/dang-ky")} className={navItemClass("register")}>
            Đăng ký theo dõi
          </button>
          <button type="button" onClick={() => navigate("/tra-cuu")} className={navItemClass("search")}>
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

const SummaryCard = ({ icon: Icon, value, label, tone }) => (
  <div className="rounded-lg border border-white/70 bg-white/70 p-4 shadow-sm">
    <div className="flex items-center gap-3">
      <span className={`grid h-10 w-10 place-items-center rounded-lg ${tone.bg} ${tone.text}`}>
        <Icon size={19} />
      </span>
      <div>
        <p className={`text-2xl font-black ${tone.value}`}>{value}</p>
        <p className="text-xs font-black uppercase tracking-[0.13em] text-slate-400">{label}</p>
      </div>
    </div>
  </div>
);

const SearchField = ({ icon: Icon, label, name, placeholder, value, onChange }) => (
  <label className="block">
    <span className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-[0.11em] text-slate-600">
      <Icon size={15} className="text-blue-600" />
      {label}
    </span>
    <div className="relative">
      <Icon size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
      <input
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="h-[52px] w-full rounded-lg border border-slate-200 bg-slate-50/80 pl-11 pr-4 text-[15px] font-bold text-slate-800 shadow-inner outline-none transition duration-200 placeholder:font-semibold placeholder:text-slate-400 hover:border-blue-300 hover:bg-white focus:border-blue-600 focus:bg-white focus:ring-4 focus:ring-blue-100"
      />
    </div>
  </label>
);

export default function SearchPage() {
  const [filters, setFilters] = useState({
    studentName: "",
    subjectCode: "",
    subjectName: "",
  });
  const [submittedFilters, setSubmittedFilters] = useState(filters);
  const [currentPage, setCurrentPage] = useState(1);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const navigate = useNavigate();

  const filteredRows = useMemo(() => {
    const studentName = normalize(submittedFilters.studentName);
    const subjectCode = normalize(submittedFilters.subjectCode);
    const subjectName = normalize(submittedFilters.subjectName);

    return examRows.filter((row) => {
      const matchesStudent = !studentName || normalize(row.studentName).includes(studentName);
      const matchesCode = !subjectCode || normalize(row.subjectCode).includes(subjectCode);
      const matchesSubject = !subjectName || normalize(row.subjectName).includes(subjectName);

      return matchesStudent && matchesCode && matchesSubject;
    });
  }, [submittedFilters]);

  const totalPages = Math.max(1, Math.ceil(filteredRows.length / ITEMS_PER_PAGE));
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const pagedRows = filteredRows.slice(startIndex, startIndex + ITEMS_PER_PAGE);
  const displayStart = filteredRows.length === 0 ? 0 : startIndex + 1;
  const displayEnd = Math.min(startIndex + ITEMS_PER_PAGE, filteredRows.length);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = (event) => {
    event.preventDefault();
    setSubmittedFilters(filters);
    setCurrentPage(1);
  };

  const handleRefresh = () => {
    setIsRefreshing(true);
    window.setTimeout(() => setIsRefreshing(false), 650);
  };

  return (
    <PageShell>
      <Navbar />

      <main className="flex-1 px-5 py-8 sm:px-8">
        <div className="mx-auto max-w-[1680px]">
          <div className="mb-7 overflow-hidden rounded-xl border border-white/80 bg-white/82 shadow-[0_18px_55px_rgba(15,23,42,0.11)] backdrop-blur-xl">
            <div className="relative overflow-hidden bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900 p-6 text-white lg:p-7">
              <div className="absolute -right-14 -top-16 h-52 w-52 rounded-full bg-cyan-400/20 blur-2xl" />
              <div className="absolute -bottom-24 left-1/2 h-56 w-56 rounded-full bg-emerald-400/15 blur-3xl" />
              <div className="relative flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-sm font-black text-cyan-100">
                    <Activity size={16} />
                    Dữ liệu danh sách thi
                  </div>
                  <h1 className="text-3xl font-black tracking-tight sm:text-4xl">
                    Tra cứu danh sách thi
                  </h1>
                  <p className="mt-3 max-w-3xl text-sm font-medium leading-6 text-slate-300 sm:text-base">
                    Tìm kiếm nhanh theo họ tên sinh viên, mã môn học hoặc tên môn học trong các tệp đã thu thập.
                  </p>
                </div>

                <div className="flex flex-wrap gap-3">
                  <button
                    type="button"
                    onClick={() => navigate("/dang-ky")}
                    className="h-[48px] rounded-lg border border-white/15 bg-white/10 px-5 font-black text-white backdrop-blur transition hover:-translate-y-0.5 hover:bg-white/16 hover:shadow-md"
                  >
                    Đăng ký theo dõi
                  </button>
                  <button
                    type="button"
                    onClick={handleRefresh}
                    className="inline-flex h-[48px] items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-cyan-500 px-5 font-black text-white shadow-[0_14px_28px_rgba(37,99,235,0.28)] transition hover:-translate-y-0.5 hover:shadow-[0_18px_34px_rgba(14,165,233,0.34)]"
                  >
                    <RefreshCw size={18} className={isRefreshing ? "animate-spin" : ""} />
                    Làm mới dữ liệu
                  </button>
                </div>
              </div>
            </div>

            <div className="grid gap-3 bg-slate-50/70 p-5 md:grid-cols-3">
              <SummaryCard icon={FileText} value={examRows.length} label="Bản ghi" tone={{ bg: "bg-blue-50", text: "text-blue-700", value: "text-blue-600" }} />
              <SummaryCard icon={CalendarDays} value="04" label="Ngày thi" tone={{ bg: "bg-emerald-50", text: "text-emerald-700", value: "text-emerald-600" }} />
              <SummaryCard icon={MapPin} value="12" label="Phòng/tệp" tone={{ bg: "bg-rose-50", text: "text-rose-700", value: "text-rose-500" }} />
            </div>
          </div>

          <form
            onSubmit={handleSearch}
            className="mb-7 rounded-xl border border-white/80 bg-white/82 p-5 shadow-[0_18px_55px_rgba(15,23,42,0.1)] backdrop-blur-xl"
          >
            <div className="grid grid-cols-1 items-end gap-4 md:grid-cols-3 xl:grid-cols-[1fr_1fr_1fr_auto]">
              <SearchField
                icon={User}
                label="Họ tên sinh viên"
                name="studentName"
                value={filters.studentName}
                onChange={handleInputChange}
                placeholder="Nhập họ tên sinh viên..."
              />
              <SearchField
                icon={Hash}
                label="Mã môn học"
                name="subjectCode"
                value={filters.subjectCode}
                onChange={handleInputChange}
                placeholder="Ví dụ: CS 201"
              />
              <SearchField
                icon={BookOpen}
                label="Tên môn học"
                name="subjectName"
                value={filters.subjectName}
                onChange={handleInputChange}
                placeholder="Nhập tên môn học..."
              />
              <button
                type="submit"
                className="inline-flex h-[52px] items-center justify-center gap-2 rounded-lg bg-slate-950 px-8 font-black text-white shadow-[0_12px_24px_rgba(15,23,42,0.18)] transition hover:-translate-y-0.5 hover:bg-blue-700 hover:shadow-[0_16px_30px_rgba(37,99,235,0.27)]"
              >
                <Search size={18} />
                Tìm
              </button>
            </div>
          </form>

          <section className="overflow-hidden rounded-xl border border-white/80 bg-white/82 shadow-[0_18px_55px_rgba(15,23,42,0.11)] backdrop-blur-xl">
            <div className="flex flex-col gap-2 border-b border-slate-200/80 bg-gradient-to-r from-white via-slate-50 to-blue-50/70 px-6 py-5 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="mb-2 inline-flex rounded-full bg-blue-600/10 px-3 py-1 text-xs font-black uppercase tracking-[0.14em] text-blue-700">
                  Results
                </p>
                <h2 className="text-2xl font-black tracking-tight text-slate-950">
                  Kết quả tra cứu
                </h2>
                <p className="mt-1 text-sm font-semibold text-slate-500">
                  Hiển thị <span className="font-black text-slate-900">{filteredRows.length}</span> kết quả phù hợp
                </p>
              </div>
            </div>

            <div className="max-h-[560px] overflow-auto">
              <table className="w-full min-w-[1120px] text-left">
                <thead className="sticky top-0 z-10 border-b border-slate-200 bg-slate-100/95 backdrop-blur">
                  <tr>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Tên môn học</th>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Ngày thi</th>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Giờ thi</th>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Phòng thi</th>
                    <th className="px-6 py-4 text-xs font-black uppercase tracking-[0.12em] text-slate-500">Tệp nguồn chứa dữ liệu</th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-100 bg-white/70">
                  {pagedRows.length > 0 ? (
                    pagedRows.map((row, index) => (
                      <tr key={row.id} className="group transition duration-200 hover:bg-blue-50/80">
                        <td className="px-6 py-5">
                          <div className="flex items-start gap-3">
                            <span className={`grid h-10 w-10 shrink-0 place-items-center rounded-full text-xs font-black text-white shadow-sm ${index % 3 === 0 ? "bg-blue-600" : index % 3 === 1 ? "bg-emerald-500" : "bg-rose-500"}`}>
                              {initials(row.studentName)}
                            </span>
                            <div>
                              <div className="font-black text-slate-950">{row.subjectName}</div>
                              <div className="mt-2 flex flex-wrap gap-2 text-sm">
                                <span className="rounded-md border border-blue-100 bg-blue-50 px-2.5 py-1 font-black text-blue-700">
                                  {row.subjectCode}
                                </span>
                                <span className="rounded-md bg-slate-100 px-2.5 py-1 font-bold text-slate-600">
                                  {row.studentName}
                                </span>
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="whitespace-nowrap px-6 py-5">
                          <span className="inline-flex items-center gap-2 font-black text-slate-800">
                            <Clock size={16} className="text-blue-700" />
                            {row.examDate}
                          </span>
                        </td>
                        <td className="whitespace-nowrap px-6 py-5 font-black text-slate-800">{row.examTime}</td>
                        <td className="px-6 py-5">
                          <span className="inline-flex items-center gap-2 rounded-md border border-emerald-100 bg-emerald-50 px-3 py-2 font-black text-emerald-700 shadow-sm">
                            <MapPin size={16} />
                            {row.room}
                          </span>
                        </td>
                        <td className="px-6 py-5">
                          <span
                            title={row.sourceFile}
                            className="inline-flex max-w-[500px] items-center gap-2 rounded-md bg-slate-100 px-3 py-2 text-sm font-bold text-slate-700"
                          >
                            <FileText size={16} className="shrink-0 text-blue-700" />
                            <span className="truncate">{row.sourceFile}</span>
                          </span>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" className="px-6 py-20 text-center">
                        <div className="flex flex-col items-center text-slate-500">
                          <span className="mb-4 grid h-16 w-16 place-items-center rounded-full bg-slate-100 text-slate-400">
                            <SearchX size={34} />
                          </span>
                          <p className="font-black text-slate-900">Không tìm thấy kết quả phù hợp</p>
                          <p className="mt-1 text-sm font-semibold">Hãy thử rút gọn từ khóa hoặc kiểm tra lại mã môn học.</p>
                        </div>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="flex flex-col gap-3 border-t border-slate-200/80 bg-slate-50/70 px-6 py-4 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-sm font-bold text-slate-600">
                Hiển thị {displayStart} - {displayEnd} trên {filteredRows.length} kết quả
              </p>

              <div className="flex items-center justify-end gap-4">
                <button
                  type="button"
                  onClick={() => setCurrentPage((page) => Math.max(1, page - 1))}
                  disabled={currentPage === 1}
                  className="inline-flex h-10 items-center gap-2 rounded-md border border-slate-200 bg-white px-4 font-black text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:text-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <ChevronLeft size={16} />
                  Trước
                </button>
                <span className="font-black text-slate-800">
                  Trang {currentPage} / {totalPages}
                </span>
                <button
                  type="button"
                  onClick={() => setCurrentPage((page) => Math.min(totalPages, page + 1))}
                  disabled={currentPage === totalPages}
                  className="inline-flex h-10 items-center gap-2 rounded-md border border-slate-200 bg-white px-4 font-black text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:text-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Sau
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>
          </section>
        </div>
      </main>
    </PageShell>
  );
}
