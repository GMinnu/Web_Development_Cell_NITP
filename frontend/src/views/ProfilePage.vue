<template>
  <div>
    <h1 class="page-title">👤 My Profile</h1>
    <p class="page-sub">View and update your personal information</p>

    <div class="profile-grid">
      <!-- Left: Profile Card -->
      <div class="card profile-card">
        <div class="avatar">{{ initials }}</div>
        <h2>{{ user?.name }}</h2>
        <span class="role-badge" :class="user?.role">
          {{ user?.role === "super_admin" ? "👑 Super Admin" : "👤 Faculty" }}
        </span>
        <p class="info-line">✉️ {{ user?.email }}</p>
        <p class="info-line">{{ user?.bio || "No bio yet." }}</p>
        <p v-if="user?.contact" class="info-line">📞 {{ user.contact }}</p>
        <p v-if="user?.department" class="info-line">
          🏛️ {{ user.department }}
        </p>
      </div>

      <!-- Right: Edit Form -->
      <div class="card edit-card">
        <h2>Edit Profile</h2>

        <div v-if="error" class="error-msg">{{ error }}</div>
        <div v-if="success" class="success-msg">{{ success }}</div>

        <form @submit.prevent="handleUpdate">
          <div class="form-group">
            <label>Full Name</label>
            <input v-model="form.name" type="text" />
          </div>
          <div class="form-group">
            <label>Bio</label>
            <textarea
              v-model="form.bio"
              rows="3"
              placeholder="Tell us about yourself..."
            ></textarea>
          </div>
          <div class="form-group">
            <label>Contact</label>
            <input
              v-model="form.contact"
              type="text"
              placeholder="Phone or social handle"
            />
          </div>
          <div class="form-group">
            <label>Department</label>
            <input
              v-model="form.department"
              type="text"
              placeholder="e.g. Computer Science"
            />
          </div>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? "Saving..." : "Save Changes" }}
          </button>
        </form>

        <!-- Danger Zone -->
        <div class="danger-zone">
          <h3>⚠️ Danger Zone</h3>
          <p>Deleting your account is permanent and cannot be undone.</p>
          <button class="btn btn-danger" @click="confirmDelete">
            Delete My Account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth.js";
import { profileAPI } from "@/services/api.js";

const router = useRouter();
const auth = useAuthStore();
const user = computed(() => auth.user);
const form = ref({ name: "", bio: "", contact: "", department: "" });
const error = ref("");
const success = ref("");
const loading = ref(false);

const initials = computed(() => {
  if (!user.value?.name) return "?";
  return user.value.name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
});

onMounted(() => {
  if (user.value) {
    form.value.name = user.value.name || "";
    form.value.bio = user.value.bio || "";
    form.value.contact = user.value.contact || "";
    form.value.department = user.value.department || "";
  }
});

async function handleUpdate() {
  error.value = "";
  success.value = "";
  loading.value = true;
  try {
    const res = await profileAPI.updateProfile(form.value);
    auth.user = res.data.user;
    success.value = "Profile updated successfully!";
  } catch (err) {
    error.value = err.response?.data?.error || "Failed to update";
  } finally {
    loading.value = false;
  }
}

async function confirmDelete() {
  if (!confirm("Are you sure? This will permanently delete your account."))
    return;
  try {
    await profileAPI.deleteAccount();
    auth.user = null;
    router.push("/");
  } catch {
    error.value = "Failed to delete account";
  }
}
</script>

<style scoped>
.profile-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  align-items: start;
}
@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

.profile-card {
  text-align: center;
}
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 auto 1rem;
}
.profile-card h2 {
  margin-bottom: 0.5rem;
}
.role-badge {
  display: inline-block;
  padding: 0.2rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  background: rgba(79, 70, 229, 0.2);
  border: 1px solid var(--primary);
  margin-bottom: 1rem;
}
.role-badge.super_admin {
  background: rgba(6, 182, 212, 0.2);
  border-color: var(--accent);
}
.info-line {
  color: var(--muted);
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.edit-card h2 {
  margin-bottom: 1.5rem;
}
.danger-zone {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
}
.danger-zone h3 {
  color: var(--danger);
  margin-bottom: 0.5rem;
}
.danger-zone p {
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}
</style>
