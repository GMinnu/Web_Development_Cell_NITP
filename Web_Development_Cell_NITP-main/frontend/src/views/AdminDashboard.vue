<template>
  <div>
    <h1 class="page-title">⚙️ Admin Panel</h1>
    <p class="page-sub">
      Logged in as <strong>{{ auth.user?.name }}</strong> ·
      <span class="role-chip" :class="auth.user?.role">
        {{
          auth.user?.role === "super_admin" ? "👑 Super Admin" : "👤 Faculty"
        }}
      </span>
    </p>

    <!-- Faculty: limited view -->
    <div v-if="auth.isFaculty" class="card info-card">
      <h2>👋 Hi, {{ auth.user?.name }}!</h2>
      <p>As a Faculty member you can only view and edit your own profile.</p>
      <router-link to="/profile" class="btn btn-primary"
        >Edit My Profile →</router-link
      >
    </div>

    <!-- Super Admin: full module grid -->
    <div v-if="auth.isSuperAdmin" class="admin-grid">
      <router-link to="/admin/faculty" class="module-card card">
        <div class="module-icon">👥</div>
        <h3>Faculty Profiles</h3>
        <p>Manage all faculty members</p>
        <span class="go">Manage →</span>
      </router-link>

      <router-link to="/admin/notices" class="module-card card">
        <div class="module-icon">📢</div>
        <h3>Notices</h3>
        <p>Post and manage announcements</p>
        <span class="go">Manage →</span>
      </router-link>

      <router-link to="/admin/events" class="module-card card">
        <div class="module-icon">🗓️</div>
        <h3>Events</h3>
        <p>Create and manage club events</p>
        <span class="go">Manage →</span>
      </router-link>

      <router-link to="/admin/news" class="module-card card">
        <div class="module-icon">📰</div>
        <h3>News</h3>
        <p>Write and publish news articles</p>
        <span class="go">Manage →</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/store/auth.js";
const auth = useAuthStore();
</script>

<style scoped>
.role-chip {
  padding: 0.2rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  background: rgba(79, 70, 229, 0.2);
  border: 1px solid var(--primary);
}
.role-chip.super_admin {
  background: rgba(6, 182, 212, 0.2);
  border-color: var(--accent);
}

.info-card {
  max-width: 500px;
}
.info-card h2 {
  margin-bottom: 0.75rem;
}
.info-card p {
  color: var(--muted);
  margin-bottom: 1.5rem;
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}
.module-card {
  text-decoration: none;
  color: var(--text);
  transition:
    transform 0.2s,
    border-color 0.2s;
}
.module-card:hover {
  transform: translateY(-4px);
  border-color: var(--primary);
}
.module-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}
.module-card h3 {
  margin-bottom: 0.5rem;
}
.module-card p {
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}
.go {
  color: var(--accent);
  font-size: 0.9rem;
}
</style>
