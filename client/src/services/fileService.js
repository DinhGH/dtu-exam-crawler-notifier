import apiClient from "./apiClient";

export const fileService = {
  async getFiles(page = 1, pageSize = 10, q = "") {
    const params = new URLSearchParams({
      page,
      page_size: pageSize,
    });
    if (q) {
      params.append("q", q);
    }
    const res = await apiClient.get(`/files?${params.toString()}`);

    return res.data;
  },
  async getFileDetail(fileId) {
    const response = await apiClient.get(`/files/${fileId}`);
    return response.data;
  },

  async getFileUrl(fileId) {
    const response = await apiClient.get(`/files/${fileId}/download`, {
      responseType: "blob",
    });
    return response;
  },

  async crawlFiles(crawlLatestOnly = false) {
    const response = await apiClient.post("/files/crawl", null, {
      params: { crawl_latest_only: crawlLatestOnly },
    });
    return response.data;
  },
};
