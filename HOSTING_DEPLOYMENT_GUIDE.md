# MentorBee Class Link Management System
## Production Hosting & Deployment Guide

This guide covers complete, step-by-step instructions to host and deploy the **MentorBee Class Link Management System** across multiple hosting environments:

---

## 🌟 Option 1: One-Click Cloud Hosting (Render.com) — *Recommended (Easiest & Free/Low Cost)*

Render provides free SSL, automated Git deployments, and instant background workers.

### Steps:
1. **Push your repository to GitHub / GitLab**.
2. **Log into [Render.com](https://render.com)**.
3. Click **New +** → **Web Service**.
4. Connect your GitHub repository.
5. Set the following build configuration:
   - **Name**: `mentorbee-meeting-system`
   - **Region**: Singapore or Frankfurt (or nearest to your users)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python bootstrap.py`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables**:
   - `SECRET_KEY`: `<Generate a random 32-character string>`
   - `DATABASE_URL`: `sqlite:///./mentorbee.db` *(or attach a managed PostgreSQL database)*
7. Click **Create Web Service**.
8. Render will build and deploy the app. Once ready, you'll receive your live URL (e.g., `https://mentorbee-meeting-system.onrender.com`).

---

## 🚂 Option 2: Railway.app Hosting

1. Log into [Railway.app](https://railway.app).
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select your repository.
4. Railway will automatically detect the `Procfile` and `requirements.txt`.
5. Add Environment Variables:
   - `SECRET_KEY`: `your_random_secret_key_here`
   - `DATABASE_URL`: `sqlite:///./mentorbee.db`
6. In **Settings** → **Networking**, click **Generate Domain** (or attach your custom domain).
7. Deployment completes automatically!

---

## 🐳 Option 3: Docker & Docker Compose Hosting (Any Cloud VPS / AWS / DigitalOcean)

The project includes a ready-to-run `Dockerfile` and `docker-compose.yml`.

### Quick Launch:
```bash
# 1. Clone or copy project to server
git clone <your-repo-url> /var/www/mentorbee
cd /var/www/mentorbee

# 2. Build and start containers in detached mode
docker compose up -d --build

# 3. View live server logs
docker compose logs -f
```
Your application will be live on `http://<your-server-ip>:8000`.

---

## 💻 Option 4: Linux Cloud VPS Deployment (Ubuntu / Debian + Nginx + SSL + Systemd)

For high performance, full control, and production reliability on AWS EC2, DigitalOcean Droplet, Linode, or Hetzner.

### Step 1: System Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git certbot python3-certbot-nginx
```

### Step 2: Clone & Install
```bash
sudo mkdir -p /var/www/mentorbee
sudo chown -R $USER:$USER /var/www/mentorbee
cd /var/www/mentorbee
git clone <your-repo-url> .

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run initial database and coordinator bootstrap
python bootstrap.py
```

### Step 3: Configure Systemd Service
Create service file `/etc/systemd/system/mentorbee.service`:
```ini
[Unit]
Description=MentorBee Class Link Management System ASGI Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mentorbee
Environment="PATH=/var/www/mentorbee/venv/bin"
Environment="SECRET_KEY=change_this_to_a_secure_random_key_in_production"
Environment="DATABASE_URL=sqlite:////var/www/mentorbee/mentorbee.db"
ExecStart=/var/www/mentorbee/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo chown -R www-data:www-data /var/www/mentorbee
sudo systemctl daemon-reload
sudo systemctl start mentorbee
sudo systemctl enable mentorbee
```

### Step 4: Configure Nginx Reverse Proxy with WebSocket Support
Create `/etc/nginx/sites-available/mentorbee`:
```nginx
server {
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket endpoint support for live real-time sync
    location /ws/ {
        proxy_pass http://127.0.0.1:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site & reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/mentorbee /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Install Free Automated SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🪟 Option 5: Windows Server / Local Network Deployment

1. Install Python 3.10+ on the Windows machine (ensure "Add Python to PATH" is checked).
2. Open PowerShell or Command Prompt in the project directory:
   ```cmd
   pip install -r requirements.txt
   ```
3. Double-click or run:
   ```cmd
   run.bat
   ```
4. Access via browser:
   - Local: `http://localhost:8000`
   - LAN / WiFi: `http://<your-local-ip>:8000`

---

## 🔍 Verification & Health Check

After deployment, test the health endpoint:
```bash
curl http://your-domain.com/health
```
Response:
```json
{
  "status": "healthy",
  "service": "MentorBee Class Link Management System",
  "version": "1.0.0"
}
```
