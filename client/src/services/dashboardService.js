import apiClient from "./apiClient";

export const dashboardService = {
  async getStats() {
    const response = await apiClient.get("/dashboard/stats");
    return response.data;
  },

  async getFilesOverTime() {
    const response = await apiClient.get("/dashboard/files-over-time");
    return response.data;
  },

  async getEmailsOverTime() {
    const response = await apiClient.get("/dashboard/emails-over-time");
    return response.data;
  },
};
