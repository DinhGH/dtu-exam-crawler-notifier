import apiClient from "./apiClient";

export const fileService = {
  async getFiles(params = {}) {
    const response = await apiClient.get("/files", { params });
    return response.data;
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
};
