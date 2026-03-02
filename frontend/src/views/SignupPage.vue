<template>
  <div class="auth-page">
    <div class="auth-card card">
      <div class="auth-header">
        <span class="auth-icon">✨</span>
        <h1 class="page-title">Join WDC</h1>
        <p class="page-sub">Create your account</p>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>
      <div v-if="success" class="success-msg">{{ success }}</div>

      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label>Full Name</label>
          <input
            v-model="form.name"
            type="text"
            placeholder="John Doe"
            required
          />
        </div>
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
            placeholder="Min 8 chars + a number"
            required
          />
          <!-- Live password strength hints -->
          <ul class="hints">
            <li :class="{ met: form.password.length >= 8 }">
              ✓ At least 8 characters
            </li>
            <li :class="{ met: /[A-Za-z]/.test(form.password) }">
              ✓ Contains a letter
            </li>
            <li :class="{ met: /\d/.test(form.password) }">
              ✓ Contains a number
            </li>
          </ul>
        </div>
        <div class="form-group">
          <label>Role</label>
          <select v-model="form.role">
            <option value="faculty">Faculty</option>
            <option value="super_admin">Super Admin</option>
          </select>
        </div>
        <button
          type="submit"
          class="btn btn-primary full-width"
          :disabled="loading"
        >
          {{ loading ? "Creating account..." : "Create Account" }}
        </button>
      </form>

      <p class="auth-footer">
        Already have an account?
        <router-link to="/login">Login here</router-link>
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
const form = ref({ name: "", email: "", password: "", role: "faculty" });
const error = ref("");
const success = ref("");
const loading = ref(false);

async function handleSignup() {
  error.value = "";
  success.value = "";
  loading.value = true;
  const result = await auth.signup(
    form.value.name,
    form.value.email,
    form.value.password,
    form.value.role,
  );
  loading.value = false;

  if (result.success) {
    success.value = "Account created! Redirecting to login...";
    setTimeout(() => router.push("/login"), 1500);
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

.hints {
  list-style: none;
  margin-top: 0.5rem;
  font-size: 0.8rem;
}
.hints li {
  color: var(--muted);
  padding: 0.1rem 0;
}
.hints li.met {
  color: var(--success);
}
</style>
