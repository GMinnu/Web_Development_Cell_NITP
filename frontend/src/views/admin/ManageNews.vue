<template>
  <div>
    <h1 class="page-title">📰 Manage News</h1>
    <p class="page-sub">Write and publish news articles for the club</p>

    <div class="manage-grid">
      <!-- Form -->
      <div class="card form-panel">
        <h2>{{ editingId ? "Edit Article" : "New Article" }}</h2>

        <div v-if="error" class="error-msg">{{ error }}</div>
        <div v-if="success" class="success-msg">{{ success }}</div>

        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Title</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="WDC wins Hackathon 2025!"
              required
            />
          </div>
          <div class="form-group">
            <label>Body</label>
            <textarea
              v-model="form.body"
              rows="8"
              placeholder="Write your article here..."
              required
            ></textarea>
          </div>
          <div class="row-btns">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? "Saving..." : editingId ? "Update" : "Publish" }}
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
        <h2>All Articles ({{ news.length }})</h2>
        <div v-if="news.length === 0" class="card empty">No articles yet.</div>
        <div v-for="item in news" :key="item.id" class="card news-item">
          <h3>{{ item.title }}</h3>
          <p class="preview">
            {{ item.body.substring(0, 150)
            }}{{ item.body.length > 150 ? "..." : "" }}
          </p>
          <div class="news-footer">
            <span class="date">{{ formatDate(item.created_at) }}</span>
            <div class="row-btns">
              <button class="btn btn-sm btn-primary" @click="startEdit(item)">
                Edit
              </button>
              <button
                class="btn btn-sm btn-danger"
                @click="deleteNews(item.id)"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { adminAPI } from "@/services/api.js";

const news = ref([]);
const form = ref({ title: "", body: "" });
const editingId = ref(null);
const error = ref("");
const success = ref("");
const loading = ref(false);

onMounted(fetchNews);

async function fetchNews() {
  try {
    const r = await adminAPI.getNews();
    news.value = r.data.news;
  } catch {
    error.value = "Failed to load news";
  }
}

async function handleSubmit() {
  error.value = "";
  success.value = "";
  loading.value = true;
  try {
    if (editingId.value) {
      await adminAPI.updateNews(editingId.value, form.value);
      success.value = "Article updated!";
    } else {
      await adminAPI.createNews(form.value);
      success.value = "Article published!";
    }
    resetForm();
    await fetchNews();
  } catch (err) {
    error.value = err.response?.data?.error || "Failed";
  } finally {
    loading.value = false;
  }
}

function startEdit(item) {
  editingId.value = item.id;
  form.value = { title: item.title, body: item.body };
  window.scrollTo({ top: 0, behavior: "smooth" });
}
function cancelEdit() {
  editingId.value = null;
  resetForm();
}
function resetForm() {
  form.value = { title: "", body: "" };
  editingId.value = null;
}

async function deleteNews(id) {
  if (!confirm("Delete this article?")) return;
  try {
    await adminAPI.deleteNews(id);
    success.value = "Deleted";
    await fetchNews();
  } catch {
    error.value = "Failed to delete";
  }
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
.news-item {
  margin-bottom: 1rem;
}
.news-item h3 {
  margin-bottom: 0.5rem;
}
.preview {
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}
.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.date {
  color: var(--muted);
  font-size: 0.8rem;
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
