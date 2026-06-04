import { useState, useEffect, useMemo } from "react";
import { examService } from "../../services/examService";
import { SearchBox } from "../../components/ui/SearchBox";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../../components/ui/Table";
import { LoadingSpinner } from "../../components/ui/LoadingSpinner";
import { EmptyState } from "../../components/ui/EmptyState";
import { FileText, Search as SearchIcon } from "lucide-react";

const Search = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [examSchedules, setExamSchedules] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchExams();
  }, []);

  const filteredExams = useMemo(() => {
    if (searchTerm.trim() === "") return examSchedules;
    const searchTermLower = searchTerm.toLowerCase();
    return examSchedules.filter((exam) => {
      return (
        exam.course_name?.toLowerCase().includes(searchTermLower) ||
        exam.class_name?.toLowerCase().includes(searchTermLower) ||
        exam.date?.toLowerCase().includes(searchTermLower) ||
        exam.time?.toLowerCase().includes(searchTermLower) ||
        exam.location?.toLowerCase().includes(searchTermLower)
      );
    });
  }, [searchTerm, examSchedules]);

  async function fetchExams() {
    setLoading(true);
    try {
      const data = await examService.getExamSchedules();
      setExamSchedules(data);
    } catch (error) {
      console.error("Error fetching exams:", error);
    } finally {
      setLoading(false);
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }).format(date);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          Tra cứu danh sách thi
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Tìm kiếm thông tin danh sách thi theo môn học, lớp, hoặc ngày thi
        </p>
      </div>

      <div className="mb-6">
        <SearchBox
          placeholder="Tìm kiếm theo môn học, lớp, ngày thi..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <LoadingSpinner size={48} />
        </div>
      ) : filteredExams.length === 0 ? (
        <EmptyState
          icon={SearchIcon}
          title="Không tìm thấy kết quả"
          description={
            searchTerm
              ? `Không tìm thấy môn thi nào匹配 với "${searchTerm}"`
              : "Hiện chưa có danh sách thi nào. Vui lòng quay lại sau!"
          }
          action={
            !searchTerm && (
              <button
                onClick={fetchExams}
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                Tải lại danh sách
              </button>
            )
          }
        />
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Môn học</TableHead>
                <TableHead>Lớp</TableHead>
                <TableHead>Ngày thi</TableHead>
                <TableHead>Giờ thi</TableHead>
                <TableHead>Địa điểm</TableHead>
                <TableHead>File</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredExams.map((exam, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <div className="font-medium text-gray-900 dark:text-gray-100">
                      {exam.course_name || "-"}
                    </div>
                  </TableCell>
                  <TableCell>{exam.class_name || "-"}</TableCell>
                  <TableCell>{formatDate(exam.date) || "-"}</TableCell>
                  <TableCell>{exam.time || "-"}</TableCell>
                  <TableCell>{exam.location || "-"}</TableCell>
                  <TableCell>
                    {exam.file_id ? (
                      <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                    ) : (
                      <span className="text-gray-400">-</span>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Tìm thấy {filteredExams.length} kết quả
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Search;
