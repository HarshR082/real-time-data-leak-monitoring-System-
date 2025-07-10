# 🚨 Data Sentinel API

**Status: 🚧 Development Phase (Alpha) 🚧**

Data Sentinel is a FastAPI-powered backend for monitoring, storing, and managing potential data leaks found on the public web. It is designed to help security teams detect, track, and analyze suspicious disclosures, with plans for automated scraping, alerting, and advanced analysis.

---

## 🌟 Project Goals

- Central API to manage detected data leaks
- User authentication with JWT
- Admin capabilities (add / delete / view events)
- Automated scraping of known paste sites
- User-defined keywords to watch for
- Alerts when new leaks match keywords

---

## ✅ Current Features

- [x] User Registration & Login (JWT)
- [x] CRUD for Leak Events (admin-protected)
- [x] CRUD for Keywords
- [x] Search & Filter leak events by title/description/severity
- [x] Pastebin scraping module
- [x] Background scheduler integration with FastAPI startup
- [x] Swagger UI with Bearer token auth

---

## 🚧 In Development

- Automatic hourly scraping (initial implementation, needs refinement)
- Email notifications for new keyword-matching leaks
- Admin dashboard / UI
- Geo-location of IP sources (future)
- Rate-limit handling for scrapers
- Tests & production-ready deployment

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **ORM**: SQLAlchemy with SQLite
- **Auth**: JWT (OAuth2PasswordBearer)
- **Scraping**: httpx + BeautifulSoup
- **Scheduling**: Threaded background tasks on server startup

---

## 📂 Project Structure

