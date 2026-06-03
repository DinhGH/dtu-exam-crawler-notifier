import apiClient from "./apiClient";

export const examService = {
  async getExamSchedules(params = {}) {
    const response = await apiClient.get("/exam-schedules", { params });
    return response.data;
  },

  async getExamScheduleById(id) {
    const response = await apiClient.get(`/exam-schedules/${id}`);
    return response.data;
  },
};
