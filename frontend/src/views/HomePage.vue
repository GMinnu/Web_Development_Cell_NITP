<template>
  <div class="home">
    <!-- HERO -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">⚡ Web Development Club</div>
        <h1 class="hero-title">
          Build. Create. <span class="gradient-text">Innovate.</span>
        </h1>
        <p class="hero-sub">
          A community of passionate developers and designers at the forefront of
          modern web technology.
        </p>
        <div class="hero-buttons">
          <!-- Only show these buttons if NOT logged in -->
          <template v-if="!auth.isLoggedIn">
            <router-link to="/signup" class="btn btn-primary"
              >Join the Club</router-link
            >
            <router-link to="/login" class="btn btn-outline"
              >Login →</router-link
            >
          </template>
          <!-- Show this if already logged in -->
          <template v-else>
            <router-link to="/admin" class="btn btn-primary"
              >Go to Admin Panel →</router-link
            >
          </template>
        </div>
      </div>

      <div class="hero-visual">
        <div class="code-block">
          <span class="code-line"><span class="kw">const</span> wdc = {</span>
          <span class="code-line"
            >&nbsp;&nbsp;passion: <span class="str">"unlimited"</span>,</span
          >
          <span class="code-line"
            >&nbsp;&nbsp;skills: <span class="str">"growing"</span>,</span
          >
          <span class="code-line"
            >&nbsp;&nbsp;members: <span class="str">"awesome"</span></span
          >
          <span class="code-line">};</span>
        </div>
      </div>
    </section>

    <!-- NOTICES -->
    <section class="section">
      <h2 class="section-title">📢 Latest Notices</h2>
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else class="cards-grid">
        <div
          v-for="notice in notices.slice(0, 3)"
          :key="notice.id"
          class="card notice-card"
        >
          <h3>{{ notice.title }}</h3>
          <div class="notice-body" v-html="notice.content"></div>
          <span class="date">{{ formatDate(notice.created_at) }}</span>
        </div>
        <p v-if="notices.length === 0" class="empty">No notices yet.</p>
      </div>
    </section>

    <!-- EVENTS -->
    <section class="section">
      <h2 class="section-title">🗓️ Upcoming Events</h2>
      <div class="cards-grid">
        <div v-for="event in events.slice(0, 3)" :key="event.id" class="card">
          <div class="event-date-badge">
            {{ formatEventDate(event.event_date) }}
          </div>
          <h3>{{ event.title }}</h3>
          <p class="muted-text">{{ event.description }}</p>
          <span class="location">📍 {{ event.location || "TBA" }}</span>
        </div>
        <p v-if="events.length === 0" class="empty">No events yet.</p>
      </div>
    </section>

    <!-- NEWS -->
    <section class="section">
      <h2 class="section-title">📰 Latest News</h2>
      <div class="news-list">
        <div
          v-for="item in news.slice(0, 4)"
          :key="item.id"
          class="card news-item"
        >
          <div>
            <h3>{{ item.title }}</h3>
            <p class="muted-text">{{ item.body.substring(0, 150) }}...</p>
          </div>
          <span class="date">{{ formatDate(item.created_at) }}</span>
        </div>
        <p v-if="news.length === 0" class="empty">No news yet.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { adminAPI } from "@/services/api.js";
import { useAuthStore } from "@/store/auth.js";
const auth = useAuthStore();
const notices = ref([]);
const events = ref([]);
const news = ref([]);
const loading = ref(true);

onMounted(async () => {
  const [n, e, nw] = await Promise.all([
    adminAPI.getNotices().catch(() => ({ data: { notices: [] } })),
    adminAPI.getEvents().catch(() => ({ data: { events: [] } })),
    adminAPI.getNews().catch(() => ({ data: { news: [] } })),
  ]);
  notices.value = n.data.notices || [];
  events.value = e.data.events || [];
  news.value = nw.data.news || [];
  loading.value = false;
});

function formatDate(d) {
  return new Date(d).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}
function formatEventDate(d) {
  return new Date(d).toLocaleDateString("en-US", {
    day: "numeric",
    month: "short",
  });
}
</script>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  padding: 4rem 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 3rem;
}
@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
  }
}

.hero-badge {
  display: inline-block;
  padding: 0.3rem 1rem;
  background: rgba(79, 70, 229, 0.2);
  border: 1px solid var(--primary);
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--accent);
  margin-bottom: 1rem;
}
.hero-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1rem;
}
.gradient-text {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub {
  color: var(--muted);
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}
.hero-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}
.btn-outline:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.code-block {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 2rem;
  font-family: "Courier New", monospace;
  font-size: 1.05rem;
}
.code-line {
  display: block;
  padding: 0.2rem 0;
}
.kw {
  color: #7c3aed;
}
.str {
  color: #10b981;
}

.section {
  margin-bottom: 3rem;
}
.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.notice-card h3 {
  margin-bottom: 0.75rem;
}
.notice-body {
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}
.date {
  color: var(--muted);
  font-size: 0.8rem;
}
.muted-text {
  color: var(--muted);
  font-size: 0.9rem;
  margin: 0.5rem 0;
}
.location {
  color: var(--muted);
  font-size: 0.85rem;
}

.event-date-badge {
  display: inline-block;
  background: rgba(6, 182, 212, 0.2);
  border: 1px solid var(--accent);
  color: var(--accent);
  padding: 0.2rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-bottom: 0.75rem;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.news-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}
.news-item h3 {
  margin-bottom: 0.4rem;
}

.loading {
  color: var(--muted);
  padding: 2rem;
  text-align: center;
}
.empty {
  color: var(--muted);
  font-style: italic;
}
</style>
