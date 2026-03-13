# ⚡ WDC Platform — Web Development Club

A full-stack web application built with **Flask** (Python backend) + **Vue.js** (frontend) + **MySQL** database.

---

## 📁 Project Structure

```
wdc-platform/
│
├── backend/                    ← Flask Python backend
│   ├── app.py                  ← 🚀 Main entry point (run this!)
│   ├── config.py               ← All settings (DB URL, JWT secret, etc.)
│   ├── extensions.py           ← Flask plugin setup (db, jwt, limiter)
│   ├── models.py               ← Database tables (User, Notice, Event, News)
│   ├── requirements.txt        ← Python packages to install
│   └── routes/
│       ├── auth_routes.py      ← Signup, Login, Logout, /me
│       ├── profile_routes.py   ← View/Update/Delete profile (CRUD)
│       └── admin_routes.py     ← Admin panel (Faculty, Notices, Events, News)
│
└── frontend/                   ← Vue.js frontend
    ├── index.html              ← HTML entry point (has TinyMCE CDN)
    ├── vite.config.js          ← Vite build config
    ├── package.json            ← Node.js dependencies
    └── src/
        ├── main.js             ← Vue app entry point
        ├── App.vue             ← Root component + navbar
        ├── services/
        │   └── api.js          ← All API calls (axios)
        ├── store/
        │   └── auth.js         ← Global auth state (Pinia)
        ├── router/
        │   └── index.js        ← Routes + navigation guards
        └── views/
            ├── HomePage.vue    ← Public landing page
            ├── LoginPage.vue   ← Login form
            ├── SignupPage.vue  ← Signup form with live validation
            ├── ProfilePage.vue ← View/edit your profile (CRUD)
            ├── AdminDashboard.vue ← Role-based admin home
            └── admin/
                ├── ManageFaculty.vue  ← Faculty CRUD (Super Admin)
                ├── ManageNotices.vue  ← Notices CRUD + TinyMCE editor
                ├── ManageEvents.vue   ← Events CRUD
                └── ManageNews.vue     ← News articles CRUD
```

---

## 🛠️ SETUP GUIDE (Step by Step)

### Step 1: Create the MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE wdc_db;
```

### Step 2: Setup the Backend

```bash
# Go to backend folder
cd wdc-platform/backend

# Install Python packages
pip install -r requirements.txt

# Edit config.py and update the database URL:
# "mysql+pymysql://root:yourpassword@localhost/wdc_db"
# Replace "yourpassword" with your MySQL root password

# Start the Flask server
python app.py
```

Backend will run at: **http://localhost:5000**

### Step 3: Setup the Frontend

```bash
# Go to frontend folder
cd wdc-platform/frontend

# Install Node.js packages
npm install

# Start the Vue dev server
npm run dev
```

Frontend will run at: **http://localhost:5173**

### Step 4: Create a Super Admin Account

Go to http://localhost:5173/signup and create an account with role **Super Admin**.

---

## ✅ Features Checklist

### Backend

- [x] **Secure Signup API** — bcrypt password hashing + input validation
- [x] **Secure Login API** — bcrypt.checkpw + returns JWT cookie
- [x] **JWT Authentication** — using flask-jwt-extended
- [x] **GET /api/auth/me** — decodes JWT token, returns user details
- [x] **MySQL Integration** — via SQLAlchemy ORM
- [x] **Profile CRUD** — GET, PUT (update name/bio/contact), DELETE
- [x] **BONUS: Rate Limiting** — 5/min on signup, 10/min on login
- [x] **BONUS: HttpOnly Cookies** — JWT stored in HttpOnly cookie (XSS safe)
- [x] **BONUS: XSS Sanitization** — bleach library sanitizes HTML in notices

### Full Stack

- [x] **WDC Platform redesign** — modern dark theme
- [x] **Role-Based Access Control**
  - Faculty: can only view/edit their own profile
  - Super Admin: full access to all modules
- [x] **Manage Faculty Profiles** — table with edit/delete
- [x] **Add/Manage Notices** — CRUD with rich text editor
- [x] **Add/Manage Events** — CRUD with date/location
- [x] **Add/Manage News** — CRUD for articles
- [x] **BONUS: TinyMCE Rich Text Editor** — in Notices form

---

## 🔗 API Endpoints Reference

| Method | URL                    | Auth Required  | Description                  |
| ------ | ---------------------- | -------------- | ---------------------------- |
| POST   | /api/auth/signup       | No             | Register new user            |
| POST   | /api/auth/login        | No             | Login (sets HttpOnly cookie) |
| POST   | /api/auth/logout       | No             | Clear JWT cookie             |
| GET    | /api/auth/me           | ✅             | Decode token, get user info  |
| GET    | /api/profile/          | ✅             | Get own profile              |
| PUT    | /api/profile/update    | ✅             | Update name, bio, contact    |
| DELETE | /api/profile/delete    | ✅             | Delete own account           |
| GET    | /api/admin/faculty     | ✅ Super Admin | List all faculty             |
| PUT    | /api/admin/faculty/:id | ✅             | Update faculty profile       |
| DELETE | /api/admin/faculty/:id | ✅ Super Admin | Remove faculty               |
| GET    | /api/admin/notices     | Public         | List notices                 |
| POST   | /api/admin/notices     | ✅ Super Admin | Create notice                |
| PUT    | /api/admin/notices/:id | ✅ Super Admin | Update notice                |
| DELETE | /api/admin/notices/:id | ✅ Super Admin | Delete notice                |
| GET    | /api/admin/events      | Public         | List events                  |
| POST   | /api/admin/events      | ✅ Super Admin | Create event                 |
| PUT    | /api/admin/events/:id  | ✅ Super Admin | Update event                 |
| DELETE | /api/admin/events/:id  | ✅ Super Admin | Delete event                 |
| GET    | /api/admin/news        | Public         | List news                    |
| POST   | /api/admin/news        | ✅ Super Admin | Create news                  |
| PUT    | /api/admin/news/:id    | ✅ Super Admin | Update news                  |
| DELETE | /api/admin/news/:id    | ✅ Super Admin | Delete news                  |

---

## 🔐 Security Features Explained

1. **bcrypt hashing** — Passwords are hashed with a random salt. The original password is never stored.
2. **JWT tokens** — After login, a signed token identifies the user. The server never stores session data.
3. **HttpOnly Cookies** — The JWT is stored in a cookie that JavaScript cannot read, protecting against XSS theft.
4. **Rate Limiting** — Limits login attempts per IP to prevent brute force attacks.
5. **XSS Sanitization** — The `bleach` library strips dangerous HTML tags before saving to database.
6. **Role-Based Access** — Backend checks user role before every protected operation.
