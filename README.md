# 🏠 Dormitory Management System

A Django web app (Persian interface) for running a university dormitory: define dorms and rooms, register students and assign them to rooms.

---

## 🎯 The Problem

Dormitory staff often juggle spreadsheets to track which student lives in which room, how full each room is and who asked to share with whom. This app keeps all of it in one place.

## ✨ Features

| Area | What it does |
|---|---|
| Dorm management | Create and edit dorms (code, status, gender) |
| Room management | Rooms linked to a dorm, with capacity and occupancy |
| Student management | Student profiles (student number, grade, contact details, native/non-native, paying, early bird, noise sensitivity) |
| Room assignment | Assign a student to a room and confirm the assignment |
| Roommate requests | A student can request a specific roommate |
| Accounts | Registration, login and logout; an admin setting can turn new registrations on or off |
| Admin | Django admin site for all data |

<!-- TODO: add screenshots of the dashboard, e.g. ![Dashboard](docs/dashboard.png) -->

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 4.1 |
| Database | SQLite |
| Serving | Gunicorn + Nginx |
| Packaging | Docker, Docker Compose |
| CI | GitHub Actions |

## 🚀 Getting Started

### Locally

```bash
git clone https://github.com/mersad31/Dormitory-Management-Sysytem.git
cd Dormitory-Management-Sysytem
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://localhost:8000>.

### With Docker

```bash
docker compose up --build
```

## 🗺️ Main Pages

| URL | Page |
|---|---|
| `/` | Home |
| `/login`, `/logout`, `/register` | Authentication |
| `/dorm-management` | Dorms |
| `/room-management` | Rooms |
| `/student-management` | Students |

## 📂 Repository Layout

| Path | Purpose |
|---|---|
| `DormManagementSystem/` | Django project settings and URLs |
| `Panel/` | Main app: models, views, migrations |
| `Templates/`, `StaticFiles/` | HTML templates and static assets |
| `Dockerfile`, `docker-compose.yml`, `nginx.conf` | Container setup |

## 📝 License

MIT License.
