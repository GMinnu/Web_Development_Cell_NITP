<template>
  <div>
    <h1 class="page-title">📢 Manage Notices</h1>
    <p class="page-sub">Create and manage club announcements</p>

    <div class="manage-grid">
      <!-- Form -->
      <div class="card form-panel">
        <h2>{{ editingId ? "Edit Notice" : "New Notice" }}</h2>

        <div v-if="error" class="error-msg">{{ error }}</div>
        <div v-if="success" class="success-msg">{{ success }}</div>

        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Title</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="Notice title"
              required
            />
          </div>

          <div class="form-group">
            <label>Content</label>
            <!-- Rich Text Toolbar -->
            <div class="rich-toolbar">
              <button type="button" @click="wrap('**', '**')" title="Bold">
                <b>B</b>
              </button>
              <button type="button" @click="wrap('*', '*')" title="Italic">
                <i>I</i>
              </button>
              <button type="button" @click="addBullet()" title="Bullet">
                • List
              </button>
              <button type="button" @click="addHeading()" title="Heading">
                H1
              </button>
            </div>
            <textarea
              v-model="form.content"
              ref="contentRef"
              rows="10"
              placeholder="Write your notice content here..."
              class="rich-textarea"
              required
            ></textarea>
            <p class="hint">
              💡 Tip: Use **bold**, *italic*, or bullet points in your content
            </p>
          </div>

          <!-- Live Preview -->
          <div v-if="form.content" class="preview-box">
            <p class="preview-label">Preview:</p>
            <div class="preview-content">{{ form.content }}</div>
          </div>

          <div class="row-btns">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{
                loading
                  ? "Saving..."
                  : editingId
                    ? "Update Notice"
                    : "Post Notice"
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

      <!-- Notices List -->
      <div class="list-panel">
        <h2>All Notices ({{ notices.length }})</h2>
        <div v-if="fetchLoading" class="card empty">Loading...</div>
        <div v-else-if="notices.length === 0" class="card empty">
          No notices yet.
        </div>
        <div v-for="n in notices" :key="n.id" class="card notice-item">
          <div class="notice-header">
            <h3>{{ n.title }}</h3>
            <span class="date">{{ formatDate(n.created_at) }}</span>
          </div>
          <p class="preview">
            {{ n.content.substring(0, 180)
            }}{{ n.content.length > 180 ? "..." : "" }}
          </p>
          <div class="row-btns">
            <button class="btn btn-sm btn-primary" @click="startEdit(n)">
              Edit
            </button>
            <button class="btn btn-sm btn-danger" @click="deleteNotice(n.id)">
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

const notices = ref([]);
const form = ref({ title: "", content: "" });
const editingId = ref(null);
const error = ref("");
const success = ref("");
const loading = ref(false);
const fetchLoading = ref(true);
const contentRef = ref(null); // Reference to textarea element

onMounted(fetchNotices);

async function fetchNotices() {
  fetchLoading.value = true;
  try {
    const res = await adminAPI.getNotices();
    notices.value = res.data.notices;
  } catch {
    error.value = "Failed to load notices";
  } finally {
    fetchLoading.value = false;
  }
}

async function handleSubmit() {
  error.value = "";
  success.value = "";
  loading.value = true;

  try {
    if (editingId.value) {
      await adminAPI.updateNotice(editingId.value, form.value);
      success.value = "✅ Notice updated!";
    } else {
      await adminAPI.createNotice(form.value);
      success.value = "✅ Notice posted!";
    }
    resetForm();
    await fetchNotices();
  } catch (err) {
    error.value = err.response?.data?.error || "Failed to save notice";
  } finally {
    loading.value = false;
  }
}

function startEdit(n) {
  editingId.value = n.id;
  form.value.title = n.title;
  form.value.content = n.content;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function cancelEdit() {
  editingId.value = null;
  resetForm();
}

function resetForm() {
  form.value = { title: "", content: "" };
  editingId.value = null;
}

async function deleteNotice(id) {
  if (!confirm("Delete this notice?")) return;
  try {
    await adminAPI.deleteNotice(id);
    success.value = "Notice deleted";
    await fetchNotices();
  } catch {
    error.value = "Failed to delete";
  }
}

// ── Toolbar helper functions ──────────────────────────────
function wrap(before, after) {
  // Wraps selected text with formatting characters
  const ta = contentRef.value;
  const start = ta.selectionStart;
  const end = ta.selectionEnd;
  const selected = form.value.content.substring(start, end) || "text";
  form.value.content =
    form.value.content.substring(0, start) +
    before +
    selected +
    after +
    form.value.content.substring(end);
}

function addBullet() {
  form.value.content += "\n• ";
  contentRef.value?.focus();
}

function addHeading() {
  form.value.content += "\n# ";
  contentRef.value?.focus();
}

function formatDate(d) {
  return new Date(d).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
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

/* Rich text toolbar */
.rich-toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: var(--dark);
  border: 1px solid var(--border);
  border-bottom: none;
  border-radius: 8px 8px 0 0;
}
.rich-toolbar button {
  background: var(--card-bg);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.3rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}
.rich-toolbar button:hover {
  background: var(--primary);
  border-color: var(--primary);
}

.rich-textarea {
  border-radius: 0 0 8px 8px !important;
  font-family: "Courier New", monospace;
  font-size: 0.95rem;
  line-height: 1.6;
  resize: vertical;
}

.hint {
  color: var(--muted);
  font-size: 0.8rem;
  margin-top: 0.4rem;
}

/* Live preview box */
.preview-box {
  background: var(--dark);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}
.preview-label {
  color: var(--accent);
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}
.preview-content {
  color: var(--text);
  font-size: 0.9rem;
  white-space: pre-wrap;
  line-height: 1.6;
}

/* Notice list */
.notice-item {
  margin-bottom: 1rem;
}
.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.date {
  color: var(--muted);
  font-size: 0.8rem;
}
.preview {
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 1rem;
  white-space: pre-wrap;
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
