# 🚀 Sathish Farewell Site — Deployment Guide

## 📁 Project Structure

```
farewell-app/
├── app.py              ← Flask backend (API + serves the HTML)
├── requirements.txt    ← Python dependencies
├── farewell.db         ← SQLite database (auto-created on first run)
└── templates/
    └── index.html      ← Your farewell website
```

---

## 💻 Run Locally (Test on Your Machine)

### Step 1 — Install Python dependencies
```bash
cd farewell-app
pip install -r requirements.txt
```

### Step 2 — Start the server
```bash
python app.py
```

You'll see:
```
✅  Database ready: /path/to/farewell.db
🚀  Starting server at http://localhost:5000
```

### Step 3 — Open in browser
Go to → **http://localhost:5000**

Roast & Toast submissions now save to `farewell.db` permanently. ✅

---

## 🌐 Deploy Online (Share with Your Team)

### Option A — Render.com (FREE, recommended)

Render gives you a free Python web server. Perfect for this.

**Step 1** — Push your project to GitHub
```bash
git init
git add .
git commit -m "Sathish farewell site"
# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/farewell-app.git
git push -u origin main
```

**Step 2** — Go to [render.com](https://render.com) → Sign up free

**Step 3** — New → Web Service → Connect your GitHub repo

**Step 4** — Fill in these settings:
| Field | Value |
|---|---|
| Name | sathish-farewell |
| Environment | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python app.py` |
| Instance Type | Free |

**Step 5** — Click **Deploy** → Get a URL like:
`https://sathish-farewell.onrender.com`

Share that link with your 23 teammates! 🎉

---

### Option B — Run on Your Office PC / Laptop

If you just want teammates on the **same network** to access it:

```bash
python app.py
# Server starts on 0.0.0.0:5000
```

Find your local IP:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

Share: **http://YOUR_IP:5000** with your team (must be on same Wi-Fi/VPN)

---

### Option C — PythonAnywhere (FREE)

1. Go to [pythonanywhere.com](https://pythonanywhere.com) → free account
2. Upload your files via the **Files** tab
3. Go to **Web** tab → Add new web app → Flask
4. Set source code path to your `app.py`
5. Your site goes live at `yourusername.pythonanywhere.com`

---

## 🗄️ How the Database Works

- **SQLite file** (`farewell.db`) is created automatically on first run
- Every Roast & Toast submission is saved with: name, type, message, timestamp
- Data persists forever — even after server restarts
- To view all entries directly:

```bash
sqlite3 farewell.db "SELECT * FROM entries;"
```

---

## 🔌 API Endpoints

| Method | URL | What it does |
|---|---|---|
| GET | `/` | Serves the website |
| GET | `/api/entries` | Returns all roast/toast entries as JSON |
| POST | `/api/entries` | Saves a new entry |

### Example POST request (for testing):
```bash
curl -X POST http://localhost:5000/api/entries \
  -H "Content-Type: application/json" \
  -d '{"name":"Pandia","type":"toast","message":"Sathish, best colleague ever!"}'
```

---

## ❓ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| Port 5000 already in use | Change `port=5000` to `port=8080` in `app.py` |
| Entries not showing | Check browser console — is the server running? |
| Render site sleeping | Free tier sleeps after 15min inactivity, wakes in ~30sec on first visit |
