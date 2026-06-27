import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { fileService } from "../../services/fileService";
import { examService } from "../../services/examService";
import {
  Table, TableBody, TableCell,
  TableHead, TableHeader, TableRow,
} from "../../components/ui/Table";
import { LoadingSpinner } from "../../components/ui/LoadingSpinner";
import { EmptyState } from "../../components/ui/EmptyState";
import { SearchBox } from "../../components/ui/SearchBox";
import { Button } from "../../components/ui/Button";
import {
  ArrowLeft, FileText, Calendar,
  Database, Download, Search,
  ChevronLeft, ChevronRight, Clock, MapPin,
} from "lucide-react";

const PAGE_SIZE = 20;

const FileDetail = () => {
  const { fileId } = useParams();
  const navigate = useNavigate();

  const [fileInfo, setFileInfo] = useState(null);
  const [fileLoading, setFileLoading] = useState(true);
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [searchInput, setSearchInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  // Load thông tin tệp
  useEffect(() => {
    const load = async () => {
      setFileLoading(true);
      try {
        const data = await fileService.getFileDetail(fileId);
        setFileInfo(data);
      } catch (err) {
        console.error(err);
        toast.error("Không thể tải thông tin tệp");
      } finally {
        setFileLoading(false);
      }
    };
    load();
  }, [fileId]);

  // Load danh sách sinh viên trong tệp
  const loadSchedules = useCallback(async () => {
    setLoading(true);
    try {
      const params = { page, page_size: PAGE_SIZE };
      if (searchQuery.trim()) params.student_name = searchQuery.trim();
      // Nếu backend hỗ trợ lọc theo file_id thì thêm vào
      // params.file_id = fileId;
      const data = await examService.getExamSchedulesByFile(fileId, params);
      setSchedules(data?.items || []);
      setTotal(data?.total || 0);
    } catch (err) {
      console.error(err);
      toast.error("Không thể tải danh sách sinh viên");
    } finally {
      setLoading(false);
    }
  }, [fileId, page, searchQuery]);

  useEffect(() => { loadSchedules(); }, [loadSchedules]);

  const handleSearch = () => { setSearchQuery(searchInput); setPage(1); };

  const formatDate = (iso) => {
    if (!iso) return "-";
    try {
      return new Intl.DateTimeFormat("vi-VN", {
        timeZone: "Asia/Ho_Chi_Minh",
        day: "2-digit", month: "2-digit", year: "numeric",
        hour: "2-digit", minute: "2-digit", hour12: false,
      }).format(new Date(iso));
    } catch { return iso; }
  };

  const formatExamDate = (d) => {
    if (!d) return "-";
    const parts = String(d).split("-");
    if (parts.length === 3) return `${parts[2]}/${parts[1]}/${parts[0]}`;
    return d;
  };

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div className="space-y-5">
      {/* Nút quay lại */}
      <button
        onClick={() => navigate("/files")}
        className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-blue-600 font-medium transition-colors"
      >
        <ArrowLeft className="h-4 w-4" /> Quay lại danh sách tệp
      </button>

      {/* Card thông tin tệp */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        {fileLoading ? (
          <div className="p-6 animate-pulse space-y-3">
            <div className="h-5 bg-gray-200 rounded w-2/3" />
            <div className="h-4 bg-gray-200 rounded w-1/3" />
          </div>
        ) : (
          <div className="p-5">
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-11 h-11 bg-blue-50 rounded-lg flex items-center justify-center">
                  <FileText className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900 break-all leading-snug">
                    {fileInfo?.file_name || "-"}
                  </h1>
                  <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-500">
                    <span className="flex items-center gap-1.5">
                      <Calendar className="h-4 w-4 text-gray-400" />
                      Thu thập: {formatDate(fileInfo?.crawl_time)}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Database className="h-4 w-4 text-gray-400" />
                      {(fileInfo?.total_records || 0).toLocaleString("vi-VN")} bản ghi
                    </span>
                  </div>
                </div>
              </div>
              {fileInfo?.download_link && (
                <a
                  href={fileInfo.download_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors flex-shrink-0"
                >
                  <Download className="h-4 w-4" /> Tải xuống
                </a>
              )}
            </div>

            {/* Stats mini */}
            <div className="mt-4 grid grid-cols-3 gap-3">
              {[
                { label: "Tổng bản ghi", value: (fileInfo?.total_records || 0).toLocaleString("vi-VN"), color: "text-blue-600" },
                { label: "Đang hiển thị", value: `${schedules.length} bản ghi`, color: "text-emerald-600" },
                { label: "Trang hiện tại", value: `${page} / ${totalPages || 1}`, color: "text-orange-500" },
              ].map(({ label, value, color }) => (
                <div key={label} className="bg-gray-50 rounded-md px-3 py-2.5 border border-gray-100">
                  <p className={`text-base font-bold ${color}`}>{value}</p>
                  <p className="text-xs text-gray-400 mt-0.5">{label}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Bảng danh sách sinh viên */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
        {/* Thanh tìm kiếm */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 px-4 py-3 border-b border-gray-100 bg-gray-50/60">
          <div>
            <h2 className="font-semibold text-gray-800">Danh sách sinh viên trong tệp</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Tổng <span className="font-semibold text-gray-700">{total.toLocaleString("vi-VN")}</span> bản ghi
            </p>
          </div>
          <div className="flex gap-2">
            <SearchBox
              placeholder="Tìm theo họ tên..."
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="w-full sm:w-60"
            />
            <Button
              onClick={handleSearch}
              className="inline-flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700 transition-colors"
            >
              <Search className="h-4 w-4" /> Tìm
            </Button>
          </div>
        </div>

        {/* Bảng cuộn */}
        <div className="overflow-auto" style={{ maxHeight: "520px" }}>
          {loading ? (
            <div className="flex items-center justify-center py-20">
              <LoadingSpinner size={36} />
            </div>
          ) : schedules.length === 0 ? (
            <EmptyState
              icon="search"
              title="Không tìm thấy kết quả"
              description="Thử tìm kiếm với từ khóa khác."
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="whitespace-nowrap">MSSV</TableHead>
                  <TableHead className="whitespace-nowrap">Họ và tên</TableHead>
                  <TableHead className="whitespace-nowrap">Mã môn</TableHead>
                  <TableHead className="whitespace-nowrap">Tên môn học</TableHead>
                  <TableHead className="whitespace-nowrap">Ngày thi</TableHead>
                  <TableHead className="whitespace-nowrap">Giờ thi</TableHead>
                  <TableHead className="whitespace-nowrap">Phòng thi</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {schedules.map((s, i) => (
                  <TableRow key={s.id || i}>
                    <TableCell>
                      <span className="font-mono text-xs text-gray-400">{s.student_id || "-"}</span>
                    </TableCell>
                    <TableCell>
                      <span className="font-medium text-gray-900 whitespace-nowrap">{s.student_name || "-"}</span>
                    </TableCell>
                    <TableCell>
                      <span className="inline-flex items-center px-2 py-0.5 bg-blue-50 text-blue-700 rounded text-xs font-semibold font-mono">
                        {s.subject_code || "-"}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span className="text-gray-700 line-clamp-2 max-w-xs">{s.subject_name || "-"}</span>
                    </TableCell>
                    <TableCell className="whitespace-nowrap">
                      <span className="flex items-center gap-1.5 text-gray-700">
                        <Clock className="h-3.5 w-3.5 text-gray-400" />
                        {formatExamDate(s.exam_date)}
                      </span>
                    </TableCell>
                    <TableCell className="whitespace-nowrap font-medium text-gray-700">
                      {s.exam_time || "-"}
                    </TableCell>
                    <TableCell>
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-md text-xs font-semibold">
                        <MapPin className="h-3 w-3" /> {s.exam_room || "-"}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>

        {/* Phân trang */}
        {total > 0 && (
          <div className="flex flex-col sm:flex-row items-center justify-between px-4 py-3 border-t border-gray-100 gap-3 text-sm text-gray-600">
            <span>
              Hiển thị {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, total)} trên {total.toLocaleString("vi-VN")} bản ghi
            </span>
            <div className="flex items-center gap-2">
              <button
                disabled={page === 1}
                onClick={() => setPage((p) => p - 1)}
                className="inline-flex items-center gap-1 px-3 py-1 border rounded disabled:opacity-40 hover:bg-gray-50 bg-white transition-colors"
              >
                <ChevronLeft className="h-3.5 w-3.5" /> Trước
              </button>
              <span className="px-2 whitespace-nowrap">Trang {page} / {totalPages || 1}</span>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
                className="inline-flex items-center gap-1 px-3 py-1 border rounded disabled:opacity-40 hover:bg-gray-50 bg-white transition-colors"
              >
                Sau <ChevronRight className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileDetail;
