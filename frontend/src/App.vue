<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <span class="brand-icon">⚡</span>
        <span class="brand-text">WDC Platform</span>
      </div>

      <div class="nav-links">
        <router-link to="/">Home</router-link>

        <template v-if="auth.isLoggedIn">
          <router-link to="/profile">My Profile</router-link>
          <router-link to="/admin">Admin Panel</router-link>
          <span class="user-badge" :class="auth.user.role">
            {{
              auth.user.role === "super_admin" ? "👑 Super Admin" : "👤 Faculty"
            }}
          </span>
          <button class="btn-logout" @click="handleLogout">Logout</button>
        </template>

        <template v-else>
          <router-link to="/login">Login</router-link>
          <router-link to="/signup" class="btn-signup">Sign Up</router-link>
        </template>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/store/auth.js";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

async function handleLogout() {
  await auth.logout();
  router.push("/login");
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #4f46e5;
  --secondary: #7c3aed;
  --accent: #06b6d4;
  --dark: #0f172a;
  --card-bg: #1e293b;
  --text: #e2e8f0;
  --muted: #94a3b8;
  --success: #10b981;
  --danger: #ef4444;
  --border: #334155;
}

body {
  font-family: "Segoe UI", system-ui, sans-serif;
  background: var(--dark);
  color: var(--text);
  min-height: 100vh;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: var(--card-bg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--accent);
}

.brand-icon {
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links a {
  color: var(--muted);
  text-decoration: none;
  transition: color 0.2s;
}
.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--accent);
}

.user-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  background: rgba(79, 70, 229, 0.2);
  border: 1px solid var(--primary);
}
.user-badge.super_admin {
  background: rgba(6, 182, 212, 0.2);
  border-color: var(--accent);
}

.btn-logout {
  background: transparent;
  border: 1px solid var(--danger);
  color: var(--danger);
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-logout:hover {
  background: var(--danger);
  color: white;
}

.btn-signup {
  background: var(--primary) !important;
  color: white !important;
  padding: 0.4rem 1rem;
  border-radius: 6px;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* ===== Reusable Styles (used across all pages) ===== */
.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}
.form-group label {
  display: block;
  color: var(--muted);
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
}
.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: var(--dark);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 1rem;
  transition: border-color 0.2s;
}
.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}
.btn-primary {
  background: var(--primary);
  color: white;
}
.btn-primary:hover {
  background: var(--secondary);
}
.btn-danger {
  background: var(--danger);
  color: white;
}
.btn-danger:hover {
  opacity: 0.85;
}
.btn-success {
  background: var(--success);
  color: white;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-msg {
  color: var(--danger);
  background: rgba(239, 68, 68, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}
.success-msg {
  color: var(--success);
  background: rgba(16, 185, 129, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.page-sub {
  color: var(--muted);
  margin-bottom: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
th {
  color: var(--muted);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
tr:hover td {
  background: rgba(255, 255, 255, 0.03);
}
</style>
