<template>
  <div class="auth-page">
    <div class="auth-card card">
      <div class="auth-header">
        <span class="auth-icon">🔐</span>
        <h1 class="page-title">Welcome Back</h1>
        <p class="page-sub">Login to your WDC account</p>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email Address</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="you@college.edu"
            required
          />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Your password"
            required
          />
        </div>
        <button
          type="submit"
          class="btn btn-primary full-width"
          :disabled="loading"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <p class="auth-footer">
        Don't have an account?
        <router-link to="/signup">Sign up here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth.js";

const router = useRouter();
const auth = useAuthStore();
const form = ref({ email: "", password: "" });
const error = ref("");
const loading = ref(false);

async function handleLogin() {
  error.value = "";
  loading.value = true;
  const result = await auth.login(form.value.email, form.value.password);
  loading.value = false;

  if (result.success) {
    router.push("/admin");
  } else {
    error.value = result.error;
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}
.auth-card {
  width: 100%;
  max-width: 420px;
}
.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}
.auth-icon {
  font-size: 2.5rem;
}
.full-width {
  width: 100%;
  margin-top: 0.5rem;
}
.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--muted);
  font-size: 0.9rem;
}
.auth-footer a {
  color: var(--accent);
  text-decoration: none;
}
</style>
