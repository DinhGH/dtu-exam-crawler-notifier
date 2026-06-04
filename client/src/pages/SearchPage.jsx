import { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { 
  Activity, ChevronRight, Search, User, Hash, BookOpen, 
  Calendar, Clock, MapPin, FileText, Download, 
  ChevronLeft, Loader2, SearchX
} from "lucide-react";

// ==========================================
// 1. COMPONENT NAVBAR
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
            <button onClick={() => navigate("/tra-cuu")} className="text-blue-400 font-semibold">Tra cứu</button>
            <button onClick={() => navigate("/dang-ky")} className="text-slate-300 hover:text-white font-medium transition-colors">Đăng ký</button>
          </div>
        </div>
      </div>
    </nav>
  );
};

// ==========================================
// 2. DỮ LIỆU MẪU (MOCK DATA)
// ==========================================
const mockData = [
  { id: 1, studentName: "Nguyễn Văn Tin", subjectCode: "CS101", subjectName: "Nhập môn Lập trình", date: "15/06/2026", time: "07:30", room: "Phòng 201 - Quang Trung", file: "CS101_Midterm.pdf" },
  { id: 2, studentName: "Trần Thị Bé", subjectCode: "MAT201", subjectName: "Toán rời rạc", date: "16/06/2026", time: "09:00", room: "Phòng 305 - Hòa Khánh", file: "MAT201_Final.pdf" },
  { id: 3, studentName: "Lê Hoàng Vũ", subjectCode: "ENG302", subjectName: "Tiếng Anh chuyên ngành", date: "18/06/2026", time: "13:30", room: "Phòng 102 - Quang Trung", file: "ENG302_Speaking.pdf" },
  { id: 4, studentName: "Nguyễn Văn Tin", subjectCode: "PHY102", subjectName: "Vật lý đại cương", date: "20/06/2026", time: "07:30", room: "Phòng 404 - Hòa Khánh", file: "PHY102_List.xlsx" },
  { id: 5, studentName: "Phạm Văn Minh", subjectCode: "CS101", subjectName: "Nhập môn Lập trình", date: "15/06/2026", time: "07:30", room: "Phòng 201 - Quang Trung", file: "CS101_Midterm.pdf" },
  { id: 6, studentName: "Đỗ Thị Hương", subjectCode: "SWE401", subjectName: "Công nghệ Phần mềm", date: "22/06/2026", time: "15:00", room: "Phòng 501 - Quang Trung", file: "SWE401_Final.pdf" },
  { id: 7, studentName: "Hoàng Văn Tuấn", subjectCode: "NET201", subjectName: "Mạng máy tính", date: "25/06/2026", time: "09:30", room: "Phòng 202 - Hòa Khánh", file: "NET201_Midterm.pdf" },
];

// ==========================================
// 3. TRANG TRA CỨU CHÍNH
// ==========================================
export default function SearchPage() {
  const [searchParams, setSearchParams] = useState({
    studentName: "", subjectCode: "", subjectName: ""
  });
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({ ...prev, [name]: value }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      const filtered = mockData.filter(item => {
        const matchName = item.studentName.toLowerCase().includes(searchParams.studentName.toLowerCase());
        const matchCode = item.subjectCode.toLowerCase().includes(searchParams.subjectCode.toLowerCase());
        const matchSubject = item.subjectName.toLowerCase().includes(searchParams.subjectName.toLowerCase());
        return matchName && matchCode && matchSubject;
      });
      setResults(filtered);
      setCurrentPage(1);
      setHasSearched(true);
      setIsLoading(false);
    }, 800);
  };

  const totalPages = Math.ceil(results.length / itemsPerPage);
  const currentTableData = useMemo(() => {
    const firstPageIndex = (currentPage - 1) * itemsPerPage;
    return results.slice(firstPageIndex, firstPageIndex + itemsPerPage);
  }, [currentPage, results]);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans selection:bg-blue-200 selection:text-blue-900 relative">
      <Navbar />

      {/* HEADER BANNER (Giữ màu tối làm nền tương phản cho thanh Search) */}
      <div className="pt-32 pb-28 bg-gradient-to-br from-slate-900 via-slate-800 to-blue-950 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-500/20 rounded-full mix-blend-screen filter blur-[80px] pointer-events-none"></div>
        
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
            Tra Cứu <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Danh Sách Thi</span>
          </h1>
          <p className="text-slate-400 text-lg">
            Tìm kiếm thông tin lịch thi, phòng thi và tải tệp nguồn trực tiếp.
          </p>
        </div>
      </div>

      <main className="flex-grow w-full px-4 sm:px-6 lg:px-8 pb-16 relative z-20">
        
        {/* KHỐI TÌM KIẾM: UNIFIED BAR LƯỚT LÊN TRÊN HEADER */}
        <div className="max-w-5xl mx-auto bg-white p-3 rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.15)] border border-slate-100 -mt-14 mb-10">
          <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-2">
            
            {/* Soft UI Input 1 */}
            <div className="flex-1 relative group bg-slate-50 hover:bg-slate-100 focus-within:bg-white focus-within:ring-2 focus-within:ring-blue-500 transition-all rounded-[1.5rem] p-3 flex flex-col justify-center min-h-[70px]">
              <div className="absolute top-1/2 -translate-y-1/2 left-5 text-slate-400 group-focus-within:text-blue-600 transition-colors">
                <User size={22} />
              </div>
              <div className="pl-12 pr-2">
                <label className="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-0.5">Học viên</label>
                <input
                  type="text" name="studentName"
                  value={searchParams.studentName} onChange={handleInputChange}
                  placeholder="Nhập tên..."
                  className="w-full bg-transparent border-none outline-none text-slate-800 font-bold placeholder:font-medium placeholder:text-slate-400 text-sm md:text-base"
                />
              </div>
            </div>

            {/* Dải phân cách */}
            <div className="hidden md:block w-px bg-slate-200 my-4"></div>

            {/* Soft UI Input 2 */}
            <div className="flex-1 relative group bg-slate-50 hover:bg-slate-100 focus-within:bg-white focus-within:ring-2 focus-within:ring-blue-500 transition-all rounded-[1.5rem] p-3 flex flex-col justify-center min-h-[70px]">
              <div className="absolute top-1/2 -translate-y-1/2 left-5 text-slate-400 group-focus-within:text-blue-600 transition-colors">
                <Hash size={22} />
              </div>
              <div className="pl-12 pr-2">
                <label className="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-0.5">Mã môn</label>
                <input
                  type="text" name="subjectCode"
                  value={searchParams.subjectCode} onChange={handleInputChange}
                  placeholder="VD: CNT101"
                  className="w-full bg-transparent border-none outline-none text-slate-800 font-bold placeholder:font-medium placeholder:text-slate-400 text-sm md:text-base uppercase"
                />
              </div>
            </div>

            {/* Dải phân cách */}
            <div className="hidden md:block w-px bg-slate-200 my-4"></div>

            {/* Soft UI Input 3 */}
            <div className="flex-1 relative group bg-slate-50 hover:bg-slate-100 focus-within:bg-white focus-within:ring-2 focus-within:ring-blue-500 transition-all rounded-[1.5rem] p-3 flex flex-col justify-center min-h-[70px]">
              <div className="absolute top-1/2 -translate-y-1/2 left-5 text-slate-400 group-focus-within:text-blue-600 transition-colors">
                <BookOpen size={22} />
              </div>
              <div className="pl-12 pr-2">
                <label className="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-0.5">Tên môn</label>
                <input
                  type="text" name="subjectName"
                  value={searchParams.subjectName} onChange={handleInputChange}
                  placeholder="Từ khóa..."
                  className="w-full bg-transparent border-none outline-none text-slate-800 font-bold placeholder:font-medium placeholder:text-slate-400 text-sm md:text-base"
                />
              </div>
            </div>

            {/* Nút Call-to-Action tích hợp khối */}
            <button 
              type="submit"
              disabled={isLoading}
              className="md:ml-2 min-h-[70px] px-10 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-[1.5rem] font-bold text-base transition-all shadow-[0_8px_15px_rgba(37,99,235,0.25)] hover:shadow-[0_12px_25px_rgba(37,99,235,0.4)] hover:-translate-y-0.5 disabled:opacity-70 disabled:transform-none flex justify-center items-center gap-2"
            >
              {isLoading ? <Loader2 size={24} className="animate-spin" /> : <><Search size={22} className="stroke-[2.5]" /> <span className="md:hidden lg:inline">Tra Cứu</span></>}
            </button>
          </form>
        </div>

        {/* BẢNG KẾT QUẢ ĐỒNG BỘ SAAS CARD */}
        <div className="max-w-5xl mx-auto bg-white rounded-[2rem] shadow-xl border border-slate-100 overflow-hidden">
          
          <div className="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-white">
            <h3 className="font-extrabold text-slate-800 text-xl tracking-tight">Kết Quả Tra Cứu</h3>
            {hasSearched && !isLoading && (
              <span className="text-sm font-bold text-blue-700 bg-blue-50 px-4 py-1.5 rounded-full border border-blue-100">
                Tìm thấy {results.length} bản ghi
              </span>
            )}
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/80 border-b border-slate-100">
                  <th className="px-8 py-5 text-[11px] font-extrabold text-slate-400 uppercase tracking-widest">Học viên / Môn học</th>
                  <th className="px-8 py-5 text-[11px] font-extrabold text-slate-400 uppercase tracking-widest">Thời gian thi</th>
                  <th className="px-8 py-5 text-[11px] font-extrabold text-slate-400 uppercase tracking-widest">Phòng thi</th>
                  <th className="px-8 py-5 text-[11px] font-extrabold text-slate-400 uppercase tracking-widest text-right">Tệp nguồn</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                
                {isLoading && (
                  <tr>
                    <td colSpan="4" className="px-8 py-24 text-center">
                      <div className="flex flex-col items-center justify-center text-slate-400">
                        <Loader2 size={40} className="animate-spin mb-4 text-blue-500" />
                        <p className="font-bold text-slate-600 text-lg">Đang phân tích dữ liệu...</p>
                      </div>
                    </td>
                  </tr>
                )}

                {!isLoading && hasSearched && results.length === 0 && (
                  <tr>
                    <td colSpan="4" className="px-8 py-24 text-center">
                      <div className="flex flex-col items-center justify-center text-slate-400">
                        <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-5 border border-slate-100">
                          <SearchX size={36} className="text-slate-400" />
                        </div>
                        <p className="font-extrabold text-slate-700 text-xl mb-2">Không tìm thấy kết quả</p>
                        <p className="text-sm font-medium text-slate-500">Thử thay đổi từ khóa hoặc kiểm tra lại mã môn học.</p>
                      </div>
                    </td>
                  </tr>
                )}

                {!isLoading && currentTableData.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/50 transition-colors group">
                    <td className="px-8 py-5">
                      <div className="font-extrabold text-slate-800 text-base mb-1.5">{item.studentName}</div>
                      <div className="flex items-center gap-2">
                        <span className="inline-flex text-[11px] font-extrabold bg-blue-50 text-blue-600 border border-blue-100 px-2 py-0.5 rounded-md uppercase tracking-wider">
                          {item.subjectCode}
                        </span>
                        <span className="text-sm font-semibold text-slate-500">{item.subjectName}</span>
                      </div>
                    </td>
                    <td className="px-8 py-5">
                      <div className="flex items-center gap-2 text-sm text-slate-700 mb-1.5 font-bold">
                        <Calendar size={16} className="text-blue-400" /> {item.date}
                      </div>
                      <div className="flex items-center gap-2 text-sm text-slate-500 font-semibold">
                        <Clock size={16} className="text-slate-400" /> {item.time}
                      </div>
                    </td>
                    <td className="px-8 py-5">
                      <div className="flex items-center gap-2 text-sm text-slate-700 font-bold bg-white border border-slate-200 shadow-sm px-3 py-1.5 rounded-xl inline-flex">
                        <MapPin size={16} className="text-rose-400" />
                        {item.room}
                      </div>
                    </td>
                    <td className="px-8 py-5 text-right">
                      <button className="inline-flex items-center gap-2 text-sm font-bold text-slate-600 hover:text-blue-600 bg-slate-50 hover:bg-blue-50 px-4 py-2 rounded-[1rem] transition-all shadow-sm">
                        <FileText size={16} className="text-blue-500" />
                        <span className="hidden sm:inline-block max-w-[140px] truncate" title={item.file}>{item.file}</span>
                        <Download size={14} className="opacity-40 group-hover:opacity-100 transition-opacity" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* PHÂN TRANG */}
          {!isLoading && totalPages > 1 && (
            <div className="px-8 py-5 border-t border-slate-100 bg-white flex items-center justify-between">
              <span className="text-sm text-slate-500 font-semibold bg-slate-50 px-4 py-2 rounded-xl border border-slate-100">
                Trang <span className="font-extrabold text-slate-800">{currentPage}</span> / {totalPages}
              </span>
              <div className="flex gap-2">
                <button 
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="p-3 rounded-full border border-slate-200 bg-white text-slate-600 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm"
                >
                  <ChevronLeft size={18} />
                </button>
                <button 
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="p-3 rounded-full border border-slate-200 bg-white text-slate-600 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm"
                >
                  <ChevronRight size={18} />
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}