<template>
  <div>
    <h1 class="page-title">🗓️ Manage Events</h1>
    <p class="page-sub">Create and manage upcoming club events</p>

    <div class="manage-grid">
      <!-- Form -->
      <div class="card form-panel">
        <h2>{{ editingId ? "Edit Event" : "New Event" }}</h2>

        <div v-if="error" class="error-msg">{{ error }}</div>
        <div v-if="success" class="success-msg">{{ success }}</div>

        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Title</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="Workshop: Intro to Vue"
              required
            />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="What will happen?"
            ></textarea>
          </div>
          <div class="form-group">
            <label>Date &amp; Time</label>
            <input v-model="form.event_date" type="datetime-local" required />
          </div>
          <div class="form-group">
            <label>Location</label>
            <input
              v-model="form.location"
              type="text"
              placeholder="Room 101 / Online"
            />
          </div>
          <div class="row-btns">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{
                loading ? "Saving..." : editingId ? "Update" : "Create Event"
              }}
            </button>
            <button
              v-if="editingId"
              type="button"
              class="btn btn-outline"
              @click="cancelEdit"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <!-- List -->
      <div class="list-panel">
        <h2>All Events ({{ events.length }})</h2>
        <div v-if="events.length === 0" class="card empty">No events yet.</div>
        <div v-for="e in events" :key="e.id" class="card event-item">
          <span class="date-badge">{{ formatShort(e.event_date) }}</span>
          <h3>{{ e.title }}</h3>
          <p class="muted">{{ e.description }}</p>
          <p class="loc">📍 {{ e.location || "TBA" }}</p>
          <div class="row-btns">
            <button class="btn btn-sm btn-primary" @click="startEdit(e)">
              Edit
            </button>
            <button class="btn btn-sm btn-danger" @click="deleteEvent(e.id)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { adminAPI } from "@/services/api.js";

const events = ref([]);
const form = ref({ title: "", description: "", event_date: "", location: "" });
const editingId = ref(null);
const error = ref("");
const success = ref("");
const loading = ref(false);

onMounted(fetchEvents);

async function fetchEvents() {
  try {
    const r = await adminAPI.getEvents();
    events.value = r.data.events;
  } catch {
    error.value = "Failed to load events";
  }
}

async function handleSubmit() {
  error.value = "";
  success.value = "";
  loading.value = true;
  const payload = {
    ...form.value,
    event_date: new Date(form.value.event_date).toISOString(),
  };
  try {
    if (editingId.value) {
      await adminAPI.updateEvent(editingId.value, payload);
      success.value = "Event updated!";
    } else {
      await adminAPI.createEvent(payload);
      success.value = "Event created!";
    }
    resetForm();
    await fetchEvents();
  } catch (err) {
    error.value = err.response?.data?.error || "Failed";
  } finally {
    loading.value = false;
  }
}

function startEdit(e) {
  editingId.value = e.id;
  form.value = {
    title: e.title,
    description: e.description,
    location: e.location,
    event_date: new Date(e.event_date).toISOString().slice(0, 16),
  };
  window.scrollTo({ top: 0, behavior: "smooth" });
}
function cancelEdit() {
  editingId.value = null;
  resetForm();
}
function resetForm() {
  form.value = { title: "", description: "", event_date: "", location: "" };
  editingId.value = null;
}

async function deleteEvent(id) {
  if (!confirm("Delete this event?")) return;
  try {
    await adminAPI.deleteEvent(id);
    success.value = "Deleted";
    await fetchEvents();
  } catch {
    error.value = "Failed to delete";
  }
}

function formatShort(d) {
  return new Date(d).toLocaleDateString("en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}
</script>

<style scoped>
.manage-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}
@media (max-width: 900px) {
  .manage-grid {
    grid-template-columns: 1fr;
  }
}
.form-panel h2,
.list-panel h2 {
  margin-bottom: 1.5rem;
}
.event-item {
  margin-bottom: 1rem;
}
.date-badge {
  display: inline-block;
  background: rgba(6, 182, 212, 0.2);
  border: 1px solid var(--accent);
  color: var(--accent);
  padding: 0.2rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}
.event-item h3 {
  margin-bottom: 0.4rem;
}
.muted {
  color: var(--muted);
  font-size: 0.9rem;
  margin: 0.4rem 0;
}
.loc {
  color: var(--muted);
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
}
.row-btns {
  display: flex;
  gap: 0.5rem;
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
