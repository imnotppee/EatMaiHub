# 🍱 EatMaiHub Cheat Sheet

> **Backend:** FastAPI | **Frontend:** Flet | **Database:** PostgreSQL  
> A quick reference for setup, configuration, and testing in local development.

---

## 🏗️ Project Structure

```
EatMaiHub/
├─ backend/              → FastAPI backend (API, Auth, DB models)
├─ frontend/             → Flet UI (mobile-style interface)
├─ Database/             → SQL schema, seed data
├─ Threat Model *.tm7    → DFD & security model files
├─ requirements.txt      → Python dependencies
├─ Requirements.md       → Feature list / design notes
├─ summary.md            → Project summary
```

---

## ⚙️ Setup & Run (Local)

### 🔧 Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# หรือ .venv\Scripts\activate   # Windows

pip install -r ../requirements.txt
uvicorn main:app --reload
```

➡️ **Backend will run at:** [http://localhost:8000](http://localhost:8000)

---

### 🖥️ Frontend (Flet UI)

```bash
cd frontend
flet run main.py
```

➡️ **UI opens in:** your default browser or Flet Desktop Client

---

## 🧰 Developer Tips

### 🗝️ Environment Variables

Create a `.env` file in the **root directory** (same level as `/backend` & `/frontend`)  
Use the following structure ⤵️

```env
# === GOOGLE OAUTH CONFIG ===
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# === APP SECURITY ===
SECRET_KEY=generate_with_openssl_or_python
REDIRECT_URI=http://localhost:8000/auth/google/callback

# === DATABASE CONFIG ===
DATABASE_URL=postgresql://user:password@localhost:5432/eatmaihub
```

> ⚠️ **Important:**  
> - `.env` is listed in `.gitignore` for security reasons.  
> - 🚫 **Do NOT push or share your .env file on GitHub.**  
> - Share only a safe template like `.env.example` with your team.

---

## 🧪 URL for Testing (via Postman)
**Date:** *10/11/2025*

![Test URLs Screenshot](image.png)

---

## 💡 Notes

- Use virtual environments to isolate dependencies.  
- Ensure PostgreSQL is running before starting backend.  
- If OAuth login fails, verify your **Redirect URI** matches Google Cloud settings.  
- For better collaboration: share only `.env.example`, never `.env`.  
- Regularly update dependencies in `requirements.txt` as needed.
- Use Postman or similar tools to test API endpoints.
- DM me on Discord Group if you need help and need env keys!