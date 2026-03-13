import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/store/auth.js";

const HomePage = () => import("@/views/HomePage.vue");
const LoginPage = () => import("@/views/LoginPage.vue");
const SignupPage = () => import("@/views/SignupPage.vue");
const ProfilePage = () => import("@/views/ProfilePage.vue");
const AdminDashboard = () => import("@/views/AdminDashboard.vue");
const ManageFaculty = () => import("@/views/admin/ManageFaculty.vue");
const ManageNotices = () => import("@/views/admin/ManageNotices.vue");
const ManageEvents = () => import("@/views/admin/ManageEvents.vue");
const ManageNews = () => import("@/views/admin/ManageNews.vue");

const routes = [
  { path: "/", component: HomePage },
  { path: "/login", component: LoginPage },
  { path: "/signup", component: SignupPage },

  { path: "/profile", component: ProfilePage, meta: { requiresAuth: true } },
  { path: "/admin", component: AdminDashboard, meta: { requiresAuth: true } },
  {
    path: "/admin/faculty",
    component: ManageFaculty,
    meta: { requiresAuth: true, requiresSuperAdmin: true },
  },
  {
    path: "/admin/notices",
    component: ManageNotices,
    meta: { requiresAuth: true, requiresSuperAdmin: true },
  },
  {
    path: "/admin/events",
    component: ManageEvents,
    meta: { requiresAuth: true, requiresSuperAdmin: true },
  },
  {
    path: "/admin/news",
    component: ManageNews,
    meta: { requiresAuth: true, requiresSuperAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard — runs before every page change
router.beforeEach(async (to) => {
  const auth = useAuthStore();

  // Check if user is logged in (only once)
  if (auth.user === null) {
    await auth.fetchCurrentUser();
  }

  // Not logged in → redirect to login
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { path: "/login" };
  }

  // Not super admin → redirect to profile
  if (to.meta.requiresSuperAdmin && !auth.isSuperAdmin) {
    return { path: "/profile" };
  }
});

export default router;
