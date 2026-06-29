import apiClient from "./apiClient";

export const subscriptionService = {
  async subscribe(data) {
    const dataToSend = {
      student_id: data.student_id,
      email: data.email,
      subject_code: data.subject_code,
    };

    const response = await apiClient.post("/subscriptions", dataToSend);
    return response.data;
  },

  async getSubscriptions(skip = 0, limit = 100) {
    const response = await apiClient.get(
      `/subscriptions?skip=${skip}&limit=${limit}`,
    );
    return response.data;
  },

  async getSubscriptionByEmail(email) {
    const response = await apiClient.get(`/subscriptions/email/${email}`);
    return response.data;
  },

  async getSubscriptionById(id) {
    const response = await apiClient.get(`/subscriptions/${id}`);
    return response.data;
  },

  async updateSubscription(id, data) {
    const payload = {
      student_id: data.student_id,
      email: data.email,
      subject_code: data.subject_code,
    };
    const response = await apiClient.put(`/subscriptions/${id}`, payload);
    return response.data;
  },

  async deleteSubscription(id) {
    const response = await apiClient.delete(`/subscriptions/${id}`);
    return response.data;
  },
};
