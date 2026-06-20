import apiClient from "./apiClient";

export const userService = {
  async getMe() {
    const response = await apiClient.get("/users/me");
    return response.data;
  },
};
