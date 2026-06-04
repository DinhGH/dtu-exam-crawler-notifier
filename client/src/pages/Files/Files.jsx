import { useState, useEffect } from "react";
import { fileService } from "../../services/fileService";
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
import { FileText, Download, RefreshCw } from "lucide-react";

const Files = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [crawling, setCrawling] = useState(false);
  const [crawlMessage, setCrawlMessage] = useState("");

  useEffect(() => {
    fetchFiles();
  }, []);

  async function fetchFiles() {
    setLoading(true);
    try {
      const data = await fileService.getFiles();
      setFiles(data?.items || []);
    } catch (err) {
      console.error("Error fetching files:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDownload(downloadLink) {
    try {
      // Open the download link in a new tab
      window.open(downloadLink, "_blank");
    } catch (err) {
      console.error("Download error:", err);
    }
  }

  async function handleCrawlLatest() {
    setCrawling(true);
    setCrawlMessage("");
    try {
      const result = await fileService.crawlFiles(true);
      setCrawlMessage(result.message);
      fetchFiles(); // Refresh the list after crawling
    } catch (err) {
      console.error("Crawl error:", err);
      setCrawlMessage("Crawl failed: " + err.message);
    } finally {
      setCrawling(false);
    }
  }

  const formatDate = (iso) => {
    if (!iso) return "-";
    try {
      return new Intl.DateTimeFormat("vi-VN", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      }).format(new Date(iso));
    } catch {
      return iso;
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12 flex justify-center">
        <LoadingSpinner size={48} />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          Danh sách tệp
        </h1>
        <button
          onClick={handleCrawlLatest}
          disabled={crawling}
          className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`h-4 w-4 ${crawling ? "animate-spin" : ""}`} />
          {crawling ? "Đang cào..." : "Cào dữ liệu mới (100 file)"}
        </button>
      </div>

      {crawlMessage && (
        <div
          className={`mb-4 p-3 rounded-md ${crawlMessage.includes("success") || crawlMessage.includes("completed") ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}
        >
          {crawlMessage}
        </div>
      )}

      {!loading && files.length === 0 ? (
        <div className="mt-8">
          <EmptyState
            icon={FileText}
            title="Không có tệp"
            description="Hiện chưa có tệp nào được lưu. Bấm nút 'Cào dữ liệu mới' để lấy dữ liệu từ website."
            action={
              <button
                onClick={handleCrawlLatest}
                className="mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
              >
                <RefreshCw className="inline-block mr-2 h-4 w-4" />
                Cào dữ liệu mới
              </button>
            }
          />
        </div>
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Tên tệp</TableHead>
                <TableHead>Ngày cào</TableHead>
                <TableHead>Hành động</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {files.map((f, i) => (
                <TableRow key={f.id || i} hover>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                      <div className="font-medium text-gray-900 dark:text-gray-100 max-w-2xl truncate">
                        <span className="font-medium text-gray-900 dark:text-gray-100">
                          {f.file_name}
                        </span>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    {formatDate(f.crawl_time || f.created_at)}
                  </TableCell>
                  <TableCell>
                    <button
                      onClick={() =>
                        handleDownload(f.download_link, f.file_name)
                      }
                      className="inline-flex items-center gap-2 px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                    >
                      <Download className="h-4 w-4" /> Tải xuống
                    </button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
};

export default Files;
