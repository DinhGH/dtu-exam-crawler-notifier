import apiClient from "./apiClient";

export const subscriptionService = {
  async subscribe(data) {
    const response = await apiClient.post("/subscriptions", data);
    return response.data;
  },

  async getSubscriptionByEmail(email) {
    const response = await apiClient.get(`/subscriptions?email=${email}`);
    return response.data;
  },
};
