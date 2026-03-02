<template>
  <div>
    <h1 class="page-title">👥 Manage Faculty</h1>
    <p class="page-sub">View, edit and remove faculty members</p>

    <div v-if="error" class="error-msg">{{ error }}</div>
    <div v-if="success" class="success-msg">{{ success }}</div>

    <!-- Edit Form (shows when editing) -->
    <div v-if="editingFaculty" class="card edit-form">
      <h2>Editing: {{ editingFaculty.name }}</h2>
      <div class="two-col">
        <div class="form-group">
          <label>Name</label>
          <input v-model="editForm.name" type="text" />
        </div>
        <div class="form-group">
          <label>Department</label>
          <input v-model="editForm.department" type="text" />
        </div>
      </div>
      <div class="form-group">
        <label>Bio</label>
        <textarea v-model="editForm.bio" rows="3"></textarea>
      </div>
      <div class="form-group">
        <label>Contact</label>
        <input v-model="editForm.contact" type="text" />
      </div>
      <div class="row-btns">
        <button class="btn btn-success" @click="saveEdit" :disabled="saving">
          {{ saving ? "Saving..." : "Save Changes" }}
        </button>
        <button class="btn btn-outline" @click="editingFaculty = null">
          Cancel
        </button>
      </div>
    </div>

    <!-- Faculty Table -->
    <div class="card">
      <div v-if="fetchLoading" class="empty">Loading...</div>
      <div v-else-if="faculty.length === 0" class="empty">
        No faculty found.
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Contact</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="f in faculty" :key="f.id">
            <td>
              <div class="name-cell">
                <div class="mini-av">{{ f.name[0] }}</div>
                {{ f.name }}
              </div>
            </td>
            <td class="muted">{{ f.email }}</td>
            <td>{{ f.department || "—" }}</td>
            <td class="muted">{{ f.contact || "—" }}</td>
            <td>
              <div class="row-btns">
                <button class="btn btn-sm btn-primary" @click="startEdit(f)">
                  Edit
                </button>
                <button
                  class="btn btn-sm btn-danger"
                  @click="removeFaculty(f.id)"
                >
                  Remove
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { adminAPI } from "@/services/api.js";

const faculty = ref([]);
const editingFaculty = ref(null);
const editForm = ref({});
const error = ref("");
const success = ref("");
const saving = ref(false);
const fetchLoading = ref(true);

onMounted(fetchFaculty);

async function fetchFaculty() {
  fetchLoading.value = true;
  try {
    const res = await adminAPI.getAllFaculty();
    faculty.value = res.data.faculty;
  } catch {
    error.value = "Failed to load faculty";
  } finally {
    fetchLoading.value = false;
  }
}

function startEdit(f) {
  editingFaculty.value = f;
  editForm.value = {
    name: f.name,
    bio: f.bio,
    contact: f.contact,
    department: f.department,
  };
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function saveEdit() {
  saving.value = true;
  error.value = "";
  try {
    await adminAPI.updateFaculty(editingFaculty.value.id, editForm.value);
    success.value = "Faculty updated!";
    editingFaculty.value = null;
    await fetchFaculty();
  } catch (err) {
    error.value = err.response?.data?.error || "Update failed";
  } finally {
    saving.value = false;
  }
}

async function removeFaculty(id) {
  if (!confirm("Remove this faculty member?")) return;
  try {
    await adminAPI.deleteFaculty(id);
    success.value = "Removed.";
    await fetchFaculty();
  } catch {
    error.value = "Failed to delete";
  }
}
</script>

<style scoped>
.edit-form {
  margin-bottom: 2rem;
}
.edit-form h2 {
  margin-bottom: 1.5rem;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.row-btns {
  display: flex;
  gap: 0.5rem;
}
.name-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.mini-av {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  flex-shrink: 0;
}
.muted {
  color: var(--muted);
}
.btn-sm {
  padding: 0.3rem 0.75rem;
  font-size: 0.85rem;
}
.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
}
.empty {
  color: var(--muted);
  padding: 2rem;
  text-align: center;
}
</style>
