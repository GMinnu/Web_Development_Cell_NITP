import axios from "axios";

// withCredentials: true is REQUIRED for HttpOnly cookies to work
const api = axios.create({
  baseURL: "http://localhost:5000/api",
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

// ── AUTH ──────────────────────────────────────────
export const authAPI = {
  signup: (data) => api.post("/auth/signup", data),
  login: (data) => api.post("/auth/login", data),
  logout: () => api.post("/auth/logout"),
  getMe: () => api.get("/auth/me"),
};

// ── PROFILE (CRUD) ────────────────────────────────
export const profileAPI = {
  getProfile: () => api.get("/profile/"),
  updateProfile: (data) => api.put("/profile/update", data),
  deleteAccount: () => api.delete("/profile/delete"),
};

// ── ADMIN ─────────────────────────────────────────
export const adminAPI = {
  // Faculty
  getAllFaculty: () => api.get("/admin/faculty"),
  updateFaculty: (id, data) => api.put(`/admin/faculty/${id}`, data),
  deleteFaculty: (id) => api.delete(`/admin/faculty/${id}`),

  // Notices
  getNotices: () => api.get("/admin/notices"),
  createNotice: (data) => api.post("/admin/notices", data),
  updateNotice: (id, data) => api.put(`/admin/notices/${id}`, data),
  deleteNotice: (id) => api.delete(`/admin/notices/${id}`),

  // Events
  getEvents: () => api.get("/admin/events"),
  createEvent: (data) => api.post("/admin/events", data),
  updateEvent: (id, data) => api.put(`/admin/events/${id}`, data),
  deleteEvent: (id) => api.delete(`/admin/events/${id}`),

  // News
  getNews: () => api.get("/admin/news"),
  createNews: (data) => api.post("/admin/news", data),
  updateNews: (id, data) => api.put(`/admin/news/${id}`, data),
  deleteNews: (id) => api.delete(`/admin/news/${id}`),
};

export default api;
