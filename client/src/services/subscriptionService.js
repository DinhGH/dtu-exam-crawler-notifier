import apiClient from "./apiClient";

export const subscriptionService = {
  async subscribe(data) {
    const dataToSend = {
      full_name: data.fullName,
      email: data.email,
      subject_code: data.subjectCode,
      subject_name: data.subjectName,
    };

    const response = apiClient.post("/subscriptions", dataToSend);
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
};
