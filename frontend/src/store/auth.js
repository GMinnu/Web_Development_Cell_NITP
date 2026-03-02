import { defineStore } from "pinia";
import { authAPI } from "@/services/api.js";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null, // logged in user object or null
    loading: false,
    error: null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.user,
    isSuperAdmin: (state) => state.user?.role === "super_admin",
    isFaculty: (state) => state.user?.role === "faculty",
  },

  actions: {
    // Called on app start to check if already logged in
    async fetchCurrentUser() {
      try {
        const res = await authAPI.getMe();
        this.user = res.data.user;
      } catch {
        this.user = null;
      }
    },

    async login(email, password) {
      this.loading = true;
      this.error = null;
      try {
        const res = await authAPI.login({ email, password });
        this.user = res.data.user;
        return { success: true };
      } catch (err) {
        this.error = err.response?.data?.error || "Login failed";
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    async signup(name, email, password, role = "faculty") {
      this.loading = true;
      this.error = null;
      try {
        const res = await authAPI.signup({ name, email, password, role });
        return { success: true, data: res.data };
      } catch (err) {
        this.error = err.response?.data?.error || "Signup failed";
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      try {
        await authAPI.logout();
      } finally {
        this.user = null;
      }
    },
  },
});
